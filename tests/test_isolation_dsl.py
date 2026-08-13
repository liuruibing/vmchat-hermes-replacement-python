import pytest
import asyncio
import json
from typing import AsyncGenerator, Any
from pathlib import Path

from app.compatibility.hermes_request import VmChatInput, GlobalQueryParameters
from app.compatibility.hermes_events import MessageDeltaEvent, RunCompletedEvent
from app.provider.fixed_provider import ModelSkillRunInput, ModelStreamChunk
from app.orchestrator.vmchat_orchestrator import stream_vm_chat, StreamOrchestratorOptions
from app.resources.resource_loader import ResourceLoader

class MockDslProvider:
    def __init__(self, dsl_content: str):
        self.dsl_content = dsl_content
        
    async def run_skill(self, input: ModelSkillRunInput) -> AsyncGenerator[ModelStreamChunk, None]:
        yield ModelStreamChunk(contentDelta=self.dsl_content)
        yield ModelStreamChunk(usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}, done=True)

    async def generate(self, input: Any) -> Any:
        from dataclasses import dataclass
        @dataclass
        class Result:
            type: str
            dsl: Any
        @dataclass
        class Output:
            result: Any
            usage: dict
        return Output(
            result=Result(type="dsl", dsl=json.loads(self.dsl_content)),
            usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}
        )

@pytest.mark.anyio
async def test_orchestrator_dsl_flow():
    # Load realistic resources to pass validation
    loader = ResourceLoader()
    await loader.load()
    resources = loader.get_resources()
    
    # We load a truly valid DSL from validator-parity corpus
    valid_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [
            {
                "id": "req1",
                "moduleId": "assetContribute",
                "sqlCode": "4c15f9fd-98c1-4280-b7bb-56893691279a",
            },
        ],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { const data = responses.req1; return [{ col1: data }]; }",
        },
        "view": {
            "type": "table",
            "title": "资产贡献表",
            "columns": [{"field": "col1", "label": "列1"}],
        },
    }
    expected_dsl = json.dumps(valid_dsl)
    
    vm_input = VmChatInput(userMessage="Hello", globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}))
    
    opts = StreamOrchestratorOptions(
        input=vm_input,
        resources=resources,
        provider=MockDslProvider(expected_dsl),
        message_chunk_chars=256
    )
    
    events = []
    async for evt in stream_vm_chat(opts):
        events.append(evt)
        
    message_deltas = [e for e in events if isinstance(e, MessageDeltaEvent)]
    
    # Also check if it's RunCompletedEvent
    done_events = [e for e in events if hasattr(e, "output") and getattr(e, "event", getattr(e, "type", "")) in ("run.completed", "stream.done")]
    
    assert len(done_events) == 1, f"Expected 1 Done event, got {len(done_events)}. Events: {events}"
    final_output = done_events[0].output
    
    assert final_output != "", "Final output is empty!"
    
    # Compare JSON equivalence
    assert json.loads(final_output) == json.loads(expected_dsl)
    assert len(message_deltas) > 0, "No message deltas yielded!"
