import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'
import { executeTransformForTest } from './vm-transform-test-executor.mjs'

const { createVmReportBlock } = loadVmSource('../src/views/vmChat/vm-chat-helpers.js')
const { hydrateVmBlock } = loadVmSource('../src/views/vmChat/vm-block-hydrator.js')

const paramResolver = async params => Object.assign({}, params, {
  benchmarkA: params.benchmarkA === '沪深300' ? '000300' : params.benchmarkA,
  benchmarkB: params.benchmarkB === '沪深300' ? '000300' : params.benchmarkB,
  dataFreq: params.dataFreq === '日频' ? '1' : params.dataFreq
})

const tableDsl = {
  action: 'create',
  id: '550e8400-e29b-41d4-a716-446655440000',
  params: {
    fundCode: 'SM0513',
    beginDate: '20220101',
    endDate: '20220131',
    dataFreqOpen: 'true',
    benchmarks: '1',
    benchmarkA: '沪深300',
    dataFreq: '日频'
  },
  requests: [
    {
      id: 'profit',
      moduleId: 'tenProfitIndustry',
      sqlCode: 'fe842e36-d296-432d-8696-d6ec8f2aab03'
    }
  ],
  transform: {
    language: 'javascript',
    function: [
      'function transform(responses) {',
      '  var response = responses && responses.profit;',
      '  var rows = response && Array.isArray(response.body) ? response.body : [];',
      '  return rows.map(function (row) {',
      '    return {',
      '      securityCode: row.VC_SYMBOL,',
      '      income: row.F_INCOME',
      '    };',
      '  });',
      '}'
    ].join('\n')
  },
  view: {
    type: 'table',
    title: '盈利个股',
    columns: [
      { field: 'securityCode', label: '证券代码', format: { type: 'text', nullValue: '-' } },
      { field: 'income', label: '本期盈利', unit: '元', format: { type: 'decimal', digits: 2 } }
    ]
  }
}

const block = createVmReportBlock({
  title: '盈利个股',
  dsl: tableDsl
})

assert.strictEqual(block.blockId, '550e8400-e29b-41d4-a716-446655440000')
assert.strictEqual(block.viewType, 'table')
assert.strictEqual(block.title, '盈利个股')
assert.strictEqual(block.moduleKey, 'tenProfitIndustry')
assert.strictEqual(block.queryContext.fundCode, 'SM0513')

const hydrated = await hydrateVmBlock(block, async requestSpec => {
  assert.strictEqual(requestSpec.moduleKey, 'tenProfitIndustry')
  assert.strictEqual(requestSpec.sqlCode, 'fe842e36-d296-432d-8696-d6ec8f2aab03')
  assert.strictEqual(requestSpec.params.fundCode, 'SM0513')
  return {
    body: [
      { VC_SYMBOL: '600000', F_INCOME: 320000.12 }
    ]
  }
}, { paramResolver, transformExecutor: executeTransformForTest })

assert.strictEqual(hydrated.renderState.status, 'ready')
assert.strictEqual(hydrated.renderSpec.columns.length, 2)
assert.strictEqual(hydrated.renderSpec.rows.length, 1)
assert.strictEqual(hydrated.renderSpec.rows[0].securityCode, '600000')
assert.strictEqual(hydrated.renderSpec.rows[0].income, 320000.12)
assert.strictEqual(hydrated.sourceData.runtime.requestCount, 1)
assert.strictEqual(hydrated.sourceData.runtime.rowCounts.profit, 1)

