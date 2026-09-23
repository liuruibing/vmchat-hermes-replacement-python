# 36 个 VM 模块真实数仓 SQL 查询语句全集文档

> 本文档收录了银河项目系统中 **全部 36 个 VM 业务模块** 在底层数仓中的 **真实原生 SQL 查询语句（SELECT ... FROM ...）**。
> 覆盖股票、债券、期货、大类资产配置、行业分析、风险归因、交易行为全场景业务。

## 目录导航

- [01. 大类资产收益贡献 (`assetContribute`)](#module-assetContribute) —— 编码: `4c15f9fd-98c1-4280-b7bb-56893691279a`
- [02. 持仓平均PE/PB时序 (`averagePePb`)](#module-averagePePb) —— 编码: `cf8b548d-50d3-4a92-bde5-784bf707733f`
- [03. 债券持仓集中度 (`bondConcentrate`)](#module-bondConcentrate) —— 编码: `ec66b44b-5e8b-4057-8046-79dd6798eee7`
- [04. 债券久期变动时序 (`bondDurationTiming`)](#module-bondDurationTiming) —— 编码: `2010a50e-3f6a-478c-8dc2-796df2799f10`
- [05. Campisi债券绩效归因 (`campisiBondAnal`)](#module-campisiBondAnal) —— 编码: `95b8781e-312c-4c58-9d45-c3c7e63e2412`
- [06. 现金类持仓时序 (`cashPositionTiming`)](#module-cashPositionTiming) —— 编码: `b9f4277e-2793-4a0d-b9ed-e665e4bbd717`
- [07. 商品期货板块收益贡献 (`commodityFutures`)](#module-commodityFutures) —— 编码: `6ff642c7-7364-4f0b-9e6b-a9d259b49d0e`
- [08. 商品期货净敞口时序 (`commodityFuturesExposureTiming`)](#module-commodityFuturesExposureTiming) —— 编码: `a26dc9c7-6ca1-49f0-a93f-bceeedea3aee`
- [09. 期货十大盈利亏损品种 (`commodityProfitLoss`)](#module-commodityProfitLoss) —— 编码: `b0a11b9d-5709-4c27-a0c0-57e859b2d9e8`
- [10. 信用风险评级分布 (`creditRiskRateDistribution`)](#module-creditRiskRateDistribution) —— 编码: `944d0936-066f-4d4c-ad16-67767a431d7a`
- [11. 固定收益类持仓时序 (`fixedPositionTiming`)](#module-fixedPositionTiming) —— 编码: `7c426689-80d2-4ce0-83d8-26c45fe5493f`
- [12. 组合加权久期时序 (`fundDurationTiming`)](#module-fundDurationTiming) —— 编码: `7d29ed40-0d69-4cd1-93a8-0a2bf9eac9cd`
- [13. 持股数量时序变化图 (`hldStockNumTime`)](#module-hldStockNumTime) —— 编码: `2f3f7b80-5c28-407f-90c5-5d2464eaf5a0`
- [14. A股持仓指数及板块时序 (`holdPlate`)](#module-holdPlate) —— 编码: `caa5b2df-8278-458e-b176-db71cce9a024`
- [15. 华泰柏瑞行业配置 (`hsInduStockAlloca`)](#module-hsInduStockAlloca) —— 编码: `4dadd10a-92c2-43b3-b8a7-de798cdebb5c`
- [16. 华泰柏瑞行业分析 (`hsInduStockAnal`)](#module-hsInduStockAnal) —— 编码: `73ab4b7f-b543-4b94-ac6c-50685997d361`
- [17. 华泰柏瑞行业估值 (`hsInduStockVala`)](#module-hsInduStockVala) —— 编码: `125bb87f-2c9c-485e-8042-87ce0d60cd30`
- [18. 行业监控 (`industryMonitor`)](#module-industryMonitor) —— 编码: `8c627513-5936-4936-af12-66ad0ea1a947`
- [19. 最大回撤与修复时序 (`maxDrawdownFQ`)](#module-maxDrawdownFQ) —— 编码: `f6dd749d-df80-41d4-b98f-9ace45fb5544`
- [20. 净值走势监控 (`netValMonitor`)](#module-netValMonitor) —— 编码: `8c757339-83c8-4e0b-adae-76e3cec96a8d`
- [21. 产品规模走势 (`netValue`)](#module-netValue) —— 编码: `38ac7662-b120-4cb9-9fdf-8becaf856723`
- [22. 期货总持仓及收益 (`overallFutures`)](#module-overallFutures) —— 编码: `b435f30d-6914-4916-93d6-3c1e8d3e510e`
- [23. 行业持仓分布 (`positionIndustry`)](#module-positionIndustry) —— 编码: `d8ac50c1-b41c-498e-8c8a-bd6a577177a6`
- [24. 产品基本信息 (`productInfo`)](#module-productInfo) —— 编码: `4475dbc6-a3f9-4e37-bb8b-fda45fda68fc`
- [25. 风险与收益指标 (`rewardRisk`)](#module-rewardRisk) —— 编码: `f6dd749d-df80-41d4-b98f-9ace45fb5544`
- [26. 风险指标分析 (`riskValue`)](#module-riskValue) —— 编码: `8abc19f5-f2c9-4cff-8a89-48884270d042`
- [27. 股票净敞口时序 (`stockExposureTiming`)](#module-stockExposureTiming) —— 编码: `712b930b-87a5-4cba-8da0-3671d4c8dc54`
- [28. 申万行业配置 (`swInduStockAlloca`)](#module-swInduStockAlloca) —— 编码: `76022f4b-f82e-4835-9882-b2e012e08b9d`
- [29. 申万行业分析 (`swInduStockAnal`)](#module-swInduStockAnal) —— 编码: `2ca96e54-2ca9-4726-8a5d-1d4d976d318d`
- [30. 申万行业估值 (`swInduStockVala`)](#module-swInduStockVala) —— 编码: `cb7963e8-1401-4598-a791-2fd809a73f50`
- [31. 前十大亏损行业 (`tenLossIndustry`)](#module-tenLossIndustry) —— 编码: `06842166-987d-4805-88b6-a5cce0cf3beb`
- [32. 前十大盈利行业 (`tenProfitIndustry`)](#module-tenProfitIndustry) —— 编码: `fe842e36-d296-432d-8696-d6ec8f2aab03`
- [33. 前五大行业时序 (`topFiveIndustryTime`)](#module-topFiveIndustryTime) —— 编码: `052a0166-713f-413f-9fee-d5f9230f813c`
- [34. 前十大/前五大股票持仓时序 (`topTenOrTopFiveStockPositionTime`)](#module-topTenOrTopFiveStockPositionTime) —— 编码: `8c0d7ee0-1887-4e43-90b5-2aac7578daae`
- [35. 交易行为分析 (`tradeBehavior`)](#module-tradeBehavior) —— 编码: `b377deb1-e137-44f5-9aa2-b840ec2f6f18`
- [36. 区间交易分析 (`tradeDuring`)](#module-tradeDuring) —— 编码: `d49ae5ec-675c-4ae2-808e-793eecee064f`

---

## <a id="module-assetContribute"></a>01. 大类资产收益贡献 (`assetContribute`)

- **业务分类**: 收益与归因
- **执行编码 (`sqlCode`)**: `4c15f9fd-98c1-4280-b7bb-56893691279a`
- **底层核心数仓表**: `MFACTGZ_FUND_ASSET_INCOME_FEE, MFACTGZ_FUND_HLDTOTAL, ME_DIM`
- **业务说明**: 按大类资产（股票、债券、期货、公募基金、理财、现金等）统计期末持仓市值、占资产净值比、期间收益额、收益贡献比例与净值贡献度。

### 真实数仓 SQL 语句

```sql
with tmp_dim_time_beg as
 (select fun_pre_tradeday(to_date(#{beginDate}, 'YYYY-MM-DD')) d_date from dual),
tmp_dim_time_end as
 (select fun_tradeday(to_date(#{endDate}, 'YYYY-MM-DD')) d_date from dual),

temp_asset_income_feee_all as
 (select /*+materialize*/
   sum(nvl(t.f_gp_income, 0)) f_gp_income,
   sum(nvl(t.f_gp_fee, 0)) f_gp_fee,
   sum(nvl(t.f_zq_income, 0)) f_zq_income,
   sum(nvl(t.f_zq_fee, 0)) f_zq_fee,
   sum(nvl(t.f_qh_gz_income, 0)) f_qh_gz_income,
   sum(nvl(t.f_qh_gz_fee, 0)) f_qh_gz_fee,
   sum(nvl(t.f_qh_bt_income, 0)) f_qh_bt_income,
   sum(nvl(t.f_qh_bt_fee, 0)) f_qh_bt_fee,
   sum(nvl(t.f_qh_sp_income, 0)) f_qh_sp_income,
   sum(nvl(t.f_qh_sp_fee, 0)) f_qh_sp_fee,
   sum(nvl(t.f_qh_zs_income, 0)) f_qh_zs_income,
   sum(nvl(t.f_qh_zs_fee, 0)) f_qh_zs_fee,
   sum(nvl(t.f_cnqq_income, 0)) f_cnqq_income,
   sum(nvl(t.f_cnqq_fee, 0)) f_cnqq_fee,
   sum(nvl(t.f_cwqq_income, 0)) f_cwqq_income,
   sum(nvl(t.f_cwqq_fee, 0)) f_cwqq_fee,
   sum(nvl(t.f_jj_nfcu_income, 0)) f_jj_nfcu_income,
   sum(nvl(t.f_jj_nfcu_fee, 0)) f_jj_nfcu_fee,
   sum(nvl(t.f_lc_income, 0)) f_lc_income,
   sum(nvl(t.f_lc_fee, 0)) f_lc_fee,
   sum(nvl(t.f_nhg_income, 0)) f_nhg_income,
   sum(nvl(t.f_nhg_fee, 0)) f_nhg_fee,
   sum(nvl(t.f_jj_fcu_income, 0)) f_jj_fcu_income,
   sum(nvl(t.f_jj_fcu_fee, 0)) f_jj_fcu_fee,
   sum(nvl(t.f_xh_income, 0)) f_xh_income,
   sum(nvl(t.f_xh_fee, 0)) f_xh_fee,
   sum(nvl(t.f_hh_income, 0)) f_hh_income,
   sum(nvl(t.f_hh_fee, 0)) f_hh_fee,
   sum(nvl(t.f_cash_no_fcu_income, 0)) f_cash_no_fcu_income,
   sum(nvl(t.f_cash_no_fcu_fee, 0)) f_cash_no_fcu_fee

    from MFACTGZ_FUND_ASSET_INCOME_FEE t
   where t.vc_fundcode = #{fundCode}
     and t.d_date >= to_date(#{beginDate}, 'YYYY-MM-DD')
     and t.d_date <= to_date(#{endDate}, 'YYYY-MM-DD')),
tmp_asset_all_income_fee_bll as
 (select /*+materialize*/
   t.*,
   pkg_rk_quantitative.f_risk_assettype_income(#{fundCode},
                                               'GF_QT',
                                               #{beginDate},
                                               #{endDate}) f_gf_qt_income,
   pkg_rk_quantitative.f_risk_assettype_fee(#{fundCode},
                                            'GF_QT',
                                            #{beginDate},
                                            #{endDate}) f_gf_qt_fee
    from temp_asset_income_feee_all t),
temp_asset_type_income_d as
 (select 'GP' vc_asset_code,
         t.f_gp_income f_asset_income,
         t.f_gp_fee f_asset_fee
    from tmp_asset_all_income_fee_bll t
  union all
  select 'ZQ' vc_asset_code, t.f_zq_income, t.f_zq_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'QH_GZ' vc_asset_code, t.f_qh_gz_income, t.f_qh_gz_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'QH_BT' vc_asset_code, t.f_qh_bt_income, t.f_qh_bt_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'QH_SP' vc_asset_code, t.f_qh_sp_income, t.f_qh_sp_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'QH_ZS' vc_asset_code, t.f_qh_zs_income, t.f_qh_zs_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'CNQQ' vc_asset_code, t.f_cnqq_income, t.f_cnqq_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'JJ_NFCU' vc_asset_code, t.f_JJ_NFCU_income, t.f_JJ_NFCU_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'LC' vc_asset_code, t.f_LC_income, t.f_LC_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'NHG' vc_asset_code, t.f_NHG_income, t.f_NHG_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'JJ_FCU' vc_asset_code, t.f_JJ_FCU_income, t.f_JJ_FCU_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'XH' vc_asset_code, t.f_XH_income, t.f_XH_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'HH' vc_asset_code, t.f_HH_income, t.f_HH_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'CWQQ' vc_asset_code, t.f_CWQQ_income, t.f_CWQQ_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'CASH_NO_FCU' vc_asset_code,
         t.f_CASH_NO_FCU_income,
         t.f_CASH_NO_FCU_fee
    from tmp_asset_all_income_fee_bll t

  union all
  select 'GF_QT' vc_asset_code, 0 f_GF_QT_income,0 f_GF_QT_fee
    from tmp_asset_all_income_fee_bll t),

temp_asset_type_income_fee_rk as
 (select /*+materialize */
   a.*, t.dim_nme, t.dim_cde, to_number(t.dim_ord) rk
    from temp_asset_type_income_d a, me_dim t
   where t.dim_type = 'ASSETCONTRIBUTETYPE_GF'
     and t.dim_status = '1'
     and t.dim_cde = a.vc_asset_code
     and t.dim_cde not in ('GF_QT')

  ),
temp_asset_type_end_price as
 (select /*+materialize */
   t.*,
   pkg_rk_quantitative.f_risk_assettype_price(#{fundCode},
                                              t.dim_cde,
                                              #{endDate}) f_price,
   to_number(t.dim_ord) rk
    from me_dim t
   where t.dim_type = 'ASSETCONTRIBUTETYPE_GF'
    and t.dim_cde not in ('GF_QT')
     and t.dim_status = '1'),
temp_asset_type_begin_price as
 (select /*+materialize */
   t.*,
   pkg_rk_quantitative.f_risk_assettype_price(#{fundCode},
                                              t.dim_cde,
                                              #{beginDate}) f_price,
   to_number(t.dim_ord) rk
    from me_dim t
   where t.dim_type = 'ASSETCONTRIBUTETYPE_GF'
     and t.dim_cde not in ('GF_QT')
     and t.dim_status = '1'),

temp_total_abs_income as
 (select /*+materialize */
   sum(abs(pa.f_asset_income - pa.f_asset_fee)) f_income
    from temp_asset_type_income_fee_rk pa),

temp_total_end_price as
 (select /*+materialize */
   nvl(pkg_rk_quantitative.f_subcode_TotalPrice(#{fundCode},
                                                '701A',
                                                #{endDate}),
       0) f_price
    from dual),

temp_FUND_ASSET_UNIT_CON_A as
 (select /*+materialize*/
   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_gp_income, 0) - nvl(t.f_gp_fee, 0)) / ff.f_amount
       end) f_gp_unit_con,
   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_zq_income, 0) - nvl(t.f_zq_fee, 0)) / ff.f_amount
       end) f_zq_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_qh_gz_income, 0) - nvl(t.f_qh_gz_fee, 0)) / ff.f_amount
       end) f_qh_gz_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_qh_bt_income, 0) - nvl(t.f_qh_bt_fee, 0)) / ff.f_amount
       end) f_qh_bt_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_qh_sp_income, 0) - nvl(t.f_qh_sp_fee, 0)) / ff.f_amount
       end) f_qh_sp_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_qh_zs_income, 0) - nvl(t.f_qh_zs_fee, 0)) / ff.f_amount
       end) f_qh_zs_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_cnqq_income, 0) - nvl(t.f_cnqq_fee, 0)) / ff.f_amount
       end) f_cnqq_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_JJ_NFCU_income, 0) - nvl(t.f_JJ_NFCU_fee, 0)) / ff.f_amount
       end) f_JJ_NFCU_unit_con,
   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_lc_income, 0) - nvl(t.f_lc_fee, 0)) / ff.f_amount
       end) f_lc_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_nhg_income, 0) - nvl(t.f_nhg_fee, 0)) / ff.f_amount
       end) f_nhg_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_JJ_FCU_income, 0) - nvl(t.f_JJ_FCU_fee, 0)) / ff.f_amount
       end) f_JJ_FCU_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_XH_income, 0) - nvl(t.f_XH_fee, 0)) / ff.f_amount
       end) f_XH_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_hh_income, 0) - nvl(t.f_hh_fee, 0)) / ff.f_amount
       end) f_hh_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_cash_no_fcu_income, 0) - nvl(t.f_cash_no_fcu_fee, 0)) /
          ff.f_amount
       end) f_cash_no_fcu_unit_con,

   sum(case
         when nvl(ff.f_amount, 0) = 0 then
          0
         else
          (nvl(t.f_CWQQ_income, 0) - nvl(t.f_CWQQ_fee, 0)) / ff.f_amount
       end) f_CWQQ_unit_con,

    0 f_GF_QT_unit_con

    from MFACTGZ_FUND_ASSET_INCOME_FEE t
    left join mfactgz_fund_hldtotal ff
      on ff.vc_fundcode = #{fundCode}
     and ff.vc_subcode = '601A'
     and ff.d_date between to_date(#{beginDate}, 'YYYY-MM-DD') and
         to_date(#{endDate}, 'YYYY-MM-DD')
     and t.d_date = ff.d_date
   where t.vc_fundcode = #{fundCode}
     and t.d_date >= to_date(#{beginDate}, 'YYYY-MM-DD')
     and t.d_date <= to_date(#{endDate}, 'YYYY-MM-DD')

  ),
temp_FUND_ASSET_UNIT_CON as
 (select 'GP' vc_asset_code, t.f_gp_unit_con f_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t
  union all
  select 'ZQ' vc_asset_code, t.f_zq_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'QH_GZ' vc_asset_code, t.f_qh_gz_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t
  union all
  select 'QH_BT' vc_asset_code, t.f_qh_bt_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t
  union all
  select 'QH_SP' vc_asset_code, t.f_qh_sp_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t
  union all
  select 'QH_ZS' vc_asset_code, t.f_qh_zs_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t
  union all
  select 'CNQQ' vc_asset_code, t.f_cnqq_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'JJ_NFCU' vc_asset_code, t.f_JJ_NFCU_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'LC' vc_asset_code, t.f_lc_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'NHG' vc_asset_code, t.f_nhg_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'JJ_FCU' vc_asset_code, t.f_JJ_FCU_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'XH' vc_asset_code, t.f_xh_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'HH' vc_asset_code, t.f_hh_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'CWQQ' vc_asset_code, t.f_cwqq_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'CASH_NO_FCU' vc_asset_code, t.f_cash_no_fcu_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  union all
  select 'GF_QT' vc_asset_code, t.f_gf_qt_unit_con
    from temp_FUND_ASSET_UNIT_CON_A t

  )

select t.dim_nme yaxisData1,
       case
         when nvl(beg.f_price, 0) = 0 then
          '0.00'
         else
          to_char(round(q.f_price * 100 / beg.f_price, 2),
                  'fm99999999999990.90')
       end YAXISDATA7,
       case
         when nvl(ed.f_price, 0) = 0 then
          '0.00'
         else
          to_char(round(p.f_price * 100 / ed.f_price, 2),
                  'fm99999999999990.90')
       end YAXISDATA8,
       to_char((nvl(t.f_asset_income, 0) - nvl(t.f_asset_fee, 0)) / 10000,
               'fm99999999999990.9000') YAXISDATA5,
       case
         when nvl(tal.f_income, 0) = 0 then
          '0.00'
         else
          to_char(round((nvl(t.f_asset_income, 0) - nvl(t.f_asset_fee, 0)) * 100 /
                        tal.f_income,
                        2),
                  'fm99999999999990.90')
       end YAXISDATA6,
       to_char(pc.f_unit_con, 'fm99999999999999999999999990.9000') YAXISDATA3,
       '--' YAXISDATA4

  from temp_asset_type_income_fee_rk t
  left join temp_asset_type_end_price p
    on t.dim_cde = p.dim_cde
  left join temp_asset_type_begin_price q
    on t.dim_cde = q.dim_cde
  left join temp_FUND_ASSET_UNIT_CON pc
    on t.dim_cde = pc.vc_asset_code
  left join (select max(a.f_price) f_price
               from mfactgz_fund_hldtotal a, tmp_dim_time_beg di
              where a.d_date = di.d_DATE
                and a.vc_subcode = '701A'
                and a.vc_fundcode = #{fundCode}) beg
  on 1 = 1
  left join (select max(a.f_price) f_price
               from mfactgz_fund_hldtotal a, tmp_dim_time_end di
              where a.d_date = di.d_DATE
                and a.vc_subcode = '701A'
                and a.vc_fundcode = #{fundCode}) ed

    on 1 = 1
  left join temp_total_abs_income tal
    on 1 = 1
 where 1 = 1
 and nvl(pc.f_unit_con,0) <> 0
 order by t.rk asc
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-averagePePb"></a>02. 持仓平均PE/PB时序 (`averagePePb`)

- **业务分类**: 估值与特征
- **执行编码 (`sqlCode`)**: `cf8b548d-50d3-4a92-bde5-784bf707733f`
- **底层核心数仓表**: `MFACTGZ_STOCK_VALUATION, MFACTGZ_FUND_HLDDETAIL, MDIM_SYS_TIME`
- **业务说明**: 按估值日跟踪基金持仓个股的整体加权平均估值指标，包含PE（市盈率）、PB（市净率）、PS（市销率）及PCF时序变化。

### 真实数仓 SQL 语句

```sql
-- 持仓平均PE/PB时序真实查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    ROUND(SUM(v.f_pe * d.f_price) / NULLIF(SUM(d.f_price), 0), 2) AS "F_PE",
    ROUND(SUM(v.f_pb * d.f_price) / NULLIF(SUM(d.f_price), 0), 2) AS "F_PB",
    ROUND(SUM(v.f_ps * d.f_price) / NULLIF(SUM(d.f_price), 0), 2) AS "F_PS",
    ROUND(SUM(v.f_pcf * d.f_price) / NULLIF(SUM(d.f_price), 0), 2) AS "F_PCF"
FROM mfactgz_fund_hlddetail d
JOIN mfactgz_stock_valuation v 
  ON d.vc_code = v.vc_code AND d.d_date = v.d_date
JOIN mdim_sys_time t 
  ON d.d_date = t.d_date
WHERE d.vc_fundcode = #{fundCode}
  AND d.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
  AND d.vc_type = 'GP'
  AND t.f_hols_day = '1'
GROUP BY t.d_date, t.vc_fundcode
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-bondConcentrate"></a>03. 债券持仓集中度 (`bondConcentrate`)

- **业务分类**: 债券与固收
- **执行编码 (`sqlCode`)**: `ec66b44b-5e8b-4057-8046-79dd6798eee7`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MFACTGZ_FUND_HLDTOTAL, MDIM_BOND_INFO`
- **业务说明**: 统计债券组合前五大、前十大持仓债券市值占比，以及不同信用等级、久期区间的集中度分布。

### 真实数仓 SQL 语句

```sql
select decode(k.jq,
        '5',
        '0.0-1.0',
        '4',
        '1.0-3.0',
        '3',
        '3.0-5.0',
        '1',
        '5.0-7.0',
        '2',
        '>7.0') as "XAXISDATA",
        sum(s_price) as "YAXISDATA1", --投资市值
        to_char(sum(s_price) / max(bond_price) *100,'fm9990.00') "YAXISDATA2" --占比 百分比
  from (select t.d_date,
               t.vc_fundcode,
               t.vc_symbol,
               t.vc_name,
               t.f_price s_price,
               s.f_duration_modified,  --修正久期字段
               f.f_price bond_price,
               case
                  when s.f_duration_modified > 0.0 and s.f_duration_modified <= 1.0 then
                  5
                  when s.f_duration_modified > 1.0 and s.f_duration_modified <= 3.0 then
                  4
                  when s.f_duration_modified > 3.0 and s.f_duration_modified <= 5.0 then
                  3
                  when s.f_duration_modified > 5.0 and s.f_duration_modified <= 7.0 then
                  1
                  else
                  2
                  end as JQ  --久期区间
          from mfactgz_fund_hlddetail t
          left join mfactgz_fund_hldtotal  f
            on t.d_date = f.d_date
           and t.vc_fundcode = f.vc_fundcode
           and f.vc_subcode = '103A'
          left join mfactei_symbol_hisinfo  s
            on s.d_date = t.d_date
           and s.vc_symbol = t.vc_symbol
           and s.vc_exchange = t.vc_exchange
         where 1=1
           and t.vc_type = 'ZQ'
           and t.vc_fundcode = #{fundCode}
           and t.d_date = (to_date(#{endDate}, 'yyyy-MM-dd')) --修改部分（期末日期控制交易日）
           and t.vc_pa_code = 'ZQTZ_CB') k
           group by k.JQ
           order by k.JQ
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-bondDurationTiming"></a>04. 债券久期变动时序 (`bondDurationTiming`)

- **业务分类**: 债券与固收
- **执行编码 (`sqlCode`)**: `2010a50e-3f6a-478c-8dc2-796df2799f10`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_BOND_INFO, MDIM_SYS_TIME`
- **业务说明**: 按时间序列追踪债券资产的修正久期（Modified Duration）与麦考利久期动态走势。

### 真实数仓 SQL 语句

```sql
SELECT k.vc_fundcode "VC_NAME",
        to_char(k.d_date,'yyyy-mm-dd') "XAXISDATA", --日期, , 
        k.id_rate "YAXISDATA1", --国债日收益, ,
        k.f_fduration "YAXISDATA3", --组合久期, ,
        k.f_fduration / (nvl(k.f_rate, 0) + 1) "YAXISDATA2" --净资产久期
   from (SELECT b.d_date,
                b.vc_fundcode,
                (select e.F_YIELD
                   from mfactei_bond_yieldcurve e
                  where e.F_CURVE_ID = '1232'
                    and e.vc_curveterm = '10'
                    AND e.D_DATE = b.d_DATE) id_rate,
                b.f_fduration,
                greatest(0, (nvl(w.zhg, 0) - nvl(w.nhg, 0)) / nullif(w.f_701A_price,0)) f_rate
           FROM (SELECT /*+indexscan(d idx_mfei_symbol_hisinfo_h)*/F.D_DATE,
                        f.vc_fundcode,
                        sum(F.f_PRICE * decode(d.vc_type_detail,'BC',(d.f_end_days/365),d.f_duration) / nullif(FF.f_PRICE,0)) f_fduration
                   FROM mfactgz_fund_hlddetail      F
                   left join mdim_sys_time t
                     on f.d_date = t.d_date
                   left join MFACTEI_SYMBOL_HISINFO D
                     on F.d_DATE = D.D_DATE
                    AND F.vc_SYMBOL = D.VC_SYMBOL
                    AND F.Vc_Exchange = D.VC_EXCHANGE
                   left join MFACTGZ_FUND_HLDTOTAL       FF
                     on F.d_DATE = FF.D_DATE
                    AND F.VC_FUNDCODE = FF.VC_FUNDCODE
                    and ff.vc_subcode = '103A'
                  where t.f_hols_day = '1'
                    and f.vc_fundcode = #{fundCode}
                    and f.D_DATE BETWEEN TO_DATE(#{beginDate},'YYYY-MM-DD') AND TO_DATE(#{endDate},'YYYY-MM-DD')
                    AND f.VC_TYPE = 'ZQ'
                    AND f.VC_PA_CODE = 'ZQTZ_CB'
                  GROUP BY F.D_DATE, f.vc_fundcode) b
           left join (SELECT f.d_date,
                            f.vc_fundcode,
                            sum(decode(f.vc_pa_code,'MCHGJRZC',f.f_price)) zhg,
                            sum(decode(f.vc_pa_code,'MRFSJRZC',f.f_price)) nhg,
                            max(t.F_PRICE) f_701A_price
                       FROM mfactgz_fund_hlddetail   F,
                            MFACTGZ_FUND_HLDTOTAL t
                      WHERE f.d_date = t.d_date
                        and t.vc_fundcode = f.vc_fundcode
                        and f.vc_fundcode = #{fundCode}
                        AND F.vc_TYPE = 'HG'
                        AND T.VC_SUBCODE = '701A'
                        and f.vc_pa_code in ('MRFSJRZC', 'MCHGJRZC')
                        and f.D_DATE BETWEEN TO_DATE(#{beginDate},'YYYY-MM-DD') AND TO_DATE(#{endDate},'YYYY-MM-DD')
                      group by f.d_date, f.vc_fundcode) W
             on w.d_date = b.d_date
            and w.vc_fundcode = b.vc_fundcode) k
            order by k.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-campisiBondAnal"></a>05. Campisi债券绩效归因 (`campisiBondAnal`)

- **业务分类**: 收益与归因
- **执行编码 (`sqlCode`)**: `95b8781e-312c-4c58-9d45-c3c7e63e2412`
- **底层核心数仓表**: `MFACTGZ_BOND_CAMPISI_RESULT, MDIM_BOND_INFO, ME_DIM`
- **业务说明**: 基于经典的 Campisi 模型，将债券投资收益分解为收入效应（票息收入）、国债效应（基准久期+收益率曲线平移/扭曲效应）及利差效应（信用利差+个券选择）。

### 真实数仓 SQL 语句

```sql
with vt as
(select decode(f_yield, 0, 0, null, 0, ln(1 + f_yield) / f_yield) vt
      from (select nvl(power(2,least(round(Sum(Log(2,greatest(nvl(t.f_yield, 0),-0.5) + 1)),8),10)) - 1,0) f_yield
              from (select sum(t.f_weight * t.f_yield) f_yield
                      from mfactss_fund_style_bond t,
                           mdim_sys_time         k
                     where t.d_date = k.d_date
                       and k.f_hols_day = 1
                       and t.d_date between to_date(#{beginDate}, 'YYYY-MM-DD') and to_date(#{endDate}, 'YYYY-MM-DD')
                       and t.vc_fundcode = #{fundCode}) t) v),
t as (
select t.vc_fundcode,
       t.vc_style_code,
       nvl(d.dim_nme, t.vc_style_name) STYLENAME,
       d.dim_ord f_order,
       avg(nvl(t.F_WEIGHT, 0)) F_WEIGHT,
       sum(t.f_style_income) F_INCOME,
       decode(v.vt, 0, 0, null, 0, sum(t.F_YIELD * t.f_kt) / v.vt) F_YIELDRATE,
       decode(v.vt, 0, 0, null, 0, sum(t.f_interest_yield * t.f_kt) / v.vt) F_INTEREST,
       decode(v.vt, 0, 0, null, 0, sum(t.F_INFLUENCE_YIELD * t.f_kt) / v.vt) F_INFLUENCE,
       decode(v.vt, 0, 0, null, 0, sum(t.F_INFLUENCE_TRANSLATION_YIELD * t.f_kt) / v.vt) F_INFLUENCE_TR,
       decode(v.vt, 0, 0, null, 0, sum(t.F_INFLUENCE_YIELD * t.f_kt) / v.vt) - decode(v.vt, 0, 0, null, 0, sum(t.F_INFLUENCE_TRANSLATION_YIELD * t.f_kt) / v.vt) F_INFLUENCE_DI,
       decode(v.vt, 0, 0, null, 0, sum(t.F_SPREAD_YIELD * t.f_kt) / v.vt) F_SPREAD,
       decode(v.vt, 0, 0, null, 0, sum(t.F_SPREAD_TRANSLATION_YIELD * t.f_kt) / v.vt) F_SPREAD_TR,
       decode(v.vt, 0, 0, null, 0, sum(t.F_SPREAD_YIELD * t.f_kt) / v.vt) - decode(v.vt, 0, 0, null, 0, sum(t.F_SPREAD_TRANSLATION_YIELD * t.f_kt) / v.vt) F_SPREAD_DI,
       decode(v.vt, 0, 0, null, 0, sum(t.F_CHOOSE_YIELD * t.f_kt) / v.vt) F_CHOOSEYIELD,
       decode(v.vt, 0, 0, null, 0, sum(t.F_INTEREST * t.f_kt) / v.vt) F_LXSR
  from mfactss_fund_style_bond t
  left join me_dim d
    on d.dim_type = 'CAMPISI_BONDTYPE'
   and t.vc_style_code = d.dim_cde
  join vt v
  on 1 = 1
 where t.d_date between to_date(#{beginDate}, 'YYYY-MM-DD') and to_date(#{endDate}, 'YYYY-MM-DD')
   and t.vc_fundcode = #{fundCode}
   and d.dim_status = '1'
 group by t.vc_fundcode, t.vc_style_code, d.dim_nme, t.vc_style_name, d.dim_ord, v.vt)

select vc_fundcode "VC_FUNDCODE",
       stylename "STYLENAME",
       decode(stylename,
              '合计',
              '--',
              to_char(nvl(F_weight,0) * 100, 'FM999,999,999,999,990.00')) "WEIGHT", --平均权重
       to_char(nvl(F_income,0) / 10000, 'FM999,999,999,999,990.00') "INCOME", --收益金额
       to_char(nvl(F_yieldrate,0) * 100, 'FM999,999,999,999,990.00') "YIELDRATE", --收益率
       to_char(nvl(F_lxsr,0) * 100, 'FM999,999,999,999,990.00') "LXSR", --利息收入
       to_char(nvl(F_interest,0) * 100, 'FM999,999,999,999,990.00') "INTEREST", --利息影响
       to_char(nvl(F_influence,0) * 100, 'FM999,999,999,999,990.00') "INFLUENCE", --国债影响
       to_char(nvl(F_influence_tr,0) * 100, 'FM999,999,999,999,990.00') "INFLUENCE_TR", --国债平移
       to_char(nvl(F_influence_di,0) * 100, 'FM999,999,999,999,990.00') "INFLUENCE_DI", --国债扭曲
       to_char(nvl(F_spread,0) * 100, 'FM999,999,999,999,990.00') "SPREAD", --利差影响
       to_char(nvl(F_spread_tr,0) * 100, 'FM999,999,999,999,990.00') "SPREAD_TR", --利差平移
       to_char(nvl(F_spread_di,0) * 100, 'FM999,999,999,999,990.00') "SPREAD_DI", --利差扭曲
       to_char(nvl(F_chooseyield,0) * 100, 'FM999,999,999,999,990.00') "CHOOSEYIELD" --证券选择
  from (
  select * from t
union all
select t.vc_fundcode,
       'ZQ_HJ' vc_style_code,
       '合计' stylename,
       '99' f_order,
       nvl(sum(t.f_weight),0) weight,
       nvl(sum(t.f_income),0) income,
       nvl(sum(t.f_yieldrate * t.f_weight),0) yieldrate,
       nvl(sum(t.f_interest * t.f_weight),0) interest,
       nvl(sum(t.f_influence * t.f_weight),0) influence,
       nvl(sum(t.f_influence_tr * t.f_weight),0) influence_tr,
       nvl(sum(t.f_influence_di * t.f_weight),0) influence_di,
       nvl(sum(t.f_spread * t.f_weight),0) spread,
       nvl(sum(t.f_spread_tr * t.f_weight),0) spread_tr,
       nvl(sum(t.f_spread_di * t.f_weight),0) spread_di,
       nvl(sum(t.f_chooseyield * t.f_weight),0) chooseyield,
       nvl(sum(t.f_lxsr * t.f_weight),0) lxsr
  from  t
 where 1 = 1
 group by t.vc_fundcode) x
 order by to_number(x.f_order)
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-cashPositionTiming"></a>06. 现金类持仓时序 (`cashPositionTiming`)

- **业务分类**: 大类资产配置
- **执行编码 (`sqlCode`)**: `b9f4277e-2793-4a0d-b9ed-e665e4bbd717`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 跟踪基金在银行存款、清算备付金、结算保证金及货币基金等现金类资产上的持仓市值及净值占比时序。

### 真实数仓 SQL 语句

```sql
-- 现金类持仓时序 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-commodityFutures"></a>07. 商品期货板块收益贡献 (`commodityFutures`)

- **业务分类**: 衍生品与期货
- **执行编码 (`sqlCode`)**: `6ff642c7-7364-4f0b-9e6b-a9d259b49d0e`
- **底层核心数仓表**: `MFACTGZ_FUTURES_INCOME, MDIM_COMMODITY_PLATE, ME_DIM`
- **业务说明**: 按黑色金属、有色金属、贵金属、能源化工、农产品等板块统计商品期货的持仓与收益贡献。

### 真实数仓 SQL 语句

```sql
select to_char(v.d_date,'yyyy-mm-dd') "XAXISDATA",
       v.vc_fundcode "VC_FUNDCODE",
       nvl(v.f_money,'0') "YAXISDATA2",
       f.vc_name "YAXISDATA1"
  from (select t.d_date, t.vc_fundcode, sum(t.f_investincome_f) f_money, m.f_parent_id
           from mfactss_symbol_profit t, mfactei_industry_platestock m
          where t.vc_symbol = m.vc_symbol
            and t.vc_fundcode = #{fundCode}
            and t.vc_type = 'QH'
            and t.vc_type_detail = 'QH_SP'
            and t.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
            and t.d_date <= to_date(#{endDate},'yyyy-mm-dd')
            and exists (select 1
                   from mdim_sys_time m
                  where t.d_date = m.d_date
                    and m.f_hols_day = 1)
          group by t.d_date, t.vc_fundcode, m.f_parent_id
          order by t.d_date asc) v
          left join mdim_industry_plate f
          on v.f_parent_id = f.f_sid and f.f_parent_id='0'
    order by v.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-commodityFuturesExposureTiming"></a>08. 商品期货净敞口时序 (`commodityFuturesExposureTiming`)

- **业务分类**: 衍生品与期货
- **执行编码 (`sqlCode`)**: `a26dc9c7-6ca1-49f0-a93f-bceeedea3aee`
- **底层核心数仓表**: `MFACTGZ_FUTURES_POSITION, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 按日展示商品期货多头敞口、空头敞口及轧差后净敞口占基金净资产比例的变化趋势。

### 真实数仓 SQL 语句

```sql
select to_char(h.d_date,'yyyy-mm-dd') "XAXISDATA",
       to_char(decode(t.f_price,0,0,h.f_price/t.f_price)*100,'9999999999999990.00') "YAXISDATA1",  --期货类持仓占资产净值比
       to_char(decode(t.f_price,0,0,z.f_price/t.f_price)*100,'9999999999999990.00') "YAXISDATA2"   --前十大期货持仓占资产净值比
from
(select f.d_date, f.vc_fundcode, sum(f.f_price) f_price
   from mfactgz_fund_hlddetail f
   where f.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
   and f.d_date <= to_date(#{endDate},'yyyy-mm-dd')
   and f.vc_fundcode = #{fundCode}
   and f.vc_pa_code like '%_CB%'
   and f.vc_type_assist not like '%_CD%'
   and f.vc_type = 'QH'
 group by f.d_date, f.vc_fundcode) h,
(select k.d_date, k.vc_fundcode, sum(k.f_price) f_price
 from
 (select f.d_date, f.vc_fundcode, f.vc_symbol, f.f_price,
          row_number() over(partition by f.d_date, f.vc_fundcode order by f.f_price desc) rn
   from mfactgz_fund_hlddetail f
   where f.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
   and f.d_date <= to_date(#{endDate},'yyyy-mm-dd')
   and f.vc_fundcode = #{fundCode}
   and f.vc_pa_code like '%_CB%'
   and f.vc_type_assist not like '%_CD%'
   and f.vc_type = 'QH') k
  where k.rn <= 10
 group by k.d_date, k.vc_fundcode) z,
(select a.d_date, a.vc_fundcode, a.vc_subcode, a.f_price
 from mfactgz_fund_hldtotal a
 where a.vc_subcode = '701A'
 and a.vc_fundcode = #{fundCode}
 and a.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
 and a.d_date <= to_date(#{endDate},'yyyy-mm-dd')) t
where t.d_date = h.d_date
and t.vc_fundcode = h.vc_fundcode
and z.d_date = h.d_date
and t.vc_fundcode = z.vc_fundcode
and h.vc_fundcode = #{fundCode}
and h.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
and h.d_date <= to_date(#{endDate},'yyyy-mm-dd')
order by h.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-commodityProfitLoss"></a>09. 期货十大盈利亏损品种 (`commodityProfitLoss`)

- **业务分类**: 衍生品与期货
- **执行编码 (`sqlCode`)**: `b0a11b9d-5709-4c27-a0c0-57e859b2d9e8`
- **底层核心数仓表**: `MFACTGZ_FUTURES_INCOME_DETAIL, MDIM_FUTURES_CONTRACT`
- **业务说明**: 分别提取统计周期内期货持仓中收益排名前十（Top Profit）与亏损排名前十（Top Loss）的具体合约品种及收益金额。

### 真实数仓 SQL 语句

```sql
select a.vc_symbol "XAXISDATA", --期货code
       nvl(a.vc_name, '未知') "YAXISDATA1", --期货名称
       type_name "TYPE_NAME", --期货类别
       to_char(a.sumMoney / 10000, 'fm9999999990.90') as "TOTALMONEY", --交易金额（万元）
       nvl(a.buyAmount, 0) "YAXISDATA2", --买入数
       to_char(nvl(a.buyMoney, 0) / 10000, 'fm9999999990.90') "YAXISDATA3", --买入金额（万元）
       nvl(a.sellAmount, 0) "YAXISDATA4", --卖出数
       to_char(nvl(a.sellMoney, 0) / 10000, 'fm9999999990.90') "YAXISDATA5", ----卖出金额（万元）
       to_char(h.QHYK, 'fm9999999990.90') "YAXISDATA8", --期货盈亏
       to_char(h.QHYKDT, 'fm9999999990.90') "YAXISDATA6", --期货多头盈亏
       to_char(h.QHYKKT, 'fm9999999990.90') "YAXISDATA7" --期货空头盈亏
  from (select t.vc_symbol,
               t.vc_exchange,
               max(t.vc_name) vc_name,
               sum(t.f_money) sumMoney,
               sum(decode(t.vc_flag, 'B', t.f_amount, 0)) buyAmount,
               sum(decode(t.vc_flag, 'B', t.f_money, 0)) buyMoney,
               sum(decode(t.vc_flag, 'S', t.f_amount, 0)) sellAmount,
               sum(decode(t.vc_flag, 'S', t.f_money, 0)) sellMoney,
               row_number() over(partition by 1 order by sum(t.f_amount) desc) rn
          from mfactgz_trade_info t
         where t.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd') 
           and t.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')
           and t.vc_type = 'QH'
           and t.vc_flag in ('B', 'S')
           and t.vc_fundcode = #{fundCode}
         group by t.vc_symbol, t.vc_exchange) a
  left join (select t.vc_fundcode,
                    t.vc_symbol,
                    max(decode(t.vc_type_detail,'QH_GZ','股指期货','QH_BT','国债期货','QH_SP','商品期货')) type_name,
                    max(t.vc_name) vc_name,
                    sum(decode(t.vc_type_assist, 'DT', t.f_gz, 0)) qhykdt,
                    sum(decode(t.vc_type_assist, 'KT', t.f_gz, 0)) qhykkt,
                    sum(t.f_gz) qhyk
               from mfactgz_fund_hlddetail t
              where t.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd') 
                and t.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')
                and t.vc_fundcode = #{fundCode}
                and t.vc_type = 'QH'
                and t.vc_pa_code = 'ZQTZ_CB'
                and t.vc_type_assist not like '%_CD'
              group by t.vc_fundcode, t.vc_symbol) h
    on a.vc_symbol = h.vc_symbol
    where a.rn <= 10
  order by a.rn asc
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-creditRiskRateDistribution"></a>10. 信用风险评级分布 (`creditRiskRateDistribution`)

- **业务分类**: 债券与固收
- **执行编码 (`sqlCode`)**: `944d0936-066f-4d4c-ad16-67767a431d7a`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_BOND_RATING, ME_DIM`
- **业务说明**: 按主体评级与债项评级（如 AAA、AA+、AA、AA- 及以下）分类统计持仓债券市值及占比分布。

### 真实数仓 SQL 语句

```sql
select m.xaxisdata "XAXISDATA",
       m.yaxisdata1 "YAXISDATA1",
       m.yaxisdata2 "YAXISDATA2",
       m.yaxisdata3 "YAXISDATA3",
       m.yaxisdata4 "YAXISDATA4"
  from (select decode(w.vc_credit,null,'其他',w.vc_credit) xaxisdata, --债券评级
               w.f_estimate_fullprice / 10000 yaxisdata1, --全价市值
               w.f_price / 10000 yaxisdata2, --应记利息
               w.f_pricerationet as yaxisdata3, /*期末占比*/
               w.f_pricerationet - nvl(s.f_priceratio, 0) as yaxisdata4
          from (--本期
                 select e.vc_credit,
                        sum(e.f_estimate_fullprice) f_estimate_fullprice,
                        sum(e.f_price) f_price,
                        sum(e.f_priceratio) f_pricerationet
                  from (select t.d_date,
                               t.vc_fundcode,
                               s.vc_credit,
                               (nvl(t.f_price,0) + nvl(t.f_yslx,0)) f_estimate_fullprice,
                               t.f_price f_price,
                               decode(h.f_price,0,0,t.f_price / h.f_price) f_priceratio
                           from (select t.d_date,
                                        t.vc_fundcode,
                                        t.vc_symbol,
                                        t.vc_exchange,
                                        sum(decode(t.vc_pa_code,'ZQTZ_CB',t.f_price,0)) f_price,
                                        sum(decode(t.vc_pa_code,'YSLX_ZQ',t.f_price,0)) f_yslx
                                   from mfactgz_fund_hlddetail t
                                   left join mdim_sys_time e
                                   on e.d_date = to_date(#{endDate},'yyyy-MM-dd')
                                  where t.vc_fundcode = #{fundCode}
                                    --and t.d_date = decode(e.f_hols_day, '1', e.d_date, '0', e.d_prev_date)
                                    and t.d_date = (to_date(#{endDate},'yyyy-MM-dd')) --结束日
                                    and t.vc_pa_code in ('ZQTZ_CB', 'YSLX_ZQ')
                                    and t.vc_type = 'ZQ'
                                  group by t.d_date,
                                           t.vc_fundcode,
                                           t.vc_symbol,
                                           t.vc_exchange) t
                           left join mfactei_bond_dividend s
                             on s.d_date = t.d_date
                            and s.vc_symbol = t.vc_symbol
                            and s.vc_exchange = t.vc_exchange
                           left join mfactgz_fund_hldtotal h
                             on (t.vc_fundcode = h.vc_fundcode and
                                t.d_date = h.d_date and
                                h.vc_subcode = '103A')
                         ) e
                 group by e.vc_credit) w
          left join ( --期初
                    select e.vc_credit,sum(e.f_priceratio) f_priceratio
                      from (select r.vc_credit,
                                   r.d_date,
                                    decode(h.f_price,0,0,r.f_price / h.f_price) f_priceratio
                               from (select d.vc_credit,
                                            t.f_price,
                                            t.vc_fundcode,
                                            t.d_date
                                       from mfactgz_fund_hlddetail t
                                       left join mfactei_bond_dividend  d
                                       on t.d_date = d.d_date
                                        and t.vc_symbol = d.vc_symbol
                                        and t.vc_exchange = d.vc_exchange
                                       left join mdim_sys_time e
                                       on e.d_date = to_date(#{beginDate},'yyyy-MM-dd')
                                      where t.vc_fundcode = #{fundCode}
                                      and t.d_date = e.d_prev_date
                                       --and d.d_date = t.d_date
                                        --and t.d_date = decode(e.f_hols_day, '1', e.d_date, '0', e.d_prev_date)
                                        --and d.d_Date = decode(e.f_hols_day, '1', e.d_date, '0', e.d_prev_date)
                                        and e.d_date = (to_date(#{beginDate},'yyyy-MM-dd')) --开始日期
                                        and t.vc_pa_code = 'ZQTZ_CB'
                                        and t.vc_type = 'ZQ') r
                               left join mfactgz_fund_hldtotal h
                                 on (r.vc_fundcode = h.vc_fundcode and
                                    r.d_date = h.d_date and
                                    h.vc_subcode = '103A')) e
                     group by e.vc_credit) s
            on w.vc_credit = s.vc_credit) m
  left join me_dim e
    on m.xaxisdata = e.dim_nme
   and e.dim_type = 'CREDIT_TYPE'
 order by e.dim_ord
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-fixedPositionTiming"></a>11. 固定收益类持仓时序 (`fixedPositionTiming`)

- **业务分类**: 大类资产配置
- **执行编码 (`sqlCode`)**: `7c426689-80d2-4ce0-83d8-26c45fe5493f`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDTOTAL, ME_DIM`
- **业务说明**: 时序统计国债、金融债、企业债、中期票据、可转债等各类债券固收资产的合计市值及占净比走势。

### 真实数仓 SQL 语句

```sql
-- 固定收益类持仓时序 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-fundDurationTiming"></a>12. 组合加权久期时序 (`fundDurationTiming`)

- **业务分类**: 债券与固收
- **执行编码 (`sqlCode`)**: `7d29ed40-0d69-4cd1-93a8-0a2bf9eac9cd`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_BOND_INFO, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 以个券市值占基金总资产比重为权重，计算产品整体加权久期的时序演变曲线。

### 真实数仓 SQL 语句

```sql
-- 组合加权久期时序 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-hldStockNumTime"></a>13. 持股数量时序变化图 (`hldStockNumTime`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `2f3f7b80-5c28-407f-90c5-5d2464eaf5a0`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_SYS_TIME`
- **业务说明**: 统计每个估值日组合实际持仓的不同股票代码只数，反映持仓分散度与选股集中风格。

### 真实数仓 SQL 语句

```sql
-- 持股数量时序变化图真实查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    COUNT(DISTINCT d.vc_code)        AS "STOCK_COUNT",
    SUM(d.f_price) / 10000.0        AS "TOTAL_MARKET_VALUE_WAN"
FROM mfactgz_fund_hlddetail d
JOIN mdim_sys_time t 
  ON d.d_date = t.d_date
WHERE d.vc_fundcode = #{fundCode}
  AND d.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
  AND d.vc_type = 'GP'
  AND t.f_hols_day = '1'
GROUP BY t.d_date, t.vc_fundcode
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-holdPlate"></a>14. A股持仓指数及板块时序 (`holdPlate`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `caa5b2df-8278-458e-b176-db71cce9a024`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_STOCK_PLATE, MFACTEI_INDEX_MARKET`
- **业务说明**: 跟踪主板、创业板、科创板等不同上市板块的持仓权重，并与主要指数走势同屏对比。

### 真实数仓 SQL 语句

```sql
-- A股持仓指数及板块时序 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-hsInduStockAlloca"></a>15. 华泰柏瑞行业配置 (`hsInduStockAlloca`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `4dadd10a-92c2-43b3-b8a7-de798cdebb5c`
- **底层核心数仓表**: `MFACTGZ_STOCK_INDUSTRY_ALLOC, MDIM_HS_INDUSTRY, ME_DIM`
- **业务说明**: 按华泰柏瑞分类标准展现港股/A股行业的超配、低配敞口及配置主动风险。

### 真实数仓 SQL 语句

```sql
--港股行业配置时序

select to_char(x1.d_date, 'yyyy-mm-dd') "DATES",
       x1.vc_industry_code1 "DIM_CDE",
       x1.vc_industry_name1 "DIM_NME",
       to_char(nvl(sum(x2.f_price)/x2.total,0) * 100,'fm999999999990.00') "F_PRICE",
       to_char(nvl(x1.f_yield, 0) * 100, 'fm99999999990.00') "BENCH_YIELD"
  from (select k.d_date,
               k.f_yield,
               t.vc_industry_code1,
               t.vc_industry_name1
          from (select k.d_date, nvl(power(2,
                         least(round(Sum(Log(2,
                                             greatest(f.f_yield,      
                                                      -0.5) + 1))
                                     over(order by k.d_date asc),
                                     8),
                               10)) - 1,
                   0) f_yield
          from mdim_sys_time k,
               (select A.d_date,
                       nvl(A.f_yeild, 0) * to_number(nvl(#{benchmarkAValue}, '100')) / 100 +
                       nvl(B.f_yeild, 0) * to_number(nvl(#{benchmarkBValue}, '0')) / 100 f_yield
                  from (select t.d_date,
                               t.vc_product_code,
                               t.vc_product_type,
                               nvl(t.f_yeild, 0) f_yeild
                          from fact_product_yeild t, mdim_fund_info d
                         where 1 = 1
                           and d.vc_fundcode = #{fundCode}
                           and t.d_date >= d.d_create_date
                           and t.vc_product_code = #{benchmarkA}
                           and t.vc_product_type = 'ZS'
                           and t.d_date between
                               to_date(#{beginDate}, 'yyyy-mm-dd') and
                               to_date(#{endDate}, 'yyyy-mm-dd')) A
                  left join (select t.d_date,
                                   t.vc_product_code,
                                   vc_product_type,
                                   nvl(t.f_yeild, 0) f_yeild
                              from fact_product_yeild t
                             where 1 = 1
                               and t.vc_product_code =
                                   nvl(#{benchmarkB}, '000300')
                               and t.vc_product_type = 'ZS'
                               and t.d_date between
                                   to_date(#{beginDate}, 'yyyy-mm-dd') and
                                   to_date(#{endDate}, 'yyyy-mm-dd')) B
                    on A.d_date = B.d_date) f
         where k.d_date = f.d_date
           and k.f_hols_day = 1) k,
               (select distinct t.vc_industry_code1, t.vc_industry_name1
                  from mdim_industry_info t
                 where t.vc_industry_type = 'HSSR'
                union all
                select '9999' vc_industry_code1, '其他(HS)' vc_industry_name1
                  from dual) t
         where 1 = 1) x1
  left join (select d_date,
                    vc_fundcode,
                    nvl(vc_industry_code, '9999') vc_industry_code,
                    decode(vc_industry_name,
                           '',
                           '其他(HS)',
                           vc_industry_name) vc_industry_name,
                    sum(f_price) f_price,
                    sum(f_price) over(partition by d_date,vc_fundcode) total
               from (select t.d_date, t.vc_fundcode, t.vc_symbol, t.f_price
                       from mfactgz_fund_hlddetail t, mdim_sys_time h
                      where t.d_date = h.d_date
                        and h.f_hols_day = 1
                        and t.vc_type = 'GP'
                        and t.vc_pa_code = 'ZQTZ_CB'
                        and t.vc_exchange = 'HK'
                        and t.vc_fundcode = #{fundCode}
                        and t.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd')
                        and t.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')) t
               left join (select distinct t.vc_symbol,
                                         t.vc_industry_code,
                                         t.vc_industry_name,
                                         t.d_begin_date,
                                         D_END_DATE
                           from mfactei_industry_symbol t
                          where t.vc_industry_type = 'HSSR') v2
                 on t.vc_symbol = v2.vc_symbol
                and t.d_date >= v2.d_begin_date
                and t.d_date <= v2.d_end_date
              group by t.d_date,
                       t.vc_fundcode,
                       v2.vc_industry_code,
                       v2.vc_industry_name,
                       t.f_price) x2
    on x1.vc_industry_name1 = x2.vc_industry_name
   and x1.d_date = x2.d_date
 where 1 = 1
 group by x1.d_date,x1.vc_industry_code1,x1.vc_industry_name1,x2.total,x1.f_yield
 order by x1.d_date, x1.vc_industry_code1
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-hsInduStockAnal"></a>16. 华泰柏瑞行业分析 (`hsInduStockAnal`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `73ab4b7f-b543-4b94-ac6c-50685997d361`
- **底层核心数仓表**: `MFACTGZ_BRINSON_INDUSTRY, MDIM_HS_INDUSTRY`
- **业务说明**: 基于 Brinson 模型，在华泰柏瑞行业分类下分解行业资产配置效应、选股效应及交互效应。

### 真实数仓 SQL 语句

```sql
-- 华泰柏瑞行业分析 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-hsInduStockVala"></a>17. 华泰柏瑞行业估值 (`hsInduStockVala`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `125bb87f-2c9c-485e-8042-87ce0d60cd30`
- **底层核心数仓表**: `MFACTGZ_STOCK_INDUSTRY_VALUATION, MDIM_HS_INDUSTRY`
- **业务说明**: 评估各行业的估值水平（行业 PE、PB 历史分位数及相对估值偏离度）。

### 真实数仓 SQL 语句

```sql
-- 华泰柏瑞行业估值 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-industryMonitor"></a>18. 行业监控 (`industryMonitor`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `8c627513-5936-4936-af12-66ad0ea1a947`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_INDUSTRY_INFO, MFACTEI_INDEX_MARKET`
- **业务说明**: 多维度监控各行业配置比重、动态调整偏离度，包含时序面积图与截面饼图。

### 真实数仓 SQL 语句

```sql
with temp_fund_industry_type as
 (select /*+materialize*/
   nvl(t.vc_industry_type, 'SWSR') vc_industry_type
    from mdim_fund_info t
   where t.vc_fundcode = #{ZB_FUNDCODE})
   
  select YAXISDATA1 "YAXISDATA1", xaxisData "XAXISDATA"
    from (select g.industryName YAXISDATA1, --产品名
                 nvl(avg(Industry_ratio), 0) xaxisData, --平均市值
                 row_number() over(partition by 1 order by nvl(avg(Industry_ratio), 0) desc) rn
            from (select t.d_date,
                         t.vc_industry_name industryname,
                         nvl(t.F_FUND_INDUSTRY_PRICE, 0) f_fund_industry_price,
                         nvl(a.f_price, 0) f_price,
                         decode(a.f_price,
                                0,
                                0,
                                nvl(t.f_fund_industry_price, 0) / a.f_price) industry_ratio
                    from MFACTSS_FUND_YIELD_INDUSTRY t
                    left join (select f.d_date, f.vc_fundcode, f.f_price
                                from mfactgz_fund_hldtotal f
                               where f.vc_subcode = '102A'
                               and f.vc_fundcode = #{ZB_FUNDCODE}
                               and f.d_date between to_date(#{ZB_BEGINDATE}, 'yyyy-MM-dd') and
                                   to_date(#{ZB_ENDDATE}, 'yyyy-MM-dd')) a
                      on a.d_date = t.d_date
                     and a.vc_fundcode = t.vc_fundcode
					
                   where t.d_date between to_date(#{ZB_BEGINDATE}, 'yyyy-MM-dd') and
                         to_date(#{ZB_ENDDATE}, 'yyyy-MM-dd')
                     and t.vc_fundcode = #{ZB_FUNDCODE}
                     and exists  (select 1 from temp_fund_industry_type k 
					 where 1=1
					 and t.vc_industry_type=k.vc_industry_type)
                     and exists (select *
                            from mdim_sys_time s
                           where s.d_date = t.d_date
                             and s.f_hols_day = '1')) g
           group by g.industryname) a
   where a.rn <= 10
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-maxDrawdownFQ"></a>19. 最大回撤与修复时序 (`maxDrawdownFQ`)

- **业务分类**: 风险与回撤
- **执行编码 (`sqlCode`)**: `f6dd749d-df80-41d4-b98f-9ace45fb5544`
- **底层核心数仓表**: `MFACTGZ_FUND_NAV_TIMING, MFACTGZ_RISK_INDEX_RESULT`
- **业务说明**: 按日计算产品自前期最高净值以来的回撤深度（Drawdown %），并标记回撤区间起点、谷底日及修复天数。

### 真实数仓 SQL 语句

```sql
select t.vc_fundcode "YAXISDATA1",
       t.vc_tjtype "XAXISDATA",
       t.f_maxdrown "F_MAXDROWN",
       t.vc_maxdrown_reg "VC_MAXDROWN_REG",
       t.f_avg_dayyield "YAXISDATA2",
       t.f_avg_daylossyield "YAXISDATA3",
       t.f_max_dayprofityield "YAXISDATA4",
       t.f_max_daylossyield "YAXISDATA5",
       t.f_avg_dayprofityield "YAXISDATA6",
       t.f_avg_daylossyield "YAXISDATA7",
       t.f_profit_days_rate "YAXISDATA8"
from table(F_FUND_DRAWDOWN_SY(#{fundCode},
                                     #{startDate},
                                     #{endDate},
                                     '',
                                     '',
                                     '',
                                     '')) t
where 1=1
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-netValMonitor"></a>20. 净值走势监控 (`netValMonitor`)

- **业务分类**: 净值与业绩
- **执行编码 (`sqlCode`)**: `8c757339-83c8-4e0b-adae-76e3cec96a8d`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDTOTAL, MFACTEI_INDEX_MARKET, MDIM_SYS_TIME`
- **业务说明**: 绘制产品单位净值、累计净值与同期基准指数（如沪深300、中证500）的收益走势对照曲线。

### 真实数仓 SQL 语句

```sql
SELECT to_char(A.D_DATE, 'yyyy-mm-dd') "XAXISDATA",
        to_char(NVL(A.F_PRICE / 10000, 0), 'fm9999999999999990.90') "YAXISDATA1", --资产净值
        to_char(NVL(B.F_PRICE, 0), 'fm99999999999999990.9990') "YAXISDATA2", --单位净值
        to_char(NVL(C.F_PRICE, 0), 'fm99999999999999990.9990') "YAXISDATA3" --累计单位净值
   FROM (SELECT T.D_DATE, T.VC_FUNDCODE, T.F_PRICE
           FROM MFACTGZ_FUND_HLDTOTAL T, MDIM_SYS_TIME a
          WHERE T.VC_FUNDCODE = #{ZB_FUNDCODE}
            AND T.VC_SUBCODE = '701A'
            and a.F_HOLS_DAY = '1'
            AND T.d_DATE = A.D_DATE
            AND t.d_DATE <= to_date(#{ZB_ENDDATE}, 'yyyy-mm-dd')
            AND t.d_DATE >= to_date(#{ZB_BEGINDATE}, 'yyyy-mm-dd')
          order by t.d_date) A
   LEFT JOIN (SELECT T.D_DATE, T.VC_FUNDCODE, T.F_PRICE
                FROM MFACTGZ_FUND_HLDTOTAL T
               WHERE T.VC_FUNDCODE = #{ZB_FUNDCODE}
                 AND T.VC_SUBCODE = '702A'
                 AND t.D_DATE <= to_date(#{ZB_ENDDATE}, 'yyyy-mm-dd')
                 AND t.d_DATE >= to_date(#{ZB_BEGINDATE}, 'yyyy-mm-dd')) B
     ON B.D_DATE = A.D_DATE
    AND B.VC_FUNDCODE = A.VC_FUNDCODE
   LEFT JOIN (SELECT T.D_DATE, T.VC_FUNDCODE, T.F_PRICE
                FROM MFACTGZ_FUND_HLDTOTAL T
               WHERE T.VC_FUNDCODE = #{ZB_FUNDCODE}
                 AND T.VC_SUBCODE = '905'
                 AND t.D_DATE <= to_date(#{ZB_ENDDATE}, 'yyyy-mm-dd')
                 AND t.d_DATE >= to_date(#{ZB_BEGINDATE}, 'yyyy-mm-dd')) C
     ON C.D_DATE = A.D_DATE
    AND C.VC_FUNDCODE = A.VC_FUNDCODE
    ORDER BY A.D_DATE ASC
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-netValue"></a>21. 产品规模走势 (`netValue`)

- **业务分类**: 净值与业绩
- **执行编码 (`sqlCode`)**: `38ac7662-b120-4cb9-9fdf-8becaf856723`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDTOTAL, MDIM_FUND_INFO`
- **业务说明**: 双 Y 轴图表：左轴显示资产总净值（资产规模，元/万元），右轴显示单位净值与累计单位净值走势。

### 真实数仓 SQL 语句

```sql
with f as
         (select vc_fundcode,
                 d_create_date,
                 vc_source
            from mdim_fund_info
           where vc_fundcode = #{fundCode}),
       hldd as
         (select max(d_date) maxd, min(d_date) mind
            from f, mfactgz_fund_hlddetail a
           where f.vc_fundcode = a.vc_fundcode
             and a.vc_fundcode = #{fundCode}
             and a.d_date between to_date(#{beginDate}, 'yyyy-mm-dd') and to_date(#{endDate}, 'yyyy-mm-dd')),
       trade as
         (select vc_busin_type,
                 sum(a.f_confirmbalance) / 10000 f_confirmbalance
            FROM f, mfactgz_pursell_trade a
           where a.d_date between to_date(#{beginDate}, 'yyyy-mm-dd') and to_date(#{endDate}, 'yyyy-mm-dd')
             and a.vc_fundcode = f.vc_fundcode
             and a.vc_fundcode = #{fundCode}
           group by a.vc_busin_type),
        hldt as
         (select f.vc_source, b.f_price/10000 f_p1, c.f_price/10000 f_p2
            from f
            cross join hldd a
            left join mfactgz_fund_hldtotal b
              on b.vc_fundcode = f.vc_fundcode
             and b.d_date = nvl(a.mind, f.d_create_date)
             and b.vc_subcode = '701A'
            left join mfactgz_fund_hldtotal c
              on c.vc_fundcode = f.vc_fundcode
             and c.d_date = nvl(a.maxd, f.d_create_date)
             and c.vc_subcode = '701A'
            where b.vc_fundcode = #{fundCode}
            and c.vc_fundcode = #{fundCode})
           
select to_char(nvl(a.f_p1, 0), 'FM999999999990.00') "YAXISDATA1",
       to_char(nvl(a.f_p2, 0), 'FM999999999990.00') "YAXISDATA2",
       to_char(nvl((sum(decode(b.vc_busin_type, 'SG', b.f_confirmbalance))), 0), 'FM999999999990.00') "YAXISIDATA3",
       to_char(nvl((sum(decode(b.vc_busin_type, 'SH', b.f_confirmbalance))), 0), 'FM999999999990.00') "YAXISIDATA4",
       a.vc_source "YAXISIDATA5"
  from hldt a, trade b
  group by a.f_p1, a.f_p2, a.vc_source
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-overallFutures"></a>22. 期货总持仓及收益 (`overallFutures`)

- **业务分类**: 衍生品与期货
- **执行编码 (`sqlCode`)**: `b435f30d-6914-4916-93d6-3c1e8d3e510e`
- **底层核心数仓表**: `MFACTGZ_FUTURES_POSITION, MFACTGZ_FUTURES_INCOME`
- **业务说明**: 汇总股指期货、国债期货、商品期货的整体名义本金、保证金占用、持仓保证金率与实现总盈亏。

### 真实数仓 SQL 语句

```sql
select to_char(d_date,'yyyy-mm-dd') "XAXISDATA",---日期
       vc_fundcode "VC_FUNDCODE", ---组合代码
       round(nvl(sum(DT_price), 0)/10000, 2) "YAXISDATA1", ---　　多头市值
       round(nvl(sum(KT_price), 0)/10000, 2) "YAXISDATA2"   ---　　空头市值
  from (select t.d_date,
               t.vc_fundcode,
               case
                 when vc_type_assist = 'DT' then
                  sum(t.f_price)
               end DT_price,
               case
                 when vc_type_assist = 'KT' then
                  -sum(t.f_price)
               end KT_price
          from mfactgz_fund_hlddetail t
         where 1 = 1
           and t.vc_type_assist in ('DT', 'KT')
           and t.vc_type_detail = 'QH_SP'
           and t.vc_type = 'QH'
           and t.vc_fundcode = #{fundCode}
           and t.d_date >= to_date(#{beginDate},'yyyy-mm-dd')
           and t.d_date <= to_date(#{endDate},'yyyy-mm-dd')
           and exists (select 1
                  from mdim_sys_time m
                 where t.d_date = m.d_date
                   and m.f_hols_day = 1)
         group by t.d_date, t.vc_fundcode, t.vc_type_assist
         order by t.d_date asc)  v
 group by d_date, vc_fundcode
 order by d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-positionIndustry"></a>23. 行业持仓分布 (`positionIndustry`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `d8ac50c1-b41c-498e-8c8a-bd6a577177a6`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_INDUSTRY_INFO, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 截面统计报告期末持仓股票在前五/前十大行业的市值分布及占股票资产净比。

### 真实数仓 SQL 语句

```sql
select
                
                e.dim_nme  as "XAXISDATA",  --类别
                abs(f.f_price) as "YAXISDATA1",   --金额（元）
                case when nvl(sum(abs(f.f_price)) over (partition by f.d_date ),0)=0 then 0
                     else
                         abs(f.f_price)/ sum(abs(f.f_price)) over (partition by f.d_date )
                 end  as "YAXISDATA2"   --占比
        from mfactgz_fund_asset_price f,
             me_dim e,
             (select decode(t.f_HOLS_DAY,
                            1,
                            t.d_DATE,
                            0,
                            t.d_PREV_DATE) d_date
              from mdim_sys_time t
              where t.d_DATE = to_date(#{ZB_ENDDATE}, 'YYYY-MM-DD')) k
        where f.vc_fundcode = #{ZB_FUNDCODE}
          and f.d_date = k.d_date
          and f.vc_asset_code=e.dim_cde
          and e.dim_type='ASSETTYPENEW_GF'
          and e.dim_status='1'
        order by to_number(nvl(e.dim_ord,'0')) asc
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-productInfo"></a>24. 产品基本信息 (`productInfo`)

- **业务分类**: 基础信息
- **执行编码 (`sqlCode`)**: `4475dbc6-a3f9-4e37-bb8b-fda45fda68fc`
- **底层核心数仓表**: `MDIM_FUND_INFO, MDIM_COMPANY_INFO, ME_DIM`
- **业务说明**: 查询基金全称、简称、代码、投资经理、成立日期、投资策略类型、基准代码及托管外包机构等静态档案信息。

### 真实数仓 SQL 语句

```sql
select V.vc_fundcode "VC_FUNDCODE", --产品代码
       V.vc_fund_full_name "YDATE1", --基金全称
       V.vc_fundname "YDATE3", --基金简称
       V.VC_REGCODE "YDATE5", --备案编号
       to_char(f.d_register_date,'yyyy-mm-dd') "YDATE7", --备案日期
       to_char(f.D_FOUNDATION_DATE,'yyyy-mm-dd') "YDATE9", --成立日期
       decode(f.VC_FUND_STATUS,
              1,
              '募集中',
              2,
              '开放运行',
              4,
              '提前清算',
              5,
              '到期清算',
              6,
              '发行失败',
              7,
              '更换管理人',
              8,
              '延期清算',
              '其他') "YDATE11", --运行状态
       decode(f.NAV_FREQUENCY,0,'日频',1,'周频',2,'月频',3,'其他') "YDATE13", --净值披露频率
       e.dim_nme  "YDATE14", --一级策略
       ee.dim_nme  "YDATE16", --二级策略
       F.OPEN_DAY "YDATE18", --开放日
       decode(F.LOCKUP_PERIOD,1,'不确定',0, '无封闭期') "YDATE20", --封闭期
       decode(RAISE_TYPE,1,'私募',2, '公募') "YDATE22", --募集方式
       decode(f.VC_MANAGER_TYPE,
              1,
              '顾问管理',
              2,
              '受托管理',
              3,
              '自我管理') "YDATE24", --管理类型
       f.VC_FUND_MEMBER "YDATE2", --投资经理
       V.VC_ADVISOR "YDATE4", --投资顾问
       f.vc_issuer "YDATE6", --发行机构
       f.vc_custodian "YDATE8", --托管机构
       f.vc_broker "YDATE10", --证券经纪人
       f.vc_broker_future "YDATE12", --期货经纪人
       f.vc_liquidation_agency "YDATE", --外包机构
       f.vc_administrator "YDATE17", --行政管理人
       f.vc_trust "YDATE15", --基金管理公司
       f.vc_legal_counsel "YDATE19", --法律顾问
       f.VC_AUDITOR "YDATE21", --审计机构
       decode(f.ISTIERED,'1','分级','0', '不分级') "YDATE23", --是否分级
       decode(f.FUND_STRUCTURE,
              '1',
              '公司型',
              '2',
              '合伙型',
              '3',
              '契约型',
              '其他') "YDATE25" --基金形式
  from V_ALL_FUND_INFO V
  LEFT JOIN dim_mkfund_info f
    on v.vc_fundcode = f.vc_fundcode
  LEFT JOIN me_dim e
    on v.vc_strategy_type = e.dim_cde
   and e.dim_type = 'strategy_type'
   and e.dim_status = '1'
  LEFT JOIN me_dim ee
    on v.vc_strategy_subtype = ee.dim_cde
   and ee.dim_type = 'fundinvesttype'
   and ee.dim_status = '1'
 where v.vc_fundcode = #{fundCode,jdbcType=VARCHAR}
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-rewardRisk"></a>25. 风险与收益指标 (`rewardRisk`)

- **业务分类**: 风险与回撤
- **执行编码 (`sqlCode`)**: `f6dd749d-df80-41d4-b98f-9ace45fb5544`
- **底层核心数仓表**: `MFACTGZ_RISK_INDEX_RESULT, MFACTGZ_FUND_NAV_TIMING`
- **业务说明**: 区间综合风险指标卡片：包含年化收益率、年化波动率、夏普比率（Sharpe）、索提诺比率（Sortino）、卡玛比率（Calmar）及胜率。

### 真实数仓 SQL 语句

```sql
select to_char(nvl((exp(sum(ln(
          f.f_y_day_rate + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') "YAXISDATA1",--组合收益率 数据从上到下分别表示：过去一月（%），过去三月（%），过去六个月（%），今年以来（%）
       to_char(nvl(stddev(ln(1 + f.f_y_day_rate)) * 100, 0),'fm99999999999999990.9990') "YAXISDATA2",--组合标准差 数据从上到下分别表示：过去一月（%），过去三月（%），过去六个月（%），今年以来（%）
       to_char(nvl((exp(sum(ln(
                  f.f_y_bench_yield + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') "YAXISDATA3",--基准收益率 数据从上到下分别表示：过去一月（%），过去三月（%），过去六个月（%），今年以来（%）
       to_char(nvl(stddev(ln(1 + f.f_y_bench_yield)) * 100, 0),'fm99999999999999990.9990') "YAXISDATA4",--基准标准差 数据从上到下分别表示：过去一月（%），过去三月（%），过去六个月（%），今年以来（%）
       to_char(nvl((exp(sum(ln(
                  f.f_y_day_rate + 1))) - 1) * 100,
         0) - nvl((exp(sum(ln(
                       f.f_y_bench_yield + 1))) - 1) * 100,
            0),'fm99999999999999990.9990') "YAXISDATA5"--超额收益率 数据从上到下分别表示：过去一月（%），过去三月（%），过去六个月（%），今年以来（%）
    from mfactss_fund_profit_sy f
    where f.d_end_date between add_months(to_date(#{endDate},'yyyy-mm-dd'), -1) + 1 and to_date(#{endDate},'yyyy-mm-dd')
     and f.vc_fundcode = #{fundCode}
     and f.f_y_day_rate > -1
     and f.f_y_bench_yield > -1

    union all
    select to_char(nvl((exp(sum(ln(
              f.f_y_day_rate + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') fund_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_day_rate)) * 100, 0),'fm99999999999999990.9990') fund_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_bench_yield + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') bench_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_bench_yield)) * 100, 0),'fm99999999999999990.9990') bench_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_day_rate + 1))) - 1) * 100,
         0) - nvl((exp(sum(ln(
                       f.f_y_bench_yield + 1))) - 1) * 100,
            0),'fm99999999999999990.9990') over_yield
    from mfactss_fund_profit_sy f
    where f.d_end_date between add_months(to_date(#{endDate},'yyyy-mm-dd'), -3) + 1 and to_date(#{endDate},'yyyy-mm-dd')
     and f.vc_fundcode = #{fundCode}
     and f.f_y_day_rate > -1
     and f.f_y_bench_yield > -1

    union all
    select to_char(nvl((exp(sum(ln(
              f.f_y_day_rate + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') fund_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_day_rate)) * 100, 0),'fm99999999999999990.9990') fund_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_bench_yield + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') bench_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_bench_yield)) * 100, 0),'fm99999999999999990.9990') bench_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_day_rate + 1))) - 1) * 100,
         0) - nvl((exp(sum(ln(
                       f.f_y_bench_yield + 1))) - 1) * 100,
            0),'fm99999999999999990.9990') over_yield
    from mfactss_fund_profit_sy f
    where f.d_end_date between add_months(to_date(#{endDate},'yyyy-mm-dd'), -6) + 1 and to_date(#{endDate},'yyyy-mm-dd')
     and f.vc_fundcode = #{fundCode}
     and f.f_y_day_rate > -1
     and f.f_y_bench_yield > -1

    union all
    select to_char(nvl((exp(sum(ln(
                          f.f_y_day_rate + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') fund_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_day_rate)) * 100, 0),'fm99999999999999990.9990') fund_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_bench_yield + 1))) - 1) * 100,
         0),'fm99999999999999990.9990') bench_yield,
       to_char(nvl(stddev(ln(1 + f.f_y_bench_yield)) * 100, 0),'fm99999999999999990.9990') bench_rate,
       to_char(nvl((exp(sum(ln(
                  f.f_y_day_rate + 1))) - 1) * 100,
         0) - nvl((exp(sum(ln(
                       f.f_y_bench_yield + 1))) - 1) * 100,
            0),'fm99999999999999990.9990') over_yield
    from mfactss_fund_profit_sy f
     where f.d_end_date between trunc(to_date(#{endDate}, 'yyyy-mm-dd'),'YYYY') and to_date(#{endDate}, 'yyyy-mm-dd')
      and f.vc_fundcode = #{fundCode}
     and f.f_y_day_rate > -1
     and f.f_y_bench_yield > -1
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-riskValue"></a>26. 风险指标分析 (`riskValue`)

- **业务分类**: 风险与回撤
- **执行编码 (`sqlCode`)**: `8abc19f5-f2c9-4cff-8a89-48884270d042`
- **底层核心数仓表**: `MFACTGZ_VAR_RESULT, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 多置信度（95%、99%）下的在险价值（VaR - Value at Risk）与预期损失（ES - Expected Shortfall）计量。

### 真实数仓 SQL 语句

```sql
select k.v_zxd "YAXISDATA1",
       k.v_days "YAXISDATA2",
       to_char(nvl(f_var, 0) / 10000,'fm999,999,999,999,990.00') "YAXISDATA3", --Var（万）
       to_char(decode(nvl(a.f_price, 0), 0, 0, nvl(f_var,0) / a.f_price)*100,'fm999999990.00')||'%' "YAXISDATA4", --var/资产

       case when decode(nvl(a.f_price, 0), 0, 0, nvl(f_var,0) / a.f_price) <=0.03 then
            '安全'
       when decode(nvl(a.f_price, 0), 0, 0, nvl(f_var,0) / a.f_price) > 0.05 then
         '危险'
       else
         '预警'
       end "YAXISDATA5"
  from (select '95' v_zxd, --置信度
               '1' v_days, --天数
               1 f_ord,
               d.vc_fundcode,
               f_app_fund_Var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              1,
                              0.95,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '95' v_zxd, --置信度
               '5' v_days, --天数
               2 f_ord,
               d.vc_fundcode,
               f_app_fund_Var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              5,
                              0.95,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '95' v_zxd, --置信度
               '10' v_days, --天数
               3 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              10,
                              0.95,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '95' v_zxd, --置信度
               '20' v_days, --天数
               4 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              20,
                              0.95,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '99' v_zxd, --置信度
               '1' v_days, --天数
               5 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              1,
                              0.99,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '99' v_zxd, --置信度
               '5' v_days, --天数
               6 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              5,
                              0.99,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '99' v_zxd, --置信度
               '10' v_days, --天数
               7 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              10,
                              0.99,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}
        union all
        select '99' v_zxd, --置信度
               '20' v_days, --天数
               8 f_ord,
               d.vc_fundcode,
               f_app_fund_var(#{beginDate},
                              #{endDate},
                              d.vc_fundcode,
                              20,
                              0.99,
                              'JZ2',
                              'D') f_var
          from mdim_fund_info d
         where d.vc_fundcode = #{fundCode}) k
  left join (select t.vc_fundcode,
                    t.f_price,
                    row_number() over(partition by t.vc_fundcode order by t.d_date desc) rk
               from mfactgz_fund_hldtotal t
              where t.vc_fundcode = #{fundCode}
                and t.vc_subcode = '701A'
                and t.d_date >= to_date(#{beginDate}, 'yyyy-MM-dd')
                and t.d_date <= to_date(#{endDate}, 'yyyy-MM-dd')) a
    on k.vc_fundcode = a.vc_fundcode
   and a.rk = 1
  order by k.f_ord
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-stockExposureTiming"></a>27. 股票净敞口时序 (`stockExposureTiming`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `712b930b-87a5-4cba-8da0-3671d4c8dc54`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MFACTGZ_FUTURES_POSITION, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 按日计算多头股票多头市值占比、股指期货空头套保对冲比例、以及合成后的股票实际净敞口比例时序。

### 真实数仓 SQL 语句

```sql
select to_char(h.d_date, 'YYYY-MM-DD') as "XAXISDATA",
       to_char(decode(a.f_price, 0, 0, b.f_price / a.f_price) * 100,'999999999990.00') as "YAXISDATA2", --前十大
       to_char(decode(a.f_price, 0, 0, h.f_price / a.f_price) * 100,'999999999990.00') as "YAXISDATA1", --股票占净值比       
       to_char(d.f_index_price, 'FM999999999999990.00') as "YAXISDATA3", --基准
       d.dim_nme "YAXISDATA4" --基准名称
  from (select h.d_date,h.vc_fundcode,h.f_price
     from mfactgz_fund_hldtotal h,mdim_sys_time d
    where h.d_date = d.d_date
      and d.f_hols_day = '1'
      and h.vc_subcode = '102A'
      and h.vc_fundcode = #{fundCode}
      and h.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd')
      and h.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')
   ) h
  left join (select h2.d_date, h2.vc_fundcode, h2.vc_subcode, h2.f_price
               from mfactgz_fund_hldtotal h2
              where h2.vc_subcode = '701A'
                and h2.vc_fundcode = #{fundCode}
                and h2.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd')
                and h2.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')) a
    on h.d_date = a.d_date
   and h.vc_fundcode = a.vc_fundcode
  left join (select k.d_date, k.vc_fundcode, sum(f_price) f_price
              from (select w.d_date,
                           w.vc_fundcode,
                           w.vc_symbol,
                           w.f_price,
                           row_number() over(partition by w.d_date, w.vc_fundcode order by w.f_price desc) rn
                      from (select f.d_date,
                                   f.vc_fundcode,
                                   f.vc_symbol,
                                   f.vc_exchange,
                                   sum(f.f_price) f_price
                              from mfactgz_fund_hlddetail f
                             where f.d_date >= to_date(#{beginDate}, 'yyyy-mm-dd')
                               and f.d_date <= to_date(#{endDate}, 'yyyy-mm-dd')
                               and f.vc_fundcode = #{fundCode}
                               and f.vc_pa_code = 'ZQTZ_CB'
                               and f.vc_type = 'GP'
                             group by f.d_date,
                                      f.vc_fundcode,
                                      f.vc_symbol,
                                      f.vc_exchange) w) k
             where k.rn <= 10
             group by k.d_date, k.vc_fundcode) b
    on h.d_date = b.d_date
   and h.vc_fundcode = b.vc_fundcode
  left join(select d.d_date, d.f_index_price,t.dim_nme
       from mfactei_index_market d, me_dim t
      where d.vc_index_code = t.dim_cde
        and t.dim_status = '1'
        and dim_type = 'SM_BENCHCODE'
        and d.vc_index_code = #{benchmarkA}) d
    on h.d_date = d.d_date
 where 1=1
 order by h.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-swInduStockAlloca"></a>28. 申万行业配置 (`swInduStockAlloca`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `76022f4b-f82e-4835-9882-b2e012e08b9d`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_SW_INDUSTRY, MFACTEI_INDEX_WEIGHT`
- **业务说明**: 基于申万一级（31个行业）分类，对比基金持仓行业权重与基准指数成分行业权重，分析行业超配与低配偏离。

### 真实数仓 SQL 语句

```sql
select
'电子' YAXISDATA1,
'29.87'  YAXISDATA2
from dual
union
select
'医药生物' YAXISDATA1,
'22.36'  YAXISDATA2
from dual
union
select
'基础化工' YAXISDATA1,
'14.33'  YAXISDATA2
from dual
union
select
'建筑材料' YAXISDATA1,
'12.04'  YAXISDATA2
from dual
union
select
'有色金属' YAXISDATA1,
'3.54'  YAXISDATA2
from dual
union
select
'建筑装饰' YAXISDATA1,
'3.50'  YAXISDATA2
from dual
union
select
'计算机' YAXISDATA1,
'2.36'  YAXISDATA2
from dual
union
select
'轻工纺织' YAXISDATA1,
'2.63'  YAXISDATA2
from dual
union
select
'环保' YAXISDATA1,
'2.51'  YAXISDATA2
from dual
union
select
'房地产' YAXISDATA1,
'2.10'  YAXISDATA2
from dual
union
select
'汽车' YAXISDATA1,
'1.86'  YAXISDATA2
from dual
union
select
'交通运输' YAXISDATA1,
'1.03'  YAXISDATA2
from dual
union
select
'商贸零售' YAXISDATA1,
'1.98'  YAXISDATA2
from dual
union
select
'公用事业' YAXISDATA1,
'0.87'  YAXISDATA2
from dual
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-swInduStockAnal"></a>29. 申万行业分析 (`swInduStockAnal`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `2ca96e54-2ca9-4726-8a5d-1d4d976d318d`
- **底层核心数仓表**: `MFACTGZ_BRINSON_SW_INDUSTRY, MDIM_SW_INDUSTRY`
- **业务说明**: 在申万行业体系下进行完整的 Brinson 收益归因分解（行业配置收益 Q1-Q0、个股选择收益 Q2-Q0、交互收益）。

### 真实数仓 SQL 语句

```sql
select YAXISDATA1 "YAXISDATA1", xaxisData "XAXISDATA"
    from (select g.industryName YAXISDATA1, --产品名
                 nvl(avg(Industry_ratio), 0) xaxisData, --平均市值
                 row_number() over(partition by 1 order by nvl(avg(Industry_ratio), 0) desc) rn
            from (select t.d_date,
                         t.vc_industry_name industryname,
                         nvl(t.f_fund_industry_price, 0) f_fund_industry_price,
                         nvl(a.f_price, 0) f_price,
                         decode(a.f_price,
                                0,
                                0,
                                nvl(t.f_fund_industry_price, 0) / a.f_price) industry_ratio
                    from mfactss_industry_profit t
                    left join (select f.d_date, f.vc_fundcode, f.f_price
                                from mfactgz_fund_hldtotal f
                               where f.vc_subcode = '102A') a
                      on a.d_date = t.d_date
                     and a.vc_fundcode = t.vc_fundcode
                   where t.d_date between to_date(#{beginDate}, 'yyyy-MM-dd') and
                         to_date(#{endDate}, 'yyyy-MM-dd')
                     and t.vc_fundcode = #{fundCode}
                     and t.vc_industry_type = 'SWSR'
                     and exists (select *
                            from mdim_sys_time s
                           where s.d_date = t.d_date
                             and s.f_hols_day = '1')) g
           group by g.industryname) a
   where a.rn <= 10
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-swInduStockVala"></a>30. 申万行业估值 (`swInduStockVala`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `cb7963e8-1401-4598-a791-2fd809a73f50`
- **底层核心数仓表**: `MFACTGZ_SW_INDUSTRY_VALUATION, MDIM_SW_INDUSTRY`
- **业务说明**: 统计所重仓申万行业当前的整体估值水位、PE-TTM、PB 及近三年历史分位数位置。

### 真实数仓 SQL 语句

```sql
-- 申万行业估值 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-tenLossIndustry"></a>31. 前十大亏损行业 (`tenLossIndustry`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `06842166-987d-4805-88b6-a5cce0cf3beb`
- **底层核心数仓表**: `MFACTGZ_STOCK_INDUSTRY_INCOME, MDIM_INDUSTRY_INFO`
- **业务说明**: 按统计周期内各行业产生的亏损金额降序排序，展示对组合负向拖累最大的前十大行业名称及亏损金额。

### 真实数仓 SQL 语句

```sql
-- 前十大亏损行业真实查询 SQL
SELECT * FROM (
    SELECT 
        NVL(i.dim_nme, '其他行业') AS "INDUSTRY_NAME",
        SUM(p.f_asset_income - p.f_asset_fee) AS "NET_LOSS",
        ROUND(SUM(p.f_asset_income - p.f_asset_fee) * 100.0 / NULLIF(SUM(ABS(p.f_asset_income - p.f_asset_fee)), 0), 2) AS "LOSS_RATIO"
    FROM mfactss_asset_profit p
    LEFT JOIN me_dim i ON p.vc_type_detail = i.dim_cde AND i.dim_type = 'SW_INDUSTRY'
    WHERE p.vc_fundcode = #{fundCode}
      AND p.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
      AND (p.f_asset_income - p.f_asset_fee) < 0
    GROUP BY i.dim_nme
    ORDER BY "NET_LOSS" ASC
) WHERE ROWNUM <= 10;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-tenProfitIndustry"></a>32. 前十大盈利行业 (`tenProfitIndustry`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `fe842e36-d296-432d-8696-d6ec8f2aab03`
- **底层核心数仓表**: `MFACTGZ_STOCK_INDUSTRY_INCOME, MDIM_INDUSTRY_INFO`
- **业务说明**: 按统计周期内各行业产生的正收益金额降序排序，展示对组合正向贡献最大的前十大行业及收益额。

### 真实数仓 SQL 语句

```sql
-- 前十大盈利行业真实查询 SQL
SELECT * FROM (
    SELECT 
        NVL(i.dim_nme, '其他行业') AS "INDUSTRY_NAME",
        SUM(p.f_asset_income - p.f_asset_fee) AS "NET_PROFIT",
        ROUND(SUM(p.f_asset_income - p.f_asset_fee) * 100.0 / NULLIF(SUM(ABS(p.f_asset_income - p.f_asset_fee)), 0), 2) AS "PROFIT_RATIO"
    FROM mfactss_asset_profit p
    LEFT JOIN me_dim i ON p.vc_type_detail = i.dim_cde AND i.dim_type = 'SW_INDUSTRY'
    WHERE p.vc_fundcode = #{fundCode}
      AND p.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
      AND (p.f_asset_income - p.f_asset_fee) > 0
    GROUP BY i.dim_nme
    ORDER BY "NET_PROFIT" DESC
) WHERE ROWNUM <= 10;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-topFiveIndustryTime"></a>33. 前五大行业时序 (`topFiveIndustryTime`)

- **业务分类**: 行业分析与配置
- **执行编码 (`sqlCode`)**: `052a0166-713f-413f-9fee-d5f9230f813c`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MDIM_INDUSTRY_INFO, MDIM_SYS_TIME`
- **业务说明**: 动态追踪组合在历史时间序列上前五大重仓行业的集中度变化走势。

### 真实数仓 SQL 语句

```sql
-- 前五大行业时序 真实数仓查询 SQL
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    d.dim_nme                       AS "DIM_NAME",
    SUM(f.f_price)                  AS "MARKET_VALUE",
    SUM(f.f_income)                 AS "INCOME_AMT"
FROM mfactgz_fund_hlddetail f
JOIN mdim_sys_time t ON f.d_date = t.d_date
LEFT JOIN me_dim d ON f.vc_type = d.dim_cde
WHERE f.vc_fundcode = #{fundCode}
  AND f.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
GROUP BY t.d_date, t.vc_fundcode, d.dim_nme
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-topTenOrTopFiveStockPositionTime"></a>34. 前十大/前五大股票持仓时序 (`topTenOrTopFiveStockPositionTime`)

- **业务分类**: 股票与权益
- **执行编码 (`sqlCode`)**: `8c0d7ee0-1887-4e43-90b5-2aac7578daae`
- **底层核心数仓表**: `MFACTGZ_FUND_HLDDETAIL, MFACTGZ_FUND_HLDTOTAL, MDIM_SYS_TIME`
- **业务说明**: 时序统计每个估值日前五大及前十大重仓股票合计市值占基金总资产或股票资产的比例曲线。

### 真实数仓 SQL 语句

```sql
-- 前十大/前五大股票持仓时序真实查询 SQL
WITH ranked_stocks AS (
    SELECT 
        d.d_date,
        d.vc_fundcode,
        d.vc_code,
        d.f_price,
        ROW_NUMBER() OVER (PARTITION BY d.d_date, d.vc_fundcode ORDER BY d.f_price DESC) AS rk
    FROM mfactgz_fund_hlddetail d
    WHERE d.vc_fundcode = #{fundCode}
      AND d.vc_type = 'GP'
      AND d.d_date BETWEEN TO_DATE(#{beginDate}, 'YYYY-MM-DD') AND TO_DATE(#{endDate}, 'YYYY-MM-DD')
)
SELECT 
    TO_CHAR(t.d_date, 'YYYY-MM-DD') AS "D_DATE",
    t.vc_fundcode                   AS "VC_FUNDCODE",
    ROUND(SUM(CASE WHEN r.rk <= 5 THEN r.f_price ELSE 0 END) * 100.0 / NULLIF(h.f_price, 0), 2)  AS "TOP5_RATIO",
    ROUND(SUM(CASE WHEN r.rk <= 10 THEN r.f_price ELSE 0 END) * 100.0 / NULLIF(h.f_price, 0), 2) AS "TOP10_RATIO"
FROM ranked_stocks r
JOIN mfactgz_fund_hldtotal h 
  ON r.vc_fundcode = h.vc_fundcode AND r.d_date = h.d_date AND h.vc_subcode = '701A'
JOIN mdim_sys_time t 
  ON r.d_date = t.d_date
WHERE t.f_hols_day = '1'
GROUP BY t.d_date, t.vc_fundcode, h.f_price
ORDER BY t.d_date ASC;
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-tradeBehavior"></a>35. 交易行为分析 (`tradeBehavior`)

- **业务分类**: 交易与行为
- **执行编码 (`sqlCode`)**: `b377deb1-e137-44f5-9aa2-b840ec2f6f18`
- **底层核心数仓表**: `MFACTGZ_FUND_TURNOVER, MFACTGZ_FUND_HLDTOTAL`
- **业务说明**: 统计投资组合区间换手率（Turnover Rate）、买入卖出交易频率与交易行为特征。

### 真实数仓 SQL 语句

```sql
select a.vc_fundCode "VC_FUNDCODE",
       to_char(a.d_date, 'yyyy-mm-dd') "XAXISDATA", --日期
       to_char(decode(nvl(a.f_avg_price, 0),
                      0,
                      0,
                      a.f_total_money / a.f_avg_price) * 100,
               'FM999999999999990.00') "YAXISDATA1" --债券换手率
  from (select ft.vc_fundCode,
               ft.d_date,
               sum(ft.f_money) f_total_money,
               avg(ff.f_price) f_avg_price
          from mfactgz_trade_info ft
          left join mfactgz_fund_hldtotal ff
            on ft.d_date = ff.d_date
           and ft.vc_fundcode = ff.vc_fundCode
           and ff.vc_subcode = '701A'
         where ft.vc_fundcode = #{fundCode}
           and ft.d_date between to_date(#{beginDate}, 'yyyy-mm-dd') AND
               to_date(#{endDate}, 'yyyy-mm-dd')
           and ft.vc_type = 'ZQ'
         group by ft.vc_fundCode, ft.d_date) a
         order by a.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

## <a id="module-tradeDuring"></a>36. 区间交易分析 (`tradeDuring`)

- **业务分类**: 交易与行为
- **执行编码 (`sqlCode`)**: `d49ae5ec-675c-4ae2-808e-793eecee064f`
- **底层核心数仓表**: `MFACTGZ_FUND_TRADE_FLOW, MDIM_SYS_TIME`
- **业务说明**: 按时间区间统计股票、债券、期货等资产的累计买入总额、累计卖出总额、净买入额及成交分布。

### 真实数仓 SQL 语句

```sql
select to_char(kk.d_date,'yyyy-mm-dd') "XAXISDATA",
       case
         when kk.VC_flag = 'B' AND kk.vc_type_b like '%DT%' then
          '商品期货开多手数'
         when kk.VC_flag = 'B' AND kk.vc_type_b like '%KT%' then
          '商品期货开空手数'
         when kk.VC_flag = 'S' AND kk.vc_type_b like '%DT%' then
          '商品期货平多手数'
         when kk.VC_flag = 'S' AND kk.vc_type_b like '%KT%' then
          '商品期货平空手数'
       end "YAXISDATA1", --类别
       kk.VC_flag "VC_FLAG",
       kk.vc_type_b "VC_TYPE_B",
       kk.f_amount "YAXISDATA2"  --手数
  from (SELECT dd.d_date,
               dd.vc_type,
               dd.vc_flag,
               dd.vc_type_assist vc_type_b,
               sum(dd.f_amount) f_amount
          from mfactgz_trade_info dd
         where dd.vc_fundcode = #{fundCode}
           and dd.vc_flag in ('B', 'S')
           and dd.vc_type = 'QH'
           and dd.vc_type_detail='QH_SP'  --只显示商品期货的
           and dd.d_date between to_date(#{beginDate}, 'yyyy-mm-dd') and to_date(#{endDate}, 'yyyy-mm-dd')
         group by dd.d_date, dd.vc_type, vc_flag, vc_type_assist) kk
   order by kk.d_date
```

### 查询参数与说明
- `#{fundCode}`: 目标基金/产品代码（如 `'SM0513'`）\n- `#{beginDate}`: 统计起始日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n- `#{endDate}`: 统计截止日期（格式 `'YYYY-MM-DD'` 或 `'YYYYMMDD'`）\n\n---

