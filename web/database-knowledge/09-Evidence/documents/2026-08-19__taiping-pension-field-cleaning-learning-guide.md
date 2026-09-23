---
type: evidence
domain: 职年计划投资业绩
name: 种子证据-太平年金清洗指南HTML
status: confirmed
confidence: 5
sources:
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: 全文
related_tables:
  - MDIM_PLAN_INFO
  - MDIM_FUND_INFO
  - MFACTGZ_FUND_HLDTOTAL
  - MFACTGZ_FUND_ASSETINOUT
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - DW_ZNST_INDEX_NEW.F_PLAN_DYIELD_BZ
last_verified: 2026-08-19
---

# 种子证据登记：太平年金清洗及计算学习指南 HTML

本文件登记种子学习资料 `outputs/taiping-pension-field-cleaning-learning-guide.html` 的档案摘要与证据元数据。

---

## 1. 档案基本信息
- **证据 ID**：`EVID-DOC-002`
- **文件路径**：`outputs/taiping-pension-field-cleaning-learning-guide.html`
- **原始标题**：太平养老职业年金与企业年金数据清洗及指标计算深入浅出学习指南
- **证据等级**：**E1**（权威业务指南与自测题库）
- **适用业务域**：职年计划投资业绩

---

## 2. 核心内容摘要
1. **术语对照表**：
   - 计划、组合、701A（资产规模）、702A（单价）、IN/OUT 流力、受托/投管报酬、BP 基点、几何连乘。
2. **架构流向图**：
   - 从估值贴源 `DD_AODS` 到 DW 过程 `DW_ZNST_INDEX_NEW` 到宽表 `MPRF_F_PLAN_DAYNETVALUE` 到前端 UNION ALL 查询 SQL 的全景链路。
3. **推导手算例**：
   - $Nav_{prev} = 100$, $IN = 20$, $Nav_t = 125 \implies R_2 = (125 - 100 - 20) / 100 = 5\%$。
   - $Nav_{prev} = 20\text{ 亿}$, $STBC + TGBC = 20\text{ 万} \implies 200,000 / 2,000,000,000 * 10000 = 1.00\text{ BP}$。
4. **合计行风控序列**：
   - 解释了为何波动率/最大回撤不能用 `AVG()`，必须对全池加权形成总体日收益序列后求 `STDDEV() * SQRT(250)`。
