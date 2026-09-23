import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-type' : 'application/x-www-form-urlencoded'}

export default {
  // 模板-左侧指标树
  indexTree: async function (params) {
    return request({
      url: '/api/report/side/v1.0/indexTree',
      method: 'post',
      data: params
    })
  },

  // 指标预览div
  previewIndex: async function (params) {
    return request({
      url: '/api/report/side/v1.0/previewIndex',
      method: 'post',
      data: params,
      params: params,
    })
  },

  // 模板-新增保存
  addSave: async function (params) {
    return request({
      url: '/api/report/side/v1.0/addSave',
      method: 'post',
      data: params,
    })
  },

  // 模板-列表
  list: async function (params) {
    return request({
      url: '/api/report/side/v1.0/list',
      method: 'post',
      data: params,
    })
  },

  // 模板-删除
  delete: async function (params) {
    return request({
      url: '/api/report/side/v1.0/delete',
      method: 'post',
      data: params,
    })
  },

  // 模板-复制
  copy: async function (params) {
    return request({
      url: '/api/report/side/v1.0/copy',
      method: 'post',
      params: params
    })
  },

  // 模板-关联指标
  relatedIndex: async function (params) {
    return request({
      url: '/api/report/side/v1.0/relatedIndex',
      method: 'post',
      data: params,
    })
  },

  // 模板-编辑保存
  editSave: async function (params) {
    return request({
      url: '/api/report/side/v1.0/editSave',
      method: 'post',
      data: params,
    })
  },

  // 机构列表（分页）
  companyPageList: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/companyPageList',
      method: 'post',
      data: params,
    })
  },

  // 复制权限-机构弹框（不分页）
  companyDialogList: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/companyDialogList',
      method: 'post',
      data: params,
    })
  },

  // 复制权限-确定
  copyPermission: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/copyPermission',
      method: 'post',
      data: params,
    })
  },

  // 指标授权-指标弹框（不分页）
  indexDialogList: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/indexDialogList',
      method: 'post',
      data: params,
    })
  },

  // 指标授权-确定
  grantIndexByDept: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/grantIndexByDept',
      method: 'post',
      data: params,
    })
  },

  // 指标列表（分页）
  indexPageList: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/indexPageList',
      method: 'post',
      data: params,
    })
  },

  // 授权-机构弹框（不分页）
  deptDialogList: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/deptDialogList',
      method: 'post',
      data: params,
    })
  },

  // 授权-确定
  grantDeptByIndex: async function (params) {
    return request({
      url: '/api/indexGrant/v1.0/grantDeptByIndex',
      method: 'post',
      data: params,
    })
  },
}
