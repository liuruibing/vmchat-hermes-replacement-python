/* 风险管理接口 */
import { post } from '@/utils/request'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }


// 风险管理-集中度分析
export function doConcentrationAnalysisUrl (params) {
  return post('/api/riskManager/riskController/doConcentrationAnalysis', qs.stringify(params), isForm)
}

// 风险管理-流动性风险分析-最近7天变现图
export function cashInSenvenDayChartsUrl (params) {
  return post('/api/riskManager/riskController/cashInSenvenDayCharts', qs.stringify(params), isForm)
}

// 风险管理-流动性风险分析-最近7天变现列表
export function cashInSenvenDayTableUrl (params) {
  return post('/api/riskManager/riskController/cashInSenvenDayTable', qs.stringify(params), isForm)
}

// 风险管理-流动性风险分析-利率弹性
export function rateElasticityUrl (params) {
  return post('/api/riskManager/riskController/rateElasticity', qs.stringify(params), isForm)
}

// 风险管理-流动性风险分析-杠杆比例
export function leverageRatiosUrl (params) {
  return post('/api/riskManager/riskController/leverageRatios', qs.stringify(params), isForm)
}

// 证券分析-返回开始日期
export function selectEndDateUrl (params) {
  return post('/api/manageView/stockAningysis/selectEndDate', qs.stringify(params), isForm)
}
