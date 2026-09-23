import assert from 'assert'
import http from 'http'
import https from 'https'
import { loadVmSource } from './load-vm-source.mjs'
import { executeTransformForTest } from './vm-transform-test-executor.mjs'

const { createVmParamResolver, normalizeVmBenchmarkOptions, normalizeVmDataFrequencyOptions } = loadVmSource('../src/views/vmChat/vm-param-resolver.js')
const { assertVmBusinessSuccess } = loadVmSource('../src/views/vmChat/vm-api-response.js')
const { createVmDslReportBlock, hydrateVmDslReportBlock } = loadVmSource('../src/views/vmChat/vm-report-dsl-runtime.js')
const { validateVmReportDsl } = loadVmSource('../src/views/vmChat/vm-report-dsl-validator.js')

if (process.env.VM_CHAT_LIVE_E2E !== '1') {
  console.log('跳过 vmChat 真实链路测试：设置 VM_CHAT_LIVE_E2E=1 后运行')
  process.exit(0)
}

const apiBaseUrl = String(process.env.VM_CHAT_API_BASE_URL || '').replace(/\/$/, '')
const apiToken = String(process.env.VM_CHAT_API_TOKEN || '')
const hermesUrl = String(process.env.VM_CHAT_HERMES_URL || 'http://127.0.0.1:8642/v1/chat/completions')
const hermesModel = String(process.env.VM_CHAT_HERMES_MODEL || 'vm-report-template')
const hermesApiKey = String(process.env.VM_CHAT_HERMES_API_KEY || '')

assert.ok(apiBaseUrl, 'VM_CHAT_API_BASE_URL 不能为空')
assert.ok(apiToken, 'VM_CHAT_API_TOKEN 不能为空')

function joinUrl(base, path) {
  return base.replace(/\/$/, '') + '/' + path.replace(/^\//, '')
}

function authHeaders(extra = {}) {
  return Object.assign({ Authorization: apiToken }, extra)
}

function extractJson(text) {
  const source = String(text || '').trim()
  const fenced = source.match(/```(?:json)?\s*([\s\S]*?)\s*```/i)
  return JSON.parse(fenced ? fenced[1] : source)
}

function requestJson(url, options, displayName, timeoutMs) {
  return new Promise((resolve, reject) => {
    const target = new URL(url)
    const transport = target.protocol === 'https:' ? https : http
    const requestOptions = Object.assign({}, options || {})
    const body = requestOptions.body === undefined ? '' : String(requestOptions.body)
    delete requestOptions.body
    const request = transport.request(target, requestOptions, response => {
      const chunks = []
      response.on('data', chunk => chunks.push(Buffer.from(chunk)))
      response.on('end', () => {
        const text = Buffer.concat(chunks).toString('utf8')
        const status = Number(response.statusCode || 0)
        if (status < 200 || status >= 300) {
          reject(new Error(displayName + ' HTTP 失败：' + status + ' ' + text.slice(0, 300)))
          return
        }
        try {
          resolve(JSON.parse(text))
        } catch (error) {
          reject(new Error(displayName + '没有返回 JSON'))
        }
      })
    })
    request.setTimeout(timeoutMs, () => request.destroy(new Error(displayName + '请求超时')))
    request.on('error', reject)
    if (body) request.write(body)
    request.end()
  })
}

const hermesHeaders = { 'content-type': 'application/json' }
if (hermesApiKey) hermesHeaders.Authorization = 'Bearer ' + hermesApiKey
const hermesPayload = await requestJson(hermesUrl, {
  method: 'POST',
  headers: hermesHeaders,
  body: JSON.stringify({
    model: hermesModel,
    stream: false,
    messages: [{
      role: 'user',
      content: 'SM0513 在 2022-01-01 到 2022-01-31 的股票净敞口时序全部指标，用沪深300单基准、日频。直接返回最终 DSL。'
    }]
  })
}, 'Hermes', 180000)
const dslText = hermesPayload.choices && hermesPayload.choices[0] && hermesPayload.choices[0].message
  ? hermesPayload.choices[0].message.content
  : ''
const dsl = validateVmReportDsl(extractJson(dslText))
assert.strictEqual(dsl.params.benchmarkA, '沪深300')
assert.strictEqual(dsl.params.dataFreq, '日频')

async function fetchBusinessJson(url, options, displayName) {
  return assertVmBusinessSuccess(await requestJson(url, options, displayName, 60000), displayName)
}

const resolver = createVmParamResolver({
  async getBenchmarkOptions() {
    const payload = await fetchBusinessJson(
      joinUrl(apiBaseUrl, '/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d'),
      {
        method: 'POST',
        headers: authHeaders({ 'content-type': 'application/json' }),
        body: JSON.stringify({ indexCode: 'd43c924b-eebd-4d8f-97e5-ed46b609456d' })
      },
      '基准字典'
    )
    return normalizeVmBenchmarkOptions(payload.data)
  },
  async getDataFrequencyOptions() {
    const payload = await fetchBusinessJson(
      joinUrl(apiBaseUrl, '/api/common/edim/DATAFREQ'),
      { method: 'GET', headers: authHeaders() },
      '频率字典'
    )
    return normalizeVmDataFrequencyOptions(payload.data)
  },
  cacheTtlMs: 0
})

const block = createVmDslReportBlock({ dsl })
const hydrated = await hydrateVmDslReportBlock(block, async requestSpec => {
  const url = new URL(joinUrl(apiBaseUrl, '/rest/report/getSqlDataBySqlCode.do'))
  Object.entries(Object.assign({ sqlCode: requestSpec.sqlCode }, requestSpec.params || {}))
    .forEach(([key, value]) => url.searchParams.set(key, value))
  return fetchBusinessJson(url.toString(), { method: 'GET', headers: authHeaders() }, 'VM SQL')
}, {
  paramResolver: resolver,
  transformExecutor: executeTransformForTest
})

assert.strictEqual(hydrated.renderState.status, 'ready', hydrated.renderState.errorMessage)
assert.ok(hydrated.sourceData.runtime.resolvedParams)
assert.notStrictEqual(hydrated.sourceData.runtime.resolvedParams.benchmarkA, '沪深300')
assert.notStrictEqual(hydrated.sourceData.runtime.resolvedParams.dataFreq, '日频')
if (dsl.view.type === 'table') {
  assert.ok(Array.isArray(hydrated.renderSpec.rows))
} else {
  assert.ok(hydrated.renderSpec.option)
  assert.ok(Array.isArray(hydrated.renderSpec.option.dataset.source))
}

console.log('vmChat 真实 E2E 通过：自然语言 → Hermes → DSL 校验 → 实时字典 → SQL → transform → renderSpec')
