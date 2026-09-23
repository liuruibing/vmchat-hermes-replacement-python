---
type: rule
domain: 职年计划投资业绩
name: 业绩报酬-BP换算
status: confirmed
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段4剔除与报酬篇
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: BP基点换算
  - path: 09-Evidence/sql/2026-08-19__dw_procedures__sql.md
    level: E2
    location: F_PLAN_YJYX
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - F_PLAN_YJYX
last_verified: 2026-08-19
---

# 业务规则：业绩报酬 BP 换算

## 1. 规则标准文本描述
- 业绩报酬影响率在计算层面为万分比小数，为了方便金融业务展示，在 SQL 展示层必须统一乘以 **10000** 转换为 **BP (Basis Point 基点)**。

## 2. 算例与公式
- **比例公式**：$\text{日影响率} = \frac{\text{STBC} + \text{TGBC}}{\text{前一日资产净值}}$
- **BP 转化公式**：$\text{展示值 (BP)} = \text{日影响率} \times 10000$
- **手算例 (E1 通关例)**：
  - 前一日资产净值 20 亿元 ($2,000,000,000$)
  - 受托报酬 $STBC = 40,000$ 元，投管报酬 $TGBC = 160,000$ 元，总额 $200,000$ 元
  - 影响率 $= 200,000 / 2,000,000,000 = 0.00010$
  - 展示值 $= 0.00010 \times 10000 = \mathbf{1.00\text{ BP}}$
