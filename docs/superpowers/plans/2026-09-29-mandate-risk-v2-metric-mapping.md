# Mandate Risk V2 Phase B Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking. The default is single-agent execution because the stages share one evidence contract; request an independent review only for the final high-risk matching gate.

**Goal:** 在 V2 Requirement IR 通过合同覆盖审计后，对只读风险指标库逐项做语义与算法口径匹配，输出用户确认的六列主表，并明确展示待确认及指标库缺口。

**Architecture:** 保留 Phase A 的 PDF → canonical clauses → Requirement IR，不让指标库反向影响合同理解。Phase B 对完整原始指标库分批建立带逐维 Compatibility Matrix 的候选映射及完整 Requirement destinations，再由独立 Critic 审查全部 DIRECT 与 LIBRARY_GAP。Python 只校验身份、引用、结构、覆盖与状态一致性，不凭关键词或规则替模型做业务语义判断；双阶段审计未闭合不发布正式报告。

**Tech Stack:** Python 3、FastAPI、Pydantic、现有 ModelSkillRunInput/DeepSeek Provider、pytest；前端仅在后端验收后联调静态测试页。

---

## 0. 范围、基线与不能妥协的输出契约

- 规划基线：后端分支 optimize/mandate-risk-generic-recall，检查时 HEAD 为 0d0ff29；实施前重新核对 HEAD 和工作区。当前 V2 Agent mandate-risk-v2-lab 仅输出 Requirement IR，生产 V1 不替换。
- 指标事实源：agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv，由 RawRiskMetricRegistry 只读加载；原始名称、算法、Mandate 字段及适用策略不能由模型改写。目录新增行不得要求修改 Python 指标名规则。
- 主表固定为「分组｜名称｜Mandate解读｜值｜参考组合｜相似度」。名称取原始库行；Mandate解读取 canonical clause 的逐字原文，完整引文、页码及来源跨度在详情保留。当前缺少组合持仓和参考组合数据，后三列一律显示「—」，绝不把模型置信度当相似度、把合同限额当组合实际值。
- 主表仅放有合同直接依据、测量对象/分母/时点/前瞻或年化等限定词与库算法口径一致的指标。相关但口径不足或冲突者进入「待确认」；合同有明确要求而库无等价指标者进入「指标库缺口」。定义、背景、一般许可和治理事项不能为了凑表变成正式指标。
- 分组先兼容已有 key/core/Indicator 分类；把当前已知指标的展示分组放在独立展示配置中。未被配置覆盖的新指标显示「待分类」，不得默认为 Indicator；分组不参与匹配决策。
- 不把用户示意表的 AA/BB 组合、99% 等值或 VaR、Beta、Sortino 行写入业务结果。年化事前 Tracking Error 与现有 TE=σ(Rp−Rb) 未证明等价时列待确认。
- 运行代码不能按 PDF 文件名、固定 clause_id、固定库行号、预期主表条数或示例英文句子作判断。样例预期只允许出现在验收数据/测试中。

## 1. 文件职责与阶段边界

