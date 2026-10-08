# ==============================================================================
# 文件：app/workflow/graphs/performance_report.py
# 文件作用：生成报表 DSL（JSON 配置），并组织校验、自动修复和最终输出。
# 全局位置：main.py → Engine（vm-report）→ 本文件的图 → Provider / Python 业务校验器。
# 谁调用它：legacy.py 注册实例，WorkflowEngine 按 vm-report id 调用 stream(context)。
# 输入：用户报表要求、现有报表、指标/资源目录、角色规则、知识检索回调及 Provider。
# 输出：文字答复或校验后的 DSL，以及过程说明、用量和完成/失败事件。
# 主要流程：解析语义 → 生成 → 文字直接输出 / DSL 校验 → 通过输出 / 修复后重校验 / 次数耗尽失败。
# 前端类比：像带校验和重试的表单提交流程；state 保存候选配置、错误和修复次数。
# 边界：模型生成候选，Python 判断业务规则；LangGraph 按判断结果走分支，不自动保证配置正确。
# 阅读入口：先看 StateGraph 连线与 route_validation()，再看 generate/validate/repair 和 stream。
# ==============================================================================

from __future__ import annotations

import inspect
import json
import os
from typing import Any, AsyncGenerator, Dict, List

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.compatibility.hermes_events import (
    ClientDisconnectedError,
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.contracts.types import ValidationIssue, VmChatRunError
from app.orchestrator.vmchat_orchestrator import (
    MAX_DSL_REPAIR_ATTEMPTS,
    _add_usage,
    _call_build_generate_prompt,
    _call_build_repair_prompt,
    _call_validate_vm_report_dsl_set,
    _classify_model_output,
)
from app.provider.fixed_provider import ModelGenerateInput, ModelSkillRunInput
from app.resources.skill_resource_reader import SkillResourceReader, SkillResourceReaderOptions
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.performance_report_state import PerformanceReportGraphState
from app.workflow.graphs.performance_semantics import build_semantic_plan, resolve_metrics


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _usage_dict(value: Any) -> Dict[str, int]:
    # 把不同 Provider 的用量对象转成同一种字典，后面的修复调用才能继续累计。
    result = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    _add_usage(result, value)
    return result


def _issue_to_dict(issue: Any) -> Dict[str, Any]:
    # model_dump 是 Pydantic 对象转字典的方法；图 state 中保存可记录的普通数据。
    if hasattr(issue, "model_dump"):
        return issue.model_dump(exclude_none=True)
    if isinstance(issue, dict):
        return dict(issue)
    return {
        "code": str(getattr(issue, "code", "VALIDATION_ERROR")),
        "path": str(getattr(issue, "path", "/")),
        "message": str(getattr(issue, "message", issue)),
    }


def _dict_to_issue(item: Dict[str, Any]) -> ValidationIssue:
    return ValidationIssue(
        code=str(item.get("code") or "VALIDATION_ERROR"),
        path=str(item.get("path") or "/"),
        message=str(item.get("message") or "DSL 校验失败"),
    )


def _current_block_ids(context: WorkflowContext) -> List[str]:
    ids: List[str] = []
    for item in context.input_val.currentDsls or []:
        block_id = getattr(item, "blockId", None) or getattr(item, "id", None)
        if block_id:
            ids.append(str(block_id))
    return ids


def _resource_context(context: WorkflowContext, paths: List[str]) -> Dict[str, str]:
    # 只取生成时实际读过的资料交给修复步骤，避免重新塞入整份资源库。
    resources = context.resources
    resource_map = getattr(resources, "toolResourceTextByPath", None) or getattr(
        resources, "tool_resource_text_by_path", None
    )
    if not isinstance(resource_map, dict):
        return {}
    return {
        path: str(resource_map[path])
        for path in paths
        if path in resource_map
    }


class PerformanceReportLangGraphWorkflow:
    """LangGraph implementation of the existing vm-report workflow.

    Runtime-owned Session/Context/Knowledge/Artifact services remain outside the
    graph. The graph only orchestrates one bounded report-generation run.
    """

    id = "vm-report"

    def __init__(self) -> None:
        # 内存检查点保存图执行状态；服务重启会丢失，不承担会话和产物的长期存储。
        self._checkpointer = InMemorySaver()

    def _compile(self, context: WorkflowContext):
        # 节点是嵌套函数，可通过闭包访问本次 context；state 只放节点间需要传递的数据。
        if context.resources is None:
            raise VmChatRunError(
                "SERVICE_DEGRADED",
                "当前 Agent 资源尚未加载完成",
            )

        resources = context.resources
        input_val = context.input_val
        provider = context.provider
        signal = context.signal
        skill_md = getattr(resources, "skillMd", None) or getattr(resources, "skill_md", "")
        current_block_ids = _current_block_ids(context)

        async def resolve_semantics(_state: PerformanceReportGraphState) -> Dict[str, Any]:
            # 先用 Python 根据用户措辞和资源目录解析指标、制定语义计划，此步骤不调用模型。
            metrics = resolve_metrics(input_val.userMessage, resources)
            plan = build_semantic_plan(metrics, resources)
            return {
                "resolved_metrics": metrics,
                "semantic_plan": plan,
            }

        def enriched_input(state: PerformanceReportGraphState):
            # model_copy(update=...) 类似 {...input, resolvedMetrics: ...}，生成新输入对象。
            return input_val.model_copy(
                update={
                    "resolvedMetrics": state.get("resolved_metrics") or [],
                    "semanticPlan": state.get("semantic_plan") or {},
                }
            )

        async def generate(state: PerformanceReportGraphState) -> Dict[str, Any]:
            # 节点一：生成候选。先检查取消信号，再准备 Prompt 和模型可读取的受控资源。
            if _is_aborted(signal):
                raise ClientDisconnectedError("CLIENT_DISCONNECTED: Execution aborted during generation")

            max_prompt_chars = int(os.environ.get("MAX_PROMPT_CHARS", "120000"))
            run_input_val = enriched_input(state)
            sys_prompt, user_prompt = _call_build_generate_prompt(
                run_input_val,
                skill_md,
                context.role_prompt,
            )
            # resource reader 是工具回调的执行方，负责路径和上下文额度限制。
            reader = SkillResourceReader(
                resources,
                SkillResourceReaderOptions(
                    maxContextChars=max_prompt_chars,
                    initialContextChars=len(sys_prompt) + len(user_prompt),
                    maxResourceChars=int(os.environ.get("MAX_RESOURCE_CONTEXT_CHARS", "40000")),
                ),
            )

            run_skill = getattr(provider, "run_skill", None) or getattr(provider, "runSkill", None)
            if run_skill is None:
                raise RuntimeError("Provider does not have runSkill or run_skill method")

            answer_parts: List[str] = []
            reasoning: List[str] = []
            run_usage: Any = None
            # 工作流不知道模型厂商，只调 Provider；LangChain 的 bind_tools/模型循环在适配器内。
            stream = run_skill(
                ModelSkillRunInput(
                    system_prompt=sys_prompt,
                    user_prompt=user_prompt,
                    # lambda 类似 path => reader.read(path)；模型发出请求后由 Provider 调用。
                    read_resource=lambda path: reader.read(path),
                    search_knowledge=context.knowledge_search,
                    signal=signal,
                )
            )

            if hasattr(stream, "__aiter__"):
                # Provider 返回异步迭代对象时，async for 等待每个片段，先收集到列表中。
                async for chunk in stream:
                    if _is_aborted(signal):
                        raise ClientDisconnectedError("CLIENT_DISCONNECTED: Execution aborted during generation")
                    r_delta = getattr(chunk, "reasoningDelta", None) or getattr(chunk, "reasoning_delta", None)
                    if r_delta:
                        reasoning.append(str(r_delta))
                    delta = getattr(chunk, "contentDelta", None) or getattr(chunk, "content_delta", None)
                    if delta:
                        answer_parts.append(str(delta))
                    usage = getattr(chunk, "usage", None)
                    if usage:
                        run_usage = usage
            else:
                # 兼容同步的测试实现；不把每种 Provider 都强制写成同一种底层客户端。
                for chunk in stream:
                    delta = getattr(chunk, "contentDelta", None) or getattr(chunk, "content_delta", None)
                    if delta:
                        answer_parts.append(str(delta))
                    usage = getattr(chunk, "usage", None)
                    if usage:
                        run_usage = usage

            raw_output = "".join(answer_parts).strip()
            if not raw_output:
                raise VmChatRunError("EMPTY_MODEL_OUTPUT", "AI 助手未生成有效内容，请重试")

            # 先区分文字和 DSL，并解析候选；“能解析成 JSON”不代表“符合报表业务规则”。
            classified = _classify_model_output(raw_output)
            update: Dict[str, Any] = {
                "raw_output": raw_output,
                "reasoning": reasoning,
                "usage": _usage_dict(run_usage),
                "read_resource_paths": list(reader.get_read_resources().keys()),
                "attempt_count": 1,
                "repair_attempts": 0,
            }
            if classified["kind"] == "text":
                update.update(
                    {
                        "result_type": "text",
                        "final_text": str(classified.get("text") or raw_output),
                        "validation_ok": True,
                    }
                )
            else:
                update.update(
                    {
                        "result_type": "dsl",
                        "candidate": classified.get("candidate"),
                        "validation_errors": [
                            _issue_to_dict(issue)
                            for issue in (classified.get("issues") or [])
                        ],
                        "candidate_dirty": not bool(classified.get("issues")),
                        "validation_ok": False,
                    }
                )
            # 节点返回局部 state 更新；未返回的字段保留，返回的同名字段覆盖原值。
            return update

        def route_after_generate(state: PerformanceReportGraphState) -> str:
            # 路由函数返回下一站的名称；文字答复不必走报表 DSL 校验。
            return "finalize_text" if state.get("result_type") == "text" else "validate"

        async def validate(state: PerformanceReportGraphState) -> Dict[str, Any]:
            # 节点二：由 Python 校验器检查配置；模型不能自己宣布“校验通过”。
            existing_errors = state.get("validation_errors") or []
            # 内容未变化且已有错误时保留失败状态，等待修复，避免重复校验同一份无效候选。
            if existing_errors and not state.get("candidate_dirty", True):
                return {"validation_ok": False}

            result = _call_validate_vm_report_dsl_set(
                state.get("candidate"),
                resources,
                current_block_ids,
            )
            if getattr(result, "ok", False):
                dsls = getattr(result, "dsls", []) or []
                return {
                    "validation_ok": True,
                    "validation_errors": [],
                    "validated_dsls": [
                        item.model_dump(exclude_none=True)
                        if hasattr(item, "model_dump")
                        else item
                        for item in dsls
                    ],
                    "candidate_dirty": False,
                }
            return {
                "validation_ok": False,
                "validation_errors": [
                    _issue_to_dict(issue)
                    for issue in (getattr(result, "errors", []) or [])
                ],
                "candidate_dirty": False,
            }

        def route_validation(state: PerformanceReportGraphState) -> str:
            # 类似根据表单校验结果选择页面下一步：通过就输出，次数用尽就失败，否则修复。
            if state.get("validation_ok"):
                return "finalize_dsl"
            if int(state.get("repair_attempts") or 0) >= MAX_DSL_REPAIR_ATTEMPTS:
                return "failed"
            return "repair"

        async def repair(state: PerformanceReportGraphState) -> Dict[str, Any]:
            # 节点三：把具体错误和旧候选放入修复 Prompt，再次请求模型；修完仍需 Python 重校验。
            if _is_aborted(signal):
                raise ClientDisconnectedError("CLIENT_DISCONNECTED: Execution aborted during repair")

            errors = [_dict_to_issue(item) for item in (state.get("validation_errors") or [])]
            sys_prompt, user_prompt = _call_build_repair_prompt(
                state.get("candidate"),
                errors,
                enriched_input(state),
                _resource_context(context, state.get("read_resource_paths") or []),
                skill_md,
            )

            generate_fn = getattr(provider, "generate", None)
            if generate_fn is None:
                raise RuntimeError("Provider does not have generate method")

            request = ModelGenerateInput(
                system_prompt=sys_prompt,
                user_prompt=user_prompt,
                signal=signal,
                purpose="repair",
            )
            # generate 与生成节点的 run_skill 不同：这里要一次完整的结构化修复结果。
            response = generate_fn(request)
            if inspect.isawaitable(response):
                # 类似判断是否需要 await Promise；也兼容直接返回结果的同步测试 Provider。
                response = await response

            # dict(...) 先复制旧字典，再累计本轮用量并返回，避免直接改动已有 state 中的对象。
            usage = dict(state.get("usage") or {})
            _add_usage(usage, getattr(response, "usage", None) or (
                response.get("usage") if isinstance(response, dict) else None
            ))

            repair_result = getattr(response, "result", None) or (
                response.get("result") if isinstance(response, dict) else None
            )
            result_type = getattr(repair_result, "type", None) or (
                repair_result.get("type") if isinstance(repair_result, dict) else None
            )

            repair_attempts = int(state.get("repair_attempts") or 0) + 1
            attempt_count = int(state.get("attempt_count") or 1) + 1
            if result_type == "text":
                # 这一步要求修复 DSL，返回文字也算失败；尝试次数仍增加，防止无限循环。
                return {
                    "usage": usage,
                    "repair_attempts": repair_attempts,
                    "attempt_count": attempt_count,
                    "validation_ok": False,
                    "candidate_dirty": False,
                    "validation_errors": [
                        {
                            "code": "REPAIR_DSL_REQUIRED",
                            "path": "/",
                            "message": "修复请求必须返回 DSL JSON",
                        }
                    ],
                }

            candidate = getattr(repair_result, "dsl", None) or (
                repair_result.get("dsl") if isinstance(repair_result, dict) else None
            )
            # 新候选被标记为 dirty，下一次 validate 必须重新检查它。
            return {
                "candidate": candidate,
                "usage": usage,
                "repair_attempts": repair_attempts,
                "attempt_count": attempt_count,
                "validation_errors": [],
                "validation_ok": False,
                "candidate_dirty": True,
            }

        async def finalize_text(state: PerformanceReportGraphState) -> Dict[str, Any]:
            # 输出前检查字符上限；环境变量读出来是字符串，所以先 int(...) 转数字。
            text = str(state.get("final_text") or "")
            max_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
            if len(text) > max_chars:
                raise VmChatRunError(
                    "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
                    f"生成的文本长度 ({len(text)}) 超过上限 ({max_chars})",
                )
            return {"final_text": text}

        async def finalize_dsl(state: PerformanceReportGraphState) -> Dict[str, Any]:
            # JSON 序列化类似 JSON.stringify；单块和多块报表分别保持对象/数组形状。
            candidate = state.get("candidate")
            dsls = state.get("validated_dsls") or []
            is_array_candidate = isinstance(candidate, list) or len(dsls) > 1
            if is_array_candidate:
                final_text = json.dumps(dsls, indent=2, ensure_ascii=False)
            else:
                first = dsls[0] if dsls else candidate
                final_text = json.dumps(first, indent=2, ensure_ascii=False)

            max_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
            if len(final_text) > max_chars:
                raise VmChatRunError(
                    "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
                    f"生成的 DSL 长度 ({len(final_text)}) 超过上限 ({max_chars})",
                )
            return {"final_text": final_text, "result_type": "dsl"}

        async def failed(_state: PerformanceReportGraphState) -> Dict[str, Any]:
            # “失败节点”也是普通函数：把错误写进 state，外层 stream 再转成失败事件。
            return {
                "error_code": "DSL_REPAIR_EXHAUSTED",
                "error_message": "AI 助手生成的报表格式无法自动修复，请调整描述后重试",
            }

        # 定义图：add_node 绑定名字与函数；此时只是登记，不会立即执行函数。
        builder = StateGraph(PerformanceReportGraphState)
        builder.add_node("resolve_semantics", resolve_semantics)
        builder.add_node("generate", generate)
        builder.add_node("validate", validate)
        builder.add_node("repair", repair)
        builder.add_node("finalize_text", finalize_text)
        builder.add_node("finalize_dsl", finalize_dsl)
        builder.add_node("failed", failed)

        # 固定边规定先后顺序；START / END 是图的虚拟节点，不是启动/关闭 Python 服务。
        builder.add_edge(START, "resolve_semantics")
        builder.add_edge("resolve_semantics", "generate")
        # 条件边：源节点执行后，调用路由函数，用返回值查后面的“返回值 → 目标节点”映射。
        builder.add_conditional_edges(
            "generate",
            route_after_generate,
            {"finalize_text": "finalize_text", "validate": "validate"},
        )
        builder.add_conditional_edges(
            "validate",
            route_validation,
            {
                "finalize_dsl": "finalize_dsl",
                "repair": "repair",
                "failed": "failed",
            },
        )
        # 这条回边形成修复循环；route_validation 中的修复次数上限让循环有终点。
        builder.add_edge("repair", "validate")
        builder.add_edge("finalize_text", END)
        builder.add_edge("finalize_dsl", END)
        builder.add_edge("failed", END)
        # compile 返回可运行对象，检查点供图记录状态；真正的执行在下面 ainvoke 中开始。
        return builder.compile(checkpointer=self._checkpointer)

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        try:
            graph = self._compile(context)
            # thread_id 是检查点的逻辑标识，不是线程；优先使用本次 run_id 隔离任务。
            thread_id = context.run_id or context.session_id or "vm-report"
            # await 类似等待 Promise；ainvoke 一直等到图结束，再返回最终 state。
            result = await graph.ainvoke(
                {
                    "resolved_metrics": [],
                    "semantic_plan": {},
                    "reasoning": [],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": 0,
                        "total_tokens": 0,
                    },
                    "read_resource_paths": [],
                    "attempt_count": 1,
                    "repair_attempts": 0,
                    "validation_errors": [],
                    "validation_ok": False,
                    "candidate_dirty": True,
                    "error_code": "",
                    "error_message": "",
                },
                config={"configurable": {"thread_id": thread_id}},
            )
        except VmChatRunError as err:
            message = getattr(err, "public_message", None) or getattr(err, "publicMessage", None) or str(err)
            yield RunFailedEvent(error=message)
            return
        except Exception as err:
            yield RunFailedEvent(error=f"AI 助手任务执行失败: {err}")
            return

        if result.get("error_message"):
            yield RunFailedEvent(error=str(result["error_message"]))
            return

        # 下面才开始 yield 业务事件。内部模型用了流式调用，也不代表浏览器实时看到那些片段。
        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        final_text = str(result.get("final_text") or "")
        if not final_text:
            yield RunFailedEvent(error="AI 助手未生成有效内容")
            return

        chunk_size = max(64, int(context.message_chunk_chars or 256))
        for chunk in code_point_chunks(final_text, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        # main.py 将完成事件转成 SSE 并保存结果；这里同时给出完整正文和所有调用的累计用量。
        yield RunCompletedEvent(
            output=final_text,
            usage=result.get("usage") or {},
        )
