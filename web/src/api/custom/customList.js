import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};

export default{
  // 待办列表
  getTaskList: async function (params) {
    return request({
      url: '/api/customTransfer/v1.0/customTaskList' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 已办列表
  getDealtList: async function (params) {
    return request({
      url: '/api/customTransfer/v1.0/customDealtList' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 发起
  StartCustom: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/customTransfer/v1.0/startCustom',
      method: 'post',
      data: params,
    })
  },
  // 暂存
  TsCustom: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/customTransfer/v1.0/add',
      method: 'post',
      data: params,
    })
  },
  // 根据产品代码查询账户
  getAccounts: async function (params) {
    return request({
      url: '/api/trade/acco/list?'+qs.stringify(params),
      method: 'post',
    })
  },
}