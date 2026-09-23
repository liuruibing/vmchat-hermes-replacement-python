import request from '@/utils/request'
import qs from 'qs'
export default {
  // 合同定稿----------------------------------------
  // 合同定稿列表查询
  finalizedList: async function (params) {
    return request({
      url: '/api/finalizedContract/v1.0/finalizedList'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },
  // 合同定稿发起流程
  finalizedLaunch: async function (params) {
    return request({
      url: '/api/finalizedContract/v1.0/finalizedLaunch',
      method: 'post',
      data: params
    })
  },

  // 合同定稿退回到业务发起时的提交接口
  updateContractChange: async function (params) {
    return request({
      url: '/api/finalizedContract/v1.0/updateContractChange',
      method: 'post',
      data: params
    })
  },



  // 合同变更----------------------------------------
  // 合同变更列表查询
  changeList: async function (params) {
    return request({
      url: '/api/contractChange/v1.0/changeList'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },
  // 合同变更发起流程
  changeLaunch: async function (params) {
    return request({
      url: '/api/contractChange/v1.0/changeLaunch',
      method: 'post',
      data: params
    })
  },

  // 合同变更 退回到业务发起时的提交接口
  updateContractChange2: async function (params) {
    return request({
      url: '/api/contractChange/v1.0/updateContractChange',
      method: 'post',
      data: params
    })
  },



  // 查询合同变更可选择产品
  getFundCode: async function (params) {
    return request({
      url: '/api/contractChange/v1.0/getFundCode',
      method: 'get',
      // data: params
    })
  },
  
  


}