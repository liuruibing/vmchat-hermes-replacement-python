---
type: table
domain: 职年计划投资业绩
name: MDIM_PLAN_INFO
status: supported
confidence: 4
sources:
  - path: DD_DW.MDIM_PLAN_INFO
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MDIM_PLAN_INFO` (计划维度表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录受托或托管管理的各省市职业年金及企业年金计划基本物理属性的维表。
- **数据粒度**：一行代表一个独立的年金计划实体。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **非空列**：`VC_PLAN_CODE` (VARCHAR2(50), NOT NULL)
- **候选主键粒度**：`VC_PLAN_LIC_ID`（年金计划登记号）或 `VC_PLAN_CODE`（计划代码）

## 3. 核心字段分组
1. **身份与代码**：
   - `VC_PLAN_CODE` (VARCHAR2, NOT NULL)：计划代码
   - `VC_PLAN_LIC_ID` (VARCHAR2)：年金计划登记号
   - `VC_PLAN_NAME` / `VC_PLAN_FNAME` (VARCHAR2)：计划名称 / 全称
2. **分类与地区**：
   - `VC_TYPE_DETAIL` (VARCHAR2)：计划类型明细（职业年金为 `'ZYNJ'`）
   - `VC_PLAN_TYPE` (VARCHAR2)：计划类型描述（含权、固收）
   - `VC_AREA` (VARCHAR2)：省份
3. **生命周期与托管**：
   - `D_CREATE_DATE` / `D_ESTABLISH_DATE` (TIMESTAMP)：成立日期
   - `D_END_DATE` (TIMESTAMP, DEFAULT `2999-12-31`)：终止日期
   - `VC_BANK` (VARCHAR2)：托管银行

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT VC_PLAN_CODE, VC_PLAN_LIC_ID, VC_PLAN_NAME, VC_TYPE_DETAIL, D_CREATE_DATE FROM DD_DW.MDIM_PLAN_INFO WHERE ROWNUM <= 5`
- **探查结果**:
  | VC_PLAN_CODE | VC_PLAN_LIC_ID | VC_PLAN_NAME | VC_TYPE_DETAIL | D_CREATE_DATE |
  |---|---|---|---|---|
  *(0 rows)*

## 5. 上下游关联与常用 JOIN
- **下游组合表**：与 `DD_DW.MDIM_FUND_INFO` 关联。
- **候选 JOIN 条件**：`MDIM_PLAN_INFO.VC_PLAN_LIC_ID = MDIM_FUND_INFO.VC_PLAN_CODE`
- **职年过滤条件**：`WHERE VC_TYPE_DETAIL = 'ZYNJ'`

## 6. 未确认问题
- 详见 [`OQ-001`](../99-Inbox/Open-Questions.md#oq-001)：数据库中 `VC_PLAN_LIC_ID` 是否有显式 FOREIGN KEY。
