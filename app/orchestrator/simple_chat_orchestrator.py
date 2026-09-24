from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, Optional, Union

from app.compatibility.hermes_events import RunCompletedEvent
from app.compatibility.hermes_request import VmChatInput
from app.orchestrator.vmchat_orchestrator import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunFailedEvent,
    _is_aborted,
)
from app.provider.fixed_provider import ModelSkillRunInput


async def stream_simple_chat(
    *,
    input_val: VmChatInput,
    provider: Any,
    skill_md: str,
    role_prompt: str = "",
    knowledge_search: Optional[Any] = None,
    signal: Optional[Any] = None,
    message_chunk_chars: int = 256,
) -> AsyncGenerator[Any, None]:
    system_prompt = "\n".join(
        [
            role_prompt.strip() if role_prompt else "你是一个企业领域 AI 助手。",
            "你必须优先依据当前 Agent Skill 与检索到的知识作答。",
            "若 search_agent_knowledge 工具可用，涉及知识库事实时先检索再回答。",
            "不要编造知识库中不存在的业务事实；证据不足时明确说明需要更多资料。",
            "",
            "# Agent Skill",
            skill_md or "按用户要求提供准确、简洁的回答。",
        ]
    )

    history_lines = []
    if input_val.sessionSummary:
        history_lines.append(f"<session_summary>\n{input_val.sessionSummary}\n</session_summary>")
    if input_val.historyMessages:
        history_lines.append("<chat_history>")
        for item in input_val.historyMessages:
            history_lines.append(f"{item.role}: {item.content}")
        history_lines.append("</chat_history>")
    history_lines.extend(
        [
            "<user_request>",
            input_val.userMessage,
            "</user_request>",
        ]
    )
    user_prompt = "\n".join(history_lines)

    run_skill = getattr(provider, "run_skill", None) or getattr(provider, "runSkill", None)
    if run_skill is None:
        yield RunFailedEvent(error="AI Provider 不支持 Skill 运行")
        return

    visible_output = ""
    usage: Dict[str, Any] = {}
    reasoning_seq = 0

    run_input = ModelSkillRunInput(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
        search_knowledge=knowledge_search,
        signal=signal,
    )

    try:
        stream = run_skill(run_input)
        if hasattr(stream, "__aiter__"):
            async for chunk in stream:
                if _is_aborted(signal):
                    yield RunFailedEvent(error="客户端连接已中断")
                    return
                reasoning = getattr(chunk, "reasoningDelta", None) or getattr(
                    chunk, "reasoning_delta", None
                )
                if reasoning:
                    reasoning_seq += 1
                    yield ReasoningDeltaEvent(delta=reasoning, sequence=reasoning_seq)
                content = getattr(chunk, "contentDelta", None) or getattr(
                    chunk, "content_delta", None
                )
                if content:
                    visible_output += content
                chunk_usage = getattr(chunk, "usage", None)
                if chunk_usage:
                    usage = chunk_usage
        else:
            for chunk in stream:
                content = getattr(chunk, "contentDelta", None) or getattr(
                    chunk, "content_delta", None
                )
                if content:
                    visible_output += content
                chunk_usage = getattr(chunk, "usage", None)
                if chunk_usage:
                    usage = chunk_usage

        if not visible_output.strip():
            yield RunFailedEvent(error="AI 助手未生成有效内容")
            return

        chunk_size = max(64, int(message_chunk_chars or 256))
        for index in range(0, len(visible_output), chunk_size):
            yield MessageDeltaEvent(delta=visible_output[index:index + chunk_size])
        yield RunCompletedEvent(output=visible_output, usage=usage or {})
    except Exception as err:
        yield RunFailedEvent(error=f"AI 助手任务执行失败: {err}")
