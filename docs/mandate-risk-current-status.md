# Mandate 风险识别：当前进度交接

更新：2026-09-29。后端分支：`optimize/mandate-risk-generic-recall`。本文件记录本地代码和测试状态，不代表已部署到 Colab，也不代表 Excel 样例已完全通过。

## 已确认的业务口径

- 正式主表只放有合同直接依据、测量对象与算法口径相符的原始库指标；推断项单列待确认。Excel 是覆盖核对参考，不是照抄指标清单。
- “Mandate解读”引用 PDF 可定位的逐字原文与页码；不得把跨页片段拼成一条连续原文。
- 不创建正式指标、算法或阈值。明确量化要求没有等价指标时沿用“指标库缺口”；暂不新增“投资合规约束”报告类别。
- 权益合同的“年化事前 Tracking Error ≤100%”与原始库 `TE=σ(Rp−Rb)` 未证明同口径，用户决定先列待确认。**当前代码尚未落实这一条，真实报告仍把跟踪误差列主表。**
- 先直接测试后端接口；静态页是后续正式入口，Vue 业务页不影响当前接口测试。

## 当前代码做到了什么

| 部位 | 现状 |
| --- | --- |
| 原始库与候选 | 支持非固定行数的库；词法候选和 Mandate 回退仍保留；新增受控目录审计，按固定行序覆盖全部策略适用库行，能把无共享英文元数据的中文新指标从英文合同召回。 |
| 身份和引文 | Python 校验审计提案的库行、策略和真实 `clause_id`，从提取文本重建原文、页码和偏移；同一行保留原候选并按条款 ID 合并审计证据。 |
| 完整性门禁 | 语义模型对每个**已送审候选行**必须恰好返回一次；漏行、重复、未知行、错名会重试一次，仍错误则 `run.failed`，不补造 `REJECTED`。审计非法、超时也失败。**这不是合同条款全集覆盖门禁。** |
| 主表与报告 | 目前仅 `DIRECT` 进入主表；推断项在待确认。摘要“Mandate解读”从已校验引文选取；值、参考组合、相似度没有数据时显示 `—`。报告问答 Agent 配置存在，但本轮未重新测试前端问答闭环。 |
| 调用量 | 审计与语义判断的 Provider usage 分别统计；缺少 `total_tokens` 或某次调用未报 usage 时不宣称总量完整。 |
| PDF 条款 | `split_document_clauses` 保留页码和精确 source span；局部修复了独立印刷页码混入下一段引文。权益 PDF 第 7 页 `c0118` 现在是 `sector<100%`，但第 6–7 页仍是两段独立引文，未自动重建跨页完整句。 |

代码主要位于 `app/mandate_risk/`、`app/workflow/graphs/mandate_risk.py`，测试位于 `tests/test_mandate_risk*.py`。实现中仍有按既有指标名称写的 alias、分组、策略适用例外和少数测量对象规则；目录审计降低了新增指标对 alias 的依赖，**没有消除所有硬编码与误判风险**。原始指标 CSV 未修改。

## 已验证的证据

本地在当前代码上运行：

```text
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -p no:cacheprovider -q \
  tests/test_mandate_risk_provenance.py tests/test_mandate_risk_coverage_audit.py \
  tests/test_mandate_risk.py tests/test_mandate_risk_precision.py \
  tests/test_mandate_risk_precision_v2.py tests/test_mandate_risk_renderer_table.py \
  tests/test_mandate_risk_semantics_v3.py
```

结果：69 passed；`git diff --check` 通过。测试覆盖候选漏行重试/失败、跨语言合成新指标、非法审计提案、审计超时、证据合并、usage 完整性、部分数值/条件引文校验，以及页码污染。**测试通过不代表真实模型稳定识别。**

本地新起 `127.0.0.1:8001`，以 `deepseek-v4-flash` 上传原 PDF 并经 `/v1/runs/{run_id}/events` 读取 SSE 终态（测试后已停掉该临时进程，未动已有 8000 服务）：

| PDF | run ID | 终态 | 主表 / 待确认 / 缺口 | 未解决 |
| --- | --- | --- | --- | --- |
| `/Users/liuruibing/Downloads/sample(1)/固收sample.pdf` | `run-50346207-ac19-40cf-b26a-8731addf92b1` | `run.completed` | 0 / 6 / 2 | 新购收益率比基准高 10 bps 已列缺口；“稳定现金流”是否应列缺口仍待判。 |
| `/Users/liuruibing/Downloads/sample(1)/权益sample.pdf` | `run-47f343f6-bc1b-4bc4-a80f-2818705e4011` | `run.completed` | 3 / 8 / 4 | §9.10 两档 TPMF 市值限额（当前解析 `c0111`、`c0112`）整条漏报；跟踪误差仍错误地在主表；某些待确认项测量对象不等价。 |

两次报告分别使用 Provider 报告的 40,322 / 43,130 tokens，其中目录审计为 16,018 / 12,480 tokens。这个成本是本地 DeepSeek 的一次观察，不能外推到 Gemini。权益报告中的 `sector<100%` 曾混入印刷页码 `7`；**页码局部修复发生在这次接口运行之后**，只通过测试和原 PDF 重新提取验证，尚未重新跑真实接口。

## 当前阻塞和工作边界

最大的正确性缺口是：模型可以漏掉整条合同限额，而校验器只看它已经提出的 `matches/gaps`；所以上述权益报告仍错误地以 `run.completed` 结束。计划过“量化条款去向”门禁，但在用户要求交接时已停止执行代理，**没有实现或提交阶段 3 的覆盖门禁**。用户确认的跟踪误差降级也尚未实现。

Colab/Gemini 公网后端及静态页完整闭环未对本分支复验。前端仓库 `/Volumes/onePiece/公司前端项目/友邦绩效/datadriver-fund-amc-tyjx-vue` 仍有独立未提交页面/路由/代理改动；本次后端交接提交不包含它们。后端根目录的未跟踪 `MANDATE_RISK_DEV_ENVIRONMENT.md` 是环境参考资料，本次不纳入提交。不要把当前本地 API 结果写成公网验收。
