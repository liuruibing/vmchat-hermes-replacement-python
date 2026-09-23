---
type: evidence
domain: 职年计划投资业绩
name: DBX元数据-首批10张表结构描述
status: supported
confidence: 5
sources:
  - path: DD_DW.MDIM_PLAN_INFO
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MDIM_FUND_INFO
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MFACTGZ_FUND_HLDTOTAL
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MFACTGZ_FUND_ASSETINOUT
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MPRF_F_PLAN_DAYNETVALUE
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MPRF_PTYPE_DYIELD
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MDIM_SYS_TIME
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MFACTGZ_FUND_HLDDETAIL
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MMON_F_RISK_INDICATORS
    level: E3
    location: dbx_describe_table
  - path: DD_DW.MDIM_FUND_LASTDATE
    level: E3
    location: dbx_describe_table
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

# DBX 原始元数据证据：首批 10 张核心表 Schema (E3 原始返回)

- **执行日期**：2026-08-19
- **数据库连接**：`DD_AODS` (Dameng 达梦 192.168.1.206:5236)
- **工具调用**：`dbx_describe_table`
- **证据级别**：**E3** (数据库元数据与系统列注释，不包含任何外部业务推理)

---

## `DD_DW.MDIM_PLAN_INFO`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| VC_PLAN_CODE | VARCHAR2(50 BYTE) | NO |  | 计划代码 |
| VC_BANK | VARCHAR2(200 BYTE) | YES |  | 托管行 |
| VC_PLAN_NAME | VARCHAR2(100 BYTE) | YES |  | 计划名称 |
| VC_AREA | VARCHAR2(100 BYTE) | YES |  | 省份 |
| VC_PLAN_LIC_ID | VARCHAR2(50 BYTE) | YES |  | 年金计划登记号 |
| D_CREATE_DATE | TIMESTAMP | YES |  | 成立日期 |
| RPT_RANK | NUMBER | YES |  | 报告排序 |
| VC_PLAN_FNAME | VARCHAR2(100 BYTE) | YES |  | 计划全称 |
| D_ESTABLISH_DATE | TIMESTAMP | YES |  | 计划实际成立日 |
| D_END_DATE | TIMESTAMP | YES |  DATE'2999-12-31' |  |
| VC_TYPE_DETAIL | VARCHAR2(20 BYTE) | YES |  |  |
| VC_PLAN_FNAME1 | VARCHAR2(100 BYTE) | YES |  | 计划全称_BACK |
| VC_PLAN_TYPE | VARCHAR2(100 BYTE) | YES |  | 计划类型 （含权，固收） |

---

