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

  // 获取chart图数据
  countData: async function (params) {
    return request({
      url: '/api/etl/v1.0/countData'+'?'+qs.stringify(params),
      method: 'get',
    })
  },


  // 资讯 列表查询
  procZxList: async function (params) {
    return request({
      url: '/api/etl/v1.0/procZxList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

  /*
    资讯--执行/批量执行
    概述：重新执行所选资讯抽取过程
    接口：api/etl/v1.0/executeProcZx
    接口类型：post
    参数类型：html/text
    参数：清洗项procIds  （必填，可传递多个）
    文件(业务)日期 fileDate（必填） YYYY-MM-DD
  */
  executeProcZx: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/etl/v1.0/executeProcZx',
      method: 'POST',
      data: qs.stringify(params)
    })
  },

  // 清洗 列表查询
  procList: async function (params) {
    return request({
      url: '/api/etl/v1.0/procList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

  /* 
    概述：重新执行估值/TA所有清洗过程
    接口：api/etl/v1.0/executeProc
    接口类型：post
    参数：机构 agencyCode   （必填）
    文件(业务)日期 fileDate（必填） YYYY-MM-DD
  */
  executeProc: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/etl/v1.0/executeProc',
      method: 'POST',
      data: qs.stringify(params)
    })
  },
}