| 文件 | 职责 |
| --- | --- |
| app/mandate_risk_v2/coverage.py | 修正 Phase A 引用校验；不承担指标判断 |
| app/mandate_risk_v2/mapping_models.py（新） | 模型提案、逐 Requirement 去向、映射结果的严格类型 |
| app/mandate_risk_v2/mapping_prompts.py（新） | 使用 Requirement IR、canonical 原文和库行构造分批映射/复核提示 |
| app/mandate_risk_v2/mapping_validator.py（新） | 校验 requirement_id、raw_row_id、证据 clause_id、目录批次与去向完整性 |
| app/mandate_risk_v2/mapping.py（新） | 全目录分批比较、合并候选、口径复核、用量统计和 fail-closed |
| app/mandate_risk_v2/critic.py（新） | 独立复核所有 DIRECT 和 LIBRARY_GAP，提出异议并触发修订或未决 |
| app/mandate_risk_v2/report.py（新） | 把验证后的 V2 结果转换为报告结构；不决定哪些指标可以 DIRECT |
| app/mandate_risk/renderer.py | 复用六列渲染，新增可注入的展示分组映射；保持 V1 默认行为 |
| agents/mandate_risk_v2_lab/metric-display-groups.json（新） | 只保存当前已知指标的展示分组，不修改原始 CSV |
| app/workflow/graphs/mandate_risk_v2.py | Phase A 成功后执行 Phase B；只在双门禁通过时发 run.completed |
| tests/test_mandate_risk_v2_mapping_*.py（新） | 身份、证据、口径、漏行、报告及工作流定向测试 |
| docs/mandate-risk-v2-acceptance.md（新） | 两份真实 PDF 的人工复核矩阵、终态与未决项 |
| 前端 static/test-mandate-risk.html | 最后阶段只调整 V2 结果说明与状态展示，不作为后端验收前置条件 |

V2 的可测试接口以这些字段为核心；实现可以加内部字段，但不能删掉身份和去向：

~~~python
class MappingLink(StrictModel):
    requirement_id: str
    raw_row_id: int
    level: Literal["DIRECT", "REVIEW", "REJECTED"]
    compatibility: list[CompatibilityDimension]
    evidence_clause_ids: list[str]
    reason: str

class RequirementDisposition(StrictModel):
    requirement_id: str
    destinations: list[RequirementDestination]
    reason: str

class RequirementDestination(StrictModel):
    destination: Literal["MAIN_TABLE", "PENDING_REVIEW", "LIBRARY_GAP", "NON_METRIC"]
    raw_row_ids: list[int]
    evidence_clause_ids: list[str]
    aspect: str
    reason: str

class CompatibilityDimension(StrictModel):
    dimension: str
    requirement_basis: str
    metric_basis: str
    relation: Literal["EQUIVALENT", "INSUFFICIENT", "CONFLICT", "NOT_APPLICABLE"]
    reason: str

class MetricRowAssessment(StrictModel):
    raw_row_id: int
    outcome: Literal["LINKED", "NOT_RELEVANT"]
    reason: str

class MappingBatch(StrictModel):
    links: list[MappingLink]
    row_assessments: list[MetricRowAssessment]

class FinalMappingReview(StrictModel):
    dispositions: list[RequirementDisposition]

class CriticVerdict(StrictModel):
    requirement_id: str
    destination: Literal["MAIN_TABLE", "LIBRARY_GAP"]
    raw_row_id: int | None
    verdict: Literal["CONFIRM", "CHALLENGE", "UNRESOLVED"]
    reason: str
    evidence_clause_ids: list[str]
~~~

分批模型输出只产生候选 links 和本批每个库行的审计处置；全库审计完成后才汇总最终 dispositions。每个 Requirement 必须有完整 destinations；多个条件分支/可分割 aspect 可分别去主表、待确认或缺口，不能以一个 MAPPED 掩盖剩余部分。一个 Requirement 可关联多个库行，一库行也可由多个 Requirement 支持。Critic 独立审查全部 MAIN_TABLE 与 LIBRARY_GAP；异议须修订并复核，或明确落待确认/未决。无法闭合时 fail-closed。

Python 只执行可机械核查的事实：ID 存在、证据 clause 属于该 Requirement、库行真实、批次与列表完整、destinations 与 links 一致、Critic 覆盖所有需审项。测量对象、分母、时点、策略适用、算法等价、是否真正存在库缺口均由模型及 Critic 判断；Python 不以指标名称、正则或样例规则作业务裁决。Matrix 中的维度可扩展，但合同显式限定词必须逐项说明；依据缺失由模型标 INSUFFICIENT，不能静默等价。

## 2. 实施任务

### Task 1：锁定 Phase A 合同覆盖门禁

