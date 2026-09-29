import pytest

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS
from app.mandate_risk_v2.mapping_validator import (
    validate_batch,
    validate_critic,
    validate_dispositions,
)
from app.mandate_risk_v2.models import Definition, EvidenceRef, Requirement, RequirementIR


def _fixture():
    ir = RequirementIR(document_name="new.pdf", requirements=[
        Requirement(
            requirement_id="REQ-0001", requirement_type="QUANTITATIVE_LIMIT",
            semantic_summary="Portfolio exposure cap", evidence=EvidenceRef(clause_ids=["c0001"]),
        ),
    ])
    registry = RawRiskMetricRegistry([
        RawRiskMetric(row_id=2, source_row=2, metric_name="New Exposure Measure",
                      algorithm="exposure / NAV"),
        RawRiskMetric(row_id=3, source_row=3, metric_name="Unrelated New Measure",
                      algorithm="turnover / AUM"),
    ])
    return ir, registry


def _matrix(*, relation="EQUIVALENT"):
    return [
        {
            "dimension": dimension,
            "requirement_basis": f"requirement {dimension}",
            "metric_basis": f"metric {dimension}",
            "relation": relation,
            "reason": "audited",
        }
        for dimension in CORE_COMPATIBILITY_DIMENSIONS
    ]


def _link(relation="EQUIVALENT", *, level="DIRECT", row_id=2):
    return {
        "requirement_id": "REQ-0001", "raw_row_id": row_id, "level": level,
        "compatibility": _matrix(relation=relation),
        "evidence_clause_ids": ["c0001"], "reason": "directly measurable",
    }


def _batch_payload(link):
    return {"links": [link], "row_assessments": [
        {"raw_row_id": 2, "outcome": "LINKED" if link["raw_row_id"] == 2 else "NOT_RELEVANT",
         "reason": "audited"},
        {"raw_row_id": 3, "outcome": "LINKED" if link["raw_row_id"] == 3 else "NOT_RELEVANT",
         "reason": "audited"},
    ]}


def test_direct_requires_complete_structural_matrix_and_real_evidence():
    ir, registry = _fixture()
    payload = _batch_payload(_link())
    assert len(validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3}).links) == 1

    payload = _batch_payload(_link())
    payload["links"][0]["compatibility"] = [
        item for item in payload["links"][0]["compatibility"]
        if item["dimension"] != "annualisation"
    ]
    with pytest.raises(ValueError, match="missing core dimensions.*annualisation"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})

    payload = _batch_payload(_link())
    payload["links"][0]["compatibility"][0]["relation"] = "INSUFFICIENT"
    with pytest.raises(ValueError, match="DIRECT.*compatibility"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})

    payload = _batch_payload(_link())
    payload["links"][0]["evidence_clause_ids"] = ["c9999"]
    with pytest.raises(ValueError, match="evidence"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})


def test_empty_algorithm_cannot_supply_equivalent_direct_algorithm_basis():
    ir, _ = _fixture()
    registry = RawRiskMetricRegistry([
        RawRiskMetric(row_id=2, source_row=2, metric_name="No Algorithm", algorithm=""),
        RawRiskMetric(row_id=3, source_row=3, metric_name="Other", algorithm="turnover"),
    ])
    with pytest.raises(ValueError, match="algorithm_semantics.*empty"):
        validate_batch(_batch_payload(_link()), ir=ir, registry=registry, batch_row_ids={2, 3})


def test_definition_clause_may_support_but_not_replace_requirement_evidence():
    ir, registry = _fixture()
    ir.definitions.append(Definition(definition_id="DEF-0001", term="NAV",
                                     semantic_summary="Net asset value",
                                     evidence=EvidenceRef(clause_ids=["c0002"])))
    payload = _batch_payload(_link())
    payload["links"][0]["evidence_clause_ids"] = ["c0001", "c0002"]
    assert validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3}).links
    payload["links"][0]["evidence_clause_ids"] = ["c0002"]
    with pytest.raises(ValueError, match="requirement.*evidence"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})


