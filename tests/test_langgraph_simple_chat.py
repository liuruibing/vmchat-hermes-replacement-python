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


class CapturePromptProvider:
    def __init__(self):
        self.captured_input = None

    async def run_skill(self, input_val):
        self.captured_input = input_val
        yield Chunk(content="doc answer")
        yield Chunk(usage={"prompt_tokens": 10, "completion_tokens": 4, "total_tokens": 14})


class MockParsedDoc:
    def __init__(self, text, filename="sample.pdf"):
        self.text = text
        self.filename = filename


@pytest.mark.anyio
async def test_simple_chat_loads_and_injects_document_context():
    provider = CapturePromptProvider()
    doc_store = {"doc-123": MockParsedDoc("条款1: 跟踪误差不得超过 100%。\n条款2: 标的为 Listed Equity。")}

    workflow = SimpleChatLangGraphWorkflow()
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage="这份委托的跟踪误差限制是多少？",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=provider,
        agent_id="mandate-risk-chat",
        role_id="risk-assistant",
        skill_md="回答关于文档的问题。",
        document_ids=["doc-123"],
        document_loader=lambda doc_id: doc_store[doc_id],
    )

    events = []
    async for event in workflow.stream(context):
        events.append(event)

    completed = next(event for event in events if getattr(event, "event", None) == "run.completed")
    assert completed.output == "doc answer"
    assert provider.captured_input is not None
    assert "<document_content>" in provider.captured_input.user_prompt
    assert "条款1: 跟踪误差不得超过 100%。" in provider.captured_input.user_prompt
