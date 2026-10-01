from __future__ import annotations

import json
from typing import Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS, critic_targets
from app.mandate_risk_v2.models import RequirementIR

_CORE_DIMENSIONS_TEXT = ", ".join(CORE_COMPATIBILITY_DIMENSIONS)

MAPPING_SYSTEM_PROMPT = f"""你是 Mandate PDF 的风险指标筛选员。任务是筛选符合文档要求、目标、策略或风险暴露的原始库指标，供用户判断；不是确认自动入库、合规通过或算法完全等价。
只用 Requirement IR、逐字原文及给定原始库行，不创造指标、阈值或实际组合数值。
完整浏览分配给你的每个库行；有合理监控用途的指标应保留。合同没有点名指标、库算法为空、年化/事前口径不明，不是自动排除理由，写出差异即可。
每个相关行至少保留一条最有依据的 Requirement link；只有多个独立要求才增加关联，不输出笛卡尔积。仅凭一般风险政策或共同关键词，不能推出整个库都有用；无相关资产暴露的专属指标也不能牵强解释为排除性监控。
level 的含义：DIRECT 是与 PDF 明确测量概念或要求直接对应；REVIEW 是有合理的间接监控关联或适用性仍需用户判断；REJECTED 是无合理用途。DIRECT 不代表算法等价或入库确认。
每个 DIRECT/REVIEW 必须返回 match_score（0–100 的数字）和 score_reason（具体评分理由）。这是模型评估的文档匹配程度，不是统计校准的正确概率、文本向量余弦相似度或用户认可率。
评分参考：90–100 为文档有明确对应要求且对象、资产/策略适用性充分支持；75–89 为业务关联清晰，存在需要说明的口径差异；50–74 为合理但较间接的监控用途或适用条件依据较弱；0–49 为关联弱或有重大不适用因素。独立依据原文评分，不按指标名称、链接类型、固定分数或凑数量评分；不确定性须反映在理由中。Python 不按分数阈值自动过滤。
compatibility 只解释实际影响匹配的维度，不要求填齐十二项。可参考：{_CORE_DIMENSIONS_TEXT}，也可增加合同特有维度；至少解释一个实质关联或差异。
每项写 requirement_basis、metric_basis、relation 和 reason；relation 只能是 EQUIVALENT、INSUFFICIENT、CONFLICT、NOT_APPLICABLE。算法缺失不能猜等价；计价基础、时点、年化、事前/事后或资产适用性差异要写清，但不因差异自动丢掉有用途的指标。
row_assessments.outcome 只能 LINKED 或 NOT_RELEVANT；本批有该行的任意 link 则 LINKED，否则 NOT_RELEVANT。DIRECT、REVIEW、REJECTED 只能用于 link.level。
每个 link 的 evidence_clause_ids 至少包含该 Requirement 自身 evidence.clause_ids 中的一项；定义、上下文和有 IR relation 的其他 Requirement 条款可补充主证据，不发明 clause_id。
只输出一个 JSON 对象。"""

DESTINATION_SYSTEM_PROMPT = """你是 Mandate 筛选结果覆盖审计员。
逐条说明每个 Requirement 的独立对象、时间窗口和条件分支。去向只能 MAIN_TABLE、PENDING_REVIEW、LIBRARY_GAP、NON_METRIC。
MAIN_TABLE 可引用已有 DIRECT 或 REVIEW link，表示该要求有筛选出的相关指标，不代表算法确认或自动入库。PENDING_REVIEW 可引用 DIRECT/REVIEW 指标并说明实际差异；不能引用 REJECTED。
算法不完整、合同未点名指标或口径未确认不构成库缺口；只有完整库确无可合理用于该测量 aspect 的指标时才用 LIBRARY_GAP。NON_METRIC 用于无需风险指标表达的治理、许可、禁止或流程要求，不应隐藏可匹配的测量要求。
一个 Requirement 可有多个不同 aspect 去向；一个 aspect 有指标不能隐藏其他分支。引用原 Requirement 的 clause_id。只输出一个 JSON 对象。"""

