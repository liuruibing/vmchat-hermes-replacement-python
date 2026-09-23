import axios from 'axios'

export const HERMES_BASE_URL_STORAGE_KEY = 'fof-research-hermes-base-url'
export const HERMES_API_KEY_STORAGE_KEY = 'fof-research-hermes-api-key'
export const HERMES_RUN_EVENTS_DISABLED_STORAGE_KEY = 'fof-research-hermes-run-events-disabled'
export const DEFAULT_HERMES_BASE_URL = '/hermes-api'
export const DEFAULT_HERMES_API_KEY = String(process.env.HERMES_API_KEY || '').trim()
export const DEFAULT_HERMES_DATA_MODEL = 'deepseek-v4-flash'
export const DEFAULT_HERMES_ANALYSIS_MODEL = 'deepseek-v4-flash'

const LEGACY_HERMES_BASE_URLS = [
  'http://192.168.30.241:8642',
  'http://127.0.0.1:8642',
  'http://localhost:8642',
  'http://0.0.0.0:8642',
  'http://127.0.0.1:8648',
  'http://localhost:8648',
  'http://0.0.0.0:8648'
]

function buildDefaultHermesBaseUrl() {
  return DEFAULT_HERMES_BASE_URL
}

function migrateLegacyHermesUiUrl(value) {
  const normalizedValue = String(value || '').trim()
  if (!normalizedValue) return normalizedValue
  if (normalizedValue === DEFAULT_HERMES_BASE_URL) {
    return DEFAULT_HERMES_BASE_URL
  }
  if (
    LEGACY_HERMES_BASE_URLS.includes(normalizedValue.replace(/\/+$/, '')) ||
    /^https?:\/\/(127\.0\.0\.1|localhost|0\.0\.0\.0):8648(?=\/|$)/i.test(normalizedValue)
  ) {
    return DEFAULT_HERMES_BASE_URL
  }
  return normalizedValue
}

function normalizeBaseUrl(baseUrl) {
  const value = migrateLegacyHermesUiUrl(baseUrl)
  if (!value) return buildDefaultHermesBaseUrl()
  return value.replace(/\/+$/, '')
}

export function getHermesBaseUrl() {
  if (typeof window === 'undefined') {
    return DEFAULT_HERMES_BASE_URL
  }
  const normalizedBaseUrl = normalizeBaseUrl(window.localStorage.getItem(HERMES_BASE_URL_STORAGE_KEY))
  window.localStorage.setItem(HERMES_BASE_URL_STORAGE_KEY, normalizedBaseUrl)
  return normalizedBaseUrl
}

export function setHermesBaseUrl(baseUrl) {
  const normalizedBaseUrl = normalizeBaseUrl(baseUrl)
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(HERMES_BASE_URL_STORAGE_KEY, normalizedBaseUrl)
  }
  return normalizedBaseUrl
}

export function getHermesApiKey() {
  if (typeof window === 'undefined') {
    return DEFAULT_HERMES_API_KEY
  }
  const configuredApiKey = String(DEFAULT_HERMES_API_KEY || '').trim()
  const storedApiKey = String(window.localStorage.getItem(HERMES_API_KEY_STORAGE_KEY) || '').trim()
  const normalizedApiKey = configuredApiKey || storedApiKey
  window.localStorage.setItem(HERMES_API_KEY_STORAGE_KEY, normalizedApiKey)
  return normalizedApiKey
}

export function setHermesApiKey(apiKey) {
  const normalizedApiKey = String(apiKey || '').trim()
  if (typeof window !== 'undefined') {
    window.localStorage.setItem(HERMES_API_KEY_STORAGE_KEY, normalizedApiKey)
  }
  return normalizedApiKey
}

export function getHermesRunEventsDisabled() {
  if (typeof window === 'undefined' || !window.localStorage) return false
  return String(window.localStorage.getItem(HERMES_RUN_EVENTS_DISABLED_STORAGE_KEY) || '').trim() === 'true'
}

export function setHermesRunEventsDisabled(disabled) {
  if (typeof window !== 'undefined' && window.localStorage) {
    if (disabled) {
      window.localStorage.setItem(HERMES_RUN_EVENTS_DISABLED_STORAGE_KEY, 'true')
    } else {
      window.localStorage.removeItem(HERMES_RUN_EVENTS_DISABLED_STORAGE_KEY)
    }
  }
  return Boolean(disabled)
}

