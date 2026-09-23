---
type: evidence
domain: 职年计划投资业绩
name: DBX源码证据-DW关键计算函数完整源码导出
status: confirmed
confidence: 5
sources:
  - path: DD_DW.ALL_SOURCE
    level: E2
    location: dbx_execute_query
related_tables:
  - MPRF_F_PLAN_DAYNETVALUE
  - MFACTGZ_FUND_HLDTOTAL
  - MFACTGZ_FUND_HLDDETAIL
related_functions:
  - F_PLAN_END_NETVALUE
  - F_PLAN_DYIELD_BZ_ZYNJ
  - F_PLAN_YIELD_BZ
  - F_PLAN_STBC
  - F_PLAN_TGBC
  - F_PLAN_YJYX
last_verified: 2026-08-19
---

# DBX 核心计算函数完整源码证据 (E2 逐行全量无截断导出)

- **执行日期**：2026-08-19
- **数据库连接**：`DD_AODS` (Dameng 达梦)
- **提取视图**：`DD_DW.ALL_SOURCE`
- **证据级别**：**E2** (已验证的底层 PL/SQL 函数源码)

---

## 函数源码: `DD_DW.F_PLAN_END_NETVALUE` (长度 1204 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_END_NETVALUE"(
                               I_PLAN_TYPE_DETAIL IN VARCHAR2,
                               I_TYPE_IN IN VARCHAR2,
                               I_DATE IN VARCHAR2) return NUMBER is
  V_RESULT NUMBER;
  V_TYPE_IN VARCHAR2(10);
  -- I_PLAN_TYPE_DETAIL 产品投资类型: ZYNJ QYNJ
  -- I_TYPE_IN 产品类型: JH集合   DY单一
BEGIN
  V_TYPE_IN := I_TYPE_IN;
  
  IF V_TYPE_IN IS NOT NULL THEN
    SELECT NVL(SUM(T.F_PRICE), 0) INTO V_RESULT
    FROM MFACTGZ_FUND_HLDTOTAL T 
    WHERE T.D_DATE = TO_DATE(I_DATE, 'YYYY-MM-DD')
    AND T.VC_SUBCODE = '701A'
    AND T.VC_FUNDCODE IN (
        select F.VC_FUNDCODE from MDIM_FUND_INFO F 
        where F.VC_TYPE_DETAIL = I_PLAN_TYPE_DETAIL
        AND F.VC_TYPE_IN = I_TYPE_IN
    );
  END IF;
  
  IF V_TYPE_IN IS NULL OR V_TYPE_IN = '' THEN 
    SELECT NVL(SUM(T.F_PRICE), 0) INTO V_RESULT
    FROM MFACTGZ_FUND_HLDTOTAL T 
    WHERE T.D_DATE = TO_DATE(I_DATE, 'YYYY-MM-DD')
    AND T.VC_SUBCODE = '701A'
    AND T.VC_FUNDCODE IN (
        select F.VC_FUNDCODE from MDIM_FUND_INFO F 
        where F.VC_TYPE_DETAIL = I_PLAN_TYPE_DETAIL
    );
  END IF;
  
  RETURN V_RESULT;
