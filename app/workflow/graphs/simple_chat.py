# ==============================================================================
# 文件：app/workflow/graphs/simple_chat.py
# 文件作用：实现最简单的聊天工作流，先检索当前 Agent 的知识，再让模型回答问题。
# 全局位置：main.py → Engine（simple-chat）→ 本文件的图 → context.provider → 模型服务。
# 谁调用它：legacy.py 注册实例，WorkflowEngine 按 simple-chat id 调用 stream(context)。
# 输入：WorkflowContext 中的用户问题、历史摘要、角色/Skill、检索回调、Provider 和取消信号。
# 输出：过程说明、回答片段、完成或失败事件；最终结果包含完整答案与用量。
# 主要流程：START → retrieve_knowledge（Python 检索）→ answer（Provider 调模型）→ END。
# 前端类比：图像有顺序的任务流程；state 像本次任务的 store，节点返回类似 patch 的局部更新。
# 边界：LangGraph 管步骤和状态，Provider 管模型调用；ainvoke 完成后才向外发送结果片段。
# 阅读入口：先看 _compile() 末尾的节点/连线，再看两个节点函数，最后看 stream()。
# ==============================================================================

from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, List

# InMemorySaver 保存图检查点；StateGraph 构建流程，START / END 是虚拟起止节点。
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.provider.fixed_provider import ModelSkillRunInput
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.simple_chat_state import SimpleChatGraphState


def _is_aborted(signal: Any) -> bool:
    # getattr 类似可选属性读取；兼容 controller.aborted 和 controller.signal.aborted 两种形状。
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _history_payload(context: WorkflowContext) -> List[Dict[str, str]]:
    # 列表推导式 [表达式 for item in 列表]，类似 JS 的 history.map(item => ({...}))。
    return [
        {"role": item.role, "content": item.content}
        for item in context.input_val.historyMessages
    ]


def _build_user_prompt(state: SimpleChatGraphState) -> str:
    # 把摘要、历史、检索资料、本次问题拼成模型输入；标签用于分隔内容，并不会执行 HTML。
    parts: List[str] = []
    summary = str(state.get("session_summary") or "").strip()
    if summary:
        parts.append(f"<session_summary>\n{summary}\n</session_summary>")

    history = state.get("history") or []
    if history:
        history_lines = ["<chat_history>"]
        for item in history:
            history_lines.append(
                f"{str(item.get('role') or '')}: {str(item.get('content') or '')}"
            )
        history_lines.append("</chat_history>")
        parts.append("\n".join(history_lines))

    knowledge = str(state.get("knowledge_context") or "").strip()
    if knowledge and knowledge != "KNOWLEDGE_NOT_FOUND":
        parts.append(
            "<retrieved_knowledge>\n"
            + knowledge
            + "\n</retrieved_knowledge>"
        )

    parts.append(
        "<user_request>\n"
        + str(state.get("user_message") or "")
        + "\n</user_request>"
    )
    return "\n\n".join(parts)


