import { post } from '@/utils/request'
import qs from 'qs'

const isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  /** 子基金持仓查询列表 */
  queryList(params) {
    return post('/api/subfundPosition/dosubfundPositionList', qs.stringify(params), isForm)
  }
}
