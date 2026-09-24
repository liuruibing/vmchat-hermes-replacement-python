import { createVmDslReportBlock } from './vm-report-dsl-runtime.js'
import { writeVmDebugFile } from './vm-debug-file-logger.js'

const ALLOWED_OPERATION_TYPES = ['appendBlock', 'replaceBlock']
const NOTICE_STATUSES = ['clarify', 'rejected', 'error']
const VM_PROTOCOL_VERSION = 'hermes-workspace + vm-report-dsl-v1 + vm-chat-protocol-v3'

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

function stripJsonFence(content) {
  const value = String(content || '').trim()
  const fenced = value.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/i)
  return fenced ? fenced[1].trim() : value
}

function normalizeSmartQuotes(text) {
  return String(text || '')
    .replace(/[“”]/g, '"')
    .replace(/[‘’]/g, "'")
}

function trimTrailingAnchorText(text) {
  return String(text || '').replace(/\n+\s*已记录 vmChat 会话锚点[\s\S]*$/i, '').trim()
}

function extractBalancedJsonValueAt(source, start) {
  const openChar = source[start]
  if (openChar !== '{' && openChar !== '[') return ''
  const closeChar = openChar === '[' ? ']' : '}'
  let depth = 0
  let inString = false
  let escaped = false
  for (let index = start; index < source.length; index += 1) {
    const char = source[index]
    if (inString) {
      if (escaped) {
        escaped = false
        continue
      }
      if (char === '\\') {
        escaped = true
        continue
      }
      if (char === '"') {
        inString = false
      }
      continue
    }
    if (char === '"') {
      inString = true
      continue
    }
    if (char === openChar) depth += 1
    if (char === closeChar) {
      depth -= 1
      if (depth === 0) {
        return source.slice(start, index + 1)
      }
    }
  }
  return ''
}

function isProtocolJsonCandidate(value) {
  if (Array.isArray(value)) {
    return value.length > 0 && value.every(item => isProtocolJsonCandidate(item))
  }
  if (!value || typeof value !== 'object') return false
  if (value.action && value.id && Array.isArray(value.requests) && value.transform && value.view) return true
  return ['renderType', 'intent', 'operations', 'clarify'].some(field => Object.prototype.hasOwnProperty.call(value, field))
}

function findFirstBalancedJsonValue(content) {
  const source = trimTrailingAnchorText(normalizeSmartQuotes(stripJsonFence(content)))
  let fallback = ''
  for (let start = 0; start < source.length; start += 1) {
    if (source[start] !== '{' && source[start] !== '[') continue
    const candidate = extractBalancedJsonValueAt(source, start)
    if (!candidate) continue
    let parsed
    try {
      parsed = JSON.parse(repairUnescapedQuotes(candidate))
    } catch (error) {
      continue
    }
    if (isProtocolJsonCandidate(parsed)) return candidate
    if (!fallback) fallback = candidate
  }
  return fallback || source
}

function nextNonWhitespaceChar(source, startIndex) {
  for (let index = startIndex; index < source.length; index += 1) {
    const char = source[index]
    if (!/\s/.test(char)) return char
  }
  return ''
}

function repairUnescapedQuotes(source) {
  let result = ''
  let inString = false
  let escaped = false
  for (let index = 0; index < source.length; index += 1) {
    const char = source[index]
    if (!inString) {
      result += char
      if (char === '"') {
        inString = true
        escaped = false
      }
      continue
    }
    if (escaped) {
      result += char
      escaped = false
      continue
    }
    if (char === '\\') {
      result += char
      escaped = true
      continue
    }
    if (char === '"') {
      const nextChar = nextNonWhitespaceChar(source, index + 1)
      if (nextChar && ',}:]'.indexOf(nextChar) === -1) {
        result += '\\"'
        continue
      }
      result += char
      inString = false
      continue
    }
    result += char
  }
  return result
}

function inspectJsonExtraction(content) {
  const normalizedContent = trimTrailingAnchorText(normalizeSmartQuotes(stripJsonFence(content)))
  const extractedJson = findFirstBalancedJsonValue(content)
  const repairedJson = repairUnescapedQuotes(extractedJson)
  return {
    normalizedContent,
    extractedJson,
    repairedJson
  }
}

