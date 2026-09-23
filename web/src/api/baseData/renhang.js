import request from '@/utils/request'
import qs from 'qs'
// const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
  // 产品基本信息
  //查询 /api/rh/v1.0/list
  list: async function (params) {
    return request({
      url: '/api/rh/v1.0/list',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 新增
  add: async function (params) {
    return request({
      url: '/api/rh/v1.0/add'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 编辑
  edit: async function (params) {
    return request({
      url: '/api/rh/v1.0/edit'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 删除
  delete: async function (params) {
    return request({
      url: '/api/rh/v1.0/delete'+'?'+qs.stringify(params),
      method: 'get',
    })
  },


  // 产品终止信息
  //查询 /api/rh/v1.0/list
  duelist: async function (params) {
    return request({
      url: '/api/rh/v1.0/duelist',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 新增
  addDue: async function (params) {
    return request({
      url: '/api/rh/v1.0/addDue'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 编辑
  editDue: async function (params) {
    return request({
      url: '/api/rh/v1.0/editDue'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 删除
  deleteDue: async function (params) {
    return request({
      url: '/api/rh/v1.0/deleteDue'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  
  findPosition: async function (params) {
    return request({
      url: '/api/paramSetting/v1.0/findPosition'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

  
}