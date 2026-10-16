from __future__ import annotations

import json
import re
import unicodedata
from decimal import Decimal, InvalidOperation
from typing import Any, Iterable

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.models import RequirementConstraint, RequirementDraft


_COMPARATIVE_OPERATORS = {
    "<", "<=", ">", ">=", "=", "==",
    "LT", "LTE", "GT", "GTE", "EQ",
}
_BETWEEN_OPERATORS = {"BETWEEN", "RANGE"}


def _normalize_text(value: str) -> str:
    norm = unicodedata.normalize("NFKC", str(value or ""))
    norm = re.sub(r"[\u00ad\u2010\u2011\u2012\u2013\u2014\u2015\u2212\uff0d]", "-", norm)
    norm = re.sub(r"(?<=\w)[ \t]*-[ \t]*\r?\n[ \t]*(?=\w)", "-", norm)
    norm = re.sub(r"(\d+)\s+%", r"\1%", norm)
    return re.sub(r"\s+", " ", norm).strip().casefold()


def _relaxed_key(value: str) -> str:
    norm = _normalize_text(value)
    return re.sub(r"[^a-z0-9%<>=.]+", "", norm)


def is_text_grounded_in_evidence(needle: str, haystack: str) -> bool:
    if not needle:
        return True
    norm_needle = _normalize_text(needle)
    norm_haystack = _normalize_text(haystack)
    if not norm_needle:
        return True
    if norm_needle in norm_haystack:
        return True
    rel_needle = _relaxed_key(norm_needle)
    rel_haystack = _relaxed_key(norm_haystack)
    if rel_needle and rel_needle in rel_haystack:
        return True
    return False

def _scalar_text(value: Any) -> str | None:
    if value is None or isinstance(value, bool) or isinstance(value, (dict, list, tuple, set)):
        return None
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def _numeric(value: Any) -> Decimal | None:
    if isinstance(value, bool) or value is None:
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        return None


def _evidence_text(requirement: RequirementDraft, clauses_by_id: dict[str, DocumentClause]) -> str:
    return " ".join(
        clauses_by_id[clause_id].text
        for clause_id in requirement.evidence.clause_ids
        if clause_id in clauses_by_id
    )


def _validate_constraint_shape(constraint: RequirementConstraint, *, owner: str) -> None:
    operator = str(constraint.operator or "").strip().upper()
    if operator in _COMPARATIVE_OPERATORS and constraint.value is None:
        if not (constraint.benchmark or "").strip() and not (constraint.formula or "").strip():
            raise ValueError(f"{owner} comparative constraint requires value, benchmark or formula")
        if not constraint.raw_value_text:
            raise ValueError(f"{owner} symbolic comparison requires raw_value_text")
    if operator in _BETWEEN_OPERATORS:
        if constraint.value is None or constraint.value_to is None:
            raise ValueError(f"{owner} range constraint requires value and value_to")
        left = _numeric(constraint.value)
        right = _numeric(constraint.value_to)
        if left is not None and right is not None and right < left:
            raise ValueError(f"{owner} range constraint has value_to < value")

    if (constraint.value is not None or constraint.value_to is not None) and not constraint.raw_value_text:
        raise ValueError(f"{owner} quantitative constraint requires raw_value_text")


def _validate_constraint_provenance(
    constraint: RequirementConstraint,
    *,
    evidence_text: str,
    owner: str,
) -> None:
    raw_value_text = constraint.raw_value_text or ""
    if raw_value_text and not is_text_grounded_in_evidence(raw_value_text, evidence_text):
        raise ValueError(f"{owner} raw_value_text is not present in evidence")
    if constraint.value is None and str(constraint.operator or "").strip().upper() in _COMPARATIVE_OPERATORS:
        benchmark = constraint.benchmark or ""
        if benchmark and not is_text_grounded_in_evidence(benchmark, evidence_text):
            raise ValueError(f"{owner} benchmark is not present in evidence")

    # Verify scalar values are grounded in the copied raw value span. This is
    # deliberately lexical only: Python does not infer financial semantics,
    # rating order, percentage validity, or unit conversions.
    source_for_values = raw_value_text or evidence_text
    for label, value in (("value", constraint.value), ("value_to", constraint.value_to)):
        token = _scalar_text(value)
        if token is None:
            continue
        if not is_text_grounded_in_evidence(token, source_for_values):
            raise ValueError(f"{owner} {label} is not present in raw evidence text")

def validate_requirement_constraints(
    requirements: Iterable[RequirementDraft],
    *,
    clauses: Iterable[DocumentClause],
) -> None:
    """Fail closed on structurally or textually ungrounded constraint fields.

    This validator never decides what a clause *means*. It only verifies that
    model-supplied normalized values are internally complete and traceable to
    the Python-owned canonical evidence selected by that Requirement.
    """

    clauses_by_id = {clause.clause_id: clause for clause in clauses}
    for requirement in requirements:
        constraint = requirement.constraint
        if constraint is None:
            continue
        owner = f"requirement {requirement.local_id}"
        evidence_text = _evidence_text(requirement, clauses_by_id)
        try:
            _validate_constraint_shape(constraint, owner=owner)
            _validate_constraint_provenance(constraint, evidence_text=evidence_text, owner=owner)
        except ValueError as exc:
            context = json.dumps({
                "constraint": constraint.model_dump(exclude_none=True),
                "evidence_text": evidence_text,
            }, ensure_ascii=False, separators=(",", ":"))
            raise ValueError(f"{exc}; original constraint and evidence: {context}") from exc
