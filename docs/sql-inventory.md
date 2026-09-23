# VM 模块与 SQL Code 清单清单

> 本文档汇总了系统中全部 **36 个 VM 报表模块**、执行契约 `sqlCode`、数据库配置名称、后端运行模式以及对应的 Wiki 知识库文档路径。

## 一、元数据基础信息
- **数据库**: OceanBase (Oracle 模式)
- **所在 Schema**: `DD_PORTAL`
- **配置主表**: `CR_SQL_INFO` (字段: `VC_CODE` = sqlCode, `VC_SQL` = 转发URL/SQL, `F_TYPE_RUN` = 运行模式, `VC_DATA_TEST` = 测试JSON数据)
- **运行模式**: `F_TYPE_RUN = 4`（代表通过统一数据服务网关转发至后台绩效计算微服务 `{$xcjxApiDomainUrl}/perf/api/reportData/sql/{sqlCode}?`）

## 二、全量 36 个 VM 模块对照清单

| 序号 | 模块标识 (moduleId) | 模块名称 | 执行编码 (sqlCode) | 数据库名称 (VC_SQL_NAME) | 数据形态 | 子模块 (submodules) | Wiki 规范路径 |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `assetContribute` | 大类资产收益贡献 | `4c15f9fd-98c1-4280-b7bb-56893691279a` | 大类资产收益贡献-信创 | 单数据集 (数组, 7 项) | 无 | [`assetContribute.md`](../resources/catalog/modules/assetContribute.md) |
| 2 | `averagePePb` | 持仓平均PE/PB时序 | `cf8b548d-50d3-4a92-bde5-784bf707733f` | 持仓平均PE/PB时序-信创 | 单数据集 (数组, 21 项) | 无 | [`averagePePb.md`](../resources/catalog/modules/averagePePb.md) |
| 3 | `bondConcentrate` | 债券持仓集中度 | `ec66b44b-5e8b-4057-8046-79dd6798eee7` | 债券持仓集中度-信创 | 多数据集 (topNData, tabData) | 无 | [`bondConcentrate.md`](../resources/catalog/modules/bondConcentrate.md) |
| 4 | `bondDurationTiming` | 债券久期变动时序 | `2010a50e-3f6a-478c-8dc2-796df2799f10` | 债券久期变动时序-信创 | 多数据集 (dayDataColumn, dayData) | 无 | [`bondDurationTiming.md`](../resources/catalog/modules/bondDurationTiming.md) |
| 5 | `campisiBondAnal` | Campisi债券绩效归因 | `95b8781e-312c-4c58-9d45-c3c7e63e2412` | Campisi债券绩效归因-信创 | 多数据集 (tabData, totalData) | 无 | [`campisiBondAnal.md`](../resources/catalog/modules/campisiBondAnal.md) |
| 6 | `cashPositionTiming` | 现金类持仓时序 | `b9f4277e-2793-4a0d-b9ed-e665e4bbd717` | 现金类持仓时序-信创 | 单数据集 (数组, 19 项) | 无 | [`cashPositionTiming.md`](../resources/catalog/modules/cashPositionTiming.md) |
| 7 | `commodityFutures` | 商品期货板块收益贡献 | `6ff642c7-7364-4f0b-9e6b-a9d259b49d0e` | 商品期货板块收益贡献-信创 | 单数据集 (数组, 5 项) | 无 | [`commodityFutures.md`](../resources/catalog/modules/commodityFutures.md) |
| 8 | `commodityFuturesExposureTiming` | 商品期货净敞口时序 | `a26dc9c7-6ca1-49f0-a93f-bceeedea3aee` | 商品期货净敞口时序-信创 | 单数据集 (数组, 19 项) | 无 | [`commodityFuturesExposureTiming.md`](../resources/catalog/modules/commodityFuturesExposureTiming.md) |
| 9 | `commodityProfitLoss` | 期货十大盈利亏损品种 | `b0a11b9d-5709-4c27-a0c0-57e859b2d9e8` | 期货十大盈利亏损品种-信创 | 多数据集 (YLData, KSData) | topLossCommodities, topProfitCommodities | [`commodityProfitLoss.md`](../resources/catalog/modules/commodityProfitLoss.md) |
| 10 | `creditRiskRateDistribution` | 信用风险评级分布 | `944d0936-066f-4d4c-ad16-67767a431d7a` | 信用风险评级分布-信创 | 单数据集 (数组, 3 项) | 无 | [`creditRiskRateDistribution.md`](../resources/catalog/modules/creditRiskRateDistribution.md) |
| 11 | `fixedPositionTiming` | 固定收益类持仓时序 | `7c426689-80d2-4ce0-83d8-26c45fe5493f` | 固定收益类持仓时序-信创 | 单数据集 (数组, 19 项) | 无 | [`fixedPositionTiming.md`](../resources/catalog/modules/fixedPositionTiming.md) |
| 12 | `fundDurationTiming` | 组合加权久期时序 | `7d29ed40-0d69-4cd1-93a8-0a2bf9eac9cd` | 组合加权久期时序-信创 | 单数据集 (数组, 19 项) | 无 | [`fundDurationTiming.md`](../resources/catalog/modules/fundDurationTiming.md) |
| 13 | `hldStockNumTime` | 持股数量时序变化图 | `2f3f7b80-5c28-407f-90c5-5d2464eaf5a0` | 持股数量时序变化图-信创 | 单数据集 (数组, 281 项) | 无 | [`hldStockNumTime.md`](../resources/catalog/modules/hldStockNumTime.md) |
| 14 | `holdPlate` | A股持仓指数及板块时序 | `caa5b2df-8278-458e-b176-db71cce9a024` | A股持仓指数及板块时序-信创 | 多数据集 (dayIndexData, dayBoardColumn, dayBoardData) | 无 | [`holdPlate.md`](../resources/catalog/modules/holdPlate.md) |
| 15 | `hsInduStockAlloca` | 华泰柏瑞行业配置 | `4dadd10a-92c2-43b3-b8a7-de798cdebb5c` | 港股行业配置风险-信创 | 单数据集 (数组, 3 项) | 无 | [`hsInduStockAlloca.md`](../resources/catalog/modules/hsInduStockAlloca.md) |
| 16 | `hsInduStockAnal` | 华泰柏瑞行业分析 | `73ab4b7f-b543-4b94-ac6c-50685997d361` | 港股行业brinson分解-信创 | 单数据集 (数组, 13 项) | 无 | [`hsInduStockAnal.md`](../resources/catalog/modules/hsInduStockAnal.md) |
| 17 | `hsInduStockVala` | 华泰柏瑞行业估值 | `125bb87f-2c9c-485e-8042-87ce0d60cd30` | 港股行业估值风险-信创 | 单数据集 (数组, 3 项) | 无 | [`hsInduStockVala.md`](../resources/catalog/modules/hsInduStockVala.md) |
| 18 | `industryMonitor` | 行业监控 | `8c627513-5936-4936-af12-66ad0ea1a947` | A股行业监控-信创 | 多数据集 (timeLineData, tabData, bthyData, btpieData) | 无 | [`industryMonitor.md`](../resources/catalog/modules/industryMonitor.md) |
| 19 | `maxDrawdownFQ` | 最大回撤与修复时序 | `f6dd749d-df80-41d4-b98f-9ace45fb5544` | vm风险指标通用查询-信创 | 单数据集 (数组, 9 项) | 无 | [`maxDrawdownFQ.md`](../resources/catalog/modules/maxDrawdownFQ.md) |
| 20 | `netValMonitor` | 净值走势监控 | `8c757339-83c8-4e0b-adae-76e3cec96a8d` | 净值走势图-Echart-信创 | 单数据集 (数组, 19 项) | 无 | [`netValMonitor.md`](../resources/catalog/modules/netValMonitor.md) |
| 21 | `netValue` | 产品规模走势 | `38ac7662-b120-4cb9-9fdf-8becaf856723` | 产品规模走势-信创 | 多数据集 (lastData, hisData) | latestNetValue, netValueTrend | [`netValue.md`](../resources/catalog/modules/netValue.md) |
| 22 | `overallFutures` | 期货总持仓及收益 | `b435f30d-6914-4916-93d6-3c1e8d3e510e` | 期货大类归因-信创 | 单数据集 (数组, 2 项) | 无 | [`overallFutures.md`](../resources/catalog/modules/overallFutures.md) |
| 23 | `positionIndustry` | 行业持仓分布 | `d8ac50c1-b41c-498e-8c8a-bd6a577177a6` | 股票期末持仓行业占比-信创 | 单数据集 (数组, 3 项) | 无 | [`positionIndustry.md`](../resources/catalog/modules/positionIndustry.md) |
| 24 | `productInfo` | 产品基本信息 | `4475dbc6-a3f9-4e37-bb8b-fda45fda68fc` | 产品基本信息-信创 | 单数据集 (数组, 1 项) | 无 | [`productInfo.md`](../resources/catalog/modules/productInfo.md) |
| 25 | `rewardRisk` | 风险与收益指标 | `f6dd749d-df80-41d4-b98f-9ace45fb5544` | vm风险指标通用查询-信创 | 单数据集 (数组, 9 项) | 无 | [`rewardRisk.md`](../resources/catalog/modules/rewardRisk.md) |
| 26 | `riskValue` | 风险指标分析 | `8abc19f5-f2c9-4cff-8a89-48884270d042` | VaR-信创 | 多数据集 (beta, varval, varrate, esval, esrate) | 无 | [`riskValue.md`](../resources/catalog/modules/riskValue.md) |
| 27 | `stockExposureTiming` | 股票净敞口时序 | `712b930b-87a5-4cba-8da0-3671d4c8dc54` | 股票净敞口时序-信创 | 单数据集 (数组, 19 项) | 无 | [`stockExposureTiming.md`](../resources/catalog/modules/stockExposureTiming.md) |
| 28 | `swInduStockAlloca` | 申万行业配置 | `76022f4b-f82e-4835-9882-b2e012e08b9d` | A股行业配置风险-信创 | 单数据集 (数组, 6 项) | 无 | [`swInduStockAlloca.md`](../resources/catalog/modules/swInduStockAlloca.md) |
| 29 | `swInduStockAnal` | 申万行业分析 | `2ca96e54-2ca9-4726-8a5d-1d4d976d318d` | A股行业brinson分解-信创 | 单数据集 (数组, 32 项) | 无 | [`swInduStockAnal.md`](../resources/catalog/modules/swInduStockAnal.md) |
| 30 | `swInduStockVala` | 申万行业估值 | `cb7963e8-1401-4598-a791-2fd809a73f50` | A股行业估值风险-信创 | 单数据集 (数组, 7 项) | 无 | [`swInduStockVala.md`](../resources/catalog/modules/swInduStockVala.md) |
| 31 | `tenLossIndustry` | 前十大亏损行业 | `06842166-987d-4805-88b6-a5cce0cf3beb` | A股前十亏损行业-信创 | 单数据集 (数组, 4 项) | 无 | [`tenLossIndustry.md`](../resources/catalog/modules/tenLossIndustry.md) |
| 32 | `tenProfitIndustry` | 前十大盈利行业 | `fe842e36-d296-432d-8696-d6ec8f2aab03` | A股前十盈利行业-信创 | 单数据集 (数组, 5 项) | 无 | [`tenProfitIndustry.md`](../resources/catalog/modules/tenProfitIndustry.md) |
| 33 | `topFiveIndustryTime` | 前五大行业时序 | `052a0166-713f-413f-9fee-d5f9230f813c` | A股行业集中度-信创 | 多数据集 (dayDataColumn, dayData) | 无 | [`topFiveIndustryTime.md`](../resources/catalog/modules/topFiveIndustryTime.md) |
| 34 | `topTenOrTopFiveStockPositionTime` | 前十大/前五大股票持仓时序 | `8c0d7ee0-1887-4e43-90b5-2aac7578daae` | 个股持仓前十/前五占比时序-信创 | 单数据集 (数组, 19 项) | 无 | [`topTenOrTopFiveStockPositionTime.md`](../resources/catalog/modules/topTenOrTopFiveStockPositionTime.md) |
| 35 | `tradeBehavior` | 交易行为分析 | `b377deb1-e137-44f5-9aa2-b840ec2f6f18` | 组合换手率-信创 | 多数据集 (turnOverData, dayDataColumn, dayData) | 无 | [`tradeBehavior.md`](../resources/catalog/modules/tradeBehavior.md) |
| 36 | `tradeDuring` | 区间交易分析 | `d49ae5ec-675c-4ae2-808e-793eecee064f` | 期间交易额-信创 | 单数据集 (数组, 5 项) | 无 | [`tradeDuring.md`](../resources/catalog/modules/tradeDuring.md) |

## 三、sqlCode 唯一性说明
- 全量 36 个模块中，共有 **35 个唯一 `sqlCode`**：
  - `maxDrawdownFQ`（最大回撤与修复时序）与 `rewardRisk`（风险与收益指标）共享同一 `sqlCode`：`f6dd749d-df80-41d4-b98f-9ace45fb5544`，返回多数据集结构，由前端 DSL 分别抽取渲染。
- 包含显式子模块的模块有：
  - `netValue` (产品规模走势): `latestNetValue` (最新净值), `netValueTrend` (走势图)
  - `commodityProfitLoss` (期货十大盈利亏损品种): `topProfitCommodities` (前十盈利), `topLossCommodities` (前十亏损)

## 四、相关文件索引
- **全量模块详细 SQL/接口技术文档**: [`docs/vm-modules-sql-detail.md`](./vm-modules-sql-detail.md)
- **DBX / 数据库快速查询脚本**: [`docs/scripts/export_all_vm_sql_info.sql`](./scripts/export_all_vm_sql_info.sql)
- **执行契约定义**: [`resources/catalog/execution-contract.json`](../resources/catalog/execution-contract.json)
- **子模块定义**: [`resources/catalog/submodules.json`](../resources/catalog/submodules.json)
