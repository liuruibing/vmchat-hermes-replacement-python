import {
  buildHermesAuthHeaders,
  buildHermesRequestUrl,
  DEFAULT_HERMES_ANALYSIS_MODEL
} from './hermesResearch'

const DEFAULT_DOCUMENT_PROMPT = '请分析这个投资策略，并严格从风险指标库中匹配适配的风险指标。'

function normalizeHttpError(response, fallback) {
  return response.text().then(text => {
    let message = text
    try {
      const payload = text ? JSON.parse(text) : null
      message = payload && (payload.error || payload.message) || text
    } catch (error) {
      // Keep the raw response as the diagnostic message.
    }
    const next = new Error(message || fallback || ('HTTP ' + response.status))
    next.status = response.status
    return next
  })
}

export async function uploadHermesPdfDocument(file) {
  const rawFile = file && (file.raw || file)
  if (!rawFile) throw new Error('请选择 PDF 文件')
  const filename = String(rawFile.name || '').trim()
  const mimeType = String(rawFile.type || '').toLowerCase()
  if (!/\.pdf$/i.test(filename) || mimeType && mimeType !== 'application/pdf' && mimeType !== 'application/x-pdf') {
    throw new Error('当前只支持 PDF 文件')
  }

  const formData = new FormData()
  formData.append('file', rawFile, filename || 'document.pdf')
  const response = await window.fetch(buildHermesRequestUrl('/v1/documents'), {
    method: 'POST',
    headers: buildHermesAuthHeaders(),
    body: formData
  })
  if (!response.ok) throw await normalizeHttpError(response, 'PDF 上传失败')
  const payload = await response.json()
  if (!payload || !payload.document || !payload.document.document_id) {
    throw new Error('PDF 上传成功，但服务端没有返回 document_id')
  }
  return payload.document
}

function dispatchRunEvent(frame, state, handlers) {
  const lines = String(frame || '').split(/\r?\n/)
  const dataLines = lines
    .filter(line => /^data:/.test(line))
    .map(line => line.replace(/^data:\s?/, ''))
  if (!dataLines.length) return

  let payload
  try {
    payload = JSON.parse(dataLines.join('\n'))
  } catch (error) {
    return
  }
  const eventName = String(payload.event || '')
  if (handlers && handlers.onEvent) handlers.onEvent(payload)
  if (eventName === 'reasoning.delta') {
    const delta = String(payload.delta || '')
    state.thinking += delta
    if (delta && handlers && handlers.onThinking) handlers.onThinking(delta, state.thinking)
    return
  }
  if (eventName === 'message.delta') {
    const delta = String(payload.delta || '')
    state.content += delta
    if (delta && handlers && handlers.onContent) handlers.onContent(delta, state.content)
    return
  }
  if (eventName === 'run.completed') {
    state.completed = true
    if (typeof payload.output === 'string' && payload.output) state.content = payload.output
    state.usage = payload.usage || {}
    return
  }
  if (eventName === 'run.failed') {
    const error = new Error(String(payload.error || 'AI 风险指标分析失败'))
    error.code = 'HERMES_RUN_FAILED'
    throw error
  }
}

async function streamRunEvents(runId, handlers) {
  const response = await window.fetch(
    buildHermesRequestUrl('/v1/runs/' + encodeURIComponent(runId) + '/events'),
    { headers: buildHermesAuthHeaders({ Accept: 'text/event-stream' }) }
  )
  if (!response.ok) throw await normalizeHttpError(response, 'AI 风险指标分析失败')
  if (!response.body || !response.body.getReader) {
    throw new Error('当前浏览器不支持 Hermes 流式响应')
  }

  const state = { content: '', thinking: '', completed: false, usage: {} }
  const reader = response.body.getReader()
  const decoder = new TextDecoder('utf-8')
  let buffer = ''
  try {
    while (true) {
      const result = await reader.read()
      if (result.done) break
      buffer += decoder.decode(result.value, { stream: true })
      const frames = buffer.split(/\r?\n\r?\n/)
      buffer = frames.pop() || ''
      for (const frame of frames) {
        if (!String(frame || '').trim() || /^:\s*keep-alive/m.test(frame)) continue
        dispatchRunEvent(frame, state, handlers)
      }
    }
    buffer += decoder.decode()
    if (buffer.trim() && !/^:\s*keep-alive/m.test(buffer)) {
      dispatchRunEvent(buffer, state, handlers)
    }
  } finally {
    reader.releaseLock()
  }
  if (!state.completed && !state.content) {
    throw new Error('AI 风险指标分析未返回有效结果')
  }
  return state
}

export async function sendMandateRiskDocumentRun(options, handlers) {
  const documentId = String(options && options.documentId || '').trim()
  if (!documentId) throw new Error('documentId 不能为空')
  const question = String(options && options.question || '').trim() || DEFAULT_DOCUMENT_PROMPT
  const sessionId = String(options && options.sessionId || 'mandate-risk-ai')
  const model = String(options && options.model || DEFAULT_HERMES_ANALYSIS_MODEL)

  const response = await window.fetch(buildHermesRequestUrl('/v1/runs'), {
    method: 'POST',
    headers: buildHermesAuthHeaders({ 'Content-Type': 'application/json;charset=UTF-8' }),
    body: JSON.stringify({
      model,
      input: [{ role: 'user', content: question }],
      instructions: '',
      session_id: sessionId,
      agent_id: 'mandate-risk-ai',
      role_id: 'risk-analyst',
      documents: [documentId]
    })
  })
  if (!response.ok) throw await normalizeHttpError(response, '创建风险指标分析任务失败')
  const payload = await response.json()
  const runId = String(payload && payload.run_id || '').trim()
  if (!runId) throw new Error('服务端没有返回 run_id')
  return streamRunEvents(runId, handlers)
}

export { DEFAULT_DOCUMENT_PROMPT }
