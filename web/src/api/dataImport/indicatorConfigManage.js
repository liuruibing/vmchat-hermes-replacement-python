import request from '@/utils/request'
import store from '@/store'
const qs = require('qs')
export default {
  // 查询分页列表
  getIndParaThemeList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/page?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 新增
  postIndParaThemeAdd: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/add',
      method: 'post',
      data: params
    })
  },
  // 编辑
  postIndParaThemeEdit: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/update',
      method: 'post',
      data: params
    })
  },
  //删除列表
  postIndParaThemeDel: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/delete?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取vcCode
  getVcCode: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/id',
      method: 'get'
    })
  },
  //获取详情
  getDetail: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/info?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取关联的sql列表
  getSqlList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/sql/list?' + qs.stringify(params),
      method: 'get'
    })
  },
  //校验别名
  keyCheck: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/sql/keycheck?' + qs.stringify(params),
      method: 'post'
    })
  },
  //新增SQL数据
  addSqls: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/sql/adds',
      method: 'post',
      data: params
    })
  },
  //删除SQL数据
  deleteSql: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/sql/delete?' + qs.stringify(params),
      method: 'post'
    })
  },
  //获取模板数据
  getTemplateData: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/template/page?' + qs.stringify(params),
      method: 'get'
    })
  },
  //删除模板数据
  deleteTemplateData: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/target/delete?' + qs.stringify(params),
      method: 'get'
    })
  },
  //新增指标数据
  addIndicator: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/template/v1.0/target/adds',
      method: 'post',
      data: params
    })
  },
  //获取id
  getAddId: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/id',
      method: 'get'
    })
  }
}
