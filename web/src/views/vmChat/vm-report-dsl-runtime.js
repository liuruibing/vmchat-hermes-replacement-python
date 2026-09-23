import { executeVmQueryPlan } from './vm-query-executor.js'
import { validateVmReportDsl } from './vm-report-dsl-validator.js'

const DEFAULT_EMPTY_DISPLAY = '-'
const TRANSFORM_TIMEOUT_MS = 5000

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

function toTitle(value, fallback) {
  const text = String(value || '').trim()
  return text || fallback
}

function deriveModuleKey(dsl) {
  const requests = Array.isArray(dsl && dsl.requests) ? dsl.requests : []
  const moduleIds = requests.map(item => String(item && item.moduleId || '').trim()).filter(Boolean)
  return Array.from(new Set(moduleIds)).join('+')
}

function deriveQueryContext(params) {
  const source = params && typeof params === 'object' ? params : {}
  return {
    fundCode: source.fundCode || '',
    productCode: source.fundCode || '',
    beginDate: source.beginDate || '',
    endDate: source.endDate || '',
    dateRange: source.beginDate && source.endDate ? [source.beginDate, source.endDate] : [],
    benchmarkA: source.benchmarkA || '',
    benchmarkB: source.benchmarkB || '',
    benchmarks: source.benchmarks || '',
    dataFreq: source.dataFreq || ''
  }
}

function formatValue(value, format) {
  if (value === null || value === undefined || value === '') {
    return format && format.nullValue !== undefined ? format.nullValue : DEFAULT_EMPTY_DISPLAY
  }
  if (!format || !format.type || format.type === 'raw') return value

  const prefix = format.prefix || ''
  const suffix = format.suffix || ''

  if (format.type === 'text' || format.type === 'date') {
    return prefix + String(value) + suffix
  }

  const num = Number(value)
  if (isNaN(num)) return value

  if (format.type === 'number') {
    return prefix + String(value) + suffix
  }
  if (format.type === 'decimal') {
    const digits = format.digits !== undefined ? format.digits : 2
    return prefix + num.toFixed(digits) + suffix
  }
  if (format.type === 'percentage') {
    const digits = format.digits !== undefined ? format.digits : 2
    return prefix + num.toFixed(digits) + suffix
  }
  return String(value)
}

function buildTableColumns(view) {
  return (Array.isArray(view && view.columns) ? view.columns : []).map(column => ({
    field: column.field,
    title: column.label || column.field,
    label: column.label || column.field,
    unit: column.unit,
    format: column.format,
    align: column.align || 'left',
    formatter: column.format ? ({ cellValue }) => formatValue(cellValue, column.format) : undefined
  }))
}

function buildChartOption(view, title) {
  const series = Array.isArray(view && view.series) ? view.series : []
  const isPie = series.length > 0 && series.every(item => item && item.type === 'pie')

  const formatBySeriesName = {}
  const yDimBySeriesName = {}
  series.forEach(item => {
    if (item && item.format) {
      formatBySeriesName[item.name] = item.format
    }
    if (item && item.encode && item.encode.y) {
      yDimBySeriesName[item.name] = item.encode.y
    }
  })

  const option = {
    title: { text: title, show: false },
    tooltip: {
      trigger: isPie ? 'item' : 'axis',
      ...(!isPie ? {
        formatter(params) {
          const items = Array.isArray(params) ? params : [params]
          const dimNames = items[0] && items[0].dimensionNames || []
          const dateLabel = dimNames[0] && items[0].value ? (items[0].value[dimNames[0]] || '') : ''
          const lines = [String(dateLabel)]
          items.forEach(p => {
            const yDim = yDimBySeriesName[p.seriesName] || p.seriesName
            const fmt = formatBySeriesName[p.seriesName]
            const rawValue = p.value && p.value[yDim]
            const displayValue = formatValue(rawValue, fmt)
            lines.push(p.marker + ' ' + p.seriesName + '：' + displayValue)
          })
          return lines.join('<br/>')
        }
      } : undefined)
    },
    legend: clone(view.legend || { show: true, data: [] }),
    dataset: {
      dimensions: Array.isArray(view && view.dataset && view.dataset.dimensions) ? clone(view.dataset.dimensions) : [],
      source: []
    },
    series: series.map(item => {
      const next = {
        name: item.name,
        type: item.type,
        encode: clone(item.encode)
      }
      if (item.stack) next.stack = item.stack
      if (item.format) next.format = clone(item.format)
      if (item.type !== 'pie') next.yAxisIndex = Number(item.yAxisIndex || 0)
      return next
    })
  }
  if (!isPie) {
    const yAxisCount = Math.max(1, series.reduce((max, item) => Math.max(max, Number(item && item.yAxisIndex || 0) + 1), 0))
    const xField = series[0] && series[0].encode ? series[0].encode.x : 'x'
    option.grid = clone(view.grid || { left: 48, right: yAxisCount > 1 ? 48 : 24, top: 48, bottom: 36 })
    option.xAxis = clone(view.xAxis || { type: 'category', name: xField })
    option.yAxis = clone(view.yAxis || Array.from({ length: yAxisCount }).map((_, index) => ({ type: 'value', position: index === 0 ? 'left' : 'right' })))
  }
  return option
}

