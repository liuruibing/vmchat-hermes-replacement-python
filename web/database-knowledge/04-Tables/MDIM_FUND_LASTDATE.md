---
type: table
domain: 职年计划投资业绩
name: MDIM_FUND_LASTDATE
status: supported
confidence: 4
sources:
  - path: DD_DW.MDIM_FUND_LASTDATE
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/schema/2026-08-19__10_tables__constraints.md
    level: E3
    location: dbx_execute_query
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_FUND_INFO
  - MDIM_PLAN_INFO
related_functions: []
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MDIM_FUND_LASTDATE` (组合最新日期表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录每个组合及计划最新有估值/持仓数据日期的物理快照表。
- **数据粒度**：一个组合（`VC_FUNDCODE`）一行记录。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **非空列**：`VC_FUNDCODE` (VARCHAR2(50), NOT NULL)
- **候选主键粒度**：`VC_FUNDCODE`

## 3. 核心字段分组
- `VC_FUNDCODE` (VARCHAR2(50), NOT NULL)：组合代码
- `VC_FNAME` (VARCHAR2(100))：组合名称
- `VC_PLANCODE` (VARCHAR2(40))：计划登记号
- `VC_PLANNAME` (VARCHAR2(500))：计划名称
- `D_DATE` (VARCHAR2(10))：最新持仓/核算日期字符串
- `VC_TYPE_DETAIL` / `VC_TYPE_IN`：分类明细
- `D_UPDATETIME` (TIMESTAMP)：更新时间

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT VC_PLANCODE, VC_FUNDCODE, VC_FNAME, D_DATE FROM DD_DW.MDIM_FUND_LASTDATE WHERE ROWNUM <= 5`
- **探查结果**:
  | VC_PLANCODE | VC_FUNDCODE | VC_FNAME | D_DATE |
  |---|---|---|---|
  *(0 rows)*

## 5. 上下游关联
- 用于前端报表或 ETL 查询时快速定位每个组合的最晚可用核算切片日期。
