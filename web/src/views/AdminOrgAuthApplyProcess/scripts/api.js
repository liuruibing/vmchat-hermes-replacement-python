import request from '@/utils/request'

export default {
  pageList(params) {
    return request({
      url: '/api/sysMgrAuthApplyProcess/list',
      method: 'post',
      data: params
    })
  },
  approve(ids) {
    return request({
      url: '/api/sysMgrAuthApplyProcess/approve',
      method: 'post',
      data: { ids: ids }
    })
  },
  reject(ids) {
    return request({
      url: '/api/sysMgrAuthApplyProcess/reject',
      method: 'post',
      data: { ids: ids }
    })
  }
}
