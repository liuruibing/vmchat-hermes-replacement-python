from __future__ import annotations

from dataclasses import dataclass
from typing import Any, AsyncGenerator, Callable, Optional, Protocol, runtime_checkable

from app.compatibility.hermes_request import VmChatInput


@dataclass
class WorkflowContext:
    """Runtime inputs shared by every Agent workflow.

    Long-lived conversation/knowledge/artifact state stays in the AI Runtime.
    A workflow only receives the bounded, current-run context it needs.
    """

    input_val: VmChatInput
    provider: Any
    agent_id: str
    role_id: str
    role_prompt: str = ""
    skill_md: str = ""
    knowledge_search: Optional[Callable[[str], str]] = None
    resources: Any = None
    signal: Optional[Any] = None
    message_chunk_chars: int = 256
    run_id: Optional[str] = None
    session_id: Optional[str] = None


@runtime_checkable
class WorkflowProtocol(Protocol):
    id: str

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        ...


class WorkflowEngine:
    """Dispatch a named workflow without coupling the runtime to LangGraph."""

    def __init__(self, registry: Any) -> None:
        self.registry = registry

    def stream(
        self,
        workflow_id: str,
        context: WorkflowContext,
    ) -> AsyncGenerator[Any, None]:
        workflow = self.registry.require(workflow_id)
        return workflow.stream(context)
