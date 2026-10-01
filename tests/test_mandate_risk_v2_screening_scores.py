import json
import math
from types import SimpleNamespace

import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingPipeline, MappingResult
from app.mandate_risk_v2.mapping_models import CriticReview, FinalMappingReview, MappingLink
from app.mandate_risk_v2.mapping_validator import validate_batch, validate_critic, validate_dispositions
from app.mandate_risk_v2.models import EvidenceRef, Requirement, RequirementIR
from app.mandate_risk_v2.report import render_v2_report
from app.mandate_risk_v2.result import build_v2_analysis_result


def fixture():
    clauses = [DocumentClause(clause_id=f"c000{i}", text=text, page=i)
               for i, text in enumerate(("Maintain sufficient portfolio liquidity.",
                                         "Monitor credit risk exposure."), 1)]
    ir = RequirementIR(document_name="screening.pdf", requirements=[
        Requirement(requirement_id=f"REQ-000{i}", requirement_type="OBJECTIVE",
                    semantic_summary=clause.text, evidence=EvidenceRef(clause_ids=[clause.clause_id]))
        for i, clause in enumerate(clauses, 1)
    ])
    registry = RawRiskMetricRegistry([
        RawRiskMetric(row_id=2, source_row=2, metric_name="Liquidity indicator", algorithm=""),
        RawRiskMetric(row_id=3, source_row=3, metric_name="Credit indicator", algorithm="credit spread"),
        RawRiskMetric(row_id=4, source_row=4, metric_name="Unrelated indicator", algorithm="turnover"),
    ])
    return ir, clauses, registry


def link(row=2, requirement=1, score=88, level="REVIEW"):
    return {"requirement_id": f"REQ-000{requirement}", "raw_row_id": row, "level": level,
            "match_score": score, "score_reason": "The PDF expressly requires monitoring this risk.",
            "reason": "Relevant risk monitoring purpose; calculation details need confirmation.",
            "evidence_clause_ids": [f"c000{requirement}"], "compatibility": [{
                "dimension": "algorithm_semantics", "requirement_basis": "qualitative monitoring objective",
                "metric_basis": "incomplete calculation basis", "relation": "INSUFFICIENT",
                "reason": "An incomplete algorithm does not prevent selecting a relevant indicator.",
            }]}


def batch(item):
    return {"links": [item], "row_assessments": [{
        "raw_row_id": row, "outcome": "LINKED" if row == item["raw_row_id"] else "NOT_RELEVANT",
        "reason": "catalogue row inspected",
    } for row in (2, 3, 4)]}


def test_screening_accepts_direct_relevance_without_algorithm_equivalence_or_twelve_dimensions():
    ir, _, registry = fixture()
    result = validate_batch(batch(link(level="DIRECT")), ir=ir, registry=registry,
                            batch_row_ids={2, 3, 4}, require_scores=True)
    assert result.links[0].match_score == 88


@pytest.mark.parametrize("score", [-1, 101, math.nan, math.inf, True])
def test_screening_rejects_invalid_scores(score):
    ir, _, registry = fixture()
    with pytest.raises(ValueError):
        validate_batch(batch(link(score=score)), ir=ir, registry=registry,
                       batch_row_ids={2, 3, 4}, require_scores=True)


@pytest.mark.parametrize("field", ["match_score", "score_reason"])
def test_new_model_outputs_require_a_score_and_its_reason(field):
    ir, _, registry = fixture()
    item = link()
    item.pop(field)
    with pytest.raises(ValueError, match="score"):
        validate_batch(batch(item), ir=ir, registry=registry,
                       batch_row_ids={2, 3, 4}, require_scores=True)


def test_unified_screening_result_merges_requirements_sorts_scores_and_excludes_rejected_metrics():
    ir, clauses, registry = fixture()
    mapping = MappingResult(
        links=[MappingLink.model_validate(item) for item in (
            link(score=78), link(requirement=2, score=62, level="DIRECT"),
            link(row=3, requirement=2, score=94), link(row=4, score=55))],
        dispositions=FinalMappingReview(dispositions=[]), usage={},
        critic=CriticReview.model_validate({"verdicts": [], "rejected_candidates": [{
            "requirement_id": "REQ-0001", "raw_row_id": 4, "reason": "No document-supported use",
            "evidence_clause_ids": ["c0001"],
        }]}),
    )
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert [item.metric.raw_row_id for item in result.screened_metrics] == [3, 2]
    assert [item.match_score for item in result.screened_metrics] == [94, 78]
    liquidity = result.screened_metrics[1]
    assert [item.match_score for item in liquidity.requirements] == [78, 62]
    assert liquidity.score_reason == link()["score_reason"]
    report = render_v2_report(ir=ir, clauses=clauses, registry=registry, mapping=mapping, analysis=result)
    table = report.split("## 筛选结果", 1)[1].split("## 指标匹配依据", 1)[0]
    assert table.index("Credit indicator") < table.index("Liquidity indicator")
    assert "94/100" in table and "78/100" in table
    assert "Unrelated indicator" not in report
    assert "## 建议关注的候选指标" not in report
    assert "正确概率" in report and "最高" in report
    assert "Maintain sufficient portfolio liquidity.（第 1 页）" in report


