from pathlib import Path

from app.mandate_risk.models import EvidenceQuote, MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.renderer import render_markdown


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"


def test_renderer_emits_fixed_six_column_markdown_summary_table():
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
    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in markdown
    assert "| key（直观判断组合运行情况） | 跟踪误差 | The portfolio should be managed with low Tracking Error. | — | — | — |" in markdown
    assert "### 1. 跟踪误差" in markdown
    # Auditable match level / page / confidence remain in the detail section;
    # they are not mixed into the fixed UI summary columns.
    assert "- 匹配级别：`DIRECT`" in markdown
    assert "- 置信度：0.99" in markdown
    assert "（第 5 页）" in markdown


def test_renderer_escapes_markdown_table_pipes_in_quote():
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
                reason="模型解释不能作为合同原文",
                evidence=[EvidenceQuote(text="A | B", page=2)],
            )
        ]
    )

    markdown = render_markdown(result, registry)
    assert "| key（直观判断组合运行情况） | 跟踪误差 | A \\| B | — | — | — |" in markdown
    assert "模型解释不能作为合同原文 |" not in markdown


def test_summary_excludes_review_only_metrics():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    duration = registry.get_by_name("久期")
    assert tracking is not None and duration is not None
    result = RiskAnalysisResult(
        selected_metrics=[
            MetricMatch(
                raw_row_id=tracking.row_id,
                metric_name=tracking.metric_name,
                match_level="DIRECT",
                evidence=[EvidenceQuote(text="Tracking Error shall not exceed 5%." )],
            )
        ],
        review_metrics=[
            MetricMatch(
                raw_row_id=duration.row_id,
                metric_name=duration.metric_name,
                match_level="WEAK_INFERRED",
                evidence=[EvidenceQuote(text="Duration adjustment is permitted.")],
            )
        ],
    )

    markdown = render_markdown(result, registry)
    summary = markdown.split("## 匹配摘要", 1)[1].split("## 建议匹配指标", 1)[0]
    assert "| 跟踪误差 |" in summary
    assert "| 久期 |" not in summary
    assert "### 1. 久期" in markdown.split("## 待确认指标", 1)[1]


def test_summary_prefers_complete_mandate_clause_over_definition():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    duration = registry.get_by_name("久期")
    assert duration is not None
    result = RiskAnalysisResult(
        selected_metrics=[
            MetricMatch(
                raw_row_id=duration.row_id,
                metric_name=duration.metric_name,
                match_level="STRONG_INFERRED",
                evidence=[
                    EvidenceQuote(text='"Duration" means price sensitivity to yield;'),
                    EvidenceQuote(text="Duration adjustment is expected when managing long-term bonds."),
                ],
            )
        ]
    )

    summary = render_markdown(result, registry).split("## 匹配摘要", 1)[1].split("## 建议匹配指标", 1)[0]
    assert "| Duration adjustment is expected when managing long-term bonds. |" in summary