## `DD_DW.MDIM_FUND_INFO`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| VC_FUNDCODE | VARCHAR2(50 BYTE) | NO |  | 产品代码 |
| VC_STBY_CODE | VARCHAR2(200 BYTE) | YES |  | 辅助代码 |
| VC_FUNDNAME | VARCHAR2(100 BYTE) | YES |  | 产品名称 |
| VC_SHORT_FUNDNAME | VARCHAR2(100 BYTE) | YES |  | 产品简称 |
| VC_SHORTNAME | VARCHAR2(100 BYTE) | YES |  | 辅助名称 |
| VC_PLAN_NAME | VARCHAR2(500 BYTE) | YES |  | 计划名称 |
| VC_PLAN_CODE | VARCHAR2(50 BYTE) | YES |  | 计划代码 |
| D_CREATE_DATE | TIMESTAMP | YES |  | 成立日期 |
| VC_NAME_TGR | VARCHAR2(120 BYTE) | YES |  | 托管人名称 |
| VC_TYPE_DETAIL | VARCHAR2(100 BYTE) | YES |  | 产品投资类型 |
| D_EDATE | TIMESTAMP | YES |  | 产品到期日期 |
| VC_TYPE_IN | VARCHAR2(20 BYTE) | YES |  | 产品类型(2 企业年金和职业年金 7 传统险 8 投连险 15 保险理财产品 16 养老金产品 20 基本养老保险基金) |
| D_BEGIN_DATE | TIMESTAMP | YES |  | 合同起始日 |
| D_END_DATE | TIMESTAMP | YES |  | 合同终止日 |
| VC_PARTNT_CODE | VARCHAR2(50 BYTE) | YES |  | 父级产品代码 |
| VC_BE_CODE | VARCHAR2(500 BYTE) | YES |  | 基准编码 |
| F_SET_AMOUNT | NUMBER(22,8) | YES | 0. | 设立金额（成立日实收资本） |
| VC_INVEST_GOAL | VARCHAR2(1000 BYTE) | YES |  | 投资目标 |
| VC_INVEST_STRATEGY | VARCHAR2(4000 BYTE) | YES |  | 投资策略 |
| VC_RISK_CHARATER | VARCHAR2(1000 BYTE) | YES |  | 风险收益特征 |
| VC_ACCOUNTING_FIRM | VARCHAR2(1000 BYTE) | YES |  | 会计事务所 |
| VC_REGISTRANT_ORG | VARCHAR2(1000 BYTE) | YES |  | 注册登记机构 |
| VC_INVEST_STYLE | VARCHAR2(20 BYTE) | YES |  | 投资风格 |
| VC_IS_END | VARCHAR2(2 BYTE) | YES | 0 | 是否到期 |
| VC_FUND_MANAGE | NVARCHAR | YES |  | 投资经理人 (可显示多个) |
| VC_PRODUCER | VARCHAR2(30 BYTE) | YES |  | 报表制作人 |
| VC_PERSONINCHARGE | VARCHAR2(30 BYTE) | YES |  | 报表负责人 |
| VC_TEL | VARCHAR2(30 BYTE) | YES |  | 电话号码 |
| VC_FAX | VARCHAR2(50 BYTE) | YES |  | 邮箱 |
| VC_ADDRESS | VARCHAR2(100 BYTE) | YES |  | 地址 |
| VC_POSTCODE | VARCHAR2(10 BYTE) | YES |  | 邮编 |
| F_GLF_RATIO | NUMBER(20,6) | YES |  | 管理费率(%)(手动维护) |
| VC_YIELD_METHOD | VARCHAR2(10 BYTE) | YES |  | 净值增长率算法 |
| VC_IS_INNER | VARCHAR2(2 BYTE) | YES |  | 是否集团内账户 |
| VC_IS_OUTER | VARCHAR2(2 BYTE) | YES |  | 是否委外 |
| VC_REMARKS | VARCHAR2(200 BYTE) | YES |  | 备注 |
| VC_SOURCE | VARCHAR2(10 BYTE) | YES |  | 数据来源 |
| VC_QY_MANAGE | VARCHAR2(100 BYTE) | YES |  | 权益类投资经理 |
| VC_GS_MANAGE | VARCHAR2(100 BYTE) | YES |  | 固收类投资经理 |
| VC_FUNDNAME1 | VARCHAR2(100 BYTE) | YES |  | 一级账户 |
| VC_FUNDNAME2 | VARCHAR2(100 BYTE) | YES |  | 二级账户 |
| VC_NAME_GLR | VARCHAR2(120 BYTE) | YES |  | 管理人名称 |
| VC_NAME_WTR | VARCHAR2(120 BYTE) | YES |  | 委托人名称 |
| VC_TADATA_ID | VARCHAR2(20 BYTE) | YES |  | TA系统账户ID |
| VC_CLIENT_ID | VARCHAR2(20 BYTE) | YES |  | 客户ID |
| VC_TRADE_CODE | VARCHAR2(20 BYTE) | YES |  | 恒生账户代码 |
| VC_ALTERNATIVE_CODE | VARCHAR2(50 BYTE) | YES |  | 另类投资系统账户代码 |
| VC_INDEX | VARCHAR2(10 BYTE) | YES |  | 指数类型 |
| F_COMPANYID | NUMBER | YES |  | 机构代码 (sys_dept 中级别为1的部门为机构) |
| VC_HETONGHAO | VARCHAR2(100 BYTE) | YES |  | 合同号 |
| VC_CODE_GLR | VARCHAR2(100 BYTE) | YES |  | 管理人类型 |
| VC_FUND_TYPE | VARCHAR2(100 BYTE) | YES |  | 基金类型 |
| VC_STRUCTURED_TYPE | VARCHAR2(100 BYTE) | YES |  | 结构产品类型 |
| VC_MATCHING_RULE | VARCHAR2(1000 BYTE) | YES |  | 匹配规则 |
| F_COMPANY_NAME | VARCHAR2(100 BYTE) | YES |  | 机构名称 |
| VC_PRODUCT_INVESTMENT_TYPE | VARCHAR2(100 BYTE) | YES |  | 产品投资类型(1.混合型、2.股票型、3.货币型、 4.固收型、 5.信托型、6.债权计划型、7.存款型、8商业银行理财型 9保险产品型.10特定资产管理计划型 11债券基金型12债券型 19其他) |
| VC_SECOND_LEVEL_PRODUCT | VARCHAR2(100 BYTE) | YES |  | 二级产品 |
| VC_TEMPLATE_ID | VARCHAR2(100 BYTE) | YES |  | 估值表模板id |
| VC_GZ_FREQUENCY | VARCHAR2(10 BYTE) | YES |  | 估值频率:0日估值,1周估值,2月估值 |
| VC_IS_TIER | VARCHAR2(2 BYTE) | YES |  | 是否分级：1-分级，0-不分级; |
| VC_BASE_CURRENCY | VARCHAR2(10 BYTE) | YES |  | 基础货币,1-人民币，2-港币，3-美元，4-份，-1-其他 |
| VC_SUBSCRIPTION_FEE | NUMBER(20,6) | YES |  | 认购费(%) |
| VC_REDEMPTION_FEE | NUMBER(20,6) | YES |  | 赎回费(%) |
| VC_PERFORMANCE_FEE | NUMBER(20,6) | YES |  | 业绩报酬（%） |
| VC_HURDLE_RATE | NUMBER(20,6) | YES |  | Hurdle Rate（%） |
| VC_PERFORMANCE_JT | VARCHAR2(10 BYTE) | YES |  | 业绩报酬计提方式:0-未设 1-份额计提 2-净值计提 3-混合 |
| VC_SMPP_CODE | VARCHAR2(20 BYTE) | YES |  | 私募排排账号 |
| D_CREATETIME | TIMESTAMP | YES |  | 产品首次创建时间(有持仓数据首个日期) |
| D_UPDATETIME | TIMESTAMP | YES |  | 产品最新更新时间 |
| VC_SALES_CHANNELS | VARCHAR2(10 BYTE) | YES |  | 销售渠道：cs01-中金，cs02-中投，cs03-中金+中投，cs04-未销售  字典表 |
| VC_FOF_INVESTMENT | VARCHAR2(10 BYTE) | YES |  | FOF投资：0否；1是 |
| VC_IF_CLEAN | VARCHAR2(10 BYTE) | YES |  | 是否清盘 |
| VC_ADVISOR | VARCHAR2(100 BYTE) | YES |  | 投资顾问 |
| VC_DEPTID | NUMBER | YES |  | 部门代码(sys_dept 中级别为2的部门为部门) |
| VC_IS_OUTER_FUND | VARCHAR2(10 BYTE) | YES |  | 是否外部基金；0否1是；判断哪些是自己产品，哪些是外部导入 |
| F_IFEFFECTED | NUMBER | YES | 0 | 是否有效 |
| F_IFPUBLIC | NUMBER | YES |  | 是否公募 |
| D_RANKSTARTDATE | TIMESTAMP | YES |  | 考核起始日 |
| F_STRUPROPERTIES | NUMBER | YES |  | 产品结构属性 |
| VC_STRURATIODESC | VARCHAR2(500 BYTE) | YES |  | 结构化产品杠杆比例说明 |
| VC_INVESTTARGET | VARCHAR2(200 BYTE) | YES |  | 产品投资标的 |
| VC_IFMARGIN | CHAR(1 BYTE) | YES |  | 是否参与融资融券 |
| VC_COMPANY_NAME | VARCHAR2(50 BYTE) | YES |  | 所属投资部 |
| VC_CURRENCY_NO | CHAR(3 BYTE) | YES |  | 估值币种 |
| VC_FJJTGREN | VARCHAR2(100 BYTE) | YES |  | 托管行名称 |
| VC_ASSETTYPE | VARCHAR2(10 BYTE) | YES |  | 数据来源投研一体化 |
| VC_INVESTMANAGETYPE | VARCHAR2(10 BYTE) | YES |  | 数据来源投研一体化 |
| VC_INVESTASSETTYPE | VARCHAR2(10 BYTE) | YES |  | 数据来源投研一体化 |
| VC_BMDESC | VARCHAR2(200 BYTE) | YES |  | 数据来源投研一体化 |
| F_MAXEQUITY | NUMBER | YES |  | 权益上限 |
| VC_IFMERGEDCAL | CHAR(1 BYTE) | YES |  | 数据来源投研一体化 |
| VC_MAINTENFLAG | CHAR(1 BYTE) | YES |  | 数据来源投研一体化 |
| VC_IFEQUITYCAL | CHAR(1 BYTE) | YES |  | 数据来源投研一体化 |
| D_ETL_CREATEDATE | TIMESTAMP | YES |  | 数据抽取时间 |
| D_ETL_UPDATEBY | VARCHAR2(20 BYTE) | YES |  | 数据更新时间人 |
| D_ETL_CREATEBY | VARCHAR2(20 BYTE) | YES |  | 数据抽取人 |
| D_ETL_UPDATEDATE | TIMESTAMP | YES |  | 数据更新时间 |
| F_BELONGS_BRACE | NUMBER | YES |  | 所属支柱 |
| VC_ANNUITY_TYPE | VARCHAR2(20 BYTE) | YES |  | 年金类型 |
| VC_IFACOUNT | VARCHAR2(20 BYTE) | YES |  | 是否集合 0否1是 |
| VC_IFEQUITY | VARCHAR2(20 BYTE) | YES |  | 是否权益 0否1是 |
| VC_FUNDCODE_RECENTLY | VARCHAR2(100 BYTE) | YES |  | 最近曾用帐套代码 |
| F_MJJE | NUMBER(19,4) | YES |  | 募集金额 |
| F_MJFE | NUMBER(21,6) | YES |  | 募集份额 |
| VC_FJJLX | VARCHAR2(20 BYTE) | YES |  | 基金种类  |
| F_FUND_RANK | NUMBER | YES |  | 组合排名（供报告使用） |
| VC_PLANCODE | VARCHAR2(40 BYTE) | YES |  | 计划登记号 |
| VC_PLANNAME | VARCHAR2(500 BYTE) | YES |  |  |
| F_UNITVALUE | NUMBER(12,6) | YES |  | 期初单位净值(有持仓数据首个日期) |

