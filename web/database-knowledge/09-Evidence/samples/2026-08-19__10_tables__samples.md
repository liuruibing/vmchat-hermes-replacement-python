---
type: evidence
domain: 职年计划投资业绩
name: DBX数据探查-首批10张表全量只读样例与分布
status: supported
confidence: 5
sources:
  - path: DD_DW.MDIM_PLAN_INFO
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MDIM_FUND_INFO
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MFACTGZ_FUND_HLDTOTAL
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MFACTGZ_FUND_ASSETINOUT
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MPRF_F_PLAN_DAYNETVALUE
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MPRF_PTYPE_DYIELD
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MDIM_SYS_TIME
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MFACTGZ_FUND_HLDDETAIL
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MMON_F_RISK_INDICATORS
    level: E4
    location: dbx_execute_query
  - path: DD_DW.MDIM_FUND_LASTDATE
    level: E4
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

# DBX 数据探查证据：首批 10 张表全量只读探查样例 (E4 Verbatim)

- **执行日期**：2026-08-19
- **数据库连接**：`DD_AODS` (Dameng 达梦)
- **只读 SQL 门禁**：所有探查与分布查询均显式限制 `ROWNUM <= 5` 或 `ROWNUM <= 20`，严禁无限制扫描。
- **证据编号**：`EVID-SMP-001` ~ `EVID-SMP-011`

---

## 探查目标: `DD_DW.MDIM_PLAN_INFO` (E4 探查)

- **只读 SQL**: `SELECT VC_PLAN_CODE, VC_PLAN_LIC_ID, VC_PLAN_NAME, VC_TYPE_DETAIL, D_CREATE_DATE FROM DD_DW.MDIM_PLAN_INFO WHERE ROWNUM <= 5` 
- **返回结果**:

| VC_PLAN_CODE | VC_PLAN_LIC_ID | VC_PLAN_NAME | VC_TYPE_DETAIL | D_CREATE_DATE |
|---|---|---|---|---|
(0 rows, 19ms)

---

## 探查目标: `DD_DW.MDIM_FUND_INFO` (E4 探查)

- **只读 SQL**: `SELECT VC_FUNDCODE, VC_PLAN_CODE, VC_FUNDNAME, VC_NAME_GLR, VC_PRODUCT_INVESTMENT_TYPE, F_SET_AMOUNT FROM DD_DW.MDIM_FUND_INFO WHERE ROWNUM <= 5` 
- **返回结果**:

| VC_FUNDCODE | VC_PLAN_CODE | VC_FUNDNAME | VC_NAME_GLR | VC_PRODUCT_INVESTMENT_TYPE | F_SET_AMOUNT |
|---|---|---|---|---|---|
| TZ000001 | ZP0001 | 测试职年组合000001 | 测试投资管理人01 | NULL | 10010000.00000000 |
| TZ000002 | ZP0001 | 测试职年组合000002 | 测试投资管理人02 | NULL | 10020000.00000000 |
| TZ000003 | ZP0001 | 测试职年组合000003 | 测试投资管理人03 | NULL | 10030000.00000000 |
| TZ000004 | ZP0001 | 测试职年组合000004 | 测试投资管理人04 | NULL | 10040000.00000000 |
| TZ000005 | ZP0001 | 测试职年组合000005 | 测试投资管理人05 | NULL | 10050000.00000000 |
(5 rows, 9ms)

---

## 探查目标: `DD_DW.MDIM_FUND_INFO_DIST` (E4 探查)

- **只读 SQL**: `SELECT VC_PRODUCT_INVESTMENT_TYPE, COUNT(*) AS CNT FROM DD_DW.MDIM_FUND_INFO WHERE ROWNUM <= 20 GROUP BY VC_PRODUCT_INVESTMENT_TYPE ORDER BY CNT DESC` 
- **返回结果**:

| VC_PRODUCT_INVESTMENT_TYPE | CNT |
|---|---|
| NULL | 20 |
(1 rows, 19ms)

---

## 探查目标: `DD_DW.MFACTGZ_FUND_HLDTOTAL` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, VC_FUNDCODE, VC_SUBCODE, VC_SUBNAME, F_PRICE FROM DD_DW.MFACTGZ_FUND_HLDTOTAL WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | VC_FUNDCODE | VC_SUBCODE | VC_SUBNAME | F_PRICE |
|---|---|---|---|---|
| 2025-01-01 00:00:00 | TQ001601 | 601A | 实收资本 | 26010000.000000000 |
| 2025-01-01 00:00:00 | TQ001601 | 701A | 资产净值 | 26009869.950000000 |
| 2025-01-01 00:00:00 | TQ001601 | 702A | 单位净值 | 0.999995000 |
| 2025-01-01 00:00:00 | TQ001602 | 601A | 实收资本 | 26020000.000000000 |
| 2025-01-01 00:00:00 | TQ001602 | 701A | 资产净值 | 26020312.240000000 |
(5 rows, 10ms)

