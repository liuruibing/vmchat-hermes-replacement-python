from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.models import CoverageReview, RequirementIR


# These are recall hints only. They must never create a Requirement or assign a
# business meaning without model review.
_NUMERIC_RE = re.compile(
    r"(?:\b\d+(?:\.\d+)?\s*(?:%|bps?|bp|days?|years?|months?|million|billion)\b|"
    r"(?:RMB|CNY|USD|EUR|HKD)\s*\d+(?:\.\d+)?)",
    re.I,
)
_COMPARATOR_RE = re.compile(
    r"(?:<=|>=|<|>|≤|≥|\b(?:not\s+exceed|no\s+more\s+than|at\s+least|at\s+most|"
    r"less\s+than|more\s+than|in\s+excess\s+of)\b)",
    re.I,
)
_OBLIGATION_RE = re.compile(
    r"\b(?:shall|must|may\s+only|is\s+not\s+permitted|are\s+not\s+permitted|"
    r"should\s+target|is\s+subject\s+to|are\s+subject\s+to|required\s+to)\b",
    re.I,
)
_CONDITION_RE = re.compile(r"\b(?:if|unless|except|exception|provided\s+that|subject\s+to)\b", re.I)


def build_coverage_hints(clauses: Sequence[DocumentClause]) -> List[Dict[str, object]]:
    """Return generic high-recall review hints without assigning semantics.

    This intentionally does not know metric names, asset classes or sample
    clauses. Its only job is to help the AI reviewer notice places where a
    silent omission would be costly.
    """

    hints: List[Dict[str, object]] = []
    for clause in clauses:
        signals: List[str] = []
        text = clause.text
        if _NUMERIC_RE.search(text):
            signals.append("numeric_or_unit")
        if _COMPARATOR_RE.search(text):
            signals.append("comparison_or_threshold")
        if _OBLIGATION_RE.search(text):
            signals.append("obligation_or_prohibition")
        if _CONDITION_RE.search(text):
            signals.append("condition_or_exception")
        if signals:
            hints.append(
                {
                    "clause_id": clause.clause_id,
                    "page": clause.page,
                    "signals": signals,
                }
            )
    return hints


def validate_coverage_review(
    payload: dict,
    *,
    clauses: Sequence[DocumentClause],
    requirement_ir: RequirementIR,
) -> CoverageReview:
    review = CoverageReview.model_validate(payload)
    known_clause_ids = {clause.clause_id for clause in clauses}
    known_requirement_ids = {
        requirement.requirement_id for requirement in requirement_ir.requirements
    }

    missing_ids = [item.clause_id for item in review.missing_clauses]
    if len(set(missing_ids)) != len(missing_ids):
        raise ValueError("coverage review contains duplicate missing clause_id")
    unknown_missing = [item for item in missing_ids if item not in known_clause_ids]
    if unknown_missing:
        raise ValueError(
            "coverage review contains unknown missing clause_id: "
            + ", ".join(unknown_missing)
        )

    partial_ids = [item.requirement_id for item in review.partial_requirements]
    if len(set(partial_ids)) != len(partial_ids):
        raise ValueError("coverage review contains duplicate partial requirement_id")
    unknown_requirements = [
        item for item in partial_ids if item not in known_requirement_ids
    ]
    if unknown_requirements:
        raise ValueError(
            "coverage review contains unknown requirement_id: "
            + ", ".join(unknown_requirements)
        )

    for partial in review.partial_requirements:
        if len(set(partial.related_clause_ids)) != len(partial.related_clause_ids):
            raise ValueError(
                f"coverage review {partial.requirement_id} contains duplicate related_clause_ids"
            )
        unknown = [
            clause_id
            for clause_id in partial.related_clause_ids
            if clause_id not in known_clause_ids
        ]
        if unknown:
            raise ValueError(
                f"coverage review {partial.requirement_id} contains unknown related clause_id: "
                + ", ".join(unknown)
            )
    return review


def unresolved_clause_ids(review: CoverageReview) -> set[str]:
    result = {item.clause_id for item in review.missing_clauses}
    for item in review.partial_requirements:
        result.update(item.related_clause_ids)
    return result


def requirements_covering_clause(
    requirement_ir: RequirementIR, clause_id: str
) -> List[str]:
    return [
        item.requirement_id
        for item in requirement_ir.requirements
        if clause_id in item.evidence.clause_ids
    ]
