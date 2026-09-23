import request from '@/utils/request'
import qs from 'qs'
export default {
  // 列表查询
  list: async function (params) {
    return request({
      url: '/api/establishAndFiling/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },
  // 提交备案材料
  submitForRecord: async function (params) {
    return request({
      url: '/api/establishAndFiling/v1.0/submitForRecord',
      method: 'post',
      data: params
    })
  },

  // 提交备案材料(退回后重新发起)
  updateFilingChange: async function (params) {
    return request({
      url: '/api/establishAndFiling/v1.0/updateFilingChange',
      method: 'post',
      data: params
    })
  },
  
  


}