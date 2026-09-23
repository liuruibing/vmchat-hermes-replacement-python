---
type: inbox
domain: 职年计划投资业绩
name: 待确认问题登记簿
status: open
confidence: 3
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段1-5
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: 自测题与陷阱
  - path: 09-Evidence/sql/2026-08-19__dw_procedures__sql.md
    level: E2
    location: F_PLAN_DYIELD_BZ_ZYNJ
related_tables:
  - MDIM_PLAN_INFO
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - F_PLAN_DYIELD_BZ_ZYNJ
last_verified: 2026-08-19
---

# 待确认问题登记簿 (Open Questions)

本文档归集所有无法由当前 E1（业务文档）、E2（代码源码）、E3（元数据）或 E4（数据探查）完全关闭的疑点与待验证事项。任何未经完全证实的假设不得写为既定事实。

---

## 登记事项清单

### OQ-001: `VC_PLAN_LIC_ID` 与 `VC_PLAN_CODE` 是否存在显式外键约束？
- **发现日期**：2026-08-19
- **关联对象**：`MDIM_PLAN_INFO`, `MDIM_FUND_INFO`
- **关联字段**：`MDIM_PLAN_INFO.VC_PLAN_LIC_ID`, `MDIM_FUND_INFO.VC_PLAN_CODE`
- **当前证据与现状**：E1 种子文档指出两者用于关联计划与组合，但数据库中是否存在显式 FOREIGN KEY 约束需在 DBX `dbx_describe_table` 中验证。
- **需要人工 / DBX 验证内容**：在 DM 数据库中查询两表的主外键与约束元数据（E3 已验证无显式外键）。

### OQ-002: 大宽表 21 个未赋值字段的后续处理规划
- **发现日期**：2026-08-19
- **关联对象**：`MPRF_F_PLAN_DAYNETVALUE`
- **关联字段**：久期 `F_MODDURATION_*`、本年/成立以来基准收益等 21 个字段
- **当前证据与现状**：E1 种子文档指出该 21 个字段在存储过程加工中完全未被赋值（查询恒为 NULL）。
- **需要人工 / DBX 验证内容**：确认这些字段是历史遗留无用列，还是有后续新的 ETL 计划补充。

### OQ-003: 风险指标（波动率、夏普比率、最大回撤）具体存储过程源码位置
- **发现日期**：2026-08-19
- **关联表/对象**：`MMON_F_RISK_INDICATORS`, 前端查询 SQL
- **当前证据与现状**：E1/E2 明确了前端 SQL 会对加权日收益序列求 `STDDEV() * SQRT(250)`，但夜间 DW 是否存在单独的风险指标统计存储过程包需进一步探查。
- **需要人工 / DBX 验证内容**：探查 `PKG_DW_OPERATION` 或相关风险过程源码。

### OQ-004: 组合投资类型 `VC_PRODUCT_INVESTMENT_TYPE` 字典映射表
- **发现日期**：2026-08-19
- **关联对象**：`MDIM_FUND_INFO`
- **关联字段**：`VC_PRODUCT_INVESTMENT_TYPE`, `VC_TYPE_IN`
- **当前证据与现状**：E4 探查可获得该枚举值的分布，但具体代码含义（如 `'1'` 代表股票型还是混合型）尚无 E1/E2 字典表对应。
- **需要人工 / DBX 验证内容**：寻找系统字典维表或存储过程中的 CASE WHEN 映射逻辑。

### OQ-005: 单计划级别 (`VC_PLANCODE`) 宽表日收益率落盘过程源码验证
- **发现日期**：2026-08-19
- **关联对象**：`MPRF_F_PLAN_DAYNETVALUE`
- **关联字段**：`F_DP_YIELD_BZ`
- **关联函数**：`F_PLAN_DYIELD_BZ_ZYNJ` (E2) vs `P_MPRF_F_PLAN_DAYNETVAL`
- **当前证据与现状**：已导出 E2 源码 `F_PLAN_DYIELD_BZ_ZYNJ` 仅接收 `I_DATE` 计算职年整体日收益率；单计划级别 (`VC_PLANCODE`) 在 `MPRF_F_PLAN_DAYNETVALUE` 表中的逐计划清洗落盘存储过程源码待导出验证。
- **需要人工 / DBX 验证内容**：探查 `P_MPRF_F_PLAN_DAYNETVAL` 或包体中的单计划游标循环落盘代码。
