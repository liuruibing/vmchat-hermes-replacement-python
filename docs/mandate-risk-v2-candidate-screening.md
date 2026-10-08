# V2 指标筛选口径与验证记录（2026-09-30）

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
