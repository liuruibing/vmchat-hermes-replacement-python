import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }

const qs = require('qs')
export default {
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/getDataSourceList',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 添加 数据源设置
  addDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/addDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 修改 数据源设置
  updateDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/updateDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 删除单个  数据源设置
  deleteDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/deleteDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
  // 批量删除  数据源设置
  batchDeleteDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/batchDeleteDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 测试连接
  testDataSource: async function(params) {
    return request({
      headers: ContentTypeFormData,

      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/etl/datasource/testDataSource',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
