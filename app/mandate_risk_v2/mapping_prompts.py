from __future__ import annotations

import json
from typing import Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk_v2.models import RequirementIR


MAPPING_SYSTEM_PROMPT = """你是 Mandate Requirement 与原始风险指标库的语义映射员。
只用 Requirement IR、逐字条款及给定原始库行作判断，不创造新指标，不按相似词宣称算法等价。
对每个候选比较 measurement object、scope、denominator、time point、annualisation、ex-ante/ex-post、benchmark、condition，以及合同新增限定词。
compatibility 每个维度写合同依据、库算法依据、关系和理由。库算法/定义没交代的口径标 INSUFFICIENT，不可猜等价。关系冲突标 CONFLICT。
compatibility.relation 只允许以下四个**精确英文值**：EQUIVALENT（双方有依据且同口径）、INSUFFICIENT（一方依据不足或仅部分支持）、CONFLICT（明确不同口径）、NOT_APPLICABLE（该维度无关）。绝不可输出 MATCH、MISMATCH、PARTIAL、UNKNOWN 等同义词。
DIRECT 仅用于合同直接支持、测量对象与全部必要限定词等价的库行；其余相关候选用 REVIEW，明显不符用 REJECTED。
每个 link 的 evidence_clause_ids 必须至少包含所引用 Requirement 自身 evidence.clause_ids 中的一项；定义、上下文或相关 Requirement 的 clause 可作补充，不能取代主证据。不得发明 clause_id。
Python 不做业务语义判断；你必须完整审计分配给你的每个库行。只输出一个 JSON 对象。"""

DESTINATION_SYSTEM_PROMPT = """你是 Mandate Requirement 去向审计员。
对每个 Requirement 完整说明所有可区分的条件分支和测量 aspect，去向只能是 MAIN_TABLE、PENDING_REVIEW、LIBRARY_GAP、NON_METRIC。
MAIN_TABLE 必须引用已有 DIRECT link；PENDING_REVIEW 可引用已有 REVIEW link；LIBRARY_GAP 必须在已检查完整库后才能确认；NON_METRIC 仅用于确实不属于可测指标的要求。
一个 Requirement 可以有多个不同 aspect 去向，不能因一个 aspect 映射成功而隐藏另一个缺口。每个 destination 引用原 Requirement 的 clause_id。只输出一个 JSON 对象。"""

CRITIC_SYSTEM_PROMPT = """你是独立 Mandate 映射 Critic。不要沿用映射员结论；独立核对 Requirement、逐字合同、完整原始指标库、候选 Compatibility Matrix 和 destinations。
必须逐项审查所有 MAIN_TABLE/DIRECT：合同是否真的支持，库算法是否与对象、范围、分母、时点、年化、事前/事后、基准和条件分支等价。
必须逐项审查所有 LIBRARY_GAP：完整库里是否有被漏掉的等价候选，或合同本身是否不构成该缺口。
对每项返回 CONFIRM、CHALLENGE 或 UNRESOLVED；异议说出具体原文/库行证据。不得为凑表放宽标准。只输出一个 JSON 对象。"""


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _rows(rows: Sequence[RawRiskMetric]):
    return [
        {"row_id": row.row_id, "name": row.metric_name, "algorithm": row.algorithm,
         "mandate": row.mandate, "strategy_type": row.strategy_type}
        for row in rows
    ]


def _evidence(ir: RequirementIR, clauses: Sequence[DocumentClause]):
    used = {
        cid for item in (*ir.requirements, *ir.definitions, *ir.contextual_facts)
        for cid in item.evidence.clause_ids
    }
    return [
        {"clause_id": clause.clause_id, "page": clause.page, "text": clause.text}
        for clause in clauses if clause.clause_id in used
    ]


def batch_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                 feedback: str | None = None) -> str:
    parts = ["# V2 mapping batch", "# Requirement IR (JSON)", _json(ir.model_dump()),
             "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
             "# Raw metric rows (JSON)", _json(_rows(rows)),
             'compatibility 项 JSON 形状必须为 {"dimension":"denominator","requirement_basis":"合同原文支持的口径","metric_basis":"库算法支持的口径","relation":"EQUIVALENT","reason":"双方依据"}；relation 只能取 EQUIVALENT / INSUFFICIENT / CONFLICT / NOT_APPLICABLE，不能取 MATCH / MISMATCH / PARTIAL。',
             "返回 {links:[{requirement_id,raw_row_id,level,compatibility:[{dimension,requirement_basis,metric_basis,relation,reason}],evidence_clause_ids,reason}],row_assessments:[{raw_row_id,outcome,reason}]}。每个库行必须恰好一个 row_assessment。"]
    if feedback:
        parts.extend(["# Previous invalid output feedback", feedback])
    return "\n".join(parts)


def destinations_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                        links, feedback: str | None = None) -> str:
    parts = ["# V2 final destinations", "# Requirement IR (JSON)", _json(ir.model_dump()),
             "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
             "# Complete raw metric catalogue (JSON)", _json(_rows(rows)),
             "# Validated mapping links (JSON)", _json([x.model_dump() for x in links]),
             "返回 {dispositions:[{requirement_id,reason,destinations:[{destination,raw_row_ids,evidence_clause_ids,aspect,reason}]}]}。"]
    if feedback:
        parts.extend(["# Previous review feedback", feedback])
    return "\n".join(parts)


def critic_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                  links, dispositions) -> str:
    return "\n".join([
        "# V2 independent critic", "# Requirement IR (JSON)", _json(ir.model_dump()),
        "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
        "# Complete raw metric catalogue (JSON)", _json(_rows(rows)),
        "# Validated mapping links (JSON)", _json([x.model_dump() for x in links]),
        "# Proposed destinations (JSON)", _json(dispositions.model_dump()),
        "返回 {verdicts:[{requirement_id,destination,raw_row_id,aspect,verdict,reason,evidence_clause_ids}]}。对每个 MAIN_TABLE 库行及每个 LIBRARY_GAP aspect 恰好一项。",
    ])
