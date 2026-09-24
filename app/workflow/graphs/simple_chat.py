from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, List

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
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _history_payload(context: WorkflowContext) -> List[Dict[str, str]]:
    return [
        {"role": item.role, "content": item.content}
        for item in context.input_val.historyMessages
    ]


def _build_user_prompt(state: SimpleChatGraphState) -> str:
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
        self._checkpointer = InMemorySaver()

    def _compile(self, context: WorkflowContext):
        async def retrieve_knowledge(
            state: SimpleChatGraphState,
        ) -> Dict[str, Any]:
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}
            search = context.knowledge_search
            if not callable(search):
                return {"knowledge_context": ""}
            try:
                result = search(str(state.get("user_message") or ""))
                if hasattr(result, "__await__"):
                    result = await result
                return {"knowledge_context": str(result or "")}
            except Exception:
                # Knowledge retrieval is useful but not allowed to make a basic
                # conversation unavailable.
                return {"knowledge_context": ""}

        async def answer(state: SimpleChatGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            role_prompt = context.role_prompt.strip() if context.role_prompt else ""
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
            stream = run_skill(run_input)

            if hasattr(stream, "__aiter__"):
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
                for chunk in stream:
                    delta = getattr(chunk, "contentDelta", None) or getattr(
                        chunk, "content_delta", None
                    )
                    if delta:
                        answer_parts.append(str(delta))
                    chunk_usage = getattr(chunk, "usage", None)
                    if chunk_usage:
                        usage = dict(chunk_usage) if isinstance(chunk_usage, dict) else usage

            answer_text = "".join(answer_parts).strip()
            if not answer_text:
                return {"error": "AI 助手未生成有效内容"}
            return {
                "answer": answer_text,
                "reasoning": reasoning,
                "usage": usage,
            }

        builder = StateGraph(SimpleChatGraphState)
        builder.add_node("retrieve_knowledge", retrieve_knowledge)
        builder.add_node("answer", answer)
        builder.add_edge(START, "retrieve_knowledge")
        builder.add_edge("retrieve_knowledge", "answer")
        builder.add_edge("answer", END)
        return builder.compile(checkpointer=self._checkpointer)

    async def stream(
        self,
        context: WorkflowContext,
    ) -> AsyncGenerator[Any, None]:
        graph = self._compile(context)
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
            thread_id = context.run_id or context.session_id or "simple-chat"
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

        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        answer = str(result.get("answer") or "")
        chunk_size = max(64, int(context.message_chunk_chars or 256))
        for chunk in code_point_chunks(answer, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        yield RunCompletedEvent(
            output=answer,
            usage=result.get("usage") or {},
        )
