# V2 指标筛选口径与验证记录（2026-09-30）

## 金融概念准入与可追溯评测（当前实现）

本节覆盖历史记录中“不同概念但有监控用途也可 REVIEW”的口径。原文上半区、下方六列表格、Excel及前端代码不变；不部署外部项目、向量库或新模型。

### 概念知识与准入

- `app/mandate_risk_v2/concept_knowledge.py` 提供34行目录的辅助定义、经区分的英文名称及近邻概念边界。定义由本方目录算法推导，不是业务专家已审核的金融标准。参考 FIBO 的定义、区分特征与来源建模方法；QuantStats、PyPortfolioOpt 链接用于核对实现口径，不能覆盖本方算法。未复制外部训练集，也未把模型生成问答当作权威定义。
- 参考绑定目录 SHA-256 `4163180c3f3cc921e23fe7d553ccf7975ca6231430a86cefcf7ef2180481a261`、行号、名称和算法。目录源版本或行身份改变后返回无参考，不把旧解释应用到新指标；维护目录后须重新审核注释并重启进程。缺失算法、评级因子等信息保持未知。
- Copilot/detailed 中，`DIRECT` 表示原文对应同一测量概念；`REVIEW` 只承接同概念的口径不确定，不再承接不同概念的辅助监控工具。对象、层级、范围、分母、单位和核心运算被模型同时标为已知 `CONFLICT` 的保留关联，属于不一致输出：要求模型按原文/算法重新核对，不能作为高分候选直接放行。未知参数使用 `INSUFFICIENT`；事前/事后、年化等差异不会机械排除整个跟踪误差概念。
- 不要求名称逐字相同、每项都有数字限额或算法完全等价。资本增长/总回报可对应收益概念；同对象的明确配置范围可对应配置占比，但不补造目录备注门槛。正文管理调整或交易条件对某测量概念的实质使用也可关联；仅定义、公式操作数、背景分类不能各自变成独立指标。
- 证券不等于发行人；绝对行业敞口不等于减基准权重；股息收益率不等于贡献、增长或基准股息率比值；第三方基金底层条件不等于本组合流动性；购入时债券收益率利差不等于持有期超额收益或对国债信用利差。
- 独立 `screening` 路径也使用相同概念参考和非逐字识别原则，但仍只有 `DIRECT` 入表，仍为 `coverage_status=not_audited`，没有新增独立Critic调用。不能用快速模式验证代替Copilot详细链路验证。

### 候选复核

- `critic_targets()` 覆盖每个去向，包括 `PENDING_REVIEW`；没有被去向引用的保留关联也建立目标。不能通过不分配去向绕过复核；多行去向逐行核对。
- `CONFIRM` 确认概念关联；`CHALLENGE` 表示原文不支持或实质不同概念，该关联进入排除集合；`UNRESOLVED` 表示同概念实现口径未定，保留候选而非确认算法等价。非指标规则、库缺口及未覆盖条件仍保留后端去向。
- 证据ID继续严格校验，不自动补零或猜测条款。提取提示明确提供允许ID列表并要求保留前导零；校验不通过仍失败，不把分析失败包装为准确率提升。

### 评测及复现

- `tests/fixtures/mandate_recognition_equity.json`：权益PDF全部34行初标，5项同概念可关联、28项不应关联、1项区域分布待业务裁定；每项保存理由、原算法、页码及原文锚点。PDF SHA-256为 `3aaf3f50e4015129d6d388425fe6b6503eed5e7391b0ef6d20950afd30c117d6`。这是 assistant 初标开发基线，不是独立专家金标准，不是盲测或跨文档准确率结论。
- `scripts/evaluate_mandate_recognition.py` 按文档—指标去重，分别报告 DIRECT、REVIEW及二者合并的TP/FP/FN、Precision/Recall/F1；歧义项单列，未知行或变化后的算法拒绝评分。主指标是合并结果，不能靠把误报挪到REVIEW获得虚假改善。重复输入报告选集Jaccard及差集。
- 提供 `--pdf` 时核对基线PDF哈希，并检查引文页码、原文及初标锚点；没有PDF或缺证据不能记作已验证。原文出处正确不代表语义蕴含、所有数值与条件都正确，这些仍需业务复核。
- `tests/fixtures/mandate_recognition_contrasts.json` 为13组模型真实调用对照：无名称公式、同义改写、证券/发行人、绝对/相对行业、基金底层/组合、股息比率、Alpha操作数、无数值门槛的管理动作等。它们是合成开发样例，不注入生产Prompt，不代表完整PDF业务准确率。

