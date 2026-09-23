const GLOBAL_LOG_KEY = '__VM_CHAT_LOGS__'
const STORAGE_LOG_KEY = 'vm-chat-logs'
const MAX_LOGS = 600
const DEBUG_SESSION_TTL_MS = 30 * 60 * 1000
const MAX_STRING_LENGTH = 2000
const MAX_ARRAY_SAMPLE = 3
const MAX_OBJECT_KEYS = 40

function nowIso() {
  return new Date().toISOString()
}

function isBrowser() {
  return typeof window !== 'undefined'
}

function isProduction() {
  if (typeof process === 'undefined' || !process.env || !process.env.NODE_ENV) return true
  return process.env.NODE_ENV === 'production'
}

function removeStoredLogs(storage) {
  try {
    if (storage) storage.removeItem(STORAGE_LOG_KEY)
  } catch (error) {
    // Logging cleanup must never break vmChat.
  }
}

function safeString(value) {
  const text = String(value === undefined ? '' : value)
  return text.length > MAX_STRING_LENGTH ? text.slice(0, MAX_STRING_LENGTH) + '...[truncated]' : text
}

function redactKey(key, value) {
  if (/authorization|token|api[-_]?key|password|secret/i.test(String(key))) {
    return value ? '[redacted]' : value
  }
  return value
}

export function summarizeVmLogValue(value, depth = 0) {
  if (value === null || value === undefined) return value
  if (typeof value === 'string') return safeString(value)
  if (typeof value === 'number' || typeof value === 'boolean') return value
  if (value instanceof Error) {
    return {
      name: value.name,
      message: value.message,
      code: value.code || '',
      stack: value.stack ? safeString(value.stack) : ''
    }
  }
  if (Array.isArray(value)) {
    return {
      type: 'array',
      length: value.length,
      sample: value.slice(0, MAX_ARRAY_SAMPLE).map(item => summarizeVmLogValue(item, depth + 1))
    }
  }
  if (typeof value === 'object') {
    const keys = Object.keys(value)
    const result = {
      type: 'object',
      keys: keys.slice(0, MAX_OBJECT_KEYS)
    }
    keys.slice(0, MAX_OBJECT_KEYS).forEach(key => {
      const nextValue = redactKey(key, value[key])
      if (depth >= 2 && nextValue && typeof nextValue === 'object') {
        result[key] = Array.isArray(nextValue)
          ? { type: 'array', length: nextValue.length }
          : { type: 'object', keys: Object.keys(nextValue).slice(0, MAX_OBJECT_KEYS) }
        return
      }
      result[key] = summarizeVmLogValue(nextValue, depth + 1)
    })
    return result
  }
  return safeString(value)
}

function summarizeProductionPayload(payload) {
  if (payload instanceof Error) {
    return {
      name: payload.name,
      code: payload.code || ''
    }
  }
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) {
    return { type: Array.isArray(payload) ? 'array' : typeof payload }
  }

  const safeKeys = [
    'requestId',
    'moduleKey',
    'mode',
    'sqlCode',
    'templateCode',
    'durationMs',
    'rowCount',
    'requestCount',
    'uniqueRequestCount',
    'totalRows',
    'dataMode',
    'mockFallback',
    'status',
    'code'
  ]
  const result = {}
  safeKeys.forEach(key => {
    const value = payload[key]
    if (value === null || ['string', 'number', 'boolean'].includes(typeof value)) {
      result[key] = value
    }
  })
  if (payload.error instanceof Error) {
    result.error = {
      name: payload.error.name,
      code: payload.error.code || ''
    }
  }
  return result
}

function readDebugSessionLogs() {
  if (!isBrowser() || isProduction() || !window.sessionStorage) return []
  try {
    const persisted = window.sessionStorage.getItem(STORAGE_LOG_KEY)
    if (!persisted) return []
    const parsed = JSON.parse(persisted)
    if (!parsed.expiresAt || parsed.expiresAt <= Date.now()) {
      window.sessionStorage.removeItem(STORAGE_LOG_KEY)
      return []
    }
    return Array.isArray(parsed.logs) ? parsed.logs.slice(-MAX_LOGS) : []
  } catch (error) {
    removeStoredLogs(window.sessionStorage)
    return []
  }
}

function getStore() {
  if (!isBrowser()) return { logs: [] }
  removeStoredLogs(window.localStorage)
  if (!window[GLOBAL_LOG_KEY]) {
    const persistedLogs = readDebugSessionLogs()
    window[GLOBAL_LOG_KEY] = {
      createdAt: nowIso(),
      logs: persistedLogs
    }
  }
  return window[GLOBAL_LOG_KEY]
}

function persistStore(store) {
  if (!isBrowser()) return
  removeStoredLogs(window.localStorage)
  if (isProduction() || !window.sessionStorage) {
    removeStoredLogs(window.sessionStorage)
    return
  }
  try {
    window.sessionStorage.setItem(STORAGE_LOG_KEY, JSON.stringify({
      updatedAt: nowIso(),
      expiresAt: Date.now() + DEBUG_SESSION_TTL_MS,
      logs: store.logs.slice(-MAX_LOGS)
    }))
  } catch (error) {
    // Logging must never break the vmChat execution path.
  }
}

export function createVmTraceId(prefix = 'vm-chat') {
  return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(16).slice(2, 8)
}

export function logVmChatEvent(stage, event, payload, options = {}) {
  const entry = {
    id: createVmTraceId('log'),
    time: nowIso(),
    level: options.level || 'info',
    traceId: options.traceId || '',
    stage: String(stage || 'unknown'),
    event: String(event || 'event'),
    payload: isProduction() ? summarizeProductionPayload(payload) : summarizeVmLogValue(payload)
  }
  const store = getStore()
  store.logs.push(entry)
  if (store.logs.length > MAX_LOGS) {
    store.logs.splice(0, store.logs.length - MAX_LOGS)
  }
  persistStore(store)

  if (isBrowser() && typeof console !== 'undefined') {
    const method = entry.level === 'error' ? 'error' : entry.level === 'warn' ? 'warn' : 'info'
    if (console[method]) {
      console[method]('[vmChat][' + entry.stage + '][' + entry.event + ']', entry)
    }
  }
  return entry
}

export function getVmChatLogs(options = {}) {
  const store = getStore()
  const limit = options.limit || 200
  const traceId = options.traceId || ''
  const logs = traceId
    ? store.logs.filter(item => item.traceId === traceId)
    : store.logs
  return logs.slice(Math.max(0, logs.length - limit))
}

export function clearVmChatLogs() {
  const store = getStore()
  store.logs = []
  persistStore(store)
}
