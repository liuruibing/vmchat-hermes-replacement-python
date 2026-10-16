from __future__ import annotations

import json
from typing import Sequence

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk_v2.concept_knowledge import SOURCES, metric_concept_reference
from app.mandate_risk_v2.mapping_models import CORE_COMPATIBILITY_DIMENSIONS, critic_targets
from app.mandate_risk_v2.models import RequirementIR

_CORE_DIMENSIONS_TEXT = ", ".join(CORE_COMPATIBILITY_DIMENSIONS)

MAPPING_SYSTEM_PROMPT = f"""你是 Mandate PDF 的风险指标识别员。识别与原文明示要求、目标或等价计算约束相对应的库指标，不是推荐所有有用的监控工具，也不是确认算法等价或合规通过。
只用 Requirement IR、逐字原文及给定原始库行，不创造指标、阈值或实际组合数值。concept_reference 是有版本的辅助概念解释，不是合同证据；以原始库算法为准，外部常见定义不能覆盖本库特殊口径。
完整浏览分配给你的每个库行，并以已抽取的原文要求为锚点判断。合同不必点名指标，允许同义测量概念和口径待确认的直接对应；算法为空、年化/事前差异不是自动排除理由。
要求不局限于数值上限：当正文的管理动作、调整规则或交易例外明确以某测量概念为操作对象时，属于实质使用，可关联该概念；不能仅因没有数值目标而排除。仅定义、背景分类、公式操作数或泛管理目标不构成独立指标要求。
原文明示主要/限定配置于某资产类别或市场时，可关联同一配置对象的占比概念；未给数值限额、分母或计算算法不等于完全没有该配置要求，未知部分保留为REVIEW，不能套用指标库mandate中的比例门槛。须区分发行人所在地、上市地、风险所在国和币种；单纯许可某工具不支持其他对象的比例指标。
不得以长期增长、主动管理、一般风险政策或共同关键词给整批常见风险指标找用途。指标库 mandate 只是分类线索，不是 PDF 证据。证券集中度不等于发行人集中度，绝对行业集中度不等于行业相对基准偏离，股息收益率不等于增长率、贡献率或基准股息率比值；第三方基金底层流动性条件不能套到整个组合。实质不同概念或仅可作辅助监控的一律 REJECTED，而不是 REVIEW。没有原文对应依据的下跌条件、风险调整模型、比率运算不得自行引入；但原文等价公式即使没有指标名称也可以关联。
level：DIRECT 是与 PDF 明示测量概念对应（不要求名称逐字一致）；REVIEW 只用于已确定是同一测量概念，但具体算法、分母口径、事前估计方法等尚缺信息的情况。已知对象/层级/分母/核心运算不同不能当作“待确认”。REJECTED 是不同概念、仅相关工具或缺少原文要求。资本增长或总回报目标可对应基金收益概念，超基准目标可对应超额收益，不能因此排除所有非数字目标或推导任意风险指标。DIRECT 不代表算法等价、合规通过或入库确认。
每个 DIRECT/REVIEW 必须返回 match_score（0–100 的数字）和 score_reason（具体评分理由）。这是模型评估的文档匹配程度，不是统计校准的正确概率、文本向量余弦相似度或用户认可率。
评分参考：文档概念明确且适用性充分支持可给高分，口径不明应说明不确定性。分数不能使不同概念或仅间接监控用途入选；不按指标名称、固定分数或凑数量评分，Python 不按分数阈值过滤。
compatibility 只解释实际影响匹配的维度，不要求填齐十二项。可参考：{_CORE_DIMENSIONS_TEXT}，也可增加合同特有维度；至少解释一个实质关联或差异。
每项写 requirement_basis、metric_basis、relation 和 reason；relation 只能是 EQUIVALENT、INSUFFICIENT、CONFLICT、NOT_APPLICABLE。算法缺失不能猜等价。同概念但口径未知用 INSUFFICIENT；对象、层级、范围、分母、单位或核心运算有确证 CONFLICT 时不得同时返回 DIRECT/REVIEW，须核对原文与库算法后 REJECTED。年化、事前/事后估计差异须写清，不将同一跟踪误差概念误作完全无关指标。
row_assessments.outcome 只能 LINKED 或 NOT_RELEVANT；本批有该行的任意 link 则 LINKED，否则 NOT_RELEVANT。DIRECT、REVIEW、REJECTED 只能用于 link.level。
每个 link 的 evidence_clause_ids 至少包含该 Requirement 自身 evidence.clause_ids 中的一项；定义、上下文和有 IR relation 的其他 Requirement 条款可补充主证据，不发明 clause_id。
只输出一个 JSON 对象。"""

