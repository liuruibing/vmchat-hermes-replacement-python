---
type: overview
domain: 职年计划投资业绩
name: Schema地图
status: confirmed
confidence: 4
sources:
  - path: outputs/taiping_pension_learning_roadmap.md
    level: E1
    location: 阶段1与阶段2
  - path: outputs/taiping-pension-field-cleaning-learning-guide.html
    level: E1
    location: 流向架构图
related_tables:
  - MDIM_PLAN_INFO
  - MDIM_FUND_INFO
  - MPRF_F_PLAN_DAYNETVALUE
related_functions: []
last_verified: 2026-08-19
---

# 数据库 Schema 架构地图 (Schema Map)

本文档整理达梦数据库（DM）中实测可见的 Schema 及其分层关系与业务职责。

---

## 1. 实测 Schema 分布与层级职责

根据 DBX 接口及 SQL 源码探查，目前可见的 Schema 如下：

| Schema / 模式名称 | 数仓层级定位 | 证据等级 | 职责与主要存储内容 | 已验证核心表举例 |
|---|---|---|---|---|
| **`DD_DW`** | 数据仓库层 (Data Warehouse) | **E1/E2** | 存放洗净的维度表、事实表及指标汇总大宽表；运行 `DW_ZNST_INDEX_NEW` 等存储过程包 | `MDIM_PLAN_INFO`, `MDIM_FUND_INFO`, `MPRF_F_PLAN_DAYNETVALUE` |
| **`DD_AODS`** | 贴源数据层 (Active ODS) | **E2/E3** | 存放估值系统同步的原始日终核算数据与流水 | `MFACTGZ_FUND_HLDTOTAL`, `MFACTGZ_FUND_ASSETINOUT`, `MFACTGZ_FUND_HLDDETAIL` |
| **`DD_SODS`** | 阶段/历史贴源层 (Staging ODS) | **I** | *(推断)* 存放历史快照或接口缓冲区数据，暂未被 SQL 源码直接证明 | *(待探查)* |
| **`DD_ETL`** | 数据清洗与转换过程模式 | **I** | *(推断)* 存放 ETL 作业控制表、清洗临时表与调优脚本 | *(待探查)* |
| **`DD_PORTAL`** | 前端门户/应用展示层 | **I** | *(推断)* 存放报表配置、查询视图或缓存表 | *(待探查)* |
| **`SYSDBA`** | 系统管理员模式 | **E3** | 达梦数据库默认管理员模式，包含数据字典与系统表 | `SYS.SYSOBJECTS`, `ALL_CONSTRAINTS` |

---

## 2. 数据流动与加工链路概览

根据种子文档 `EVID-DOC-001` 及 HTML 架构图 `EVID-DOC-002`，基础流动路径如下：

```text
[ 估值系统原始核算 ]
      │
      ▼ (ODS 同步)
 [ DD_AODS 贴源表 ]
   ├── MFACTGZ_FUND_HLDTOTAL (701A / 702A)
   ├── MFACTGZ_FUND_ASSETINOUT (IN / OUT)
   └── MFACTGZ_FUND_HLDDETAIL (221002 / 220602)
      │
      ▼ (夜间 DW 存储过程包: DD_DW.DW_ZNST_INDEX_NEW)
 [ DD_DW 数据仓库层 ]
   ├── MDIM_PLAN_INFO (计划维表)
   ├── MDIM_FUND_INFO (组合维表)
   └── MPRF_F_PLAN_DAYNETVALUE (计划日净值大宽表)
      │
      ▼ (前端 SQL 实时 UNION ALL 加权)
 [ 职年计划投资业绩查询报表 ]
```

---

## 3. 注意事项与推断边界

1. **未证实关系的标注**：`DD_SODS`、`DD_ETL`、`DD_PORTAL` 的职责仅由 Schema 命名惯例得出（标记 **I**），不得视为既定数仓事实。
2. **跨 Schema 访问**：在 SQL 查询与存储过程中，必须使用完整的 `SCHEMA.TABLE_NAME` 显式限定引用（如 `DD_DW.MDIM_PLAN_INFO`）。