function isRejectedChatMessage(message) {
  const compact = String(message || '').replace(/\s+/g, '')
  return /(不能合并|无法合并|不能组合|无法组合|不能放到一起|无法放到一起|不允许合并|不可合并)/.test(compact)
}

function assertNewBlockShape(source) {
  const forbiddenFields = ['moduleKey', 'queryContext', 'sourceData', 'renderSpec', 'transformDsl', 'requests']
  const hit = forbiddenFields.find(field => Object.prototype.hasOwnProperty.call(source || {}, field))
  if (hit) {
    throw new Error('block 中包含旧协议字段：' + hit)
  }
  if (!source || typeof source !== 'object' || !source.dsl) {
    throw new Error('block 缺少 dsl')
  }
}

export function isLikelyVmProtocolContent(content) {
  const text = String(content || '').trim()
  if (!text) return false
  const jsonStart = text.indexOf('{')
  const arrayStart = text.indexOf('[')
  const startIndexes = [jsonStart, arrayStart].filter(index => index >= 0)
  if (!startIndexes.length) return false
  const jsonValueStart = Math.min.apply(null, startIndexes)
  const sample = text.slice(jsonValueStart, jsonValueStart + 1600)
  if (/"(intent|renderType|operations|clarify)"\s*:/.test(sample)) return true
  return /"action"\s*:\s*"(create|update)"/.test(sample) &&
    /"id"\s*:/.test(sample) &&
    /"requests"\s*:/.test(sample) &&
    /"transform"\s*:/.test(sample) &&
    /"view"\s*:/.test(sample)
}

export function formatVmAssistantStreamingContent(content, fallback = '正在生成可执行报告协议...') {
  const text = String(content || '').trim()
  if (!text) return fallback
  return isLikelyVmProtocolContent(text) ? fallback : text
}

export function getVmProtocolVersion() {
  return VM_PROTOCOL_VERSION
}

export function isExplicitVmBatchUpdateRequest(question) {
  const compact = String(question || '').replace(/\s+/g, '')
  return /(全部|所有|每个|批量)/.test(compact) && /(更新|修改|调整|改成|变成)/.test(compact)
}

export function createVmReportBlock(input, options = {}) {
  const source = input && typeof input === 'object' ? input : {}
  assertNewBlockShape(source)
  return createVmDslReportBlock(source, options)
}

export function getVmBlockDisplayTitle(block) {
  const dslTitle = block && block.dsl && block.dsl.view && block.dsl.view.title
  const title = dslTitle || block && block.title
  return String(title || '').trim()
}

export function buildVmReportBlocksSummary(reportBlocks) {
  const blocks = Array.isArray(reportBlocks) ? reportBlocks : []
  return JSON.stringify(blocks.map((block, index) => ({
    index: index + 1,
    blockId: block.blockId,
    title: getVmBlockDisplayTitle(block),
    viewType: block.viewType || block.type,
    moduleKey: block.moduleKey || '',
    dsl: block.dsl ? {
      action: block.dsl.action,
      id: block.dsl.id,
      params: block.dsl.params,
      requests: block.dsl.requests,
      view: block.dsl.view
    } : null,
    runtime: block.sourceData && block.sourceData.runtime ? {
      requestCount: block.sourceData.runtime.requestCount,
      totalRows: block.sourceData.runtime.totalRows,
      rowCounts: block.sourceData.runtime.rowCounts,
      lastError: block.sourceData.runtime.lastError
    } : null,
    status: block.renderState && block.renderState.status || 'idle'
  })), null, 2)
}

function createVmReportNotice(input, options = {}) {
  const source = input && typeof input === 'object' ? input : {}
  const status = String(source.status || '')
  if (NOTICE_STATUSES.indexOf(status) === -1) {
    throw new Error('不支持的 vmReportNotice.status：' + status)
  }
  const message = String(source.message || source.reason || '')
  return {
    status,
    message,
    questions: Array.isArray(source.questions) ? source.questions.map(item => String(item)) : [],
    reason: String(source.reason || message),
    traceId: String(options.traceId || source.traceId || ''),
    debugPayload: options.debugPayload !== undefined ? options.debugPayload : (source.debugPayload || null),
    createdAt: String(options.createdAt || source.createdAt || new Date().toISOString())
  }
}

