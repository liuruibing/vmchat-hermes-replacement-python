import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {

  // 个股持仓查询
  fun_selectStockPosition: async function (params) {
    return post('/api/stockPosition/selectStockPosition',qs.stringify(params), isForm)
  },

  //行业字典
  edimsCommon: async function (dimType) {
    return request({
      url: '/api/stockPosition/listEdims/' + dimType,
      method: 'get',
    })
  }
}
