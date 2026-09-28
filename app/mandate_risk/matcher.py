from __future__ import annotations

import re
from typing import Iterable, List, Tuple

from app.mandate_risk.models import MetricCandidate, RawRiskMetric


_EQUITY_HINTS = (
    "a-share",
    "a share",
    "listed equity",
    "common shares",
    "stock",
    "equity",
    "dividend",
    "benchmark index",
    "沪深",
    "股票",
    "权益",
)
_FIXED_HINTS = (
    "bond",
    "credit securities",
    "credit risk",
    "duration",
    "dv01",
    "yield spread",
    "债券",
    "固收",
    "久期",
    "信用",
)


def normalize_text(value: str) -> str:
    value = str(value or "").lower()
    value = re.sub(r"[\s\u00a0]+", " ", value)
    value = re.sub(r"[^0-9a-z\u3400-\u9fff%+.-]+", " ", value)
    return value.strip()


def infer_strategy_type(document_text: str) -> Tuple[str, float]:
    text = normalize_text(document_text)
    equity_score = sum(1 for term in _EQUITY_HINTS if term in text)
    fixed_score = sum(1 for term in _FIXED_HINTS if term in text)

    if equity_score and fixed_score:
        if abs(equity_score - fixed_score) <= 1:
            return "混合", 0.7
        if equity_score > fixed_score:
            return "权益", min(0.95, 0.65 + 0.05 * equity_score)
        return "固收", min(0.95, 0.65 + 0.05 * fixed_score)
    if equity_score:
        return "权益", min(0.95, 0.65 + 0.05 * equity_score)
    if fixed_score:
        return "固收", min(0.95, 0.65 + 0.05 * fixed_score)
    return "未知", 0.0


def _mandate_fragments(value: str) -> Iterable[str]:
    for part in re.split(r"[/;\n]+", value or ""):
        item = normalize_text(part)
        if len(item) >= 5:
            yield item


def _english_words(value: str) -> set[str]:
    return {
        token
        for token in re.findall(r"[a-z][a-z0-9+-]{2,}", normalize_text(value))
        if token not in {"the", "and", "with", "from", "into", "over", "for", "that", "this"}
    }


def score_metric(document_text: str, metric: RawRiskMetric) -> MetricCandidate:
    doc = normalize_text(document_text)
    score = 0.0
    hits: List[str] = []

    metric_name_norm = normalize_text(metric.metric_name)
    if metric_name_norm and metric_name_norm in doc:
        score += 8.0
        hits.append(metric.metric_name)

    doc_words = _english_words(doc)
    for fragment in _mandate_fragments(metric.mandate):
        if fragment in doc:
            score += 6.0
            hits.append(fragment)
            continue
        frag_words = _english_words(fragment)
        if frag_words:
            overlap = len(doc_words & frag_words) / max(1, len(frag_words))
            if overlap >= 0.75:
                score += 4.0 * overlap
                hits.append(fragment)
            elif overlap >= 0.45:
                score += 2.0 * overlap

    algorithm_norm = normalize_text(metric.algorithm)
    if algorithm_norm and len(algorithm_norm) <= 80 and algorithm_norm in doc:
        score += 2.0
        hits.append(metric.algorithm)

    return MetricCandidate(
        raw_row_id=metric.row_id,
        metric_name=metric.metric_name,
        deterministic_score=round(score, 4),
        exact_hits=hits[:5],
    )


def build_candidates(document_text: str, metrics: Iterable[RawRiskMetric]) -> List[MetricCandidate]:
    candidates = [score_metric(document_text, metric) for metric in metrics]
    return sorted(candidates, key=lambda item: (-item.deterministic_score, item.raw_row_id))
