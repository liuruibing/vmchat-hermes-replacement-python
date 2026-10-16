from __future__ import annotations

import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.constraint_validator import (
    is_text_grounded_in_evidence,
    validate_requirement_constraints,
)
from app.mandate_risk_v2.models import (
    EvidenceRef,
    RequirementConstraint,
    RequirementDraft,
)


def test_hyphen_line_break_and_whitespace_grounding():
    raw = "shall not exceed 100% of the market value of the Sub-Portfolio"
    ev_broken = (
        "9.7. Single-Name Concentration Limits\n"
        "During the portfolio build-up stage: \n"
        "The exposure to any single security shall not exceed 100% of the market value of the Sub- \n"
        "Portfolio."
    )
    assert is_text_grounded_in_evidence(raw, ev_broken)

    # Various PDF hyphen and whitespace variations
    assert is_text_grounded_in_evidence(
        raw,
        "shall not exceed 100 % of the market value of the Sub -\nPortfolio",
    )
    assert is_text_grounded_in_evidence(
        raw,
        "shall not exceed 100% of the market value of the Sub\u2011\r\n  Portfolio",
    )
    assert is_text_grounded_in_evidence(
        raw,
        "shall not exceed 100% of the market value of the Sub\xad\nPortfolio",
    )


def test_validate_requirement_constraints_with_broken_hyphen():
    clauses = [
        DocumentClause(
            clause_id="c0085",
            page=5,
            text="The Sub-Portfolio is subject to the below specific investment restrictions:",
        ),
        DocumentClause(
            clause_id="c0099",
            page=6,
            text="9.7. Single-Name Concentration Limits\nDuring the portfolio build-up stage: \nThe exposure to any single security shall not exceed 100% of the market value of the Sub- \nPortfolio.",
        ),
    ]

    draft = RequirementDraft(
        local_id="r13",
        requirement_type="QUANTITATIVE_LIMIT",
        semantic_summary="Single security exposure limit during build-up",
        subject={"text": "single security exposure"},
        measurement={"concept": "Concentration", "object": "single security"},
        constraint=RequirementConstraint(
            operator="<=",
            value=100,
            unit="%",
            raw_value_text="shall not exceed 100% of the market value of the Sub-Portfolio",
        ),
        evidence=EvidenceRef(clause_ids=["c0085", "c0099"]),
        attributes={"source_heading": "9.7. Single-Name Concentration Limits"},
    )

    # Should succeed without ValueError
    validate_requirement_constraints([draft], clauses=clauses)


def test_validate_requirement_constraints_fails_on_genuine_hallucination():
    clauses = [
        DocumentClause(
            clause_id="c0099",
            page=6,
            text="The exposure to any single security shall not exceed 100% of the market value.",
        ),
    ]

    draft_fake_value = RequirementDraft(
        local_id="r1",
        requirement_type="QUANTITATIVE_LIMIT",
        semantic_summary="Fake threshold",
        constraint=RequirementConstraint(
            operator="<=",
            value=50,
            unit="%",
            raw_value_text="shall not exceed 50%",
        ),
        evidence=EvidenceRef(clause_ids=["c0099"]),
    )
    with pytest.raises(ValueError, match="raw_value_text is not present in evidence"):
        validate_requirement_constraints([draft_fake_value], clauses=clauses)
