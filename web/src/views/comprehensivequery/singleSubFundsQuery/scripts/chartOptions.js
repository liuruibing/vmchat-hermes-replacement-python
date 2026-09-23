import { processing_Decimal, getMin_Max } from '../../fundTradeAnalysis/scripts/dataHandle'

export function buildSingleSubFundsChartOption(data) {
  if (!data || data.length === 0) {
    return null
  }

  const xaxisData = []
  const symbolShare = []
  const symbolPrice = []
  const symbolCost = []
  const symbolYield = []
  const symbolContribute = []
  const symbolName = data[0].symbolName || ''

  let interval = 0
  if (data.length > 31) {
    interval = Math.floor(data.length / 30)
  }

  for (let i = 0; i < data.length; i++) {
    xaxisData[i] = data[i].tDate
    symbolShare[i] = data[i].symbolShare
    symbolPrice[i] = data[i].symbolPrice
    symbolCost[i] = data[i].symbolCost
    symbolYield[i] = data[i].symbolYield
    symbolContribute[i] = data[i].symbolContribute
  }

  return {
    animation: false,
    title: { text: symbolName, borderColor: '#FFF', textAlign: 'center', x: 'center', y: 'top' },
    tooltip: { trigger: 'axis' },
    toolbox: {
      borderColor: '#FFF',
      feature: {
        dataView: { lang: ['数据视图', '关闭', '刷新'], readOnly: false, show: true, title: '数据视图', buttonColor: '#4ca1ff' },
        saveAsImage: { lang: ['点击保存'], show: true, title: '保存为图片', type: 'svg' }
      },
      right: '70px'
    },
    grid: { x: '80px', y: '50px', x2: '80px', y2: '110px' },
    legend: {
      data: [
        { name: '份额(左)', icon: 'circle', textStyle: { fontSize: 12 } },
        { name: '市值(左)', icon: 'circle', textStyle: { fontSize: 12 } },
        { name: '成本(左)', icon: 'circle', textStyle: { fontSize: 12 } },
        { name: '收益率%(右)', icon: 'circle', textStyle: { fontSize: 12 } },
        { name: '日净值贡献%(右)', icon: 'circle', textStyle: { fontSize: 12 } }
      ],
      bottom: '0px',
      itemWidth: 15,
      itemGap: 20,
      borderColor: '#FFF'
    },
    xAxis: {
      type: 'category',
      data: xaxisData,
      axisLabel: { show: true, interval, rotate: -90, fontSize: 12, color: '#000' },
      axisLine: { lineStyle: { color: '#8d8d8d' } },
      splitLine: { show: true, lineStyle: { type: 'dotted' } },
      axisTick: { show: false }
    },
    yAxis: [{
      type: 'value',
      splitLine: { show: true, lineStyle: { type: 'dotted' } },
      axisTick: { show: false },
      axisLine: { lineStyle: { color: '#8d8d8d' } },
      max: processing_Decimal(Number(getMin_Max([symbolShare, symbolPrice, symbolCost])[1]), 2),
      min: processing_Decimal(Number(getMin_Max([symbolYield, symbolPrice, symbolCost])[0]), 2),
      axisLabel: { formatter: '{value}', fontSize: 12, color: '#000' }
    }, {
      type: 'value',
      splitLine: { show: false },
      axisTick: { show: false },
      max: processing_Decimal(Number(getMin_Max([symbolYield, symbolContribute])[1]), 4),
      min: processing_Decimal(Number(getMin_Max([symbolYield, symbolContribute])[0]), 4),
      axisLine: { lineStyle: { color: '#8d8d8d' } },
      axisLabel: { formatter: '{value}%', fontSize: 12, color: '#000' }
    }],
    series: [{
      name: '份额(左)',
      type: 'line',
      smooth: true,
      symbol: 'none',
      yAxisIndex: 0,
      data: symbolShare
    }, {
      name: '市值(左)',
      type: 'line',
      smooth: true,
      symbol: 'none',
      yAxisIndex: 0,
      data: symbolPrice
    }, {
      name: '成本(左)',
      type: 'line',
      smooth: true,
      symbol: 'none',
      yAxisIndex: 0,
      data: symbolCost
    }, {
      name: '收益率%(右)',
      type: 'line',
      smooth: true,
      symbol: 'none',
      yAxisIndex: 1,
      data: symbolYield
    }, {
      name: '日净值贡献%(右)',
      type: 'line',
      smooth: true,
      symbol: 'none',
      yAxisIndex: 1,
      data: symbolContribute
    }]
  }
}
