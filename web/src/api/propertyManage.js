/* 资产接口 */
import { post, get } from '@/utils/request'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

// 组合资产总览
export function portfolioListUrl (params) {
  return post('/api/asset/assetInfo/PortfolioList', qs.stringify(params), isForm)
}

// 字典表通用查询
// export function listEdimsUrl (dimType) {
//   return get(`/api/common/edimsCommon/listEdims/${dimType}`)
// }

// 人设部通用查询
export function listRulesUrl (typeNumber) {
  return get(`/api/common/rulesCommon/listRules/${typeNumber}`)
}

// 组合资产详情- 资产配置-资产分类下拉框
export function selectAssetTypeListUrl () {
  return post('/api/asset/detail/selectAssetTypeList')
}

// 组合资产详情-组合基本信息展示
export function portfolioListDetailUrl (params) {
  return post('/api/asset/assetInfo/PortfolioListDetail', qs.stringify(params), isForm)
}

// 组合资产详情-投资经理变动一览
export function managerPersonsByCodeUrl (params) {
  return post('/api/asset/assetInfo/ManagerPersonsByCode', qs.stringify(params), isForm)
}

// 综合持仓查询
export function syntheticalHoldUrl (params) {
  return post('/api/assert/holdSelect/syntheticalHold/list', qs.stringify(params), isForm)
}

// 综合持仓查询汇总
export function syntheticalHoldTotalUrl (params) {
  return post('/api/assert/holdSelect/syntheticalHold/listTotal', qs.stringify(params), isForm)
}

// 个股持仓查询
export function stockHoldUrl (params) {
  return post('/api/assert/holdSelect/stockHold/list', qs.stringify(params), isForm)
}

// 个股持仓查询汇总
export function stockHoldTotalUrl (params) {
  return post('/api/assert/holdSelect/stockHold/listTotal', qs.stringify(params), isForm)
}

// 债券持仓查询
export function bondHoldUrl (params) {
  return post('/api/assert/holdSelect/bondHold/list', qs.stringify(params), isForm)
}

// 债券持仓查询汇总
export function bondHoldTotalUrl (params) {
  return post('/api/assert/holdSelect/bondHold/listTotal', qs.stringify(params), isForm)
}

// 子基金持仓查询
export function childFundHoldUrl (params) {
  return post('/api/assert/holdSelect/childFundHold/list', qs.stringify(params), isForm)
}

// 子基金持仓查询汇总
export function childFundHoldTotalUrl (params) {
  return post('/api/assert/holdSelect/childFundHold/listTotal', qs.stringify(params), isForm)
}

// 组合资产详情-收益率走势
export function selectYieldTrendUrl (params) {
  return post('/api/asset/assetInfo/SelectYieldTrend', qs.stringify(params), isForm)
}

// 资产配置信息展示
export function assetConfigurationUrl (params) {
  return post('/api/asset/detail/assetConfiguration/list', qs.stringify(params), isForm)
}

// 组合资产详情-资产配置
export function selectAssetAllocationUrl (params) {
  return post('/api/asset/assetInfo/selectAssetAllocation', qs.stringify(params), isForm)
}

// 资产配置监控
export function assetMonitorUrl (params) {
  return get('/api/manageView/nvestmentCommittee/assetMonitor', params)
}

// 组合资产明细-资产配置
export function selectAssetAllocationDetailUrl (params) {
  return post('/api/asset/detail/selectAssetAllocation', qs.stringify(params), isForm)
}

// 资产配置-资产分布列表
export function selectAssertListUrl (params) {
  return post('/api/asset/detail/assetConfiguration/selectAssertList', qs.stringify(params), isForm)
}

// 盈亏变动信息展示
export function profitLossChangeListUrl (params) {
  return post('/api/profitLoss/profitLossChange/list', qs.stringify(params), isForm)
}

// 盈亏走势
export function profitLossChangeListTodayListUrl (params) {
  return post('/api/profitLoss/profitLossChange/today/list', qs.stringify(params), isForm)
}

// 持仓事件查询
export function holdEventListUrl (params) {
  return post('/api/asset/detail/selectPositionEventList', qs.stringify(params), isForm)
}

// 组合资产详情-持仓事件查询
export function selectPositionEventListUrl (params) {
  return post('/api/asset/assetInfo/selectPositionEventList', qs.stringify(params), isForm)
}

// 个券变动流水查询
export function couponSerialListUrl (params) {
  return post('/api/asset/transaction/couponSerial/list', qs.stringify(params), isForm)
}

// 资金流入流出
export function fundInOutListUrl (params) {
  return post('/api/asset/transaction/fundInOut/list', qs.stringify(params), isForm)
}

// 费用查询
export function costListUrl (params) {
  return post('/api/asset/detail/cost/list', qs.stringify(params), isForm)
}

// 重合度信息展示
export function superpositionRatioListUrl (params) {
  return post('/api/asset/detail/superpositionRatio/list', qs.stringify(params), isForm)
}

// 重合度分析展示
export function selectCoincidenceAnalysisUrl (params) {
  return post('/api/asset/detail/selectCoincidenceAnalysis', qs.stringify(params), isForm)
}

// 重合度信息展示Excel导出
export function superpositionRatioListExcelUrl (params) {
  return post('/api/asset/detail/superpositionRatio/listExcel', qs.stringify(params), isForm)
}

// 最新估值日期
export function fundNewGzDateUrl (params) {
  return post(`/api/performance-detail/v1.0/fund-new-gz-date/${params}`)
}
