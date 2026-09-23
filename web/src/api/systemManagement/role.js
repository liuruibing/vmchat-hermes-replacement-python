import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};

export default {
  // 字典查询
  edimsCommon: async function (dimType) {
    return request({
      url: '/api/common/edimsCommon/listEdims/' + dimType,
      method: 'get',
    })
  },

  // 查询 
  getScherList: async function (params) {
    return request({
      url: '/api/role/roles' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 新增前代码唯一性
  checkCode: async function (params) {
    return request({
      url: '/api/role/checkCode' + '?' + qs.stringify(params),
      method: 'post',
    })
  },


  // 新增
  addRole: async function (params) {
    return request({
      headers:ContentTypeFormData,
      url: '/api/role/roles',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 修改
  updateRole: async function (params) {
    return request({
      url: '/api/role/roles' + '?' + qs.stringify(params),
      method: 'put',
    })
  },

  // 删除
  deleteRole: async function (params) {
    return request({
      url: '/api/role/roles' + '?' + qs.stringify(params),
      method: 'delete',
    })
  },

  // 菜单权限设置 列表
  roleActionSet: async function (params) {
    return request({
      url: '/api/role/roleActionSet' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 菜单权限添加
  roleActions: async function (data) {
    return request({
      url: '/api/role/roleActions',
      method: 'post',
      data,
    })
  },

  // 角色授权 列表
  roleUserSet: async function (params) {
    return request({
      url: '/api/role/roleUserSet' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 角色授权添加
  roleUsers: async function (data) {
    return request({
      url: '/api/role/roleUsers',
      method: 'post',
      data,
    })
  },







}