```bash
# 真实模型概念对照；需要已有OMP认证，不包含在常规pytest中
OMP_TEST_MODEL=google-antigravity/gemini-3.8-flash \
  uv run python scripts/check_mandate_recognition_contrasts.py \
  --report-dir .runtime/v2-validation/concept-recognition/contrasts

# 对已保存的真实结果评分；多个 --result 可检查重复运行稳定性
uv run python scripts/evaluate_mandate_recognition.py \
  --result /path/to/run-result.json \
  --gold tests/fixtures/mandate_recognition_equity.json \
  --pdf '/Users/liuruibing/Downloads/sample(1)/权益sample.pdf' \
  --output .runtime/v2-validation/recognition-evaluation.json

uv run pytest -q
```

### 已观察的验证证据

- 全后端回归402项通过；保留既有Starlette/httpx弃用警告和一条Pydantic夹具序列化警告。新增测试检查概念冲突、未知参数、候选逐项复核、挑战排除、去重评分、歧义项及证据缺失；删除两条只锁定Prompt字面的旧测试。
- 首轮12组真实模型对照全部符合初标；最终规则的13组对照也全部通过，包括后来加入的无数字限额管理动作。真实调用模型为Gemini 3.8 Flash；最终逐例结构化结果和调用用量在 `.runtime/v2-validation/concept-recognition/contrasts-final/summary.json`，原始模型输出在 `.runtime/concept-recognition-contrast-final-omp/`。这些是合成语义对照，不冒充完整PDF准确率。
- 异类固收PDF首轮快速识别误将“Duration adjustment”当成仅提及，漏选久期。明确实质操作使用无需数值限额后，`run-131483d2-ccd8-4996-a5fb-240aee0edeb0` 完成，选择久期并引用第3页定义和第4页操作条款；购入时10bps相对基准收益率目标未错配为组合超额收益或对国债信用利差。证据在 `.runtime/v2-validation/concept-recognition/fixed-income-final/`。该PDF已经用于发现和修正问题，不能继续称为独立盲测。
- 最终规则的权益完整Copilot运行 `run-608f38aa-5afb-4e38-b19f-c7d21f5f0f50` 返回 `run.completed`，耗时264.316秒；关联基金收益率、基准超额收益、跟踪误差、单一证券占比、境内资产占比，其中境内资产占比为同概念口径待确认。下行Beta、Alpha、信息比率、其他股息比率、相对行业偏离及基金底层/组合流动性误配均未入表。没有按文档名、固定条款或目标数量设置运行规则。
- 同一34行初标下，历史报告为TP=4、FP=10、FN=1（另有1项区域分布歧义），上述最终报告为TP=5、FP=0、FN=0。明细在 `.runtime/v2-validation/concept-recognition/final/evaluation.json`；这是单文档初标对照，不能宣称业务准确率100%。
- 最终规则的第二次重复运行 `run-8aed8c4c-5000-464c-b225-da2a7c03ea14` 在映射阶段遇到上游OMP/Gemini `unknown certificate verification error` 而失败，不能计为通过或空选集。未关闭TLS校验、未增加自动重试、未用其他模型冒充同模型稳定性。原始模型错误在 `.runtime/concept-recognition-final-omp/06fceb288b694533a60852e589da2039.json`。
- 本轮为后端/模型验证，没有重新做浏览器E2E，不沿用下方历史截图宣称当前页面已验收。历史已保存报告不会自动改写；只有加载新代码的后端重新分析才应用新规则。

