---
type: evidence
domain: 职年计划投资业绩
name: DBX元数据-首批10张表显式约束描述
status: supported
confidence: 5
sources:
  - path: DD_DW.ALL_CONSTRAINTS
    level: E3
    location: dbx_execute_query
related_tables:
  - MDIM_PLAN_INFO
  - MDIM_FUND_INFO
  - MFACTGZ_FUND_HLDTOTAL
  - MFACTGZ_FUND_ASSETINOUT
  - MPRF_F_PLAN_DAYNETVALUE
  - MPRF_PTYPE_DYIELD
  - MDIM_SYS_TIME
  - MFACTGZ_FUND_HLDDETAIL
  - MMON_F_RISK_INDICATORS
  - MDIM_FUND_LASTDATE
related_functions: []
last_verified: 2026-08-19
---

# DBX 原始元数据证据：首批 10 张表显式约束 (PK / FK / UNIQUE) 查询结果

- **执行日期**：2026-08-19
- **数据库连接**：`DD_AODS` (Dameng 达梦)
- **工具调用**：`dbx_execute_query`
- **执行 SQL**：
  ```sql
  SELECT c.TABLE_NAME, c.CONSTRAINT_NAME, c.CONSTRAINT_TYPE, cc.COLUMN_NAME
  FROM ALL_CONSTRAINTS c
  JOIN ALL_CONS_COLUMNS cc ON c.OWNER = cc.OWNER AND c.CONSTRAINT_NAME = cc.CONSTRAINT_NAME
  WHERE c.OWNER = 'DD_DW' AND c.TABLE_NAME IN (
    'MDIM_PLAN_INFO', 'MDIM_FUND_INFO', 'MFACTGZ_FUND_HLDTOTAL', 
    'MFACTGZ_FUND_ASSETINOUT', 'MPRF_F_PLAN_DAYNETVALUE', 'MPRF_PTYPE_DYIELD', 
    'MDIM_SYS_TIME', 'MFACTGZ_FUND_HLDDETAIL', 'MMON_F_RISK_INDICATORS', 'MDIM_FUND_LASTDATE'
  )
  ORDER BY c.TABLE_NAME, c.CONSTRAINT_NAME, cc.POSITION
  ```
- **证据级别**：**E3** (数据库底层显式约束元数据)

---

## 查询返回结果 (Verbatim Output)

| TABLE_NAME | CONSTRAINT_NAME | CONSTRAINT_TYPE | COLUMN_NAME |
|---|---|---|---|
| MPRF_F_PLAN_DAYNETVALUE | PK_PD | P | VC_PLANCODE |
| MPRF_F_PLAN_DAYNETVALUE | PK_PD | P | D_DATE |

---

## 结论分析与审计判定 (E3 结论)
1. **唯一显式主键**：仅 `DD_DW.MPRF_F_PLAN_DAYNETVALUE` 存在显式数据库 PRIMARY KEY 约束 `PK_PD`，作用于联合字段 `(VC_PLANCODE, D_DATE)`。
2. **其余 9 张表约束现状**：`MDIM_PLAN_INFO`、`MDIM_FUND_INFO`、`MFACTGZ_FUND_HLDTOTAL`、`MFACTGZ_FUND_ASSETINOUT`、`MPRF_PTYPE_DYIELD`、`MDIM_SYS_TIME`、`MFACTGZ_FUND_HLDDETAIL`、`MMON_F_RISK_INDICATORS`、`MDIM_FUND_LASTDATE` 在数据库层面**均无显式 PK、FK 或 UNIQUE 约束**。
3. **表卡规范约束**：所有表卡片必须严格按照此 E3 元数据区分“显式数据库约束”与“业务逻辑/SQL 支持的候选关联键”，严禁将 NOT NULL 或列名相似性擅自升级为数据库约束事实。
