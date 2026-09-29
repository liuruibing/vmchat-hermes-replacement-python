from __future__ import annotations

import json
from typing import Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS
from app.mandate_risk_v2.models import RequirementIR

_CORE_DIMENSIONS_TEXT = ", ".join(CORE_COMPATIBILITY_DIMENSIONS)

MAPPING_SYSTEM_PROMPT = f"""你是 Mandate Requirement 与原始风险指标库的语义映射员。
只用 Requirement IR、逐字条款及给定原始库行作判断，不创造新指标，不按相似词宣称算法等价。
对每个候选比较 measurement object、aggregation level、scope、denominator、time point、annualisation、ex-ante/ex-post、benchmark、unit semantics、conditions、strategy applicability 和 algorithm semantics，以及合同新增限定词。
每个 DIRECT 或 REVIEW link 的 compatibility 必须完整覆盖以下核心维度，dimension 必须使用这些精确英文值；即使某维度确实不适用，也必须显式写 NOT_APPLICABLE，绝不能省略：{_CORE_DIMENSIONS_TEXT}。
measurement_object 与 algorithm_semantics 对 DIRECT 必须是 EQUIVALENT；不能用 NOT_APPLICABLE 绕过正式指标等价判断。
aggregation_level 专门核对 single security / purchase / issuer / fund / portfolio / underlying fund 等聚合层级；unit_semantics 专门核对 return、yield、spread、bps、percentage、days、rating 等度量语义，不能只看表面单位相同。
estimation_basis 专门核对 ex-ante/ex-post、预测/实现口径等估计基础；strategy_applicability 必须核对 Requirement/IR 支持的策略、资产对象与 metric.strategy_type，不能只因主题相似就视为适用；algorithm_semantics 必须以原始库 algorithm 为依据，库算法为空或没有说明合同关键口径时不得猜测 EQUIVALENT。
合同还存在 confidence level、lookback、holding period、purchase-time、underlying-fund level 等额外限定词时，应增加开放的额外 compatibility dimension；这些额外维度不能替代核心维度。
compatibility 每个维度写合同依据、库算法/库字段依据、关系和理由。库算法/定义没交代的口径标 INSUFFICIENT，不可猜等价。关系冲突标 CONFLICT。
compatibility.relation 只允许以下四个精确英文值：EQUIVALENT、INSUFFICIENT、CONFLICT、NOT_APPLICABLE。绝不可输出 MATCH、MISMATCH、PARTIAL、UNKNOWN 等同义词。
DIRECT 仅用于合同直接支持、测量对象与全部必要限定词等价的库行；其余相关候选用 REVIEW，明显不符用 REJECTED。DIRECT 不能存在 INSUFFICIENT 或 CONFLICT。
每个 link 的 evidence_clause_ids 必须至少包含所引用 Requirement 自身 evidence.clause_ids 中的一项；定义、上下文或与该 Requirement 通过 IR relation 明确关联的 Requirement clause 可作补充，不能取代主证据。不要引用无 relation 的其他 Requirement clause，不得发明 clause_id。
Python 不做业务语义判断；你必须完整审计分配给你的每个库行。只输出一个 JSON 对象。"""

DESTINATION_SYSTEM_PROMPT = """你是 Mandate Requirement 去向审计员。
对每个 Requirement 完整说明所有可区分的条件分支和测量 aspect，去向只能是 MAIN_TABLE、PENDING_REVIEW、LIBRARY_GAP、NON_METRIC。
MAIN_TABLE 必须引用已有 DIRECT link；PENDING_REVIEW 若引用指标行，则每个指标行都必须来自已有 REVIEW link，不能把 REJECTED 或 DIRECT 候选改挂到待确认；LIBRARY_GAP 必须在已检查完整库后才能确认；NON_METRIC 仅用于确实属于治理、许可/禁止、流程或其他不应映射为正式风险指标的要求，不能把有明确测量对象的量化要求当成 NON_METRIC 逃避映射。
一个 Requirement 可以有多个不同 aspect 去向，不能因一个 aspect 映射成功而隐藏另一个缺口。每个 destination 引用原 Requirement 的 clause_id。只输出一个 JSON 对象。"""

CRITIC_SYSTEM_PROMPT = """你是独立 Mandate 映射 Critic。不要沿用映射员结论；独立核对 Requirement、逐字合同、完整原始指标库、候选 Compatibility Matrix 和 destinations。
必须逐项审查所有 MAIN_TABLE/DIRECT：合同是否真的支持，核心 Compatibility Matrix 是否完整，库算法是否与对象、聚合层级、范围、分母、时点、年化、事前/事后、基准、单位语义、条件分支、策略适用性以及合同额外限定词等价。
必须逐项审查所有 LIBRARY_GAP：完整库里是否有被漏掉的等价候选，或合同本身是否不构成该缺口。
必须逐项审查所有 NON_METRIC：确认该 Requirement 确实不应映射为正式风险指标，特别关注 QUANTITATIVE_TARGET、QUANTITATIVE_LIMIT、CONDITIONAL_RULE，防止量化要求被静默归入 NON_METRIC。
对每项返回 CONFIRM、CHALLENGE 或 UNRESOLVED；异议说出具体原文/库行证据。不得为凑表放宽标准。只输出一个 JSON 对象。"""


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _rows(rows: Sequence[RawRiskMetric]):
    return [{"row_id": row.row_id, "name": row.metric_name, "algorithm": row.algorithm,
             "mandate": row.mandate, "strategy_type": row.strategy_type} for row in rows]


def _evidence(ir: RequirementIR, clauses: Sequence[DocumentClause]):
    used = {cid for item in (*ir.requirements, *ir.definitions, *ir.contextual_facts)
            for cid in item.evidence.clause_ids}
    return [{"clause_id": clause.clause_id, "page": clause.page, "text": clause.text}
            for clause in clauses if clause.clause_id in used]


def batch_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                 feedback: str | None = None) -> str:
    parts = ["# V2 mapping batch", "# Requirement IR (JSON)", _json(ir.model_dump()),
             "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
             "# Raw metric rows (JSON)", _json(_rows(rows)),
             "# Required core compatibility dimensions", _json(list(CORE_COMPATIBILITY_DIMENSIONS)),
             'compatibility 项 JSON 形状必须为 {"dimension":"denominator","requirement_basis":"合同原文支持的口径","metric_basis":"库算法支持的口径","relation":"EQUIVALENT","reason":"双方依据"}；relation 只能取 EQUIVALENT / INSUFFICIENT / CONFLICT / NOT_APPLICABLE。DIRECT/REVIEW 必须逐项返回全部核心维度；额外限定词另加 dimension。',
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
                  links, dispositions, feedback: str | None = None) -> str:
    parts = [
        "# V2 independent critic", "# Requirement IR (JSON)", _json(ir.model_dump()),
        "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
        "# Complete raw metric catalogue (JSON)", _json(_rows(rows)),
        "# Validated mapping links (JSON)", _json([x.model_dump() for x in links]),
        "# Proposed destinations (JSON)", _json(dispositions.model_dump()),
        "返回 {verdicts:[{requirement_id,destination,raw_row_id,aspect,verdict,reason,evidence_clause_ids}]}。对每个 MAIN_TABLE 库行、每个 LIBRARY_GAP aspect 和每个 NON_METRIC aspect 恰好一项；LIBRARY_GAP/NON_METRIC 的 raw_row_id 为 null。",
    ]
    if feedback:
        parts.extend(["# Previous critic validation feedback", feedback])
    return "\n".join(parts)