let commodityCallCount = 0
const combinedCommodityBlock = createVmReportBlock({
  dsl: {
    action: 'create',
    id: '450e8400-e29b-41d4-a716-446655440000',
    params: {
      fundCode: 'SM0513',
      beginDate: '20220101',
      endDate: '20220131',
      dataFreqOpen: 'true',
      benchmarks: '1',
      benchmarkA: '沪深300',
      dataFreq: '日频'
    },
    requests: [
      {
        id: 'profit',
        moduleId: 'commodityProfitLoss',
        submoduleId: 'topProfitCommodities',
        sqlCode: 'b0a11b9d-5709-4c27-a0c0-57e859b2d9e8'
      },
      {
        id: 'loss',
        moduleId: 'commodityProfitLoss',
        submoduleId: 'topLossCommodities',
        sqlCode: 'b0a11b9d-5709-4c27-a0c0-57e859b2d9e8'
      }
    ],
    transform: {
      language: 'javascript',
      function: [
        'function transform(responses) {',
        '  var profitRows = responses && responses.profit && responses.profit.body && Array.isArray(responses.profit.body.YLData) ? responses.profit.body.YLData : [];',
        '  var lossRows = responses && responses.loss && responses.loss.body && Array.isArray(responses.loss.body.KSData) ? responses.loss.body.KSData : [];',
        '  function convert(row, type) {',
        '    return {',
        '      profitLossType: type,',
        '      commodityName: row.VC_FUT_DETAIL_NAME,',
        '      direction: row.VC_DIRECTION,',
        '      income: row.F_INCOME === null || row.F_INCOME === undefined ? null : Number(row.F_INCOME) / 10000,',
        '      contribution: row.F_GXD === null || row.F_GXD === undefined ? null : Number(row.F_GXD) * 100,',
        '      exposure: row.F_JZZB === null || row.F_JZZB === undefined ? null : Number(row.F_JZZB) * 100',
        '    };',
        '  }',
        "  return profitRows.map(function (row) { return convert(row, '盈利'); }).concat(lossRows.map(function (row) { return convert(row, '亏损'); }));",
        '}'
      ].join('\n')
    },
    view: {
      type: 'table',
      title: '期货十大盈利亏损品种',
      columns: [
        { field: 'profitLossType', label: '盈亏类型', format: { type: 'text', nullValue: '-' } },
        { field: 'commodityName', label: '期货品种', format: { type: 'text', nullValue: '-' } },
        { field: 'direction', label: '多空方向', format: { type: 'text', nullValue: '-' } },
        { field: 'income', label: '收益额', unit: '万元', format: { type: 'decimal', digits: 4 } },
        { field: 'contribution', label: '贡献度', unit: '%', format: { type: 'percentage', digits: 2, suffix: '%' } },
        { field: 'exposure', label: '期间平均风险暴露占净值比', unit: '%', format: { type: 'percentage', digits: 2, suffix: '%' } }
      ]
    }
  }
})

const hydratedCommodity = await hydrateVmBlock(combinedCommodityBlock, async requestSpec => {
  commodityCallCount += 1
  assert.strictEqual(requestSpec.moduleKey, 'commodityProfitLoss')
  assert.strictEqual(requestSpec.submoduleId, 'topProfitCommodities')
  return {
    body: {
      YLData: [{ VC_FUT_DETAIL_NAME: '沪深300指数', VC_DIRECTION: '空头', F_INCOME: 119400, F_GXD: 0.3784, F_JZZB: -0.0012 }],
      KSData: [{ VC_FUT_DETAIL_NAME: '锡', VC_DIRECTION: '空头', F_INCOME: -2190780, F_GXD: 0.5404, F_JZZB: -0.2047 }]
    }
  }
}, { paramResolver, transformExecutor: executeTransformForTest })

assert.strictEqual(commodityCallCount, 1)
assert.strictEqual(hydratedCommodity.renderState.status, 'ready')
assert.strictEqual(hydratedCommodity.renderSpec.rows.length, 2)
assert.strictEqual(hydratedCommodity.renderSpec.rows[0].profitLossType, '盈利')
assert.strictEqual(hydratedCommodity.renderSpec.rows[0].commodityName, '沪深300指数')
assert.strictEqual(hydratedCommodity.renderSpec.rows[0].income, 11.94)
assert.strictEqual(hydratedCommodity.renderSpec.rows[1].profitLossType, '亏损')
assert.strictEqual(hydratedCommodity.renderSpec.rows[1].commodityName, '锡')
assert.strictEqual(hydratedCommodity.renderSpec.rows[1].income, -219.078)
assert.strictEqual(hydratedCommodity.sourceData.runtime.requestCount, 2)
assert.strictEqual(hydratedCommodity.sourceData.runtime.uniqueRequestCount, 1)
assert.strictEqual(hydratedCommodity.sourceData.runtime.totalRows, 2)
assert.strictEqual(hydratedCommodity.sourceData.runtime.transformRowCount, 2)
assert.strictEqual(hydratedCommodity.sourceData.runtime.rowCounts.profit, 0)
assert.ok(hydratedCommodity.requestDiagnostics[0].detail.includes('已接收响应'))

