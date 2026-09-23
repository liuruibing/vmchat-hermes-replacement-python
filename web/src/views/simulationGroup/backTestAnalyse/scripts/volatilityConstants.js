import { CHART_COLOR_ARR } from "@/metaData/enum.js"


export const VOLATILITY_CHART_OPTIONS = {
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
    data: ['组合波动率', '基准波动率']
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
        formatter: function(value) {
          return value + '%'
        }
      },
      splitLine: {
        show: true,
        lineStyle: {
          type: 'solid',
          color: '#ececec'
        }
      },
      name: '波动率（%）'
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
      name: '组合波动率',
      type: 'line',
      smooth: true,
      symbolSize: 0,
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: []
    },
    {
      name: '基准波动率',
      type: 'line',
      smooth: true,
      symbolSize: 0,
      lineStyle: {
        normal: {
          width: 2
        }
      },
      data: []
    }
  ]
}

export default {
  VOLATILITY_CHART_OPTIONS
}
