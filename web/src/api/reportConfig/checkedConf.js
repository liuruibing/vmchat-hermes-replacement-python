import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
// /api/reportVerify/v1.0/
export default {
  //查询 
  list: async function (params) {
    return request({
      url: '/api/reportVerify/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  //报表配置信息查询 
  reportList: async function (params) {
    return request({
      url: '/api/reportVerify/v1.0/reportList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  //勾稽校验配置新增 
  insert: async function (params) {
    return request({
      url: '/api/reportVerify/v1.0/insert',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  //勾稽校验配置编辑
  update: async function (params) {
    return request({
      url: '/api/reportVerify/v1.0/update',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  //勾稽校验配置删除
  delete: async function (params) {
    return request({
      url: '/api/reportVerify/v1.0/delete',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  
}