END F_PLAN_END_NETVALUE; 
(1 rows, 20ms)
```

---

## 函数源码: `DD_DW.F_PLAN_DYIELD_BZ_ZYNJ` (长度 3621 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_DYIELD_BZ_ZYNJ"( I_DATE IN VARCHAR2)
    RETURN NUMBER DETERMINISTIC IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 日计划收益率（标准现金流法+ 不剔除归集户利息+ 不剔除支付组合）
    *
    * 作 者： WZ
    * 创建日期：2026-01-07
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 日期
    *             传出 -> 职年整体的日时间加权收益率
    *
    \*****************************************************************************/
    V_RESULT      NUMBER;
    V_NETVALUE    NUMBER;
    V_YNETVALUE   NUMBER;
    V_DATE        DATE;
    V_YDATE       DATE;
    V_CAPITAL_IN  NUMBER;
    V_CAPITAL_OUT NUMBER;
    V_CREATE_DATE DATE;
    V_SET_AMOUNT  NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE        := TO_DATE(I_DATE, 'YYYY-MM-DD');
    V_YDATE       := TO_DATE(I_DATE, 'YYYY-MM-DD') - 1;
    V_RESULT      := 0;
    V_NETVALUE    := 0;
    V_YNETVALUE   := 0;
    V_CAPITAL_IN  := 0;
    V_CAPITAL_OUT := 0;

    SELECT MIN(T.D_CREATE_DATE), SUM(T.F_SET_AMOUNT)
      INTO V_CREATE_DATE, V_SET_AMOUNT
      FROM MDIM_FUND_INFO T
     WHERE T.VC_TYPE_DETAIL = 'ZYNJ'--T.VC_PLAN_CODE = I_PLANCODE
       AND T.VC_REMARKS = '组合';

    IF V_DATE < V_CREATE_DATE THEN
      RETURN 0;
    END IF;

    IF V_DATE = V_CREATE_DATE THEN
      SELECT NVL(SUM(F_FUND_END_NETVALUE(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(CASE
                       WHEN T.D_CREATE_DATE = V_DATE THEN
                        T.F_SET_AMOUNT
                       ELSE
                        0
                     END),
                 0)
        INTO V_NETVALUE, V_SET_AMOUNT
        FROM MDIM_FUND_INFO T
       WHERE T.VC_TYPE_DETAIL = 'ZYNJ' --T.VC_PLAN_CODE = I_PLANCODE
         AND T.VC_REMARKS = '组合';

      SELECT DECODE(NVL(V_SET_AMOUNT, 0),
                    0,
                    0,
                    ((V_NETVALUE - V_SET_AMOUNT) / V_SET_AMOUNT))
        INTO V_RESULT
        FROM DUAL;
      RETURN NVL(V_RESULT, 0);
    END IF;

    IF V_DATE > V_CREATE_DATE THEN

      SELECT /* + parallel(4)*/ NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_END_NETVALUE(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_END_NETVALUE(T.VC_FUNDCODE,
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'),
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'))),
                 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_IN(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_OUT(T.VC_FUNDCODE, I_DATE, I_DATE)), 0)
        INTO V_NETVALUE, V_YNETVALUE, V_CAPITAL_IN, V_CAPITAL_OUT
        FROM MDIM_FUND_INFO T
       WHERE T.VC_TYPE_DETAIL = 'ZYNJ' --T.VC_PLAN_CODE = I_PLANCODE
         AND T.VC_REMARKS = '组合'
         /*and t.d_create_date <= V_DATE
         and t.d_edate >= V_DATE*/;

   -- DBMS_OUTPUT.PUT_LINE(V_CREATE_DATE||'-'||TO_CHAR(V_YDATE, 'YYYY-MM-DD')||'-'||V_NETVALUE||'-'||V_YNETVALUE||'-'||V_CAPITAL_IN||'-'||V_CAPITAL_OUT);
      SELECT DECODE(NVL(V_YNETVALUE, 0),
                    0,
                    0,
                    (V_NETVALUE - V_YNETVALUE - V_CAPITAL_IN + V_CAPITAL_OUT) /
                    V_YNETVALUE)
        INTO V_RESULT
        FROM DUAL;

      RETURN NVL(V_RES
(1 rows, 30ms)
 ...ULT, 0);
    END IF;

  END F_PLAN_DYIELD_BZ_ZYNJ; [chars 3500..3550; end of value] 
(1 rows, 20ms)
```

---

