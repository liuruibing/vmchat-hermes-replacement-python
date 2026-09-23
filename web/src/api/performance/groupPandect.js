import request from '@/utils/request'
export default {

  // 组合绩效情况总览获取前一个月的最后一个交易日
  prevMonthLastDay: async function (date) {

    return request({
      url: '/api/performance-overview/v1.0/prev-month-last-day/'+ date,
      method: 'post',
    })
  },

  // 组合绩效情况总览
  performanceOverview: async function (date,fundCodes,fundTypes,investTypes,orderBy,pageNum,pageSize) {

    return request({
      url: '/api/performance-overview/v1.0/fund-performance-overview-table/'+ date
      + '?fundCodes=' + fundCodes
      + '&fundTypes=' + fundTypes
      + '&investTypes=' + investTypes
      + '&orderBy=' + orderBy
      + '&pageNum=' + pageNum
      + '&pageSize=' + pageSize,
      method: 'post',
    })
  },

  // 组合绩效情况总览导出
  performanceOverviewExport: async function (date,fundCodes,fundTypes,investTypes,orderBy,pageNum,pageSize,name,month) {

    return request({
      url: '/api/performance-overview/v1.0/fund-performance-overview-table/'+ date
      + '?fundCodes=' + fundCodes
      + '&fundTypes=' + fundTypes
      + '&investTypes=' + investTypes
      + '&orderBy=' + orderBy
      + '&pageNum=' + pageNum
      + '&pageSize=' + pageSize
      + "&ex_tmp_name=" + name
      + "&month=" + month,
      method: 'post',
    })
  },

  // 亮点组合 问题组合 危机组合 1,2,3
  brightSpotFund: async function (date,fundCode,fundTypes,investTypes,type,orderStr) {

    return request({
      url: '/api/performance-overview/v1.0/bright-spot-fund'
      + '?nowdate=' + date
      + '&fundCode=' + fundCode
      + '&fundTypes=' + fundTypes
      + '&investTypes=' + investTypes
      + '&type='+ type
      + '&orderStr='+ orderStr,
      method: 'post',
    })
  },

  // 亮点组合 问题组合 危机组合 1,2,3  导出
  brightSpotFundExport: async function (date,fundCode,fundTypes,investTypes,type,orderStr,name,oneYear,twoYear,threeYear) {

    return request({
      url: '/api/performance-overview/v1.0/bright-spot-fund'
      + '?nowdate=' + date
      + '&fundCode=' + fundCode
      + '&fundTypes=' + fundTypes
      + '&investTypes=' + investTypes
      + '&type='+ type
      + '&orderStr='+ orderStr
      + "&ex_tmp_name=" + name
      + "&oneYear=" + oneYear
      + "&twoYear=" + twoYear
      + "&threeYear=" + threeYear,
      method: 'post',
    })
  },

  // 互联网金融个养产品
  internetFinanceProduct: async function (date,fundCode,investTypes,orderStr) {

    return request({
      url: '/api/performance-overview/v1.0/internet-finance-product' + '?nowdate=' + date + '&fundCode=' + fundCode + '&investTypes=' + investTypes + '&orderStr='+ orderStr,
      method: 'post',
    })
  },

  // 互联网金融个养产品
  internetFinanceProductExport: async function (date,fundCode,investTypes,orderStr,name) {

    return request({
      url: '/api/performance-overview/v1.0/internet-finance-product' + '?nowdate=' + date + '&fundCode=' + fundCode + '&investTypes=' + investTypes  + '&orderStr='+ orderStr + "&ex_tmp_name=" + name,
      method: 'post',
    })
  },






}