export function buildVmReportNoticeFromPayload(payload, options = {}) {
  const source = payload && typeof payload === 'object' ? payload : {}
  const renderType = String(source.renderType || source.intent || '')
  const message = String(source.message || '')
  if (renderType === 'clarify') {
    const questions = source.clarify && Array.isArray(source.clarify.questions)
      ? source.clarify.questions
      : Array.isArray(source.questions) ? source.questions : []
    return createVmReportNotice({
      status: 'clarify',
      message,
      questions,
      reason: message
    }, options)
  }
  if (renderType === 'chat' && isRejectedChatMessage(message)) {
    return createVmReportNotice({
      status: 'rejected',
      message,
      reason: source.reason || message
    }, options)
  }
  return null
}

function extractProtocolPreamble(normalizedContent, extractedJson) {
  const source = String(normalizedContent || '')
  const json = String(extractedJson || '')
  if (!source || !json) return ''
  const jsonIndex = source.indexOf(json)
  if (jsonIndex <= 0) return ''
  const preamble = source.slice(0, jsonIndex).trim()
  if (!preamble || /^```(?:json)?\s*$/i.test(preamble)) return ''
  return preamble.replace(/```\s*$/i, '').trim()
}

function normalizeNonReportPayload(payload, options = {}) {
  const source = payload && typeof payload === 'object' && !Array.isArray(payload) ? payload : null
  if (!source) return null

  const intent = String(source.intent || '').trim().toLowerCase()
  const renderType = String(source.renderType || '').trim().toLowerCase()
  let type = renderType || intent
  if (type !== 'chat' && type !== 'clarify' && type !== 'businessinfo') return null
  const isKnownClarifyMismatch = intent === 'clarify' && renderType === 'chat'
  if (isKnownClarifyMismatch) {
    type = 'clarify'
  } else if ((intent && intent !== type) || (renderType && renderType !== type)) {
    throw new Error('Hermes 非报表协议的 intent 与 renderType 必须一致')
  }
  if (Object.prototype.hasOwnProperty.call(source, 'operations') || Object.prototype.hasOwnProperty.call(source, 'blocks')) {
    throw new Error('Hermes JSON 响应只能是完整 vm-report-dsl 或规范的 chat/clarify/businessInfo；非报表回答不得携带 operations 或 blocks')
  }

  const message = String(source.message || '').trim()
  if (!message) {
    throw new Error('Hermes 非报表协议缺少 message')
  }

  const nestedQuestions = source.clarify && Array.isArray(source.clarify.questions)
    ? source.clarify.questions
    : []
  const topLevelQuestions = Array.isArray(source.questions) ? source.questions : []
  const questions = (nestedQuestions.length ? nestedQuestions : topLevelQuestions)
    .map(item => String(item || '').trim())
    .filter(Boolean)

  const normalized = {
    intent: type,
    renderType: type,
    message,
    raw: clone(source)
  }
  if (source.reason) normalized.reason = String(source.reason)
  if (options.thinking) normalized.thinking = String(options.thinking)
  if (type === 'businessinfo') {
    const title = String(source.title || '').trim()
    if (!title) throw new Error('Hermes businessInfo 协议缺少 title')
    normalized.intent = 'businessInfo'
    normalized.renderType = 'businessInfo'
    normalized.title = title
  }
  if (type === 'clarify') {
    normalized.clarify = { questions }
  }
  return normalized
}

export function buildVmReportNoticeFromError(error, options = {}) {
  const message = error && error.message ? String(error.message) : String(error || 'vmChat 请求失败')
  return createVmReportNotice({
    status: 'error',
    message,
    reason: message
  }, options)
}

function buildCurrentDsls(reportBlocks) {
  return (Array.isArray(reportBlocks) ? reportBlocks : [])
    .filter(item => item && item.dsl)
    .map(item => ({
      blockId: item.blockId,
      id: item.dsl.id,
      title: getVmBlockDisplayTitle(item),
      viewType: item.viewType || item.type,
      dsl: {
        action: item.dsl.action,
        id: item.dsl.id,
        params: item.dsl.params,
        requests: item.dsl.requests,
        transform: item.dsl.transform,
        view: item.dsl.view
      }
    }))
}