function buildRenderSpecFromDsl(dsl, title) {
  if (dsl.view.type === 'table') {
    return {
      renderer: 'table',
      columns: buildTableColumns(dsl.view),
      rows: []
    }
  }
  return {
    renderer: 'echarts',
    option: buildChartOption(dsl.view, title)
  }
}

function createErrorState(message) {
  return {
    status: 'error',
    errorMessage: message,
    hydratedAt: new Date().toISOString()
  }
}

function buildRequestPlan(dsl, resolvedParams) {
  return {
    requests: dsl.requests.map(request => ({
      requestId: request.id,
      moduleKey: request.moduleId,
      submoduleId: request.submoduleId || '',
      mode: 'sql',
      sqlCode: request.sqlCode,
      params: Object.assign({}, resolvedParams || {})
    }))
  }
}

function buildRuntimeDiagnostics(queryResult, lastError, resolvedParams) {
  const timings = queryResult && queryResult.timings || {}
  const rowCounts = Object.keys(timings).reduce((accumulator, requestId) => {
    accumulator[requestId] = timings[requestId].rowCount
    return accumulator
  }, {})
  return {
    requestCount: queryResult && queryResult.requestCount || 0,
    uniqueRequestCount: queryResult && queryResult.uniqueRequestCount || 0,
    totalRows: queryResult && queryResult.totalRows || 0,
    dataMode: queryResult && queryResult.dataMode || 'live',
    rowCounts,
    timings,
    displayDiagnostics: [],
    lastError: lastError || '',
    resolvedParams: resolvedParams ? clone(resolvedParams) : null
  }
}

