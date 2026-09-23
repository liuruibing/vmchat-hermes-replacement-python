import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }

const qs = require('qs')
export default {
  // 查询
  dispatchLists: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/dispatch/dispatchLists',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 取消调度
  cancelDispatch: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/dispatch/cancelDispatch',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 查看调度设置
  selectDispatchSet: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/dispatch/selectDispatchSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
