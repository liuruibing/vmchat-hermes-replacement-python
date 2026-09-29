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
4. requirement_type 只能是：OBJECTIVE、STRATEGY、SCOPE、QUANTITATIVE_TARGET、QUANTITATIVE_LIMIT、PROHIBITION、PERMISSION、CONDITIONAL_RULE、EXTERNAL_POLICY、GOVERNANCE、OTHER。
5. 复杂条件必须保留所有分支、阈值、单位、时点、scope、例外。不要把多档条件压缩成一条模糊总结。
6. evidence 只能返回输入中真实存在的 clause_id。不要返回 page，不要自行复制或改写原文作为证据。
7. 不得跨页拼接成输入中不存在的单条原文。需要多个条款共同支持时列出多个 clause_id。
8. measurement / qualifiers / scope / conditions / attributes 是开放语义字段。只填写原文能够支持的信息，不要为了填满 schema 猜测。
9. relations 可选；type 只能是 BRANCH_OF、QUALIFIES、EXCEPTION_TO、DEFINES_SCOPE_FOR、DEPENDS_ON，target_local_id 必须指向当前批次真实 Requirement local_id。不确定时留空。
10. local_id 只需在当前批次唯一，例如 r1、r2、d1、c1。
11. Coverage Reviewer 的反馈只是重新检查线索。必须重新依据原始 clauses 判断，不能无条件接受反馈。
12. 只输出一个 JSON 对象，不要输出 Markdown 或解释文字。
"""


COVERAGE_SYSTEM_PROMPT = """你是 Mandate Requirement Coverage Reviewer。

你不负责重新做风险指标匹配。你只审核：当前 Requirement IR 是否完整覆盖了输入文档中重要的目标、义务、限制、禁止、许可、条件分支和例外。

严格规则：
1. 不因为句子含数字就自动认定它是 Requirement；Definition、页码、版本号、日期背景等可合理排除。
2. 重点检查：明确量化限额/目标、shall/must/may only/not permitted 等义务语气、if/unless/except 条件分支、复合阈值、scope/denominator/measurement basis。
3. 如果一个多档或复合规则只抽取了一部分，放入 partial_requirements，而不是假装已覆盖。
4. missing_clauses 和 related_clause_ids 只能引用真实输入 clause_id。
5. partial_requirements 只能引用真实 requirement_id。
6. 对 Python coverage hints 中的每一个 clause_id，必须在 hint_assessments 中恰好返回一次处置，不得省略。disposition 只能是 COVERED、DEFINITION_OR_CONTEXT、NOT_REQUIREMENT、MISSING、PARTIAL。
7. COVERED/PARTIAL 必须给出直接引用该 clause 的真实 requirement_ids，并且 requirement_ids 只能从“Deterministic requirement evidence map”中该 clause_id 对应的列表选择；如果该列表为空，不得标记 COVERED/PARTIAL。DEFINITION_OR_CONTEXT、NOT_REQUIREMENT、MISSING 不得填 requirement_ids。
8. Python coverage hints 只是“值得重点检查”的线索，不是结论；你必须根据原文和当前 IR 独立判断。
9. 如果上一轮 Reviewer 输出因确定性校验失败，必须根据校验错误纠正引用关系或处置；不要重复同一个无效引用。
10. 不要创建或讨论正式风险指标。
11. 只输出一个 JSON 对象，不要输出 Markdown 或解释文字。
"""


def _clause_payload(clauses: Iterable[DocumentClause]):
    return [
        {"clause_id": clause.clause_id, "page": clause.page, "text": clause.text}
        for clause in clauses
    ]


def _requirements_by_hint_clause(
    requirement_ir: RequirementIR,
    coverage_hints: Sequence[dict],
) -> dict[str, list[str]]:
    result = {str(item["clause_id"]): [] for item in coverage_hints}
    for requirement in requirement_ir.requirements:
        for clause_id in requirement.evidence.clause_ids:
            if clause_id in result:
                result[clause_id].append(requirement.requirement_id)
    return result


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
    validation_feedback: str | None = None,
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
        "hint_assessments": [
            {
                "clause_id": "c0003",
                "disposition": "COVERED",
                "requirement_ids": ["REQ-0002"],
                "reason": "说明该高风险线索如何被当前 IR 覆盖；若不是 Requirement，也要明确分类原因。",
            }
        ],
    }
    parts = [
        "# Requirement coverage review",
        json.dumps({"document_name": document_name}, ensure_ascii=False, separators=(",", ":")),
        "# All canonical clauses (JSON)",
        json.dumps(_clause_payload(clauses), ensure_ascii=False, separators=(",", ":")),
        "# Current Requirement IR (JSON)",
        json.dumps(requirement_ir.model_dump(), ensure_ascii=False, separators=(",", ":")),
        "# Python coverage hints (JSON; every hint must be assessed exactly once)",
        json.dumps(coverage_hints, ensure_ascii=False, separators=(",", ":")),
        "# Deterministic requirement evidence map for hinted clauses (JSON)",
        json.dumps(
            _requirements_by_hint_clause(requirement_ir, coverage_hints),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
    ]
    if validation_feedback:
        parts.extend(
            [
                "# Previous coverage review failed deterministic validation (JSON)",
                json.dumps({"error": validation_feedback}, ensure_ascii=False, separators=(",", ":")),
                "请纠正整个 coverage review。若某 hint 没有直接引用它的 Requirement，不要声称它已 COVERED；应依据原文改判为 MISSING、NOT_REQUIREMENT 或 DEFINITION_OR_CONTEXT。",
            ]
        )
    parts.extend(
        [
            "# Required output shape",
            json.dumps(output_shape, ensure_ascii=False, separators=(",", ":")),
            "即使没有遗漏，missing_clauses/partial_requirements 返回空数组，但 hint_assessments 仍必须逐条覆盖所有 Python coverage hints。",
        ]
    )
    return "\n".join(parts)