## 2026-10-15：Copilot 改为原文要求驱动（当前入口）

- 本节覆盖下述“默认快速筛选”对 `mandate-risk-copilot` 的描述。Copilot 固定复用 detailed 流程：原文要求提取 → 覆盖复核 → 完整指标库关联/去向分配 → 独立复核；策略原文分支独立并行。独立 `mandate-risk-analysis-v2` 的显式 screening 能力未删除。
- 先识别真实章节内的实质义务，再判断可否映射；标题不是天然数值指标，一个标题可包含多个禁令或条件分支。保留规则/非指标要求、文档配置、待确认和指标库缺口，不用指标数量代替要求覆盖。DIRECT 允许同义概念而非名称完全一致；REVIEW 必须锚定具体要求，不能仅凭长期增长、主动管理、一般风险监控或指标库 Mandate 分类引入下行Beta等指标。
- 原文标题通过 `attributes.source_heading` 保存，并验证其来自引用条款；条件、例外和复合下限/上限公式继续使用既有 Requirement IR。这些结构用于后端指标识别，不新增前端区域；中间区域保持既定上半部分委托原文及下半部分指标表，Excel保持原格式，不追加要求或配置清单。
- 真实模型/HTTP-SSE 初验：使用用户的 `/Users/liuruibing/Downloads/sample(1)/权益sample.pdf`，运行 `run-5865d644-5bfa-4cbf-8fee-a334ba131620` 完成，耗时 307.08 秒。本次得到 27 项原文要求、13 个去重关联指标（3 个直接关联、11 个候选，其中 1 个跨要求同时有两类关联）、7 个库缺口、15 项规则/非指标去向及 6 项配置事实。下行Beta 未进入关联指标。数量是本次模型结果，不是硬编码标准或人工准确率结论。
- 已核对 9.1–9.12 均有原文证据；9.10 保留建仓期、低于/达到十亿元分支、`lower of` 一亿元和100%的复合上限、分散度及1天/7天流动性全部条件，未把这些前置条件变成组合通用指标。证据 `/tmp/mandate-requirements-smoke-result.json`、`/tmp/mandate-requirements-smoke.sse`。
- 定向回归：`uv run pytest -q tests/test_mandate_risk_copilot.py tests/test_mandate_risk_v2_*.py`，157 passed；一条既有 Pydantic 夹具序列化警告。前端模块回归及修改组件 ESLint 通过。提取/覆盖/独立复核增加真实模型调用及耗时；不承诺固定调用次数或完整业务准确率。
- 界面范围已纠正：撤回新增的“原文要求与处置”组件及附加导出，保留后端识别改进。当前界面回归基于浏览器已有真实完成报告，未重新调用模型；原文区、15行指标表、PDF依据定位和原格式Excel均可用。截图 `/tmp/mandate-original-layout-restored.png`，日志 `/tmp/mandate-original-layout-restored-log.json`。以下页面要求筛选操作为撤回前的历史验证，不代表当前界面。
- 实际页面 E2E PASS：本地服务已重启为 PID 26620，通过 `http://127.0.0.1:9528/#/mandate-risk-v2/index` 上传同一用户 PDF 并发送分析。首次运行 `run-377f94ce-4278-4889-a2bd-0cfe58a39764` 发生客户端连接中断；点击重新分析后，`run-cffb43da-a443-42fb-ba5e-f48252c90191` 返回完成（后端 358.276 秒）。终态和 DOM 均为 27 项要求、15 个去重库指标，3 个直接关联、13 个待确认候选（跟踪误差跨要求同时有两类关联），下行Beta未关联。候选集合存在模型波动，不能宣称数量固定或全部可用。
- 页面交互断言：规则去向筛选保留 15 项；借款禁令可展开并定位 PDF 第5页，观察到31个高亮矩形；按 `9.10` 和库缺口筛选得到4项，保留两档规模条件、`lower of` 公式、分散度及1天/7天流动性。过滤状态下点击实际 Excel 导出，下载的有效工作簿仍包含27项要求、借款禁令、4项第三方基金分支及CNY配置。
- 最终运行创建与 SSE 均为 HTTP 200，完成事件已从实际代理回放核对。console error / pageerror 为0；有既有重复命名路由警告。证据：`/tmp/mandate-requirements-e2e-result.json`、`/tmp/mandate-requirements-e2e.sse`、`/tmp/mandate-requirements-e2e-log.json`、`/tmp/mandate-requirements-e2e-overview.png`、`/tmp/mandate-requirements-e2e-borrowing.png`。仅本地源码和本地服务生效，未改远程部署。

