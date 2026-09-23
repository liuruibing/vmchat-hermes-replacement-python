import request from '@/utils/request'
const qs = require('qs');
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const ContentTypeJson = {'Content-Type': 'application/json'};

export default {

  // 查询模板数据
  getTempList: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/list',
      method: 'post',
      data: params
    })
  },

  // 新增保存模板
  addSaveTemp: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/addSave',
      method: 'post',
      data: params
    })
  },

  // 编辑保存模板
  editSaveTemp: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/editSave',
      method: 'post',
      data: params
    })
  },

  // 删除模板
  deleteTemp: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/delete',
      method: 'post',
      data: params
    })
  },

  // 模板关联指标详情
  getRelatedIndex: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/relatedIndex',
      method: 'post',
      data: params
    })
  },

  // 查询左侧指标树数据
  getIndexTree: async function (params) {
    return request({
      url: '/api/dynamicReport/v1.0/indexTree',
      method: 'post',
      data: params
    })
  },

  // 模板复制
  copyTemp: async function (templateId) {
    return request({
      url: '/api/dynamicReport/v1.0/copy',
      method: 'post',
      headers: ContentTypeFormData,
      data: qs.stringify({ templateId })
    })
  },

  // 指标预览
  previewIndex: async function (indexCode) {
    return request({
      url: '/api/dynamicReport/v1.0/previewIndex',
      method: 'post',
      headers: ContentTypeFormData,
      data: qs.stringify({ indexCode })
    })
  },
  
  // 指标预览-jsp接口
  previewIndexJsp: async function (indexCode) {
    return request({
      url: '/rest/report/previewIndex.do',
      method: 'post',
      headers: ContentTypeFormData,
      data: qs.stringify({ indexCode })
    })
  },

}
