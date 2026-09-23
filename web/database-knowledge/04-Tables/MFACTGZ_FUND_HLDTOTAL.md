---
type: table
domain: 职年计划投资业绩
name: MFACTGZ_FUND_HLDTOTAL
status: supported
confidence: 4
sources:
  - path: DD_DW.MFACTGZ_FUND_HLDTOTAL
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

# 表画像：`DD_DW.MFACTGZ_FUND_HLDTOTAL` (估值持仓总表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录各个投资组合每日核算科目（如 701A 资产净值、702A 单位净值、601A 实收资本）金额与市值的底层贴源表。
- **数据粒度**：一个组合在某一核算日期的某一个核算科目（`VC_FUNDCODE + D_DATE + VC_SUBCODE`）。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **非空列**：`F_ID` (NUMBER, NOT NULL), `D_DATE` (TIMESTAMP, NOT NULL), `VC_FUNDCODE` (VARCHAR2(20), NOT NULL), `VC_SUBCODE` (VARCHAR2(20), NOT NULL)
- **候选联合逻辑键**：`VC_FUNDCODE + D_DATE + VC_SUBCODE`

## 3. 核心字段分组
1. **核算标识与时间**：
   - `F_ID` (NUMBER)：主键 ID
   - `D_DATE` (TIMESTAMP)：核算日期
   - `VC_FUNDCODE` (VARCHAR2)：组合代码
2. **科目与金额**：
   - `VC_SUBCODE` (VARCHAR2)：科目代码（**`'701A'` = 资产净值**, **`'702A'` = 单位净值**, `'601A'` = 实收资本）
   - `VC_SUBNAME` (VARCHAR2)：科目名称
   - `F_PRICE` (NUMBER)：本位币市值/总额
3. **审计与状态**：
   - `VC_DELETE` (VARCHAR2)：删除与来源标志（`'QT'` 体外组合，空表示本地估值组合）

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, VC_FUNDCODE, VC_SUBCODE, VC_SUBNAME, F_PRICE FROM DD_DW.MFACTGZ_FUND_HLDTOTAL WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | VC_FUNDCODE | VC_SUBCODE | VC_SUBNAME | F_PRICE |
  |---|---|---|---|---|
  | 2025-01-01 | TQ001601 | 701A | 资产净值 | 26009869.95 |
  | 2025-01-01 | TQ001601 | 702A | 单位净值 | 0.999995 |

## 5. 上下游关联
- 上游：估值系统每日推送数据。
- 下游：由存储过程汇总提取 `701A` 与 `702A` 写入大宽表 `MPRF_F_PLAN_DAYNETVALUE`。