class SimpleChatLangGraphWorkflow:
    id = "simple-chat"

    def __init__(self) -> None:
        # self 类似 JS 的 this；检查点仅在当前进程内存中，会话的长期存储由外部服务负责。
        self._checkpointer = InMemorySaver()

    def _compile(self, context: WorkflowContext):
        # 嵌套函数形成闭包：节点拿到 state，同时可以访问本次 context 中的 provider 和检索回调。
        # 节点返回的是 state 的局部更新，类似 store.patch({knowledge_context: ...})。
        async def retrieve_knowledge(
            state: SimpleChatGraphState,
        ) -> Dict[str, Any]:
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}
            search = context.knowledge_search
            # callable 判断是否可调用；检索由 Python KnowledgeService 提供，不是图自带的知识库。
            if not callable(search):
                return {"knowledge_context": ""}
            try:
                result = search(str(state.get("user_message") or ""))
                # 同时兼容同步结果和可 await 的结果；await 等待期间不会独占事件循环。
                if hasattr(result, "__await__"):
                    result = await result
                return {"knowledge_context": str(result or "")}
            except Exception:
                # Knowledge retrieval is useful but not allowed to make a basic
                # conversation unavailable.
                return {"knowledge_context": ""}

        async def answer(state: SimpleChatGraphState) -> Dict[str, Any]:
            # 固定边仍会进入这个节点；若上一步写入 error，直接返回空更新，不再调用模型。
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            role_prompt = context.role_prompt.strip() if context.role_prompt else ""
            # system_prompt 提供角色和规则；user_prompt 携带用户问题及前面检索得到的上下文。
            system_prompt = "\n".join(
                [
                    role_prompt or "你是一个企业领域 AI 助手。",
                    "你必须优先依据当前 Agent Skill 与检索到的知识作答。",
                    "检索结果已经由 Python KnowledgeService 选取；不要要求读取整份知识库。",
                    "不要编造知识库中不存在的业务事实；证据不足时明确说明需要更多资料。",
                    "",
                    "# Agent Skill",
                    context.skill_md or "按用户要求提供准确、简洁的回答。",
                ]
            )
            user_prompt = _build_user_prompt(state)

            run_skill = getattr(context.provider, "run_skill", None) or getattr(
                context.provider, "runSkill", None
            )
            if run_skill is None:
                return {"error": "AI Provider 不支持 Skill 运行"}

            # lambda 类似箭头函数。知识已经预检索，此处禁止额外读资源，也不再提供检索工具。
            run_input = ModelSkillRunInput(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
                search_knowledge=None,
                signal=context.signal,
            )

            answer_parts: List[str] = []
            reasoning: List[str] = []
            usage: Dict[str, Any] = {}
            # 返回生成器，类似 AsyncIterable；调用后由下面的循环驱动它，不是一次拿到完整答案。
            stream = run_skill(run_input)

            if hasattr(stream, "__aiter__"):
                # async for 逐块等待模型输出；此处先收集，尚未 yield 给浏览器。
                async for chunk in stream:
                    if _is_aborted(context.signal):
                        return {"error": "客户端连接已中断"}
                    r_delta = getattr(chunk, "reasoningDelta", None) or getattr(
                        chunk, "reasoning_delta", None
                    )
                    if r_delta:
                        reasoning.append(str(r_delta))
                    delta = getattr(chunk, "contentDelta", None) or getattr(
                        chunk, "content_delta", None
                    )
                    if delta:
                        answer_parts.append(str(delta))
                    chunk_usage = getattr(chunk, "usage", None)
                    if chunk_usage:
                        usage = dict(chunk_usage) if isinstance(chunk_usage, dict) else {
                            "prompt_tokens": int(getattr(chunk_usage, "prompt_tokens", 0) or 0),
                            "completion_tokens": int(getattr(chunk_usage, "completion_tokens", 0) or 0),
                            "total_tokens": int(getattr(chunk_usage, "total_tokens", 0) or 0),
                        }
            else:
                # 测试 Provider 等实现也可以返回普通可迭代对象，使用同步 for 消费。
                for chunk in stream:
                    delta = getattr(chunk, "contentDelta", None) or getattr(
                        chunk, "content_delta", None
                    )
                    if delta:
                        answer_parts.append(str(delta))
                    chunk_usage = getattr(chunk, "usage", None)
                    if chunk_usage:
                        usage = dict(chunk_usage) if isinstance(chunk_usage, dict) else usage

            # 类似 answerParts.join('')；所有片段拼好后，一次更新答案、过程说明和用量。
            answer_text = "".join(answer_parts).strip()
            if not answer_text:
                return {"error": "AI 助手未生成有效内容"}
            return {
                "answer": answer_text,
                "reasoning": reasoning,
                "usage": usage,
            }

        # StateGraph 接收状态的类型；add_node 注册“节点名 → 函数”，不会在这里执行函数。
        builder = StateGraph(SimpleChatGraphState)
        builder.add_node("retrieve_knowledge", retrieve_knowledge)
        builder.add_node("answer", answer)
        # add_edge 定义固定顺序；与 Promise.then 链相似，但中间数据统一通过 state 传递。
        builder.add_edge(START, "retrieve_knowledge")
        builder.add_edge("retrieve_knowledge", "answer")
        builder.add_edge("answer", END)
        # compile 将定义变成可执行的图，并接入内存检查点；此时仍没有调用模型。
        return builder.compile(checkpointer=self._checkpointer)

    async def stream(
        self,
        context: WorkflowContext,
    ) -> AsyncGenerator[Any, None]:
        graph = self._compile(context)
        # 本次执行的初始 store；历史和摘要由 Runtime 提供，不由 InMemorySaver 自动补齐。
        initial: SimpleChatGraphState = {
            "user_message": context.input_val.userMessage,
            "session_summary": context.input_val.sessionSummary or "",
            "history": _history_payload(context),
            "knowledge_context": "",
            "answer": "",
            "reasoning": [],
            "usage": {},
            "error": "",
        }

        try:
            # thread_id 是检查点分组标识，不是 Python 线程；这里优先使用独立的 run_id。
            thread_id = context.run_id or context.session_id or "simple-chat"
            # ainvoke 等整张图跑完，result 是最终 state；这里没用图的 astream 逐步转发。
            result = await graph.ainvoke(
                initial,
                config={"configurable": {"thread_id": thread_id}},
            )
        except Exception as err:
            yield RunFailedEvent(error=f"AI 助手任务执行失败: {err}")
            return

        if result.get("error"):
            yield RunFailedEvent(error=str(result["error"]))
            return

        # enumerate(..., start=1) 类似带索引的遍历，从 1 编号后交给前端按顺序展示。
        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        answer = str(result.get("answer") or "")
        chunk_size = max(64, int(context.message_chunk_chars or 256))
        # yield 类似 async function* 的 yield：交出一个事件，调用方再读取时继续往下执行。
        # 这些片段是图完成后的答案拆分，不能据此认为前端实时收到了模型 token。
        for chunk in code_point_chunks(answer, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        # 完成事件携带完整输出与用量，main.py 会负责保存任务结果并序列化为 SSE。
        yield RunCompletedEvent(
            output=answer,
            usage=result.get("usage") or {},
        )
