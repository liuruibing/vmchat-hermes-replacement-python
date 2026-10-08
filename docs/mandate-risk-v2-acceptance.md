# Mandate Risk V2 定向验证与关键条款核对（2026-09-30）

说明：本文记录的是此前“正式/候选”严格口径版本。后续筛选与匹配评分变更见 `mandate-risk-v2-candidate-screening.md`；下列旧运行结果不含分数，不应作为评分版本的验收证据。

本次验证覆盖结果组装、指标映射协议、复合要求去向和真实模型运行。它是关键条款核对记录，不是完整合同的独立 Gold 验收，也不代表前端或公网部署已验收。

分支为 `optimize/mandate-risk-generic-recall`，基线 HEAD 为 `39c355e3c1ee9ae3e9f600b983b103034ef9af3a`，验证使用含未提交改动的工作区。代码哈希及文档哈希保存在本地 `.runtime/v2-validation/2026-09-30/manifest*.json`，不能只用 HEAD 重现本次运行。原始指标库未修改。

## 本次修复

- 同一库指标分别关联 DIRECT 和 REVIEW 要求时，正式表及候选表各自保留对应关联、原文与差异，REVIEW 不因该指标已有正式关联而丢失或升级。
- `row_assessments.outcome` 明确只能使用 `LINKED` / `NOT_RELEVANT`，与 `links.level` 的 DIRECT / REVIEW / REJECTED 分开。
- 合同明确要求计量基础时，不能把库里的资产总值、总资产或 NAV 默认视为 market value；依据不足保留 REVIEW。
- 去向审计须说明全部独立时间窗口、阈值、对象和条件分支。Critic 新增 `missing_aspects`：引用真实 Requirement 与原文，将遗漏维度显式列为待确认；未知 ID、无关证据和重复维度被拒绝。Python 只保存 Critic 提案，不从样例规则生成业务要求或指标。
- 模型超时给出 `MANDATE_MODEL_TIMEOUT`、阶段及预算。抽取、覆盖、分批映射和去向审计默认 120 秒，Critic 单独使用 240 秒的有界预算。超时仍失败，不发布半张正式表。

## 确定性测试

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_mandate_risk_v2_*.py tests/test_main_and_config.py \
  tests/test_run_store_active_ttl.py