## 2026-10-15：默认快速筛选改为原文明示准入

- 本节覆盖下文历史版本中“间接监控候选也进入筛选表”的快速模式口径；旧 detailed 模式未改动。
- 只有 `DIRECT` 进入 `screened_metrics` / `matched_metrics`。`REVIEW` 不入选，目录评估记录为 `NOT_RELEVANT` 并保留间接或待确认原因，`candidate_metrics` 为空。高匹配分不能绕过此准入条件。
- 原文必须明确要求、使用或限制对应测量概念；同义名称和明确等价计算约束可匹配，不要求名称逐字一致。仅有定义、长期增长、稳定股息、主动管理或一般风险政策不足以推导额外指标；指标库 Mandate 分类不是 PDF 证据。
- 已保存历史报告不会自动改写；新规则需由加载新代码的后端重新分析后生效，旧 Docker 部署不受本地源码修改影响。
- 回归验证：筛选、Copilot、策略依据与评分相关测试共 56 项通过；有一条既有 Pydantic 证据夹具序列化警告。
- 真实 OMP / HTTP-SSE 验证：已上传的 `权益sample.pdf`，运行 `run-4cd119f8-5916-457c-a305-ae41b37dc113` 返回 `run.completed`。本次入选超额收益率（基准超额）、跟踪误差、单一证券占比；下行Beta 为 `NOT_RELEVANT`，所有入选关联均为 `DIRECT`。终态证据：`/tmp/mandate-explicit-evidence-smoke-result.json`。此结果不代表其他指标或全部文档已完成业务验收，语义分类仍依赖模型。
- 页面实际链路复验：旧本地后端 PID 7719 于 14:02 启动，早于 14:52 的规则修改且未启用自动重载；已重启为 PID 22255。使用 `/Users/liuruibing/Downloads/sample(1)/权益sample.pdf`，从 `http://127.0.0.1:9528/#/mandate-risk-v2/index` 选择附件并发送分析，运行 `run-3bb186ef-6202-4684-88f8-008acaad3853` 完成（后端分析 28.505 秒）。DOM 与 SSE 均只包含超额收益率（基准超额）、跟踪误差、单一证券占比；下行Beta 评估为 `NOT_RELEVANT`。上传 201、创建运行 200、SSE 200；无 console error、pageerror 或失败业务请求。截图 `/tmp/mandate-equity-explicit-e2e.png`，结构化证据 `/tmp/mandate-equity-explicit-e2e-result.json`。本次仅重启本地后端，不修改代理或远程部署。

## 2026-10-01：默认快速筛选

用户当前目标是筛选与 PDF 相关的指标供人工选择。默认流程改为 PDF 原文 + 完整指标库直接筛选，省去 Requirement IR 提取、逐条覆盖审计、去向分配及独立 Critic。普通长度 PDF、当前 34 行指标库正常仅调用模型一次；格式/引用校验失败最多修复一次。原文、页码、库行名称和算法仍由程序从权威来源读取，分数按 0–100 校验并降序展示；不按固定阈值过滤候选。

