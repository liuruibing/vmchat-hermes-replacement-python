from pathlib import Path

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import (
    build_candidates,
    build_mandate_recall_candidates,
    infer_strategy_type,
    merge_candidate_sets,
    select_candidates,
)
from app.mandate_risk.models import MetricMatch, RiskAnalysisResult
from app.mandate_risk.prompts import SYSTEM_PROMPT, build_semantic_judge_prompt
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.renderer import render_markdown
from app.mandate_risk.validator import validate_model_result


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"


FIXED_INCOME_EXTRACT = """[Page 3]
“Duration” means may either refer to the present value weighted average of the times until fixed cash flows are received for a Fixed Income security, or a measure of the price sensitivity to yield.
“High Yield Strategies” means Investment Portfolios or Sub-Portfolios which predominantly invest in Fixed Income securities with an ORR below 4-.
“Investment Grade Strategies” means Investment Portfolios or Sub-Portfolios which predominantly invest in Fixed Income securities with an ORR of 4- or higher.

[Page 4]
The primary investment objective of the Sub-Portfolio is to provide stable cash flows with reasonable credit risk exposure. The Sub-Portfolio should mainly focus on purchasing CNY denominated long-term Public Credit securities.
The Sub-Portfolio shall be managed in a “Buy and Maintain” style to achieve the investment objective, but the manager shall seek to add value to the Sub-Portfolio through relative value investment in CNY denominated Public Credit securities registered in the Chinese market.
Public Credit securities included both Investment Grade Strategies and High Yield Strategies.
With the exception of divestment for relative value trades, Duration adjustment, capital management or credit concerns, assets are expected to be held-to-maturity.
The Sub-Portfolio should target new purchase yield in excess of Sub-Portfolio Benchmark Index yield by 10 bps at the time of purchase (target spread).
"""


EQUITY_EXTRACT = """[Page 4]
“Tracking Error” means the standard deviation of the Excess Return.
The primary investment objective of the Sub-Portfolio is to generate total return in excess of the Sub-Portfolio Benchmark Index by 0.5% p.a.
The Sub-Portfolio aim to gain stable dividend yield and achieve long term capital growth through mainly investing into high-quality Common Shares issued by Chinese Issuers.

[Page 5]
The Sub-Portfolio shall deliver excess return over the designated Benchmark by executing geographic, Industry/Sector and trading strategies.
The Sub-Portfolio should be managed under the enhanced index strategy with proper active management and low Tracking Error.
The Sub-Portfolio shall invest in listed stocks with solid fundamentals to gain stable dividend yield and achieve long term capital growth.

[Page 6]
The exposure to any single security shall not exceed 100% of the market value of the Sub-Portfolio.
The annualised ex-ante Tracking Error shall not exceed 100%.
"""


def _merged_candidates(document_text: str, strategy_type: str):
    registry = RawRiskMetricRegistry.from_path(METRICS)
    eligible = registry.eligible_for_strategy(strategy_type)
    primary = select_candidates(build_candidates(document_text, eligible))
    fallback = select_candidates(build_mandate_recall_candidates(document_text, eligible))
    return registry, merge_candidate_sets(primary, fallback)


def test_fixed_income_regression_recalls_credit_metrics_without_sample_rules():
    strategy, confidence = infer_strategy_type(FIXED_INCOME_EXTRACT)
    assert strategy == "固收"
    assert confidence >= 0.7

    _registry, candidates = _merged_candidates(FIXED_INCOME_EXTRACT, strategy)
    by_name = {item.metric_name: item for item in candidates}

    assert "久期" in by_name
    assert "信用利差（债券）" in by_name
    assert "加权平均信用评级" in by_name
    assert by_name["久期"].recall_source == "primary"
    assert by_name["信用利差（债券）"].recall_source == "mandate_fallback"
    assert by_name["加权平均信用评级"].recall_source == "mandate_fallback"
    # Shared generic credit-risk wording must not independently pull the
    # non-standard/private-credit spread metric into this public-credit sample.
    assert "信用利差（非标）" not in by_name