git diff --check
```

结果：80 passed；`git diff --check` 通过。新增覆盖两种正式/候选混合关联、Critic 遗漏维度的保存与拒绝边界、三个映射阶段的超时诊断、独立 Critic 预算的成功与拒绝边界。测试有一条现有 Starlette/httpx 弃用警告。

## 输入快照

| 文档 | SHA-256 | 页数 / canonical clauses |
| --- | --- | --- |
| 权益sample.pdf | `3aaf3f50e4015129d6d388425fe6b6503eed5e7391b0ef6d20950afd30c117d6` | 7 / 136 |
| 固收sample.pdf | `316c96750fc2395222bcab9e191f2e5190795c28d843f8899375b9b10eb761f8` | 6 / 109 |

指标源为 `agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv`，34 个数据行，SHA-256 为 `cd097edb49be7b73152292722db71d41e7f65d40444b35cd7fc3e96a071fc4d5`。库行 ID 为源行身份，不等于数据行总数。

## 真实模型记录

使用 `.env` 配置的 `deepseek-v4-flash`。HTTP 验证使用本地独立 8002 进程，不影响原有 8000、8001、7310 服务。

| 验证 | 身份 / 终态 | 结果与限制 |
| --- | --- | --- |
| 权益首轮 HTTP 全流程 | `run-49397a1c-d634-4905-9154-2e0bbd501a4b` / `run.completed` | 583.81 秒；35 条要求、1 个正式指标、22 个候选。机械证据校验通过，但人工发现单券分母等价依据不足、TPMF 流动性最终去向仅说明 7 日，未作业务验收通过。 |
| 固收首轮 HTTP 全流程 | `run-cc39942a-a4c6-48d9-96fe-e8ce8288c1ee` / `run.failed` | 465.54 秒；映射阶段失败且旧错误文本为空。失败前 Phase A 识别 20 条要求，不输出正式结果。 |
| 固收加入诊断后的 HTTP 复测 | 见 `results-after-review.jsonl` / `run.failed` | 486.06 秒；Phase A 识别 18 条要求，明确为 `stage=critic; timeout_seconds=120`。据此增加独立 Critic 预算。 |
| 权益修正后 Phase B 单独复测 | 无新的 HTTP run ID；复用权益首轮已覆盖 IR / `analysis.completed` | 293.84 秒；35 条要求、0 个正式指标、24 个候选、23 个待确认、8 个库缺口、18 个非指标要求。映射与 Critic 共 7 次调用，校验重试 0 次，Provider 报告 232,443 tokens。此轮发生在 Critic 预算调整前；没有重新执行 Phase A 或 HTTP SSE。 |
| 固收使用 240 秒 Critic 预算的 HTTP 复测 | `run-66201517-f72e-4aac-beec-49f8159af451` / `run.completed` | 365.62 秒；22 条要求、0 个正式指标、18 个候选、15 个待确认、1 个库缺口、16 个非指标要求。映射与 Critic 共 7 次调用，校验重试 0 次；全流程 Provider 报告 256,069 tokens。HTTP SSE 重放的结构化结果与首次保存结果完全一致。 |

权益首轮映射阶段为 13 次调用、6 次校验错误（五个批次的 outcome 枚举及一次 Critic 引用），Provider 报告 427,450 tokens；修正后 Phase B 为 7 次调用且无校验重试。两轮同时改变了提示和去向复核口径，是运行观察，不能据此宣称稳定的成本或准确率。

## 权益关键条款核对

以下编号只对应上述 PDF/parser 快照，不参与运行时判断。原文、页码和 source span 分别保存在 `权益sample-clauses.json`；人工清单保存在 `key-requirements.json`。已校验结果的全部 CanonicalEvidence 与源条款一致，指标身份/算法来自只读库，34 个库行均有唯一处置。

| 要求 | 原文条款 / 页码 | IR 与最新 Phase B 去向 |
| --- | --- | --- |
| 超额收益与策略 | c0073 / p.5 | REQ-0006 已抽取；地理、行业和交易策略分别待确认。超额收益目标自身的去向与其他回报要求的关联仍需完整 Gold 核对。 |
| 单券限额 | c0103 / p.6 | REQ-0018：建仓期、单一证券敞口、子组合市值分母、≤100% 保留。单一证券占比因“资产总值”计价基础不明为 REVIEW，不进主表。 |
| 行业限额与 TPMF 纳入范围 | c0105/c0106 / p.6 | REQ-0019/0020：GICS、≤100%、建仓期、行业专属 TPMF 纳入范围保留；行业偏离度为辅助候选，绝对行业敞口及 TPMF 穿透口径列缺口。 |
| 年化事前 TE | c0108 / p.6 | REQ-0021 保留条件与≤100%；库 `TE=σ(Rp−Rb)` 未说明 annualised / ex-ante，跟踪误差为 REVIEW。 |
| TPMF 市值低于 RMB 1bn | c0111 / p.6 | REQ-0022 独立保留条件与 `min(100%基金市值,RMB100m)`；基金层算法列库缺口。 |
| TPMF 市值达到 RMB 1bn | c0112 / p.6 | REQ-0023 独立保留≥门槛与≤100%基金市值；列库缺口。 |
| TPMF 特殊许可 | c0113 / p.6 | REQ-0024 保留全部准入条件及 DEPENDS_ON 分散度/流动性要求；基金层测量列缺口。许可类别与缺口呈现仍需业务确认。 |
| TPMF 分散度 | c0115/c0118 / p.6–7 | REQ-0025 保留单名、前十、单行业三个<100%门槛；两页证据分别引用；底层持仓算法列缺口。 |
| TPMF 底层流动性 | c0119 / p.7 | REQ-0026 的最终 aspect 显式保留 `1 day >0%` 和 `7 days >0%`，列底层算法缺口；组合自身七日清算比例不被当作等价算法。 |
| 单一 MMF 限额 | c0120 / p.7 | REQ-0027 保留 AI Business Unit、MMF AUM 分母和≤100%；列库缺口。 |
| 百分比限制按市值计量 | c0121 / p.7 | REQ-0028 独立保留为计量约定，并在单券候选差异中引用该口径；本身为 NON_METRIC。 |

Critic 还指出 REQ-0004 中“主要投资于中国 Issuer 的高质量 Common Shares”对象维度没有去向，已保存为 PENDING_REVIEW，未静默删除。

## 固收关键条款核对

购买时点的新购收益率相对指定子组合 Benchmark Index yield 高 10 bps，原文为 c0064 / p.4。最终 REQ-0008 保留 `new purchase yield`、`at the time of purchase`、指定基准、10 bps 和完整原文；相关的组合超额收益率、信息比率和债券信用利差均为 REVIEW，未宣称等价正式算法。

该条尚不能判为完全正确：IR 使用 `> 10 bps`，去向 aspect 写 `≥10 bps`，reason 又写 `>10 bps`。目标型表达与比较符号仍需人工核对；原文已保留，不能把归一化字段当成已确认的严格阈值。该要求当前只列待确认，是否应另列正式算法缺口仍需业务确认。

Critic 还发现 held-to-maturity 的 `credit concerns` 例外分支没有独立去向，已列为 PENDING_REVIEW。当前唯一库缺口为“CNY 计价货币口径与 mainly 购买占比量化”，该定性范围是否应成为库缺口尚未验收。

固收结果的全部 CanonicalEvidence、指标名称/算法/库快照校验无错误，34 个库行均有唯一处置。固定数量不能证明准确率：本次三轮固收 Phase A 分别输出 20、18、22 条要求，须按合同语义核对拆分与合并。

## 本地证据与未验收范围

本地证据目录：`.runtime/v2-validation/2026-09-30/`。目录被 Git 忽略，包含输入快照、代码哈希、HTTP 运行记录、Markdown/结构化 JSON、独立 Critic 输出及机械核对结果；需留存该目录才能复查真实运行。

完整合同的 Requirement recall、Definition false positive 和全部映射准确率尚未通过独立 Gold 验收。库缺口、一般许可和定性目标的业务分类仍需核对；本次没有前端联调、公网部署或生产 V1 替换。
