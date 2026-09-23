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
  //提交
  submit: async function (params) {
    return request({
      url: '/api/kpiReport/v1.0/submit',
      method: 'post',
      data:params
    })
  },
  //取消提交
  unSubmit: async function (params) {
    return request({
      url: '/api/kpiReport/v1.0/unSubmit',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 查询
  getList: async function (params) {
    return request({
      url: '/api/kpiReport/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
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