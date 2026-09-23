---
type: table
domain: 职年计划投资业绩
name: MFACTGZ_FUND_ASSETINOUT
status: supported
confidence: 4
sources:
  - path: DD_DW.MFACTGZ_FUND_ASSETINOUT
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - F_PLAN_DYIELD_BZ_ZYNJ
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MFACTGZ_FUND_ASSETINOUT` (资金申赎流水表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录各个投资组合申购（流入 IN）与赎回（流出 OUT）资金发生额的贴源流水表。
- **数据粒度**：一次特定的资金申赎事件记录。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **候选关联逻辑键**：`VC_FUNDCODE + D_CONFIRM_DATE`

## 3. 核心字段分组
1. **身份与时间**：
   - `VC_FUNDCODE` (VARCHAR2)：组合代码
   - `D_CONFIRM_DATE` (TIMESTAMP)：确认日期 (关键日期关联字段)
   - `D_CHARGEUP_DATE` (TIMESTAMP)：到账日期
2. **业务类型与发生额**：
   - `VC_TYPE` (VARCHAR2)：业务类别（**`'IN'`** 代表流入，**`'OUT'`** 代表流出）
   - `F_AMOUNT` (NUMBER)：发生金额
   - `F_SHARE` (NUMBER)：份额

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_CONFIRM_DATE, VC_FUNDCODE, VC_TYPE, F_AMOUNT FROM DD_DW.MFACTGZ_FUND_ASSETINOUT WHERE ROWNUM <= 5`
- **探查结果**:
  | D_CONFIRM_DATE | VC_FUNDCODE | VC_TYPE | F_AMOUNT |
  |---|---|---|---|
  | 2025-02-17 | TQ001601 | OUT | 30100.00 |
  | 2025-05-25 | TQ001601 | OUT | 30100.00 |

## 5. 上下游关联与收益率算法调用
- 在 `F_PLAN_DYIELD_BZ_ZYNJ` 中按 `D_CONFIRM_DATE = D_DATE` 汇总当日组合的 `IN` 与 `OUT` 金额，用于扣除申赎对投资收益率的影响。
