import json

import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.screening import ScreeningPipeline
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_v2 import MandateRiskV2Workflow


TEXT = "[Page 1]\nThe portfolio invests in bonds.\n\n[Page 2]\nMaintain sufficient liquidity."


def registry():
    return RawRiskMetricRegistry([
        RawRiskMetric(row_id=2, source_row=2, metric_name="Liquidity", algorithm="liquid assets / NAV"),
        RawRiskMetric(row_id=3, source_row=3, metric_name="Duration", algorithm="weighted duration"),
    ], source_sha256="source-sha")


def row(row_id, score, clauses, level="DIRECT"):
    return {"raw_row_id": row_id, "level": level, "match_score": score,
            "reason": "Relevant monitoring of the stated exposure.",
            "evidence_clause_ids": clauses, "differences": "Confirm calculation basis."}


class Provider:
    def __init__(self, responses):
        self.responses = responses
        self.calls = []

    async def run_skill(self, request):
        self.calls.append(request)
        response = self.responses[min(len(self.calls) - 1, len(self.responses) - 1)]
        yield type("Chunk", (), {"contentDelta": json.dumps(response), "usage": {"total_tokens": 10}})()


@pytest.mark.anyio
async def test_default_workflow_screens_once_preserving_catalogue_and_exact_pdf_evidence(monkeypatch):
    monkeypatch.delenv("MANDATE_RISK_V2_MODE", raising=False)
    provider = Provider([{"rows": [row(2, 92, ["c0002"]), row(3, 78, ["c0001"], "REVIEW")]}])
    input_val = VmChatInput(userMessage=f"<document_name>sample.pdf</document_name><document_text>{TEXT}</document_text>",
                            globalQueryParameters=GlobalQueryParameters())
    context = WorkflowContext(input_val=input_val, provider=provider, agent_id="mandate-risk-v2-lab", role_id="requirement-analyst")
    events = [event async for event in MandateRiskV2Workflow(metric_registry=registry()).stream(context)]
    terminal = events[-1]
    assert terminal.event == "run.completed"
    assert len(provider.calls) == 1
    result = terminal.metadata["mandate_risk_v2"]["result"]
    assert result["analysis_mode"] == "screening"
    assert result["coverage_status"] == "not_audited"
    assert result["metric_catalogue_sha256"] == "source-sha"
    assert [item["match_score"] for item in result["screened_metrics"]] == [92, 78]
    assert result["screened_metrics"][0]["metric"]["algorithm"] == "liquid assets / NAV"
    quote = result["screened_metrics"][0]["requirements"][0]["mapping_evidence"][0]
    assert quote["page"] == 2
    assert TEXT[quote["source_start"]:quote["source_end"]] == quote["text"]
    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in terminal.output
    assert "未执行逐条要求覆盖审计" in terminal.output
    assert terminal.usage["total_tokens"] == 10


@pytest.mark.anyio
@pytest.mark.parametrize("invalid", [
    {"rows": [row(99, 92, ["c0001"]), row(3, 70, ["c0001"])]},
    {"rows": [row(2, 92, ["invented"]), row(3, 70, ["c0001"])]},
    {"rows": [row(2, 92, ["c0001"])]},
    {"rows": [row(2, 92, ["c0001"]), row(2, 70, ["c0001"])]},
    {"rows": [row(2, 101, ["c0001"]), row(3, 70, ["c0001"])]},
    {"rows": [row(2, "92", ["c0001"]), row(3, 70, ["c0001"])]},
    {"rows": [row(2, 92, []), row(3, 70, ["c0001"])]},
])
async def test_invalid_identity_score_or_evidence_retries_once_then_fails(invalid):
    provider = Provider([invalid])
    with pytest.raises(ValueError, match="MANDATE_SCREENING_INVALID"):
        await ScreeningPipeline().run(document_name="bad.pdf", document_text=TEXT,
                                     registry=registry(), provider=provider)
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_structural_retry_can_recover_without_semantic_audit():
    valid = {"rows": [row(2, 100, ["c0002"]), row(3, 0, [], "NOT_RELEVANT")]}
    provider = Provider([{"rows": []}, valid])
    analysis, usage = await ScreeningPipeline().run(document_name="sample.pdf", document_text=TEXT,
                                                  registry=registry(), provider=provider)
    assert len(analysis.screened_metrics) == 1
    assert usage["total_tokens"] == 20
    assert usage["expected_calls"] == 2


@pytest.mark.anyio
async def test_malformed_json_is_repaired_once_and_usage_stays_honest():
    class JsonProvider(Provider):
        async def run_skill(self, request):
            if not self.calls:
                self.calls.append(request)
                yield type("Chunk", (), {"contentDelta": "invalid JSON", "usage": {"total_tokens": 10}})()
            else:
                async for chunk in super().run_skill(request):
                    yield chunk

    provider = JsonProvider([{"rows": [row(2, 92, ["c0002"]), row(3, 0, [], "NOT_RELEVANT")]}])
    analysis, usage = await ScreeningPipeline().run(document_name="sample.pdf", document_text=TEXT,
                                                  registry=registry(), provider=provider)
    assert len(analysis.screened_metrics) == 1
    assert usage["expected_calls"] == 2
    assert usage["complete"] is False
    assert "total_tokens" not in usage


@pytest.mark.anyio
async def test_empty_selection_is_success_and_is_not_forced_into_candidates():
    provider = Provider([{"rows": [row(2, 0, [], "NOT_RELEVANT"), row(3, 0, [], "NOT_RELEVANT")]}])
    analysis, _ = await ScreeningPipeline().run(document_name="other.pdf", document_text=TEXT,
                                              registry=registry(), provider=provider)
    assert analysis.screened_metrics == []
    assert len(analysis.catalogue_assessments) == 2


@pytest.mark.anyio
async def test_long_document_reads_every_window_and_keeps_later_evidence():
    class WindowProvider(Provider):
        async def run_skill(self, request):
            self.calls.append(request)
            clauses = json.loads(request.user_prompt.split("# PDF clauses (JSON)\n", 1)[1].split("\n", 1)[0])
            target = next((item for item in clauses if "liquidity" in item["text"]), None)
            output = {"rows": [row(2, 91 if target else 0, [target["clause_id"]] if target else [],
                                   "DIRECT" if target else "NOT_RELEVANT"), row(3, 0, [], "NOT_RELEVANT")]}
            yield type("Chunk", (), {"contentDelta": json.dumps(output), "usage": {"total_tokens": 10}})()

    provider = WindowProvider([])
    analysis, usage = await ScreeningPipeline(document_window_chars=80).run(
        document_name="long.pdf", document_text=TEXT, registry=registry(), provider=provider)
    assert len(provider.calls) == 2
    assert len(analysis.screened_metrics) == 1
    assert analysis.screened_metrics[0].requirements[0].mapping_evidence[0].page == 2
    assert usage["document_windows"] == 2
