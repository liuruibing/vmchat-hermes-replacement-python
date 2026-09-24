from dataclasses import dataclass
from types import SimpleNamespace

import pytest

import app.workflow.graphs.performance_report as graph_module
from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.contracts.types import ValidationFailure, ValidationIssue, ValidationSuccess
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.performance_report import PerformanceReportLangGraphWorkflow
from app.workflow.graphs.performance_semantics import build_semantic_plan, resolve_metrics


class Resources:
    skillMd = "# skill"
    toolResourceTextByPath = {}
    moduleProfiles = {
        "averagePePb": {
            "moduleId": "averagePePb",
            "entity": "fund",
            "shape": "time_series",
            "grain": {"primaryCanonicalKeys": ["date"]},
            "taxonomy": None,
            "render": {"metrics": [{"name": "PE", "rawField": "F_PETTM"}]},
            "fields": [{"rawField": "F_PETTM", "unit": "未明确"}],
        },
        "stockExposureTiming": {
            "moduleId": "stockExposureTiming",
            "entity": "fund",
            "shape": "time_series",
            "grain": {"primaryCanonicalKeys": ["date"]},
            "taxonomy": None,
            "render": {
                "metrics": [
                    {"name": "股票净敞口占比(左)", "rawField": "F_STOCK_EXP"}
                ]
            },
            "fields": [{"rawField": "F_STOCK_EXP", "unit": "%"}],
        },
        "fundDurationTiming": {
            "moduleId": "fundDurationTiming",
            "entity": "fund",
            "shape": "time_series",
            "grain": {"primaryCanonicalKeys": ["date"]},
            "taxonomy": None,
            "render": {
                "metrics": [{"name": "组合久期", "rawField": "F_MDF_DURATION"}]
            },
            "fields": [{"rawField": "F_MDF_DURATION", "unit": "未明确"}],
        },
    }
    profileIndex = {"modules": {}}
    catalogContract = {}
    schemaJson = {}


def make_input(message):
    return VmChatInput(
        userMessage=message,
        globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
    )


def make_context(provider, message="hello"):
    return WorkflowContext(
        input_val=make_input(message),
        provider=provider,
        agent_id="performance-ai",
        role_id="performance-analyst",
        resources=Resources(),
    )


class TextProvider:
    async def run_skill(self, _input):
        yield SimpleNamespace(contentDelta="普通回答", reasoningDelta=None, usage=None)
        yield SimpleNamespace(
            contentDelta=None,
            reasoningDelta=None,
            usage={"prompt_tokens": 3, "completion_tokens": 2, "total_tokens": 5},
        )


@pytest.mark.anyio
async def test_performance_langgraph_keeps_text_protocol():
    workflow = PerformanceReportLangGraphWorkflow()
    events = []
    async for event in workflow.stream(make_context(TextProvider(), "解释一下PE")):
        events.append(event)

    completed = next(event for event in events if getattr(event, "event", None) == "run.completed")
    assert completed.output == "普通回答"
    assert completed.usage["total_tokens"] == 5


class RepairProvider:
    def __init__(self):
        self.generate_calls = 0

    async def run_skill(self, _input):
        yield SimpleNamespace(
            contentDelta='{"action":"create","requests":[],"view":{"type":"table"}}',
            reasoningDelta=None,
            usage={"prompt_tokens": 4, "completion_tokens": 3, "total_tokens": 7},
        )

    async def generate(self, _input):
        self.generate_calls += 1
        return SimpleNamespace(
            result=SimpleNamespace(
                type="dsl",
                dsl={
                    "action": "create",
                    "id": "repaired-id",
                    "requests": [],
                    "view": {"type": "table"},
                },
            ),
            usage={"prompt_tokens": 2, "completion_tokens": 2, "total_tokens": 4},
        )


@pytest.mark.anyio
async def test_performance_langgraph_routes_validation_failure_through_repair(monkeypatch):
    calls = {"count": 0}

    def fake_validate(candidate, _resources, _block_ids):
        calls["count"] += 1
        if calls["count"] == 1:
            return ValidationFailure(
                errors=[
                    ValidationIssue(
                        code="INVALID_SCHEMA",
                        path="/id",
                        message="missing id",
                    )
                ]
            )
        return ValidationSuccess(dsls=[candidate])

    monkeypatch.setattr(graph_module, "_call_validate_vm_report_dsl_set", fake_validate)

    provider = RepairProvider()
    workflow = PerformanceReportLangGraphWorkflow()
    events = []
    async for event in workflow.stream(make_context(provider, "生成报表")):
        events.append(event)

    completed = next(event for event in events if getattr(event, "event", None) == "run.completed")
    assert '"id": "repaired-id"' in completed.output
    assert provider.generate_calls == 1
    assert calls["count"] == 2
    assert completed.usage["total_tokens"] == 11


def test_metric_resolver_and_semantic_plan_are_metric_centric():
    resources = Resources()
    message = "把持仓平均PE、股票净敞口占比和组合久期放到一张表里"
    metrics = resolve_metrics(message, resources)
    names = {item["name"] for item in metrics}
    modules = {item["moduleId"] for item in metrics}

    assert "PE" in names
    assert "股票净敞口占比(左)" in names
    assert "组合久期" in names
    assert modules == {"averagePePb", "stockExposureTiming", "fundDurationTiming"}

    plan = build_semantic_plan(metrics, resources)
    assert plan["mergeable"] is True
    assert plan["joinKey"] == "date"
    assert plan["entities"] == ["fund"]
