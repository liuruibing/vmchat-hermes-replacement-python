from pathlib import Path
import json

import pytest

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
from app.workflow.graphs.mandate_risk import MandateRiskLangGraphWorkflow


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


def test_new_metric_library_row_loads_and_reaches_candidate_search(tmp_path):
    source = tmp_path / "metrics.csv"
    source.write_text(
        "风险类型一级,风险类型二级,指标名称,指标算法,Mandate字段,适用策略种类\n"
        "流动性风险,流动性,组合流动性缓冲率,高流动性资产/组合净值,liquidity buffer,固收\n",
        encoding="utf-8",
    )
    registry = MandateRiskLangGraphWorkflow(str(source))._load_registry()
    candidates = select_candidates(
        build_candidates("组合应维持组合流动性缓冲率不低于10%。", registry.eligible_for_strategy("固收"))
    )
    english_candidates = select_candidates(
        build_mandate_recall_candidates(
            "The fund shall maintain a liquidity buffer of at least 25%.",
            registry.eligible_for_strategy("固收"),
        )
    )

    assert len(registry.all()) == 1
    assert [item.metric_name for item in candidates] == ["组合流动性缓冲率"]
    assert [item.metric_name for item in english_candidates] == ["组合流动性缓冲率"]


def test_empty_metric_library_is_rejected(tmp_path):
    source = tmp_path / "empty.csv"
    source.write_text(
        "风险类型一级,风险类型二级,指标名称,指标算法,Mandate字段,适用策略种类\n",
        encoding="utf-8",
    )
    with pytest.raises(RuntimeError, match="MANDATE_RISK_METRIC_LIBRARY_INVALID"):
        MandateRiskLangGraphWorkflow(str(source))._load_registry()


def test_fixed_income_contract_reaches_related_duration_maturity_liquidity_metrics():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    turnover = registry.get_by_name("换手率(%)")
    assert turnover is not None
    assert turnover.strategy_type == "权益"
    eligible = registry.eligible_for_strategy("固收")
    assert turnover in eligible

    _registry, candidates = _merged_candidates(FIXED_INCOME_EXTRACT, "固收")
    names = {item.metric_name for item in candidates}
    assert {"久期", "DV01", "剩余期限", "债券资产变现天数", "换手率(%)"} <= names
    assert "VaR" not in names
    assert "信用利差（非标）" not in names


def test_strategy_inference_uses_explicit_asset_class_for_private_and_mixed_portfolios():
    private_credit = (
        "Private Credit; Cash and Cash Equivalents. "
        "Invest in CNY denominated Private Credit Investments and privately issued Fixed Income securities. "
        "The Benchmark Index is China (10- Years). Optimize Duration gap level."
    )
    mixed = (
        "The Fund implements asset allocation between its Equity Portfolio and Fixed Income Portfolio. "
        "Equity assets: Listed Equity. Fixed income assets: Bonds."
    )
    assert infer_strategy_type(private_credit)[0] == "固收"
    assert infer_strategy_type(mixed)[0] == "混合"


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
    assert "每个 Candidate" in SYSTEM_PROMPT
    assert "每项明确数值目标或限额" in SYSTEM_PROMPT
    assert "数字必须出现在引用条款" in SYSTEM_PROMPT
    assert "复合限额" in SYSTEM_PROMPT
    assert '"clause_id":"c0003"' in prompt
    assert '"text":"逐字原文引文"' not in prompt


def test_gap_prompt_exposes_canonical_clause_ids_without_metric_candidates():
    document = (
        "[Page 6]\n"
        "If a fund is below RMB 1 billion, investment shall not exceed RMB 100 million;\n\n"
        "[Page 7]\n"
        "Holdings in a single MMF shall not exceed 100% of its assets."
    )
    registry = RawRiskMetricRegistry.from_path(METRICS)
    prompt = build_semantic_judge_prompt(
        document_text=document,
        document_name="new-mandate.pdf",
        strategy_type="权益",
        registry=registry,
        candidates=[],
    )

    for clause in split_document_clauses(document):
        canonical = json.dumps(
            {"clause_id": clause.clause_id, "page": clause.page, "text": clause.text},
            ensure_ascii=False,
            separators=(",", ":"),
        )
        assert canonical in prompt
    assert '"clause_id":"c0003"' not in prompt
    assert '"clause_id":"c0008"' not in prompt


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

    assert result.selected_metrics == []
    assert len(result.review_metrics) == 1
    match = result.review_metrics[0]
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


