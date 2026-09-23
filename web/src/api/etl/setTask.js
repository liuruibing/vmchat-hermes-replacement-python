import request from '@/utils/request'
import store from '@/store'

const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 任务类型数据集合 任务设置
  getTaskTypeList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getTaskTypeList',
      method: 'POST'
    })
  },

  // 查询 任务设置
  getTaskList: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getTaskList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 数据源数据集合
  getDataSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getDataSourceList',
      method: 'POST'
    })
  },

  // 数据源SPL数据集合
  getSPLDataSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getSPLDataSourceList',
      method: 'POST'
    })
  },

  // 新增 任务
  addTaskSet: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/addTaskSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 修改 任务
  updateTaskSet: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/updateTaskSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 根据任务编码 删除
  deleteTaskset: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/deleteTaskset',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 根据任务编码 删除
  batchDeleteDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/batchDeleteDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务手工执行
  implementTask: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/implementTask',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 根据任务编码查询任务
  getTaskSetByCode: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getTaskSetByCode',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 手工执行组合列表
  getFundList: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskset/getFundList',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