`MANDATE_RISK_V2_MODE=screening` 为默认值；需要原详细流程时设置 `MANDATE_RISK_V2_MODE=detailed` 后重启后端。`phase_a_only` 仍运行原要求提取流程。快速结果明确返回 `analysis_mode=screening`、`coverage_status=not_audited`，不宣称合同要求完整覆盖、指标库缺口或独立复核通过。

单次默认最多读取约 60,000 字符的条款，指标库每批最多 40 行，并发 2。超长文档按连续条款分段，每段浏览全部库行并合并有依据的候选；不会截断后续条款。跨段上下文的关联可能弱于全文阅读，需人工判断。结构化 `requirements` 在快速模式下仅为选中指标的原文依据，ID 使用 `SRC-`，不是完整的合同要求提取结果。

以下 Phase A / Phase B 描述和旧验收记录对应详细模式。

## 产品口径（筛选与匹配评分）

V2 的用途是帮助用户筛选符合 PDF 要求、目标、策略或风险暴露的相关指标，供用户判断。结果不代表自动入库、合规通过或算法完全等价。

- 相关指标统一进入六列“筛选结果”，按模型匹配分降序排列；同一指标合并展示全部独立要求。
- 相似度列显示 `match_score`（0–100），表示本次模型评估的文档关联程度。它不是统计校准的正确概率，也不是文本向量余弦相似度。
- 页面默认展示 ≥50 分，低分和历史未评分结果通过“显示全部候选”查看；该开关只改变页面视图，完整报告及结构化结果仍保留。表格按分类聚合、分类内分数降序，第一列纵向合并；详情同步筛选。
- V2 测试页从 `/health.runtime` 读取调用入口、后端模型和实际 V2 模式，服务端固定模型时禁用页面模型选择。快速筛选不显示覆盖审计或独立复核已执行；旧后端没有运行信息时明确标记未声明。
- 两种 PDF 的初标与核心漏选检查见 [人工复核清单](review/mandate-risk-v2-manual-review.md)，正式业务标签尚待确认。
- 每条 Requirement → 指标关联保留独立分数、`score_reason`、原文、页码、算法及实际差异；表格分数取该指标最高关联分，不表示整篇 PDF 覆盖率。
- 合同未点名指标、算法缺失、年化/事前口径不明，不自动排除合理监控候选。Python 不按评分阈值过滤，不要求填满十二个兼容维度。
- 值和参考组合缺少权威数据时仍为“—”。历史结果没有评分时显示“未评分”，不补造默认分数。

## 实现边界

Phase A 独立提取合同要求并审计全部条款；Phase B 全库分批筛选，由模型判断关联与评分。Python 校验原文 ID、原始库行身份、覆盖完整性、有限的0–100分数及非空评分理由。

DIRECT 表示与文档测量概念/要求有直接关联，REVIEW 表示间接监控用途或仍有差异，二者均进入统一筛选结果。compatibility 只解释实际相关维度，不再作为算法等价准入门禁。LIBRARY_GAP 表示确无可合理用于该 aspect 的库指标，不因缺一个完全等价算法就认定缺口。

独立 Critic 浏览完整库和排除理由，补召回、删除有具体证据的牵强关联、复核去向和遗漏条件。`score_adjustments` 可以修改已有相关关联的评分；补召回也必须评分。复核分数进入最终结构化结果和排序。

结构化主结果为 `screened_metrics`，`score_type=model_relevance`。原 `matched_metrics`、`candidate_metrics` 暂保留兼容，但不再解释为已确认入库指标。SSE 的 `run.completed.metadata.mandate_risk_v2.result` 返回上述内容；Markdown从同一结果生成。

新模型输出的相关关联必须有分数及理由，格式错误可重试。没有默认分数，也没有按样例名、固定条款 ID、指标行号或数量判断的运行规则。

## 当前评分版本的阶段交付记录