def test_dividend_yield_goal_does_not_directly_require_contribution_ratio():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    contribution = registry.get_by_name("股息贡献率")
    assert contribution is not None
    document = "[Page 4]\nThe Sub-Portfolio shall aim to gain stable dividend yield."
    clause = split_document_clauses(document)[0]
    payload = {
        "matches": [
            {
                "raw_row_id": contribution.row_id,
                "metric_name": contribution.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.95,
                "evidence": [{"clause_id": clause.clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[contribution.row_id],
        document_text=document,
        document_name="equity.pdf",
        strategy_type="权益",
        candidate_clause_ids={contribution.row_id: [clause.clause_id]},
    )

    assert result.selected_metrics == []
    assert result.review_metrics[0].match_level == "STRONG_INFERRED"


def test_private_credit_asset_name_alone_does_not_prove_remaining_maturity():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    maturity = registry.get_by_name("非标剩余期限")
    assert maturity is not None
    document = "[Page 4]\nThe Sub-Portfolio shall invest in Private Credit Investments."
    clause = split_document_clauses(document)[0]
    payload = {
        "matches": [
            {
                "raw_row_id": maturity.row_id,
                "metric_name": maturity.metric_name,
                "match_level": "STRONG_INFERRED",
                "confidence": 0.9,
                "evidence": [{"clause_id": clause.clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[maturity.row_id],
        document_text=document,
        document_name="private-credit.pdf",
        strategy_type="固收",
        candidate_clause_ids={maturity.row_id: [clause.clause_id]},
    )

    assert result.selected_metrics == []
    assert result.review_metrics[0].match_level == "WEAK_INFERRED"


def test_stable_cash_flows_do_not_support_fund_return_metric():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    fund_return = registry.get_by_name("基金收益率")
    assert fund_return is not None
    document = "[Page 4]\nThe primary investment objective is to provide stable cash flows."
    clause = split_document_clauses(document)[0]
    payload = {
        "matches": [
            {
                "raw_row_id": fund_return.row_id,
                "metric_name": fund_return.metric_name,
                "match_level": "STRONG_INFERRED",
                "confidence": 0.91,
                "reason": "Stable cash flows imply returns.",
                "evidence": [{"clause_id": clause.clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[fund_return.row_id],
        document_text=document,
        document_name="fixed-income.pdf",
        strategy_type="固收",
        candidate_clause_ids={fund_return.row_id: [clause.clause_id]},
    )

    assert result.selected_metrics == []
    assert result.rejected_metrics[0].match_level == "REJECTED"


def test_explicit_total_return_goal_supports_fund_return_metric():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    fund_return = registry.get_by_name("基金收益率")
    assert fund_return is not None
    document = "[Page 4]\nThe primary investment objective is to generate total return."
    clause = split_document_clauses(document)[0]
    payload = {
        "matches": [
            {
                "raw_row_id": fund_return.row_id,
                "metric_name": fund_return.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.9,
                "evidence": [{"clause_id": clause.clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[fund_return.row_id],
        document_text=document,
        document_name="equity.pdf",
        strategy_type="权益",
        candidate_clause_ids={fund_return.row_id: [clause.clause_id]},
    )

    assert len(result.selected_metrics + result.review_metrics) == 1
    assert (result.selected_metrics + result.review_metrics)[0].match_level in {"DIRECT", "STRONG_INFERRED"}


def test_gap_threshold_condition_must_match_quoted_clause():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document = (
        "[Page 6]\n"
        "If total market value of Third-Party Managed Fund is less than RMB 1 billion, "
        "the aggregate investment shall not exceed the lower of 100% and RMB 100 million.\n\n"
        "If total market value of Third-Party Managed Fund is RMB 1 billion or more, "
        "the aggregate investment shall not exceed 100% of its total market value."
    )
    clauses = split_document_clauses(document)
    lower_clause = next(item for item in clauses if "less than RMB 1 billion" in item.text)
    higher_clause = next(item for item in clauses if "RMB 1 billion or more" in item.text)
    requirement = "若基金市值低于RMB 1 billion，投资不得超过100%。"

    def validate(quote):
        return validate_model_result(
            payload={"matches": [], "gaps": [{"requirement": requirement, "evidence": [{"clause_id": quote.clause_id}]}]},
            registry=registry,
            allowed_row_ids=[],
            document_text=document,
            document_name="equity.pdf",
            strategy_type="权益",
        )

    assert validate(higher_clause).library_gaps == []
    assert len(validate(lower_clause).library_gaps) == 1


def test_gap_numeric_unit_survives_adjacent_chinese_text():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document = "[Page 6]\nThe investment shall not exceed 100% of its total market value."
    clause = split_document_clauses(document)[0]
    result = validate_model_result(
        payload={
            "matches": [],
            "gaps": [{
                "requirement": "投资上限为RMB 100 million中的较低者。",
                "evidence": [{"clause_id": clause.clause_id}],
            }],
        },
        registry=registry,
        allowed_row_ids=[],
        document_text=document,
        document_name="equity.pdf",
        strategy_type="权益",
    )

    assert result.library_gaps == []


def test_gap_threshold_direction_is_not_tied_to_sample_currency_or_value():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document = (
        "[Page 2]\nIf fund assets are USD 2 million or more, "
        "the allocation shall not exceed 50% of net assets."
    )
    clause = split_document_clauses(document)[0]
    result = validate_model_result(
        payload={
            "matches": [],
            "gaps": [{
                "requirement": "若基金资产低于USD 2 million，配置不得超过50%。",
                "evidence": [{"clause_id": clause.clause_id}],
            }],
        },
        registry=registry,
        allowed_row_ids=[],
        document_text=document,
        document_name="another-contract.pdf",
        strategy_type="权益",
    )

    assert result.library_gaps == []


@pytest.mark.parametrize(
    "requirement, clause_text",
    [
        ("基金资产不低于USD 2 million。", "The fund shall hold no less than USD 2 million."),
        ("基金资产低于USD 2 million。", "If assets are USD 2 million or  less."),
    ],
)
def test_gap_threshold_parses_negation_and_pdf_whitespace(requirement, clause_text):
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document = f"[Page 2]\n{clause_text}"
    clause = split_document_clauses(document)[0]
    result = validate_model_result(
        payload={"matches": [], "gaps": [{
            "requirement": requirement,
            "evidence": [{"clause_id": clause.clause_id}],
        }]},
        registry=registry,
        allowed_row_ids=[],
        document_text=document,
        document_name="another-contract.pdf",
        strategy_type="固收",
    )

    assert len(result.library_gaps) == 1


def test_gap_threshold_rejects_same_amount_in_wrong_currency():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document = "[Page 2]\nIf fund assets are below EUR 2 million, allocation is limited to 50%."
    clause = split_document_clauses(document)[0]
    result = validate_model_result(
        payload={"matches": [], "gaps": [{
            "requirement": "若基金资产低于USD 2 million，配置限额为50%。",
            "evidence": [{"clause_id": clause.clause_id}],
        }]},
        registry=registry,
        allowed_row_ids=[],
        document_text=document,
        document_name="another-contract.pdf",
        strategy_type="固收",
    )

    assert result.library_gaps == []


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
    assert "| key（直观判断组合运行情况） | 久期 | — | — | — | — |" in markdown
