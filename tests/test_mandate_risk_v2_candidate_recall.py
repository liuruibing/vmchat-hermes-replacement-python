import asyncio
import json
from types import SimpleNamespace

import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingPipeline, MappingResult
from app.mandate_risk_v2.mapping_models import CriticReview, FinalMappingReview, MappingLink
from app.mandate_risk_v2.mapping_validator import validate_batch, validate_critic
from app.mandate_risk_v2.models import EvidenceRef, Requirement, RequirementIR
from app.mandate_risk_v2.report import render_v2_report
from app.mandate_risk_v2.result import build_v2_analysis_result


def data():
    ir = RequirementIR(document_name="unseen.pdf", requirements=[Requirement(
        requirement_id="REQ-0001", requirement_type="OBJECTIVE",
        semantic_summary="Manage the portfolio's liquidity", evidence=EvidenceRef(clause_ids=["c0001"]),
    )])
    clauses = [DocumentClause(clause_id="c0001", text="Maintain sufficient liquidity.", page=2)]
    registry = RawRiskMetricRegistry([
        RawRiskMetric(row_id=19, source_row=19, metric_name="New liquidity monitoring measure", algorithm=""),
        RawRiskMetric(row_id=29, source_row=29, metric_name="Unrelated measure", algorithm="issuer count"),
    ])
    return ir, clauses, registry


def candidate(row_id=19):
    return {"requirement_id": "REQ-0001", "raw_row_id": row_id, "level": "REVIEW",
        "match_score": 82, "score_reason": "The PDF requires liquidity monitoring; calculation basis is incomplete.",
        "compatibility": [
            {"dimension": "measurement_object", "requirement_basis": "liquidity",
             "metric_basis": "liquidity monitoring", "relation": "EQUIVALENT", "reason": "related monitoring purpose"},
            {"dimension": "algorithm_semantics", "requirement_basis": "qualitative objective",
             "metric_basis": "not supplied", "relation": "INSUFFICIENT", "reason": "algorithm needs confirmation"},
        ], "evidence_clause_ids": ["c0001"], "reason": "Useful candidate for the contract liquidity objective"}


def test_related_candidate_needs_evidence_but_not_a_complete_equivalence_matrix():
    ir, _, registry = data()
    payload = {"links": [candidate()], "row_assessments": [
        {"raw_row_id": 19, "outcome": "LINKED", "reason": "related"},
        {"raw_row_id": 29, "outcome": "NOT_RELEVANT", "reason": "different purpose"},
    ]}
    assert validate_batch(payload, ir=ir, registry=registry, batch_row_ids={19, 29}).links[0].level == "REVIEW"
    payload["links"][0]["level"] = "DIRECT"
    assert validate_batch(payload, ir=ir, registry=registry, batch_row_ids={19, 29}).links[0].level == "DIRECT"


def test_review_candidate_survives_even_if_destination_review_does_not_select_it():
    ir, clauses, registry = data()
    mapping = MappingResult(links=[MappingLink.model_validate(candidate())],
        dispositions=FinalMappingReview(dispositions=[]), critic=CriticReview(verdicts=[]), usage={})
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert result.matched_metrics == []
    assert [item.metric.raw_row_id for item in result.candidate_metrics] == [19]
    assert result.candidate_metrics[0].requirements[0].mapping_evidence[0].page == 2
    report = render_v2_report(ir=ir, clauses=clauses, registry=registry, mapping=mapping, analysis=result)
    main = report.split("## 筛选结果", 1)[1].split("## 指标匹配依据", 1)[0]
    assert "New liquidity monitoring measure" in main
    assert "82/100" in main
    assert "New liquidity monitoring measure" in report
    assert "Maintain sufficient liquidity." in report
    assert "algorithm needs confirmation" in report
    assert "Unrelated measure" not in report


def test_critic_recall_accepts_only_grounded_library_candidates():
    ir, _, registry = data()
    dispositions = FinalMappingReview(dispositions=[])
    payload = {"verdicts": [], "recalled_links": [candidate()]}
    review = validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=[])
    assert review.recalled_links[0].raw_row_id == 19
    payload["recalled_links"][0]["level"] = "DIRECT"
    with pytest.raises(ValueError, match="REVIEW"):
        validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=[])
    payload["recalled_links"][0] = candidate(row_id=999)
    with pytest.raises(ValueError, match="raw_row_id"):
        validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=[])


def test_critic_can_remove_an_unrelated_review_candidate_without_removing_others():
    ir, clauses, registry = data()
    links = [MappingLink.model_validate(candidate(row_id=row_id)) for row_id in (19, 29)]
    review = validate_critic({"verdicts": [], "rejected_candidates": [{
        "requirement_id": "REQ-0001", "raw_row_id": 29,
        "reason": "Issuer count is unrelated to this liquidity objective",
        "evidence_clause_ids": ["c0001"]}]}, ir=ir,
        dispositions=FinalMappingReview(dispositions=[]), registry=registry, links=links)
    mapping = MappingResult(links=links, dispositions=FinalMappingReview(dispositions=[]), critic=review, usage={})
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert [item.metric.raw_row_id for item in result.candidate_metrics] == [19]


