import request from '@/utils/request'
import store from '@/store'
const qs = require('qs')
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  // 任务日志列表
  getETLLogList: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/tasklog/getETLLogList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务明细日志列表
  getDetailLogList: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/tasklog/getDetailLogList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 单个删除 / 批量删除 /全部删除
  deleteEtlLog: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/tasklog/deleteEtlLog',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 取消调度
  mainLogCancle: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/tasklog/mainLogCancle',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
