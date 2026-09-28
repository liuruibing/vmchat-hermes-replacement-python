from __future__ import annotations

import re
from collections import Counter
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
    "trading strategy",
    "trading strategies",
    "bottom-up",
    "top-down",
}

# Derived search aliases are intentionally separate from the immutable metric
# library. They improve bilingual recall but never overwrite source values.
_DERIVED_ALIASES: dict[str, tuple[str, ...]] = {
    "基金收益率": ("fund return", "portfolio return", "基金收益率"),
    "超额收益率（基准超额）": (
        "excess return", "returns in excess", "return in excess", "outperformance", "超额收益",
    ),
    "Alpha": ("alpha",),
    "股息贡献率": ("dividend contribution", "dividend yield", "stable dividend yield", "股息贡献"),
    "Sortino索提诺": ("sortino", "索提诺"),
    "信息比率": ("information ratio", "信息比率"),
    "VaR": ("value at risk", "var"),
    "最大回撤": ("maximum drawdown", "max drawdown", "最大回撤"),
    "波动率": ("volatility", "波动率"),
    "组合Beta贝塔": ("portfolio beta", "组合beta", "组合贝塔", "beta"),
    "下行Beta": ("downside beta", "下行beta", "下行贝塔"),
    "行业偏离度": ("industry deviation", "sector deviation", "行业偏离"),
    "跟踪误差": ("tracking error", "跟踪误差"),
    "久期": ("duration", "久期"),
    "DV01": ("dv01",),
    "股息支付率NII": ("dividend payout", "payout ratio", "nii", "股息支付"),
    "股息增长率": ("dividend growth", "股息增长"),
    "股息覆盖率": ("dividend coverage", "股息覆盖", "portfolio dividend yield benchmark dividend yield"),
    "境内资产占比": (
        "domestic asset", "chinese issuers", "mainland china listed equity", "china a-share market", "境内资产",
    ),
    "单一证券占比": ("single security", "single stock", "single name concentration", "单一证券"),
    "可用融资余额": ("available financing", "financing balance", "repo capacity", "可用融资余额"),
    "换手率(%)": ("turnover", "换手率"),
    "剩余期限": ("remaining maturity", "remaining term", "剩余期限"),
    "非标剩余期限": ("private credit remaining maturity", "private credit remaining term", "非标剩余期限"),
    "债券资产变现天数": ("bond liquidation days", "days to liquidate bonds", "债券资产变现天数"),
    "流通受限资产占比": ("restricted asset", "locked asset", "lock-up", "流通受限资产"),
    "优质动性资产占比": ("high quality liquid asset", "hqlA", "优质流动性资产", "优质动性资产"),
    "流动性上市权益资产占比": (
        "liquid listed equity", "7 trading days", "10% participation rate", "流动性上市权益资产",
    ),
    "信用利差（债券）": ("credit spread", "bond credit spread", "信用利差"),
    "信用利差（非标）": ("private credit spread", "non-standard credit spread", "非标信用利差"),
    "加权平均信用评级": ("weighted average credit rating", "warf", "加权平均信用评级"),
    "债券AA+及以下评级占比(%)": ("aa+ and below", "aa+ or below", "aa+及以下", "低评级债券占比"),
    "单一发行人集中度": ("single issuer concentration", "issuer concentration", "单一发行人集中度"),
    "区域分布": ("regional distribution", "geographic distribution", "regional allocation", "区域分布"),
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


def _is_specific_mandate_fragment(fragment: str) -> bool:
    fragment = normalize_text(fragment)
    if not fragment:
        return False
    if re.search(r"[\u3400-\u9fff]", fragment):
        return True

    words = _english_words(fragment)
    if len(words) <= 1:
        return False

    # A generic phrase plus at most one modifier is still generic. Fragments
    # that add several concrete terms remain eligible as recall evidence.
    for generic in _GENERIC_MANDATE:
        if generic in fragment:
            residual = normalize_text(fragment.replace(generic, " "))
            if len(_english_words(residual)) <= 1:
                return False
    return True


def _phrase_in_text(text: str, phrase: str) -> bool:
    phrase_norm = normalize_text(phrase)
    if not phrase_norm:
        return False
    # Any single Latin token uses token boundaries. This fixes substring false
    # positives generically (for example VaR must not match "varied").
    if re.fullmatch(r"[a-z0-9+.-]+", phrase_norm):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(phrase_norm)}(?![a-z0-9])", text))
    return phrase_norm in text