class RecallProvider:
    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# V2 mapping batch" in prompt:
            output = {"links": [], "row_assessments": [
                {"raw_row_id": row_id, "outcome": "NOT_RELEVANT", "reason": "no exact algorithm"}
                for row_id in (19, 29)]}
        elif "# V2 final destinations" in prompt:
            output = {"dispositions": [{"requirement_id": "REQ-0001", "reason": "no exact metric",
                "destinations": [{"destination": "LIBRARY_GAP", "raw_row_ids": [],
                    "evidence_clause_ids": ["c0001"], "aspect": "liquidity", "reason": "no exact algorithm"}]}]}
        else:
            output = {"verdicts": [{"requirement_id": "REQ-0001", "destination": "LIBRARY_GAP",
                "raw_row_id": None, "aspect": "liquidity", "verdict": "CONFIRM",
                "reason": "No equivalent algorithm; a related monitoring candidate is still useful",
                "evidence_clause_ids": ["c0001"]}], "recalled_links": [candidate()]}
        yield SimpleNamespace(contentDelta=json.dumps(output), usage={"total_tokens": 1})


@pytest.mark.anyio
async def test_critic_recovers_candidate_missed_by_initial_full_catalogue_mapping():
    ir, clauses, registry = data()
    mapping = await MappingPipeline(max_critic_repairs=0).run(
        ir=ir, clauses=clauses, registry=registry, provider=RecallProvider())
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert result.matched_metrics == []
    assert [item.metric.raw_row_id for item in result.candidate_metrics] == [19]
    assert len(result.library_gaps) == 1
    assert {item.raw_row_id for item in result.catalogue_assessments} == {19, 29}


@pytest.mark.anyio
async def test_critic_missing_condition_is_preserved_as_pending_without_inventing_a_metric():
    class MissingConditionProvider(RecallProvider):
        async def run_skill(self, run_input):
            async for chunk in super().run_skill(run_input):
                if "# V2 independent critic" in run_input.user_prompt:
                    payload = json.loads(chunk.contentDelta)
                    payload["missing_aspects"] = [{
                        "requirement_id": "REQ-0001", "aspect": "9-day liquidity condition",
                        "reason": "The final destinations omitted the independent 9-day threshold.",
                        "evidence_clause_ids": ["c0001"],
                    }]
                    chunk.contentDelta = json.dumps(payload)
                yield chunk

    ir, clauses, registry = data()
    clauses[0].text = "Maintain liquidity above 3% in 2 days and above 4% in 9 days."
    ir.requirements[0].semantic_summary = "Maintain both the 2-day and 9-day liquidity thresholds."
    mapping = await MappingPipeline().run(
        ir=ir, clauses=clauses, registry=registry, provider=MissingConditionProvider(),
    )
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert len(result.library_gaps) == 1
    assert len(result.pending_review) == 1
    pending = result.pending_review[0]
    assert pending.aspect == "9-day liquidity condition"
    assert "omitted the independent 9-day threshold" in pending.reason
    assert pending.candidate_metrics == []
    assert pending.evidence[0].text == clauses[0].text
    report = render_v2_report(ir=ir, clauses=clauses, registry=registry, mapping=mapping, analysis=result)
    assert "9-day liquidity condition" in report.split("## 需用户关注的差异与待确认项", 1)[1]


@pytest.mark.parametrize("invalid", ["unknown_requirement", "unknown_clause", "duplicate", "existing_aspect"])
def test_critic_missing_aspect_rejects_invalid_identity_or_duplicate_destination(invalid):
    ir, _, registry = data()
    dispositions = FinalMappingReview.model_validate({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "one known condition", "destinations": [{
            "destination": "PENDING_REVIEW", "raw_row_ids": [],
            "evidence_clause_ids": ["c0001"], "aspect": "known condition", "reason": "needs confirmation",
        }],
    }]})
    missing = {"requirement_id": "REQ-0001", "aspect": "missing condition",
               "reason": "not covered", "evidence_clause_ids": ["c0001"]}
    payload = {"verdicts": [], "missing_aspects": [missing]}
    if invalid == "unknown_requirement":
        missing["requirement_id"] = "REQ-FAKE"
    elif invalid == "unknown_clause":
        missing["evidence_clause_ids"] = ["c9999"]
    elif invalid == "duplicate":
        payload["missing_aspects"].append(dict(missing))
    else:
        missing["aspect"] = "known condition"
    with pytest.raises(ValueError):
        validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=[])


@pytest.mark.anyio
async def test_independent_catalogue_batches_overlap_without_losing_rows():
    class ParallelProvider(RecallProvider):
        def __init__(self):
            self.active = 0
            self.peak = 0
            self.started = asyncio.Event()

        async def run_skill(self, run_input):
            if "# V2 mapping batch" not in run_input.user_prompt:
                async for chunk in super().run_skill(run_input):
                    yield chunk
                return
            rows = json.loads(run_input.user_prompt.split("# Raw metric rows (JSON)\n", 1)[1].split("\n", 1)[0])
            self.active += 1
            self.peak = max(self.peak, self.active)
            if self.active == 2:
                self.started.set()
            await asyncio.wait_for(self.started.wait(), timeout=1)
            self.active -= 1
            yield SimpleNamespace(contentDelta=json.dumps({"links": [], "row_assessments": [
                {"raw_row_id": row["row_id"], "outcome": "NOT_RELEVANT", "reason": "no exact equivalent"}
                for row in rows]}), usage={"total_tokens": 1})

    ir, clauses, registry = data()
    provider = ParallelProvider()
    mapping = await MappingPipeline(batch_size=1, concurrency=2).run(
        ir=ir, clauses=clauses, registry=registry, provider=provider)
    assert provider.peak == 2
    assert [item.raw_row_id for item in mapping.row_assessments] == [19, 29]
