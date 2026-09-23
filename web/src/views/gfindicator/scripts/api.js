import service from '@/utils/request'
import qs from 'qs'

const FORM = { 'Content-Type': 'application/x-www-form-urlencoded' }

function qsForm(data) {
  return qs.stringify(data, { arrayFormat: 'brackets' })
}

/** BootstrapTable 分页结构解析 */
export function parseBootstrapPage(res) {
  const body = res && res.data !== undefined ? res.data : res
  if (!body) return { rows: [], total: 0 }
  if (body.rows !== undefined) {
    return { rows: body.rows || [], total: Number(body.total) || 0 }
  }
  if (body.data && body.data.rows !== undefined) {
    return { rows: body.data.rows || [], total: Number(body.data.total) || 0 }
  }
  return { rows: [], total: 0 }
}

/** 解析 Result / ResultDTO 等接口返回体 */
export function parseApiResult(res) {
  if (!res) return {}
  if (res.resultCode !== undefined || res.message !== undefined) {
    return res
  }
  if (res.data && (res.data.resultCode !== undefined || res.data.message !== undefined)) {
    return res.data
  }
  return res
}

export function isApiSuccess(body) {
  const code = body && body.resultCode
  return code === 1 || code === '1'
}

/** 指标类型 GFINDICATOR */
export function getIndicatorType() {
  return service.post('/api/indicator/getIndicatorType', qsForm({}), { headers: FORM })
}

/** 指标列表 */
export function fetchIndicatorList(params) {
  const url = `/api/indicator/doIndicatorList`
  return service.post(url, qsForm(params), { headers: FORM })
}

/** 重跑数据 */
export function executeIndicatorData(params) {
  return service.post('/api/indicator/executeData', qsForm(params), { headers: FORM })
}

/** 导出 CSV */
export function exportIndicatorList(params) {
  const url = `/api/indicator/exportIndicatorList`
  return service.post(url, qsForm(params), {
    headers: FORM,
    responseType: 'blob'
  })
}

/** 主日志列表 */
export function queryIndicatorMainLog(params) {
  return service.post('/api/indicatorLog/queryIndicatorMainLog', qsForm(params), { headers: FORM })
}

/** 明细日志 */
export function queryIndicatorDetailLog(params) {
  return service.post('/api/indicatorLog/queryIndicatorDetailLog', qsForm(params), { headers: FORM })
}
