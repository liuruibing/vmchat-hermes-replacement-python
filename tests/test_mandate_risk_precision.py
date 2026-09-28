from pathlib import Path

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import build_candidates
from app.mandate_risk.registry import RawRiskMetricRegistry


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"

TEXT = """The Sub-Portfolio targets to generate a total returns in excess of the Sub-Portfolio Benchmark Index.
The Sub-Portfolio shall be actively managed.
The Sub-Portfolio should be managed under the enhanced index strategy with proper active management and low Tracking Error.
The Sub-Portfolio shall invest in listed stocks with solid fundamentals to gain stable dividend yield and achieve long term capital growth.
"""


def test_clause_splitter_preserves_exact_source_text():
    clauses = split_document_clauses(TEXT)
    assert clauses
    assert all(clause.text in TEXT for clause in clauses)
    assert any("low Tracking Error" in clause.text for clause in clauses)


def test_candidate_scoring_does_not_accumulate_generic_mandate_phrases():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    eligible = registry.eligible_for_strategy("权益")
    candidates = build_candidates(TEXT, eligible)
    by_name = {item.metric_name: item for item in candidates}

    tracking = by_name["跟踪误差"]
    info_ratio = by_name["信息比率"]
    sortino = by_name["Sortino索提诺"]

    assert tracking.deterministic_score > 0
    assert tracking.deterministic_score >= info_ratio.deterministic_score
    assert tracking.deterministic_score >= sortino.deterministic_score
    assert tracking.matched_clauses
    assert all(hint.text in TEXT for hint in tracking.matched_clauses)


def test_shared_dividend_mandate_remains_ambiguous_for_semantic_judge():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    candidates = build_candidates(TEXT, registry.eligible_for_strategy("权益"))
    by_name = {item.metric_name: item for item in candidates}

    scores = {
        by_name[name].deterministic_score
        for name in ("股息贡献率", "股息支付率NII", "股息增长率", "股息覆盖率")
    }
    assert len(scores) == 1
    assert next(iter(scores)) > 0
