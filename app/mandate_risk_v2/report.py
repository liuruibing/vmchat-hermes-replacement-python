from __future__ import annotations

import json
from pathlib import Path
from typing import Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingResult
from app.mandate_risk_v2.models import RequirementIR


GROUPS_PATH = (
    Path(__file__).resolve().parents[2]
    / "agents"
    / "mandate_risk_v2_lab"
    / "metric-display-groups.json"
)


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


def _source_label(registry: RawRiskMetricRegistry) -> str:
    if not registry.source_path:
        return "传入的只读指标库"
    return Path(registry.source_path).name


def render_v2_report(
    *,
    ir: RequirementIR,
    clauses: Sequence[DocumentClause],
    registry: RawRiskMetricRegistry,
    mapping: MappingResult,
) -> str:
    clause_by_id = {item.clause_id: item for item in clauses}
    groups = _groups()
    lines = [
        "# Mandate 风险指标报告（V2）",
        "",
        f"- 文档：{ir.document_name}",
        f"- 指标库：{_source_label(registry)}",
        f"- 指标库 SHA-256：{registry.source_sha256 or '未提供'}",
        "",
        "## 匹配摘要",
        "",
        "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    direct_by_row: dict[int, list] = {}
    requirement_by_id = {item.requirement_id: item for item in ir.requirements}
    for link in mapping.direct_links:
        direct_by_row.setdefault(link.raw_row_id, []).append(link)

    for row_id, links in direct_by_row.items():
        metric = registry.require(row_id)
        lead_link = links[0]
        own_ids = set(requirement_by_id[lead_link.requirement_id].evidence.clause_ids)
        quote_id = next(cid for cid in lead_link.evidence_clause_ids if cid in own_ids)
        quote = clause_by_id[quote_id].text
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(groups.get(metric.metric_name, "待分类")),
                    _cell(metric.metric_name),
                    _cell(quote),
                    "—",
                    "—",
                    "—",
                ]
            )
            + " |"
        )
    if not direct_by_row:
        lines.extend(["", "当前没有通过独立复核的主表指标。"])

    lines.extend(["", "## 主表指标依据", ""])
    if not direct_by_row:
        lines.append("无。")
    for row_id, links in direct_by_row.items():
        metric = registry.require(row_id)
        lines.extend(
            [
                f"### {metric.metric_name}",
                "",
                f"- 原始库行：{metric.source_row}",
                f"- 指标算法（原始值）：{metric.algorithm or '空'}",
                "",
            ]
        )
        cited: set[str] = set()
        for link in links:
            for clause_id in link.evidence_clause_ids:
                if clause_id in cited:
                    continue
                cited.add(clause_id)
                clause = clause_by_id[clause_id]
                page = f"第 {clause.page} 页" if clause.page is not None else "页码未知"
                lines.extend([f"> {clause.text}（{page}）", ""])
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
    pending = [
        (item.requirement_id, dest)
        for item in mapping.dispositions.dispositions
        for dest in item.destinations
        if dest.destination == "PENDING_REVIEW"
    ]
    if not pending:
        lines.append("无。")
    for requirement_id, dest in pending:
        names = ", ".join(registry.require(x).metric_name for x in dest.raw_row_ids) or "未指定库行"
        lines.append(f"- {requirement_id} / {dest.aspect}：{names}；{dest.reason}")

    lines.extend(["", "## 指标库缺口", ""])
    gaps = [
        (item.requirement_id, dest)
        for item in mapping.dispositions.dispositions
        for dest in item.destinations
        if dest.destination == "LIBRARY_GAP"
    ]
    if not gaps:
        lines.append("无。")
    for requirement_id, dest in gaps:
        lines.append(f"### {requirement_id} / {dest.aspect}")
        lines.append(f"- 原因：{dest.reason}")
        for clause_id in dest.evidence_clause_ids:
            clause = clause_by_id[clause_id]
            page = f"第 {clause.page} 页" if clause.page is not None else "页码未知"
            lines.extend([f"> {clause.text}（{page}）", ""])

    lines.extend(["", "## 非指标要求", ""])
    non_metrics = [
        (item.requirement_id, dest)
        for item in mapping.dispositions.dispositions
        for dest in item.destinations
        if dest.destination == "NON_METRIC"
    ]
    if not non_metrics:
        lines.append("无。")
    for requirement_id, dest in non_metrics:
        lines.append(f"### {requirement_id} / {dest.aspect}")
        lines.append(f"- 原因：{dest.reason}")
        for clause_id in dest.evidence_clause_ids:
            clause = clause_by_id[clause_id]
            page = f"第 {clause.page} 页" if clause.page is not None else "页码未知"
            lines.extend([f"> {clause.text}（{page}）", ""])

    lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 主表只包含合同直接支持、已通过逐维兼容审查及独立 Critic 复核的原始库指标。",
            "- 值、参考组合、相似度没有权威组合数据，统一显示“—”。",
            "- 待确认、指标库缺口和非指标要求与主表分开；合同原文保持可追溯，不创建新指标。",
        ]
    )
    return "\n".join(lines).strip() + "\n"