DESTINATION_SYSTEM_PROMPT = """你是 Mandate 筛选结果覆盖审计员。
逐条说明每个 Requirement 的独立对象、时间窗口和条件分支。去向只能 MAIN_TABLE、PENDING_REVIEW、LIBRARY_GAP、NON_METRIC。
MAIN_TABLE 只引用 DIRECT link，表示原文明示测量概念有对应库指标，不代表算法确认或自动入库。REVIEW 放 PENDING_REVIEW，仅承接同概念的未确认口径；不同概念不能以候选进入，不能引用 REJECTED。
LIBRARY_GAP 表示当前库没有对应该独立测量要求的指标；相关监控工具不能掩盖缺口。仅算法缺失或可确认参数差异不自动构成缺口。NON_METRIC 用于交易禁令、工具白名单、配置、治理或流程规则；它们仍是必须保留和执行的原文要求，不等于不重要或已合规。一个方面有指标不能隐藏其他方面。
一个 Requirement 可有多个不同 aspect 去向；一个 aspect 有指标不能隐藏其他分支。引用原 Requirement 的 clause_id。只输出一个 JSON 对象。"""

CRITIC_SYSTEM_PROMPT = """你是独立 Mandate 指标筛选复核员。独立核对 Requirement、逐字合同、完整原始指标库、关联解释、评分和去向。
逐条核对原文要求是否都有明确去向，不能只评价入选指标。名称或可确认参数差异不是删除理由，但不得混淆测量对象、资产范围、分母和条件分支。一般长期增长、主动管理和风险政策不足以支持任意风险指标；对只增加通用监控用途而没有具体原文目标的关联应排除。
实质使用也包括正文明确以某测量概念为对象的管理调整或交易条件，不必另有数值门槛。不要把这类操作性条款误判成“仅定义/顺带提及”；也不要把公式中的每个参数各自升级成独立指标要求。
特别检查是否仅因没有数值门槛而漏掉明确配置范围对应的占比概念；同配置对象可待确认算法，但不能混同发行地、上市地、币种或把目录备注门槛写入合同。
重新浏览完整库及 NOT_RELEVANT 理由，确有原文对应概念但漏掉的指标用 recalled_links 返回，level=REVIEW，并提供 match_score、score_reason、真实 Requirement/库行/原文 ID 和实质兼容维度；说明同概念依据及待确认口径。不得仅为有用的监控工具补召回，不凑数量。
用 rejected_candidates 排除缺少原文支持或测量概念被错误替换的已有 DIRECT/REVIEW。逐项比较双方定义，不能把不确定参数误判为不同概念，也不能把不同对象降格成待确认。concept_reference 仅帮助理解原始库算法，不能充当 PDF 原文依据。
对 Required verdict targets 每项恰好返回一次结论，包括全部 MAIN_TABLE、PENDING_REVIEW 和未被去向引用的关联。CONFIRM=原文支持同一概念；CHALLENGE=不支持关联或实质不同概念，该指标关联将被排除；UNRESOLVED=同概念但实现口径仍待确认，将保留为候选。LIBRARY_GAP/NON_METRIC 也要复核是否遗漏真实测量要求。不得改写目标身份，批评及双方具体证据写入 reason。
对所有已有 DIRECT/REVIEW 的 match_score 独立复核。需要修正的分数返回 score_adjustments，字段为 requirement_id、raw_row_id、match_score、score_reason、evidence_clause_ids；不调整则省略或返回空数组。不得按链接类型固定打分或把匹配分说成正确概率。
把原文、conditions、约束及独立测量维度与全部 destinations 对照，包括 PENDING_REVIEW。遗漏的时间窗口、阈值、对象或条件分支用 missing_aspects 显式保留，不能以一个分支代替全部。不要创造 Requirement 或库指标。
只输出一个 JSON 对象。"""


