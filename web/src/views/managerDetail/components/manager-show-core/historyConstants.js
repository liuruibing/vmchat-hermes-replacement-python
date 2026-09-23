import moment from 'moment'

export const HISTORY_TABLE_COLUMNS = [
  {
    prop: 'COMPANY_SHORT_NAME',
    label: '',
    align: 'left',
    headerAlign: 'center'
  },
  {
    prop: 'YIELD',
    label: '收益率',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'NHJZ',
    label: '拟合净值',
    align: 'right',
    headerAlign: 'center'
  },
  {
    prop: 'T_POINT',
    label: '调整后点位',
    align: 'right',
    headerAlign: 'center'
  }
]

// 统计区间
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