---

## `DD_DW.MFACTGZ_FUND_HLDTOTAL`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| F_ID | NUMBER | NO |  | F_ID |
| D_DATE | TIMESTAMP | NO |  | 日期 |
| VC_FUNDCODE | VARCHAR2(20 BYTE) | NO |  | 产品代码 |
| VC_SUBCODE | VARCHAR2(20 BYTE) | NO |  | 自定义科目编码 |
| VC_SUBNAME | VARCHAR2(120 BYTE) | YES |  | 自定义科目名称 |
| VC_CURCODE | VARCHAR2(10 BYTE) | YES |  | 币种 |
| F_AMOUNT | NUMBER(25,8) | YES |  | 证券数量 |
| F_COST | NUMBER(35,9) | YES |  | 成本(本位币) |
| F_PRICE | NUMBER(35,9) | YES |  | 市值(本位币) |
| F_GZ | NUMBER(22,8) | YES |  | 估值增值(本位币) |
| F_COST_Y | NUMBER(22,8) | YES |  | 成本(原币) |
| F_PRICE_Y | NUMBER(22,8) | YES |  | 市值(原币) |
| F_GZ_Y | NUMBER(22,8) | YES |  | 估值增值(原币) |
| VC_SOURCE | VARCHAR2(10 BYTE) | YES |  | 数据来源 |
| D_UPDATETIME | TIMESTAMP | YES |  | 更新时间 |
| VC_DELETE | VARCHAR2(10 BYTE) | YES |  | 删除数据标志（体外组合：QT，本地估值组合：空） |
| D_ETL_CREATEDATE | TIMESTAMP | YES |  | 数据抽取时间 |
| D_ETL_CREATEBY | VARCHAR2(20 BYTE) | YES |  | 数据抽取人 |
| D_ETL_UPDATEDATE | TIMESTAMP | YES |  | 数据更新时间 |
| D_ETL_UPDATEBY | VARCHAR2(20 BYTE) | YES |  | 数据更新时间人 |