---

## 探查目标: `DD_DW.MFACTGZ_FUND_ASSETINOUT` (E4 探查)

- **只读 SQL**: `SELECT D_CONFIRM_DATE, VC_FUNDCODE, VC_TYPE, F_AMOUNT FROM DD_DW.MFACTGZ_FUND_ASSETINOUT WHERE ROWNUM <= 5` 
- **返回结果**:

| D_CONFIRM_DATE | VC_FUNDCODE | VC_TYPE | F_AMOUNT |
|---|---|---|---|
| 2025-02-17 00:00:00 | TQ001601 | OUT | 30100.0000 |
| 2025-05-25 00:00:00 | TQ001601 | OUT | 30100.0000 |
| 2025-08-30 00:00:00 | TQ001601 | OUT | 30100.0000 |
| 2025-12-05 00:00:00 | TQ001601 | OUT | 30100.0000 |
| 2025-02-16 00:00:00 | TQ001602 | OUT | 30200.0000 |
(5 rows, 10ms)

---

## 探查目标: `DD_DW.MPRF_F_PLAN_DAYNETVALUE` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, VC_PLANCODE, F_NETVALUE, F_DP_YIELD_BZ, F_PLAN_STBC, F_PLAN_TGBC FROM DD_DW.MPRF_F_PLAN_DAYNETVALUE WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | VC_PLANCODE | F_NETVALUE | F_DP_YIELD_BZ | F_PLAN_STBC | F_PLAN_TGBC |
|---|---|---|---|---|---|
(0 rows, 9ms)

---

## 探查目标: `DD_DW.MPRF_PTYPE_DYIELD` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, VC_PLAN_TYPE, F_YIELD FROM DD_DW.MPRF_PTYPE_DYIELD WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | VC_PLAN_TYPE | F_YIELD |
|---|---|---|
(0 rows, 8ms)

---

## 探查目标: `DD_DW.MDIM_SYS_TIME` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, F_YEAR, F_MONTH, F_DAY, F_HOLS_DAY, D_PREV_DATE FROM DD_DW.MDIM_SYS_TIME WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | F_YEAR | F_MONTH | F_DAY | F_HOLS_DAY | D_PREV_DATE |
|---|---|---|---|---|---|
| 2015-11-07 00:00:00 | 2015 | 11 | 7 | 0 | 2015-11-06 00:00:00 |
| 2015-11-09 00:00:00 | 2015 | 11 | 9 | 1 | 2015-11-06 00:00:00 |
| 2015-11-10 00:00:00 | 2015 | 11 | 10 | 1 | 2015-11-09 00:00:00 |
| 2015-11-11 00:00:00 | 2015 | 11 | 11 | 1 | 2015-11-10 00:00:00 |
| 2015-11-12 00:00:00 | 2015 | 11 | 12 | 1 | 2015-11-11 00:00:00 |
(5 rows, 16ms)

---

## 探查目标: `DD_DW.MFACTGZ_FUND_HLDDETAIL` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, VC_FUNDCODE, VC_SYMBOL, VC_NAME, F_PRICE FROM DD_DW.MFACTGZ_FUND_HLDDETAIL WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | VC_FUNDCODE | VC_SYMBOL | VC_NAME | F_PRICE |
|---|---|---|---|---|
(0 rows, 10ms)

---

## 探查目标: `DD_DW.MMON_F_RISK_INDICATORS` (E4 探查)

- **只读 SQL**: `SELECT D_DATE, VC_PLANCODE, F_MVIX, F_MMAXDRAW_DAY, F_MSHARP FROM DD_DW.MMON_F_RISK_INDICATORS WHERE ROWNUM <= 5` 
- **返回结果**:

| D_DATE | VC_PLANCODE | F_MVIX | F_MMAXDRAW_DAY | F_MSHARP |
|---|---|---|---|---|
(0 rows, 9ms)

---

## 探查目标: `DD_DW.MDIM_FUND_LASTDATE` (E4 探查)

- **只读 SQL**: `SELECT VC_PLANCODE, VC_FUNDCODE, VC_FNAME, D_DATE FROM DD_DW.MDIM_FUND_LASTDATE WHERE ROWNUM <= 5` 
- **返回结果**:

| VC_PLANCODE | VC_FUNDCODE | VC_FNAME | D_DATE |
|---|---|---|---|
(0 rows, 10ms)

---
