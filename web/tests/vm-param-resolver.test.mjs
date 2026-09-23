import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'
import { executeTransformForTest } from './vm-transform-test-executor.mjs'

const {
  createVmParamResolver,
  normalizeVmBenchmarkOptions,
  normalizeVmDataFrequencyOptions
} = loadVmSource('../src/views/vmChat/vm-param-resolver.js')
const { createVmDictionaryLoaderCore } = loadVmSource('../src/views/vmChat/vm-dictionary-loader.js')
const { createVmReportBlock } = loadVmSource('../src/views/vmChat/vm-chat-helpers.js')
const { assertVmUpdateHydrationSucceeded, hydrateVmBlock } = loadVmSource('../src/views/vmChat/vm-block-hydrator.js')

const benchmarkOptions = [
  { label: '沪深300指数', code: '000300' },
  { label: '中证2000', code: '932000' }
]
const dataFrequencyOptions = [
  { label: '日频', code: '1' },
  { label: '周频', code: '2' },
  { label: '月频', code: '3' }
]
assert.deepStrictEqual(normalizeVmBenchmarkOptions([
  { DIM_NME: '沪深300指数', DIM_CDE: '000300' }
]), [{ label: '沪深300指数', code: '000300' }])
assert.deepStrictEqual(normalizeVmDataFrequencyOptions([
  { dimNme: '月频', dimCde: '3', dimStatus: '1', dimOrd: 3 },
  { dimNme: '已停用', dimCde: '9', dimStatus: '0', dimOrd: 1 },
  { dimNme: '日频', dimCde: '1', dimStatus: '1', dimOrd: 1 }
]), [
  { label: '日频', code: '1' },
  { label: '月频', code: '3' }
])
let benchmarkLoads = 0
let frequencyLoads = 0
const resolver = createVmParamResolver({
  async getBenchmarkOptions() {
    benchmarkLoads += 1
    return benchmarkOptions
  },
  async getDataFrequencyOptions() {
    frequencyLoads += 1
    return dataFrequencyOptions
  }
})

const semanticParams = {
  fundCode: 'SM0513',
  beginDate: '20220101',
  endDate: '20220131',
  dataFreqOpen: 'true',
  benchmarks: '1',
  benchmarkA: '沪深300',
  dataFreq: '日频'
}

const resolved = await resolver(semanticParams)
assert.strictEqual(resolved.benchmarkA, '000300')
assert.strictEqual(resolved.dataFreq, '1')
assert.strictEqual(semanticParams.benchmarkA, '沪深300')
assert.strictEqual(semanticParams.dataFreq, '日频')

const resolvedCodeInput = await resolver(Object.assign({}, semanticParams, {
  benchmarkA: '932000',
  dataFreq: '2'
}))
assert.strictEqual(resolvedCodeInput.benchmarkA, '932000')
assert.strictEqual(resolvedCodeInput.dataFreq, '2')
assert.strictEqual(benchmarkLoads, 1)
assert.strictEqual(frequencyLoads, 1)

const composite = await resolver(Object.assign({}, semanticParams, {
  benchmarks: '2',
  benchmarkB: '中证2000'
}))
assert.strictEqual(composite.benchmarkA, '000300')
assert.strictEqual(composite.benchmarkB, '932000')

const noBenchmark = await resolver(Object.assign({}, semanticParams, {
  benchmarks: '0'
}))
assert.strictEqual(noBenchmark.dataFreq, '1')
assert.strictEqual(benchmarkLoads, 1)

await assert.rejects(
  () => resolver(Object.assign({}, semanticParams, { benchmarkA: '不存在的基准' })),
  /未在当前字典中找到/
)

const ambiguousResolver = createVmParamResolver({
  getBenchmarkOptions: async () => [
    { label: '测试指数', code: 'A' },
    { label: '测试', code: 'B' }
  ],
  getDataFrequencyOptions: async () => dataFrequencyOptions
})
await assert.rejects(
  () => ambiguousResolver(Object.assign({}, semanticParams, { benchmarkA: '测试' })),
  /匹配到多个代码/
)

