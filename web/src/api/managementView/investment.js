import request from '@/utils/request'
export default {

  // 资产类型下拉框
  selectAssetTypeList: async function () {
    return request({
      url: '/api/asset/detail/selectAssetTypeList?sort=1',
      method: 'post',
    })
  },

  //投委会有值的日期
  committeeNewDate: async function () {
    return request({
      url: '/api/manageView/nvestmentCommittee/maxDate',
      method: 'get',
    })
  },


  // 投委会会议明细
  nvestmentCommittee: async function (beginDate,endDate,keyword,pageNum,pageSize,type,vcConvokemethod,vcTracking,orderBy) {
    return request({
      url: '/api/manageView/nvestmentCommittee/list?beginDate=' + beginDate
                                                     + '&endDate=' + endDate
                                                     + '&keyword=' + keyword
                                                     + '&pageNum=' + pageNum
                                                     + '&pageSize=' + pageSize
                                                     + '&type=' + type
                                                     + '&vcConvokemethod=' + vcConvokemethod
                                                     + '&vcTracking=' + vcTracking
                                                     + '&orderBy=' + orderBy,
      method: 'get',
    })
  },
  // 投委会会议明细导出
  investmentCommitteeReport: async function (beginDate,endDate,keyword,pageNum,pageSize,type,vcConvokemethod,vcTracking,orderBy,name) {
    return request({
      url: '/api/manageView/nvestmentCommittee/list?beginDate=' + beginDate
      + '&endDate=' + endDate
      + '&keyword=' + keyword
      + '&pageNum=' + pageNum
      + '&pageSize=' + pageSize
      + '&type=' + type
      + '&vcConvokemethod=' + vcConvokemethod
      + '&vcTracking=' + vcTracking
      + '&orderBy=' + orderBy
      +'&ex_tmp_name=' + name,
      method: 'get',
    })
  },
  // 资产配置监控
  assetMonitor: async function (investTypes,beginDate,endDate,fundTypes,pageNum,pageSize,orderBy) {
    return request({
      // url: '/api/manageView/nvestmentCommittee/assetMonitor?assetCodes=' + assetCodes
      url: '/api/manageView/nvestmentCommittee/assetMonitor?investTypes=' + investTypes
                                                     + '&beginDate=' + beginDate
                                                     + '&endDate=' + endDate
                                                     + '&fundTypes=' + fundTypes
                                                     + '&pageNum=' + pageNum
                                                     + '&pageSize=' + pageSize
                                                     + '&orderBy=' + orderBy,
      method: 'get',
    })
  },
  // 资产配置监控 导出
  assetMonitorReport: async function (investTypes,beginDate,endDate,fundTypes,pageNum,pageSize,orderBy,name) {
    return request({
      // url: '/api/manageView/nvestmentCommittee/assetMonitor?assetCodes=' + assetCodes
      url: '/api/manageView/nvestmentCommittee/assetMonitor?investTypes=' + investTypes
                                                     + '&beginDate=' + beginDate
                                                     + '&endDate=' + endDate
                                                     + '&fundTypes=' + fundTypes
                                                     + '&pageNum=' + pageNum
                                                     + '&pageSize=' + pageSize
                                                     + '&orderBy=' + orderBy
                                                     +'&ex_tmp_name=' + name,
      method: 'get',
    })
  },
  // 净买入占比走势
  buyingRatio: async function (beginDate,endDate,fundTypes,investTypes) {
    return request({
      url: '/api/manageView/nvestmentCommittee/buyingRatio?beginDate=' + beginDate
                                                     + '&endDate=' + endDate
                                                     + '&fundTypes=' + fundTypes
                                                     + '&investTypes=' + investTypes,

      method: 'get',
    })
  },




}