export function shouldUseHermesRunEvents() {
  if (getHermesBaseUrl() === '/hermes-api') return true
  return !getHermesRunEventsDisabled()
}

export function buildHermesRequestUrl(path) {
  return getHermesBaseUrl() + path
}

export function buildHermesAuthHeaders(headers) {
  const normalizedHeaders = Object.assign({}, headers || {})
  const apiKey = getHermesApiKey()
  if (apiKey) {
    normalizedHeaders.Authorization = 'Bearer ' + apiKey
  }
  return normalizedHeaders
}

function unwrapResponse(response) {
  if (!response) return response
  const contentType = (response.headers && (response.headers['content-type'] || response.headers['Content-Type'])) || ''
  if (typeof response.data === 'string' && /text\/html/i.test(contentType)) {
    const htmlResponseError = new Error('AI 助手返回了页面内容，当前地址更像 Web UI 而不是 API 服务')
    htmlResponseError.code = 'HERMES_HTML_RESPONSE'
    throw htmlResponseError
  }
  const payload = response.data || response
  if (payload && Object.prototype.hasOwnProperty.call(payload, 'status') && Object.prototype.hasOwnProperty.call(payload, 'data')) {
    return payload.data
  }
  return payload
}

function createHermesClient() {
  return axios.create({
    timeout: 600000,
    withCredentials: false
  })
}

function normalizeHermesHttpError(error, requestUrl) {
  const status = error && error.response && error.response.status
  if (status !== 403) return error
  const message = 'Hermes 请求被拒绝：HTTP 403。当前地址：' + requestUrl + '。请检查 Hermes Base URL 是否应为 /hermes-api，以及浏览器 localStorage 中的 Hermes token 是否过期。'
  const nextError = new Error(message)
  nextError.code = 'HERMES_HTTP_403'
  nextError.status = status
  nextError.url = requestUrl
  nextError.cause = error
  return nextError
}

function post(path, data, headers) {
  const client = createHermesClient()
  const requestUrl = buildHermesRequestUrl(path)
  return client({
    url: requestUrl,
    method: 'post',
    data: data,
    headers: buildHermesAuthHeaders(headers)
  }).then(unwrapResponse).catch(error => {
    throw normalizeHermesHttpError(error, requestUrl)
  })
}

function get(path) {
  const client = createHermesClient()
  const requestUrl = buildHermesRequestUrl(path)
  return client({
    url: requestUrl,
    method: 'get',
    headers: buildHermesAuthHeaders()
  }).then(unwrapResponse).catch(error => {
    throw normalizeHermesHttpError(error, requestUrl)
  })
}

export function fetchHermesPayload(payloadId) {
  const normalizedPayloadId = String(payloadId || '').trim()
  if (!normalizedPayloadId) {
    return Promise.reject(new Error('payloadId 不能为空'))
  }
  return get('/api/agent/payloads/' + encodeURIComponent(normalizedPayloadId)).catch(error => {
    if (error && error.response && error.response.status === 404) {
      return get('/api/agent/payload/' + encodeURIComponent(normalizedPayloadId))
    }
    throw error
  })
}

export function createResearchBatch(payload) {
  return post('/api/fof-research/batches', payload)
}

export function uploadBatchDocuments(batchId, files) {
  const formData = new FormData()
  ;(files || []).forEach(file => {
    formData.append('files', file.raw || file)
  })
  return post('/api/fof-research/batches/' + batchId + '/documents', formData)
}

export function identifyBatchCompanies(batchId) {
  return post('/api/fof-research/batches/' + batchId + '/identify-companies')
}

export function fetchResearchBatch(batchId) {
  return get('/api/fof-research/batches/' + batchId)
}

export function fetchBatchCompanies(batchId) {
  return get('/api/fof-research/batches/' + batchId + '/companies')
}

export function confirmCompanyDocumentAssignment(companyCaseId, payload) {
  return post('/api/fof-research/companies/' + companyCaseId + '/confirm-assignment', payload)
}

export function evaluateCompanySufficiency(companyCaseId) {
  return post('/api/fof-research/companies/' + companyCaseId + '/evaluate-sufficiency')
}