**Files:** Modify: app/mandate_risk_v2/coverage.py；Test: tests/test_mandate_risk_v2_requirement_ir.py、tests/test_mandate_risk_v2_coverage_validation_repair.py；Create: docs/mandate-risk-v2-acceptance.md。

- [ ] 先运行现有 V2 定向测试，记录 HEAD、测试命令和结果；仅检查本次涉及路径。
- [ ] 写红测：一个 hinted clause 的 COVERED assessment 同时引用正确 Requirement 和另一条不引用该 clause 的 Requirement，必须拒绝；目前校验使用 any，会错误通过。另测空引用、未知引用和正常单一引用。
- [ ] 把 COVERED/PARTIAL 的引用校验改为「列表中每个 Requirement 均直接引用该 clause」，保留模型复核重试；运行上述测试验证由红转绿。
- [ ] 先定位并复用已有 Gold 版本（仓库内目前仅找到 Phase A 验收原则，未找到独立 Gold 文件）；核对其与当前 parser 原文和两份 PDF 的版本/哈希，增补缺失的原文短句、页码、对象、条件、阈值，不重建重复预期。至少覆盖固收新购收益率 +10 bps；权益 Single Name、Sector、事前年化 TE、TPMF 两档、底层分散度、1/7 日流动性和单只 MMF 上限。定义与一般许可列负例。
- [ ] 用本地 DeepSeek 分别跑两份 PDF Phase A，对照 Gold；P0 要求与两档限制漏一档时不得进入 Phase B。先记录真实差异，再只修 Phase A 的通用问题；若门禁未过，停止本阶段交付。

Run:

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mandate_risk_v2_requirement_ir.py tests/test_mandate_risk_v2_coverage_validation_repair.py
~~~

Expected: 新红测先失败，修复后本组全部通过；真实样例的 P0 Requirements 均有原文依据和独立去向。

### Task 2：定义 Phase B 的严格输入输出与确定性校验

**Files:** Create: app/mandate_risk_v2/mapping_models.py、app/mandate_risk_v2/mapping_validator.py、tests/test_mandate_risk_v2_mapping_validator.py。

- [ ] 写红测覆盖：虚构 requirement_id/库行号/条款 ID、引用非本 Requirement 的 clause、跨批次库行、重复 link、遗漏最终 destination、MAIN_TABLE 却无 DIRECT link、DIRECT Matrix 有 INSUFFICIENT/CONFLICT、空算法仍被宣称有算法依据、缺少本批任一库行的 row_assessment；同一 Requirement 多个 aspect 有不同 destinations。
- [ ] 实现严格模型契约和 validate_mapping_batch / validate_final_dispositions。模型只输出 ID 与判断，不提供可直接展示的证据文字；Python 从 Phase A clauses 重建原文与页码。
- [ ] DIRECT 的可校验必要条件是真实库行、真实 Requirement、真实 clause 证据和完整 Matrix；若模型标出 INSUFFICIENT/CONFLICT，不能同时标 DIRECT。Python 不自行判定空算法、策略或限定词是否等价；缺失依据必须交给模型与 Critic 判断，未决则不发布 DIRECT。
- [ ] 允许一条 Requirement 对应多条候选 link，但每个候选逐一审；全库阶段结束前不得将「某批没有匹配」写为库缺口。

接口：validate_mapping_batch 接收模型 JSON、RequirementIR、canonical clauses、registry 与本批 row_id 集合，返回 MappingBatch；validate_final_dispositions 接收完整目录阶段的 links 和模型最终审计 JSON，返回逐 Requirement 的 RequirementDisposition 列表。单测使用合成库行而非两份样例的固定名称。

Run:

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mandate_risk_v2_mapping_validator.py
~~~

Expected: 非法身份/证据/去向全部拒绝，合法多对多链接通过。

### Task 3：对完整指标目录做分批语义映射

**Files:** Create: app/mandate_risk_v2/mapping_prompts.py、app/mandate_risk_v2/mapping.py、tests/test_mandate_risk_v2_mapping_pipeline.py；Read-only source: app/mandate_risk/registry.py、agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv。

