import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const { executeVmQueryPlan } = loadVmSource('../src/views/vmChat/vm-query-executor.js')

const netValPayload = {
  head: {
    constrasCodeColumn: [],
    benchmarks: '',
    constrasCodeNames: [],
    dataFreq: 'day',
    benchName: ''
  },
  body: [
    {
      VC_DATE: '2022-01-04',
      FCODE: 'SM0513',
      BYEILD_PROD: 0.964,
      FCNAV: 0.964,
      TDATE: '20220104',
      FNAV: 0.964
    },
    {
      VC_DATE: '2022-01-05',
      FCODE: 'SM0513',
      BYEILD_PROD: 0.964,
      FCNAV: 0.972,
      TDATE: '20220105',
      FNAV: 0.972
    }
  ]
}

const hkIndustryPayload = [
  {
    XAXISDATA: '23',
    YAXISDATA1: '非必需性消费',
    YAXISDATA2: '-3227659.11',
    YAXISDATA3: '84.5083',
    YAXISDATA4: '12.3467',
    ROW_ID: 1
  }
]

const result = await executeVmQueryPlan({
  requests: [
    {
      requestId: 'q1',
      moduleKey: 'netValMonitor',
      sqlCode: 'sample-1'
    },
    {
      requestId: 'q2',
      moduleKey: 'tenLossHKIndustry',
      sqlCode: 'sample-2'
    }
  ]
}, async requestSpec => {
  if (requestSpec.requestId === 'q1') return netValPayload
  if (requestSpec.requestId === 'q2') return hkIndustryPayload
  return []
})

assert.strictEqual(result.requestCount, 2)
assert.strictEqual(result.totalRows, 3)
assert.strictEqual(result.rowsByRequestId.q1.length, 2)
assert.strictEqual(result.rowsByRequestId.q1[0].VC_DATE, '2022-01-04')
assert.strictEqual(result.rowsByRequestId.q2.length, 1)
assert.strictEqual(result.rowsByRequestId.q2[0].XAXISDATA, '23')

let callCount = 0
let activeCount = 0
let maxActiveCount = 0
const parallelResult = await executeVmQueryPlan({
  requests: [
    {
      requestId: 'dupA',
      moduleKey: 'productInfo',
      sqlCode: 'same-sql',
      params: { fundCode: 'SM0513', beginDate: '2022-01-01' }
    },
    {
      requestId: 'dupB',
      moduleKey: 'productInfo',
      sqlCode: 'same-sql',
      params: { beginDate: '2022-01-01', fundCode: 'SM0513' }
    },
    {
      requestId: 'other',
      moduleKey: 'overallEvalua_base',
      sqlCode: 'other-sql',
      params: { fundCode: 'SM0513' }
    }
  ]
}, async requestSpec => {
  callCount += 1
  activeCount += 1
  maxActiveCount = Math.max(maxActiveCount, activeCount)
  await new Promise(resolve => setTimeout(resolve, 20))
  activeCount -= 1
  return {
    body: [{
      requestId: requestSpec.requestId,
      sqlCode: requestSpec.sqlCode
    }]
  }
})

assert.strictEqual(callCount, 2)
assert.strictEqual(maxActiveCount, 2)
assert.strictEqual(parallelResult.requestCount, 3)
assert.strictEqual(parallelResult.uniqueRequestCount, 2)
assert.strictEqual(parallelResult.dataMode, 'live')
assert.strictEqual(parallelResult.rowsByRequestId.dupA.length, 1)
assert.strictEqual(parallelResult.rowsByRequestId.dupB.length, 1)
assert.strictEqual(parallelResult.rowsByRequestId.dupA[0].sqlCode, 'same-sql')
assert.strictEqual(parallelResult.rowsByRequestId.dupB[0].sqlCode, 'same-sql')
assert.strictEqual(parallelResult.timings.dupA.deduped, true)
assert.strictEqual(parallelResult.timings.dupB.deduped, true)
assert.strictEqual(parallelResult.timings.other.deduped, true)

const commodityPayload = {
  body: {
    YLData: [{ VC_FUT_DETAIL_NAME: '沪深300指数', VC_DIRECTION: '空头', F_INCOME: 119400, F_GXD: 0.3784, F_JZZB: -0.0012 }],
    KSData: [{ VC_FUT_DETAIL_NAME: '锡', VC_DIRECTION: '空头', F_INCOME: -2190780, F_GXD: 0.5404, F_JZZB: -0.2047 }]
  }
}
let commodityCallCount = 0
const commodityResult = await executeVmQueryPlan({
  requests: [
    {
      requestId: 'profit',
      moduleKey: 'commodityProfitLoss',
      submoduleId: 'topProfitCommodities',
      sqlCode: 'commodity-sql',
      params: { fundCode: 'SM0513' }
    },
    {
      requestId: 'loss',
      moduleKey: 'commodityProfitLoss',
      submoduleId: 'topLossCommodities',
      sqlCode: 'commodity-sql',
      params: { fundCode: 'SM0513' }
    }
  ]
}, async requestSpec => {
  commodityCallCount += 1
  assert.strictEqual(requestSpec.submoduleId, 'topProfitCommodities')
  return commodityPayload
})

assert.strictEqual(commodityCallCount, 1)
assert.strictEqual(commodityResult.requestCount, 2)
assert.strictEqual(commodityResult.uniqueRequestCount, 1)
assert.deepStrictEqual(commodityResult.payloadByRequestId.profit, commodityPayload)
assert.deepStrictEqual(commodityResult.payloadByRequestId.loss, commodityPayload)
assert.strictEqual(commodityResult.rowsByRequestId.profit.length, 0)
assert.strictEqual(commodityResult.rowsByRequestId.loss.length, 0)
assert.strictEqual(commodityResult.timings.profit.deduped, true)
assert.strictEqual(commodityResult.timings.loss.deduped, true)

let requestedDataMode = ''
const exampleModeResult = await executeVmQueryPlan({
  requests: [{
    requestId: 'example-mode',
    moduleKey: 'productInfo',
    sqlCode: 'example-sql'
  }]
}, async requestSpec => {
  requestedDataMode = requestSpec.dataMode
  return { body: [{ mode: requestSpec.dataMode }] }
}, { dataMode: 'example' })

assert.strictEqual(requestedDataMode, 'example')
assert.strictEqual(exampleModeResult.dataMode, 'example')
assert.strictEqual(exampleModeResult.rowsByRequestId['example-mode'][0].mode, 'example')

await assert.rejects(
  () => executeVmQueryPlan({
    requests: [{ requestId: 'failed', moduleKey: 'productInfo', sqlCode: 'failed-sql' }]
  }, async () => ({ status: -1, code: 'SQL_FAILED', message: 'SQL 执行失败' })),
  error => error.code === 'SQL_FAILED' && /SQL 执行失败/.test(error.message)
)

console.log('vm query executor response shape checks passed')
