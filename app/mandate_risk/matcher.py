from __future__ import annotations

import re
from typing import Iterable, List, Tuple

from app.mandate_risk.clauses import DocumentClause, split_document_clauses
from app.mandate_risk.models import CandidateClauseHint, MetricCandidate, RawRiskMetric


_EQUITY_HINTS = (
    "a-share", "a share", "listed equity", "common shares", "stock", "equity",
    "dividend", "benchmark index", "沪深", "股票", "权益",
)
_FIXED_HINTS = (
    "bond", "credit securities", "credit risk", "duration", "dv01", "yield spread",
    "债券", "固收", "久期", "信用",
)
_GENERIC_MANDATE = {
    "long term capital growth",
    "actively managed",
    "active management",
    "capital management",
}


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
        token for token in re.findall(r"[a-z][a-z0-9+-]{2,}", normalize_text(value))
        if token not in {"the", "and", "with", "from", "into", "over", "for", "that", "this"}
    }


def _fragment_score(clause_norm: str, fragment: str) -> float:
    weight = 0.45 if fragment in _GENERIC_MANDATE else 1.0
    if fragment in clause_norm:
        return 6.0 * weight
    frag_words = _english_words(fragment)
    if not frag_words:
        return 0.0
    clause_words = _english_words(clause_norm)
    overlap = len(clause_words & frag_words) / max(1, len(frag_words))
    if overlap >= 0.75:
        return 4.0 * overlap * weight
    if overlap >= 0.45:
        return 2.0 * overlap * weight
    return 0.0


def _score_clause(clause: DocumentClause, metric: RawRiskMetric) -> tuple[float, List[str]]:
    text = normalize_text(clause.text)
    score = 0.0
    hits: List[str] = []

    metric_name = normalize_text(metric.metric_name)
    if metric_name and metric_name in text:
        score += 8.0
        hits.append(metric.metric_name)

    fragment_results = [(fragment, _fragment_score(text, fragment)) for fragment in _mandate_fragments(metric.mandate)]
    fragment_results = [(fragment, value) for fragment, value in fragment_results if value > 0]
    if fragment_results:
        fragment, value = max(fragment_results, key=lambda item: item[1])
        score += value
        hits.append(fragment)

    algorithm = normalize_text(metric.algorithm)
    if algorithm and len(algorithm) <= 80 and algorithm in text:
        score += 2.0
        hits.append(metric.algorithm)

    return score, hits


def score_metric(document_text: str, metric: RawRiskMetric) -> MetricCandidate:
    clauses = split_document_clauses(document_text)
    scored: List[tuple[float, DocumentClause, List[str]]] = []
    for clause in clauses:
        score, hits = _score_clause(clause, metric)
        if score > 0:
            scored.append((score, clause, hits))
    scored.sort(key=lambda item: (-item[0], item[1].clause_id))

    best_score = scored[0][0] if scored else 0.0
    hits: List[str] = []
    hints: List[CandidateClauseHint] = []
    for score, clause, clause_hits in scored[:3]:
        for hit in clause_hits:
            if hit not in hits:
                hits.append(hit)
        hints.append(CandidateClauseHint(clause_id=clause.clause_id, text=clause.text, score=round(score, 4)))

    return MetricCandidate(
        raw_row_id=metric.row_id,
        metric_name=metric.metric_name,
        deterministic_score=round(best_score, 4),
        exact_hits=hits[:5],
        matched_clauses=hints,
    )


def build_candidates(document_text: str, metrics: Iterable[RawRiskMetric]) -> List[MetricCandidate]:
    candidates = [score_metric(document_text, metric) for metric in metrics]
    return sorted(candidates, key=lambda item: (-item.deterministic_score, item.raw_row_id))
