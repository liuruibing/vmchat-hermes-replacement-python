import request from '../../utils/request'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' };
const qs = require('qs');

export default {

  // 查询 /list
  getList: async function (params) {
    return request({
      url: '/api/ann/v1.0/zhfund/list' + '?' + qs.stringify(params),
      method: 'get',
      // data:qs.stringify(params)
    })
  },

  // 新增前校验 (校验fundCode唯一)
  check: async function (fundCode) {
    return request({
      url: `/api/ann/v1.0/zhfund/check-${fundCode}`,
      method: 'get',
    })
  },

  // 新增 
  addDataList: async function (params) {
    return request({
      url: '/api/ann/v1.0/zhfund',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // 编辑
  editInfo: async function (params) {
    return request({
      url: '/api/ann/v1.0/zhfund/edit-info',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // 删除 fundCode
  delete: async function (fundCode) {
    return request({
      url: `/api/ann/v1.0/zhfund/delete-${fundCode}`,
      method: 'post',
    })
  },

  // 详情 fundCode
  details: async function (fundCode) {
    return request({
      url: `/api/ann/v1.0/zhfund/${fundCode}` ,
      method: 'get',
    })
  },


}