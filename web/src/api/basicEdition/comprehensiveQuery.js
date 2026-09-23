import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {

  // 综合持仓查询
  fun_selectComprehensivePosition: async function (params) {
    return post('/api/comprehensiveQuery/selectComprehensivePosition',qs.stringify(params), isForm)
  },
  // 个券反查
  fun_selectBondBack: async function (params) {
    return post('/api/comprehensiveQuery/selectBondBack',qs.stringify(params), isForm)
  },
  // 交易查询
  fun_selectBondChangeStream: async function (params) {
    return post('/api/comprehensiveQuery/selectBondChangeStream',qs.stringify(params), isForm)
  },
  // 股票持仓收益综合查询
  fun_stockPositionIincomeSelect: async function (params) {
    return post('/api/comprehensiveQuery/stockPositionIincome/selectListPage',qs.stringify(params), isForm)
  },
  // 非标持仓
  fun_selectNonstatndardListPage: async function (params) {
    return post('/api/comprehensiveQuery/selectNonstatndardListPage',qs.stringify(params), isForm)
  },
  // 债券持仓收益
  fun_selectBondPositionIncomeListPage: async function (params) {
    return post('/api/comprehensiveQuery/selectBondPositionIncomeListPage',qs.stringify(params), isForm)
  },
  // 估值表查询
  fun_selectValuationTableListPage: async function (params) {
    return post('/api/comprehensiveQuery/selectValuationTableListPage',qs.stringify(params), isForm)
  },
}
