/* 证券分析接口 */
import { post, excelPost } from '@/utils/request'
import validate from '@/utils/validate'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

// 公共处理函数
function commonUrl (requesturl, params) {
  // 拼接字符串
  let str = ''
  // 全路径
  let path = ''
  // 拼接字符串
  for ( let k in params) {
    // 处理特殊字符串
    params[k] = validate.validateCharacter(params[k])
    if (str) {
      str = `${str}&${k}=${params[k]}`
    } else {
      str = `${k}=${params[k]}`
    }
    // 处理参数中带加号的问题
    // str = str.replace(/\+/g, '%2B')
  }
  path = requesturl + '?' + str
  return path
}

// 投资经理视图-证券分析-汇总
export function investSumAnalysisUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investSumAnalysis', params), payload)
}

// 投资经理视图-证券分析-债券分析-前十大集中度
export function investManagerFundViewUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investManagerFundView', params), payload)
}

// 投资经理视图-证券分析-债券分析-前十大集中度（导出excel）
export function investManagerFundViewExcelUrl (params, payload) {
  // return excelPost(commonUrl('/api/manageView/securitiesAnalysis/investManagerFundView', params), payload)
  return post(commonUrl('/api/manageView/securitiesAnalysis/investManagerFundView', params), payload)
}

// 投资经理视图-证券分析-前十大集中度（债券/债券规模 明细）
export function investBondAnalysisDetailsUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondAnalysisDetails', params), payload)
}

// 投资经理视图-证券分析-前十大集中度（发行人明细）
export function investPublisherAnalysisDetailsUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investPublisherAnalysisDetails', params), payload)
}

// 投资经理视图-证券分析-债券分析-债券类属结构变化（左）
export function investBondLeftGenericUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondLeftGeneric', params), payload)
}

// 投资经理视图-证券分析-债券分析-债券类属结构变化（右）
export function investBondGenericUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondGeneric', params), payload)
}
// 投资经理视图-证券分析-债券分析-债券类属结构变化 new
export function investBondGenericNewUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondGenericNew', params), payload)
}

// 投资经理视图-证券分析-债券分析-主体评级
export function investBondSubjectRatingUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondSubjectRating', params), payload)
}

// 投资经理视图-证券分析-债券分析-债项评级
export function investBondDebtRatingUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondDebtRating', params), payload)
}

// 投资经理视图-证券分析-债券分析-回购占比
export function investBondBuybackRatioUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondBuybackRatio', params), payload)
}

// 投资经理视图-证券分析-债券分析-期末分布(剩余期限)
export function investBondTerminalTimeUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondTerminalTime', params), payload)
}

// 投资经理视图-证券分析-债券分析-期末分布(行业)
export function investBondFinalDistributionUrl (params, payload) {
  return post(commonUrl('/api/manageView/securitiesAnalysis/investBondFinalDistribution', params), payload)
}

// 证券分析-港股分析
export function selectHkAnalysisUrl (params) {
  return post('/api/manageView/stockAningysis/selectHkAnalysis', qs.stringify(params), isForm)
}

// 证券分析-港股分析详情
export function hkAnalysisDetailsUrl (params) {
  return post('/api/manageView/stockAningysis/hkAnalysisDetails', qs.stringify(params), isForm)
}

// 证券分析-非标分析
export function selectnonStandardAnalysisUrl (params) {
  return post('/api/manageView/stockAningysis/selectnonStandardAnalysis', qs.stringify(params), isForm)
}

// 证券分析-非标分析详情
export function nonStandardAnalysisDetailsUrl (params) {
  return post('/api/manageView/stockAningysis/nonStandardAnalysisDetails', qs.stringify(params), isForm)
}

// 证券分析-存款分析
export function selectCoincidenceAnalysisUrl (params) {
  return post('/api/manageView/stockAningysis/selectCoincidenceAnalysis', qs.stringify(params), isForm)
}

// 证券分析-基金分析
export function selectFundAnalysisUrl (params) {
  return post('/api/manageView/stockAningysis/selectFundAnalysis', qs.stringify(params), isForm)
}

// 证券分析-基金分析详情
export function selectFundAnalysisDetailsUrl (params) {
  return post('/api/manageView/stockAningysis/selectFundAnalysisDetails', qs.stringify(params), isForm)
}

// 证券分析-股票分析（汇总）
export function stockPriceDateUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/stockPriceDate', params), payload)
}

// 证券分析-股票分析（股票行业分布）
export function stockIndustryDistributionUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/stockIndustryDistribution', params), payload)
}

// 证券分析-股票分析（股票仓位）
export function findStockPositionUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/findStockPosition', params), payload)
}

// 证券分析-股票分析（流入流出）
export function findInflowAndOutflowUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/findInflowAndOutflow', params), payload)
}

// 证券分析-股票分析（个股占股票资产比例）
export function frontShareOfStockUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/frontShareOfStock', params), payload)
}

// 证券分析-股票分析（个股占股票资产比例详情）
export function stockAnalysisInvestBondAnalysisDetailsUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/investBondAnalysisDetails', params), payload)
}

// 证券分析-股票分析（PE）
export function stockPeDistributionUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/stockPeDistribution', params), payload)
}

// 证券分析-股票分析（PB）
export function stockPbDistributionUrl (params, payload) {
  return post(commonUrl('/api/manageView/stockAnalysis/stockPbDistribution', params), payload)
}
