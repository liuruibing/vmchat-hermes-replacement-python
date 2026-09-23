import request from '@/utils/request'

export default {
  paramPage(params) {
    return request({
      url: '/api/indexapi/param/page',
      method: 'post',
      data: params
    })
  },

  paramInsert(params) {
    return request({
      url: '/api/indexapi/param/insert',
      method: 'post',
      data: params
    })
  },

  paramUpdate(params) {
    return request({
      url: '/api/indexapi/param/update',
      method: 'post',
      data: params
    })
  },

  paramDelete(params) {
    return request({
      url: '/api/indexapi/param/delete',
      method: 'post',
      data: params
    })
  }
}