---

## `DD_DW.MFACTGZ_FUND_ASSETINOUT`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| VC_FUNDCODE | VARCHAR2(20 BYTE) | YES |  | 组合代码 |
| VC_TYPE | VARCHAR2(50 BYTE) | YES |  | 业务类别   IN:流入  OUT 流出 |
| VC_SUBCODE | VARCHAR2(50 BYTE) | YES |  | 科目代码 |
| F_SHARE | NUMBER(18,4) | YES |  | 份额 |
| D_CHARGEUP_DATE | TIMESTAMP | YES |  | 到帐日期 |
| D_CONFIRM_DATE | TIMESTAMP | YES |  | 确认日期(日期关联字段) |
| VC_ACCOUNT_NUM | VARCHAR2(50 BYTE) | YES |  | 套帐编号 |
| VC_ENTRY_PERS | VARCHAR2(50 BYTE) | YES |  | 录入人 |
| D_BENCH_DATE | TIMESTAMP | YES |  | 净值基准日 |
| F_AMOUNT | NUMBER(18,4) | YES |  | 金额 |
| D_ETL_CREATEDATE | TIMESTAMP | YES |  | 数据抽取时间 |
| D_ETL_CREATEBY | VARCHAR2(20 BYTE) | YES |  | 数据抽取人 |
| D_ETL_UPDATEDATE | TIMESTAMP | YES |  | 数据更新时间 |
| D_ETL_UPDATEBY | VARCHAR2(20 BYTE) | YES |  | 数据更新时间人 |
| VC_SOURCE | VARCHAR2(5 BYTE) | YES |  |  |

---