## 函数源码: `DD_DW.F_PLAN_DYIELD_BZ_ZYNJ2` (长度 2135 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_DYIELD_BZ_ZYNJ2"( I_DATE IN VARCHAR2)
    RETURN NUMBER IS
    /*****************************************************************************\
    *                           太平养老年金受托报表
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：整体 - 日时间加权收益率
    *
    * 作 者： K
    * 创建日期：2026-03-11
    * 版  本  号：1.0.0
    *
    * 参      数：传入 -> 日期
    *             传出 -> 职年整体的日时间加权收益率
    *
    \*****************************************************************************/
    V_RESULT      NUMBER;
    V_NETVALUE    NUMBER;
    V_YNETVALUE   NUMBER;
    V_DATE        DATE;
    V_YDATE       DATE;
    V_CAPITAL_IN  NUMBER;
    V_CAPITAL_OUT NUMBER;
    V_CREATE_DATE DATE;
    V_SET_AMOUNT  NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE        := TO_DATE(I_DATE, 'YYYY-MM-DD');
    V_YDATE       := TO_DATE(I_DATE, 'YYYY-MM-DD') - 1;
    V_RESULT      := 0;
    V_NETVALUE    := 0;
    V_YNETVALUE   := 0;
    V_CAPITAL_IN  := 0;
    V_CAPITAL_OUT := 0;



      SELECT NVL(SUM(F_FUND_END_NETVALUE(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(F_FUND_END_NETVALUE(T.VC_FUNDCODE,
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'),
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'))),
                 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_IN(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_OUT(T.VC_FUNDCODE, I_DATE, I_DATE)), 0)
        INTO V_NETVALUE, V_YNETVALUE, V_CAPITAL_IN, V_CAPITAL_OUT
        FROM MDIM_FUND_INFO T
       WHERE T.VC_TYPE_DETAIL = 'ZYNJ'
         AND T.VC_REMARKS = '组合';

      SELECT DECODE(NVL(V_YNETVALUE, 0),
                    0,
                    0,
                    (V_NETVALUE - V_YNETVALUE - V_CAPITAL_IN + V_CAPITAL_OUT) /
                    V_YNETVALUE)
        INTO V_RESULT
        FROM DUAL;

      RETURN NVL(V_RESULT, 0);

  END F_PLAN_DYIELD_BZ_ZYNJ2; 
(1 rows, 28ms)
```

---

## 函数源码: `DD_DW.F_PLAN_DYIELD_BZ_ZYNJ_FTP` (长度 2289 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_DYIELD_BZ_ZYNJ_FTP"( I_DATE IN VARCHAR2,I_FUNDTYPE   IN VARCHAR2)
    RETURN NUMBER DETERMINISTIC IS
    /*****************************************************************************\
    *                           太平养老年金受托报表
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：整体 - 日时间加权收益率
    *
    * 作 者： K
    * 创建日期：2026-03-11
    * 版  本  号：1.0.0
    *
    * 参      数：传入 -> 日期
    *             传出 -> 职年整体的日时间加权收益率
    *
    \*****************************************************************************/
    V_RESULT      NUMBER;
    V_NETVALUE    NUMBER;
    V_YNETVALUE   NUMBER;
    V_DATE        DATE;
    V_YDATE       DATE;
    V_CAPITAL_IN  NUMBER;
    V_CAPITAL_OUT NUMBER;
    V_CREATE_DATE DATE;
    V_SET_AMOUNT  NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE        := TO_DATE(I_DATE, 'YYYY-MM-DD');
    V_YDATE       := TO_DATE(I_DATE, 'YYYY-MM-DD') - 1;
    V_RESULT      := 0;
    V_NETVALUE    := 0;
    V_YNETVALUE   := 0;
    V_CAPITAL_IN  := 0;
    V_CAPITAL_OUT := 0;



      SELECT NVL(SUM(F_FUND_END_NETVALUE(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(F_FUND_END_NETVALUE(T.VC_FUNDCODE,
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'),
                                         TO_CHAR(V_YDATE, 'YYYY-MM-DD'))),
                 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_IN(T.VC_FUNDCODE, I_DATE, I_DATE)), 0),
             NVL(SUM(DW_ZNST_INDEX_NEW.F_FUND_CAPITAL_OUT(T.VC_FUNDCODE, I_DATE, I_DATE)), 0)
        INTO V_NETVALUE, V_YNETVALUE, V_CAPITAL_IN, V_CAPITAL_OUT
        FROM MDIM_FUND_INFO T
       WHERE T.VC_TYPE_DETAIL = 'ZYNJ'
         AND T.VC_REMARKS = '组合'
         AND T.VC_FUND_TYPE = I_FUNDTYPE
         AND F_FUND_END_NETVALUE(T.VC_FUNDCODE, I_DATE, I_DATE) > 0;

      SELECT DECODE(NVL(V_YNETVALUE, 0),
                    0,
                    0,
                    (V_NETVALUE - V_YNETVALUE - V_CAPITAL_IN + V_CAPITAL_OUT) /
                    V_YNETVALUE)
        INTO V_RESULT
        FROM DUAL;

      RETURN NVL(V_RESULT, 0);

  END F_PLAN_DYIELD_BZ_ZYNJ_FTP; 
(1 rows, 20ms)
```

---

## 函数源码: `DD_DW.F_PLAN_YIELD_BZ` (长度 1251 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_YIELD_BZ" (I_PLANCODE  IN VARCHAR2,
                           I_STARTDATE IN VARCHAR2,
                           I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 计划收益率（标准现金流法+ 剔除归集户利息+ 剔除支付组合）
    *
    * 作 者： maple song
    * 创建日期：2020-03-10
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 计划代码、期初日期、期末日期
    *             传出 -> 计划收益率（标准现金流法+ 剔除归集户利息+ 剔除支付组合）

    \*****************************************************************************/
    V_RESULT NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';

    SELECT NVL((POWER(2, SUM(LOG(2, T.F_DP_YIELD_BZ + 1))) - 1), 0)
      INTO V_RESULT
      FROM MPRF_F_PLAN_DAYNETVALUE T
     WHERE T.VC_PLANCODE = I_PLANCODE
       AND T.D_DATE >= TO_DATE(I_STARTDATE, 'YYYY-MM-DD')
       AND T.D_DATE <= TO_DATE(I_ENDDATE, 'YYYY-MM-DD')
       AND T.F_DP_YIELD_BZ > -1;
    RETURN NVL(V_RESULT, 0);
  END F_PLAN_YIELD_BZ; 
(1 rows, 29ms)
```

---

## 函数源码: `DD_DW.F_PLAN_YIELD_BZ_TCG` (长度 1277 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_YIELD_BZ_TCG" (I_PLANCODE  IN VARCHAR2,
                               I_STARTDATE IN VARCHAR2,
                               I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 计划收益率（标准现金流法+ 剔除归集户利息+ 不剔除支付组合）
    *
    * 作 者： maple song
    * 创建日期：2020-03-10
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 计划代码、期初日期、期末日期
    *             传出 -> 计划收益率（标准现金流法+ 剔除归集户利息+ 不剔除支付组合）

    \*****************************************************************************/
    V_RESULT NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';

    SELECT NVL((POWER(2, SUM(LOG(2, T.F_DP_YIELD_BZ_TCG + 1))) - 1), 0)
      INTO V_RESULT
      FROM MPRF_F_PLAN_DAYNETVALUE T
     WHERE T.VC_PLANCODE = I_PLANCODE
       AND T.D_DATE >= TO_DATE(I_STARTDATE, 'YYYY-MM-DD')
       AND T.D_DATE <= TO_DATE(I_ENDDATE, 'YYYY-MM-DD')
       AND T.F_DP_YIELD_BZ_TCG > -1;
    RETURN NVL(V_RESULT, 0);
  END F_PLAN_YIELD_BZ_TCG; 
(1 rows, 31ms)
```

---

## 函数源码: `DD_DW.F_PLAN_YIELD_BZ_ZYNJ` (长度 1265 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_YIELD_BZ_ZYNJ"(--I_PLANCODE  IN VARCHAR2,
                           I_STARTDATE IN VARCHAR2,
                           I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 计划收益率（标准现金流法+ 剔除归集户利息+ 剔除支付组合）
    *
    * 作 者： WZ
    * 创建日期：2026-01-07
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 期初日期、期末日期
    *             传出 -> 职年整体的区间时间加权收益率

    \*****************************************************************************/
    V_RESULT NUMBER;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';

  SELECT NVL((POWER(2, SUM(LOG(2, F_DP_YIELD_BZ + 1))) - 1), 0)
    INTO V_RESULT
    FROM (select F_PLAN_DYIELD_BZ_ZYNJ(T.D_DATE) F_DP_YIELD_BZ
            from MDIM_SYS_TIME T
           WHERE T.D_DATE BETWEEN TO_DATE(I_STARTDATE, 'YYYY-MM-DD') AND
                 TO_DATE(I_ENDDATE, 'YYYY-MM-DD'))
            where F_DP_YIELD_BZ > -1;
  RETURN NVL(V_RESULT, 0);




  END F_PLAN_YIELD_BZ_ZYNJ; 
(1 rows, 30ms)
```

---

## 函数源码: `DD_DW.F_PLAN_NHYIELD_BZ` (长度 2596 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_NHYIELD_BZ" (I_PLANCODE  IN VARCHAR2,
                            I_STARTDATE IN VARCHAR2,
                            I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
  /*****************************************************************************\
  *                           长江养老投资数据中心
  *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
  * ===========================================================================
  *
  * 函数名：计划层指标 - 年化收益率（标准现金流法+ 不剔除归集户利息+ 不剔除支付组合）
  *
  * 作 者： ZHANG KAIYUE
  * 创建日期：2020-04-23
  * 版  本  号：1.1.1
  *
  * 参      数：传入 -> 计划代码、期初日期、期末日期
  *             传出 -> 年化收益率（标准现金流法+ 不剔除归集户利息+ 不剔除支付组合）
    修改记录：2020-07-30  zky   将本年天数修改为固定值365
  \*****************************************************************************/
  V_RESULT NUMBER;
  --V_YDAYS       NUMBER;
  V_QDAYS       NUMBER;
  V_YIELD_BZ    NUMBER; --区间收益率
  V_SDATE       DATE;
  V_EDATE       DATE;
  V_CREATE_DATE DATE;
  V_MAXDATE     DATE; -- 最大日期
  V_CNT         NUMBER;
  v_pcode       VARCHAR2(100);
 BEGIN
  EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
  V_SDATE := TO_DATE(I_STARTDATE, 'YYYY-MM-DD');
  V_EDATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');

  SELECT t.vc_plan_code,min(T.D_CREATE_DATE) ,
         max(LEAST(V_EDATE, DECODE(T.D_END_DATE, NULL, DATE '2099-12-31', T.D_EDATE)))
    INTO v_pcode,V_CREATE_DATE, V_MAXDATE
    FROM MDIM_fund_INFO T
   WHERE T.VC_planCODE = I_PLANCODE
   GROUP BY vc_plan_code;

  SELECT COUNT(1)
    INTO V_CNT
    FROM MPRF_F_PLAN_DAYNETVALUE T
   WHERE T.VC_PLANCODE = v_pcode
     AND T.D_DATE = V_MAXDATE
     AND T.F_DP_YIELD_BZ IS NOT NULL;

  IF V_CNT = 0 THEN
   RETURN 0;
  ELSE

   IF V_MAXDATE < V_SDATE THEN
    V_RESULT := 0;
   ELSE
    IF V_MAXDATE < V_CREATE_DATE THEN
     V_RESULT := 0;
    ELSE

     /*SELECT ADD_MONTHS(TRUNC(V_MAXDATE, 'YYYY'), 12) -
          TRUNC(V_MAXDATE, 'YYYY')
     INTO V_YDAYS
     FROM DUAL;*/

     IF V_SDATE < V_CREATE_DATE THEN
      SELECT V_MAXDATE - V_CREATE_DATE + 1 INTO V_QDAYS FROM DUAL;
     ELSE
      SELECT V_MAXDATE - V_SDATE + 1 INTO V_QDAYS FROM DUAL;
     END IF;

     V_YIELD_BZ := F_PLAN_YIELD_BZ(v_pcode,
                                                 I_STARTDATE,
                                                 I_ENDDATE);

     V_RESULT := 0;
     IF V_QDAYS = 0 THEN
      V_RESULT := 0;
     ELSE
      --V_RESULT := V_YDAYS * V_YIELD_BZ / V_QDAYS;
      V_RESULT := 365 * V_YIELD_BZ / V_QDAYS;
     END IF;
    END IF;
   END IF;
  END IF;
  RETURN NVL(V_RESULT, 0);

 END F_PLAN_NHYIELD_BZ; 
(1 rows, 29ms)
```

---

## 函数源码: `DD_DW.F_PLAN_STBC` (长度 1221 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_STBC" (I_PLANCODE  IN VARCHAR2,
                               I_STARTDATE IN VARCHAR2,
                               I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 受托业绩报酬
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
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_EDATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');



    SELECT NVL(SUM(T.F_PRICE), 0)
      INTO V_RESULT
      FROM MFACTGZ_FUND_HLDDETAIL T
     WHERE T.VC_FUNDCODE  IN (SELECT VC_FUNDCODE FROM MDIM_FUND_INFO WHERE VC_PLAN_CODE = I_PLANCODE)
       AND T.D_DATE = V_EDATE
       AND T.VC_SYMBOL = '221002';
    RETURN NVL(V_RESULT, 0);

  END F_PLAN_STBC; 
(1 rows, 20ms)
```

---

## 函数源码: `DD_DW.F_PLAN_TGBC` (长度 1221 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_TGBC" (I_PLANCODE  IN VARCHAR2,
                               I_STARTDATE IN VARCHAR2,
                               I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 托管业绩报酬
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
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_EDATE := TO_DATE(I_ENDDATE, 'YYYY-MM-DD');



    SELECT NVL(SUM(T.F_PRICE), 0)
      INTO V_RESULT
      FROM MFACTGZ_FUND_HLDDETAIL T
     WHERE T.VC_FUNDCODE  IN (SELECT VC_FUNDCODE FROM MDIM_FUND_INFO WHERE VC_PLAN_CODE = I_PLANCODE)
       AND T.D_DATE = V_EDATE
       AND T.VC_SYMBOL = '220602';
    RETURN NVL(V_RESULT, 0);

  END F_PLAN_TGBC; 
(1 rows, 28ms)
```

---

## 函数源码: `DD_DW.F_PLAN_YJYX` (长度 1562 字符)

```sql
CREATE or replace  FUNCTION "DD_DW"."F_PLAN_YJYX" (I_PLANCODE  IN VARCHAR2,
                               I_STARTDATE IN VARCHAR2,
                               I_ENDDATE   IN VARCHAR2) RETURN NUMBER IS
    /*****************************************************************************\
    *                           长江养老投资数据中心
    *           COPYRIGHT (C) 2020, 卓沃信息技术(上海)有限公司
    * ===========================================================================
    *
    * 函数名：计划层指标 - 业绩报酬对计划业绩影响
    *
    * 作 者： maple song
    * 创建日期：2020-02-28
    * 版  本  号：1.1.1
    *
    * 参      数：传入 -> 组合代码、期初日期、期末日期
    *             传出 -> 期末资产净值

    \*****************************************************************************/
    V_RESULT  NUMBER;


    V_DATE    DATE;

    ENDDATE   DATE;
  BEGIN
    EXECUTE IMMEDIATE 'ALTER SESSION SET NLS_DATE_FORMAT=''YYYY-MM-DD''';
    V_DATE        := TO_DATE(I_STARTDATE, 'YYYY-MM-DD');
    ENDDATE       := TO_DATE(I_ENDDATE,'YYYY-MM-DD');
    V_RESULT      := 0;


    SELECT DECODE(F_NETVALUE,0,0,(STBC+TGBC)/F_NETVALUE) INTO V_RESULT FROM(
    (SELECT F_PLAN_STBC(I_PLANCODE,I_STARTDATE,TO_CHAR(ENDDATE,'YYYY-MM-DD')) STBC,
            F_PLAN_TGBC(I_PLANCODE,I_STARTDATE,TO_CHAR(ENDDATE,'YYYY-MM-DD')) TGBC,
            DD_DW.DW_ZNST_INDEX.F_PLAN_END_NETVALUE(I_PLANCODE,I_STARTDATE,TO_CHAR(ENDDATE-1,'YYYY-MM-DD')) F_NETVALUE
                             FROM MDIM_PLAN_INFO
                             WHERE VC_PLAN_LIC_ID = I_PLANCODE)) ;

    RETURN NVL(V_RESULT,0) ;
    END F_PLAN_YJYX ; 
(1 rows, 29ms)
```

---
