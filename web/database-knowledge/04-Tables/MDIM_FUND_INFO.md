---
type: table
domain: 职年计划投资业绩
name: MDIM_FUND_INFO
status: supported
confidence: 4
sources:
  - path: DD_DW.MDIM_FUND_INFO
    level: E3
    location: dbx_describe_table
  - path: 09-Evidence/samples/2026-08-19__10_tables__samples.md
    level: E4
    location: dbx_execute_query
related_tables:
  - MDIM_PLAN_INFO
  - MFACTGZ_FUND_HLDTOTAL
related_functions: []
last_verified: 2026-08-19
---

# 表画像：`DD_DW.MDIM_FUND_INFO` (投资组合维表)

## 1. 一句话定义与数据粒度
- **一句话定义**：记录具体投资组合（专柜）基本属性、管理托管主体、估值配置及所属计划映射的维表。
- **数据粒度**：一行代表一个独立的投资组合（套帐/产品）。

## 2. 数据库约束 (E3 元数据)
- **显式约束**：无显式 PK、FK 或 UNIQUE 约束（由 E3 `ALL_CONSTRAINTS` 查询验证）。
- **非空列**：`VC_FUNDCODE` (VARCHAR2(50), NOT NULL)
- **候选主键粒度**：`VC_FUNDCODE`

## 3. 七组核心字段拆解 (首轮核心与按需)

1. **身份与名称**：
   - 首轮核心：`VC_FUNDCODE` (产品代码), `VC_FUNDNAME` (产品名称), `VC_SHORT_FUNDNAME` (简称)
   - 按需：`VC_STBY_CODE` (辅助代码), `VC_SHORTNAME`
2. **计划归属候选**：
   - 首轮核心：`VC_PLAN_CODE` (计划代码), `VC_PLAN_NAME` (计划名称)
   - 按需：`VC_PLANCODE` (计划登记号)
3. **生命周期与分类**：
   - 首轮核心：`D_CREATE_DATE` (成立日), `D_END_DATE` (到期日), `VC_TYPE_IN` (产品类型: 2年金 7传统 8投连 16养老金), `VC_PRODUCT_INVESTMENT_TYPE` (产品投资类型)
   - 分布探查 SQL (`WHERE ROWNUM <= 20`): `SELECT VC_PRODUCT_INVESTMENT_TYPE, COUNT(*) AS CNT FROM DD_DW.MDIM_FUND_INFO WHERE ROWNUM <= 20 GROUP BY VC_PRODUCT_INVESTMENT_TYPE ORDER BY CNT DESC`
   - 探查结果：实测 `VC_PRODUCT_INVESTMENT_TYPE` 为 NULL，注释映射: 1混合 2股票 3货币 4固收 5信托 6债权 7存款 8银行理财 9保险 11债基 12债券 19其他。无显式映射时仅保留原始值。
   - 按需：`D_BEGIN_DATE`, `VC_IS_END`
4. **管理与托管**：
   - 首轮核心：`VC_NAME_GLR` (投资管理人名称), `VC_NAME_TGR` (托管人名称), `F_SET_AMOUNT` (初始设立金额)
   - 按需：`VC_FUND_MANAGE` (投资经理), `VC_NAME_WTR` (委托人)
5. **费率与估值配置**：
   - 首轮核心：`F_GLF_RATIO` (管理费率 %), `VC_GZ_FREQUENCY` (估值频率: 0日估 1周估 2月估), `VC_YIELD_METHOD` (净值算法)
   - 按需：`VC_PERFORMANCE_FEE` (业绩报酬 %), `VC_PERFORMANCE_JT`
6. **外部系统映射**：
   - 按需：`VC_TADATA_ID` (TA系统ID), `VC_TRADE_CODE` (恒生代码), `VC_ALTERNATIVE_CODE` (另类代码)
7. **ETL 审计与状态**：
   - 首轮核心：`F_IFEFFECTED` (是否有效: 1有效 0无效), `D_ETL_CREATEDATE` (抽取时间), `D_ETL_UPDATEDATE` (更新时间)

## 4. 脱敏样例数据 (E4)
- **探查 SQL**: `SELECT VC_FUNDCODE, VC_PLAN_CODE, VC_FUNDNAME, VC_NAME_GLR, VC_PRODUCT_INVESTMENT_TYPE, F_SET_AMOUNT FROM DD_DW.MDIM_FUND_INFO WHERE ROWNUM <= 5`
- **探查结果**:
  | VC_FUNDCODE | VC_PLAN_CODE | VC_FUNDNAME | VC_NAME_GLR | F_SET_AMOUNT |
  |---|---|---|---|---|
  | TZ000001 | ZP0001 | 测试职年组合000001 | 测试投资管理人01 | 10010000.00 |
  | TZ000002 | ZP0001 | 测试职年组合000002 | 测试投资管理人02 | 10020000.00 |

## 5. 上下游关联与过滤规则
- **TCZ 规则过滤**：`VC_NAME_GLR LIKE '太平养老保险股份有限公司%'`
- **上游关联计划**：`MDIM_FUND_INFO.VC_PLAN_CODE = MDIM_PLAN_INFO.VC_PLAN_LIC_ID`

## 6. 待确认问题
- 详见 [`OQ-004`](../99-Inbox/Open-Questions.md#oq-004)：`VC_PRODUCT_INVESTMENT_TYPE` 在代码中的具体映射逻辑。
