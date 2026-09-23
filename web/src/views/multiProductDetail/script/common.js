import moment from 'moment'
import { getToken } from '@/utils/auth'
// 时间映射关系
export const dateShortcutMap = {
  '1': {
    onClick() {
      const end = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(end)
          .subtract(1, 'month')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '2': {
    onClick() {
      const end = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(end)
          .subtract(3, 'month')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '3': {
    onClick() {
      const end = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(end)
          .subtract(6, 'month')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '4': {
    onClick() {
      const end = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(end)
          .subtract(12, 'month')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '5': {
    onClick() {
      const end = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(end).year() + '-01-01'
      return [start, end]
    }
  }
}

// 重构 - 深度分析 - 收益与风险指标对比表格列
export const riskTableColumns = [
  {
    label: '指标',
    prop: 'YDATE',
  },
  {
    label: '收益率（年化）',
    prop: 'YDATE1',
    sortable:true,
  },
  {
    label: '波动率（年化）',
    prop: 'YDATE2',
    sortable:true,
  },
  {
    label: '下行波动率（年化）',
    prop: 'YDATE3',
    sortable:true,
  },
  {
    label: '夏普比率（年化）',
    prop: 'YDATE4',
    sortable:true,
  },
  {
    label: '索提诺比率（年化）',
    prop: 'YDATE5',
    sortable:true,
  },
  {
    label: '信息（年化）',
    prop: 'YDATE6',
    sortable:true,
  },
  {
    label: '最大回撤',
    prop: 'YDATE7',
    sortable:true,
  },
  {
    label: '卡玛比率',
    prop: 'YDATE8',
    sortable:true,
  }
]

// 重构 - 深度分析 - 动态回撤对比chart
let color = [
  '#fc6769',
  '#d2a25a',
  '#789d51',
  '#6c50f3',
  '#396f92',
  '#8EB4E3',
  '#CCC1DA',
  '#FAC090',
  '#E6B9B8',
  '#E0B1CB',
  '#967D69'
]
export const chartOptions = {
  tooltip: {
    trigger: 'axis',
    formatter: params => {
      let tip = params[0].name + '<br>'
      for (let i = 0; i < params.length; i++) {
        let value = ''
        if ((params[i].value == undefined || params[i].value == '') && params[i].value != 0) {
          value = '--'
        } else {
          value = Number(params[i].value).toFixed(2)
        }
        tip += params[i].marker + params[i].seriesName + ': ' + value + '%' + '<br>'
      }
      return tip
    }
  },
  color: color,
  legend: {
    top: '3%',
    data: [],
    itemWidth: 18,
    itemHeight: 12,
    textStyle: { color: '#000', fontSize: 12 }
  },
  animation: false,
  grid: {
    left: '100',
    right: '100',
    bottom: '10%',
    top: '22%',
    containLabel: true
  },
  xAxis: {
    type: 'category',
    boundaryGap: false,
    data: [],
    axisLabel: {
      inside: false,
      textStyle: {
        fontSize: 11
      }
    },
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    splitArea: {
      show: true,
      areaStyle: {
        color: ['rgba(250,250,250,0.3)', 'rgba(255,255,255,0.3)']
      }
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: '#e5e5e5',
        type: 'dashed'
      }
    }
  },
  yAxis: {
    name: '回撤（%）',
    type: 'value',
    position: 'left',
    axisLabel: {
      formatter: '{value}%'
    },
    axisLine: {
      show: false
    },
    axisTick: {
      show: false
    },
    splitArea: {
      show: false
    },
    splitLine: {
      show: true,
      lineStyle: {
        color: '#e5e5e5',
        type: 'dashed'
      }
    }
  },
  dataZoom: {
    show: true
  },
  series: []
}

export default {
  dateShortcutMap
}
