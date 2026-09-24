from __future__ import annotations

from typing import Any, AsyncGenerator, Callable

from app.contracts.types import VmChatRunError
from app.workflow.engine import WorkflowContext


class SimpleChatWorkflow:
    id = "simple-chat"

    def __init__(self, stream_fn: Callable[..., AsyncGenerator[Any, None]]) -> None:
        self._stream_fn = stream_fn

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        return self._stream_fn(
            input_val=context.input_val,
            provider=context.provider,
            skill_md=context.skill_md,
            role_prompt=context.role_prompt,
            knowledge_search=context.knowledge_search,
            signal=context.signal,
            message_chunk_chars=context.message_chunk_chars,
        )


class VmReportWorkflow:
    id = "vm-report"

    def __init__(self, stream_fn: Callable[..., AsyncGenerator[Any, None]]) -> None:
        self._stream_fn = stream_fn

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        if context.resources is None:
            raise VmChatRunError(
                "SERVICE_DEGRADED",
                "当前 Agent 资源尚未加载完成",
            )
        return self._stream_fn(
            {
                "input": context.input_val,
                "resources": context.resources,
                "provider": context.provider,
                "signal": context.signal,
                "message_chunk_chars": context.message_chunk_chars,
                "role_prompt": context.role_prompt,
                "knowledge_search": context.knowledge_search,
            }
        )


def build_default_workflow_registry(
    *,
    simple_chat_stream: Callable[..., AsyncGenerator[Any, None]],
    vm_report_stream: Callable[..., AsyncGenerator[Any, None]],
):
    from app.workflow.registry import WorkflowRegistry

    from app.workflow.graphs.performance_report import PerformanceReportLangGraphWorkflow
    from app.workflow.graphs.simple_chat import SimpleChatLangGraphWorkflow

    return WorkflowRegistry(
        [
            SimpleChatLangGraphWorkflow(),
            PerformanceReportLangGraphWorkflow(),
        ]
    )
