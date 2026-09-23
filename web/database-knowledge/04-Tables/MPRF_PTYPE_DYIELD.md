---
type: table
domain: 职年计划投资业绩
name: MPRF_PTYPE_DYIELD
status: supported
confidence: 4
sources:
  - path: DD_DW.MPRF_PTYPE_DYIELD
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/schema/2026-08-19__10_tables__constraints.md
    level: E3
    location: dbx_execute_query
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MPRF_PTYPE_DYIELD` (计划类型日收益率表)

## 1. 一句话定义与数据粒度
- **一句话定义**：按计划类型（如职业年金/企业年金）记录每日加权收益率的维度汇总表。
- **数据粒度**：某种计划类型在某一天的一条记录。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **非空列**：`D_DATE` (TIMESTAMP, NOT NULL), `VC_PLAN_TYPE` (VARCHAR2(50), NOT NULL)
- **候选逻辑粒度**：`D_DATE + VC_PLAN_TYPE`

## 3. 核心字段分组
- `D_DATE` (TIMESTAMP, NOT NULL)：日期
- `VC_PLAN_TYPE` (VARCHAR2(50), NOT NULL)：计划类型（E1 文档指出职业年金对应 `'ZYNJ'`）
- `F_YIELD` (NUMBER(22,8))：日收益率
- `D_UPDATETIME` (TIMESTAMP)：更新时间

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, VC_PLAN_TYPE, F_YIELD FROM DD_DW.MPRF_PTYPE_DYIELD WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | VC_PLAN_TYPE | F_YIELD |
  |---|---|---|
  *(0 rows)*

## 5. 上下游关联
- 由存储过程根据大宽表 `MPRF_F_PLAN_DAYNETVALUE` 汇总产生。
