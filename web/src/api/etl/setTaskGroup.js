import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 查询 任务组设置列表
  getTaskGroupList: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/getTaskGroupList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 添加 任务组
  addTaskGroup: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/addTaskGroup',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 修改
  updateTaskGroup: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/updateTaskGroup',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 单个删除
  deleteTaskGroup: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/deleteTaskGroup',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 手工执行
  implementTaskGroup: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/implementTaskGroup',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 获取任务组下任务列表
  getTaskByTaskGroupCode: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/getTaskByTaskGroupCode',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务组下任务启用禁用
  taskGroupOpen: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/taskGroupOpen',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务组设置批量删除
  deleteGrpMisRel: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/deleteGrpMisRel',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 获取任务或任务组列表
  doMisGrpList: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doMisGrpList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务组添加任务
  addMisRelGrpSet: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/addMisRelGrpSet',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 根据任务组编码查询任务组
  getTaskSetByCode: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/taskgroup/getTaskSetByCode',
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