def _json(value) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _rows(rows: Sequence[RawRiskMetric]):
    return [{"row_id": row.row_id, "name": row.metric_name, "algorithm": row.algorithm,
             "mandate": row.mandate, "strategy_type": row.strategy_type,
             "concept_reference": metric_concept_reference(row)} for row in rows]


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
             "# Concept reference provenance (not PDF evidence)", _json(SOURCES),
             "# Optional compatibility reference dimensions", _json(list(CORE_COMPATIBILITY_DIMENSIONS)),
             'compatibility 项 JSON 形状必须为 {"dimension":"measurement_object","requirement_basis":"合同原文支持的口径","metric_basis":"库算法支持的口径","relation":"EQUIVALENT","reason":"双方依据"}；relation 只能取 EQUIVALENT / INSUFFICIENT / CONFLICT / NOT_APPLICABLE。不要求填齐十二项；区分同概念未知口径与已知不同概念，不能用REVIEW掩盖CONFLICT。',
             'row_assessments 项形状为 {"raw_row_id":真实库行ID,"outcome":"LINKED","reason":"已有本行link"} 或 {"raw_row_id":真实库行ID,"outcome":"NOT_RELEVANT","reason":"无关联link的原因"}；outcome 只允许 LINKED / NOT_RELEVANT，不能使用 link.level 的值。',
             "返回 {links:[{requirement_id,raw_row_id,level,match_score,score_reason,compatibility:[{dimension,requirement_basis,metric_basis,relation,reason}],evidence_clause_ids,reason}],row_assessments:[{raw_row_id,outcome,reason}]}。每个库行必须恰好一个 row_assessment。"]
    parts.append("身份与证据检查：对每个 link，先按 requirement_id 找到 IR 中的对应 Requirement，复制它自身 evidence.clause_ids 作为主证据；不要因指标名称或合同条款相似而交换 Requirement 编号。补充证据仅限定义、上下文或该 Requirement 的 IR relation 所关联的条款。输出前逐项核对。")
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
        "# Concept reference provenance (not PDF evidence)", _json(SOURCES),
        "# Validated mapping links (JSON)", _json([x.model_dump() for x in links]),
        "# Proposed destinations (JSON)", _json(dispositions.model_dump()),
        "# Required verdict targets (JSON)", _json(critic_targets(dispositions, links)),
        "# Full catalogue row assessments (JSON)", _json([x.model_dump() for x in row_assessments]),
        '返回 {verdicts:[{"target_id":"TGT-0001","verdict":"CONFIRM","reason":"逐项比较合同与库算法的独立结论","evidence_clause_ids":["真实原文ID"]}]}。每个 target_id 恰好返回一次，不遗漏、不重复、不创造编号；无需返回 requirement_id、destination、raw_row_id、aspect，Python 按编号保留身份。PENDING_REVIEW 及未被去向引用的关联也必须回答；CHALLENGE 的关联将排除，UNRESOLVED 只保留同概念口径待确认者。遗漏独立维度通过 missing_aspects 报告。',
        "另返回 recalled_links:[] 与 rejected_candidates:[]。recalled_links 使用与映射 links 相同形状，level 只能 REVIEW；rejected_candidates 项为 {requirement_id,raw_row_id,reason,evidence_clause_ids}，可引用已有 DIRECT/REVIEW。无遗漏/误报时返回空数组。",
        "另返回 score_adjustments:[]，项形状为 {requirement_id,raw_row_id,match_score,score_reason,evidence_clause_ids}；只调整已有且未排除的 DIRECT/REVIEW，分数为0–100的数字。recalled_links 也必须有 match_score 和 score_reason。",
        "另返回 missing_aspects:[]，逐条列出已抽取但 destinations 遗漏的独立维度，形状为 {requirement_id,aspect,reason,evidence_clause_ids}；引用真实 Requirement 自身证据，aspect 与该 Requirement 已有 destination 不重复。没有遗漏时返回空数组。",
    ]
    if feedback:
        parts.extend(["# Previous critic validation feedback", feedback])
    return "\n".join(parts)
