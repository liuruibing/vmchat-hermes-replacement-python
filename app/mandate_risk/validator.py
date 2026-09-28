from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Mapping, Set

from app.mandate_risk.clauses import DocumentClause, split_document_clauses
from app.mandate_risk.models import EvidenceQuote, LibraryGap, MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry


_ALLOWED_LEVELS = {"DIRECT", "STRONG_INFERRED", "WEAK_INFERRED", "REJECTED"}


def _normalize_evidence(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _quote_exists(document_text: str, quote: str) -> bool:
    return bool(quote and quote.strip() and quote.strip() in document_text)


def _find_clause_for_quote(clauses: Iterable[DocumentClause], quote: str) -> DocumentClause | None:
    raw = str(quote or "").strip()
    if not raw:
        return None
    normalized = _normalize_evidence(raw)
    for clause in clauses:
        if raw in clause.text or normalized in _normalize_evidence(clause.text):
            return clause
    return None


def _canonical_evidence(
    raw_quote: Any,
    *,
    clauses: List[DocumentClause],
    clause_by_id: Mapping[str, DocumentClause],
    allowed_clause_ids: Set[str] | None = None,
) -> EvidenceQuote | None:
    if isinstance(raw_quote, str):
        text = raw_quote
        clause_id = None
        page = None
    elif isinstance(raw_quote, dict):
        text = str(raw_quote.get("text") or "")
        clause_id = str(raw_quote.get("clause_id") or "").strip() or None
        page = raw_quote.get("page")
    else:
        return None

    clause: DocumentClause | None = None
    if clause_id:
        clause = clause_by_id.get(clause_id)
        if clause is None:
            return None
        supplied = _normalize_evidence(text)
        canonical = _normalize_evidence(clause.text)
        if supplied and supplied not in canonical and canonical not in supplied:
            return None
    else:
        clause = _find_clause_for_quote(clauses, text)
        if clause is None:
            return None
        clause_id = clause.clause_id

    if allowed_clause_ids is not None and clause_id not in allowed_clause_ids:
        return None

    return EvidenceQuote(
        text=clause.text,
        page=page,
        clause_id=clause.clause_id,
        source_start=clause.source_start,
        source_end=clause.source_end,
    )


def validate_model_result(
    *,
    payload: Dict[str, Any],
    registry: RawRiskMetricRegistry,
    allowed_row_ids: Iterable[int],
    document_text: str,
    document_name: str,
    strategy_type: str,
    candidate_clause_ids: Mapping[int, Iterable[str]] | None = None,
) -> RiskAnalysisResult:
    allowed = {int(item) for item in allowed_row_ids}
    selected: List[MetricMatch] = []
    review: List[MetricMatch] = []
    rejected: List[MetricMatch] = []
    seen: set[int] = set()

    clauses = split_document_clauses(document_text)
    clause_by_id = {item.clause_id: item for item in clauses}
    metric_clause_map: Dict[int, Set[str]] = {
        int(row_id): {str(item) for item in values}
        for row_id, values in (candidate_clause_ids or {}).items()
    }

    matches = payload.get("matches") if isinstance(payload, dict) else []
    for item in matches or []:
        if not isinstance(item, dict):
            continue
        try:
            row_id = int(item.get("raw_row_id"))
        except Exception:
            continue
        if row_id in seen or row_id not in allowed:
            continue
        metric = registry.get(row_id)
        if metric is None:
            continue
        if str(item.get("metric_name") or "") != metric.metric_name:
            continue

        level = str(item.get("match_level") or "").upper()
        if level not in _ALLOWED_LEVELS:
            continue

        allowed_evidence_clauses = metric_clause_map.get(row_id)
        evidence: List[EvidenceQuote] = []
        for raw_quote in item.get("evidence") or []:
            canonical = _canonical_evidence(
                raw_quote,
                clauses=clauses,
                clause_by_id=clause_by_id,
                allowed_clause_ids=allowed_evidence_clauses if candidate_clause_ids is not None else None,
            )
            if canonical is not None and canonical not in evidence:
                evidence.append(canonical)

        # A non-rejected metric must cite one of the clauses Python itself
        # associated with that metric. Merely quoting any sentence from the
        # document is not enough.
        if level != "REJECTED" and not evidence:
            level = "REJECTED"

        confidence = item.get("confidence")
        try:
            confidence_float = max(0.0, min(1.0, float(confidence)))
        except Exception:
            confidence_float = 0.0

        match = MetricMatch(
            raw_row_id=row_id,
            metric_name=metric.metric_name,
            match_level=level,
            confidence=confidence_float,
            reason=str(item.get("reason") or "").strip(),
            evidence=evidence,
        )
        seen.add(row_id)
        if level in {"DIRECT", "STRONG_INFERRED"}:
            selected.append(match)
        elif level == "WEAK_INFERRED":
            review.append(match)
        else:
            rejected.append(match)

    gaps: List[LibraryGap] = []
    for raw_gap in (payload.get("gaps") if isinstance(payload, dict) else []) or []:
        if not isinstance(raw_gap, dict):
            continue
        evidence: List[EvidenceQuote] = []
        for raw_quote in raw_gap.get("evidence") or []:
            canonical = _canonical_evidence(
                raw_quote,
                clauses=clauses,
                clause_by_id=clause_by_id,
                allowed_clause_ids=None,
            )
            if canonical is not None and canonical not in evidence:
                evidence.append(canonical)
        requirement = str(raw_gap.get("requirement") or "").strip()
        if requirement and evidence:
            gaps.append(
                LibraryGap(
                    requirement=requirement,
                    reason=str(raw_gap.get("reason") or "").strip(),
                    evidence=evidence,
                )
            )

    return RiskAnalysisResult(
        document_name=document_name,
        strategy_type=strategy_type,
        selected_metrics=selected,
        review_metrics=review,
        rejected_metrics=rejected,
        library_gaps=gaps,
        summary=str(payload.get("summary") or "").strip() if isinstance(payload, dict) else "",
    )
