import request from '@/utils/request'
import qs from 'qs'
export default {
  // 产品信息变更------------------

  // 列表查询
  fundList: async function (params) {
    return request({
      url: '/api/InformationChange/v1.0/fundList'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },

  // 产品信息变更
  fundInfoChange: async function (params) {
    return request({
      url: '/api/InformationChange/v1.0/fundInfoChange',
      method: 'post',
      data: params
    })
  },
  updateInfoChange: async function (params) {
    return request({
      contentType: false,//这里不要落下
      dataType: 'json',
      url: '/api/InformationChange/v1.0/updateInfoChange',
      data: params,
      method: 'post',
    })
  },




  
  // 公司信息变更------------------

  // 列表查询
  orgList: async function (params) {
    return request({
      url: '/api/orgChange/v1.0/orgList'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },

  // 公司信息变更
  orgInfoChange: async function (params) {
    return request({
      url: '/api/orgChange/v1.0/orgInfoChange',
      method: 'post',
      data: params
    })
  },


}