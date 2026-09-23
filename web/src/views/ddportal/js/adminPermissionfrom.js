import request from '@/utils/request'
import store from '@/store'
const qs = require('qs');
export default {


  // 授权树
  userZtreesUrl: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/userZtrees' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  userZtreesUrlNew: async function () {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/userZtrees',
      method: 'get',
    })
  },

  //  列表
  userFundZtreesUrl: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/userFundZtrees' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  getProductsAll: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/fund/v1.0/getProductsAll' + '?' + qs.stringify(params),
      method: 'get',
    })
  },



  //  多用户添加
  userFundsUrl: async function (data) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/userFunds',
      method: 'put',
      data
    })
  },

  //  机构名称下拉框
  companysUrl: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/companys' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 字典查询
  edimsCommon: async function (dimType) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/common/edimsCommon/listEdims/' + dimType,
      method: 'get',
    })
  },


  // 授权管理-目前已拥有权限列表
  fundZtreesUrl: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/fundZtrees' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 批量删除
  deleteUserFundsUrl: async function (data) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/adminPermission/userFunds',
      method: 'delete',
      data
    })
  },








}
