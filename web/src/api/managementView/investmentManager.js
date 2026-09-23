import request from '@/utils/request'
export default {


  // 获取投资经理ID  开始时间 组合代码 是固收还是权益  姓名
  findManagerOperno: async function (beginDate,fundCode,qyOrGs,userName) {

    return request({
      url: '/api/common/fundInfoCommon/findManagerOperno?beginDate=' + beginDate
      + '&fundCode=' + fundCode
      + '&qyOrGs=' + qyOrGs
      + '&userName=' + userName,
      method: 'post',
    })
  },

  // 投资经理列表
  managerList: async function (qyOrGsOrSum) {

    return request({
      url: '/api/manageView/investManager/managerList?qyOrGsOrSum=' + qyOrGsOrSum ,
      method: 'post',
    })
  },


  // 投资经理基本信息
  investManagerInfo: async function (beginDate,endDate,manage) {
    let data = manage;
    return request({
      url: '/api/manageView/investManager/investManagerInfo?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
      data
    })
  },
  // 投资经理基本信息
  fundAssetYield: async function (beginDate,endDate,data) {
    return request({
      url: '/api/manageView/investManager/fundAssetYield?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
      data
    })
  },
  // 管理资产变动走势
  managementScale: async function (beginDate,endDate,manage) {
    let data = manage;
    return request({
      url: '/api/manageView/investManager/managementScale?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
      data
    })
  },
  // 资产收益走势图
  assetsIncomeView: async function (beginDate,endDate,similarCode,targetCode,manage) {
    let data = manage;
    return request({
      url: '/api/manageView/investManager/assetsIncomeView?beginDate=' + beginDate + '&endDate=' + endDate + '&similarCode=' + similarCode + '&targetCode=' + targetCode,
      method: 'post',
      data
    })
  },
  // 收益贡献
  incomeContribution: async function (beginDate,endDate,manage) {
    let data = manage;
    return request({
      url: '/api/manageView/investManager/incomeContribution?beginDate=' + beginDate + '&endDate=' + endDate ,
      method: 'post',
      data
    })
  },

  // 绩效情况
  // 获取投资经理管理组合
  investManagerFundView: async function (account,beginDate,endDate) {
    return request({
      url: '/api/manageView/investManagerPerformance/investManagerFundView?account=' + account + '&beginDate=' + beginDate+ '&endDate=' + endDate,
      method: 'post',
    })
  },
  // 收益贡献
  investPerformanceView: async function (account,assetsChoiceType,beginDate,endDate,typeNumber,data) {
    return request({
      url: '/api/manageView/investManagerPerformance/investPerformanceView?account=' + account + '&assetsChoiceType='+ assetsChoiceType +'&beginDate=' + beginDate + '&endDate=' + endDate + '&typeNumber='+ typeNumber,
      method: 'post',
      data,
    })
  },
  // 收益贡献  导出
  investPerformanceViewExport: async function (account,assetsChoiceType,beginDate,endDate,typeNumber,data,name,id_name,pid_name,prefix_name) {
    return request({
      url: '/api/manageView/investManagerPerformance/investPerformanceView?account=' + account
      + '&assetsChoiceType='+ assetsChoiceType
      +'&beginDate=' + beginDate
      + '&endDate=' + endDate
      + '&typeNumber='+ typeNumber
      + "&ex_tmp_name=" + name
      + "&id_name=" + id_name
      + "&pid_name=" + pid_name
      + "&prefix_name=" + prefix_name,
      method: 'post',
      data,
    })
  },
  //权益投资经理管理总览 固收投资经理总览  0 组合总览 1 权益 2 固收

  managerFundListView: async function (beginDate,managerInvest,orderStr,data) {
  return request({
    url: '/api/manageView/investManager/managerFundListView?beginDate=' + beginDate + '&managerInvest=' + managerInvest + '&orderStr=' + orderStr,
    method: 'post',
    data,
  })
},
 //权益投资经理管理总览 固收投资经理总览  0 组合总览 1 权益 2 固收 导出
  managerFundListViewExport: async function (beginDate,managerInvest,orderStr,data,name) {
  return request({
    url: '/api/manageView/investManager/managerFundListView?beginDate=' + beginDate + '&managerInvest=' + managerInvest + '&orderStr=' + orderStr+ "&ex_tmp_name=" + name,
    method: 'post',
    data,
  })
},
  //权益投资经理管理总览 固收投资经理总览  投资类型详情

  managerAssetListViewDetail: async function (beginDate,managerInvest,orderStr,data) {
  return request({
    url: '/api/manageView/investManager/managerAssetListViewDetail?beginDate=' + beginDate + '&managerInvest=' + managerInvest + '&orderStr=' + orderStr,
    method: 'post',
    data,
  })
},
  //权益投资经理管理总览 固收投资经理总览  投资类型详情 导出

  managerAssetListViewDetailExport: async function (beginDate,managerInvest,orderStr,data,name) {
  return request({
    url: '/api/manageView/investManager/managerAssetListViewDetail?beginDate=' + beginDate + '&managerInvest=' + managerInvest + '&orderStr=' + orderStr + "&ex_tmp_name=" + name,
    method: 'post',
    data,
  })
},
  //权益投资经理管理总览 固收投资经理总览  组合详情

  managerFundListViewDetail: async function (beginDate,managerInvest,orderStr,data) {
  return request({
    url: '/api/manageView/investManager/managerFundListViewDetail?beginDate=' + beginDate + '&managerInvest=' + managerInvest  + '&orderStr=' + orderStr,
    method: 'post',
    data,
  })
},
  //权益投资经理管理总览 固收投资经理总览  组合详情 导出

  managerFundListViewDetailExport: async function (beginDate,managerInvest,orderStr,data,name) {
  return request({
    url: '/api/manageView/investManager/managerFundListViewDetail?beginDate=' + beginDate + '&managerInvest=' + managerInvest  + '&orderStr=' + orderStr + "&ex_tmp_name=" + name,
    method: 'post',
    data,
  })
},



}
