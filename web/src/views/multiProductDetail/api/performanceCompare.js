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
}