## `DD_DW.MPRF_F_PLAN_DAYNETVALUE`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| VC_PLANCODE (PK) | VARCHAR2(50 BYTE) | NO |  | 计划代码 |
| VC_PLANNAME | VARCHAR2(200 BYTE) | YES |  | 计划名称 |
| D_DATE (PK) | TIMESTAMP | NO |  | 日期 |
| F_NETVALUE | NUMBER(22,2) | YES |  | 资产净值 |
| F_NETVALUE_TCZ | NUMBER(22,2) | YES |  | 资产净值（剔除支付组合） |
| F_NETVALUE_TCB | NUMBER(22,2) | YES |  | 资产净值（剔除保留账户组合） |
| F_CAPITAL_IN | NUMBER(22,2) | YES |  | 投资分配 |
| F_GJHLX_IN | NUMBER(22,2) | YES |  | 归集户利息流入 |
| F_STHLX_IN | NUMBER(22,2) | YES |  | 受托户利息流入 |
| F_CAPITAL_OUT | NUMBER(22,2) | YES |  | 投资提取 |
| F_CAPITAL_IN_TCZ | NUMBER(22,2) | YES |  | 投资分配（剔除支付组合） |
| F_GJHLX_IN_TCZ | NUMBER(22,2) | YES |  | 归集户利息流入（剔除支付组合）  |
| F_STHLX_IN_TCZ | NUMBER(22,2) | YES |  | 受托户利息流入（剔除支付组合） |
| F_CAPITAL_OUT_TCZ | NUMBER(22,2) | YES |  | 投资提取（剔除支付组合） |
| F_CAPITAL_IN_TCB | NUMBER(22,2) | YES |  | 投资分配（剔除保留账户组合） |
| F_GJHLX_IN_TCB | NUMBER(22,2) | YES |  | 归集户利息流入（剔除保留账户组合） |
| F_STHLX_IN_TCB | NUMBER(22,2) | YES |  | 受托户利息流入（剔除保留账户组合） |
| F_CAPITAL_OUT_TCB | NUMBER(22,2) | YES |  | 投资提取（剔除保留账户组合） |
| F_UNITVALUE | NUMBER(12,6) | YES |  | 单位净值 |
| F_AMOUNT | NUMBER(32,6) | YES |  | 份额 |
| F_UNITVALUE_TCZ | NUMBER(12,6) | YES |  | 单位净值（不剔除归集户利息+剔除支付组合） |
| F_AMOUNT_TCZ | NUMBER(32,6) | YES |  | 份额（不剔除归集户利息+剔除支付组合） |
| F_UNITVALUE_TCG | NUMBER(12,6) | YES |  | 单位净值（剔除归集户利息+不剔除支付组合） |
| F_AMOUNT_TCG | NUMBER(32,6) | YES |  | 份额（剔除归集户利息+不剔除支付组合） |
| F_UNITVALUE_TCGZ | NUMBER(12,6) | YES |  | 单位净值（剔除归集户利息+剔除支付组合） |
| F_AMOUNT_TCGZ | NUMBER(32,6) | YES |  | 份额（剔除归集户利息+剔除支付组合） |
| F_INCOME | NUMBER(22,2) | YES |  | 净收益额 |
| F_INCOME_TCG | NUMBER(22,2) | YES |  | 剔除归集户利息后的净收益额 |
| F_GJHLX_RATIO_BZ | NUMBER(10,8) | YES |  | 标准现金流法归集户利息影响率 |
| F_GJHLX_RATIO_JZF | NUMBER(10,8) | YES | 0 | 金转份法归集户利息影响率 |
| F_INCOME_TCZ | NUMBER(22,2) | YES |  | 净收益额（剔除支付组合） |
| F_INCOME_TCGZ | NUMBER(22,2) | YES |  | 剔除归集户利息后的净收益额（剔除支付组合） |
| F_GJHLX_RATIO_BZ_TCZ | NUMBER(10,8) | YES |  | 标准现金流法归集户利息影响率（剔除支付组合） |
| F_GJHLX_RATIO_JZF_TCZ | NUMBER(10,8) | YES | 0 | 金转份法归集户利息影响率（剔除支付组合） |
| F_INCOME_TCB | NUMBER(22,2) | YES |  | 净收益额（剔除保留账户组合） |
| F_INCOME_TCGB | NUMBER(22,2) | YES |  | 剔除归集户利息后的净收益额（剔除保留账户组合） |
| F_GJHLX_RATIO_BZ_TCB | NUMBER(10,8) | YES |  | 标准现金流法归集户利息影响率（剔除保留账户组合） |
| F_GJHLX_RATIO_JZF_TCB | NUMBER(10,8) | YES | 0 | 金转份法归集户利息影响率（剔除保留账户组合） |
| F_BM_YIELD | NUMBER(32,12) | YES |  | 日基准增长率 |
| F_BM_YIELD_TCZ | NUMBER(32,12) | YES |  | 日基准增长率（剔除支付组合） |
| F_BM_YIELD_TCB | NUMBER(32,12) | YES |  | 日基准增长率（剔除保留账户组合） |
| F_DP_YIELD_BZ_TCGZ | NUMBER(32,12) | YES |  | 日计划收益率（标准现金流法+剔除归集户利息+剔除支付组合） |
| F_DP_YIELD_BZ_TCG | NUMBER(32,12) | YES |  | 日计划收益率（标准现金流法+剔除归集户利息+不剔除支付组合） |
| F_DP_YIELD_BZ_TCZ | NUMBER(32,12) | YES |  | 日计划收益率（标准现金流法+不剔除归集户利息+剔除支付组合） |
| F_DP_YIELD_BZ | NUMBER(32,12) | YES |  | 日计划收益率（标准现金流法+不剔除归集户利息+不剔除支付组合） |
| F_DP_YIELD_BZ_TCB | NUMBER(32,12) | YES |  | 日计划收益率（标准现金流法+不剔除归集户利息+不剔除支付组合+剔除保留账户组合） |
| F_DP_YIELD_JZF_TCGZ | NUMBER(32,12) | YES | 0 | 日计划收益率（金转份法+剔除归集户利息+剔除支付组合） |
| F_DP_YIELD_JZF_TCG | NUMBER(32,12) | YES | 0 | 日计划收益率（金转份法+剔除归集户利息+不剔除支付组合） |
| F_DP_YIELD_JZF_TCZ | NUMBER(32,12) | YES | 0 | 日计划收益率（金转份法+不剔除归集户利息+剔除支付组合） |
| F_DP_YIELD_JZF | NUMBER(32,12) | YES | 0 | 日计划收益率（金转份法+不剔除归集户利息+不剔除支付组合） |
| D_UPDATETIME | TIMESTAMP | YES |  | 更新时间 |
| F_MODDURATION_ALL | NUMBER(22,2) | YES |  | 全部债券久期 |
| F_MODDURATION_BD | NUMBER(22,2) | YES |  | 波动类债券久期 |
| F_MODDURATION_JH | NUMBER(22,2) | YES |  | 计划债券久期 |
| F_MODDURATION_ALL_TCZ | NUMBER(22,2) | YES |  | 剔除支付组合全部债券久期 |
| F_MODDURATION_BD_TCZ | NUMBER(22,2) | YES |  | 剔除支付组合波动类债券久期 |
| F_MODDURATION_JH_TCZ | NUMBER(22,2) | YES |  | 剔除支付组合计划债券久期 |
| F_MODDURATION_ALL_TCB | NUMBER(22,2) | YES |  | 剔除保留组合全部债券久期 |
| F_MODDURATION_BD_TCB | NUMBER(22,2) | YES |  | 剔除保留组合波动类债券久期 |
| F_MODDURATION_JH_TCB | NUMBER(22,2) | YES |  | 剔除保留组合计划债券久期 |
| F_PLAN_YIELD_ZBZ | NUMBER(32,12) | YES |  | 标准现金流法自然日成立以来累计收益率（不剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCG | NUMBER(32,12) | YES |  | 标准现金流法自然日成立以来累计收益率（剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCZ | NUMBER(32,12) | YES |  | 标准现金流法自然日成立以来累计收益率（不剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCGZ | NUMBER(32,12) | YES |  | 标准现金流法自然日成立以来累计收益率（剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TBZ | NUMBER(32,12) | YES |  | 标准现金流法交易日成立以来累计收益率（不剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCG | NUMBER(32,12) | YES |  | 标准现金流法交易日成立以来累计收益率（剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCZ | NUMBER(32,12) | YES |  | 标准现金流法交易日成立以来累计收益率（不剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCGZ | NUMBER(32,12) | YES |  | 标准现金流法交易日成立以来累计收益率（剔除归集户利息 + 剔除支付组合） |
| F_DP_DYIELD_TBZ | NUMBER(32,12) | YES |  | 标准现金流法交易日日收益率（不剔除归集户利息 + 不剔除支付组合） |
| F_DP_DYIELD_TBZ_TCG | NUMBER(32,12) | YES |  | 标准现金流法交易日日收益率（剔除归集户利息 + 不剔除支付组合） |
| F_DP_DYIELD_TBZ_TCZ | NUMBER(32,12) | YES |  | 标准现金流法交易日日收益率（不剔除归集户利息 + 剔除支付组合） |
| F_DP_DYIELD_TBZ_TCGZ | NUMBER(32,12) | YES |  | 标准现金流法交易日日收益率（剔除归集户利息 + 剔除支付组合） |
| F_PLAN_BENCH_YEAR | NUMBER(32,12) | YES |  | 本年以来基准收益率（自然日） |
| F_PLAN_BENCH_WHOLE | NUMBER(32,12) | YES |  | 成立以来基准收益率（自然日） |
| F_PLAN_YIELD_ZBZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+自然日+不剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCG_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+自然日+剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+自然日+不剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_ZBZ_TCGZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+自然日+剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TBZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+交易日+不剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCG_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+交易日+剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+交易日+不剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TBZ_TCGZ_YEAR | NUMBER(32,12) | YES |  | 本年以来累计收益率（标准现金流法+交易日+剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TJZF | NUMBER(32,12) | YES |  | 交易日日收益率（金转份法+交易日+不剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TJZF_TCZ | NUMBER(32,12) | YES |  | 交易日日收益率（金转份法+交易日+不剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_TJZF_TCG | NUMBER(32,12) | YES |  | 交易日日收益率（金转份法+交易日+剔除归集户利息 + 不剔除支付组合） |
| F_PLAN_YIELD_TJZF_TCGZ | NUMBER(32,12) | YES |  | 交易日日收益率（金转份法+交易日+剔除归集户利息 + 剔除支付组合） |
| F_PLAN_YIELD_ZBZ_MONTH | NUMBER(32,12) | YES |  | 本月以来累计收益率（标准现金流法+自然日） |
| F_PLAN_BMYIELD_ZRRMONTH | NUMBER(32,12) | YES |  | 本月以来基准累计收益率（标准现金流法+自然日） |
| F_PLAN_STBC | NUMBER(32,12) | YES |  | 受托业绩报酬计提 |
| F_PLAN_TGBC | NUMBER(32,12) | YES |  | 投管业绩报酬计提 |
| F_PLAN_YJBCYX | NUMBER(32,12) | YES |  | 业绩报酬对计划业绩影响 |

