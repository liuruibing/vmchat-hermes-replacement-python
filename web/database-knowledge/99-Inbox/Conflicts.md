---
type: inbox
domain: 职年计划投资业绩
name: 证据冲突登记簿
status: conflicted
confidence: 5
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段4与阶段5
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: 阶段5陷阱
related_tables:
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - DW_ZNST_INDEX_NEW.F_PLAN_DYIELD_BZ_TCZ
last_verified: 2026-08-19
---

# 证据冲突登记簿 (Conflicts Registry)

本文档登记知识库构建过程中发现的矛盾证据（例如：数据库建表注释 vs 存储过程实际代码逻辑、企年算法 vs 职年算法）。根据规范，**严禁修改或删除种子结论以强行“消除”冲突**，必须同时记录双方观点、证据来源、发现日期及影响分析。

---

## 冲突登记列表

### CONF-001: TCZ 规则定义冲突（建表注释“剔除支付组合” vs 源码逻辑“剔除太平养老组合”）
- **发现日期**：2026-08-19
- **冲突焦点**：TCZ 缩写的实际业务含义与过滤代码
- **证据 A（E3 建表注释 / 缩写）**：
  - 来源：`MPRF_F_PLAN_DAYNETVALUE` 字段 `F_PLAN_DYIELD_BZ_TCZ` 建表注释及早期文档。
  - 内容：描述为“剔除支付组合收益率”（Excluding Payment Portfolio）。
- **证据 B（E2 存储过程源码）**：
  - 来源：`DW_ZNST_INDEX_NEW.F_PLAN_DYIELD_BZ_TCZ` 存储过程代码。
  - 内容：实际过滤条件为 `MDIM_FUND_INFO.VC_NAME_GLR LIKE '太平养老保险股份有限公司%'`，即剔除投资管理人为太平养老的组合。
- **现状与处理意见**：在 `07-Rules/TCZ-剔除太平养老管理组合.md` 中将规则状态标记为 `conflicted`，保留建表注释与源码逻辑两种说法，计算和业务理解以 E2 源码逻辑为准。

---

### CONF-002: 企年 TCZ 错调未剔除函数 Bug
- **发现日期**：2026-08-19
- **冲突焦点**：企业年金存储过程计算 `F_DP_YIELD_BZ_TCZ` 时未生效剔除
- **证据 A（E1 需求定义）**：
  - 来源：`outputs/taiping_pension_learning_roadmap.md` 阶段 5 历史陷阱 1。
  - 内容：企业年金计算 TCZ 收益率时要求剔除太平养老管理组合。
- **证据 B（E2 企年历史代码）**：
  - 来源：企年计算存储过程。
  - 内容：错误调用了未剔除 TCZ 的函数 `F_PLAN_DYIELD_BZ`，导致企年导出的 TCZ 收益率与普通收益率完全一致。
- **现状与处理意见**：职业年金存储过程已修正该调用，企业年金历史数据需保留此 Bug 记录。

---

### CONF-003: 企年净值 TCZ / TCB 硬编码覆盖
- **发现日期**：2026-08-19
- **冲突焦点**：`F_NETVALUE_TCZ` 与 `F_NETVALUE_TCB` 是否单独重算净值
- **证据 A（E1 业务期望）**：
  - 来源：资产净值剔除逻辑说明。
  - 内容：期望在剔除支付或保留账户后重新汇总剩余组合的净值。
- **证据 B（E2 代码实现）**：
  - 来源：企年 DW 加工过程。
  - 内容：源码中直接硬编码赋值 `F_NETVALUE_TCZ := F_NETVALUE` 及 `F_NETVALUE_TCB := F_NETVALUE`。
- **现状与处理意见**：标记为源码历史特性，在相关表卡片与规则卡片中说明。

---

### CONF-004: 职年计划 1105 特殊日期收益率硬编码
- **发现日期**：2026-08-19
- **冲突焦点**：计划 1105 在 2019-08-02 与 2019-08-03 的收益率计算规则
- **证据 A（通用现金流公式）**：
  - 来源：`DW_ZNST_INDEX_NEW.F_PLAN_DYIELD_BZ` 标准公式。
  - 内容：应根据当天净值、上一日净值及 IN/OUT 流水计算。
- **证据 B（特例补丁代码）**：
  - 来源：`DW_ZNST_INDEX_NEW` 过程中的 IF 补丁逻辑。
  - 内容：强制改写 2019-08-02 的收益率为 `0`，2019-08-03 的收益率为 `0.000007967`。
- **现状与处理意见**：特例硬编码记录在 `07-Rules/` 和表卡片中，不作为通用收益率公式推广。
