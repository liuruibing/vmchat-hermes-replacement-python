---
type: rule
domain: 职年计划投资业绩
name: TCB-剔除保留账户
status: confirmed
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段4剔除与报酬篇
  - path: 09-Evidence/schema/2026-08-19__10_tables__schema.md
    level: E3
    location: MPRF_F_PLAN_DAYNETVALUE
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 业务规则：TCB 剔除保留账户

## 1. 规则标准文本描述
- 在计算 TCB 口径业绩时，排除账户类型为保留账户的年金组合，仅统计正常运营缴费的年金组合。

## 2. 关联字段与结果表达
- **关联表/字段**：`MDIM_FUND_INFO` 账户分类标志
- **大宽表输出字段**：`F_NETVALUE_TCB`（剔除保留账户资产净值）、`F_DP_YIELD_BZ_TCB`（剔除保留账户日收益率）

## 3. 企年源码特例提示
- 企业年金存储过程存在硬编码 `F_NETVALUE_TCB := F_NETVALUE` 覆盖情况（详见 [`CONF-003`](../99-Inbox/Conflicts.md#conf-003)）。