---

## `DD_DW.MPRF_PTYPE_DYIELD`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| D_DATE | TIMESTAMP | NO |  |  |
| VC_PLAN_TYPE | VARCHAR2(50 BYTE) | NO |  |  |
| F_YIELD | NUMBER(22,8) | YES |  |  |
| D_UPDATETIME | TIMESTAMP | YES |  |  |

---

## `DD_DW.MDIM_SYS_TIME`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| D_DATE | TIMESTAMP | YES |  | 业务发生日 |
| F_YEAR | NUMBER(38) | YES |  | 年 |
| F_MONTH | NUMBER(38) | YES |  | 月 |
| F_DAY | NUMBER(38) | YES |  | 日 |
| F_HOLS_DAY | NUMBER(38) | YES |  | 假期标志位  0节假日 1 工作日 |
| D_NEXT_DATE | TIMESTAMP | YES |  | 下一工作日 |
| D_PREV_DATE | TIMESTAMP | YES |  | 前一工作日 |
| F_HOLS_DAY_BANK | NUMBER(38) | YES |  | 银行间工日 |
| D_UPDATETIME | TIMESTAMP | YES |  | 更新时间 |
| VC_MONTH_DESC | VARCHAR2(10 BYTE) | YES |  | 月份描述 |
| VC_QUART_DESC | VARCHAR2(10 BYTE) | YES |  | 季度描述 |
| VC_YEAR_DESC | VARCHAR2(10 BYTE) | YES |  | 年份描述 |
| F_PREV_WORKDAY | TIMESTAMP | YES |  | 前一个工作日 |
| F_NEXT_WORKDAY | TIMESTAMP | YES |  | 下一个工作日 |
| F_QUART | NUMBER(38) | YES |  | 季度 |
| F_HOLS_DAY_HK | NUMBER | YES |  |  |
| F_WEEK | NUMBER | YES |  |  |
| D_PREV_DATE_HK | TIMESTAMP | YES |  |  |
| D_NEXT_DATE_HK | TIMESTAMP | YES |  |  |
| F_HOLS_CFDAY | NUMBER | YES |  |  |
| D_PREV_CFDAY | TIMESTAMP | YES |  |  |
| D_NEXT_CFDAY | TIMESTAMP | YES |  |  |
| F_LAST_TRADING_DAY_W | NUMBER(1) | YES |  | 是否是周最后一个交易日 1 是 0 否 |
| F_LAST_TRADING_DAY_M | NUMBER(1) | YES |  | 是否是月最后一个交易日 1 是 0 否 |

---

