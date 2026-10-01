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
_NUMBER_RE = re.compile(r"(?<![A-Za-z0-9])\d+(?:\.\d+)?")
_NUMERIC_UNIT_RE = re.compile(
    r"(?<![A-Za-z0-9])(\d+(?:\.\d+)?)\s*"
    r"(bps|basis\s+points|%|million|billion|基点|万|亿)(?![A-Za-z])",
    re.IGNORECASE,
)
_THRESHOLD_VALUE = r"(?P<number>\d+(?:\.\d+)?)\s*(?P<unit>billion|million|%|bps|亿|万)(?![A-Za-z])"
_CURRENCY_PREFIX = r"(?P<currency>(?-i:[A-Z]{3}))?\s*"
_THRESHOLD_PREFIX_RE = re.compile(
    rf"(?P<direction>no\s+less\s+than|not\s+less\s+than|no\s+more\s+than|"
    rf"less\s+than|below|under|低于|小于|不足|"
    rf"more\s+than|greater\s+than|at\s+least|at\s+most|不低于|不少于)\s*"
    rf"{_CURRENCY_PREFIX}{_THRESHOLD_VALUE}",
    re.IGNORECASE,
)
_THRESHOLD_SUFFIX_RE = re.compile(
    rf"{_CURRENCY_PREFIX}{_THRESHOLD_VALUE}\s*(?P<direction>or\s+more|or\s+less|及以上|或以上|及以下|或以下)",
    re.IGNORECASE,
)
_MEASUREMENT_EVIDENCE_TERMS = {
    "基金收益率": ("return", "returns", "收益率", "总收益"),
    "非标剩余期限": ("remaining maturity", "remaining term", "held-to-maturity", "buy and maintain", "剩余期限"),
}


def _normalize_evidence(value: str) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def _numeric_units(value: str) -> Set[tuple[str, str]]:
    return {
        (
            number,
            "bps" if unit.lower().startswith("basis") else re.sub(r"\s+", "", unit.lower()),
        )
        for number, unit in _NUMERIC_UNIT_RE.findall(value)
    }


def _conditional_thresholds(value: str) -> Set[tuple[str, str, str, str]]:
    thresholds: Set[tuple[str, str, str, str]] = set()
    for pattern in (_THRESHOLD_PREFIX_RE, _THRESHOLD_SUFFIX_RE):
        for match in pattern.finditer(value):
            direction = re.sub(r"\s+", " ", match.group("direction").lower())
            relation = "below" if direction in {
                "less than", "below", "under", "低于", "小于", "不足",
                "no more than", "at most", "or less", "及以下", "或以下",
            } else "above"
            thresholds.add((
                match.group("number"),
                match.group("unit").lower(),
                relation,
                match.group("currency") or "",
            ))
    return thresholds


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

        measurement_terms = _MEASUREMENT_EVIDENCE_TERMS.get(metric.metric_name, ())
        downgraded_measurement = bool(
            measurement_terms
            and level in {"DIRECT", "STRONG_INFERRED"}
            and not any(
                phrase_in_text(quote.text, term)
                for quote in evidence
                for term in measurement_terms
            )
        )
        if downgraded_measurement:
            level = "REJECTED" if metric.metric_name == "基金收益率" else "WEAK_INFERRED"

        confidence = item.get("confidence")
        try:
            confidence_float = max(0.0, min(1.0, float(confidence)))
        except Exception:
            confidence_float = 0.0
        if downgraded_direct:
            confidence_float = min(confidence_float, 0.85)
        if downgraded_measurement:
            confidence_float = min(confidence_float, 0.3 if level == "REJECTED" else 0.6)

        reason = str(item.get("reason") or "").strip()
        if downgraded_direct and not downgraded_measurement:
            note = "Python校验：证据表明指标概念相关，但未形成明确的指标目标、约束、限额或监控要求，因此由 DIRECT 降为 STRONG_INFERRED。"
            reason = f"{reason} {note}".strip()
        if downgraded_measurement:
            note = (
                "引用条款只说明现金流或增长意向，未支持组合收益率这一测量对象；不纳入结果。"
                if metric.metric_name == "基金收益率"
                else "引用条款只说明资产类别，未支持剩余期限这一测量对象；降为待确认。"
            )
            reason = f"{reason} Python校验：{note}".strip()

        match = MetricMatch(
            raw_row_id=row_id,
            metric_name=metric.metric_name,
            match_level=level,
            confidence=confidence_float,
            reason=reason,
            evidence=evidence,
        )
        seen.add(row_id)
        if level == "DIRECT":
            selected.append(match)
        elif level in {"STRONG_INFERRED", "WEAK_INFERRED"}:
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
        numbers = set(_NUMBER_RE.findall(requirement))
        units = _numeric_units(requirement)
        quoted_numbers = set().union(*(set(_NUMBER_RE.findall(item.text)) for item in evidence))
        quoted_units = set().union(*(_numeric_units(item.text) for item in evidence))
        thresholds = _conditional_thresholds(requirement)
        quoted_thresholds = set().union(*(_conditional_thresholds(item.text) for item in evidence))
        missing_threshold = any(
            not any(
                required[:3] == quoted[:3]
                and (not required[3] or required[3] == quoted[3])
                for quoted in quoted_thresholds
            )
            for required in thresholds
        )
        if (
            not numbers.issubset(quoted_numbers)
            or not units.issubset(quoted_units)
            or missing_threshold
        ):
            evidence = []
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
        summary=(
            f"依据原文与指标库，识别出 {len(selected)} 项建议匹配指标、"
            f"{len(review)} 项待确认指标和 {len(gaps)} 项指标库缺口。"
        ),
    )
