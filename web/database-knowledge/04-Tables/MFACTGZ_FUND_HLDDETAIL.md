---
type: table
domain: 职年计划投资业绩
name: MFACTGZ_FUND_HLDDETAIL
status: supported
confidence: 4
sources:
  - path: DD_DW.MFACTGZ_FUND_HLDDETAIL
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - F_PLAN_STBC
  - F_PLAN_TGBC
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MFACTGZ_FUND_HLDDETAIL` (持仓明细表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录组合每日持有的具体证券、基金及费用计提持仓明细贴源表。
- **数据粒度**：一个组合在某一日期持有的某一种证券/费用明细项目。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **候选关联逻辑键**：`F_ID` (NUMBER(28)), `D_DATE` (TIMESTAMP), `VC_FUNDCODE` (VARCHAR2), `VC_SYMBOL` (VARCHAR2)

## 3. 核心字段分组
1. **组合与日期**：
   - `D_DATE` (TIMESTAMP)：核算日期
   - `VC_FUNDCODE` (VARCHAR2)：产品代码
2. **证券与代码（核心）**：
   - `VC_SYMBOL` (VARCHAR2)：证券代码 (E2 确认：**`'221002'`** 受托报酬，**`'220602'`** 投管报酬)
   - `VC_NAME` (VARCHAR2)：证券名称
   - `F_PRICE` (NUMBER(35,9))：市值 (本位币)
3. **资产与分类**：
   - `VC_TYPE` / `VC_TYPE_DETAIL`：证券大类与明细分类

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, VC_FUNDCODE, VC_SYMBOL, VC_NAME, F_PRICE FROM DD_DW.MFACTGZ_FUND_HLDDETAIL WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | VC_FUNDCODE | VC_SYMBOL | VC_NAME | F_PRICE |
  |---|---|---|---|---|
  *(0 rows)*

## 5. 上下游关联与函数提取
- `F_PLAN_STBC` 函数提取 `VC_SYMBOL = '221002'` 的 `F_PRICE` 汇总作为受托报酬。
- `F_PLAN_TGBC` 函数提取 `VC_SYMBOL = '220602'` 的 `F_PRICE` 汇总作为投管报酬。
