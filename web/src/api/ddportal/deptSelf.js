import request from '@/utils/request'
import store from '@/store'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
const qs = require('qs')
export default {
  // 获取 机构列表信息
  getInstitutionList: async function(params) {
    return request({
      url: '/api/company/v1.0/listPage' + '?' + 'pageSize=' + params.pageSize + '&pageNum=' + params.pageNum + '&limit=' + params.limit + '&offset=' + params.offset,
      method: 'POST',
      data: params
    })
  },

  // 更新 机构信息
  updateInstitution: async function(params) {
    return request({
      url: '/api/company/v1.0/update',
      method: 'POST',
      data: params
    })
  },

  // 新增 机构信息
  insertInstitution: async function(params) {
    return request({
      url: '/api/company/v1.0/insert',
      method: 'POST',
      data: params
    })
  },

  // 删除 机构信息
  deletetInstitution: async function(params) {
    return request({
      url: '/api/company/v1.0/delete',
      method: 'POST',
      data: params
    })
  },
}
