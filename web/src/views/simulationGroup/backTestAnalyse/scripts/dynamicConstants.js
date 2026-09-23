
import { CHART_COLOR_ARR } from "@/metaData/enum.js"

export const DYNAMIC_CHART_OPTIONS = {
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
    data: ['', '']
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
  yAxis: {
    type: 'value',
    name: '动态回撤（%）',
    axisLabel: {
      formatter: function(value) {
        return value + '%'
      }
    },
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    }
  },
  dataZoom: {
    show: true,
    start: 0,
    end: 100,
    moveHandleSize: 20
  },
  series: [
    {
      name: '',
      type: 'line',
      areaStyle: {
        normal: {
          color: '#6ba6e1',
          opacity: '0.4'
        }
      },
      symbolSize: 0,
      data: []
    },
    {
      name: '',
      type: 'line',
      areaStyle: {
        normal: {
          color: '#ef8080',
          opacity: '0.4'
        }
      },
      symbolSize: 0,
      data: []
    }
  ]
}
export const DYNAMIC_TABLE_COLUMNS = [
  {
    prop: 'typeName',
    label: '期间',
    align: 'center',
    headerAlign: 'center'
  },
  {
    prop: 'drawdown1m',
    label: '近一月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'drawdown3m',
    label: '近三月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'drawdown6m',
    label: '近六月',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'drawdown1y',
    label: '近一年',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'drawdowncl',
    label: '成立以来',
    align: 'right',
    headerAlign: 'center'
  }
]

export default {
  DYNAMIC_CHART_OPTIONS,
  DYNAMIC_TABLE_COLUMNS
}