const dsl = {
  action: 'create',
  id: '550e8400-e29b-41d4-a716-446655440000',
  params: semanticParams,
  requests: [{
    id: 'stock',
    moduleId: 'stockExposureTiming',
    sqlCode: '712b930b-87a5-4cba-8da0-3671d4c8dc54'
  }],
  transform: {
    language: 'javascript',
    function: 'function transform(responses) { var rows = responses.stock && responses.stock.body || []; return rows.map(function (row) { return { value: row.VALUE }; }); }'
  },
  view: {
    type: 'table',
    title: '参数解析测试',
    columns: [{ field: 'value', label: '值', format: { type: 'raw' } }]
  }
}
const block = createVmReportBlock({ dsl })
let businessRequestCount = 0
const hydrated = await hydrateVmBlock(block, async requestSpec => {
  businessRequestCount += 1
  assert.strictEqual(requestSpec.params.benchmarkA, '000300')
  assert.strictEqual(requestSpec.params.dataFreq, '1')
  return { body: [{ VALUE: 1 }] }
}, { paramResolver: resolver, transformExecutor: executeTransformForTest })
assert.strictEqual(hydrated.renderState.status, 'ready')
assert.strictEqual(hydrated.dsl.params.benchmarkA, '沪深300')
assert.strictEqual(hydrated.sourceData.runtime.resolvedParams.benchmarkA, '000300')
assert.strictEqual(businessRequestCount, 1)

const failed = await hydrateVmBlock(
  createVmReportBlock({
    dsl: Object.assign({}, dsl, {
      id: '11111111-1111-4111-8111-111111111111',
      params: Object.assign({}, semanticParams, { benchmarkA: '不存在的基准' })
    })
  }),
  async () => {
    businessRequestCount += 1
    return { body: [] }
  },
  { paramResolver: resolver }
)
assert.strictEqual(failed.renderState.status, 'error')
assert.match(failed.renderState.errorMessage, /未在当前字典中找到/)

let liveBenchmarkLoads = 0
let publishedBenchmarkOptions = []
const liveDictionaryLoader = createVmDictionaryLoaderCore({
  async fetchBenchmarkOptions() {
    liveBenchmarkLoads += 1
    return benchmarkOptions
  },
  async fetchDataFrequencyOptions() {
    return dataFrequencyOptions
  },
  publishBenchmarkOptions(options) {
    publishedBenchmarkOptions = options
  }
})
const zeroTtlResolver = createVmParamResolver(Object.assign({}, liveDictionaryLoader, { cacheTtlMs: 0 }))
await zeroTtlResolver(semanticParams)
await zeroTtlResolver(semanticParams)
assert.strictEqual(liveBenchmarkLoads, 2)
assert.deepStrictEqual(publishedBenchmarkOptions, benchmarkOptions)
assert.strictEqual(businessRequestCount, 1)

const retryOperation = { action: 'replaceBlock', targetBlockId: block.blockId, block }
let updateHydrationError = null
try {
  assertVmUpdateHydrationSucceeded(failed, retryOperation)
} catch (error) {
  updateHydrationError = error
}
assert.ok(updateHydrationError)
assert.strictEqual(updateHydrationError.code, 'VM_UPDATE_HYDRATION_FAILED')
assert.strictEqual(updateHydrationError.retryOperation, retryOperation)
assert.match(updateHydrationError.message, /已保留原报表块/)
assert.strictEqual(assertVmUpdateHydrationSucceeded(hydrated, retryOperation), hydrated)

const missingResolver = await hydrateVmBlock(block, async () => ({ body: [] }))
assert.strictEqual(missingResolver.renderState.status, 'error')
assert.match(missingResolver.renderState.errorMessage, /未配置动态参数解析器/)

console.log('vm parameter resolver checks passed')
