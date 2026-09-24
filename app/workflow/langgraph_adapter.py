from __future__ import annotations

from typing import Any, AsyncGenerator, Callable

from app.workflow.engine import WorkflowContext


class LangGraphWorkflow:
    """Optional bridge for a compiled LangGraph workflow.

    LangGraph stays behind WorkflowProtocol so the rest of the AI Runtime is not
    coupled to one workflow implementation technology.
    """

    def __init__(
        self,
        workflow_id: str,
        graph_factory: Callable[[WorkflowContext], Any],
        event_adapter: Callable[[Any, WorkflowContext], AsyncGenerator[Any, None]],
    ) -> None:
        self.id = workflow_id
        self._graph_factory = graph_factory
        self._event_adapter = event_adapter

    def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        graph = self._graph_factory(context)
        return self._event_adapter(graph, context)


def require_langgraph() -> Any:
    try:
        import langgraph  # type: ignore
    except ImportError as err:
        raise RuntimeError(
            "LANGGRAPH_NOT_INSTALLED: install LangGraph before registering a "
            "LangGraph-backed workflow"
        ) from err
    return langgraph
