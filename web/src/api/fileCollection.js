import request from '@/utils/request'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const qs = require('qs');
export default {

  getFileExtract: async function (params) {
    return request({
      url: '/api/etl/v1.0/fileExtract'+'?'+qs.stringify(params),
      method: 'get',
      
    })
  },

  getAgencyList: async function () {
    return request({
      url: '/api/etl/v1.0/agencyList',
      method: 'get',
    })
  },

  executeFile: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/etl/v1.0/execute',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  getOperationLog: async function (params) {
    return request({
      url: '/api/etl/v1.0/operationLog'+'?'+qs.stringify(params),
      method: 'get',
    })
  },




}
