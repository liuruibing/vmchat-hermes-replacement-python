import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 获取列表数据
  getIndParaThemeList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/page?',
      method: 'post',
      data: params
    })
  },
  // 新增
  postIndParaThemeAdd: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/add',
      method: 'post',
      data: params
    })
  },
  // 编辑
  postIndParaThemeEdit: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/update',
      method: 'post',
      data: params
    })
  },
  //删除
  postIndParaThemeDel: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/delete?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取字典数据
  getEdims: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/edim?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取ID
  getId: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/id',
      method: 'get'
    })
  },
  //获取详情
  getDetail: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/info?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取详情Table
  getDetailTable: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/target/page?' + qs.stringify(params),
      method: 'get'
    })
  },

  //获取id
  getAddId: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/id',
      method: 'get'
    })
  },
  deleteTemplateData: async function(params) {
    return request({
      headers: ContentTypeFormData,
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/target/delete',
      method: 'POST',
      data: qs.stringify(params)
    })
  }
}
