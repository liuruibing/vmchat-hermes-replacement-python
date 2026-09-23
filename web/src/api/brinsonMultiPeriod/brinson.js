import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectbrinson: async function (params) {
    return post('/api/brinson/brinsonList',qs.stringify(params), isForm)
  },
  fun_selectbrinsonChar: async function (params) {
    return post('/api/brinson/brinsonCharts',qs.stringify(params), isForm)
  },
}
