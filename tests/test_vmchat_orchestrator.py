import pytest
import asyncio
from typing import AsyncGenerator, Dict, Any, List, Optional
from unittest.mock import patch
from dataclasses import dataclass

from app.compatibility.hermes_request import VmChatInput, GlobalQueryParameters
from app.resources.resource_types import LoadedResources, Manifest
from app.contracts.types import VmChatRunError, ValidationSuccess, ValidationFailure, ValidationIssue
from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    HermesSseEvent,
)
from app.orchestrator.vmchat_orchestrator import (
    OrchestratorInput,
    OrchestratorOutput,
    StreamOrchestratorOptions,
    validate_and_repair_dsl,
    validateAndRepairDsl,
    run_vm_chat_orchestrator,
    runVmChatOrchestrator,
    stream_vm_chat,
    streamVmChat,
    MAX_DSL_REPAIR_ATTEMPTS,
    _classify_model_output,
)

@pytest.fixture
def anyio_backend():
    return "asyncio"

class MockProviderText:
    async def run_skill(self, input: Any) -> AsyncGenerator[Any, None]:
        @dataclass
        class Chunk:
            contentDelta: Optional[str] = None
            reasoningDelta: Optional[str] = None
            usage: Optional[Dict[str, Any]] = None

        yield Chunk(reasoningDelta="Thinking...")
        yield Chunk(contentDelta="Hello, this is pure text response.")
        yield Chunk(usage={"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15})

class MockProviderDslInvalidThenRepair:
    def __init__(self) -> None:
        self.generate_calls = 0

    async def run_skill(self, input: Any) -> AsyncGenerator[Any, None]:
        @dataclass
        class Chunk:
            contentDelta: Optional[str] = None
            reasoningDelta: Optional[str] = None
            usage: Optional[Dict[str, Any]] = None

        yield Chunk(contentDelta='{"action": "invalid"}')
        yield Chunk(usage={"prompt_tokens": 20, "completion_tokens": 30, "total_tokens": 50})

    async def generate(self, input: Any) -> Any:
        self.generate_calls += 1
        @dataclass
        class Result:
            type: str
            dsl: Any

        @dataclass
        class Output:
            result: Any
            usage: Dict[str, Any]

        return Output(
            result=Result(type="dsl", dsl={"action": "repaired", "requests": [], "transform": [], "view": {}}),
            usage={"prompt_tokens": 15, "completion_tokens": 25, "total_tokens": 40}
        )


class MockProviderAlwaysInvalidRepair:
    def __init__(self) -> None:
        self.generate_calls = 0

    async def generate(self, input: Any) -> Any:
        self.generate_calls += 1

        @dataclass
        class Result:
            type: str
            dsl: Any

        @dataclass
        class Output:
            result: Any
            usage: Dict[str, Any]

        return Output(
            result=Result(type="text", dsl=None),
            usage={"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2},
        )

def make_resources() -> LoadedResources:
    manifest = Manifest(
        schemaVersion="1.0",
        catalogVersion="1.0",
        moduleCount=0,
        files=[]
    )
    return LoadedResources(
        manifest=manifest,
        skillMd="# Skill doc",
        schemaJson={},
        catalogContract={},
        catalogIndexMd="",
        catalogMetricsMd="",
        submodulesJson=[],
        moduleMarkdownMap={},
        toolResourceTextByPath={},
    )

def make_input(msg: str) -> VmChatInput:
    return VmChatInput(
        userMessage=msg,
        globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={})
    )

@pytest.mark.anyio
async def test_run_vm_chat_orchestrator_text():
    resources = make_resources()
    provider = MockProviderText()
    vm_input = make_input("Hello")

    res = await run_vm_chat_orchestrator(OrchestratorInput(
        input=vm_input,
        resources=resources,
        provider=provider,
    ))

    assert res.resultType == "text"
    assert res.text == "Hello, this is pure text response."
    assert res.attemptCount == 1
    assert res.repairAttempts == 0
    assert res.usage["prompt_tokens"] == 10

@pytest.mark.anyio
async def test_stream_vm_chat_text():
    resources = make_resources()
    provider = MockProviderText()
    vm_input = make_input("Hello")

    events: List[HermesSseEvent] = []
    async for evt in stream_vm_chat(StreamOrchestratorOptions(
        input=vm_input,
        resources=resources,
        provider=provider,
    )):
        events.append(evt)

    # Should have ReasoningDeltaEvent, MessageDeltaEvent(s), RunCompletedEvent
    reasoning_events = [e for e in events if isinstance(e, ReasoningDeltaEvent)]
    message_events = [e for e in events if isinstance(e, MessageDeltaEvent)]
    completed_events = [e for e in events if isinstance(e, RunCompletedEvent)]

    assert len(reasoning_events) == 1
    assert reasoning_events[0].delta == "Thinking..."
    assert len(message_events) >= 1
    assert len(completed_events) == 1
    assert completed_events[0].output == "Hello, this is pure text response."

@patch("app.orchestrator.vmchat_orchestrator.validate_vm_report_dsl_set")
@pytest.mark.anyio
async def test_validate_and_repair_dsl_success(mock_validate):
    mock_validate.side_effect = [
        ValidationSuccess(dsls=[{"action": "repaired", "requests": [], "view": {}}])
    ]
    resources = make_resources()
    provider = MockProviderDslInvalidThenRepair()
    vm_input = make_input("Generate report")

    repaired = await validate_and_repair_dsl(
        initialCandidate={"action": "invalid"},
        initialIssues=[ValidationIssue(code="INVALID_SCHEMA", path="/", message="Missing requests")],
        initialUsage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        input=vm_input,
        resourceContext={},
        resources=resources,
        provider=provider,
    )

    assert repaired["attemptCount"] == 2
    assert repaired["repairAttempts"] == 1
    assert "repaired" in repaired["text"]
    assert provider.generate_calls == 1


@pytest.mark.anyio
async def test_validate_and_repair_retries_five_times_before_failing():
    resources = make_resources()
    provider = MockProviderAlwaysInvalidRepair()

    with pytest.raises(VmChatRunError, match="DSL_REPAIR_EXHAUSTED"):
        await validate_and_repair_dsl(
            initialCandidate={"action": "invalid"},
            initialIssues=[ValidationIssue(code="INVALID_SCHEMA", path="/", message="Missing requests")],
            initialUsage={},
            input=make_input("Generate report"),
            resourceContext={},
            resources=resources,
            provider=provider,
        )

    assert MAX_DSL_REPAIR_ATTEMPTS == 5
    assert provider.generate_calls == 5


@pytest.mark.anyio
async def test_validate_and_repair_passes_node_compatible_validation_options():
    resources = make_resources()
    resources.catalogContract = {
        "modules": {
            "modA": {"sqlCode": "codeA"},
        }
    }
    provider = MockProviderDslInvalidThenRepair()
    vm_input = make_input("Generate report")
    valid_dsl = {
        "action": "create",
        "id": "3d1d1f05-7f55-46eb-8e5f-155018a7b97a",
        "requests": [{"id": "req1", "moduleId": "modA", "sqlCode": "codeA"}],
        "transform": {
            "language": "javascript",
            "function": "function transform(responses) { return [{ c1: responses.req1 }]; }",
        },
        "view": {"type": "table", "title": "T", "columns": [{"field": "c1", "label": "L"}]},
    }

    repaired = await validate_and_repair_dsl(
        initialCandidate=valid_dsl,
        initialIssues=None,
        initialUsage={"prompt_tokens": 10, "completion_tokens": 10, "total_tokens": 20},
        input=vm_input,
        resourceContext={},
        resources=resources,
        provider=provider,
    )

    assert repaired["attemptCount"] == 1
    assert repaired["repairAttempts"] == 0
    assert provider.generate_calls == 0


def test_model_output_classifier_keeps_business_info_out_of_dsl_repair():
    raw = '{"intent":"businessInfo","renderType":"businessInfo","title":"说明","message":"内容"}'
    classified = _classify_model_output(raw)

    assert classified["kind"] == "text"
    assert '"businessInfo"' in classified["text"]
    assert classified["candidate"] is None


def test_model_output_classifier_extracts_prefixed_dsl_json():
    raw = (
        "已完成检索。\n"
        '{"action":"create","id":"3d1d1f05-7f55-46eb-8e5f-155018a7b97a",'
        '"requests":[],"transform":{"language":"javascript","function":"function transform(responses){return [];}"},'
        '"view":{"type":"table","columns":[]}}'
    )
    classified = _classify_model_output(raw)

    assert classified["kind"] == "dsl"
    assert classified["candidate"]["action"] == "create"