CRITIC_SYSTEM_PROMPT = """你是独立 Mandate 指标筛选复核员。独立核对 Requirement、逐字合同、完整原始指标库、关联解释、评分和去向。
任务是帮助用户筛选相关指标，不要求算法完全等价。重点检查漏召回、牵强关联、评分是否符合文档依据；算法缺失或口径差异本身不是删除理由，也不能仅因此质疑一项 MAIN_TABLE 筛选结果。
重新浏览完整库及 NOT_RELEVANT 理由，漏掉的相关指标用 recalled_links 返回，level=REVIEW，并提供 match_score、score_reason、真实 Requirement/库行/原文 ID 和实际兼容维度。
只有明显无业务关联、无合理监控用途或资产/策略明显不适用时才用 rejected_candidates，引用合同说明原因；可以排除已有 DIRECT 或 REVIEW。一般风险政策不意味着所有指标都有用，不为扩大数量引入无相关资产暴露的专属指标。
逐项核对 MAIN_TABLE 是否有合理文档关联；LIBRARY_GAP 是否确无相关筛选指标而非仅缺完全等价算法；NON_METRIC 是否隐藏了可匹配测量对象。按 Required verdict targets 的 target_id 每项恰好返回一次 CONFIRM、CHALLENGE 或 UNRESOLVED；不重写目标的身份字段，批评与重新解释写入 reason。
对所有已有 DIRECT/REVIEW 的 match_score 独立复核。需要修正的分数返回 score_adjustments，字段为 requirement_id、raw_row_id、match_score、score_reason、evidence_clause_ids；不调整则省略或返回空数组。不得按链接类型固定打分或把匹配分说成正确概率。
把原文、conditions、约束及独立测量维度与全部 destinations 对照，包括 PENDING_REVIEW。遗漏的时间窗口、阈值、对象或条件分支用 missing_aspects 显式保留，不能以一个分支代替全部。不要创造 Requirement 或库指标。
只输出一个 JSON 对象。"""


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
    parts = ["# V2 mapping batch", "# Requirement IR (JSON)", _json(ir.model_dump(exclude_none=True, exclude_defaults=True)),
             "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
             "# Raw metric rows (JSON)", _json(_rows(rows)),
             "# Optional compatibility reference dimensions", _json(list(CORE_COMPATIBILITY_DIMENSIONS)),
             'compatibility 项 JSON 形状必须为 {"dimension":"measurement_object","requirement_basis":"合同原文支持的口径","metric_basis":"库算法支持的口径","relation":"EQUIVALENT","reason":"双方依据"}；relation 只能取 EQUIVALENT / INSUFFICIENT / CONFLICT / NOT_APPLICABLE。只写实际相关维度；不要求填齐十二项，口径差异作为说明而非筛选门禁。',
             'row_assessments 项形状为 {"raw_row_id":真实库行ID,"outcome":"LINKED","reason":"已有本行link"} 或 {"raw_row_id":真实库行ID,"outcome":"NOT_RELEVANT","reason":"无关联link的原因"}；outcome 只允许 LINKED / NOT_RELEVANT，不能使用 link.level 的值。',
             "返回 {links:[{requirement_id,raw_row_id,level,match_score,score_reason,compatibility:[{dimension,requirement_basis,metric_basis,relation,reason}],evidence_clause_ids,reason}],row_assessments:[{raw_row_id,outcome,reason}]}。每个库行必须恰好一个 row_assessment。"]
    if feedback:
        parts.extend(["# Previous invalid output feedback", feedback])
    return "\n".join(parts)


def destinations_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                        links, feedback: str | None = None) -> str:
    parts = ["# V2 final destinations", "# Requirement IR (JSON)", _json(ir.model_dump(exclude_none=True, exclude_defaults=True)),
             "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
             "# Complete raw metric catalogue (JSON)", _json(_rows(rows)),
             "# Validated screening links (JSON)", _json([
                 {**link.model_dump(exclude={"compatibility", "score_reason"}, exclude_none=True),
                  "differences": [{"dimension": item.dimension, "relation": item.relation,
                                   "reason": item.reason} for item in link.compatibility
                                  if item.relation in {"INSUFFICIENT", "CONFLICT"}]}
                 for link in links
             ]),
             "返回 {dispositions:[{requirement_id,reason,destinations:[{destination,raw_row_ids,evidence_clause_ids,aspect,reason}]}]}。",
             "逐项列出每个 Requirement 的独立时间窗口、阈值、测量对象和条件分支；一个维度有候选不代表其他维度已有去向。每个独立 aspect 应各有去向，或在同一去向中完整说明全部维度及差异。"]
    if feedback:
        parts.extend(["# Previous review feedback", feedback])
    return "\n".join(parts)


def critic_prompt(ir: RequirementIR, clauses: Sequence[DocumentClause], rows,
                  links, dispositions, feedback: str | None = None, row_assessments=()) -> str:
    parts = [
        "# V2 independent critic", "# Requirement IR (JSON)", _json(ir.model_dump(exclude_none=True, exclude_defaults=True)),
        "# Canonical evidence (JSON)", _json(_evidence(ir, clauses)),
        "# Complete raw metric catalogue (JSON)", _json(_rows(rows)),
        "# Validated mapping links (JSON)", _json([x.model_dump() for x in links]),
        "# Proposed destinations (JSON)", _json(dispositions.model_dump()),
        "# Required verdict targets (JSON)", _json(critic_targets(dispositions)),
        "# Full catalogue row assessments (JSON)", _json([x.model_dump() for x in row_assessments]),
        '返回 {verdicts:[{"target_id":"TGT-0001","verdict":"CONFIRM","reason":"独立核对结论","evidence_clause_ids":["真实原文ID"]}]}。Required verdict targets 中每个 target_id 恰好返回一次，不遗漏、不重复、不创造编号；无需返回 requirement_id、destination、raw_row_id、aspect，Python 按编号保留这些身份字段。PENDING_REVIEW 不在 verdict targets 内，遗漏的独立维度仍通过 missing_aspects 报告。',
        "另返回 recalled_links:[] 与 rejected_candidates:[]。recalled_links 使用与映射 links 相同形状，level 只能 REVIEW；rejected_candidates 项为 {requirement_id,raw_row_id,reason,evidence_clause_ids}，可引用已有 DIRECT/REVIEW。无遗漏/误报时返回空数组。",
        "另返回 score_adjustments:[]，项形状为 {requirement_id,raw_row_id,match_score,score_reason,evidence_clause_ids}；只调整已有且未排除的 DIRECT/REVIEW，分数为0–100的数字。recalled_links 也必须有 match_score 和 score_reason。",
        "另返回 missing_aspects:[]，逐条列出已抽取但 destinations 遗漏的独立维度，形状为 {requirement_id,aspect,reason,evidence_clause_ids}；引用真实 Requirement 自身证据，aspect 与该 Requirement 已有 destination 不重复。没有遗漏时返回空数组。",
    ]
    if feedback:
        parts.extend(["# Previous critic validation feedback", feedback])
    return "\n".join(parts)