def test_unrelated_requirement_clause_cannot_be_used_as_supporting_evidence():
    ir, registry = _fixture()
    ir.requirements.append(Requirement(
        requirement_id="REQ-0002", requirement_type="QUANTITATIVE_LIMIT",
        semantic_summary="Unrelated issuer cap", evidence=EvidenceRef(clause_ids=["c0003"]),
    ))
    payload = _batch_payload(_link())
    payload["links"][0]["evidence_clause_ids"] = ["c0001", "c0003"]
    with pytest.raises(ValueError, match="unrelated requirement"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})


def test_dispositions_can_partition_one_requirement_and_critic_checks_all_direct_and_gaps():
    ir, registry = _fixture()
    links = validate_batch(_batch_payload(_link()), ir=ir, registry=registry,
                           batch_row_ids={2, 3}).links
    dispositions = validate_dispositions({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "two aspects", "destinations": [
            {"destination": "MAIN_TABLE", "raw_row_ids": [2], "evidence_clause_ids": ["c0001"],
             "aspect": "portfolio exposure", "reason": "algorithm matches"},
            {"destination": "LIBRARY_GAP", "raw_row_ids": [], "evidence_clause_ids": ["c0001"],
             "aspect": "issuer exposure", "reason": "no equivalent metric"},
        ],
    }]}, ir=ir, registry=registry, links=links)
    with pytest.raises(ValueError, match="critic.*missing"):
        validate_critic({"verdicts": [{"requirement_id": "REQ-0001", "destination": "MAIN_TABLE",
            "raw_row_id": 2, "aspect": "portfolio exposure", "verdict": "CONFIRM",
            "reason": "verified", "evidence_clause_ids": ["c0001"]}]},
            ir=ir, dispositions=dispositions)


def test_pending_review_metric_rows_require_review_links():
    ir, registry = _fixture()
    rejected = _link(level="REJECTED")
    rejected["compatibility"] = [{
        "dimension": "measurement_object", "requirement_basis": "exposure",
        "metric_basis": "turnover", "relation": "CONFLICT", "reason": "different object",
    }]
    links = validate_batch(_batch_payload(rejected), ir=ir, registry=registry,
                           batch_row_ids={2, 3}).links
    with pytest.raises(ValueError, match="PENDING_REVIEW.*REVIEW"):
        validate_dispositions({"dispositions": [{
            "requirement_id": "REQ-0001", "reason": "not direct", "destinations": [{
                "destination": "PENDING_REVIEW", "raw_row_ids": [2],
                "evidence_clause_ids": ["c0001"], "aspect": "exposure", "reason": "uncertain",
            }],
        }]}, ir=ir, registry=registry, links=links)

    review_link = _link(level="REVIEW")
    review_link["compatibility"][0]["relation"] = "INSUFFICIENT"
    links = validate_batch(_batch_payload(review_link), ir=ir, registry=registry,
                           batch_row_ids={2, 3}).links
    review = validate_dispositions({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "review", "destinations": [{
            "destination": "PENDING_REVIEW", "raw_row_ids": [2],
            "evidence_clause_ids": ["c0001"], "aspect": "exposure", "reason": "uncertain",
        }],
    }]}, ir=ir, registry=registry, links=links)
    assert review.dispositions[0].destinations[0].destination == "PENDING_REVIEW"


def test_direct_link_cannot_disappear_from_final_destinations():
    ir, registry = _fixture()
    links = validate_batch(_batch_payload(_link()), ir=ir, registry=registry,
                           batch_row_ids={2, 3}).links
    with pytest.raises(ValueError, match="DIRECT.*destination"):
        validate_dispositions({"dispositions": [{"requirement_id": "REQ-0001",
            "reason": "ignored candidate", "destinations": [{
                "destination": "LIBRARY_GAP", "raw_row_ids": [],
                "evidence_clause_ids": ["c0001"], "aspect": "exposure", "reason": "none",
            }]}]}, ir=ir, registry=registry, links=links)
