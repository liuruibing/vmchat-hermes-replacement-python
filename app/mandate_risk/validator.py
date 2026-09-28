from __future__ import annotations

import re
from typing import Any, Dict, Iterable, List, Mapping, Set

from app.mandate_risk.clauses import DocumentClause, split_document_clauses
from app.mandate_risk.matcher import metric_concept_phrases, phrase_in_text
from app.mandate_risk.models import EvidenceQuote, LibraryGap, MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry


_ALLOWED_LEVELS = {"DIRECT", "STRONG_INFERRED", "WEAK_INFERRED", "REJECTED"}
_DIRECT_REQUIREMENT_EN = re.compile(
    r"\b(?:shall|must|should|target(?:s|ed|ing)?|aim(?:s|ed|ing)?|objective|"
    r"require(?:s|d)?|limit(?:s|ed)?|maintain(?:s|ed)?|keep|is\s+to|"
    r"not\s+exceed|no\s+less\s+than|at\s+least|at\s+most|maximum|minimum)\b",
    re.IGNORECASE,
)
_DIRECT_REQUIREMENT_ZH = re.compile(
    r"(?:应当|应|必须|须|不得|不超过|不低于|至少|至多|目标|限额|限制|保持|维持)"
)


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
    elif isinstance(raw_quote, dict):
        text = str(raw_quote.get("text") or "")
        clause_id = str(raw_quote.get("clause_id") or "").strip() or None
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

    # Page provenance is owned by Python's document runtime / clause splitter.
    # Any page number supplied by the model is ignored so an otherwise valid
    # quote cannot invent or alter its PDF location.
    return EvidenceQuote(
        text=clause.text,
        page=clause.page,
        clause_id=clause.clause_id,
        source_start=clause.source_start,
        source_end=clause.source_end,
    )


def _supports_direct_requirement(metric: Any, evidence: Iterable[EvidenceQuote]) -> bool:
    """Return true only when one evidence clause directly requires the metric concept.

    Definitions, permitted actions, asset descriptions and general strategy prose are
    useful evidence for inferred matches, but they are not enough for DIRECT. A DIRECT
    clause must contain a stable metric concept phrase and requirement/target/limit
    language in the same auditable clause.
    """

    concept_phrases = metric_concept_phrases(metric)
    for quote in evidence:
        text = str(quote.text or "")
        if not any(phrase_in_text(text, phrase) for phrase in concept_phrases):
            continue
        if _DIRECT_REQUIREMENT_EN.search(text) or _DIRECT_REQUIREMENT_ZH.search(text):
            return True
    return False


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

        downgraded_direct = False
        if level == "DIRECT" and evidence and not _supports_direct_requirement(metric, evidence):
            # A concept definition or an allowed adjustment can establish a strong
            # semantic relationship, but not a direct monitoring/limit requirement.
            level = "STRONG_INFERRED"
            downgraded_direct = True

        confidence = item.get("confidence")
        try:
            confidence_float = max(0.0, min(1.0, float(confidence)))
        except Exception:
            confidence_float = 0.0
        if downgraded_direct:
            confidence_float = min(confidence_float, 0.85)

        reason = str(item.get("reason") or "").strip()
        if downgraded_direct:
            note = "Python校验：证据表明指标概念相关，但未形成明确的指标目标、约束、限额或监控要求，因此由 DIRECT 降为 STRONG_INFERRED。"
            reason = f"{reason} {note}".strip()

        match = MetricMatch(
            raw_row_id=row_id,
            metric_name=metric.metric_name,
            match_level=level,
            confidence=confidence_float,
            reason=reason,
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