## `DD_DW.MFACTGZ_FUND_HLDDETAIL`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| F_ID | NUMBER(28) | YES |  | 唯一编码 |
| D_DATE | TIMESTAMP | YES |  | 日期 |
| VC_FUNDCODE | VARCHAR2(2000 BYTE) | YES |  | 产品代码 |
| VC_SYMBOL_ID | VARCHAR2(2000 BYTE) | YES |  | 统一证券代码 |
| VC_SYMBOL | VARCHAR2(2000 BYTE) | YES |  | 证券代码 |
| VC_NAME | VARCHAR2(2000 BYTE) | YES |  | 证券名称 |
| VC_EXCHANGE | VARCHAR2(2000 BYTE) | YES |  | 市场代码 |
| VC_J_SYMBOL | VARCHAR2(2000 BYTE) | YES |  | 金手指代码 |
| VC_TYPE | VARCHAR2(2000 BYTE) | YES |  | 证券大类 |
| VC_TYPE_DETAIL | VARCHAR2(2000 BYTE) | YES |  | 明细分类代码 |
| VC_TYPE_LIMIT | VARCHAR2(2000 BYTE) | YES |  | 流通性： 1：流通0：非流通 |
| VC_PA_CODE | VARCHAR2(2000 BYTE) | YES |  | 核算项目  |
| VC_IVT_CLSS | VARCHAR2(2000 BYTE) | YES |  | 投资分类 |
| VC_HLD_ATTR | VARCHAR2(2000 BYTE) | YES |  | 持有属性(与投资分类相同) |
| VC_TD_ATTR | VARCHAR2(2000 BYTE) | YES |  | 交易属性  |
| VC_CURCODE | VARCHAR2(2000 BYTE) | YES |  | 币种  |
| F_AMOUNT | NUMBER(25,8) | YES |  | 数量 |
| F_COST | NUMBER(35,9) | YES |  | 成本(本位币) |
| F_PRICE | NUMBER(35,9) | YES |  | 市值(本位币) |
| F_GZ | NUMBER(20,4) | YES |  | 估值增值(本位币) |
| F_INTEREST | NUMBER(20,4) | YES |  | 利息(本位币) |
| F_DISCOUNT | NUMBER(20,4) | YES |  | 溢折价(本位币) |
| F_FULLPRICE | NUMBER(20,4) | YES |  | 全价(本位币) |
| F_COST_Y | NUMBER(20,4) | YES |  | 成本(原币) |
| F_PRICE_Y | NUMBER(20,4) | YES |  | 市值(原币) |
| F_GZ_Y | NUMBER(20,4) | YES |  | 估值增值(原币) |
| F_INTEREST_Y | NUMBER(20,4) | YES |  | 利息(原币) |
| F_DISCOUNT_Y | NUMBER(20,4) | YES |  | 溢折价(原币) |
| F_FULLPRICE_Y | NUMBER(20,4) | YES |  | 全价(原币) |
| VC_ORI_CODE | VARCHAR2(2000 BYTE) | YES |  | 原始科目编码 |
| VC_ORI_CODE_NAME | VARCHAR2(2000 BYTE) | YES |  | 原始科目名称 |
| VC_SUBCODE_TYPE | VARCHAR2(2000 BYTE) | YES |  | 标识资产负债 |
| VC_FTPXX | VARCHAR2(2000 BYTE) | YES |  | 停牌信息 |
| F_VALPRICE | NUMBER(32,12) | YES |  | 估值价格 |
| VC_SOURCE | VARCHAR2(2000 BYTE) | YES |  | 数据来源 |
| D_UPDATETIME | TIMESTAMP | YES |  | 更新时间 |
| VC_TYPE_ASSIST | VARCHAR2(2000 BYTE) | YES |  | 证券辅助类 |
| F_ZQNM | VARCHAR2(2000 BYTE) | YES |  | 证券内码 |
| VC_TYPE_ASSIST2 | VARCHAR2(2000 BYTE) | YES |  | 证券辅助类2 |
| VC_TYPE_ASSIST3 | VARCHAR2(2000 BYTE) | YES |  | 证券辅助类3 |
| F_AMOUNTS | NUMBER(20,4) | YES |  | 特殊值 |
| F_CP_PRICE | NUMBER(20,4) | YES |  | 市值成本孰底值 |
| VC_SOURCODE | VARCHAR2(2000 BYTE) | YES |  | 自定义编码 |
| F_AMOUNT2 | NUMBER(20,4) | YES |  | 数量2(本位币) |
| F_COST2 | NUMBER(20,4) | YES |  | 成本2(本位币) |
| F_PRICE2 | NUMBER(20,4) | YES |  | 市值2(本位币) |
| F_COST_Y2 | NUMBER(20,4) | YES |  | 成本2(原币) |
| F_PRICE_Y2 | NUMBER(20,4) | YES |  | 市值2(原币) |
| F_QHLB | VARCHAR2(2000 BYTE) | YES |  | 期货l类别(包括股指期货) |
| F_XTBZJJ | NUMBER(2) | YES |  | 是否信托保障基金标志 |
| VC_SUBCODE | VARCHAR2(2000 BYTE) | YES |  | 持仓汇总自定义的编码 |
| VC_TYPE_GZQH | VARCHAR2(2000 BYTE) | YES |  | 股指期货类型 |
| VC_MANAGER_TYPE | VARCHAR2(2000 BYTE) | YES |  | 管理类型 |
| VC_TQBZ | VARCHAR2(2000 BYTE) | YES |  | 套期标志 |
| VC_HOLDFLAG | VARCHAR2(2000 BYTE) | YES |  | 持仓标志 |
| VC_FQYXX | VARCHAR2(2000 BYTE) | YES |  | 权益信息 |
| VC_FACCTPARENT | VARCHAR2(2000 BYTE) | YES |  | 父级科目编码 |
| VC_TYPE_DETAIL_NEW | VARCHAR2(2000 BYTE) | YES |  | 明细分类代码(新) |
| VC_SEC_CODE | VARCHAR2(2000 BYTE) | YES |  | 内部证券代码(托管行) |
| VC_MKT_CODE | VARCHAR2(2000 BYTE) | YES |  | 内部市场代码(托管行) |

