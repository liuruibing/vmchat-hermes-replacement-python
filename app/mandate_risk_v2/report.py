from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingResult
from app.mandate_risk_v2.models import Requirement, RequirementIR
from app.mandate_risk_v2.result import (
    DestinationResultItem,
    V2AnalysisResult,
    build_v2_analysis_result,
)


GROUPS_PATH = (
    Path(__file__).resolve().parents[2]
    / "agents"
    / "mandate_risk_v2_lab"
    / "metric-display-groups.json"
)

_OPERATOR_LABELS = {
    "LT": "<",
    "LTE": "<=",
    "GT": ">",
    "GTE": ">=",
    "EQ": "=",
    "==": "=",
}
_RANGE_OPERATORS = {"BETWEEN", "RANGE"}


def _groups() -> dict[str, str]:
    data = json.loads(GROUPS_PATH.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for group, names in data.items():
        for name in names:
            if name in result:
                raise ValueError(f"duplicate display group metric: {name}")
            result[name] = group
    return result


def _cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\r\n", "<br>").replace("\n", "<br>")


def _json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _scalar_with_unit(value: Any, unit: str | None) -> str:
    text = str(value)
    if not unit:
        return text
    if unit == "%":
        return f"{text}%"
    return f"{text} {unit}"


def format_requirement_constraint(requirement: Requirement) -> str:
    """Render only facts already frozen in Requirement IR; never derive a new threshold."""

    constraint = requirement.constraint
    if constraint is None:
        return "—"

    operator = str(constraint.operator or "").strip()
    normalized_operator = _OPERATOR_LABELS.get(operator.upper(), operator)
    upper_operator = operator.upper()
    if upper_operator in _RANGE_OPERATORS and constraint.value is not None and constraint.value_to is not None:
        rendered = (
            f"{_scalar_with_unit(constraint.value, constraint.unit)} ~ "
            f"{_scalar_with_unit(constraint.value_to, constraint.unit)}"
        )
    elif constraint.value is not None:
        value = _scalar_with_unit(constraint.value, constraint.unit)
        rendered = f"{normalized_operator} {value}".strip()
    elif constraint.formula:
        rendered = str(constraint.formula)
    elif operator:
        rendered = normalized_operator
    else:
        rendered = "—"

    if constraint.benchmark:
        rendered += f"；Benchmark：{constraint.benchmark}"
    return rendered


def _append_evidence(lines: list[str], evidence) -> None:
    for item in evidence:
        page = f"第 {item.page} 页" if item.page is not None else "页码未知"
        lines.extend([f"> {item.text}（{page}）", ""])


def _append_requirement_details(lines: list[str], requirement: Requirement) -> None:
    constraint = requirement.constraint
    lines.extend(
        [
            f"- Requirement 类型：`{requirement.requirement_type}`",
            f"- Requirement：{requirement.semantic_summary}",
            f"- 结构化约束：`{format_requirement_constraint(requirement)}`",
        ]
    )
    if constraint is not None and constraint.raw_value_text:
        lines.append(f"- 原始范围表达：`{constraint.raw_value_text}`")
    if requirement.measurement.concept:
        lines.append(f"- Measurement concept：{requirement.measurement.concept}")
    if requirement.measurement.object is not None:
        lines.append(f"- Measurement object：{_json_text(requirement.measurement.object)}")
    if requirement.scope:
        lines.append(f"- Scope：`{_json_text(requirement.scope)}`")
    if requirement.conditions:
        lines.append(f"- Conditions：`{_json_text(requirement.conditions)}`")
    if requirement.exceptions:
        lines.append(f"- Exceptions：`{_json_text(requirement.exceptions)}`")
    if constraint is not None and constraint.attributes:
        lines.append(f"- Constraint qualifiers：`{_json_text(constraint.attributes)}`")


def _append_destination(lines: list[str], item: DestinationResultItem) -> None:
    requirement = item.requirement.requirement
    lines.extend(
        [
            f"### {requirement.requirement_id} / {item.aspect}",
            "",
        ]
    )
    _append_requirement_details(lines, requirement)
    if item.candidate_metrics:
        names = ", ".join(metric.metric_name for metric in item.candidate_metrics)
        lines.append(f"- 关联指标库候选：{names}")
    lines.extend([f"- 最终原因：{item.reason}", "", "**文档依据**", ""])
    _append_evidence(lines, item.evidence)


def render_v2_report(
    *,
    ir: RequirementIR,
    clauses: Sequence[DocumentClause],
    registry: RawRiskMetricRegistry,
    mapping: MappingResult,
    analysis: V2AnalysisResult | None = None,
) -> str:
    analysis = analysis or build_v2_analysis_result(
        ir=ir,
        clauses=clauses,
        registry=registry,
        mapping=mapping,
    )
    groups = _groups()
    lines = [
        "# Mandate 风险指标报告（V2）",
        "",
        f"- 文档：{analysis.document_name}",
        f"- 指标库：{analysis.metric_catalogue_name}",
        f"- 指标库 SHA-256：{analysis.metric_catalogue_sha256 or '未提供'}",
        f"- 结果摘要：{analysis.summary}",
        "",
        "## 匹配摘要",
        "",
        "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for matched in analysis.matched_metrics:
        metric = matched.metric
        # Preserve the original six-column contract: Mandate解读 remains
        # verbatim Python-owned contract evidence. Multiple Requirements are
        # shown as separate evidence snippets rather than collapsed into an AI
        # summary; normalized constraints live in the detail section below.
        summaries = "<br>".join(
            _cell(
                item.requirement.evidence[0].text
                if item.requirement.evidence
                else item.requirement.requirement.semantic_summary
            )
            for item in matched.requirements
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(groups.get(metric.metric_name, "待分类")),
                    _cell(metric.metric_name),
                    summaries or "—",
                    "—",
                    "—",
                    "—",
                ]
            )
            + " |"
        )
    if not analysis.matched_metrics:
        lines.extend(["", "当前没有通过独立复核的主表指标。"])

    lines.extend(["", "## 主表指标依据与合同要求", ""])
    if not analysis.matched_metrics:
        lines.append("无。")
    for matched in analysis.matched_metrics:
        metric = matched.metric
        lines.extend(
            [
                f"### {metric.metric_name}",
                "",
                f"- 原始库行：{metric.source_row}",
                f"- 指标算法（原始值）：{metric.algorithm or '空'}",
                f"- 指标库 Mandate（原始值）：{metric.mandate or '空'}",
                "",
            ]
        )
        for link_index, link in enumerate(matched.requirements, start=1):
            requirement = link.requirement.requirement
            lines.extend(
                [
                    f"#### 合同要求 {link_index}：{requirement.requirement_id}",
                    "",
                ]
            )
            _append_requirement_details(lines, requirement)
            lines.extend([f"- 映射理由：{link.mapping_reason}", "", "**文档依据**", ""])
            _append_evidence(lines, link.mapping_evidence)
            lines.extend(["**逐维兼容审查**", ""])
            for item in link.compatibility:
                lines.extend(
                    [
                        f"- **{item.dimension}**：{item.relation}",
                        f"  - 合同依据：{item.requirement_basis}",
                        f"  - 指标库依据：{item.metric_basis}",
                        f"  - 判断：{item.reason}",
                    ]
                )
            lines.append("")

    lines.extend(["## 待确认", ""])
    if not analysis.pending_review:
        lines.append("无。")
    for item in analysis.pending_review:
        _append_destination(lines, item)

    lines.extend(["", "## 指标库缺口", ""])
    if not analysis.library_gaps:
        lines.append("无。")
    for item in analysis.library_gaps:
        _append_destination(lines, item)

    lines.extend(["", "## 非指标要求", ""])
    if not analysis.non_metric_requirements:
        lines.append("无。")
    for item in analysis.non_metric_requirements:
        _append_destination(lines, item)

    lines.extend(["", "## 未解决 Requirement", ""])
    if not analysis.unresolved_requirements:
        lines.append("无。Phase A 当前采用 fail-closed；成功完成的正式结果不会静默保留未解决 Requirement。")
    else:
        for item in analysis.unresolved_requirements:
            lines.append(f"- {item.requirement.requirement_id}：{item.requirement.semantic_summary}")

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 主表只包含合同直接支持、已通过逐维兼容审查及独立 Critic 复核的原始库指标。",
            "- 主表“值”表示实际组合值；当前没有权威持仓/组合数据，因此仍显示“—”。PDF 中的阈值、范围和时点在“合同要求”中单独展示，避免把 Mandate 要求误当成实际组合值。",
            "- 参考组合、相似度没有权威数据，统一显示“—”；系统不会编造数值或伪精确相似度。",
            "- 同一正式指标可保留多条独立 Requirement，各自保留约束、条件、证据和兼容审查，不在展示层强行合并。",
            "- 待确认、指标库缺口和非指标要求与主表分开；合同原文保持可追溯，不创建新指标。",
        ]
    )
    return "\n".join(lines).strip() + "\n"
