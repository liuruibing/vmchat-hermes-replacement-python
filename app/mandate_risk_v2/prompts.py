from __future__ import annotations

import json
from typing import Iterable, Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.models import RequirementIR


EXTRACTION_SYSTEM_PROMPT = """你是投资委托文件（Mandate）的文档理解器。

你的任务是忠实理解输入条款本身，而不是寻找任何预设风险指标。

严格规则：
1. 当前阶段没有风险指标库。不要猜测、发明或推荐正式指标名称。
2. 区分 Requirement、Definition、Context。定义不是监控要求；背景事实不是限额。
3. Requirement 必须表示文件真实表达的目标、策略、范围、量化目标/限额、禁止、许可、条件规则、外部政策要求或治理要求。
4. 复杂条件必须保留所有分支、阈值、单位、时点、scope、例外。不要把多档条件压缩成一条模糊总结。
5. evidence 只能返回输入中真实存在的 clause_id。不要返回 page，不要自行复制或改写原文作为证据。
6. 不得跨页拼接成输入中不存在的单条原文。需要多个条款共同支持时列出多个 clause_id。
7. measurement / qualifiers / scope / conditions / attributes 是开放语义字段。只填写原文能够支持的信息，不要为了填满 schema 猜测。
8. local_id 只需在当前批次唯一，例如 r1、r2、d1、c1。
9. Coverage Reviewer 的反馈只是重新检查线索。必须重新依据原始 clauses 判断，不能无条件接受反馈。
10. 只输出一个 JSON 对象，不要输出 Markdown 或解释文字。
"""


COVERAGE_SYSTEM_PROMPT = """你是 Mandate Requirement Coverage Reviewer。

你不负责重新做风险指标匹配。你只审核：当前 Requirement IR 是否完整覆盖了输入文档中重要的目标、义务、限制、禁止、许可、条件分支和例外。

严格规则：
1. 不因为句子含数字就自动认定它是 Requirement；Definition、页码、版本号、日期背景等可合理排除。
2. 重点检查：明确量化限额/目标、shall/must/may only/not permitted 等义务语气、if/unless/except 条件分支、复合阈值、scope/denominator/measurement basis。
3. 如果一个多档或复合规则只抽取了一部分，放入 partial_requirements，而不是假装已覆盖。
4. missing_clauses 和 related_clause_ids 只能引用真实输入 clause_id。
5. partial_requirements 只能引用真实 requirement_id。
6. Python 提供的 coverage hints 只是“值得重点检查”的线索，不是结论。
7. 不要创建或讨论正式风险指标。
8. 只输出一个 JSON 对象，不要输出 Markdown 或解释文字。
"""


def _clause_payload(clauses: Iterable[DocumentClause]):
    return [
        {"clause_id": clause.clause_id, "page": clause.page, "text": clause.text}
        for clause in clauses
    ]


def build_extraction_prompt(
    *,
    document_name: str,
    clauses: Sequence[DocumentClause],
    batch_index: int = 1,
    batch_count: int = 1,
    review_feedback: dict | None = None,
) -> str:
    metadata = {
        "document_name": document_name,
        "batch_index": batch_index,
        "batch_count": batch_count,
    }
    schema_example = {
        "requirements": [
            {
                "local_id": "r1",
                "requirement_type": "QUANTITATIVE_LIMIT",
                "semantic_summary": "用当前文档语言忠实概括该要求",
                "subject": {"text": "", "normalized_type": None},
                "measurement": {"concept": None, "object": None, "qualifiers": {}},
                "constraint": {
                    "operator": "<=",
                    "value": 10,
                    "unit": "%",
                    "formula": None,
                    "benchmark": None,
                    "attributes": {},
                },
                "scope": {},
                "conditions": [],
                "exceptions": [],
                "relations": [],
                "evidence": {"clause_ids": ["c0001"]},
                "attributes": {},
            }
        ],
        "definitions": [
            {
                "local_id": "d1",
                "term": "Example Term",
                "semantic_summary": "定义内容",
                "evidence": {"clause_ids": ["c0002"]},
            }
        ],
        "contextual_facts": [
            {
                "local_id": "c1",
                "fact_type": "BENCHMARK",
                "semantic_summary": "上下文事实",
                "value": None,
                "evidence": {"clause_ids": ["c0003"]},
                "attributes": {},
            }
        ],
    }
    parts = [
        "# Requirement extraction batch",
        json.dumps(metadata, ensure_ascii=False, separators=(",", ":")),
        "# Input clauses (JSON)",
        json.dumps(_clause_payload(clauses), ensure_ascii=False, separators=(",", ":")),
    ]
    if review_feedback:
        parts.extend(
            [
                "# Previous coverage review feedback (JSON; review hints only)",
                json.dumps(review_feedback, ensure_ascii=False, separators=(",", ":")),
                "请重新独立阅读本批 clauses，并重点检查反馈指出的遗漏/不完整点；若反馈不被原文支持，不要照抄。",
            ]
        )
    parts.extend(
        [
            "# Required output shape (example only; do not copy example values)",
            json.dumps(schema_example, ensure_ascii=False, separators=(",", ":")),
            "请从 Input clauses 中完整提取 Requirements / Definitions / Contextual facts。",
        ]
    )
    return "\n".join(parts)


def build_coverage_review_prompt(
    *,
    document_name: str,
    clauses: Sequence[DocumentClause],
    requirement_ir: RequirementIR,
    coverage_hints: list[dict],
) -> str:
    output_shape = {
        "missing_clauses": [
            {"clause_id": "c0001", "reason": "说明为什么当前 IR 没有覆盖该重要要求"}
        ],
        "partial_requirements": [
            {
                "requirement_id": "REQ-0001",
                "reason": "说明缺少的 branch / threshold / scope / qualifier",
                "related_clause_ids": ["c0002"],
            }
        ],
    }
    return "\n".join(
        [
            "# Requirement coverage review",
            json.dumps({"document_name": document_name}, ensure_ascii=False, separators=(",", ":")),
            "# All canonical clauses (JSON)",
            json.dumps(_clause_payload(clauses), ensure_ascii=False, separators=(",", ":")),
            "# Current Requirement IR (JSON)",
            json.dumps(requirement_ir.model_dump(), ensure_ascii=False, separators=(",", ":")),
            "# Python coverage hints (JSON; hints only, not conclusions)",
            json.dumps(coverage_hints, ensure_ascii=False, separators=(",", ":")),
            "# Required output shape",
            json.dumps(output_shape, ensure_ascii=False, separators=(",", ":")),
            "如果没有遗漏或部分覆盖，两个数组都返回空数组。",
        ]
    )
