---
type: rule
domain: 职年计划投资业绩
name: TCG-剔除归集户利息
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
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 业务规则：TCG 剔除归集户利息

## 1. 规则标准文本描述
- 在计算纯投资收益率时，从净收益额中扣除归集户未拨付资金在银行产生的存款利息收入（`F_GJHLX_IN`），避免将归集户利息混入二级市场投资回报。

## 2. 影响字段与表达式
- **净收益额**：`F_INCOME_TCG = F_INCOME - F_GJHLX_IN`
- **大宽表输出字段**：`F_DP_YIELD_BZ_TCG` (剔除利息日收益率), `F_DP_YIELD_BZ_TCGZ` (剔除利息+剔除太平)
