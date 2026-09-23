import request from '@/utils/request'
const ContentTypeFormData = { 'Content-Type': 'application/json' }
export default {
  selectIndexInfos: async function(param) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/template/selectIndexInfos',
      data: param,
      method: 'post'
    })
  },

  // 广发-单产品分析-产品授权信息
  proAuthInfo: async function(param) {
    return request({
      url: '/api/singleProduct/proAuthInfo',
      data: param,
      method: 'post'
    })
  },
  // 其他产品-下拉
  fundList: async function(param) {
    return request({
      url: '/api/singleProduct/fundList',
      data: param,
      method: 'post'
    })
  },
  // 刷新流程状态
  refreshProcessStatus: async function(param) {
    return request({
      url: '/api/singleProduct/refreshProcessStatus',
      data: param,
      method: 'post'
    })
  },

  // 刷新流程状态
  authApply: async function(param) {
    return request({
      url: '/api/singleProduct/authApply',
      data: param,
      method: 'post'
    })
  },

}
