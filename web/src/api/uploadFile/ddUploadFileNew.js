import request from '@/utils/request'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' };
const qs = require('qs');
export default {

  // 数据导入-模板下载 http://vip.datadriver.com.cn:9910/ann/rest/dataImport/uploadTemplate.do?fileId=7
  downloadTemplateUrl: async function (fileId, params) {
    return request({
      Headers: ContentTypeFormData,
      url: '/api/ann/v1.0/dataImport/download-template/' + fileId,
      // url: '/rest/dataImport/uploadTemplate.do?fileId=7',
      // url: '/api/ann/v1.0/dataImport/uploadTemplate.do?fileId=1',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 数据导入-文件导入
  uploadfile: async function (fileId, params) {
    return request({
      url: '/api/ann/v1.0/dataImport/upload-file/' + fileId,
      method: 'post',
      data: params
    })
  },
  // 导入记录列表-查询
  uploadLog: async function (fileId, params) {
    return request({
      url: '/api/ann/v1.0/dataImport/query-import-log/' + fileId + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 数据查看列表-查询
  queryData: async function (fileId, params) {
    return request({
      url: '/api/ann/v1.0/dataImport/query-data/' + fileId + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 导入日志
  logDetail: async function (fileId, params) {
    return request({
      url: '/api/ann/v1.0/dataImport/import-log-detail/' + fileId + '?' + qs.stringify(params),
      method: 'get',
    })
  },

}
