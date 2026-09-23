import request from '@/utils/request'
import store from '@/store'
const qs = require('qs')
export default {
  // 查询sql列表数据
  getIndParaThemeList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/page?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 新增SQL配置
  postIndParaThemeAdd: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/add',
      method: 'post',
      data: params
    })
  },
  // 编辑SQL配置
  postIndParaThemeEdit: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/update',
      method: 'post',
      data: params
    })
  },
  //删除SQL配置
  postIndParaThemeDel: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/delete?' + qs.stringify(params),
      method: 'get'
    })
  },
  //获取数据源下拉框数据
  getSource: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/source',
      method: 'get'
    })
  },
  //获取数据源下拉框数据
  getSPLSourceList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/Splsource',
      method: 'get'
    })
  },

  //获取SQL配置详情
  getDetail: async function(sqlCode) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/info?sqlCode=' + sqlCode,
      method: 'get'
    })
  },
  getRelationData: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/target/page?' + qs.stringify(params),
      method: 'get'
    })
  },
  //测试执行sql
  testSql: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/test?' + qs.stringify(params),
      // url: '/api/report/sql/v1.0/doTestSqlBySPL?' + qs.stringify(params),
      method: 'post'
    })
  },
  //测试执行sql
  testSqlBySPL: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      // url: '/api/report/sql/v1.0/test?' + qs.stringify(params),
      url: '/api/report/sql/v1.0/doTestSqlBySPL?' + qs.stringify(params),
      method: 'post'
    })
  },
  //删除指标
  indexDelete: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/target/delete?' + qs.stringify(params),
      method: 'get'
    })
  },
  //添加SQL
  addSqls: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/target/v1.0/sql/adds',
      method: 'post',
      data: params
    })
  },
  //获取id
  getAddId: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/report/sql/v1.0/id',
      method: 'get'
    })
  }
}
