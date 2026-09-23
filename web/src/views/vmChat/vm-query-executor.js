import { logVmChatEvent, summarizeVmLogValue } from './vm-logger.js'
import { assertVmBusinessSuccess } from './vm-api-response.js'

function getByPath(payload, path) {
  if (!path) return payload
  return String(path)
    .split('.')
    .filter(Boolean)
    .reduce((current, key) => (current && current[key] !== undefined ? current[key] : undefined), payload)
}

function normalizeRows(payload) {
  if (Array.isArray(payload)) return payload
  if (payload && Array.isArray(payload.body)) return payload.body
  if (payload && Array.isArray(payload.data)) return payload.data
  if (payload && payload.data && Array.isArray(payload.data.rows)) return payload.data.rows
  if (payload && Array.isArray(payload.rows)) return payload.rows
  const commonPaths = ['data.list', 'data.items', 'body.list', 'body.items', 'result.list', 'result.items']
  for (let index = 0; index < commonPaths.length; index += 1) {
    const extracted = getByPath(payload, commonPaths[index])
    if (Array.isArray(extracted)) return extracted
  }
  return []
}

function stableStringify(value) {
  if (Array.isArray(value)) return '[' + value.map(stableStringify).join(',') + ']'
  if (value && typeof value === 'object') {
    return '{' + Object.keys(value).sort().map(key => JSON.stringify(key) + ':' + stableStringify(value[key])).join(',') + '}'
  }
  return JSON.stringify(value)
}

function buildRequestCacheKey(requestSpec) {
  return [
    requestSpec.mode,
    requestSpec.sqlCode,
    requestSpec.templateCode,
    stableStringify(requestSpec.params || {})
  ].join('|')
}

export function buildVmQueryRequestConfig(requestSpec) {
  const source = requestSpec && typeof requestSpec === 'object' ? requestSpec : {}
  return {
    requestId: String(source.requestId || ''),
    moduleKey: String(source.moduleKey || ''),
    submoduleId: source.submoduleId ? String(source.submoduleId) : '',
    mode: source.mode === 'template' ? 'template' : 'sql',
    sqlCode: source.sqlCode ? String(source.sqlCode) : '',
    templateCode: source.templateCode ? String(source.templateCode) : '',
    params: source.params && typeof source.params === 'object' ? Object.assign({}, source.params) : {}
  }
}

export async function executeVmQueryPlan(queryPlan, fetcher, options = {}) {
  if (typeof fetcher !== 'function') {
    throw new Error('vm query fetcher 未提供')
  }
  const traceId = options.traceId || ''
  const dataMode = options.dataMode === 'live'
    ? 'live'
    : options.dataMode === 'example'
      ? 'example'
      : fetcher.dataMode || 'live'
  const requests = Array.isArray(queryPlan && queryPlan.requests) ? queryPlan.requests : []
  const requestSpecs = requests.map((request, index) => {
    const requestSpec = buildVmQueryRequestConfig(request)
    if (!requestSpec.requestId) {
      throw new Error('queryPlan.requests[' + index + '] 缺少 requestId')
    }
    return requestSpec
  })
  const uniqueRequests = requestSpecs.reduce((accumulator, requestSpec) => {
    const cacheKey = buildRequestCacheKey(requestSpec)
    if (!accumulator.byKey[cacheKey]) {
      accumulator.byKey[cacheKey] = {
        cacheKey,
        requestSpec,
        aliases: []
      }
      accumulator.list.push(accumulator.byKey[cacheKey])
    }
    accumulator.byKey[cacheKey].aliases.push(requestSpec)
    return accumulator
  }, { byKey: {}, list: [] }).list
  const rowsByRequestId = {}
  const payloadByRequestId = {}
  const timings = {}
  let totalRows = 0
  logVmChatEvent('query-executor', 'plan.start', {
    requestCount: requests.length,
    uniqueRequestCount: uniqueRequests.length
  }, { traceId })

  const fetchedByKey = {}
  await Promise.all(uniqueRequests.map(async uniqueRequest => {
    const requestSpec = uniqueRequest.requestSpec
    const startedAt = Date.now()
    const payload = assertVmBusinessSuccess(
      await fetcher(Object.assign({}, requestSpec, { traceId, dataMode })),
      'VM 业务接口'
    )
    fetchedByKey[uniqueRequest.cacheKey] = {
      payload,
      startedAt,
      endedAt: Date.now()
    }
  }))

  requestSpecs.forEach(requestSpec => {
    const cacheKey = buildRequestCacheKey(requestSpec)
    const fetched = fetchedByKey[cacheKey]
    const payload = fetched && fetched.payload
    const rows = normalizeRows(payload)
    payloadByRequestId[requestSpec.requestId] = payload
    rowsByRequestId[requestSpec.requestId] = rows
    timings[requestSpec.requestId] = {
      startedAt: fetched ? fetched.startedAt : Date.now(),
      endedAt: fetched ? fetched.endedAt : Date.now(),
      durationMs: fetched ? fetched.endedAt - fetched.startedAt : 0,
      rowCount: rows.length,
      mockFallback: false,
      deduped: uniqueRequests.length < requestSpecs.length
    }
    totalRows += rows.length
    logVmChatEvent('query-executor', 'request.normalized', {
      requestId: requestSpec.requestId,
      moduleKey: requestSpec.moduleKey,
      rowCount: rows.length,
      mockFallback: false,
      durationMs: timings[requestSpec.requestId].durationMs,
      responseShape: summarizeVmLogValue(payload),
      rowsSample: rows.slice(0, 3)
    }, { traceId })
  })

  const result = {
    payloadByRequestId,
    rowsByRequestId,
    timings,
    mockFallbacks: {},
    dataMode,
    requestCount: requests.length,
    uniqueRequestCount: uniqueRequests.length,
    totalRows
  }
  logVmChatEvent('query-executor', 'plan.done', {
    requestCount: result.requestCount,
    uniqueRequestCount: result.uniqueRequestCount,
    dataMode: result.dataMode,
    totalRows: result.totalRows,
    timings: result.timings
  }, { traceId })
  return result
}
