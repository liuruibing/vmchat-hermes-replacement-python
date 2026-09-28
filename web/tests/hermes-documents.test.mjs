import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const originalWindow = global.window
const originalReadableStream = global.ReadableStream
const originalTextDecoder = global.TextDecoder

const storage = {
  values: {},
  getItem(key) {
    return Object.prototype.hasOwnProperty.call(this.values, key) ? this.values[key] : null
  },
  setItem(key, value) {
    this.values[key] = String(value)
  },
  removeItem(key) {
    delete this.values[key]
  }
}

const calls = []
const encoder = new TextEncoder()

global.window = {
  localStorage: storage,
  fetch: async (url, options) => {
    calls.push({ url, options: options || {} })
    if (String(url).endsWith('/v1/runs')) {
      return {
        ok: true,
        status: 200,
        json: async () => ({ run_id: 'run-document-1' }),
        text: async () => ''
      }
    }
    if (String(url).endsWith('/v1/runs/run-document-1/events')) {
      return {
        ok: true,
        status: 200,
        body: new ReadableStream({
          start(controller) {
            controller.enqueue(encoder.encode('data: {"event":"message.delta","delta":"# 风险指标匹配报告"}\n\n'))
            controller.enqueue(encoder.encode('data: {"event":"run.completed","output":"# 风险指标匹配报告"}\n\n'))
            controller.close()
          }
        }),
        text: async () => ''
      }
    }
    throw new Error('unexpected URL ' + url)
  }
}

const { sendMandateRiskDocumentRun } = loadVmSource('../src/api/hermesDocuments.js')
const result = await sendMandateRiskDocumentRun({
  documentId: 'doc_abc123',
  question: '分析这个投资策略',
  sessionId: 'session-1',
  model: 'deepseek-v4-flash'
})

assert.strictEqual(result.content, '# 风险指标匹配报告')
assert.strictEqual(calls.length, 2)
const runRequest = calls[0]
assert.strictEqual(runRequest.url, '/hermes-api/v1/runs')
const payload = JSON.parse(runRequest.options.body)
assert.strictEqual(payload.agent_id, 'mandate-risk-ai')
assert.strictEqual(payload.role_id, 'risk-analyst')
assert.deepStrictEqual(payload.documents, ['doc_abc123'])
assert.strictEqual(payload.session_id, 'session-1')
assert.strictEqual(payload.input[0].content, '分析这个投资策略')
assert.strictEqual(calls[1].url, '/hermes-api/v1/runs/run-document-1/events')

if (originalWindow === undefined) delete global.window
else global.window = originalWindow
if (originalReadableStream !== undefined) global.ReadableStream = originalReadableStream
if (originalTextDecoder !== undefined) global.TextDecoder = originalTextDecoder

console.log('Hermes document run contract checks passed')
