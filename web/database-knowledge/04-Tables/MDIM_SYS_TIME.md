---
type: table
domain: 职年计划投资业绩
name: MDIM_SYS_TIME
status: supported
confidence: 5
sources:
  - path: DD_DW.MDIM_SYS_TIME
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - DW_ZNST_INDEX_ADD.F_PLAN_YIELD_TBZ
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MDIM_SYS_TIME` (系统时间维表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录自然日历、节假日标识及交易日前后偏移量的系统基础时间维表。
- **数据粒度**：一个自然日（`D_DATE`）对应一行。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **候选逻辑键**：`D_DATE`

## 3. 核心字段分组
1. **日期主键与年月日**：
   - `D_DATE` (TIMESTAMP)：业务发生日
   - `F_YEAR` / `F_MONTH` / `F_DAY` (NUMBER)：年、月、日
2. **交易日标识与偏移（核心）**：
   - `F_HOLS_DAY` (NUMBER)：假期标志位（E3 注释：`0` 节假日 / `1` 工作日；注意：逻辑中作为交易日过滤器）
   - `D_PREV_DATE` (TIMESTAMP)：前一工作日
   - `D_NEXT_DATE` (TIMESTAMP)：下一工作日
   - `F_LAST_TRADING_DAY_W` / `F_LAST_TRADING_DAY_M` (NUMBER)：是否周/月最后一个交易日 (1是 0否)

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, F_YEAR, F_MONTH, F_DAY, F_HOLS_DAY, D_PREV_DATE FROM DD_DW.MDIM_SYS_TIME WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | F_YEAR | F_MONTH | F_DAY | F_HOLS_DAY | D_PREV_DATE |
  |---|---|---|---|---|---|
  | 2015-11-07 | 2015 | 11 | 7 | 0 | 2015-11-06 |
  | 2015-11-09 | 2015 | 11 | 9 | 1 | 2015-11-06 |

## 5. 上下游关联
- 收益率连乘过程 `DW_ZNST_INDEX_ADD.F_PLAN_YIELD_TBZ` 依靠此表过滤交易日及确定上一交易日净值。
