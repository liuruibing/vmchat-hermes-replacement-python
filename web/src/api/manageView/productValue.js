import request from '@/utils/request'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
import qs from 'qs'
export default {
  // 字典查询
  getTransferType: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get'
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      url: '/api/managerScale/v1.0/listPageNetProduct' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 查询基金经理信息
  getFundManagerInfo: async function() {
    return request.get('/api/foundManager/v1.0/getManagerAll')
  },
  // 查询基金经理信息
  getDeptInfoSel: async function() {
    return request.post('/api/deptInfo/v1.0/deptInfoSel')
  },

  getListByInstTypeDim: async function(params) {
    return request({
      headers:ContentTypeFormData,
      url: '/api/deptInfo/v1.0/getListByInstTypeDim',
      method: 'POST',
      data: qs.stringify(params)
    })
    
  },

  getSelects: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get'
    })
  },
  getProductsAll: async function() {
    return request({
      url: '/api/fund/v1.0/getProductsAll',
      method: 'get'
    })
  },
  // 查询所有 数据源设置
  getDataOverView: async function(params) {
    return request({
      // url: '/api/productdisc/v1.0/listPageProductDisc' + '?' + qs.stringify(params),
      url: '/api/generalquery/v1.0/getQueryResult.do' + '?' 
      + qs.stringify(params),
      method: 'get'
    })
  },
  getechartThreeJz: async function() {
    return request({
      // url: '/api/productdisc/v1.0/listPageProductDisc' + '?' + qs.stringify(params),
      url: '/api/outline/v1.0/graphNetAssets',
      method: 'get'
    })
  },
  getechartThreeGlAndYj: async function() {
    return request({
      // url: '/api/productdisc/v1.0/listPageProductDisc' + '?' + qs.stringify(params),
      url: '/api/outline/v1.0/graphManageCostAndMeritPay',
      method: 'get'
    })
  }

}