export function fetchCompanySufficiencyReport(companyCaseId) {
  return get('/api/fof-research/companies/' + companyCaseId + '/sufficiency-report')
}

export function confirmCompanyJudgement(companyCaseId, payload) {
  return post('/api/fof-research/companies/' + companyCaseId + '/confirm-judgement', payload || {})
}

export function triggerCompanyManagerSummary(companyCaseId) {
  return post('/api/fof-research/companies/' + companyCaseId + '/manager-summary')
}

export function triggerBatchComparison(batchId, payload) {
  return post('/api/fof-research/batches/' + batchId + '/comparison', payload || {})
}

export function sendHermesChatCompletion(messages, options) {
  const sessionId = options && options.sessionId
  const model = (options && options.model) || 'hermes-agent'
  return post(
    '/v1/chat/completions',
    {
      model: model,
      stream: false,
      user: sessionId || 'ai-chat',
      messages: messages || []
    },
    {
      'Content-Type': 'application/json;charset=UTF-8'
    }
  )
}

function splitRunMessages(messages) {
  const list = Array.isArray(messages) ? messages : []
  const system = list.find(item => item && item.role === 'system')
  return {
    instructions: system ? system.content : '',
    input: list
      .filter(item => item && item.role !== 'system')
      .map(item => ({
        role: item.role,
        content: String(item.content || '')
      }))
  }
}

export function createHermesRun(messages, options) {
  const sessionId = options && options.sessionId
  const model = (options && options.model) || 'hermes-agent'
  const skills = Array.isArray(options && options.skills) ? options.skills.filter(Boolean) : []
  const tools = Array.isArray(options && options.tools) ? options.tools.filter(Boolean) : []
  const splitMessages = splitRunMessages(messages)
  const payload = {
    model: model,
    input: splitMessages.input,
    instructions: splitMessages.instructions,
    session_id: sessionId || 'ai-chat'
  }
  if (skills.length) payload.skills = skills
  if (tools.length) payload.tools = tools
  return post('/v1/runs', payload, {
    'Content-Type': 'application/json;charset=UTF-8'
  })
}

export function parseStreamDelta(payload) {
  const choice = (payload && payload.choices && payload.choices[0]) || {}
  const delta = choice.delta || choice.message || {}
  return {
    content: delta.content || choice.text || '',
    thinking: delta.reasoning_content || delta.reasoning || delta.thinking || delta.thought || ''
  }
}

export function splitThinkingTags(content, state) {
  const source = (state.tagBuffer || '') + String(content || '')
  const thinkStart = '<think>'
  const thinkEnd = '</think>'
  let visibleContent = ''
  let thinking = ''
  let index = 0
  state.tagBuffer = ''

  while (index < source.length) {
    const remaining = source.slice(index)
    if (remaining.indexOf(thinkStart) === 0) {
      state.inThinkingTag = true
      index += thinkStart.length
      continue
    }
    if (remaining.indexOf(thinkEnd) === 0) {
      state.inThinkingTag = false
      index += thinkEnd.length
      continue
    }

    const couldBeStart = thinkStart.indexOf(remaining) === 0
    const couldBeEnd = thinkEnd.indexOf(remaining) === 0
    if (couldBeStart || couldBeEnd) {
      state.tagBuffer = remaining
      break
    }

    if (state.inThinkingTag) {
      thinking += source[index]
    } else {
      visibleContent += source[index]
    }
    index += 1
  }

  return {
    content: visibleContent,
    thinking: thinking
  }
}

export function extractHermesRunOutputText(output) {
  if (output === null || output === undefined) return ''
  if (typeof output === 'string') return output
  if (Array.isArray(output)) {
    return output
      .map(item => extractHermesRunOutputText(item))
      .filter(Boolean)
      .join('')
  }
  if (typeof output !== 'object') return ''

  if (typeof output.text === 'string') return output.text
  if (typeof output.output_text === 'string') return output.output_text
  if (typeof output.delta === 'string') return output.delta
  if (typeof output.content === 'string') return output.content
  if (Array.isArray(output.content)) return extractHermesRunOutputText(output.content)
  if (output.message) return extractHermesRunOutputText(output.message)
  if (Array.isArray(output.output)) return extractHermesRunOutputText(output.output)
  return ''
}

