import request from '@/utils/request'
const qs = require('qs')
import store from '@/store'

export const getEditDetail = (params) => {
  return request({
    baseURL: store.state.setting.baseApi, // api 的 base_url
    url: '/api/user/getEditDetail' + '?' + qs.stringify(params),
    method: 'get'
  })
}

export const getCompanys = () => {
  return request({
    baseURL: store.state.setting.baseApi, // api 的 base_url
    url: '/api/dept/companys',
    method: 'get'
  })
}

export const getEdims = (dimType) => {
  return request({
    url: '/api/common/edimsCommon/listEdims/' + dimType,
    method: 'get'
  })
}

export const updateDataSource = (params) => {
  return request({
    url: '/api/user/users',
    method: 'put',
    data: params
  })
}
