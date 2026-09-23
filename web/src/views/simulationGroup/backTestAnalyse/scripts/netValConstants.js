import { CHART_COLOR_ARR } from "@/metaData/enum.js"


export const NET_VALUE_CHART_OPTIONS = {
  tooltip: {
    trigger: 'axis',
    formatter: function(params) {
      var relVal = params[0].name
      for (var i = 0, l = params.length; i < l; i++) {
        relVal += '<br/>' + params[i].marker + params[i].seriesName + '：' + (params[i].value || '-')
      }
      return relVal
    }
  },
  color: CHART_COLOR_ARR,
  legend: {
    y: '4%',
    data: ['虚拟计提业绩报酬后的单位净值', '单位净值', '资产净值', '份额']
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '13%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    axisTick: {
      show: false
    },
    data: []
  },
  yAxis: [
    {
      type: 'value',
      axisLabel: {
        formatter: '{value} '
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'solid',
          color: '#ececec'
        }
      },
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      name: '净值'
    },
    {
      type: 'value',
      name: '资产净值（万元）',
      position: 'right',
      axisLine: {
        show: false
      },
      axisTick: {
        show: false
      },
      axisLabel: {
        formatter: '{value}'
      },
      splitLine: {
        show: false
      }
    }
  ],
  dataZoom: {
    show: true,
    start: 0,
    end: 100,
    moveHandleSize: 20
  },
  series: [
    {
      name: '虚拟计提业绩报酬后的单位净值',
      type: 'line',
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: [],
      symbol: 'none',
      smooth: true
    },
    {
      name: '单位净值',
      type: 'line',
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: [],
      symbol: 'none',
      smooth: true
    },
    {
      name: '资产净值',
      type: 'line',
      yAxisIndex: 1,
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: [],
      symbol: 'none',
      smooth: true
    },
    {
      name: '份额',
      type: 'line',
      yAxisIndex: 1,
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: [],
      symbol: 'none',
      smooth: true
    }
  ]
}

export const NET_VALUE_TABLE_COLUMNS = [
  {
    prop: 'typeName',
    label: '指标',
    align: 'center',
    headerAlign: 'center'
  },
  {
    prop: 'yieldqj',
    label: '区间',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'yield1m',
    label: '近一月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'yield3m',
    label: '近三月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'yield6m',
    label: '近六月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'yieldcl',
    label: '成立以来',
    align: 'right',
    headerAlign: 'center'
  }
]

export default {
  NET_VALUE_CHART_OPTIONS,
  NET_VALUE_TABLE_COLUMNS
}
