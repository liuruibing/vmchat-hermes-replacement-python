import request from '@/utils/request'
import qs from 'qs'
export default {
  //字典查询
  getTransferType: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  // 
  getTableList: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 查询参数设置
  findParam: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/findParam',
      method: 'get'
    })
  },
  // 新增、编辑参数设置
  addParam: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/editParam',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 删除参数设置
  deleteParam: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/deleteParam',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 提交日报
  submitReport: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/submitReport',
      method: 'post',
      data:params
    })
  },
  // 撤销提交
  unSubmit: async function (params) {
    return request({
      url: '/api/operationReport/v1.0/unSubmit',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 邮件发送
  sendMessage: async function (params) {
    return request({
      url: '/api/reportEmail/v1.0/sendMessage',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  


}