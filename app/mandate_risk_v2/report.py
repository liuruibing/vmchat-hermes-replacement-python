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
    elif operator and constraint.benchmark:
        return f"{normalized_operator} {constraint.benchmark}"
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
        ir=ir, clauses=clauses, registry=registry, mapping=mapping,
    )
    groups = _groups()
    lines = [
        "# Mandate 风险指标筛选报告（V2）", "",
        f"- 文档：{analysis.document_name}",
        f"- 指标库：{analysis.metric_catalogue_name}",
        f"- 指标库 SHA-256：{analysis.metric_catalogue_sha256 or '未提供'}",
        f"- 结果摘要：{analysis.summary}", "",
        "## 筛选结果", "",
        "相似度显示模型评估的 PDF 要求匹配分（0–100），用于筛选和排序，不是统计校准的正确概率。",
        "同一指标关联多个要求时，表格使用最高关联分；各要求的评分与差异在详情中分别保留。高分不代表覆盖整个 PDF 的全部要求。", "",
        "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for selected in analysis.screened_metrics:
        quotes = "<br>".join(_cell(item.requirement.evidence[0].text)
                              for item in selected.requirements if item.requirement.evidence)
        score = f"{selected.match_score:g}/100" if selected.match_score is not None else "未评分"
        lines.append("| " + " | ".join([
            _cell(groups.get(selected.metric.metric_name, "待分类")),
            _cell(selected.metric.metric_name), quotes or "—", "—", "—", score,
        ]) + " |")
    if not analysis.screened_metrics:
        lines.extend(["", "当前没有筛选出有文档依据的相关指标。"])

    lines.extend(["", "## 指标匹配依据", ""])
    if not analysis.screened_metrics:
        lines.append("无。")
    for selected in analysis.screened_metrics:
        metric = selected.metric
        score = f"{selected.match_score:g}/100" if selected.match_score is not None else "未评分"
        lines.extend([
            f"### {metric.metric_name}", "",
            f"- 匹配分：{score}",
            f"- 评分理由：{selected.score_reason or '历史结果未评分'}",
            f"- 原始库行：{metric.source_row}",
            f"- 指标算法（原始值）：{metric.algorithm or '未提供，供用户确认'}",
            f"- 指标库 Mandate（原始值）：{metric.mandate or '未提供'}", "",
        ])
        for link in selected.requirements:
            requirement = link.requirement.requirement
            score = f"{link.match_score:g}/100" if link.match_score is not None else "未评分"
            lines.extend([f"#### 合同要求：{requirement.requirement_id}", ""])
            _append_requirement_details(lines, requirement)
            lines.extend([
                f"- 该要求匹配分：{score}",
                f"- 评分理由：{link.score_reason or '历史结果未评分'}",
                f"- 关联理由：{link.mapping_reason}",
            ])
            lines.extend(f"- 差异说明：{note}" for note in link.review_notes)
            for dimension in link.compatibility:
                if dimension.relation in {"INSUFFICIENT", "CONFLICT"}:
                    lines.append(f"- 口径差异（{dimension.dimension}）：{dimension.reason}；"
                                 f"合同：{dimension.requirement_basis}；指标库：{dimension.metric_basis}")
            lines.extend(["", "**合同原文**", ""])
            _append_evidence(lines, link.mapping_evidence)

    for title, items in (("需用户关注的差异与待确认项", analysis.pending_review),
                         ("未找到相关指标的要求", analysis.library_gaps),
                         ("非指标要求", analysis.non_metric_requirements)):
        lines.extend(["", f"## {title}", ""])
        if not items:
            lines.append("无。")
        for item in items:
            _append_destination(lines, item)

    lines.extend([
        "", "## 说明", "",
        "- 结果用于筛选相关指标，不表示自动入库、合规通过或算法完全等价。算法缺失、年化/事前口径不明等差异保留在详情中，供用户判断。",
        "- 主表“值”表示实际组合值；当前没有权威持仓/组合数据，因此显示“—”。PDF 阈值在合同要求详情中展示，不作为实际组合值。",
        "- 参考组合没有权威数据，显示“—”；相似度来自本次模型的文档匹配评估，与参考组合比较无关。",
        "- 历史输出没有评分时显示“未评分”，不自动补造分数。",
    ])
    return "\n".join(lines).strip() + "\n"
