import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.simple_chat import SimpleChatLangGraphWorkflow


class Chunk:
    def __init__(self, content=None, reasoning=None, usage=None):
        self.contentDelta = content
        self.reasoningDelta = reasoning
        self.usage = usage


class Provider:
    async def run_skill(self, _input):
        yield Chunk(reasoning="thinking")
        yield Chunk(content="answer")
        yield Chunk(usage={"prompt_tokens": 5, "completion_tokens": 2, "total_tokens": 7})


@pytest.mark.anyio
async def test_simple_chat_runs_as_langgraph_and_retrieves_knowledge():
    seen = []

    def search(query):
        seen.append(query)
        return "--- wiki.md :: Test ---\n知识内容"

    workflow = SimpleChatLangGraphWorkflow()
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage="问题",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=Provider(),
        agent_id="demo-ai",
        role_id="expert",
        skill_md="Use knowledge.",
        knowledge_search=search,
    )

    events = []
    async for event in workflow.stream(context):
        events.append(event)

    assert seen == ["问题"]
    assert any(getattr(event, "event", None) == "reasoning.delta" for event in events)
    completed = next(event for event in events if getattr(event, "event", None) == "run.completed")
    assert completed.output == "answer"
    assert completed.usage["total_tokens"] == 7
