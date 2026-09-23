import request from '@/utils/request'
export default {

  // 管理组合整体情况 组合业绩情况接口
  portfolioPerformance: async function (date,groupType,investTypes, keyword, orderStr) {

    return request({
      url: '/api/manageView/managerView/performance/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + '&keyword=' + keyword,
      method: 'get',
    })
  },

  // 管理组合整体情况 组合业绩情况 导出接口
  portfolioPerformanceExport: async function (date,groupType,investTypes, keyword, orderStr,name) {

    return request({
      url: '/api/manageView/managerView/performance/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + '&keyword=' + keyword + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  // 管理组合整体情况 资产净值 组合数量
  totalPriceAndFundTotal: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/totalPriceAndFundTotal/' + date + '/' + groupType,
      method: 'get',
    })
  },
  // 资产变动走势
  propertyChangeTrend: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/trend/' + date + '/' + groupType,
      method: 'get',
    })
  },
  // 近一年资产净值增长情况 --按组合类型
    allScaleGrowCon: async function (beginDate,endDate,groupType) {

    return request({
      url: '/api/manageView/managerView/fundByType/' + beginDate + '/' + endDate + '/' + groupType,
      method: 'get',
    })
  },
  // 近一年资产配置走势图
  assetTrend: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/assetTrend/' + date + '/' + groupType,
      method: 'get',
    })
  },
  // 近一年资产净值增长情况 --按资产配置
  assetGrowthByConfig: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/assetGrowthByConfig/' + date + '/' + groupType,
      method: 'get',
    })
  },
  // 近一年三支柱资产走势图
  threeByBrace: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/byBrace/' + date + '/' + groupType,
      method: 'get',
    })
  },
  //近一年资产净值增长情况 --按三支柱
  assetGrowByBrace: async function (date,groupType) {

    return request({
      url: '/api/manageView/managerView/assetGrowByBrace/' + date + '/' + groupType,
      method: 'get',
    })
  },
  //新设组合
  newFund: async function (date,groupType,investTypes,orderStr) {

    return request({
      url: '/api/manageView/managerView/newFund/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes,
      method: 'get',
    })
  },
  //新设组合导出
  newFundExport: async function (date,groupType,investTypes,orderStr,name) {

    return request({
      url: '/api/manageView/managerView/newFund/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  //到期组合
  expireFund: async function (date,groupType,investTypes,orderStr) {

    return request({
      url: '/api/manageView/managerView/expireFund/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes,
      method: 'get',
    })
  },
  //到期组合导出
  expireFundExport: async function (date,groupType,investTypes,orderStr,name) {

    return request({
      url: '/api/manageView/managerView/expireFund/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  //组合大额流入
  businIn: async function (date,groupType,investTypes,orderStr) {

    return request({
      url: '/api/manageView/managerView/businIn/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes,
      method: 'get',
    })
  },
  //组合大额流入
  businInExport: async function (date,groupType,investTypes,orderStr,name) {

    return request({
      url: '/api/manageView/managerView/businIn/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  //组合大额流出
  businOut: async function (date,groupType,investTypes,orderStr) {

    return request({
      url: '/api/manageView/managerView/businOut/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes,
      method: 'get',
    })
  },
  //组合大额流出 导出
  businOutExport: async function (date,groupType,investTypes,orderStr,name) {

    return request({
      url: '/api/manageView/managerView/businOut/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  //组合托管情况
  fundTrusteeship: async function (date,groupType,investTypes,orderStr) {

    return request({
      url: '/api/manageView/managerView/fundTrusteeship/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes ,
      method: 'get',
    })
  },
  //组合托管情况 导出
  fundTrusteeshipExport: async function (date,groupType,investTypes,orderStr,name) {

    return request({
      url: '/api/manageView/managerView/fundTrusteeship/' + date + '/' + groupType + '?orderStr=' + orderStr + '&investTypes=' + investTypes  + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },
  // 绩效情况投资四象限
  invest4Quadrant: async function (beginData,endData,data) {

    return request({
      url: '/api/manageView/managerView/invest4Quadrant?beginDate=' + beginData + '&endDate=' + endData,
      method: 'post',
      data
    })
  },
  // 绩效情况投资四象限导出
  invest4QuadrantExport: async function (beginData,endData,data,name) {

    return request({
      url: '/api/manageView/managerView/invest4Quadrant?beginDate=' + beginData + '&endDate=' + endData + "&ex_tmp_name=" + name,
      method: 'post',
      data
    })
  },



  // 组合总览
  fundOverview: async function (beginData,endData,data) {

    return request({
      url: '/api/manageView/managerView/fundOverview?beginDate=' + beginData + '&endDate=' + endData,
      method: 'post',
      data
    })
  },
  // 组合总览导出
  fundOverviewExport: async function (beginData,endData,name,data) {

    return request({
      url: '/api/manageView/managerView/fundOverview?beginDate=' + beginData + '&endDate=' + endData+"&ex_tmp_name=" + name,
      method: 'post',
      data
    })
  },




}