def phrase_in_text(text: str, phrase: str) -> bool:
    """Public normalized phrase matcher used by validator guardrails."""

    return _phrase_in_text(normalize_text(text), phrase)


def metric_concept_phrases(metric: RawRiskMetric) -> tuple[str, ...]:
    """Return stable metric-name/alias phrases, excluding Mandate prose."""

    values = [metric.metric_name, *_DERIVED_ALIASES.get(metric.metric_name, ())]
    seen: set[str] = set()
    result: List[str] = []
    for value in values:
        normalized = normalize_text(value)
        if normalized and normalized not in seen:
            seen.add(normalized)
            result.append(value)
    return tuple(result)


def _alias_hits(clause_norm: str, metric: RawRiskMetric) -> List[str]:
    hits: List[str] = []
    for alias in _DERIVED_ALIASES.get(metric.metric_name, (metric.metric_name,)):
        if _phrase_in_text(clause_norm, alias):
            hits.append(alias)
    return hits


def _fragment_score(clause_norm: str, fragment: str) -> float:
    frag_words = _english_words(fragment)
    if not _is_specific_mandate_fragment(fragment):
        return 0.5 if _phrase_in_text(clause_norm, fragment) else 0.0
    if fragment in clause_norm:
        return 4.0
    if not frag_words:
        return 0.0
    clause_words = _english_words(clause_norm)
    overlap = len(clause_words & frag_words) / max(1, len(frag_words))
    # Full lexical coverage of an authoritative phrase is strong recall evidence
    # even when extra words are inserted in the document sentence.
    if overlap >= 1.0:
        return 4.0
    if overlap >= 0.8:
        return 2.5 * overlap
    if overlap >= 0.6:
        return 1.5 * overlap
    return 0.0


def _score_primary_clause(clause: DocumentClause, metric: RawRiskMetric) -> tuple[float, List[str]]:
    """High-precision candidate scoring used by the original matcher."""

    text = normalize_text(clause.text)
    score = 0.0
    hits: List[str] = []
    concept_hit = False

    if _phrase_in_text(text, metric.metric_name):
        score += 10.0
        hits.append(metric.metric_name)
        concept_hit = True

    aliases = _alias_hits(text, metric)
    if aliases:
        score += 8.0
        hits.extend(aliases[:3])
        concept_hit = True

    algorithm = normalize_text(metric.algorithm)
    if algorithm and len(algorithm) <= 80 and algorithm in text:
        score += 3.0
        hits.append(metric.algorithm)
        concept_hit = True

    # Preserve the original precision rule: Mandate text can strengthen an
    # existing concept hit, but shared business wording cannot create a primary
    # candidate by itself.
    if concept_hit:
        fragment_results = [
            (fragment, _fragment_score(text, fragment))
            for fragment in _mandate_fragments(metric.mandate)
        ]
        fragment_results = [(fragment, value) for fragment, value in fragment_results if value > 0]
        if fragment_results:
            fragment, value = max(fragment_results, key=lambda item: item[1])
            score += value
            hits.append(fragment)

    return score, hits


def _candidate_from_scored_clauses(
    metric: RawRiskMetric,
    scored: List[tuple[float, DocumentClause, List[str]]],
    *,
    recall_source: str = "primary",
) -> MetricCandidate:
    scored.sort(key=lambda item: (-item[0], item[1].clause_id))
    best_score = scored[0][0] if scored else 0.0
    hits: List[str] = []
    hints: List[CandidateClauseHint] = []
    for score, clause, clause_hits in scored[:3]:
        for hit in clause_hits:
            if hit not in hits:
                hits.append(hit)
        hints.append(
            CandidateClauseHint(
                clause_id=clause.clause_id,
                text=clause.text,
                score=round(score, 4),
                source_start=clause.source_start,
                source_end=clause.source_end,
                page=clause.page,
            )
        )

    return MetricCandidate(
        raw_row_id=metric.row_id,
        metric_name=metric.metric_name,
        deterministic_score=round(best_score, 4),
        exact_hits=hits[:5],
        matched_clauses=hints,
        recall_source=recall_source,
    )