- [ ] 写红测：两个名称任意的合成指标中，第二个没有进入词典/别名也能因 IR 语义被全目录审计到；新增库行不需改 Python 名称表；不适用策略的行不进 DIRECT；策略不明时仍检查全库。
- [ ] 从配置的只读源加载 RawRiskMetricRegistry；不按策略预先丢弃库行，而是对完整目录分批审计。提示只给 Requirement 结构、其 canonical 原文、原始库行的名称/算法/Mandate/策略；不再把整个 PDF 作为指标匹配输入。策略不符的候选可以列待确认，但不能仅凭语义相似进入 DIRECT。
- [ ] 每批明确返回该批每个库行的处置（相关链接或可说明的不匹配），Python 校验所有预期 row_id 均被处置后再汇总。模型超时、JSON 不合法或漏掉库行时有界重试；仍无法闭合则失败，不静默返回半张表。
- [ ] 对候选逐维建立 Compatibility Matrix：measurement object、scope、denominator、time point、annualisation、ex-ante/ex-post、benchmark、conditions，以及合同新增的开放限定词。模型给出双方依据与关系，不能只返回一个总分。
- [ ] 汇总所有 Requirement 的完整 destinations；独立 Critic 重新看 IR、canonical 原文与完整库，对每个 DIRECT 和 LIBRARY_GAP 出具 verdict，特别核实 GAP 是否遗漏可用指标。异议修订后再审，有界重试仍不一致则待确认/未决，不把它们伪装成已确认结论。把各次模型用量与未决原因计入结果。

Run:

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mandate_risk_v2_mapping_pipeline.py
~~~

Expected: 合成新指标可被召回，漏库行与漏 Requirement 均 fail-closed，口径不明留 REVIEW。

### Task 4：六列表格与展示分组

**Files:** Create: app/mandate_risk_v2/report.py、agents/mandate_risk_v2_lab/metric-display-groups.json、tests/test_mandate_risk_v2_report.py；Modify: app/mandate_risk/renderer.py（只作兼容性扩展）。

- [ ] 写红测：主表列名和顺序固定；仅 DIRECT 行出现；名称必须来自 registry；Mandate解读必须等于 canonical clause 文本，不允许模型改写；多 clause 的完整原文在详情分开展示并带页码；后三列为「—」；Markdown 竖线正确转义。
- [ ] 从现有 key/core/Indicator 规则生成一次性的已知指标展示配置，手工核对每条当前库行恰好归类；新库行不存在于配置时标「待分类」。展示分类不得影响是否匹配。
- [ ] 将已验证 MappingLink 转为报告使用的 MetricMatch/EvidenceQuote，并复用现有 renderer 的六列结构；保留独立的「待确认」「指标库缺口」「非指标性合同要求去向」明细。V1 的默认输出不变。
- [ ] 若 DIRECT 证据跨页，原文分别引用各页，不拼出 PDF 中不存在的句子。合同约束阈值可以在详情解释，但不能写进代表组合实际数值的「值」列。

Run:

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mandate_risk_v2_report.py tests/test_mandate_risk_renderer_table.py
~~~

Expected: 六列与原文证据正确，新增库行显示「待分类」，V1 renderer 原测试不回归。

### Task 5：接入 V2 workflow、终态与用量

**Files:** Modify: app/workflow/graphs/mandate_risk_v2.py、agents/mandate_risk_v2_lab/agent.json、agents/mandate_risk_v2_lab/roles/requirement-analyst.json；Test: tests/test_mandate_risk_v2_workflow.py、tests/test_mandate_risk_v2_registration.py。