export function buildVmHermesContext({ reportBlocks, selectedBlockId, globalQueryParams }) {
  return {
    selectedBlockId: String(selectedBlockId || ''),
    currentDsls: buildCurrentDsls(reportBlocks),
    globalQueryParams: globalQueryParams && typeof globalQueryParams === 'object'
      ? clone(globalQueryParams)
      : {}
  }
}

export function buildVmHermesMessages({ historyMessages, userInput, reportBlocks, selectedBlockId, globalQueryParams }) {
  const context = buildVmHermesContext({ reportBlocks, selectedBlockId, globalQueryParams })
  const systemPrompt = [
    'vmChat 客户端只负责传递页面上下文。',
    '业务规则、知识库检索、合并判断、DSL 生成和校验由 Python 服务端统一处理。',
    '以下机器上下文仅用于兼容旧版服务端解析；不要把它当作额外业务规则。',
    '当前 selectedBlockId：' + context.selectedBlockId,
    '当前 currentDsls：',
    JSON.stringify(context.currentDsls, null, 2),
    '当前全局查询条件：',
    JSON.stringify(context.globalQueryParams)
  ].join('\n')

  return [
    { role: 'system', content: systemPrompt },
    ...((historyMessages || [])
      .filter(item => item && (item.role === 'user' || item.role === 'assistant') && item.content)
      .slice(-8)
      .map(item => ({ role: item.role, content: String(item.content).slice(0, 4000) }))),
    { role: 'user', content: userInput }
  ]
}

function resolveUpdateTarget(dsl, options = {}, explicitTargetBlockId = '') {
  const blocks = Array.isArray(options.reportBlocks) ? options.reportBlocks : []
  if (!blocks.length) {
    throw new Error('update 缺少前端报表块快照，无法确认更新目标')
  }
  const matches = explicitTargetBlockId
    ? blocks.filter(item => item && item.blockId === explicitTargetBlockId)
    : blocks.filter(item => item && item.dsl && dsl && item.dsl.id === dsl.id)
  if (!matches.length) {
    throw new Error('update 目标不存在，请确认要更新的报表块')
  }
  if (matches.length > 1) {
    throw new Error('update 目标不唯一，当前页面命中多个报表块，请确认实际要更新的报表块')
  }
  const target = matches[0]
  if (!target.dsl || !dsl || target.dsl.id !== dsl.id) {
    throw new Error('update 的 DSL id 与目标报表块不一致')
  }
  return target
}

export function assertVmHermesOperationAllowed(action) {
  if (action === 'removeBlock') {
    throw new Error('Hermes 响应不允许删除报表块，请使用前端删除按钮')
  }
  if (ALLOWED_OPERATION_TYPES.indexOf(action) === -1) {
    if (action === 'patchBlock') throw new Error('patchBlock 已禁用，请返回完整 replaceBlock')
    throw new Error('不支持的操作：' + action)
  }
  return action
}

function assertCreateTargetIsNew(block, options = {}) {
  const blocks = Array.isArray(options.reportBlocks) ? options.reportBlocks : []
  const blockId = block && block.blockId
  const dslId = block && block.dsl && block.dsl.id
  const collision = blocks.find(item => item && (
    item.blockId === blockId ||
    item.blockId === dslId ||
    item.dsl && (item.dsl.id === dslId || item.dsl.id === blockId)
  ))
  if (collision) {
    throw new Error('create ID 已存在，不允许覆盖已有报表块：' + collision.blockId)
  }
  return block
}

function isVmReportDslPayload(payload) {
  return payload &&
    typeof payload === 'object' &&
    !Array.isArray(payload) &&
    payload.action &&
    payload.id &&
    Array.isArray(payload.requests) &&
    payload.transform &&
    payload.view
}

