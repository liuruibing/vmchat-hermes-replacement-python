---
type: evidence
domain: 职年计划投资业绩
name: DBX源码证据-DW_ZNST_INDEX_NEW包体源码
status: confirmed
confidence: 5
sources:
  - path: DD_DW.DW_ZNST_INDEX_NEW
    level: E2
    location: dbx_execute_query
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
related_functions:
  - DW_ZNST_INDEX_NEW.F_PLAN_DYIELD_BZ
last_verified: 2026-08-19
---

# DBX 存储过程包体源码证据：`DD_DW.DW_ZNST_INDEX_NEW` (E2 原始导出)

- **执行日期**：2026-08-19
- **数据库连接**：`DD_AODS` (Dameng 达梦)
- **提取来源**：`DD_DW.ALL_SOURCE`
- **证据级别**：**E2** (已验证的存储过程包体源码)

---

## 源码展示 (Package Body Text)

```sql
| TEXT |
|---|
| CREATE  PACKAGE BODY "DD_DW"."DW_ZNST_INDEX_NEW"  IS

  FUNCTION F_RISK_NONERISK(I_ENDDATE IN VARCHAR2) RETURN NUMBER AS
    /*****************************
    无风险收益率
    ZKY
    一年定期存款利率
    *****************************/
    VC_RESULT NUMBER := 0.0;
    V_ENDDATE DATE;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT = ''YYYY-MM-DD''';
    V_ENDDATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');
    
     SELECT G.F_INDEX_PRICE / 100 INTO VC_RESULT FROM MFACTEI_INDEX_MARKET G WHERE G.D_DATE = V_ENDDATE AND G.VC_INDEX_CODE = '104CNY';
  
    RETURN(VC_RESULT);
  END F_RISK_NONERISK;
  --职年受托个性化指标接口 - 组合层指标
  FUNCTION F_FUND_END_NETVALUE(I_FUNDCODE  IN VARCHAR2,
                               I_STARTDATE IN VARCHAR2,
                               I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：组合层指标 - 期末资产净值
    *
    * 作 者： maple song
    * 创建日期：2020-02-28
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 组合代码、期初日期、期末日期
    *             传出 -> 期末资产净值
    
    \*****************************************************************************/
    V_RESULT NUMBER;
    V_EDATE  DATE;
    v_cdate  DATE;
    v_DATE   DATE;
    
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_EDATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');
    
    SELECT m.d_create_date,m.d_edate
      into v_cdate,V_DATE
      from mdim_fund_info m
     where m.vc_fundcode = I_FUNDCODE;
    
    
    SELECT NVL(MAX(T.F_PRICE), 0)
      INTO V_RESULT
      FROM MFACTGZ_FUND_HLDTOTAL T
     WHERE T.VC_FUNDCODE = I_FUNDCODE
       AND T.D_DATE = V_EDATE
       AND t.d_date BETWEEN v_cdate AND V_DATE
       AND T.VC_SUBCODE = '701A';
    RETURN NVL(V_RESULT, 0);
  
  END F_FUND_END_NETVALUE;

  FUNCTION F_FUND_END_UNITVALUE(I_FUNDCODE  IN VARCHAR2,
                                I_STARTDATE IN VARCHAR2,
                                I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：组合层指标 - 期末单位净值
    *
    * 作 者： maple song
    * 创建日期：2020-02-28
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 组合代码、期初日期、期末日期
    *             传出 -> 期末单位净值
    
    \*****************************************************************************/
  
    V_RESULT NUMBER;
    V_DATE   DATE;
    V_CN     NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');
    
      SELECT NVL(MAX(T.F_PRICE), 0)
        INTO V_RESULT
        FROM MFACTGZ_FUND_HLDTOTAL T
       WHERE T.VC_FUNDCODE = I_FUNDCODE
         AND T.D_DATE = V_DATE
         AND T.VC_SUBCODE = '702A';
    RETURN NVL(V_RESULT, 0);
  
  END F_FUND_END_UNITVALUE;

  FUNCTION F_FUND_END_AMOUNT(I_FUNDCODE  IN VARCHAR2,
                             I_STARTDATE IN VARCHAR2,
                             I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：组合层指标 - 期末份额
    *
    * 作 者： maple song
    * 创建日期：2020-02-28
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 组合代码、期初日期、期末日期
    *             传出 -> 期末份额
    
    \*****************************************************************************/
  
    V_RESULT NUMBER;
    V_DATE   DATE;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE := TO_D... [chars 0..4000; next cell_char_offset=4000] |
(1 rows, 30ms)
```
