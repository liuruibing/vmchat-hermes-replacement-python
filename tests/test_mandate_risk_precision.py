from pathlib import Path

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import build_candidates, select_candidates
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
    assert all(TEXT[clause.source_start:clause.source_end] == clause.text for clause in clauses)


def test_candidate_scoring_requires_metric_concept_not_generic_mandate():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    eligible = registry.eligible_for_strategy("权益")
    candidates = build_candidates(TEXT, eligible)
    by_name = {item.metric_name: item for item in candidates}

    tracking = by_name["跟踪误差"]
    info_ratio = by_name["信息比率"]
    sortino = by_name["Sortino索提诺"]
    var = by_name["VaR"]

    assert tracking.deterministic_score > 0
    assert info_ratio.deterministic_score == 0
    assert sortino.deterministic_score == 0
    assert var.deterministic_score == 0
    assert tracking.matched_clauses
    assert all(hint.text in TEXT for hint in tracking.matched_clauses)


def test_dividend_algorithm_concept_disambiguates_shared_mandate():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    candidates = build_candidates(TEXT, registry.eligible_for_strategy("权益"))
    by_name = {item.metric_name: item for item in candidates}

    assert by_name["股息贡献率"].deterministic_score > 0
    assert by_name["股息支付率NII"].deterministic_score == 0
    assert by_name["股息增长率"].deterministic_score == 0
    assert by_name["股息覆盖率"].deterministic_score == 0
    assert by_name["换手率(%)"].deterministic_score == 0


def test_candidate_set_sent_to_llm_is_small_and_evidence_backed():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    candidates = select_candidates(
        build_candidates(TEXT, registry.eligible_for_strategy("权益"))
    )
    names = {item.metric_name for item in candidates}

    assert "跟踪误差" in names
    assert "超额收益率（基准超额）" in names
    assert "股息贡献率" in names
    assert "VaR" not in names
    assert "最大回撤" not in names
    assert "波动率" not in names
    assert "组合Beta贝塔" not in names
    assert "Sortino索提诺" not in names
    assert "信息比率" not in names
    assert all(item.deterministic_score >= 4.0 for item in candidates)
