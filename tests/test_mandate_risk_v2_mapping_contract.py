import pytest

from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
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


def _link(relation="EQUIVALENT"):
    return {
        "requirement_id": "REQ-0001", "raw_row_id": 2, "level": "DIRECT",
        "compatibility": [{"dimension": "denominator", "requirement_basis": "NAV",
                           "metric_basis": "NAV", "relation": relation, "reason": "same basis"}],
        "evidence_clause_ids": ["c0001"], "reason": "directly measurable",
    }


def test_direct_requires_complete_structural_matrix_and_real_evidence():
    ir, registry = _fixture()
    payload = {"links": [_link()], "row_assessments": [
        {"raw_row_id": 2, "outcome": "LINKED", "reason": "candidate"},
        {"raw_row_id": 3, "outcome": "NOT_RELEVANT", "reason": "other object"},
    ]}
    assert len(validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3}).links) == 1
    payload["links"][0]["compatibility"][0]["relation"] = "INSUFFICIENT"
    with pytest.raises(ValueError, match="DIRECT.*compatibility"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})
    payload["links"][0] = _link()
    payload["links"][0]["evidence_clause_ids"] = ["c9999"]
    with pytest.raises(ValueError, match="evidence"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})


def test_definition_clause_may_support_but_not_replace_requirement_evidence():
    ir, registry = _fixture()
    ir.definitions.append(Definition(definition_id="DEF-0001", term="NAV",
                                     semantic_summary="Net asset value",
                                     evidence=EvidenceRef(clause_ids=["c0002"])))
    payload = {"links": [_link()], "row_assessments": [
        {"raw_row_id": 2, "outcome": "LINKED", "reason": "candidate"},
        {"raw_row_id": 3, "outcome": "NOT_RELEVANT", "reason": "other"},
    ]}
    payload["links"][0]["evidence_clause_ids"] = ["c0001", "c0002"]
    assert validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3}).links
    payload["links"][0]["evidence_clause_ids"] = ["c0002"]
    with pytest.raises(ValueError, match="requirement.*evidence"):
        validate_batch(payload, ir=ir, registry=registry, batch_row_ids={2, 3})


def test_dispositions_can_partition_one_requirement_and_critic_checks_all_direct_and_gaps():
    ir, registry = _fixture()
    links = validate_batch({"links": [_link()], "row_assessments": [
        {"raw_row_id": 2, "outcome": "LINKED", "reason": "candidate"},
        {"raw_row_id": 3, "outcome": "NOT_RELEVANT", "reason": "other"},
    ]}, ir=ir, registry=registry, batch_row_ids={2, 3}).links
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


def test_direct_link_cannot_disappear_from_final_destinations():
    ir, registry = _fixture()
    links = validate_batch({"links": [_link()], "row_assessments": [
        {"raw_row_id": 2, "outcome": "LINKED", "reason": "candidate"},
        {"raw_row_id": 3, "outcome": "NOT_RELEVANT", "reason": "other"},
    ]}, ir=ir, registry=registry, batch_row_ids={2, 3}).links
    with pytest.raises(ValueError, match="DIRECT.*destination"):
        validate_dispositions({"dispositions": [{"requirement_id": "REQ-0001",
            "reason": "ignored candidate", "destinations": [{
                "destination": "LIBRARY_GAP", "raw_row_ids": [],
                "evidence_clause_ids": ["c0001"], "aspect": "exposure", "reason": "none",
            }]}]}, ir=ir, registry=registry, links=links)
