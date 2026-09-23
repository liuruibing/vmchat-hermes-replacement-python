---
type: table
domain: 职年计划投资业绩
name: MPRF_F_PLAN_DAYNETVALUE
status: supported
confidence: 5
sources:
  - path: DD_DW.MPRF_F_PLAN_DAYNETVALUE
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/schema/2026-08-19__10_tables__constraints.md
    level: E3
    location: PK_PD
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_PLAN_INFO
  - MFACTGZ_FUND_HLDTOTAL
  - MFACTGZ_FUND_ASSETINOUT
related_functions:
  - F_PLAN_END_NETVALUE
  - F_PLAN_DYIELD_BZ_ZYNJ
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MPRF_F_PLAN_DAYNETVALUE` (计划日净值大宽表)

## 1. 一句话定义与数据粒度
- **一句话定义**：存放经夜间存储过程加工后的各职业年金计划每日资产净值、收益率（含多种剔除口径）、业绩报酬及久期等指标的数据仓库核心大宽表。
- **数据粒度**：一个计划在某一日期的一行记录（`VC_PLANCODE + D_DATE`）。

## 2. 数据库约束 (E3 元数据)
- **显式复合主键**：`VC_PLANCODE` (VARCHAR2, NOT NULL) + `D_DATE` (TIMESTAMP, NOT NULL)，带有数据库主键约束 `PK_PD`（由 E3 `ALL_CONSTRAINTS` 查询验证）。

## 3. 核心字段分组 (103 个字段分类)
1. **身份与主键**：
   - `VC_PLANCODE` (PK), `D_DATE` (PK), `VC_PLANNAME`
2. **净值与规模**：
   - `F_NETVALUE` (普通资产净值), `F_NETVALUE_TCZ` (剔除太平), `F_NETVALUE_TCB` (剔除保留)
3. **资金申赎汇总**：
   - `F_CAPITAL_IN` (投资分配), `F_CAPITAL_OUT` (投资提取), `F_GJHLX_IN` (归集户利息)
4. **日收益率指标（核心）**：
   - `F_DP_YIELD_BZ` (标准现金流日收益率), `F_DP_YIELD_BZ_TCZ` (剔除太平), `F_DP_YIELD_BZ_TCG` (剔除利息), `F_DP_YIELD_BZ_TCGZ` (剔除利息+太平)
5. **累计与区间收益率**：
   - `F_PLAN_YIELD_TBZ` (交易日成立以来累计), `F_PLAN_YIELD_TBZ_YEAR` (本年交易日累计), `F_PLAN_YIELD_ZBZ_MONTH` (本月自然日累计)
6. **业绩报酬**：
   - `F_PLAN_STBC` (受托报酬), `F_PLAN_TGBC` (投管报酬), `F_PLAN_YJBCYX` (业绩影响 BP)
7. **历史未赋值字段 (21 个)**：
   - 久期 `F_MODDURATION_*`、基准收益 `F_PLAN_BENCH_*` 等完全未赋值（恒为 NULL，详见 [`OQ-002`](../99-Inbox/Open-Questions.md#oq-002)）。

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, VC_PLANCODE, F_NETVALUE, F_DP_YIELD_BZ, F_PLAN_STBC, F_PLAN_TGBC FROM DD_DW.MPRF_F_PLAN_DAYNETVALUE WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | VC_PLANCODE | F_NETVALUE | F_DP_YIELD_BZ | F_PLAN_STBC | F_PLAN_TGBC |
  |---|---|---|---|---|---|
  *(0 rows)*

## 5. 上下游关联与前端 SQL 应用
- 前端报表通过 `SELECT ... FROM DD_DW.MPRF_F_PLAN_DAYNETVALUE` 查询，并附加 `UNION ALL` 生成 `RK=999` 合计行。
