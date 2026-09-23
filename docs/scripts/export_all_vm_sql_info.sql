-- ================================================================================
-- 银河项目 VM 模块 SQL/接口配置一键查询脚本 (OceanBase Oracle 模式 / DD_PORTAL)
-- 可在 DBX / DBeaver / Navicat 中直接运行查询
-- ================================================================================

SELECT 
    c.VC_CODE                                         AS "sqlCode",
    c.VC_SQL_NAME                                     AS "模块名称",
    CASE c.F_TYPE_RUN
        WHEN '1' THEN '1 - 原生SQL'
        WHEN '2' THEN '2 - BO业务对象'
        WHEN '3' THEN '3 - SQL+BO'
        WHEN '4' THEN '4 - 微服务JSON URL'
        WHEN '6' THEN '6 - 存储过程'
        ELSE c.F_TYPE_RUN
    END                                               AS "运行类型",
    c.VC_SOURCE_CODE                                  AS "数据源",
    c.F_ENABLE                                        AS "启用状态",
    c.VC_SQL                                          AS "转发URL/SQL内容",
    c.VC_SQL_TEST                                     AS "测试SQL/URL",
    c.VC_DATA_TEST                                    AS "样例数据JSON"
FROM CR_SQL_INFO c
WHERE c.VC_CODE IN (
    '4c15f9fd-98c1-4280-b7bb-56893691279a', -- assetContribute (大类资产收益贡献)
    'cf8b548d-50d3-4a92-bde5-784bf707733f', -- averagePePb (持仓平均PE/PB时序)
    'ec66b44b-5e8b-4057-8046-79dd6798eee7', -- bondConcentrate (债券持仓集中度)
    '2010a50e-3f6a-478c-8dc2-796df2799f10', -- bondDurationTiming (债券久期变动时序)
    '95b8781e-312c-4c58-9d45-c3c7e63e2412', -- campisiBondAnal (Campisi债券绩效归因)
    'b9f4277e-2793-4a0d-b9ed-e665e4bbd717', -- cashPositionTiming (现金类持仓时序)
    '6ff642c7-7364-4f0b-9e6b-a9d259b49d0e', -- commodityFutures (商品期货板块收益贡献)
    'a26dc9c7-6ca1-49f0-a93f-bceeedea3aee', -- commodityFuturesExposureTiming (商品期货净敞口时序)
    'b0a11b9d-5709-4c27-a0c0-57e859b2d9e8', -- commodityProfitLoss (期货十大盈利亏损品种)
    '944d0936-066f-4d4c-ad16-67767a431d7a', -- creditRiskRateDistribution (信用风险评级分布)
    '7c426689-80d2-4ce0-83d8-26c45fe5493f', -- fixedPositionTiming (固定收益类持仓时序)
    '7d29ed40-0d69-4cd1-93a8-0a2bf9eac9cd', -- fundDurationTiming (组合加权久期时序)
    '2f3f7b80-5c28-407f-90c5-5d2464eaf5a0', -- hldStockNumTime (持股数量时序变化图)
    'caa5b2df-8278-458e-b176-db71cce9a024', -- holdPlate (A股持仓指数及板块时序)
    '4dadd10a-92c2-43b3-b8a7-de798cdebb5c', -- hsInduStockAlloca (华泰柏瑞行业配置)
    '73ab4b7f-b543-4b94-ac6c-50685997d361', -- hsInduStockAnal (华泰柏瑞行业分析)
    '125bb87f-2c9c-485e-8042-87ce0d60cd30', -- hsInduStockVala (华泰柏瑞行业估值)
    '8c627513-5936-4936-af12-66ad0ea1a947', -- industryMonitor (行业监控)
    'f6dd749d-df80-41d4-b98f-9ace45fb5544', -- maxDrawdownFQ (最大回撤与修复时序)
    '8c757339-83c8-4e0b-adae-76e3cec96a8d', -- netValMonitor (净值走势监控)
    '38ac7662-b120-4cb9-9fdf-8becaf856723', -- netValue (产品规模走势)
    'b435f30d-6914-4916-93d6-3c1e8d3e510e', -- overallFutures (期货总持仓及收益)
    'd8ac50c1-b41c-498e-8c8a-bd6a577177a6', -- positionIndustry (行业持仓分布)
    '4475dbc6-a3f9-4e37-bb8b-fda45fda68fc', -- productInfo (产品基本信息)
    'f6dd749d-df80-41d4-b98f-9ace45fb5544', -- rewardRisk (风险与收益指标)
    '8abc19f5-f2c9-4cff-8a89-48884270d042', -- riskValue (风险指标分析)
    '712b930b-87a5-4cba-8da0-3671d4c8dc54', -- stockExposureTiming (股票净敞口时序)
    '76022f4b-f82e-4835-9882-b2e012e08b9d', -- swInduStockAlloca (申万行业配置)
    '2ca96e54-2ca9-4726-8a5d-1d4d976d318d', -- swInduStockAnal (申万行业分析)
    'cb7963e8-1401-4598-a791-2fd809a73f50', -- swInduStockVala (申万行业估值)
    '06842166-987d-4805-88b6-a5cce0cf3beb', -- tenLossIndustry (前十大亏损行业)
    'fe842e36-d296-432d-8696-d6ec8f2aab03', -- tenProfitIndustry (前十大盈利行业)
    '052a0166-713f-413f-9fee-d5f9230f813c', -- topFiveIndustryTime (前五大行业时序)
    '8c0d7ee0-1887-4e43-90b5-2aac7578daae', -- topTenOrTopFiveStockPositionTime (前十大/前五大股票持仓时序)
    'b377deb1-e137-44f5-9aa2-b840ec2f6f18', -- tradeBehavior (交易行为分析)
    'd49ae5ec-675c-4ae2-808e-793eecee064f' -- tradeDuring (区间交易分析)
)
ORDER BY c.D_CREATE_TIME DESC;

-- --------------------------------------------------------------------------------
-- 附录：数仓中针对大类资产绩效归因/收益贡献的原生查询 SQL 样例 (F_TYPE_RUN = 1)
-- --------------------------------------------------------------------------------
SELECT VC_CODE, VC_SQL_NAME, VC_SQL
FROM CR_SQL_INFO
WHERE VC_CODE IN ('89576d7b8fb6499186e5f268e5aac0c2', 'd9e1e9a3-2045-425a-ba7d-4f5820f89a2b');