const chartBlock = createVmReportBlock({
  dsl: {
    action: 'create',
    id: '6ba7b810-9dad-41d1-80b4-00c04fd430c8',
    params: {
      fundCode: 'SM0513',
      beginDate: '20220101',
      endDate: '20220131',
      dataFreqOpen: 'true',
      benchmarks: '1',
      benchmarkA: '沪深300',
      dataFreq: '日频'
    },
    requests: [
      {
        id: 'exp',
        moduleId: 'stockExposureTiming',
        sqlCode: '712b930b-87a5-4cba-8da0-3671d4c8dc54'
      },
      {
        id: 'cash',
        moduleId: 'cashPositionTiming',
        sqlCode: 'b9f4277e-2793-4a0d-b9ed-e665e4bbd717'
      }
    ],
    transform: {
      language: 'javascript',
      function: [
        'function transform(responses) {',
        '  var expResponse = responses && responses.exp;',
        '  var cashResponse = responses && responses.cash;',
        '  var expRows = expResponse && Array.isArray(expResponse.body) ? expResponse.body : [];',
        '  var cashRows = cashResponse && Array.isArray(cashResponse.body) ? cashResponse.body : [];',
        '  var rowsByDate = {};',
        '  expRows.forEach(function (row) {',
        '    var key = row.TDATE;',
        '    if (!rowsByDate[key]) rowsByDate[key] = { TDATE: key };',
        '    rowsByDate[key].stockExposure = row.F_STOCK_EXP === null || row.F_STOCK_EXP === undefined ? null : Number(row.F_STOCK_EXP) * 100;',
        '  });',
        '  cashRows.forEach(function (row) {',
        '    var key = row.TDATE;',
        '    if (!rowsByDate[key]) rowsByDate[key] = { TDATE: key };',
        '    rowsByDate[key].cashRatio = row.F_CASH_RATIO === null || row.F_CASH_RATIO === undefined ? null : Number(row.F_CASH_RATIO) * 100;',
        '  });',
        '  return Object.keys(rowsByDate).sort().map(function (key) {',
        '    var row = rowsByDate[key];',
        '    if (row.stockExposure === undefined) row.stockExposure = null;',
        '    if (row.cashRatio === undefined) row.cashRatio = null;',
        '    return row;',
        '  });',
        '}'
      ].join('\n')
    },
    view: {
      type: 'echarts',
      title: '股票净敞口与现金类仓位',
      legend: {
        show: true,
        data: ['股票净敞口', '现金类仓位']
      },
      dataset: {
        source: '$transform',
        dimensions: ['TDATE', 'stockExposure', 'cashRatio']
      },
      xAxis: { type: 'category', name: '日期' },
      yAxis: [
        { type: 'value', name: '股票净敞口' },
        { type: 'value', name: '现金类仓位' }
      ],
      series: [
        { name: '股票净敞口', type: 'line', yAxisIndex: 0, encode: { x: 'TDATE', y: 'stockExposure' }, format: { type: 'percentage', digits: 2, suffix: '%' } },
        { name: '现金类仓位', type: 'line', yAxisIndex: 1, encode: { x: 'TDATE', y: 'cashRatio' }, format: { type: 'percentage', digits: 4, suffix: '%' } }
      ]
    }
  }
})

const hydratedChart = await hydrateVmBlock(chartBlock, async requestSpec => {
  if (requestSpec.moduleKey === 'stockExposureTiming') {
    return {
      body: [
        { TDATE: '20220104', F_STOCK_EXP: 1.26 },
        { TDATE: '20220105', F_STOCK_EXP: 1.25 }
      ]
    }
  }
  return {
    body: [
      { TDATE: '20220104', F_CASH_RATIO: 0.0825 },
      { TDATE: '20220105', F_CASH_RATIO: 0.0949 }
    ]
  }
}, { paramResolver, transformExecutor: executeTransformForTest })

