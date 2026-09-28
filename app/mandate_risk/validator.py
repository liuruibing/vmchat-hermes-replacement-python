from __future__ import annotations

from typing import Any, Dict, Iterable, List

from app.mandate_risk.models import EvidenceQuote, LibraryGap, MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry


_ALLOWED_LEVELS = {"DIRECT", "STRONG_INFERRED", "WEAK_INFERRED", "REJECTED"}


def _quote_exists(document_text: str, quote: str) -> bool:
    return bool(quote and quote.strip() and quote.strip() in document_text)


def validate_model_result(
    *,
    payload: Dict[str, Any],
    registry: RawRiskMetricRegistry,
    allowed_row_ids: Iterable[int],
    document_text: str,
    document_name: str,
    strategy_type: str,
) -> RiskAnalysisResult:
    allowed = {int(item) for item in allowed_row_ids}
    selected: List[MetricMatch] = []
    review: List[MetricMatch] = []
    rejected: List[MetricMatch] = []
    seen: set[int] = set()

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

        evidence: List[EvidenceQuote] = []
        for raw_quote in item.get("evidence") or []:
            if isinstance(raw_quote, str):
                text = raw_quote
                page = None
            elif isinstance(raw_quote, dict):
                text = str(raw_quote.get("text") or "")
                page = raw_quote.get("page")
            else:
                continue
            if _quote_exists(document_text, text):
                evidence.append(EvidenceQuote(text=text.strip(), page=page))

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
            if isinstance(raw_quote, str):
                text = raw_quote
                page = None
            elif isinstance(raw_quote, dict):
                text = str(raw_quote.get("text") or "")
                page = raw_quote.get("page")
            else:
                continue
            if _quote_exists(document_text, text):
                evidence.append(EvidenceQuote(text=text.strip(), page=page))
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
