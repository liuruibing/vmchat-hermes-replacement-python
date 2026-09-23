import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  //获取岗位类型
  getPositionType: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positionTypes',
      method: 'get'
    })
  },
  getDataSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positions' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  addDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positions',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  ckeckPositionType: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/ckeckPositionType' + '?' + qs.stringify(params),
      method: 'post'
    })
  },
  updateDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positions' + '?' + qs.stringify(params),
      method: 'put'
    })
  },
  getEditDetail: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/getEditDetail' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  deleteDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/position/positions' + '?' + qs.stringify(params),
      method: 'delete'
    })
  },

  getDeptDataSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/depts',
      method: 'get'
    })
  }
}
