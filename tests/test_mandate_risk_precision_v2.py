from pathlib import Path

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import build_candidates, select_candidates
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.validator import validate_model_result


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"

# Mirrors the visual-line wrapping seen in the provided high-dividend strategy PDF:
# semantic phrases are intentionally split across physical lines.
PDF_EXTRACT = """境内上市权益（高分红策略）
Benchmark
MSCI China A International High Dividend Yield Index
Investment Strategy
The primary investment objective of the Sub-Portfolio is to gain stable dividend yield and achieve long term capital growth through mainly investing into high-quality Common Shares issued by Chinese Issuers with an emphasis on value and good growth outlook, and to generate a total returns in excess of the Sub-Portfolio
Benchmark Index. The Sub-Portfolio targets to achieve an outperformance of 0.5% p.a. over a 3 to 5-year investment horizon.
To ensure the Sub-Portfolio to generate a comparable return against the Benchmark in the long term through investing in permissible instruments in the China A-Share market.
The Sub-Portfolio shall deliver excess return over the designated Benchmark by executing geographic, Industry/Sector and trading strategies. The Sub-Portfolio shall be actively managed to achieve the Investment Objective, by investing in Funds or stocks, which are listed through China A-Share market.
The Sub-Portfolio should be managed under the enhanced index strategy with proper active
management and low Tracking Error. The investment strategy could be a blend of bottom-up and top-down approach. The Sub-Portfolio shall invest in listed stocks with solid fundamentals to gain stable dividend yield and achieve long term capital growth.
"""


def test_pdf_soft_line_wrap_does_not_break_key_phrases():
    clauses = split_document_clauses(PDF_EXTRACT)
    tracking_clause = next(item for item in clauses if "low Tracking Error" in item.text)
    assert "proper active\nmanagement and low Tracking Error" in tracking_clause.text
    assert PDF_EXTRACT[tracking_clause.source_start:tracking_clause.source_end] == tracking_clause.text

    registry = RawRiskMetricRegistry.from_path(METRICS)
    selected = select_candidates(
        build_candidates(PDF_EXTRACT, registry.eligible_for_strategy("权益"))
    )
    by_name = {item.metric_name: item for item in selected}

    assert "跟踪误差" in by_name
    assert "超额收益率（基准超额）" in by_name
    assert "股息贡献率" in by_name
    assert by_name["跟踪误差"].deterministic_score >= 8
    assert by_name["超额收益率（基准超额）"].deterministic_score >= 8


def test_realistic_high_dividend_recall_excludes_generic_false_positives():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    selected = select_candidates(
        build_candidates(PDF_EXTRACT, registry.eligible_for_strategy("权益"))
    )
    names = {item.metric_name for item in selected}

    assert "VaR" not in names
    assert "最大回撤" not in names
    assert "波动率" not in names
    assert "组合Beta贝塔" not in names
    assert "Sortino索提诺" not in names
    assert "信息比率" not in names
    assert "换手率(%)" not in names
    assert "单一证券占比" not in names
    assert "流动性上市权益资产占比" not in names


def test_validator_rejects_evidence_from_an_unrelated_clause():
    document = (
        "The Sub-Portfolio should be managed with low Tracking Error. "
        "The Sub-Portfolio seeks stable dividend yield."
    )
    clauses = split_document_clauses(document)
    tracking_clause = next(item for item in clauses if "Tracking Error" in item.text)
    dividend_clause = next(item for item in clauses if "dividend yield" in item.text)

    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    payload = {
        "summary": "test",
        "matches": [
            {
                "raw_row_id": tracking.row_id,
                "metric_name": tracking.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.99,
                "reason": "wrong evidence on purpose",
                "evidence": [
                    {
                        "clause_id": dividend_clause.clause_id,
                        "text": dividend_clause.text,
                    }
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
        document_name="test.pdf",
        strategy_type="权益",
        candidate_clause_ids={tracking.row_id: [tracking_clause.clause_id]},
    )

    assert result.selected_metrics == []
    assert len(result.rejected_metrics) == 1
    assert result.rejected_metrics[0].metric_name == "跟踪误差"


def test_validator_canonicalizes_soft_wrapped_clause_by_id():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    clause = next(item for item in split_document_clauses(PDF_EXTRACT) if "low Tracking Error" in item.text)
    payload = {
        "matches": [
            {
                "raw_row_id": tracking.row_id,
                "metric_name": tracking.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.95,
                "reason": "document explicitly requires low tracking error",
                "evidence": [
                    {
                        "clause_id": clause.clause_id,
                        "text": "The Sub-Portfolio should be managed under the enhanced index strategy with proper active management and low Tracking Error.",
                    }
                ],
            }
        ],
        "gaps": [],
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[tracking.row_id],
        document_text=PDF_EXTRACT,
        document_name="high-dividend.pdf",
        strategy_type="权益",
        candidate_clause_ids={tracking.row_id: [clause.clause_id]},
    )

    assert len(result.selected_metrics) == 1
    evidence = result.selected_metrics[0].evidence[0]
    assert evidence.clause_id == clause.clause_id
    assert evidence.text == clause.text
    assert evidence.source_start == clause.source_start
    assert evidence.source_end == clause.source_end
