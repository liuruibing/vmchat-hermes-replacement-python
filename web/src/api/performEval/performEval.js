import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectperformEval: async function (params) {
    return post('/api/performEval/selectPerformEval',qs.stringify(params), isForm)
  },
  fun_selectperformEval2: async function (params) {
    return post('/api/performEval/performAnalysis',qs.stringify(params), isForm)
  },
  fun_selectdoYieldAnalysisGraphChart: async function (params) {
    return post('/api/performEval/doYieldAnalysisGraph',qs.stringify(params), isForm)
  },
  fun_selectdoPerformAnalysis: async function (params) {
    return post('/api/performEval/doPerformAnalysis',qs.stringify(params), isForm)
  },
}
