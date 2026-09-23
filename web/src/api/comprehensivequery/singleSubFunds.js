import { post } from '@/utils/request'
import service from '@/utils/request'
import qs from 'qs'

const isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

function qsForm(params) {
  return qs.stringify(params, { arrayFormat: 'brackets' })
}

export default {
  /** 根据多产品代码获取区间内持仓子基金列表 */
  getAllSubFundsListByMultiFundCodes(params) {
    return post('/api/singleSubFunds/getAllSubFundsListByMultiFundCodes', qsForm(params), isForm)
  },
  /** 单子基金查询-表格 */
  queryList(params) {
    return post('/api/singleSubFunds/doSingleSubFunds', qsForm(params), isForm)
  },
  /** 单子基金查询-图表 */
  queryChart(params) {
    return post('/api/singleSubFunds/doSingleSubFundsChart', qsForm(params), isForm)
  },
  /** 单子基金查询-导出 */
  exportList(params) {
    return service({
      url: '/api/singleSubFunds/exportSingleSubFunds',
      method: 'post',
      data: qsForm(params),
      responseType: 'blob',
      headers: isForm
    })
  }
}