def score_metric(document_text: str, metric: RawRiskMetric) -> MetricCandidate:
    clauses = split_document_clauses(document_text)
    scored: List[tuple[float, DocumentClause, List[str]]] = []
    for clause in clauses:
        score, hits = _score_primary_clause(clause, metric)
        if score > 0:
            scored.append((score, clause, hits))
    return _candidate_from_scored_clauses(metric, scored, recall_source="primary")


def build_candidates(document_text: str, metrics: Iterable[RawRiskMetric]) -> List[MetricCandidate]:
    """Build the high-precision primary candidate set."""

    candidates = [score_metric(document_text, metric) for metric in metrics]
    return sorted(candidates, key=lambda item: (-item.deterministic_score, item.raw_row_id))


def build_mandate_recall_candidates(
    document_text: str,
    metrics: Iterable[RawRiskMetric],
) -> List[MetricCandidate]:
    """Build a secondary high-recall pool from distinctive Mandate metadata.

    Only specific Mandate fragments that occur on exactly one currently eligible
    metric may independently recall a metric. Shared or generic fragments remain
    excluded from this fallback pool. The LLM still has to judge these candidates
    and Python validation still enforces the authoritative row and evidence.
    """

    metric_list = list(metrics)
    clauses = split_document_clauses(document_text)
    fragments_by_row: dict[int, set[str]] = {}
    fragment_counts: Counter[str] = Counter()

    for metric in metric_list:
        fragments = {
            fragment
            for fragment in _mandate_fragments(metric.mandate)
            if _is_specific_mandate_fragment(fragment)
        }
        fragments_by_row[metric.row_id] = fragments
        fragment_counts.update(fragments)

    result: List[MetricCandidate] = []
    for metric in metric_list:
        independent = {
            fragment
            for fragment in fragments_by_row.get(metric.row_id, set())
            if fragment_counts[fragment] == 1
        }
        scored: List[tuple[float, DocumentClause, List[str]]] = []
        for clause in clauses:
            text = normalize_text(clause.text)
            fragment_results = [
                (fragment, _fragment_score(text, fragment))
                for fragment in independent
            ]
            fragment_results = [(fragment, value) for fragment, value in fragment_results if value > 0]
            if not fragment_results:
                continue
            fragment, score = max(fragment_results, key=lambda item: item[1])
            scored.append((score, clause, [fragment]))
        result.append(
            _candidate_from_scored_clauses(
                metric,
                scored,
                recall_source="mandate_fallback",
            )
        )

    return sorted(result, key=lambda item: (-item.deterministic_score, item.raw_row_id))


def select_candidates(
    candidates: Iterable[MetricCandidate],
    *,
    min_score: float = 4.0,
    limit: int | None = None,
) -> List[MetricCandidate]:
    """Return evidence-backed candidates above the deterministic threshold."""

    selected = [item for item in candidates if item.deterministic_score >= min_score and item.matched_clauses]
    selected.sort(key=lambda item: (-item.deterministic_score, item.raw_row_id))
    if limit is None:
        return selected
    return selected[: max(1, int(limit))]


def merge_candidate_sets(
    primary: Iterable[MetricCandidate],
    fallback: Iterable[MetricCandidate],
) -> List[MetricCandidate]:
    """Merge candidate pools by row id, preferring the primary candidate."""

    merged: dict[int, MetricCandidate] = {}
    for item in primary:
        merged[item.raw_row_id] = item
    for item in fallback:
        merged.setdefault(item.raw_row_id, item)
    return sorted(merged.values(), key=lambda item: (-item.deterministic_score, item.raw_row_id))
