import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }

const qs = require('qs')
export default {
  // 查询
  getScherList: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/getScherList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 新增调度设置
  doScherAdd: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doScherAdd',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 编辑
  doScherEdit: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doScherEdit',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  //  单个删除
  doScherDelete: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doScherDelete',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 批量删除
  batchScherDelete: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/batchScherDelete',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 手工执行调度
  implementScher: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/implementScher',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  //  调度设置
  doScherSet: async function(params) {
    return request({
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doScherSet',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 根据调度编码获取调度下的任务列表
  doScherTaskRel: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doScherTaskRel',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 删除调度设置下的任务或任务组
  doTaskRelDelete: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doTaskRelDelete',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 任务或任务组列表
  doMisGrpList: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doMisGrpList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 调度设置下添加任务或任务组
  doTaskRelAdd: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/doTaskRelAdd',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 根据调度编码查询调度设置
  getScherByCode: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/scher/getScherByCode',
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