---

## `DD_DW.MMON_F_RISK_INDICATORS`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| D_DATE | TIMESTAMP | YES |  | 日期 |
| VC_PLANCODE | VARCHAR2(30 BYTE) | YES |  | 计划登记号 |
| VC_FUNDCODE | VARCHAR2(50 BYTE) | YES |  | 组合代码 |
| F_MVIX | NUMBER(22,12) | YES |  | 波动率(本月 & 交易日 &[计划:现金流法]) |
| F_MMAXDRAW_DAY | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(本月 & 交易日 &[计划:现金流法]) |
| F_MMAXDRAW_ACC | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(本月 & 交易日 &[计划:现金流法]) |
| F_MVIX_DESC | NUMBER(22,12) | YES |  | 下行风险(本月 & 交易日 &[计划:现金流法]) |
| F_MSHARP | NUMBER(22,12) | YES |  | 夏普比率(本月 & 交易日 &[计划:现金流法]) |
| F_YVIX | NUMBER(22,12) | YES |  | 波动率(本年 & 交易日 &[计划:现金流法]) |
| F_YMAXDRAW_DAY | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(本年 & 交易日 &[计划:现金流法]) |
| F_YMAXDRAW_ACC | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(本年 & 交易日 &[计划:现金流法]) |
| F_YVIX_DESC | NUMBER(22,12) | YES |  | 下行风险(本年 & 交易日 &[计划:现金流法]) |
| F_YSHARP | NUMBER(22,12) | YES |  | 夏普比率(本年 & 交易日 &[计划:现金流法]) |
| F_CVIX | NUMBER(22,12) | YES |  | 波动率(成立以来 & 交易日 &[计划:现金流法]) |
| F_CMAXDRAW_DAY | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(成立以来 & 交易日 &[计划:现金流法]) |
| F_CMAXDRAW_ACC | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(成立以来 & 交易日 &[计划:现金流法]) |
| F_CVIX_DESC | NUMBER(22,12) | YES |  | 下行风险(成立以来 & 交易日 &[计划:现金流法]) |
| F_CSHARP | NUMBER(22,12) | YES |  | 夏普比率(成立以来 & 交易日 &[计划:现金流法]) |
| VC_PTYPE | VARCHAR2(30 BYTE) | YES |  | 计划类型 |
| D_UPDATETIME | TIMESTAMP | YES |  | 数据更新时间 |
| F_MVIX_TCG | NUMBER(22,12) | YES |  | 波动率(本月 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_MMAXDRAW_DAY_TCG | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(本月 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_MMAXDRAW_ACC_TCG | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(本月 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_MVIX_DESC_TCG | NUMBER(22,12) | YES |  | 下行风险(本月 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_MSHARP_TCG | NUMBER(22,12) | YES |  | 夏普比率(本月 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_YVIX_TCG | NUMBER(22,12) | YES |  | 波动率(本年 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_YMAXDRAW_DAY_TCG | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(本年 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_YMAXDRAW_ACC_TCG | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(本年 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_YVIX_DESC_TCG | NUMBER(22,12) | YES |  | 下行风险(本年 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_YSHARP_TCG | NUMBER(22,12) | YES |  | 夏普比率(本年 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_CVIX_TCG | NUMBER(22,12) | YES |  | 波动率(成立以来 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_CMAXDRAW_DAY_TCG | NUMBER(22,12) | YES |  | 最大回撤（14号文要求）(成立以来 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_CMAXDRAW_ACC_TCG | NUMBER(22,12) | YES |  | 最大回撤（累计收益率）(成立以来 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_CVIX_DESC_TCG | NUMBER(22,12) | YES |  | 下行风险(成立以来 & 交易日 &[计划:现金流法] & 剔除归集户利息) |
| F_CSHARP_TCG | NUMBER(22,12) | YES |  | 夏普比率(成立以来 & 交易日 &[计划:现金流法] & 剔除归集户利息) |

---

## `DD_DW.MDIM_FUND_LASTDATE`

| Column | Type | Nullable | Default | Comment |
| --- | --- | --- | --- | --- |
| VC_PLANCODE | VARCHAR2(40 BYTE) | YES |  |  |
| VC_PLANNAME | VARCHAR2(500 BYTE) | YES |  |  |
| VC_FUNDCODE | VARCHAR2(50 BYTE) | NO |  |  |
| VC_FNAME | VARCHAR2(100 BYTE) | YES |  |  |
| VC_TYPE_DETAIL | VARCHAR2(100 BYTE) | YES |  |  |
| VC_TYPE_IN | VARCHAR2(20 BYTE) | YES |  |  |
| D_DATE | VARCHAR2(10 BYTE) | YES |  |  |
| VC_TYPE | CHAR(4 BYTE) | YES |  |  |
| D_UPDATETIME | TIMESTAMP | YES |  |  |

---
