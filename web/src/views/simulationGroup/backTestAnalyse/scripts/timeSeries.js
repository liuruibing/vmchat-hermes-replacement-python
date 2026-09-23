
import { CHART_COLOR_ARR } from "@/metaData/enum.js"


var colors = CHART_COLOR_ARR

export const TIME_SERIES_CHART_OPTIONS = {
  color: colors,
  tooltip: {
    trigger: 'axis',
    formatter: function(params) {
      var relVal = params[0].name
      for (var i = 0, l = params.length; i < l; i++) {
        if (
          (params[i].value != '' &&
            params[i].value != undefined &&
            params[i].value != null &&
            params[i].value != '-') ||
          params[i].value == 0
        ) {
          relVal += '<br/>' + params[i].marker + params[i].seriesName + '：' + params[i].value + '%'
        } else {
          relVal += '<br/>' + params[i].marker + params[i].seriesName + '：' + '-'
        }
      }
      return relVal
    }
  },
  legend: {
    type: 'scroll',
    top: '4%',
    left: '42%',
    itemWidth: 20,
    itemHeight: 10,
    textStyle: {
      fontSize: 14,
      padding: [3, 0, 0, 0]
    },
    data: []
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '13%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    axisTick: {
      show: true
    },
    axisLabel: {
      rotate: 90,
      interval: 'auto'
    },
    data: []
  },
  yAxis: {
    type: 'value',
    name: '占比',
    nameGap: 50,
    nameLocation: 'middle',
    axisTick: {
      show: true
    },
    splitLine: {
      show: true,
      lineStyle: {
        type: 'solid',
        color: '#ececec'
      }
    },
    axisLabel: {
      formatter: function(value) {
        return value + '%'
      }
    },
    max: 120,
    min: 0
  },
  series: []
}

export const TIME_SERIES_TABLE_COLUMNS = [
  {
    prop: 'subFundName',
    label: '子基金名称',
    align: 'left',
    headerAlign: 'center'
  },
  {
    prop: 'price',
    label: '金额（万元）',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'costRate',
    label: '占净值比',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'periodVariation',
    label: '期间变化',
    align: 'right',
    headerAlign: 'center'
  }
]

export default {
  TIME_SERIES_CHART_OPTIONS,
  TIME_SERIES_TABLE_COLUMNS
}
