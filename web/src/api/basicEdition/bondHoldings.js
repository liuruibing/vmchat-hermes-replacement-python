import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  // 债券持仓查询
  fun_selectBondHoldings: async function (params) {
    return post('/api/bondHoldings/dobondHoldingsList',qs.stringify(params), isForm)
  },

  // 字典-债券类型
  fun_selectByfundTypeEdims: async function (dimType) {
    return request({
      url: '/api/bondHoldings/selectByfundType/' + dimType,
      method: 'get',
    })
  },
  // 字典-债券信用级别
  fun_selectBybondCrditEdims: async function (dimType) {
    return request({
      url: '/api/bondHoldings/selectBybondCrdit/' + dimType,
      method: 'get',
    })
  },
  // 字典-发债主体信用级别
  fun_selectBylevelIssuerEdims: async function (dimType) {
    return request({
      url: '/api/bondHoldings/selectBylevelIssuer/' + dimType,
      method: 'get',
    })
  },
  // 字典-行业
  fun_selectByindustryNameEdims: async function (dimType) {
    return request({
      url: '/api/bondHoldings/selectByindustryName/' + dimType,
      method: 'get',
    })
  },



}