function detectForbiddenTokens(transformSource) {
  const tokens = ['window', 'document', 'fetch', 'XMLHttpRequest', 'localStorage', 'sessionStorage', 'globalThis', 'self', 'Function', 'eval']
  return tokens.find(token => new RegExp('\\b' + token.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\b').test(transformSource))
}

function createTransformSandboxDocument(channel) {
  const workerSource = [
    "'use strict';",
    'function deepFreeze(value) {',
    "  if (!value || typeof value !== 'object') return value;",
    '  Object.freeze(value);',
    '  Object.keys(value).forEach(function (key) {',
    "    if (value[key] && typeof value[key] === 'object' && !Object.isFrozen(value[key])) deepFreeze(value[key]);",
    '  });',
    '  return value;',
    '}',
    'self.onmessage = function (event) {',
    '  var payload = event.data || {};',
    '  var responsePort = event.ports && event.ports[0];',
    "  if (!responsePort) throw new Error('transform.function 安全通道缺失');",
    '  var sendResponse = MessagePort.prototype.postMessage.bind(responsePort);',
    '  var closeResponse = MessagePort.prototype.close.bind(responsePort);',
    '  var isArray = Array.isArray;',
    '  try {',
    "    var transform = Function('\"use strict\"; return (' + payload.source + ');')();",
    "    if (typeof transform !== 'function') throw new Error('transform.function 必须导出 function transform(responses)');",
    '    var result = transform(deepFreeze(payload.responses || {}));',
    "    if (!isArray(result)) throw new Error('transform.function 必须返回数组');",
    "    sendResponse({ kind: 'result', result: result });",
    '  } catch (error) {',
    "    sendResponse({ kind: 'error', error: error && error.message ? error.message : String(error || '未知错误') });",
    '  } finally {',
    '    closeResponse();',
    '  }',
    '};'
  ].join('\n')
  const escapedWorkerSource = JSON.stringify(workerSource).replace(/</g, '\\u003c')
  const escapedChannel = JSON.stringify(channel)
  return [
    '<!doctype html><html><head>',
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\' \'unsafe-eval\' blob:; worker-src blob:; connect-src \'none\'; img-src \'none\'; media-src \'none\'; font-src \'none\'; style-src \'none\'; frame-src \'none\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'">',
    '</head><body><script>',
    "'use strict';",
    'var channel = ' + escapedChannel + ';',
    'var workerUrl = URL.createObjectURL(new Blob([' + escapedWorkerSource + "], { type: 'text/javascript' }));",
    'var worker = new Worker(workerUrl);',
    'URL.revokeObjectURL(workerUrl);',
    'var started = false;',
    'worker.onerror = function () {',
    "  parent.postMessage({ channel: channel, kind: 'error', error: 'transform.function 安全沙箱执行失败' }, '*');",
    '};',
    'window.addEventListener(\'message\', function (event) {',
    '  if (started || event.source !== parent || !event.data || event.data.channel !== channel) return;',
    '  started = true;',
    '  var responseChannel = new MessageChannel();',
    '  responseChannel.port1.onmessage = function (responseEvent) {',
    '    var data = responseEvent.data || {};',
    "    if (data.kind === 'result' && Array.isArray(data.result)) {",
    "      parent.postMessage({ channel: channel, kind: 'result', result: data.result }, '*');",
    "    } else if (data.kind === 'error' && typeof data.error === 'string') {",
    "      parent.postMessage({ channel: channel, kind: 'error', error: data.error }, '*');",
    '    } else {',
    "      parent.postMessage({ channel: channel, kind: 'error', error: 'transform.function 安全沙箱返回了非法结构' }, '*');",
    '    }',
    '    responseChannel.port1.close();',
    '    worker.terminate();',
    '  };',
    '  worker.postMessage({ source: event.data.source, responses: event.data.responses }, [responseChannel.port2]);',
    '});',
    "parent.postMessage({ channel: channel, ready: true }, '*');",
    '<\/script></body></html>'
  ].join('')
}

function executeTransformInSandbox(transformSource, responses) {
  if (typeof window === 'undefined' || typeof document === 'undefined' || !document.body) {
    return Promise.reject(new Error('transform.function 安全沙箱仅支持浏览器环境'))
  }
  return new Promise((resolve, reject) => {
    const channel = 'vm-transform-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2)
    const iframe = document.createElement('iframe')
    iframe.setAttribute('sandbox', 'allow-scripts')
    iframe.setAttribute('aria-hidden', 'true')
    iframe.style.display = 'none'
    let settled = false
    const cleanup = () => {
      window.removeEventListener('message', onMessage)
      if (iframe.parentNode) iframe.parentNode.removeChild(iframe)
    }
    const finish = (callback, value) => {
      if (settled) return
      settled = true
      clearTimeout(timer)
      cleanup()
      callback(value)
    }
    const onMessage = event => {
      if (event.source !== iframe.contentWindow || !event.data || event.data.channel !== channel) return
      if (event.data.ready) {
        iframe.contentWindow.postMessage({ channel, source: transformSource, responses: clone(responses || {}) }, '*')
        return
      }
      if (event.data.kind === 'result' && Array.isArray(event.data.result)) {
        finish(resolve, event.data.result)
      } else if (event.data.kind === 'error' && typeof event.data.error === 'string') {
        finish(reject, new Error(event.data.error || 'transform.function 安全沙箱执行失败'))
      }
    }
    const timer = setTimeout(() => {
      finish(reject, new Error('transform.function 安全沙箱执行超时'))
    }, TRANSFORM_TIMEOUT_MS)
    window.addEventListener('message', onMessage)
    iframe.srcdoc = createTransformSandboxDocument(channel)
    document.body.appendChild(iframe)
  })
}

export async function executeVmReportTransformFunction(transformSource, responses, options = {}) {
  const forbiddenToken = detectForbiddenTokens(transformSource)
  if (forbiddenToken) {
    throw new Error('transform.function 使用了禁用标识：' + forbiddenToken)
  }
  try {
    const executor = typeof options.executor === 'function' ? options.executor : executeTransformInSandbox
    const result = await executor(transformSource, clone(responses || {}))
    if (!Array.isArray(result)) {
      throw new Error('transform.function 必须返回数组')
    }
    return clone(result)
  } catch (error) {
    throw new Error('transform.function 执行失败：' + (error && error.message ? error.message : String(error || '未知错误')))
  }
}

export function createVmDslReportBlock(input, options = {}) {
  const source = input && typeof input === 'object' ? input : {}
  const dsl = validateVmReportDsl(clone(source.dsl || {}), options.validationContext || {}, {
    enforceUpdateContext: options.enforceUpdateContext === true
  })
  const moduleKey = deriveModuleKey(dsl)
  const title = toTitle(dsl.view && dsl.view.title || source.title, moduleKey || 'vmChat 视图')
  const type = dsl.view.type
  return {
    blockId: String(source.blockId || dsl.id || 'vm-block-' + Date.now().toString(36)),
    title,
    type,
    viewType: type,
    moduleKey,
    dsl,
    queryContext: deriveQueryContext(dsl.params),
    renderSpec: buildRenderSpecFromDsl(dsl, title),
    renderState: source.renderState && typeof source.renderState === 'object'
      ? clone(source.renderState)
      : { status: 'idle' },
    sourceData: {
      provider: 'vm-report-dsl',
      runtime: null
    },
    requestDiagnostics: [],
    transformDiagnostics: [],
    renderSnapshot: null,
    createdAt: source.createdAt || new Date().toISOString(),
    updatedAt: source.updatedAt || new Date().toISOString()
  }
}

export async function hydrateVmDslReportBlock(block, fetcher, options = {}) {
  const source = block && typeof block === 'object' ? clone(block) : {}
  const dsl = validateVmReportDsl(clone(source.dsl || {}))
  const traceId = options.traceId || ''
  const dslParams = dsl.params && typeof dsl.params === 'object' && !Array.isArray(dsl.params) ? dsl.params : {}
  const queryParams = Object.assign({}, options.queryParams || {}, dslParams)
  let resolvedParams = null
  try {
    if (typeof options.paramResolver !== 'function') {
      throw new Error('vmChat 未配置动态参数解析器')
    }
    resolvedParams = await options.paramResolver(queryParams)
    const queryPlan = buildRequestPlan(dsl, resolvedParams)
    const queryResult = await executeVmQueryPlan(queryPlan, fetcher, {
      traceId,
      dataMode: options.dataMode
    })
    const responses = dsl.requests.reduce((accumulator, request) => {
      const payloadByRequestId = queryResult.payloadByRequestId || {}
      accumulator[request.id] = Object.prototype.hasOwnProperty.call(payloadByRequestId, request.id)
        ? payloadByRequestId[request.id]
        : { body: queryResult.rowsByRequestId[request.id] || [] }
      return accumulator
    }, {})
    const rows = await executeVmReportTransformFunction(dsl.transform.function, responses, {
      executor: options.transformExecutor
    })
    source.title = toTitle(dsl.view && dsl.view.title || source.title, source.title || 'vmChat 视图')
    source.queryContext = deriveQueryContext(queryParams)
    if (!source.renderSpec) {
      source.renderSpec = buildRenderSpecFromDsl(dsl, source.title)
    }
    if (dsl.view.type === 'table') {
      source.renderSpec.columns = buildTableColumns(dsl.view)
      source.renderSpec.rows = rows
    } else {
      source.renderSpec.option = buildChartOption(dsl.view, source.title)
      source.renderSpec.option.dataset.source = rows
    }
    const runtime = buildRuntimeDiagnostics(queryResult, '', resolvedParams)
    runtime.totalRows = rows.length
    runtime.transformRowCount = rows.length
    if (!rows.length) {
      runtime.displayDiagnostics = [{
        status: 'empty',
        detail: '接口请求成功但未返回可渲染数据。'
      }]
    }
    source.sourceData = {
      provider: 'vm-report-dsl',
      runtime
    }
    source.requestDiagnostics = Object.keys(runtime.timings).map(requestId => {
      const rowCount = runtime.timings[requestId].rowCount
      return {
        requestId,
        detail: rowCount > 0
          ? requestId + ' 返回 ' + rowCount + ' 行'
          : requestId + ' 已接收响应，渲染行数由 transform 数据路径决定'
      }
    })
    source.transformDiagnostics = [{
      status: rows.length ? 'ready' : 'empty',
      detail: 'transform.function 输出 ' + rows.length + ' 行'
    }]
    source.renderSnapshot = {
      rowCount: rows.length,
      updatedAt: new Date().toISOString()
    }
    source.renderState = {
      status: rows.length ? 'ready' : 'empty',
      hydratedAt: new Date().toISOString()
    }
    source.updatedAt = new Date().toISOString()
    return source
  } catch (error) {
    const message = error && error.message ? error.message : '模块数据加载失败'
    const runtime = buildRuntimeDiagnostics(null, message, resolvedParams)
    runtime.displayDiagnostics = [{ status: 'error', detail: message }]
    source.sourceData = {
      provider: 'vm-report-dsl',
      runtime
    }
    source.requestDiagnostics = []
    source.transformDiagnostics = [{ status: 'error', detail: message }]
    source.renderSnapshot = null
    source.renderState = createErrorState(message)
    if (source.viewType === 'table' || source.type === 'table') {
      source.renderSpec = {
        renderer: 'table',
        columns: [
          { field: 'status', title: '状态', align: 'left' },
          { field: 'detail', title: '说明', align: 'left' }
        ],
        rows: [{ status: 'error', detail: message }]
      }
    } else {
      source.renderSpec = {
        renderer: 'echarts',
        option: {
          title: { text: dsl.view && dsl.view.title || source.title || 'vmChat 图表', show: false },
          tooltip: { show: false },
          xAxis: { type: 'category', data: [] },
          yAxis: { type: 'value' },
          series: [{ type: 'line', data: [] }],
          graphic: [{
            type: 'text',
            left: 'center',
            top: 'middle',
            style: {
              text: message,
              fill: '#e53935',
              font: '14px sans-serif'
            }
          }]
        }
      }
    }
    source.updatedAt = new Date().toISOString()
    return source
  }
}