function buildOperationFromDsl(dsl, options = {}) {
  const target = dsl.action === 'update' ? resolveUpdateTarget(dsl, options) : null
  const block = createVmReportBlock({
    title: dsl.view && dsl.view.title || options.title,
    dsl
  }, target ? {
    enforceUpdateContext: true,
    validationContext: {
      currentId: target.dsl.id,
      currentDsl: target.dsl
    }
  } : {})
  if (dsl.action === 'create') assertCreateTargetIsNew(block, options)
  return {
    action: dsl.action === 'update' ? 'replaceBlock' : 'appendBlock',
    targetBlockId: target ? target.blockId : '',
    block
  }
}

function assertUniqueUpdateTargets(operations) {
  const targets = new Set()
  operations.forEach(operation => {
    if (!operation || operation.action !== 'replaceBlock') return
    if (targets.has(operation.targetBlockId)) {
      throw new Error('批量 update 不得重复更新同一个报表块：' + operation.targetBlockId)
    }
    targets.add(operation.targetBlockId)
  })
  return operations
}

export function parseVmHermesRenderPayload(content, options = {}) {
  const diagnostics = inspectJsonExtraction(content)
  const jsonText = diagnostics.repairedJson
  if (!jsonText || (jsonText[0] !== '{' && jsonText[0] !== '[')) {
    writeVmDebugFile({
      traceId: options.traceId || '',
      stage: options.stage || 'protocol.parse',
      status: 'missing-json',
      content,
      normalizedContent: diagnostics.normalizedContent,
      extractedJson: diagnostics.extractedJson,
      repairedJson: diagnostics.repairedJson
    })
    return {
      intent: 'chat',
      renderType: 'chat',
      message: trimTrailingAnchorText(String(content || '')).trim(),
      raw: {
        content: trimTrailingAnchorText(String(content || '')).trim()
      }
    }
  }
  let payload
  try {
    payload = JSON.parse(jsonText)
  } catch (error) {
    writeVmDebugFile({
      traceId: options.traceId || '',
      stage: options.stage || 'protocol.parse',
      status: 'parse-error',
      content,
      normalizedContent: diagnostics.normalizedContent,
      extractedJson: diagnostics.extractedJson,
      repairedJson: diagnostics.repairedJson,
      parseError: error && error.message ? error.message : String(error || '')
    })
    throw new Error('vmChat JSON 解析失败：' + error.message)
  }
  if (options.logSuccess) {
    writeVmDebugFile({
      traceId: options.traceId || '',
      stage: options.stage || 'protocol.parse',
      status: 'parse-success',
      content,
      normalizedContent: diagnostics.normalizedContent,
      extractedJson: diagnostics.extractedJson,
      repairedJson: diagnostics.repairedJson
    })
  }
  if (Array.isArray(payload)) {
    if (!options.allowBatchUpdate) {
      throw new Error('用户未明确要求批量修改全部模块，不允许返回 DSL 数组')
    }
    const operations = assertUniqueUpdateTargets(payload.map(item => {
      if (!isVmReportDslPayload(item)) throw new Error('DSL 数组项必须是完整 vm-report-dsl')
      if (item.action !== 'update') throw new Error('DSL 数组中的每一项都必须是 update')
      return buildOperationFromDsl(item, options)
    }))
    return {
      intent: 'report',
      renderType: 'report',
      message: '',
      raw: clone(payload),
      operations
    }
  }

  if (isVmReportDslPayload(payload)) {
    return {
      intent: 'report',
      renderType: 'report',
      message: '',
      raw: clone(payload),
      operations: [buildOperationFromDsl(payload, options)]
    }
  }

  const protocolPreamble = extractProtocolPreamble(diagnostics.normalizedContent, diagnostics.extractedJson)
  const nonReportPayload = normalizeNonReportPayload(payload, {
    thinking: protocolPreamble ? 'Hermes 检索说明：\n\n' + protocolPreamble : ''
  })
  if (nonReportPayload) return nonReportPayload

  throw new Error('Hermes JSON 响应只能是完整 vm-report-dsl 或规范的 chat/clarify/businessInfo')
}

export function extractAssistantContent(response) {
  const firstChoice = response && response.choices && response.choices[0] || {}
  if (firstChoice.message && typeof firstChoice.message.content === 'string') return firstChoice.message.content
  if (typeof firstChoice.text === 'string') return firstChoice.text
  return ''
}
