import request from '@/utils/request'

export default {
  // 查询
  reqPage(params) {
    return request({
      url: '/api/indexapi/req/page',
      method: 'post',
      data: params
    })
  },

  // 用户下拉数据
  listUser() {
    return request({
      url: '/api/indexapi/req/listUser',
      method: 'post',
      data: {}
    })
  },

  // 发起申请
  reqInsert(params) {
    return request({
      url: '/api/indexapi/req/insert',
      method: 'post',
      data: params
    })
  },

  // 批量发起申请
  reqInsertBatch(params) {
    return request({
      url: '/api/indexapi/req/insertBatch',
      method: 'post',
      data: params
    })
  },

  // 更新
  reqUpdate(params) {
    return request({
      url: '/api/indexapi/req/update',
      method: 'post',
      data: params
    })
  },

  // 删除
  reqDelete(params) {
    return request({
      url: '/api/indexapi/req/delete',
      method: 'post',
      data: params
    })
  },

  // token更换 参数vcRecordId
  freshToken(params) {
    return request({
      url: '/api/indexapi/req/freshToken',
      method: 'post',
      data: params
    })
  },

  // token失效 参数vcRecordId
  cancelToken(params) {
    return request({
      url: '/api/indexapi/req/cancelToken',
      method: 'post',
      data: params
    })
  },

}
