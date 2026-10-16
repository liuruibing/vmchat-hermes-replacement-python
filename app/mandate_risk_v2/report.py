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
from app.mandate_risk_v2.reference_portfolio import ReferencePortfolioResolver


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

def _reference_cell(item: Any) -> str:
    portfolios = getattr(item, "reference_portfolios", None)
    if portfolios:
        return _cell(ReferencePortfolioResolver.format_reference_cell(portfolios))
    return "—"


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
    if requirement.attributes.get("source_heading"):
        lines.append(f"- 原文章节：{requirement.attributes['source_heading']}")
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


def render_screening_report(analysis: V2AnalysisResult) -> str:
    groups = _groups()
    lines = ["# Mandate 风险指标筛选报告（快速筛选）", "",
             f"- 文档：{analysis.document_name}",
             f"- 指标库：{analysis.metric_catalogue_name}",
             f"- 结果摘要：{analysis.summary}", "",
             "本次直接依据 PDF 和指标库筛选，未执行逐条要求覆盖审计或独立复核。匹配分用于排序，供人工选择，不表示合规结论或算法完全等价。", "",
             "## 筛选结果", "",
             "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
             "| --- | --- | --- | --- | --- | --- |"]
    for item in analysis.screened_metrics:
        lines.append("| " + " | ".join([
            _cell(groups.get(item.metric.metric_name, "待分类")), _cell(item.metric.metric_name),
            _cell(item.score_reason or ""), "—", _reference_cell(item), f"{item.match_score:g}/100",
        ]) + " |")
    if not analysis.screened_metrics:
        lines.extend(["", "当前没有筛选出有文档依据的相关指标。"])
    lines.extend(["", "## 指标匹配依据", ""])
    for item in analysis.screened_metrics:
        lines.extend([f"### {item.metric.metric_name}", "", f"- 匹配分：{item.match_score:g}/100",
                      f"- 原始库行：{item.metric.source_row}",
                      f"- 指标算法（原始值）：{item.metric.algorithm or '未提供，供用户确认'}", ""])
        for link in item.requirements:
            lines.append(f"- 关联理由：{link.mapping_reason}")
            lines.extend(f"- 需确认：{note}" for note in link.review_notes)
            lines.extend(["", "**PDF 原文**", ""])
            _append_evidence(lines, link.mapping_evidence)
    return "\n".join(lines).strip() + "\n"


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
        "本报告先识别原文要求并复核覆盖，再关联指标库。交易禁令、配置和治理要求不因没有对应指标而省略；模型覆盖复核不等于已完成合规检查。", "",
        "## 原文要求与处置", "",
    ]
    destinations = {
        item.requirement_id: item.destinations
        for item in mapping.dispositions.dispositions
    }
    labels = {"MAIN_TABLE": "直接关联", "PENDING_REVIEW": "待确认",
              "LIBRARY_GAP": "指标库缺口", "NON_METRIC": "规则/非指标要求"}
    for item in analysis.requirements:
        requirement = item.requirement
        lines.extend([f"### {requirement.requirement_id} {requirement.attributes.get('source_heading', '')}", ""])
        _append_requirement_details(lines, requirement)
        for destination in destinations.get(requirement.requirement_id, []):
            names = "、".join(registry.require(row_id).metric_name for row_id in destination.raw_row_ids)
            lines.append(f"- {labels[destination.destination]} / {destination.aspect}"
                         f"{' / ' + names if names else ''}：{destination.reason}")
        lines.extend(["", "**PDF 原文**", ""])
        _append_evidence(lines, item.evidence)
    if analysis.contextual_facts:
        lines.extend(["", "## 文档配置与上下文", ""])
        for fact in analysis.contextual_facts:
            lines.append(f"- {fact.fact_type}：{fact.semantic_summary}")
    lines.extend([
        "", "## 指标关联结果", "",
        "DIRECT 为原文明示测量概念的直接关联；REVIEW 为待确认候选，不代表合同要求使用该指标。匹配分仅用于排序，不表示合规或算法等价。",
        "", "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ])
    for selected in analysis.screened_metrics:
        quotes = "<br>".join(_cell(item.requirement.evidence[0].text)
                              for item in selected.requirements if item.requirement.evidence)
        score = f"{selected.match_score:g}/100" if selected.match_score is not None else "未评分"
        lines.append("| " + " | ".join([
            _cell(groups.get(selected.metric.metric_name, "待分类")),
            _cell(selected.metric.metric_name), quotes or "—", "—", _reference_cell(selected), score,
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
                f"- 关联性质：{link.mapping_level}",
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
        "- “参考组合”展示基于生产配置快照匹配的基准/参考投资组合；无匹配或来源不可用时显示“—”。相似度来自本次模型的文档匹配评估，与参考组合比较无关。",
        "- 历史输出没有评分时显示“未评分”，不自动补造分数。",
    ])
    return "\n".join(lines).strip() + "\n"
