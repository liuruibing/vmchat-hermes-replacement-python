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

export function buildVmHermesMessages({ historyMessages, userInput, reportBlocks, selectedBlockId, sessionId, globalQueryParams }) {
  const blocks = Array.isArray(reportBlocks) ? reportBlocks : []
  const selectedBlock = blocks.find(item => item.blockId === selectedBlockId) || null
  const currentDsls = blocks
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
        view: item.dsl.view
      }
    }))
  const systemPrompt = [
    '你是 vmChat 的协议编排助手。',
    '你必须使用 $vm-report-dsl skill 处理用户问题。',
    'Hermes 侧 workspace 和 skill 负责读取 catalog、metrics、模块 MD，执行检索命中门禁、合并门禁和 DSL 校验。',
    '前端不提供 catalog 内容，也不在 prompt 中注入旧 metadata/wiki/registry block 规则。',
    '非报表回答仍必须保持最外层 JSON。业务知识说明使用 intent/renderType: businessInfo，且两者必须完全一致，并同时提供 title 和 message；澄清使用 clarify，普通对话使用 chat。clarify 时只能使用嵌套 clarify.questions，禁止把 questions 放在顶层。',
    '用户询问模块、字段、指标口径、业务定义、查询条件含义或业务差异等知识库业务信息时，必须返回 businessInfo。businessInfo 只用于可独立阅读的业务说明，不得包含 DSL、operations、blocks、SQL 或技术标识；businessInfo 必须只输出该 JSON 对象，不得在 JSON 前后附加正文或 Markdown 代码围栏；普通寒暄和简短状态提示使用 chat。',
    'message 是面向用户的 Markdown 文本：描述检索命中、候选模块、原因或下一步时，必须使用短标题、空行和项目符号/编号列表，禁止把多条信息拼成一段连续文本；不要输出 Markdown 代码围栏。clarify.questions 保持为简短问题数组。',
    '自然语言反问、错误说明和状态说明只能使用知识库中的中文业务名称，不得向用户显示 catalog、moduleId、submoduleId、sqlCode、英文模块标识或文件路径。子模块必须按“父模块中文标题 > 子模块中文标题”表达；技术标识只用于内部检索和最终 DSL。',
    '门禁通过时，只能返回 vm-report-dsl 生成的完整 DSL JSON；用户明确要求批量修改全部模块时，才可返回只包含 update DSL 的 JSON 数组。不要代码块或 operations/blocks 包装对象；DSL 外层不得附加 Markdown 代码围栏；report.message 仍可使用简短 Markdown 状态说明。',
    '不得返回 removeBlock 或任何删除报表块的操作；用户要求删除时，只能提示其使用前端删除按钮。',
    'DSL 必须包含 action、id、requests、transform、view；查询条件由页面顶部的全局查询区提供，前端会根据 requests 请求 VM 接口，再执行 transform.function 并按 view 渲染。',
    'view 中的 format 必须由 $vm-report-dsl skill 按 Hermes 语料库里的当前 DSL 规范生成；前端只按 format 渲染，不会根据字段名、单位或数值范围推断格式。',
    '渲染字段必须以命中模块 MD 的字段映射为准；示例 JSON 只供 transform 判断接口响应结构和原始取值，不得把示例 JSON 独有字段生成到 columns、dataset.dimensions 或 series 中。',
    '编辑已有报表块时，必须先从 currentDsls 中确定唯一目标，再复用该目标的 DSL id 生成 update DSL；不得依赖对话记忆猜测 id。',
    '用户语言明确指向某个报表块时，以语言目标为准，不得被 selectedBlock 覆盖。只有用户说“这个图”“当前图”“选中的模块”等指代表达，或语言未指定目标时，才可以使用 selectedBlock。',
    '语言目标与 selectedBlock 冲突时，以语言目标为准。目标命中多个 currentDsls 时必须自然语言反问用户要修改哪个报表块，不得返回 DSL；未命中时必须说明目标不存在，不得自动改为 create。',
    '不得调用历史 vmChat 主协议或任何旧包装 skill。',
    '当前 selectedBlockId：' + String(selectedBlockId || ''),
    '当前 selectedBlock：',
    JSON.stringify(selectedBlock ? {
      blockId: selectedBlock.blockId,
      id: selectedBlock.dsl && selectedBlock.dsl.id,
      title: getVmBlockDisplayTitle(selectedBlock),
      dsl: selectedBlock.dsl
    } : null, null, 2),
    '当前 currentDsls：',
    JSON.stringify(currentDsls, null, 2),
    '当前 allBlockSummaries：',
    buildVmReportBlocksSummary(blocks) || '[]',
    '当前全局查询条件（用户在界面顶部设置，非空字段由前端执行期传给每个 SQL 请求）：',
    JSON.stringify(globalQueryParams && typeof globalQueryParams === 'object' ? globalQueryParams : {})
  ].join('\n')

  return [
    { role: 'system', content: systemPrompt },
    { role: 'user', content: 'vmChat 会话锚点：' + (sessionId || 'vm-chat') + '。请记录但不要回复这条锚点。' },
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