def test_historical_results_remain_unscored_instead_of_getting_an_invented_number():
    ir, clauses, registry = fixture()
    item = link()
    item.pop("match_score")
    item.pop("score_reason")
    mapping = MappingResult(links=[MappingLink.model_validate(item)],
                            dispositions=FinalMappingReview(dispositions=[]),
                            critic=CriticReview(verdicts=[]), usage={})
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert result.screened_metrics[0].match_score is None
    assert "未评分" in render_v2_report(ir=ir, clauses=clauses, registry=registry,
                                   mapping=mapping, analysis=result)


def test_critic_score_adjustment_requires_existing_link_and_canonical_evidence():
    ir, _, registry = fixture()
    links = [MappingLink.model_validate(link())]
    dispositions = FinalMappingReview(dispositions=[])
    adjustment = {"requirement_id": "REQ-0001", "raw_row_id": 2, "match_score": 74,
                  "score_reason": "Relevant monitoring, but the document scope is narrower.",
                  "evidence_clause_ids": ["c0001"]}
    payload = {"verdicts": [], "score_adjustments": [adjustment]}
    assert validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry,
                           links=links).score_adjustments[0].match_score == 74
    adjustment["raw_row_id"] = 999
    with pytest.raises(ValueError, match="score adjustment"):
        validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=links)
    adjustment["raw_row_id"] = 2
    adjustment["evidence_clause_ids"] = ["c9999"]
    with pytest.raises(ValueError, match="evidence"):
        validate_critic(payload, ir=ir, dispositions=dispositions, registry=registry, links=links)


def test_relevant_metric_can_be_selected_even_when_calculation_needs_review():
    ir, _, registry = fixture()
    links = [MappingLink.model_validate(link())]
    payload = {"dispositions": [{"requirement_id": requirement.requirement_id,
        "reason": "screening decision", "destinations": [{
            "destination": "MAIN_TABLE" if index == 0 else "NON_METRIC",
            "raw_row_ids": [2] if index == 0 else [],
            "evidence_clause_ids": requirement.evidence.clause_ids,
            "aspect": "risk monitoring", "reason": "Relevant monitoring indicator",
        }]} for index, requirement in enumerate(ir.requirements)]}
    result = validate_dispositions(payload, ir=ir, registry=registry, links=links)
    assert result.dispositions[0].destinations[0].raw_row_ids == [2]


@pytest.mark.anyio
@pytest.mark.parametrize("reject_direct", [False, True])
async def test_pipeline_applies_critic_scores_or_rejections_to_the_final_screening_result(reject_direct):
    class Provider:
        async def run_skill(self, run_input):
            if "# V2 mapping batch" in run_input.user_prompt:
                output = batch(link(level="DIRECT"))
            elif "# V2 final destinations" in run_input.user_prompt:
                output = {"dispositions": [{"requirement_id": f"REQ-000{i}", "reason": "audited",
                    "destinations": [{"destination": "MAIN_TABLE" if i == 1 else "NON_METRIC",
                        "raw_row_ids": [2] if i == 1 else [], "evidence_clause_ids": [f"c000{i}"],
                        "aspect": "monitoring", "reason": "document-supported purpose"}]} for i in (1, 2)]}
            else:
                output = {"verdicts": [{"requirement_id": f"REQ-000{i}",
                    "destination": "MAIN_TABLE" if i == 1 else "NON_METRIC",
                    "raw_row_id": 2 if i == 1 else None, "aspect": "monitoring", "verdict": "CONFIRM",
                    "reason": "reviewed document evidence", "evidence_clause_ids": [f"c000{i}"]}
                    for i in (1, 2)]}
                if reject_direct:
                    output["rejected_candidates"] = [{"requirement_id": "REQ-0001", "raw_row_id": 2,
                        "reason": "The metric has no applicable monitoring use after checking scope.",
                        "evidence_clause_ids": ["c0001"]}]
                else:
                    output["score_adjustments"] = [{"requirement_id": "REQ-0001", "raw_row_id": 2,
                        "match_score": 74, "score_reason": "Relevant but narrower scope than initially assessed.",
                        "evidence_clause_ids": ["c0001"]}]
            yield SimpleNamespace(contentDelta=json.dumps(output), usage={"total_tokens": 1})

    ir, clauses, registry = fixture()
    mapping = await MappingPipeline().run(ir=ir, clauses=clauses, registry=registry, provider=Provider())
    result = build_v2_analysis_result(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    if reject_direct:
        assert result.screened_metrics == []
        assert result.matched_metrics == []
        assert result.pending_review[0].candidate_metrics == []
        assert "Critic 排除" in result.pending_review[0].reason
    else:
        assert result.screened_metrics[0].match_score == 74
        assert result.screened_metrics[0].score_reason.startswith("Critic：")
        assert result.screened_metrics[0].requirements[0].match_score == 74
        assert "74/100" in render_v2_report(ir=ir, clauses=clauses, registry=registry,
                                           mapping=mapping, analysis=result)
