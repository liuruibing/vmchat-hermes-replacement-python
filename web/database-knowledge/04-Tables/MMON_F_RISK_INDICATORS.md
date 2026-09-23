---
type: table
domain: 职年计划投资业绩
name: MMON_F_RISK_INDICATORS
status: supported
confidence: 4
sources:
  - path: DD_DW.MMON_F_RISK_INDICATORS
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - PKG_DW_OPERATION.F_RISK_NONERISK
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MMON_F_RISK_INDICATORS` (风险指标统计表)

## 1. 一句话定义与数据粒度
- **一句话定义**：保存计划与组合在不同时间窗口（本月、本年、成立以来）下波动率、最大回撤、夏普比率及下行风险计算结果的统计表。
- **数据粒度**：一个计划/组合在某一统计日期（`D_DATE + VC_PLANCODE / VC_FUNDCODE`）的一条风控记录。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **候选逻辑键**：`D_DATE`, `VC_PLANCODE`, `VC_FUNDCODE`

## 3. 核心字段分组
1. **身份与日期**：
   - `D_DATE` (TIMESTAMP), `VC_PLANCODE`, `VC_FUNDCODE`, `VC_PTYPE` (计划类型)
2. **本月风控指标**：
   - `F_MVIX` (月度波动率), `F_MMAXDRAW_DAY` (月度最大回撤-14号文), `F_MSHARP` (夏普比率), `F_MVIX_DESC` (下行风险)
3. **本年与成立以来风控指标**：
   - `F_YVIX` / `F_CVIX` (本年/成立以来波动率)
   - `F_YMAXDRAW_DAY` / `F_CMAXDRAW_DAY` (本年/成立以来最大回撤)
   - `F_YSHARP` / `F_CSHARP` (夏普比率)
4. **剔除归集户利息口径 (TCG)**：
   - `F_MVIX_TCG`, `F_MMAXDRAW_DAY_TCG`, `F_MSHARP_TCG`, `F_MVIX_DESC_TCG`

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT D_DATE, VC_PLANCODE, F_MVIX, F_MMAXDRAW_DAY, F_MSHARP FROM DD_DW.MMON_F_RISK_INDICATORS WHERE ROWNUM <= 5`
- **探查结果**:
  | D_DATE | VC_PLANCODE | F_MVIX | F_MMAXDRAW_DAY | F_MSHARP |
  |---|---|---|---|---|
  *(0 rows)*

## 5. 上下游关联
- 由存储过程根据大宽表 `MPRF_F_PLAN_DAYNETVALUE` 在月末/年末或夜间定时加工计算落盘。

## 6. 待确认问题
- 详见 [`OQ-003`](../99-Inbox/Open-Questions.md#oq-003)：夜间加工 `MMON_F_RISK_INDICATORS` 的存储过程源码细节与触发时间。
