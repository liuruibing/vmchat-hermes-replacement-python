import request from '@/utils/request'
import store from '@/store'
const qs = require('qs')
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  // 查询所有 参数设置
  getParamSetList: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/getParamSetList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 添加 参数设置
  addParamSet: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/addParamSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 修改 参数设置
  updateParamSet: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/updateParamSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 删除 参数设置
  deleteParamSet: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/deleteParamSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 批量删除 参数设置
  batchDeleteParamSet: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/batchDeleteParamSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 判断代码是否重复
  selectParamSetByCode: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/paramset/selectParamSetByCode',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
