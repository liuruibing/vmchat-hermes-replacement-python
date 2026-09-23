import request from '@/utils/request'
import qs from 'qs'

const ContentTypeFormData = { 'Content-type': 'application/x-www-form-urlencoded' }
const ContentTypeJSON = { 'Content-Type': 'application/json;charset=UTF-8' }

export default {
  // 查询模板列表
  selectTemplateList: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/list' + '?' + qs.stringify(params),
      method: 'get'
    })
  },

  //PDF 导出
  exportPDF: async function(params) {
    return request({
      header: ContentTypeJSON,
      url: '/api/workshop/v1.0/report/exportPdf',
      method: 'post',
      responseType: 'blob',
      data: params
    })
  },

  // 组件查询
  selectCompotentList: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/module/list' + '?' + qs.stringify(params),
      method: 'get'
    })
  },

  // 预览
  render: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/module/render',
      method: 'post',
      data: params
    })
  },

  // 模板-保存（报告内部组件编辑）
  saveReport: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/updateContent',
      method: 'post',
      data: params
    })
  },

  // 模板-新增(另存为)
  saveAsReport: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/insert',
      method: 'post',
      data: params
    })
  },

  // 模板-删除
  deleteTemplateReport: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/delete',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 模板-编辑（描述）
  editTemplateReport: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/update',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 模板关联组件配置-查询
  getTemplateComponent: async function(params) {
    return request({
      header: ContentTypeFormData,
      url: 'api/workshop/v1.0/report/moduleInfo' + '?' + qs.stringify(params),
      method: 'get'
    })
  }
}
