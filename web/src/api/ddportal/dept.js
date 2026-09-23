import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      // baseURL: store.state.setting.baseApi, // api 的 base_url
      // url: '/api/dept/depts',
      url: '/api/company/v1.0/listDept',
      method: 'POST',
      data: params
    })
  },
  getDeptSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts',
      method: 'get'
    })
  },
  // 查询详情
  getDeptDetail: async function(deptId) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/getEditDetail?deptId=' + deptId,
      method: 'get'
    })
  },
  // 获取用户列表
  getUserList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/user/users' + '?' + qs.stringify(params),
      method: 'get'
    })
  },

  // 获取用户列表 -- 新增加
  getUserListNew: async function(params) {
    return request({
      url: '/api/company/v1.0/listUser',
      method: 'POST',
      data: params
    })
  },

  //修改部门
  updateDept: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts' + '?' + qs.stringify(params),
      method: 'put'
      //   headers:ContentTypeFormData,
      //   baseURL: store.state.setting.baseApi, // api 的 base_url
      //   url: '/api/dept/depts',
      //  // method: 'put',
      //  method:"put",
      //   data:params
    })
  },
  //新增部门
  addDept: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  //删除部门
  deleteDept: async function(id) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts?deptId=' + id,
      method: 'delete'
    })
  },
  //获取岗位
  getPosition: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positions' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取岗位类型
  getPositionType: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positionTypes',
      method: 'get'
    })
  },
  //根据用户id获取岗位信息
  getPositionByUser: async function(userId) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positionFind?userId=' + userId,
      method: 'get'
    })
  },
  //保存岗位维护
  positionInsert: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positionInsert' + '?' + qs.stringify(params),
      method: 'post'
    })
  },
  //岗位部门维护
  positionDept: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positionDept' + '?' + qs.stringify(params),
      method: 'put'
    })
  }
}
