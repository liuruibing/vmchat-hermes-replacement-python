import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/users' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  getDeptSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts',
      method: 'get'
    })
  },

  getDeptPositionSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/posTree' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  //新增用户
  addDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/users',
      method: 'post',
      data: params
    })
  },
  //检查账户是否可用
  checkAccount: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/checkAccount' + '?' + qs.stringify(params),
      method: 'post'
    })
  },
  //检查员工编号是否可用
  checkUserNo: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/checkUserNo' + '?' + qs.stringify(params),
      method: 'post'
    })
  },
  //获取字典数据
  getEdims: async function(dimType) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/common/edimsCommon/listEdims/' + dimType,
      method: 'get'
    })
  },
  //获取机构数据
  getCompanys: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/companys',
      method: 'get'
    })
  },
  //获取角色数据
  getRoles: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/role/dialogRoles',
      method: 'get'
    })
  },

  getRolesnew: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/role/dialogRoles' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取用户详情信息
  getEditDetail: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/getEditDetail' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  //启用
  updateEnableStatus: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/userAble',
      method: 'post',
      data: params
    })
  },
  //禁用
  updateDisableStatus: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/userDisable',
      method: 'post',
      data: params
    })
  },
  //修改用户信息
  updateDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/users',
      method: 'put',
      data: params
    })
  },
  // //重置密码
  // resetPwd: async function (params) {
  //   return request({
  //     baseURL: store.state.setting.baseApi, // api 的 base_url
  //     url: '/api/user/resetPwd'+ '?' + qs.stringify(params),
  //     method: 'post',
  //   })
  // },

  //重置密码
  resetPwd: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/resetPwd',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 获取密码策略设置信息
  getPwdStrategy: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/system/passwordPolicy/getPwdStrategy',
      method: 'get'
    })
  },
  // 密码策略信息提交
  postPwdStrategy: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/system/passwordPolicy/updatePwdStrategy',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 密码验证
  checkPassword: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/system/passwordPolicy/checkPassword',
      method: 'post',
      data: qs.stringify(params)
    })
  }
}
