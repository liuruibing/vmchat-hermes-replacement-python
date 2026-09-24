import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.workflow.engine import WorkflowContext, WorkflowEngine
from app.workflow.registry import WorkflowRegistry


class DemoWorkflow:
    id = "demo"

    async def stream(self, context):
        yield {"event": "message.delta", "delta": context.input_val.userMessage}
        yield {"event": "run.completed", "output": context.input_val.userMessage}


def make_context(message="hello"):
    return WorkflowContext(
        input_val=VmChatInput(
            userMessage=message,
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=object(),
        agent_id="demo-ai",
        role_id="demo-role",
    )


@pytest.mark.anyio
async def test_workflow_engine_dispatches_registered_workflow():
    registry = WorkflowRegistry([DemoWorkflow()])
    engine = WorkflowEngine(registry)

    events = []
    async for event in engine.stream("demo", make_context("hi")):
        events.append(event)

    assert events[0]["delta"] == "hi"
    assert events[-1]["event"] == "run.completed"


def test_workflow_registry_rejects_duplicates_and_unknown_ids():
    registry = WorkflowRegistry([DemoWorkflow()])

    with pytest.raises(ValueError, match="DUPLICATE_WORKFLOW"):
        registry.register(DemoWorkflow())

    with pytest.raises(ValueError, match="UNKNOWN_WORKFLOW"):
        registry.require("missing")


def test_workflow_context_keeps_runtime_services_outside_graph_state():
    context = make_context()
    assert context.agent_id == "demo-ai"
    assert context.role_id == "demo-role"
    assert context.resources is None
    assert context.knowledge_search is None
