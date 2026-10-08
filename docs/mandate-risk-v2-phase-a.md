# Mandate Risk V2 — Phase A 状态与验收门

## 目标

V2 的第一阶段只解决一个问题：**AI 是否完整、忠实地理解了 Mandate PDF 本身。**

当前阶段刻意不读取风险指标库，也不执行 Requirement → Metric 映射。这样可以把两类错误拆开：

1. PDF 没读懂 / 漏掉合同要求；
2. PDF 已读懂，但指标映射错误。

生产 Agent `mandate-risk-ai` 仍使用 V1 `mandate-risk-analysis`。V2 只通过独立实验 Agent `mandate-risk-v2-lab` / workflow `mandate-risk-analysis-v2` 暴露，不替换生产路径。

## Phase A 流程

```text
PDF text
→ canonical clauses
→ AI Requirement Extraction
→ Requirement IR
→ AI Coverage Review
→ 若发现遗漏：带 reviewer feedback 重新完整理解文档（最多 2 轮）
→ coverage complete
→ 输出 Requirement IR
```

正常大小的 Mandate 优先一次性把全部 canonical clauses 交给模型做全局理解；只有超过通用 clause/字符阈值的长文档才使用 overlap windows。Chunking 是规模兜底，不是默认理解策略。

## 职责边界

AI 负责：

- 识别目标、策略、范围、限额、禁止、许可、条件分支、例外；
- 区分 Requirement / Definition / Context；
- 理解 measurement object、scope、qualifier、condition；
- 在 Coverage Review 中发现遗漏或部分覆盖。

Python 负责：

- clause_id 必须真实存在；
- Requirement / Definition / Context 的正式 ID；
- evidence quote/page/source span 从 clause 重建；
- reviewer 不能引用不存在的 clause/requirement；
- coverage 未闭合时 fail closed；
- 不用 sample/metric-specific 规则替 AI 做业务语义判断。

## Requirement IR 原则

Requirement 类型只描述文档角色，不枚举具体风险指标：

```text
OBJECTIVE
STRATEGY
SCOPE
QUANTITATIVE_TARGET
QUANTITATIVE_LIMIT
PROHIBITION
PERMISSION
CONDITIONAL_RULE
EXTERNAL_POLICY
GOVERNANCE
OTHER
```

业务语义保留在开放字段：

```text
subject
measurement.concept
measurement.object
measurement.qualifiers
constraint
scope
conditions
exceptions
attributes
```

复杂条件可使用关系：

```text
BRANCH_OF
QUALIFIES
EXCEPTION_TO
DEFINES_SCOPE_FOR
DEPENDS_ON
```

## Coverage Gate

Coverage Reviewer 会重点检查：

- 数字 / % / bps / currency / 时间单位；
- 比较符与阈值；
- shall / must / may only / not permitted 等义务语言；
- if / unless / except 等条件分支；
- 多档阈值、复合规则、scope、denominator、measurement basis。

Python 的这些检测只能生成 coverage hints，**不能直接创建 Requirement**。

Reviewer 返回：

```json
{
  "missing_clauses": [],
  "partial_requirements": []
}
```

两个数组非空时，系统不会把结果当作完整分析。当前实现会以 reviewer feedback 为线索重新阅读原始 clauses；旧 IR 被丢弃，Python 不做语义补丁。超过最大修复轮次仍不能闭合时返回 `MANDATE_REQUIREMENT_COVERAGE_INCOMPLETE`。

## 当前测试覆盖

已有 deterministic tests 验证：

- Extraction prompt 不包含风险指标候选；
- 假 clause_id 被拒绝；
- Definition 不会由 Python 转成 Requirement；
- evidence page/source span 由 Python 重建；
- 双条件 branch 可独立保留；
- overlap 只去除 evidence-identical exact duplicate；
- coverage hints 不赋予业务类型；
- reviewer 假 clause / requirement 引用被拒绝；
- incomplete coverage fail closed；
- reviewer 发现遗漏后可触发完整重提取并恢复第二条件 branch；
- V2 Agent / workflow 与 V1 隔离注册。

这些测试只证明协议和门禁行为，不证明真实模型识别准确率。

## 下一验收门：两份真实 PDF

在进入 Requirement → Metric Mapping 之前，必须先用真实模型对固定收益和权益两份 sample 做 Phase A 重跑，并与独立 Gold Requirement Matrix 对比。

验收目标：

```text
P0 Requirement Recall = 100%
Definition False Positive = 0
Evidence Accuracy = 100%
Silent Missing Requirement = 0
```

特别关注：

- 固收：购买时点 new purchase yield 相对 benchmark +10bps 必须被独立识别；
- 权益：Single Name、Sector、annualised ex-ante TE、TPMF 两档规则、特殊 allowance、TPMF diversification、1/7 day liquidity、single MMF limit、market-value measurement basis 必须全部拥有独立可追踪的 Requirement。

只有 Phase A 真实模型验收通过，才进入 V2 Phase B：Requirement → Metric Semantic Mapping。