function isLikelyRenderPayloadFragment(text) {
  const source = String(text || '').trim()
  if (!source) return false
  const quoteCount = (source.match(/"/g) || []).length
  const colonCount = (source.match(/:/g) || []).length
  const renderKeywordCount = [
    'renderType',
    'operations',
    'uiType',
    'payload',
    'xField',
    'yFields',
    'blockId',
    'chart',
    'option',
    'sourceData',
    'series',
    'xAxis',
    'yAxis',
    'fundCode',
    'targetBlockId'
  ].filter(keyword => source.indexOf(keyword) !== -1).length
  return renderKeywordCount >= 2 || (quoteCount >= 8 && colonCount >= 3 && /[,{}\[\]]/.test(source))
}

function dispatchSseLine(line, state, handlers) {
  const trimmedLine = String(line || '').trim()
  if (!trimmedLine || trimmedLine.indexOf('data:') !== 0) return
  const data = trimmedLine.replace(/^data:\s*/, '')
  if (data === '[DONE]') {
    state.done = true
    return
  }
  let payload
  try {
    payload = JSON.parse(data)
  } catch (error) {
    return
  }
  state.eventCount += 1
  const delta = parseStreamDelta(payload)
  const splitContent = splitThinkingTags(delta.content, state)
  const nextThinking = delta.thinking + splitContent.thinking
  const nextContent = splitContent.content
  if (nextThinking && !isLikelyRenderPayloadFragment(nextThinking)) {
    state.thinking += nextThinking
    handlers && handlers.onThinking && handlers.onThinking(nextThinking, state.thinking)
  }
  if (nextContent) {
    state.content += nextContent
    handlers && handlers.onContent && handlers.onContent(nextContent, state.content)
  }
  handlers && handlers.onRaw && handlers.onRaw(payload)
}

function dispatchRunEventLine(line, state, handlers) {
  const trimmedLine = String(line || '').trim()
  if (!trimmedLine || trimmedLine.indexOf('data:') !== 0) return
  const data = trimmedLine.replace(/^data:\s*/, '')
  let payload
  try {
    payload = JSON.parse(data)
  } catch (error) {
    return
  }
  state.eventCount += 1
  const eventName = payload.event || 'event'
  handlers && handlers.onEvent && handlers.onEvent(payload, state)

  if (eventName === 'reasoning.delta') {
    var delta = String(payload.delta || '')
    if (delta) {
      state.thinking += delta
      handlers && handlers.onThinking && handlers.onThinking(delta, state.thinking)
    }
    return
  }

  if (eventName === 'reasoning.done') {
    state.reasoningDone = true
    return
  }

  if (eventName === 'message.delta') {
    const splitContent = splitThinkingTags(payload.delta || '', state)
    if (splitContent.thinking) {
      state.thinking += splitContent.thinking
      handlers && handlers.onThinking && handlers.onThinking(splitContent.thinking, state.thinking)
    }
    if (splitContent.content) {
      state.content += splitContent.content
      handlers && handlers.onContent && handlers.onContent(splitContent.content, state.content)
    }
    return
  }

  if (eventName === 'reasoning.available') {
    const thinking = payload.text || payload.preview || ''
    if (thinking && !isLikelyRenderPayloadFragment(thinking)) {
      state.thinking += (state.thinking ? '\n' : '') + thinking
      handlers && handlers.onThinking && handlers.onThinking(thinking, state.thinking)
    }
    return
  }

  if (eventName === 'tool.started' || eventName === 'tool.completed' || eventName === 'tool.result') {
    handlers && handlers.onTool && handlers.onTool(payload, state)
    return
  }

  if (eventName === 'run.completed') {
    state.done = true
    state.finalOutput = extractHermesRunOutputText(payload.output) || state.content
    state.usage = payload.usage || {}
    handlers && handlers.onCompleted && handlers.onCompleted(payload, state)
    return
  }

  if (eventName === 'run.failed') {
    state.done = true
    const runError = new Error(payload.error || 'AI 助手任务执行失败')
    runError.code = 'HERMES_RUN_FAILED'
    state.error = runError
  }
}

export async function sendHermesRunEvents(messages, options, handlers) {
  if (!shouldUseHermesRunEvents()) {
    const disabledError = new Error('当前环境已禁用 Hermes 事件流，请直接使用普通请求')
    disabledError.code = 'HERMES_RUN_EVENTS_DISABLED'
    throw disabledError
  }
  if (typeof fetch !== 'function' || typeof ReadableStream === 'undefined') {
    const streamError = new Error('当前浏览器不支持流式读取')
    streamError.code = 'HERMES_STREAM_UNSUPPORTED'
    throw streamError
  }
  const run = await createHermesRun(messages, options)
  const runId = run && run.run_id
  if (!runId) {
    const runError = new Error('AI 助手任务创建失败：缺少 run_id')
    runError.code = 'HERMES_RUN_UNAVAILABLE'
    throw runError
  }
  handlers && handlers.onRunCreated && handlers.onRunCreated(run)
  let response
  const eventsUrl = buildHermesRequestUrl('/v1/runs/' + encodeURIComponent(runId) + '/events')
  try {
    response = await fetch(eventsUrl, {
      method: 'GET',
      headers: buildHermesAuthHeaders({
        Accept: 'text/event-stream'
      })
    })
  } catch (error) {
    const message = error && error.message ? error.message : String(error || '')
    if (/Failed to fetch/i.test(message)) {
      setHermesRunEventsDisabled(true)
      const streamError = new Error('Hermes 事件流跨域或网络不可用，已自动切换为普通请求')
      streamError.code = 'HERMES_RUN_EVENTS_FETCH_FAILED'
      streamError.cause = error
      throw streamError
    }
    throw error
  }
  const contentType = (response.headers && response.headers.get('content-type')) || ''
  handlers &&
    handlers.onHeaders &&
    handlers.onHeaders({
      status: response.status,
      contentType: contentType,
      isSse: /text\/event-stream/i.test(contentType),
      runId: runId
    })
  if (/text\/html/i.test(contentType)) {
    const htmlResponseError = new Error('AI 助手返回了页面内容，当前地址更像 Web UI 而不是 API 服务')
    htmlResponseError.code = 'HERMES_HTML_RESPONSE'
    throw htmlResponseError
  }
  if (!response.ok) {
    if (response.status === 403) {
      const forbiddenError = new Error('Hermes 事件流请求被拒绝：HTTP 403。当前地址：' + eventsUrl + '。请检查 Hermes Base URL 是否应为 /hermes-api，以及浏览器 localStorage 中的 Hermes token 是否过期。')
      forbiddenError.code = 'HERMES_HTTP_403'
      forbiddenError.status = response.status
      forbiddenError.url = eventsUrl
      throw forbiddenError
    }
    throw new Error('AI 助手事件流请求失败：HTTP ' + response.status)
  }
  if (!response.body || !response.body.getReader) {
    const streamError = new Error('AI 助手当前事件流响应不是标准流式响应')
    streamError.code = 'HERMES_STREAM_UNSUPPORTED'
    throw streamError
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  const state = {
    runId: runId,
    content: '',
    finalOutput: '',
    thinking: '',
    reasoningDone: false,
    buffer: '',
    tagBuffer: '',
    inThinkingTag: false,
    done: false,
    stoppedEarly: false,
    chunkCount: 0,
    byteLength: 0,
    eventCount: 0,
    contentType: contentType,
    usage: {}
  }
  handlers && handlers.onStart && handlers.onStart(state)

  while (!state.done) {
    const result = await reader.read()
    if (result.done) break
    state.chunkCount += 1
    state.byteLength += result.value ? result.value.byteLength : 0
    handlers &&
      handlers.onChunk &&
      handlers.onChunk({
        chunkCount: state.chunkCount,
        byteLength: state.byteLength,
        eventCount: state.eventCount,
        runId: runId
      })
    state.buffer += decoder.decode(result.value, { stream: true })
    const lines = state.buffer.split(/\r?\n/)
    state.buffer = lines.pop() || ''
    for (let index = 0; index < lines.length; index += 1) {
      dispatchRunEventLine(lines[index], state, handlers)
      if (handlers && handlers.shouldStop && handlers.shouldStop(state)) {
        state.done = true
        state.stoppedEarly = true
        break
      }
    }
    if (state.error) throw state.error
  }

  if (state.stoppedEarly && reader.cancel) {
    try {
      await reader.cancel()
    } catch (error) {
      // Ignore cancellation errors after we already have enough tool payloads.
    }
  }

  if (state.buffer && !state.stoppedEarly) {
    dispatchRunEventLine(state.buffer, state, handlers)
  }
  if (state.error) throw state.error
  handlers && handlers.onDone && handlers.onDone(state)
  if ((state.eventCount || 0) === 0) {
    const emptyEventsError = new Error('AI 助手事件流已连接但没有返回任何事件；已停止自动回退，避免同一问题重复触发模型调用')
    emptyEventsError.code = 'HERMES_RUN_EVENTS_EMPTY'
    emptyEventsError.runId = runId
    throw emptyEventsError
  }
  return {
    runId: state.runId,
    content: state.finalOutput || state.content,
    thinking: state.thinking,
    chunkCount: state.chunkCount,
    byteLength: state.byteLength,
    eventCount: state.eventCount,
    contentType: state.contentType,
    usage: state.usage,
    stoppedEarly: state.stoppedEarly
  }
}

export async function sendHermesChatCompletionStream(messages, options, handlers) {
  if (typeof fetch !== 'function' || typeof ReadableStream === 'undefined') {
    const streamError = new Error('当前浏览器不支持流式读取')
    streamError.code = 'HERMES_STREAM_UNSUPPORTED'
    throw streamError
  }
  const sessionId = options && options.sessionId
  const model = (options && options.model) || 'hermes-agent'
  const response = await fetch(buildHermesRequestUrl('/v1/chat/completions'), {
    method: 'POST',
    headers: buildHermesAuthHeaders({
      'Content-Type': 'application/json;charset=UTF-8'
    }),
    body: JSON.stringify({
      model: model,
      stream: true,
      user: sessionId || 'ai-chat',
      messages: messages || []
    })
  })
  const contentType = (response.headers && response.headers.get('content-type')) || ''
  handlers &&
    handlers.onHeaders &&
    handlers.onHeaders({
      status: response.status,
      contentType: contentType,
      isSse: /text\/event-stream/i.test(contentType)
    })
  if (/text\/html/i.test(contentType)) {
    const htmlResponseError = new Error('AI 助手返回了页面内容，当前地址更像 Web UI 而不是 API 服务')
    htmlResponseError.code = 'HERMES_HTML_RESPONSE'
    throw htmlResponseError
  }
  if (!response.ok) {
    throw new Error('AI 助手流式请求失败：HTTP ' + response.status)
  }
  if (!response.body || !response.body.getReader) {
    const streamError = new Error('AI 助手当前响应不是标准流式响应')
    streamError.code = 'HERMES_STREAM_UNSUPPORTED'
    throw streamError
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  const state = {
    content: '',
    thinking: '',
    buffer: '',
    tagBuffer: '',
    inThinkingTag: false,
    done: false,
    chunkCount: 0,
    byteLength: 0,
    eventCount: 0,
    contentType: contentType
  }
  handlers && handlers.onStart && handlers.onStart()

  while (!state.done) {
    const result = await reader.read()
    if (result.done) break
    state.chunkCount += 1
    state.byteLength += result.value ? result.value.byteLength : 0
    handlers &&
      handlers.onChunk &&
      handlers.onChunk({
        chunkCount: state.chunkCount,
        byteLength: state.byteLength,
        eventCount: state.eventCount
      })
    state.buffer += decoder.decode(result.value, { stream: true })
    const lines = state.buffer.split(/\r?\n/)
    state.buffer = lines.pop() || ''
    lines.forEach(line => dispatchSseLine(line, state, handlers))
  }

  if (state.buffer) {
    dispatchSseLine(state.buffer, state, handlers)
  }
  handlers && handlers.onDone && handlers.onDone(state)
  return {
    content: state.content,
    thinking: state.thinking,
    chunkCount: state.chunkCount,
    byteLength: state.byteLength,
    eventCount: state.eventCount,
    contentType: state.contentType
  }
}
export function fetchHermesWikiTree() {
  return get('/v1/wiki/tree')
}

export function fetchHermesWikiDocument(documentId) {
  const normalizedId = String(documentId || '').trim()
  if (!normalizedId) {
    return Promise.reject(new Error('documentId 不能为空'))
  }
  return get('/v1/wiki/documents/' + encodeURIComponent(normalizedId))
}
