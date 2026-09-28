from pathlib import Path

from app.mandate_risk.models import EvidenceQuote, MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.renderer import render_markdown


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"


def test_renderer_emits_markdown_summary_table_with_python_page():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    result = RiskAnalysisResult(
        document_name="sample.pdf",
        strategy_type="权益",
        selected_metrics=[
            MetricMatch(
                raw_row_id=tracking.row_id,
                metric_name=tracking.metric_name,
                match_level="DIRECT",
                confidence=0.99,
                reason="文档明确要求低跟踪误差。",
                evidence=[
                    EvidenceQuote(
                        text="The portfolio should be managed with low Tracking Error.",
                        page=5,
                        clause_id="c0008",
                    )
                ],
            )
        ],
    )

    markdown = render_markdown(result, registry)

    assert "## 匹配摘要" in markdown
    assert "| 分组 | 名称 | Mandate解读 | 风险分类 | 匹配级别 | 页码 | 置信度 |" in markdown
    assert "| 建议 | 跟踪误差 | 文档明确要求低跟踪误差。" in markdown
    assert "| DIRECT | 5 | 99% |" in markdown
    assert "### 1. 跟踪误差" in markdown


def test_renderer_escapes_markdown_table_pipes_in_reason():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    result = RiskAnalysisResult(
        selected_metrics=[
            MetricMatch(
                raw_row_id=tracking.row_id,
                metric_name=tracking.metric_name,
                match_level="STRONG_INFERRED",
                confidence=0.8,
                reason="A | B",
            )
        ]
    )

    markdown = render_markdown(result, registry)
    assert "A \\| B" in markdown
