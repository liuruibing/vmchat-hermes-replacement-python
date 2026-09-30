import pytest

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS
from app.mandate_risk_v2.mapping_validator import validate_batch, validate_critic, validate_dispositions
from app.mandate_risk_v2.models import EvidenceRef, Requirement, RequirementIR


def _ir():
    return RequirementIR(document_name="x.pdf", requirements=[Requirement(
        requirement_id="REQ-0001", requirement_type="QUANTITATIVE_LIMIT",
        semantic_summary="A measurable portfolio limit", evidence=EvidenceRef(clause_ids=["c0001"]),
    )])


def _registry():
    return RawRiskMetricRegistry([RawRiskMetric(
        row_id=2, source_row=2, metric_name="Metric", algorithm="exposure / NAV",
    )])


def _matrix():
    return [{"dimension": d, "requirement_basis": "contract", "metric_basis": "library",
             "relation": "EQUIVALENT", "reason": "audited"}
            for d in CORE_COMPATIBILITY_DIMENSIONS]


def _batch(matrix):
    return {"links": [{"requirement_id": "REQ-0001", "raw_row_id": 2, "level": "DIRECT",
                       "compatibility": matrix, "evidence_clause_ids": ["c0001"], "reason": "direct"}],
            "row_assessments": [{"raw_row_id": 2, "outcome": "LINKED", "reason": "audited"}]}


def test_screening_explanation_cannot_repeat_a_compatibility_dimension():
    matrix = _matrix()
    matrix.append(dict(matrix[0]))
    with pytest.raises(ValueError, match="duplicate compatibility dimension"):
        validate_batch(_batch(matrix), ir=_ir(), registry=_registry(), batch_row_ids={2})


def test_critic_must_explicitly_review_non_metric_destination():
    ir = _ir()
    dispositions = validate_dispositions({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "classified as control", "destinations": [{
            "destination": "NON_METRIC", "raw_row_ids": [], "evidence_clause_ids": ["c0001"],
            "aspect": "control", "reason": "not a formal metric",
        }],
    }]}, ir=ir, registry=_registry(), links=[])
    with pytest.raises(ValueError, match="critic verdicts missing"):
        validate_critic({"verdicts": []}, ir=ir, dispositions=dispositions)
    review = validate_critic({"verdicts": [{
        "requirement_id": "REQ-0001", "destination": "NON_METRIC", "raw_row_id": None,
        "aspect": "control", "verdict": "CONFIRM", "reason": "verified",
        "evidence_clause_ids": ["c0001"],
    }]}, ir=ir, dispositions=dispositions)
    assert review.verdicts[0].destination == "NON_METRIC"