- [ ] 写红测：Phase A 不完整时不调用指标库；Phase B 成功输出主表并 run.completed；算法口径不足但已明确分类为 REVIEW 时仍 run.completed 且不进主表；库缺失、审计漏行、非法引用或未能分类时 run.failed；V1 Agent 与 workflow 注册保持不变。
- [ ] 在 Phase A 成功之后加载 registry 并调用 MappingPipeline；将 Phase A 与 Phase B 的 usage 分阶段汇总，缺少某次用量时标 complete=false，不伪造总 token 数。
- [ ] 报告顶部明确标识 V2、指标库快照来源和审计状态。失败时不要先流出正式主表再发 run.failed；最终可展示结果只在两个阶段完成后生成。
- [ ] 更新实验 Agent 的描述，删除「本阶段不得读取指标库」这类已不准确的配置描述；保留 v1 独立入口。

Run:

~~~bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider tests/test_mandate_risk_v2_workflow.py tests/test_mandate_risk_v2_registration.py
~~~

Expected: 成功、失败及未决的事件终态与报告一致；生产 V1 路径未被替换。

### Task 6：真实 PDF 验收后再联调静态页

**Files:** Create/Update: docs/mandate-risk-v2-acceptance.md、scripts/mandate_risk_v2_remote_e2e.py；Modify only if needed: 前端仓库 static/test-mandate-risk.html。

- [ ] 用当前分支新进程启动本地后端，上传固收和权益两份 PDF，通过 POST /v1/runs 与 SSE 获取结果；记录代码 SHA、模型、run_id、文档 hash、终态、用量、时延和报告。首次真实运行各一轮；若结果波动或缺口未明，再有针对性重复，不默认压测。
- [ ] 增加独立远程 E2E runner：通过显式传入的 base URL/模型/两份 PDF 上传、创建 V2 run、读取 SSE 到终态，并按已复用的 Gold 核对原文与去向；输出版本、文档哈希、run ID、用量与差异。不把过期 Cloudflare URL 写死，也不改远程部署状态。
- [ ] 按 Gold Matrix 核对每条 P0 Requirement 的抽取、证据、库匹配去向；重点验证新购收益率不是组合超额收益率、TPMF 两档不被合并、单券/行业的对象与分母、事前年化 TE 进入待确认、底层流动性要求不冒充组合自身流动性指标。
- [ ] 用与样例不同的合成 PDF/指标库行做成功和拒绝测试：新指标无需改别名、同一 clause 多阈值、定义数字负例、库算法缺失/冲突、跨页证据、新库行待分类。
- [ ] 仅在后端报告通过验收后，更新静态页的 V2 阶段说明，浏览器验证 PDF 上传、SSE、run.completed、run.failed 和无数据时「—」显示；不改 Vue 业务页或 ddrisk-ui。
- [ ] 运行受影响的定向测试、git diff --check；记录仍需业务确认的库算法和展示分组，不把待确认包装成通过。前后端改动分仓库核对，按用户当时的提交要求分别处理。

接口验收用的最小断言：

~~~text
成功：run.completed；六列主表只含已验证 DIRECT；每行库行存在且引文逐字属于 PDF。
未决：待确认或库缺口有真实 Requirement 与原文；必要门禁不完整则 run.failed。
通用性：新增 PDF/新增指标通过同一流程，不依赖样例文件名、固定 ID 或固定主表数量。
~~~

## 3. 审阅时需要特别确认的取舍

1. 库算法为空、或缺少合同要求的前瞻/年化/分母等限定词时，本计划默认不能进主表，先列「待确认」。这会使某些示例表里的行暂时缺席，但避免把概念相关误报为算法等价。
2. 完整库审计与 DIRECT 二次口径复核会增加模型调用和成本。先测两份 PDF 的 token/时延，再决定是否做不影响召回的缓存或批大小优化；不以截断目录换速度。
3. Gold Matrix 是测试/人工验收资料，不是运行时规则；业务方可修订预期，但修订必须基于 PDF 原文和原始指标算法。

本计划写给审阅，尚未授权实施、提交或推送。确认口径后才开始 Task 1。
