import request from '@/utils/request'
import qs from 'qs'
export default {
  // 产品台账管理
  // 列表查询
  list: async function (params) {
    return request({
      url: '/api/productLedger/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },
  // 新增、编辑
  update: async function (params) {
    return request({
      url: '/api/productLedger/v1.0/update',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  


}