assert.strictEqual(hydratedChart.renderState.status, 'ready')
assert.strictEqual(hydratedChart.renderSpec.option.dataset.source.length, 2)
assert.strictEqual(hydratedChart.renderSpec.option.dataset.source[0].TDATE, '20220104')
assert.strictEqual(hydratedChart.renderSpec.option.series.length, 2)
assert.deepStrictEqual(hydratedChart.renderSpec.option.legend.data, ['股票净敞口', '现金类仓位'])
assert.strictEqual(hydratedChart.renderSpec.option.title.show, false)
assert.strictEqual(hydratedChart.renderSpec.option.title.text, '股票净敞口与现金类仓位')

const pieBlock = createVmReportBlock({
  dsl: {
    action: 'create',
    id: '8ba7b810-9dad-41d1-80b4-00c04fd430c8',
    params: {
      fundCode: 'SM0513',
      beginDate: '20220101',
      endDate: '20220131',
      dataFreqOpen: 'true',
      benchmarks: '0',
      dataFreq: '日频'
    },
    requests: [
      {
        id: 'industry',
        moduleId: 'tenProfitIndustry',
        sqlCode: 'fe842e36-d296-432d-8696-d6ec8f2aab03'
      }
    ],
    transform: {
      language: 'javascript',
      function: [
        'function transform(responses) {',
        '  var response = responses && responses.industry;',
        '  var rows = response && Array.isArray(response.body) ? response.body : [];',
        '  return rows.map(function (row) {',
        '    return { industryName: row.INDUSTRY_NAME, weight: row.WEIGHT === null || row.WEIGHT === undefined ? null : Number(row.WEIGHT) * 100 };',
        '  });',
        '}'
      ].join('\n')
    },
    view: {
      type: 'echarts',
      title: '行业权重分布',
      legend: {
        show: true,
        data: ['行业权重']
      },
      dataset: {
        source: '$transform',
        dimensions: ['industryName', 'weight']
      },
      series: [
        {
          name: '行业权重',
          type: 'pie',
          encode: {
            itemName: 'industryName',
            value: 'weight'
          },
          format: {
            type: 'percentage',
            digits: 2,
            suffix: '%'
          }
        }
      ]
    }
  }
})

const hydratedPie = await hydrateVmBlock(pieBlock, async () => ({
  body: [
    { INDUSTRY_NAME: '电子', WEIGHT: 0.2 },
    { INDUSTRY_NAME: '医药', WEIGHT: 0.1 }
  ]
}), { paramResolver, transformExecutor: executeTransformForTest })
assert.strictEqual(hydratedPie.renderState.status, 'ready')
assert.strictEqual(hydratedPie.renderSpec.option.series[0].type, 'pie')
assert.deepStrictEqual(hydratedPie.renderSpec.option.series[0].encode, { itemName: 'industryName', value: 'weight' })
assert.strictEqual(hydratedPie.renderSpec.option.title.show, false)
assert.strictEqual('xAxis' in hydratedPie.renderSpec.option, false)
assert.strictEqual('yAxis' in hydratedPie.renderSpec.option, false)

const forbiddenRuntime = await hydrateVmBlock(createVmReportBlock({
  dsl: {
    ...tableDsl,
    id: '7ba7b810-9dad-41d1-80b4-00c04fd430c8',
    transform: {
      language: 'javascript',
      function: 'function transform(responses) { var rows = responses.profit.body || []; if (window.localStorage) return []; return rows.map(function (row) { return { securityCode: row.VC_SYMBOL, income: row.F_INCOME }; }); }'
    }
  }
}), async () => ({ body: [] }), { paramResolver, transformExecutor: executeTransformForTest })

assert.strictEqual(forbiddenRuntime.renderState.status, 'error')
assert.ok(forbiddenRuntime.sourceData.runtime.lastError.includes('transform.function'))

assert.throws(
  () => createVmReportBlock({
    dsl: {
      action: 'create',
      id: '550e8400-e29b-41d4-a716-446655440000',
      params: {
        fundCode: 'SM0513',
        beginDate: '20220101',
        endDate: '20220131',
        dataFreqOpen: 'true',
        benchmarks: '1',
        benchmarkA: '沪深300',
        dataFreq: '日频'
      },
      requests: [],
      transform: {
        language: 'javascript',
        function: 'function transform(responses) { return []; }'
      },
      view: {
        type: 'table',
        title: '空请求',
        columns: []
      }
    }
  }),
  /requests/
)

console.log('vm report dsl runtime checks passed')
