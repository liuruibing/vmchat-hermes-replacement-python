from __future__ import annotations

from typing import List

from app.mandate_risk.models import MetricMatch, RiskAnalysisResult
from app.mandate_risk.registry import RawRiskMetricRegistry


def _clean(value: str) -> str:
    return str(value or "").strip()


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

    lines.extend(["", "## 建议匹配指标", ""])
    if not result.selected_metrics:
        lines.append("未找到达到 DIRECT / STRONG_INFERRED 的指标。")
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
        "- 本报告不自动生成 green / amber / red 阈值。",
    ])
    return "\n".join(lines).strip() + "\n"
