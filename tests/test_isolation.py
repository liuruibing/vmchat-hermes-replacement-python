import pytest
import asyncio
from typing import AsyncGenerator, Any

from app.compatibility.hermes_request import VmChatInput, GlobalQueryParameters
from app.compatibility.hermes_events import MessageDeltaEvent, RunCompletedEvent
from app.provider.fixed_provider import ModelSkillRunInput, ModelStreamChunk
from app.orchestrator.vmchat_orchestrator import stream_vm_chat, StreamOrchestratorOptions
from app.resources.resource_types import LoadedResources, Manifest

class MinimalMockProvider:
    async def run_skill(self, input: ModelSkillRunInput) -> AsyncGenerator[ModelStreamChunk, None]:
        yield ModelStreamChunk(contentDelta="X")
        yield ModelStreamChunk(usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15}, done=True)

@pytest.mark.anyio
async def test_minimal_orchestrator_stream():
    resources = LoadedResources(
        manifest=Manifest(schemaVersion="1.0", catalogVersion="1.0", moduleCount=0, files=[]),
        skillMd="", schemaJson={}, catalogContract={}, catalogIndexMd="", catalogMetricsMd="",
        submodulesJson=[], moduleMarkdownMap={}, toolResourceTextByPath={}
    )
    vm_input = VmChatInput(userMessage="Hello", globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}))
    
    opts = StreamOrchestratorOptions(
        input=vm_input,
        resources=resources,
        provider=MinimalMockProvider(),
        message_chunk_chars=256
    )
    
    events = []
    async for evt in stream_vm_chat(opts):
        events.append(evt)
        
    message_deltas = [e for e in events if isinstance(e, MessageDeltaEvent)]
    done_events = [e for e in events if hasattr(e, "output") and getattr(e, "event", getattr(e, "type", "")) in ("run.completed", "stream.done")]
    
    assert len(message_deltas) == 1, f"Expected 1 MessageDeltaEvent, got {len(message_deltas)}. Events: {events}"
    assert message_deltas[0].delta == "X"
    assert len(done_events) == 1, f"Expected 1 Done event, got {len(done_events)}. Events: {events}"
    assert done_events[0].output == "X"