当前版本保留每行 key/core/Indicator 展示分组，整张表按匹配分排序，尚未按分组分块排列。指标名称、算法与身份来自原始指标库；未修改原始 CSV。

保存的权益完整 HTTP/SSE 运行 `run-68ec7723-87f8-4b52-880b-600f600189dc` 已完成：32 条 Requirement、25 个筛选指标、23 个待确认项、4 个库缺口、16 个非指标要求，分数范围 40–92。保存记录中的 V2 源码 SHA-256 与本次提交前源码一致。本次检查旧 run 的 SSE 回放返回 404；本次没有重新调用真实模型，不能将保存记录解释为当前服务的实时结果。

业务验收仍未完成：单一证券占比的关联解释将库中的“组合资产总值”视为合同要求的“组合市值”，等价依据不足；借款禁令与“可用融资余额”等弱关联仍进入筛选表。固收评分版最近保存的 Phase B 运行因无关 Requirement 引文校验失败而终止，尚未取得成功的评分结果。此前无评分固收结果不能替代评分版本验收。

提交前重新运行以下受影响测试，结果为 121 passed，另有一条 Starlette/httpx 弃用警告：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_mandate_risk_v2_*.py tests/test_main_and_config.py \
  tests/test_run_store_active_ttl.py tests/test_hermes_request.py \
  tests/test_hermes_contract.py tests/test_hermes_wire.py tests/test_workflow_engine.py
```

上述测试验证结构、校验与协议行为，不代表完整合同的指标关联准确率已通过独立业务验收。本次提交为 Python 后端阶段版本，不包含前端或生产部署验收；真实运行文件保存在 Git 忽略的 `.runtime/v2-validation/2026-09-30/`，不随提交上传。

## 先前版本验证记录（以下真实结果尚无匹配评分）

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_mandate_risk_v2_*.py tests/test_main_and_config.py \
  tests/test_run_store_active_ttl.py
```

本次扩展后 80 项通过（此前为 68 项）。覆盖新指标候选保留、缺算法候选、Critic 漏召回和误报、正式指标拒绝边界、原文与库行身份、并发批次完整性、符号基准比较、长任务 TTL、真实 HTTP SSE metadata 和重放；新增正式/候选混合关联、复合要求遗漏去向、分阶段超时与 Critic 独立预算检查。

后续修复和真实运行证据见 [定向验收记录](mandate-risk-v2-acceptance.md)。同一指标可因不同要求分别出现在正式表和候选表。Critic 使用 `missing_aspects` 显式保留遗漏维度为待确认；普通阶段预算 120 秒，Critic 预算 240 秒，超时仍 fail closed。

## 真实接口验证

使用本地 FastAPI 与 deepseek-v4-flash，上传用户提供的固收和权益 PDF，经 /v1/runs 与 SSE 获取终态。runner 会保存 Markdown 和结构化 JSON；Gold 暂缓，接口成功不代表业务准确率已全面验收。

首轮固收完成：run-11004a3a-4c5c-4847-a4ea-ef47b4c2cd9c，20 条 Requirement，26 个候选，756.08 秒。原文和候选已返回；该轮尚未包含后续文本预算、并行和精简提示优化。

首轮权益失败：run-78fd9741-f11c-4e01-b885-bc9cce6da2b4，比较约束被要求必须填写数字 value。已补符号基准比较的成功与拒绝测试，并修正表示与提示。后续复测使用新进程。

运行入口：

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8001
python scripts/mandate_risk_v2_remote_e2e.py \
  --base-url http://127.0.0.1:8001 --model deepseek-v4-flash \
  --pdf /path/to/mandate.pdf --report-dir /path/to/output --timeout 1200
```

模型身份、文档 SHA-256、run_id、终态、用量与耗时由 runner 输出。上传的新 PDF 和库中新增行沿用相同流程；没有按样例名、固定条款 ID、指标行号或主表条数判断的运行规则。
