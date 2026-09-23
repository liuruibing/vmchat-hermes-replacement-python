import moment from 'moment'

export const TOP_DESC_DATA = [
  {
    label: '成立日期',
    value: ''
  },
  {
    label: '基金经理',
    value: ''
  },
  {
    label: '投资顾问',
    value: ''
  },
  {
    label: '基金管理人',
    value: ''
  },
  {
    label: '办公地',
    value: ''
  },
  // {
  //   label: '历史荣誉',
  //   value: ''
  // },
  {
    label: '策略分类',
    value: ''
  },
  {
    label: '备案编号',
    value: ''
  },
  {
    label: '运行状态',
    value: ''
  },
  /*{
    label: '绩效评级',
    value: 0
  }*/
]

export const MIDDLE_LEFT_DATA = [
  {
    label: '最新数据日期',
    value: '',
  },
  {
    label: '单位净值',
    value: ''
  },
  {
    label: '累计净值',
    value: ''
  },
  {
    label: '复权累计净值',
    value: ''
  }
]

export const MIDDLE_MIDDLE_DATA = [
  {
    label: '近三月收益率',
    value: ''
  },
  {
    label: '今年以来收益率',
    value: ''
  },
  {
    label: '近一年收益率',
    value: ''
  }
]

export const MIDDLE_RIGHT_DATA = [
  {
    label: '成立以来最大回撤',
    value: ''
  },
  {
    label: '成立以来Sharpe比率',
    value: ''
  }
]

export const STATIST_PERIOD_OPTIONS = [
  {
    label: '近一月',
    value: '1'
  },
  {
    label: '近三月',
    value: '2'
  },
  {
    label: '近六月',
    value: '3'
  },
  {
    label: '近一年',
    value: '4'
  },
  {
    label: '今年以来',
    value: '5'
  },
  {
    label: '成立以来',
    value: '6'
  },
  {
    label: '自定义',
    value: '7'
  }
]

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
      let end = new Date()
      let start = new Date()
      start = start.getFullYear() + '-1-1'
      end = end.getFullYear() + '-' + (end.getMonth() + 1) + '-' + end.getDate()
      return [start, end]
    }
  }
}

export const defalutContrasmap = {
  // 债券: ['CBA00201'],
  债券: ['CBA00203CF'],
  // '理财/回购/现金': ['CBA00201'],
  '理财/回购/现金': ['CBA00203CF'],
  // 银行理财类: ['CBA00201'],
  银行理财类: ['CBA00203CF'],
  趋势型CTA: ['NH0100'],
  套利型CTA: ['NH0100'],
  '股权/合伙企业': ['000300'],
  股票市场中性: ['000300'],
  权益多头: ['000300'],
  权益多空: ['000300'],
  指数增强: ['000300'],
  房地产: ['000300'],
  '收益权/ABS': ['000300'],
  混合类: ['000300', '000905'],
  '定增/事件驱动': ['000300', '000905'],
  母子基金: ['000300', '000905'],
  FOF: ['000300', '000905'],
  内部FOF: ['000300', '000905'],
  联接基金: ['000300', '000905']
}

export default {
  TOP_DESC_DATA,
  MIDDLE_LEFT_DATA,
  MIDDLE_MIDDLE_DATA,
  MIDDLE_RIGHT_DATA,
  STATIST_PERIOD_OPTIONS,
  dateShortcutMap,
  defalutContrasmap
}
