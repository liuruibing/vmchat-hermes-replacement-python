---
type: evidence
domain: 职年计划投资业绩
name: 种子证据-太平养老学习路径
status: confirmed
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
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

# 种子证据登记：太平养老学习路径 Markdown 说明

本文件登记种子学习资料 `outputs/taiping_pension_learning_roadmap.md` 的档案摘要与证据元数据。

---

## 1. 档案基本信息
- **证据 ID**：`EVID-DOC-001`
- **文件路径**：`outputs/taiping_pension_learning_roadmap.md`
- **原始标题**：太平养老职业年金与企业年金数据清洗及 SQL 计算深入浅出学习路径
- **证据等级**：**E1**（权威业务文档与种子分析提炼）
- **适用业务域**：职年计划投资业绩 / 企年业绩

---

## 2. 核心内容摘要
1. **实体与维表**：
   - 计划 (Plan) = 大型超市；维表 `MDIM_PLAN_INFO` (主键候选 `VC_PLAN_LIC_ID`)。
   - 组合 (Fund) = 独立专柜；维表 `MDIM_FUND_INFO` (代码 `VC_FUNDCODE`, 计划归属 `VC_PLAN_CODE`, 管理人 `VC_NAME_GLR`)。
2. **源头估值科目**：
   - `701A` 科目：`MFACTGZ_FUND_HLDTOTAL` 中 `VC_SUBCODE = '701A'` 的 `F_PRICE`（资产总净值）。
   - `702A` 科目：`MFACTGZ_FUND_HLDTOTAL` 中 `VC_SUBCODE = '702A'` 的 `F_PRICE`（单位净值 NAV）。
   - 资金流水：`MFACTGZ_FUND_ASSETINOUT` 中 `VC_TYPE = 'IN'` 或 `'OUT'` 的 `F_AMOUNT`。
3. **收益率公式与对数连乘**：
   - 成立日收益：$R_1 = (Nav_1 - F\_SET\_AMOUNT) / F\_SET\_AMOUNT$
   - 后续交易日收益：$R_t = (Nav_t - Nav_{prev} - IN_t + OUT_t) / Nav_{prev}$
   - 几何连乘对数转化：`POWER(2, SUM(LOG(2, R + 1))) - 1`
4. **剔除与业绩报酬**：
   - TCZ（剔除太平）：实际代码条件 `MDIM_FUND_INFO.VC_NAME_GLR LIKE '太平养老保险股份有限公司%'`
   - 受托报酬代码 `221002`，投管报酬代码 `220602`，日影响率乘以 10000 转化为 BP
5. **SQL 聚合与 5 大历史陷阱**：
   - 明细与 RK=999 合计行拼接
   - 企年 TCZ 错调未剔除函数、企年净值硬复制、职年 1105 特殊补丁、企年凭证完整性校验及 21 个未赋值字段
