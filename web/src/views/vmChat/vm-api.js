import request from '@/utils/request'
import store from '@/store'
import { logVmChatEvent, summarizeVmLogValue } from './vm-logger.js'
import { normalizeVmBenchmarkOptions, normalizeVmDataFrequencyOptions } from './vm-param-resolver.js'
import { assertVmBusinessSuccess, unwrapVmResponse } from './vm-api-response.js'
import { createVmDictionaryLoaderCore } from './vm-dictionary-loader.js'

const BENCHMARK_SQL_CODE = 'd43c924b-eebd-4d8f-97e5-ed46b609456d'

export async function fetchVmSqlData({ sqlCode, params }) {
  const response = await request({
    url: '/rest/report/getSqlDataBySqlCode.do',
    method: 'get',
    params: Object.assign({ sqlCode }, params || {})
  })
  return assertVmBusinessSuccess(unwrapVmResponse(response), 'VM SQL 接口')
}

// 示例数据链路不携带全局查询参数，参数只用于生成 DSL 和渲染上下文。
// 真实数据链路仍由 fetchVmSqlData 保留，便于后端接口就绪后切换。
export async function fetchVmExampleSqlData({ sqlCode }) {
  const response = await request({
    url: '/api/report/v1.0/data/test/sql/' + encodeURIComponent(sqlCode),
    method: 'post',
    params: { sqlCode },
    data: {}
  })
  const payload = unwrapVmResponse(response)
  if (payload && payload.data && typeof payload.data === 'object' && (
    Object.prototype.hasOwnProperty.call(payload.data, 'head') ||
    Object.prototype.hasOwnProperty.call(payload.data, 'body')
  )) {
    return payload.data
  }
  return assertVmBusinessSuccess(payload, 'VM 示例数据接口')
}

export async function fetchVmTemplateData({ templateCode, params }) {
  const response = await request({
    url: '/rest/report/interview.do',
    method: 'get',
    params: Object.assign({ templateCode }, params || {})
  })
  return assertVmBusinessSuccess(unwrapVmResponse(response), 'VM 模板接口')
}

function unwrapDictionaryPayload(response, displayName) {
  const payload = assertVmBusinessSuccess(unwrapVmResponse(response), displayName + '字典接口')
  if (!payload) throw new Error(displayName + '字典接口返回为空')
  return Array.isArray(payload.data) ? payload.data : []
}

export async function fetchVmBenchmarkOptions() {
  const response = await request({
    url: '/api/report/v1.0/data/sql/' + BENCHMARK_SQL_CODE,
    method: 'post',
    data: { indexCode: BENCHMARK_SQL_CODE }
  })
  return normalizeVmBenchmarkOptions(unwrapDictionaryPayload(response, '基准'))
}

export async function fetchVmDataFrequencyOptions() {
  const response = await request({
    url: '/api/common/edim/DATAFREQ',
    method: 'get'
  })
  return normalizeVmDataFrequencyOptions(unwrapDictionaryPayload(response, '频率'))
}

export function createVmDictionaryLoader() {
  return createVmDictionaryLoaderCore({
    fetchBenchmarkOptions: fetchVmBenchmarkOptions,
    fetchDataFrequencyOptions: fetchVmDataFrequencyOptions,
    publishBenchmarkOptions(options) {
      return store.dispatch('addDatumOption', options.map(item => ({ label: item.label, id: item.code })))
    }
  })
}

export function createVmRequestFetcher(options = {}) {
  const defaultDataMode = options.dataMode === 'live' ? 'live' : 'example'
  const fetchVmRequest = async function fetchVmRequest(requestSpec) {
    const dataMode = requestSpec && requestSpec.dataMode === 'live'
      ? 'live'
      : requestSpec && requestSpec.dataMode === 'example'
        ? 'example'
        : defaultDataMode
    const traceId = requestSpec && requestSpec.traceId || ''
    const startedAt = Date.now()
    logVmChatEvent('vm-api', 'request.start', {
      requestId: requestSpec && requestSpec.requestId,
      moduleKey: requestSpec && requestSpec.moduleKey,
      mode: requestSpec && requestSpec.mode,
      dataMode,
      sqlCode: requestSpec && requestSpec.sqlCode,
      templateCode: requestSpec && requestSpec.templateCode,
      params: requestSpec && requestSpec.params
    }, { traceId })
    try {
      const payload = requestSpec.mode === 'template'
        ? await fetchVmTemplateData({
          templateCode: requestSpec.templateCode,
          params: requestSpec.params
        })
        : dataMode === 'example'
          ? await fetchVmExampleSqlData({ sqlCode: requestSpec.sqlCode })
          : await fetchVmSqlData({
            sqlCode: requestSpec.sqlCode,
            params: requestSpec.params
          })
      logVmChatEvent('vm-api', 'request.success', {
        requestId: requestSpec && requestSpec.requestId,
        moduleKey: requestSpec && requestSpec.moduleKey,
        durationMs: Date.now() - startedAt,
        response: summarizeVmLogValue(payload)
      }, { traceId })
      return payload
    } catch (error) {
      logVmChatEvent('vm-api', 'request.error', {
        requestId: requestSpec && requestSpec.requestId,
        moduleKey: requestSpec && requestSpec.moduleKey,
        durationMs: Date.now() - startedAt,
        error
      }, { traceId, level: 'error' })
      throw error
    }
  }
  fetchVmRequest.dataMode = defaultDataMode
  return fetchVmRequest
}
