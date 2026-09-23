import request from '@/utils/request'
import qs from 'qs'
export default {
  // 字典查询
  getTransferType: async function (params) {
    return request({
      url: '/api/edims/v1.0/listEdims.do?dimType=' + params,
      method: 'get'
    })
  },

  // 基金分红查询,列表查询
  getFundbonusList: async function (params) {
    return request({
      url: '/api/fundbonus/v1.0/fundBonuslist' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  // 基金分红查询,列表查询
  getHistoricalShareList: async function (params) {
    return request({
      url: '/api/fundbonus/v1.0/investorHisSharelist' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  // 基金分红查询,列表查询
  getShareCurrentsList: async function (params) {
    return request({
      url: '/api/fundbonus/v1.0/shareChangeLSlist' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  // 估值表,列表查询
  getFundGzList: async function (params) {
    return request({
      url: '/api/datasearch/v1.0/gzb' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
   // 估值表,列表查询
   getFundLBalanceList: async function (params) {
    return request({
      url: '/api/datasearch/v1.0/kmyeb' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  // 估值表,列表查询
  getFundTpgpbList: async function (params) {
   return request({
     url: '/api/datasearch/v1.0/tpgpb' + '?' + qs.stringify(params),
     method: 'POST'
   })
 },
 // 资产负债表损益表,列表查询
 getSheetProfitsList: async function (params) {
  return request({
    url: '/api/datasearch/v1.0/sheetprofits' + '?' + qs.stringify(params),
    method: 'POST'
  })
}
,
 // 所有者权益表,列表查询
 getOwnerInterestList: async function (params) {
  return request({
    url: '/api/datasearch/v1.0/ownerinterest' + '?' + qs.stringify(params),
    method: 'POST'
  })
}
,
 // 成交清算日报表,列表查询
 getTradeInfoList: async function (params) {
  return request({
    url: '/api/datasearch/v1.0/tradeinfo' + '?' + qs.stringify(params),
    method: 'POST'
  })
}
,
 // 估值表,列表查询
 getFundFcwvchList: async function (params) {
  return request({
    url: '/api/datasearch/v1.0/pzb' + '?' + qs.stringify(params),
    method: 'POST'
  })
}


}
