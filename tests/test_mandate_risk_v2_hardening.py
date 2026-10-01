import pytest

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS, FinalMappingReview
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


def _critic_destinations():
    return FinalMappingReview.model_validate({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "two metrics and a gap", "destinations": [
            {"destination": "MAIN_TABLE", "raw_row_ids": [2, 3],
             "evidence_clause_ids": ["c0001"], "aspect": "Long unchanged aspect (with conditions)",
             "reason": "two rows"},
            {"destination": "LIBRARY_GAP", "raw_row_ids": [],
             "evidence_clause_ids": ["c0001"], "aspect": "Other window", "reason": "gap"},
        ],
    }]})


def _target_verdict(target_id, **kwargs):
    return {"target_id": target_id, "verdict": "CHALLENGE", "reason": "scope differs",
            "evidence_clause_ids": ["c0001"], **kwargs}


def test_critic_target_ids_preserve_each_exact_row_and_aspect():
    payload = {"verdicts": [_target_verdict("TGT-0003"), _target_verdict("TGT-0002"),
                            _target_verdict("TGT-0001")]}
    review = validate_critic(payload, ir=_ir(), dispositions=_critic_destinations())
    assert [(x.destination, x.raw_row_id, x.aspect) for x in review.verdicts] == [
        ("LIBRARY_GAP", None, "Other window"),
        ("MAIN_TABLE", 3, "Long unchanged aspect (with conditions)"),
        ("MAIN_TABLE", 2, "Long unchanged aspect (with conditions)"),
    ]
    assert all(x.verdict == "CHALLENGE" for x in review.verdicts)
    assert "requirement_id" not in payload["verdicts"][0]


@pytest.mark.parametrize("ids", [
    ["TGT-0001", "TGT-0002"],
    ["TGT-0001", "TGT-0002", "TGT-0002"],
    ["TGT-0001", "TGT-0002", "TGT-9999"],
])
def test_critic_targets_reject_missing_duplicate_or_unknown_ids(ids):
    with pytest.raises(ValueError):
        validate_critic({"verdicts": [_target_verdict(x) for x in ids]},
                        ir=_ir(), dispositions=_critic_destinations())


def test_critic_target_cannot_override_identity_or_skip_own_evidence():
    for change in [{"raw_row_id": 99}, {"aspect": "Rewritten aspect"},
                   {"evidence_clause_ids": ["c9999"]}]:
        payload = {"verdicts": [_target_verdict("TGT-0001", **change),
                                _target_verdict("TGT-0002"), _target_verdict("TGT-0003")]}
        with pytest.raises(ValueError):
            validate_critic(payload, ir=_ir(), dispositions=_critic_destinations())
