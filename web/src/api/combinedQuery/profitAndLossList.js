import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectprofitAndLossList: async function (params) {
    return post('/api/combinedQuery/fundQuery/listResults',qs.stringify(params), isForm)
  },

}
