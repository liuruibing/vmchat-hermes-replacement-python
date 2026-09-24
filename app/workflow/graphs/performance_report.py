from __future__ import annotations

import inspect
import json
import os
from typing import Any, AsyncGenerator, Dict, List

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


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _usage_dict(value: Any) -> Dict[str, int]:
    result = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    _add_usage(result, value)
    return result


def _issue_to_dict(issue: Any) -> Dict[str, Any]:
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

    def _compile(self, context: WorkflowContext):
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

        async def generate(state: PerformanceReportGraphState) -> Dict[str, Any]:
            if _is_aborted(signal):
                raise ClientDisconnectedError("CLIENT_DISCONNECTED: Execution aborted during generation")

            max_prompt_chars = int(os.environ.get("MAX_PROMPT_CHARS", "120000"))
            sys_prompt, user_prompt = _call_build_generate_prompt(
                input_val,
                skill_md,
                context.role_prompt,
            )
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
            stream = run_skill(
                ModelSkillRunInput(
                    system_prompt=sys_prompt,
                    user_prompt=user_prompt,
                    read_resource=lambda path: reader.read(path),
                    search_knowledge=context.knowledge_search,
                    signal=signal,
                )
            )

            if hasattr(stream, "__aiter__"):
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
            return update

        def route_after_generate(state: PerformanceReportGraphState) -> str:
            return "finalize_text" if state.get("result_type") == "text" else "validate"

        async def validate(state: PerformanceReportGraphState) -> Dict[str, Any]:
            existing_errors = state.get("validation_errors") or []
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
            if state.get("validation_ok"):
                return "finalize_dsl"
            if int(state.get("repair_attempts") or 0) >= MAX_DSL_REPAIR_ATTEMPTS:
                return "failed"
            return "repair"

        async def repair(state: PerformanceReportGraphState) -> Dict[str, Any]:
            if _is_aborted(signal):
                raise ClientDisconnectedError("CLIENT_DISCONNECTED: Execution aborted during repair")

            errors = [_dict_to_issue(item) for item in (state.get("validation_errors") or [])]
            sys_prompt, user_prompt = _call_build_repair_prompt(
                state.get("candidate"),
                errors,
                input_val,
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
            response = generate_fn(request)
            if inspect.isawaitable(response):
                response = await response

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
            text = str(state.get("final_text") or "")
            max_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
            if len(text) > max_chars:
                raise VmChatRunError(
                    "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
                    f"生成的文本长度 ({len(text)}) 超过上限 ({max_chars})",
                )
            return {"final_text": text}

        async def finalize_dsl(state: PerformanceReportGraphState) -> Dict[str, Any]:
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
            return {
                "error_code": "DSL_REPAIR_EXHAUSTED",
                "error_message": "AI 助手生成的报表格式无法自动修复，请调整描述后重试",
            }

        builder = StateGraph(PerformanceReportGraphState)
        builder.add_node("generate", generate)
        builder.add_node("validate", validate)
        builder.add_node("repair", repair)
        builder.add_node("finalize_text", finalize_text)
        builder.add_node("finalize_dsl", finalize_dsl)
        builder.add_node("failed", failed)

        builder.add_edge(START, "generate")
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
        builder.add_edge("repair", "validate")
        builder.add_edge("finalize_text", END)
        builder.add_edge("finalize_dsl", END)
        builder.add_edge("failed", END)
        return builder.compile()

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        try:
            graph = self._compile(context)
            result = await graph.ainvoke(
                {
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
                }
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

        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        final_text = str(result.get("final_text") or "")
        if not final_text:
            yield RunFailedEvent(error="AI 助手未生成有效内容")
            return

        chunk_size = max(64, int(context.message_chunk_chars or 256))
        for chunk in code_point_chunks(final_text, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        yield RunCompletedEvent(
            output=final_text,
            usage=result.get("usage") or {},
        )
