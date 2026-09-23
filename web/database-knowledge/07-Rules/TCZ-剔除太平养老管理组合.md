---
type: rule
domain: 职年计划投资业绩
name: TCZ-剔除太平养老管理组合
status: conflicted
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段4剔除与报酬篇
  - path: 09-Evidence/sql/2026-08-19__dw_procedures__sql.md
    level: E2
    location: F_PLAN_DYIELD_BZ_ZYNJ
  - path: 99-Inbox/Conflicts.md
    level: E1
    location: CONF-001
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - F_PLAN_DYIELD_BZ_ZYNJ
last_verified: 2026-08-19
---

# 业务规则：TCZ 剔除太平养老管理组合

## 1. 规则标准文本描述
- 在计算职业年金剔除口径收益率时，排除所有投资管理人为“太平养老保险股份有限公司”的组合，仅统计外部受托/投管组合的业绩。

## 2. 核心代码过滤条件 (E2 确认)
```sql
-- 过滤代码逻辑 (F_PLAN_DYIELD_BZ_ZYNJ 源码)
WHERE MDIM_FUND_INFO.VC_NAME_GLR LIKE '太平养老保险股份有限公司%'
```

## 3. 证据冲突与历史 Bug 说明 (E1 / E2 冲突)
1. **缩写冲突**：建表注释/早期字段描述称为“剔除支付组合”（Excluding Payment Portfolio），但 PL/SQL 代码中实际为“剔除太平养老组合”（详见 [`CONF-001`](../99-Inbox/Conflicts.md#conf-001)）。
2. **企年错调 Bug**：企业年金计算 TCZ 收益率时错调了未剔除函数，导致企年 TCZ 收益率等于普通收益率（详见 [`CONF-002`](../99-Inbox/Conflicts.md#conf-002)）。
