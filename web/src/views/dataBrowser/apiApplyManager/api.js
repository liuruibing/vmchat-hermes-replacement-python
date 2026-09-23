import request from '@/utils/request'

export default {
  reqPage(params) {
    return request({
      url: '/api/indexapi/req/pageAudit',
      method: 'post',
      data: params
    })
  },

  updateAudit(params) {
    return request({
      url: '/api/indexapi/req/updateAudit',
      method: 'post',
      data: params
    })
  }
}
