from __future__ import annotations

import re
from typing import Iterable, List

from app.mandate_risk.models import MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry


_KEY_METRICS = {
    "基金收益率", "超额收益率（基准超额）", "信息比率", "跟踪误差", "久期", "DV01",
}
_CORE_METRICS = {
    "股息覆盖率", "境内资产占比", "单一证券占比", "行业偏离度",
    "流通受限资产占比", "流动性上市权益资产占比", "剩余期限",
    "债券AA+及以下评级占比(%)", "单一发行人集中度", "区域分布",
}


def _display_group(metric_name: str) -> str:
    if metric_name in _KEY_METRICS:
        return "key（直观判断组合运行情况）"
    if metric_name in _CORE_METRICS:
        return "core（体现策略特征）"
    return "Indicator（趋势变化分析）"


def _clean(value: str) -> str:
    return str(value or "").strip()


def _md_cell(value: str) -> str:
    """Escape free text for a GitHub-flavoured Markdown table cell."""

    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text.replace("|", "\\|") or "—"


def _summary_quote(match: MetricMatch) -> str:
    if not match.evidence:
        return "—"

    def score(text: str) -> int:
        normalized = text.strip()
        return (
            2 * bool(re.search(r"\b(?:shall|should|must|target|aim|expected)\b", normalized, re.I))
            + bool(normalized.endswith((".", "。", ";", "；")))
            - 2 * bool(re.search(r"\bmeans\b", normalized, re.I))
        )

    return max(match.evidence, key=lambda item: score(item.text)).text


def _summary_rows(
    matches: Iterable[MetricMatch],
    registry: RawRiskMetricRegistry,
) -> List[str]:
    """Render rows using the fixed six-column UI contract.

    Quote text and the display group are derived from validated results.
    Value, reference portfolio and similarity need separate portfolio data.
    """

    rows: List[str] = []
    for match in matches:
        metric = registry.require(match.raw_row_id)
        interpretation = _summary_quote(match)
        rows.append(
            "| "
            + " | ".join(
                [
                    _md_cell(_display_group(metric.metric_name)),
                    _md_cell(metric.metric_name),
                    _md_cell(interpretation),
                    "—",
                    "—",
                    "—",
                ]
            )
            + " |"
        )
    return rows


def _render_summary_table(result: RiskAnalysisResult, registry: RawRiskMetricRegistry) -> List[str]:
    matches = list(result.selected_metrics)
    if not matches:
        return ["暂无可展示的匹配指标。"]

    lines = [
        "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    lines.extend(_summary_rows(matches, registry))
    return lines


def _render_match(match: MetricMatch, registry: RawRiskMetricRegistry, index: int) -> List[str]:
    metric = registry.require(match.raw_row_id)
    lines = [
        f"### {index}. {metric.metric_name}",
        "",
        f"- 匹配级别：`{match.match_level}`",
        f"- 置信度：{match.confidence:.2f}",
        f"- 风险分类：{metric.effective_risk_type_1 or '未填写'} / {metric.effective_risk_type_2 or '未填写'}",
        f"- 原始库行：{metric.source_row}",
        f"- 适用策略种类（原始值）：{metric.strategy_type or '空'}",
    ]
    lines.append(f"- 指标算法（原始值）：{_clean(metric.algorithm) or '空'}")
    lines.append(f"- Mandate字段（原始值）：{_clean(metric.mandate) or '空'}")
    if match.reason:
        lines.extend(["", f"**匹配理由**：{match.reason}"])
    if match.evidence:
        lines.extend(["", "**文档依据**"])
        for evidence in match.evidence:
            page = f"（第 {evidence.page} 页）" if evidence.page else ""
            lines.append(f"> {evidence.text}{page}")
    lines.append("")
    return lines


def render_markdown(result: RiskAnalysisResult, registry: RawRiskMetricRegistry) -> str:
    lines: List[str] = [
        "# 风险指标匹配报告",
        "",
        f"- 文档：{result.document_name or '未命名文档'}",
        f"- Python识别策略类型：{result.strategy_type or '未知'}",
        f"- 原始风险指标库：{len(registry.all())} 条，只读匹配",
    ]
    if result.summary:
        lines.extend(["", f"> {result.summary}"])

    lines.extend(["", "## 匹配摘要", ""])
    lines.extend(_render_summary_table(result, registry))

    lines.extend(["", "## 建议匹配指标", ""])
    if not result.selected_metrics:
        lines.append("未找到有合同直接依据的指标。")
    else:
        for index, match in enumerate(result.selected_metrics, start=1):
            lines.extend(_render_match(match, registry, index))

    lines.extend(["", "## 待确认指标", ""])
    if not result.review_metrics:
        lines.append("无。")
    else:
        for index, match in enumerate(result.review_metrics, start=1):
            lines.extend(_render_match(match, registry, index))

    lines.extend(["", "## 指标库缺口", ""])
    if not result.library_gaps:
        lines.append("未识别到明确的指标库缺口。")
    else:
        for index, gap in enumerate(result.library_gaps, start=1):
            lines.append(f"### {index}. {gap.requirement}")
            if gap.reason:
                lines.append(f"- 原因：{gap.reason}")
            for evidence in gap.evidence:
                page = f"（第 {evidence.page} 页）" if evidence.page else ""
                lines.append(f"> {evidence.text}{page}")
            lines.append("")

    lines.extend([
        "",
        "## 说明",
        "",
        "- 正式指标名称、算法、Mandate字段、适用策略种类均来自原始风险指标库；系统不会修改或补写原始库。",
        "- AI 不允许创建正式指标；库内无等价指标时只会进入“指标库缺口”。",
        "- 摘要表固定使用“分组 / 名称 / Mandate解读 / 值 / 参考组合 / 相似度”六列；当前没有权威数据来源的列统一显示为“—”。",
        "- 本报告不自动生成 green / amber / red 阈值。",
    ])
    return "\n".join(lines).strip() + "\n"