def test_equity_regression_keeps_direct_concepts_and_excludes_generic_risk_metrics():
    strategy, confidence = infer_strategy_type(EQUITY_EXTRACT)
    assert strategy == "权益"
    assert confidence >= 0.7

    _registry, candidates = _merged_candidates(EQUITY_EXTRACT, strategy)
    names = {item.metric_name for item in candidates}

    assert "跟踪误差" in names
    assert "超额收益率（基准超额）" in names
    assert "股息贡献率" in names
    assert "单一证券占比" in names
    assert "VaR" not in names
    assert "最大回撤" not in names
    assert "波动率" not in names
    assert "组合Beta贝塔" not in names
    assert "Sortino索提诺" not in names
    assert "信息比率" not in names


def test_prompt_exposes_full_strategy_catalogue_for_gap_checks():
    registry, candidates = _merged_candidates(FIXED_INCOME_EXTRACT, "固收")
    prompt = build_semantic_judge_prompt(
        document_text=FIXED_INCOME_EXTRACT,
        document_name="fixed-income.pdf",
        strategy_type="固收",
        registry=registry,
        candidates=candidates,
    )

    assert "# Strategy-eligible metric catalogue" in prompt
    assert '"metric_name":"信用利差（债券）"' in prompt
    assert '"metric_name":"加权平均信用评级"' in prompt
    assert '"metric_name":"超额收益率（基准超额）"' in prompt
    assert '"recall_source":"mandate_fallback"' in prompt
    assert "Candidate metrics 不是完整指标库" in SYSTEM_PROMPT
    assert "测量对象" in SYSTEM_PROMPT
    assert "稳定现金流" in SYSTEM_PROMPT
    assert "REJECTED" in SYSTEM_PROMPT


def test_validator_downgrades_definition_or_allowed_adjustment_from_direct():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    duration = registry.get_by_name("久期")
    assert duration is not None

    document = (
        "[Page 3]\n“Duration” means a measure of the price sensitivity to yield.\n\n"
        "[Page 4]\nWith the exception of Duration adjustment, assets are expected to be held-to-maturity."
    )
    clauses = split_document_clauses(document)
    evidence_clauses = [item for item in clauses if "Duration" in item.text]

    payload = {
        "matches": [
            {
                "raw_row_id": duration.row_id,
                "metric_name": duration.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.98,
                "reason": "Duration is defined and adjustment is permitted.",
                "evidence": [
                    {"clause_id": item.clause_id, "text": item.text, "page": 999}
                    for item in evidence_clauses
                ],
            }
        ],
        "gaps": [],
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[duration.row_id],
        document_text=document,
        document_name="fixed-income.pdf",
        strategy_type="固收",
        candidate_clause_ids={duration.row_id: [item.clause_id for item in evidence_clauses]},
    )

    assert len(result.selected_metrics) == 1
    match = result.selected_metrics[0]
    assert match.match_level == "STRONG_INFERRED"
    assert match.confidence <= 0.85
    assert "Python校验" in match.reason
    assert {item.page for item in match.evidence} == {3, 4}


def test_validator_preserves_direct_when_metric_has_explicit_limit():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    document = "[Page 6]\nThe annualised ex-ante Tracking Error shall not exceed 100%."
    clause = split_document_clauses(document)[0]
    payload = {
        "matches": [
            {
                "raw_row_id": tracking.row_id,
                "metric_name": tracking.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.99,
                "reason": "Explicit tracking-error limit.",
                "evidence": [
                    {"clause_id": clause.clause_id, "text": clause.text, "page": 123}
                ],
            }
        ],
        "gaps": [],
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[tracking.row_id],
        document_text=document,
        document_name="equity.pdf",
        strategy_type="权益",
        candidate_clause_ids={tracking.row_id: [clause.clause_id]},
    )

    assert len(result.selected_metrics) == 1
    match = result.selected_metrics[0]
    assert match.match_level == "DIRECT"
    assert match.confidence == 0.99
    assert match.evidence[0].page == 6


def test_summary_markdown_uses_fixed_named_six_columns():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    duration = registry.get_by_name("久期")
    assert duration is not None

    result = RiskAnalysisResult(
        document_name="fixed-income.pdf",
        strategy_type="固收",
        selected_metrics=[
            MetricMatch(
                raw_row_id=duration.row_id,
                metric_name=duration.metric_name,
                match_level="STRONG_INFERRED",
                confidence=0.8,
                reason="Duration is strongly related.",
            )
        ],
    )
    markdown = render_markdown(result, registry)

    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in markdown
    assert "| — | 久期 | Duration is strongly related. | — | — | — |" in markdown
