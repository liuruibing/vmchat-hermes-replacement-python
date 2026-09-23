---
type: learning
domain: 职年计划投资业绩
name: 职年计划投资业绩-Quiz
status: confirmed
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段1-5检验问题
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: 自测卡片与标准答案
related_tables:
  - MDIM_PLAN_INFO
  - MDIM_FUND_INFO
  - MFACTGZ_FUND_HLDTOTAL
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 学习卡：职年计划投资业绩 - 五级自测 Quiz 与标准答案

本自测卡片分为**概念级、数据级、指标级、血缘级、排障级**五个阶梯，答案必须严格链接回已验证的卡片与证据。

---

## 1. 概念级 Quiz
- **问题**：如果业务人员想查询“太平养老托管的所有职业年金计划中，由‘易方达基金’管理的组合有哪些”，你需要连接哪两张表？依靠哪两个字段进行关联？
- **标准答案**：
  1. 连接维表：`DD_DW.MDIM_PLAN_INFO`（计划维表）和 `DD_DW.MDIM_FUND_INFO`（组合维表）。
  2. 候选关联字段：`MDIM_PLAN_INFO.VC_PLAN_LIC_ID = MDIM_FUND_INFO.VC_PLAN_CODE`。
  3. 过滤条件：`MDIM_PLAN_INFO.VC_TYPE_DETAIL = 'ZYNJ'` 且 `MDIM_FUND_INFO.VC_NAME_GLR LIKE '%易方达%'`。
  4. 链向卡片与证据：[`02-Objects/职年计划.md`](../02-Objects/职年计划.md) & [`EVID-DOC-001`](../00-Overview/证据索引.md)。

---

## 2. 数据级 Quiz
- **问题**：某组合今天总资产净值（`701A`）比昨天增加了 1000 万元。你能直接断定该组合投资赚了 1000 万元吗？在数据库里还需要检查哪张表、哪两个字段？
- **标准答案**：
  1. 不能直接断定。增加的 1000 万元可能是客户今天新存入的申购款（资金流入 `IN`）。
  2. 需要检查的表：`DD_DW.MFACTGZ_FUND_ASSETINOUT`。
  3. 检查字段：确认日期 `D_CONFIRM_DATE` 对应的业务类别 `VC_TYPE`（`'IN'` 与 `'OUT'`）的发生金额 `F_AMOUNT`。
  4. 链向卡片与证据：[`02-Objects/资金流.md`](../02-Objects/资金流.md) & [`04-Tables/MFACTGZ_FUND_ASSETINOUT.md`](../04-Tables/MFACTGZ_FUND_ASSETINOUT.md)。

---

## 3. 指标级 Quiz
- **问题**：如果某计划昨天资产净值为 20 亿元。今天查询得到受托报酬 $STBC = 40,000$ 元，投管报酬 $TGBC = 160,000$ 元。计算当天的业绩报酬影响率是多少 BP（万分比）？
- **标准答案**：
  1. 业绩报酬总额 $= 40,000 + 160,000 = 200,000$ 元。
  2. 日影响率 $= 200,000 / 2,000,000,000 = 0.00010$。
  3. 转换为 BP 展示 $= 0.00010 \times 10000 = \mathbf{1.00\text{ BP}}$。
  4. 链向卡片与证据：[`03-Metrics/业绩报酬影响.md`](../03-Metrics/业绩报酬影响.md) & [`07-Rules/业绩报酬-BP换算.md`](../07-Rules/业绩报酬-BP换算.md)。

---

## 4. 血缘级 Quiz
- **问题**：标准现金流法日收益率计算公式中，为什么要在期末净值增量中扣除 $IN$ 并加回 $OUT$？
- **标准答案**：
  1. 客户新存入的钱 ($IN$) 增加了期末资产规模，但并非实际投资盈利，必须扣除；
  2. 客户拿走的钱 ($OUT$) 减少了期末资产规模，但原本属于投资成果，必须加回。
  3. 链向卡片与证据：[`05-Lineage/标准现金流收益率计算链路.md`](../05-Lineage/标准现金流收益率计算链路.md)。

---

## 5. 排障级 Quiz
- **问题**：为什么在计算前端 SQL 合计行的“波动率 (F_VIX)”时，不能直接对各个单计划的波动率取平均值 (`AVG`)？SQL 实际上采取什么步骤计算？
- **标准答案**：
  1. 原因：各个计划规模差异巨大，算术平均会严重夸大小计划波动对整体资金池的影响，违反风险计量原则。
  2. 正确步骤：先按各个计划每日资产净值作为权重，加权计算出每天的“全池总体加权日收益率时间序列”；再对此总体序列求 `STDDEV() * SQRT(250)`。
  3. 链向卡片与证据：[`03-Metrics/年化波动率.md`](../03-Metrics/年化波动率.md) & [`05-Lineage/风险指标计算链路.md`](../05-Lineage/风险指标计算链路.md)。

---

## 6. 我真正需要记住的内容 (Top 5)
1. Quiz 答案均有源可溯，严禁将未验证的猜测作为标准答案。
2. `701A` 增加不等于赚钱，必须看 `ASSETINOUT` 的 `IN` 与 `OUT`。
3. 业绩报酬在 SQL 层必须乘以 10000 转换为 BP 表达。
4. 跨计划风控聚合必须对总体加权日收益序列求标准差。
5. 唯一存在数据库显式 PK 约束的表为 `MPRF_F_PLAN_DAYNETVALUE` (`PK_PD`)。

---

## 7. 待确认问题与延伸思考
- 详见 [`99-Inbox/Open-Questions.md`](../99-Inbox/Open-Questions.md) 进行增量自测与疑问排查。
