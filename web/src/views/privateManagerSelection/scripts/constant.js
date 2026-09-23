import moment from 'moment'

// 机构规模
const orzScaleOptions = [
  {
    label: '0-5亿',
    value: '0-5亿',
    checkedState: false
  },
  {
    label: '5-10亿',
    value: '5-10亿',
    checkedState: false
  },
  {
    label: '10-20亿',
    value: '10-20亿',
    checkedState: false
  },
  {
    label: '20-50亿',
    value: '20-50亿',
    checkedState: false
  },
  {
    label: '50-100亿',
    value: '50-100亿',
    checkedState: false
  },
  {
    label: '100亿以上',
    value: '100亿以上',
    checkedState: false
  }
]

// 公司类型
const companyType = [
  {
    id: 1,
    label: '私募证券投资',
    checked: false
  },
  {
    id: 2,
    label: '公募基金公司',
    checked: false
  },
  {
    id: 3,
    label: '证券公司',
    checked: false
  },
  {
    id: 4,
    label: '信托公司',
    checked: false
  },
  {
    id: 5,
    label: '投资顾问',
    checked: false
  },
  {
    id: 6,
    label: '基金公司子公司',
    checked: false
  },
  {
    id: 7,
    label: '私募创业投资',
    checked: false
  },
  {
    id: 8,
    label: '私募其他投资',
    checked: false
  },
  {
    id: 9,
    label: '保险公司',
    checked: false
  },
  {
    id: 10,
    label: '保险公司子公司',
    checked: false
  },
  {
    id: 11,
    label: '私募资产配置类管理人',
    checked: false
  },
  {
    id: 12,
    label: '证券公司私募基金子公司',
    checked: false
  }
]

// 公司状态
const companyState = [
  {
    id: 1,
    label: '运行',
    checked: true
  },
  {
    id: 2,
    label: '注销',
    checked: false
  },
  {
    id: 3,
    label: '吊销',
    checked: false
  },
  {
    id: -1,
    label: '其他',
    checked: false
  }
]

// 备案状态
const recordsState = [
  {
    id: 2,
    label: '备案存续',
    checked: false
  },
  {
    id: 1,
    label: '备案注销',
    checked: false
  },
  {
    id: 0,
    label: '未备案',
    checked: false
  }
]

// 策略类型
const strategyType = [
  {
    title: '策略类型',
    mid: 1,
    checked: 0,
    options: [
      {
        id: 0,
        label: '不限'
      },
      {
        id: 1,
        label: '股票策略'
      },
      {
        id: 2,
        label: '债券策略'
      },
      {
        id: 3,
        label: '期货及衍生品策略'
      },
      {
        id: 4,
        label: '多资产策略'
      },
      {
        id: 5,
        label: '组合基金'
      },
      {
        id: 6,
        label: '其他'
      }
    ]
  }
]

// 成立时间
const clsjOptions = [
  {
    label: '不限',
    value: '1'
  },
  {
    label: '6个月以下',
    value: '2'
  },
  {
    label: '6个月~1年',
    value: '3'
  },
  {
    label: '1-3年',
    value: '4'
  },
  {
    label: '3-5年',
    value: '5'
  },
  {
    label: '5年以上',
    value: '6'
  },
  {
    label: '自定义',
    value: '7'
  }
]

// 成立时间映射关系
const dateShortcutMap = {
  '2': {
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
  '3': {
    onClick() {
      const dateNow = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(dateNow)
          .subtract(12, 'month')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      const end = moment(
        moment(dateNow)
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
      const dateNow = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const end = moment(
        moment(dateNow)
          .subtract(1, 'year')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(dateNow)
          .subtract(3, 'year')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '5': {
    onClick() {
      const dateNow = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const end = moment(
        moment(dateNow)
          .subtract(3, 'year')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      const start = moment(
        moment(dateNow)
          .subtract(5, 'year')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return [start, end]
    }
  },
  '6': {
    onClick() {
      const dateNow = moment()
        .subtract(1, 'days')
        .format('YYYY-MM-DD')
      const end = moment(
        moment(dateNow)
          .subtract(5, 'year')
          .format('YYYY-MM-DD')
      )
        .subtract(-1, 'days')
        .format('YYYY-MM-DD')
      return ['', end]
    }
  }
}

// 产品总数
const cpzs = [
  {
    title: '产品总数',
    mid: 1,
    start: '',
    end: '',
    style:false
  }
]

// 计算区间
const jsqjOptions = [
  {
    title: '计算区间',
    width: '70px',
    // title: "收益-风险区间",
    mid: 1,
    selected: 1,
    options: [
      {
        label: '近六月',
        value: 1
      },
      {
        label: '近一年',
        value: 2
      },
      {
        label: '今年以来',
        value: 3
      },
      {
        label: '成立以来',
        value: 4
      }
    ]
  }
]

// 收益率 / 最大回撤 / sharpe比率 / Treynor比率 / jensen指数
const sylzdhcData = [
  {
    type: 'jsqj',
    title: '收益率',
    id: '10',
    start1: '',
    end1: '',
    start2: '',
    end2: '',
    start3: '',
    end3: '',
    start4: '',
    end4: '',
    style1:false,
    style2:false,
    style3:false,
    style4:false
  },
  {
    type: 'jsqj',
    title: '最大回撤',
    id: '11',
    start1: '',
    end1: '',
    start2: '',
    end2: '',
    start3: '',
    end3: '',
    start4: '',
    end4: '',
    style1:false,
    style2:false,
    style3:false,
    style4:false
  },
  {
    type: 'jsqj',
    start: '',
    end: '',
    id: '12',
    title: 'Sharpe比率',
    style1:false,
    style2:false,
    style3:false,
    style4:false
  },
  {
    type: 'jsqj',
    start1: '',
    end1: '',
    start2: '',
    end2: '',
    start3: '',
    end3: '',
    start4: '',
    end4: '',
    id: '13',
    title: 'Treynor比率',
    style1:false,
    style2:false,
    style3:false,
    style4:false
  },
  {
    type: 'jsqj',
    start1: '',
    end1: '',
    start2: '',
    end2: '',
    start3: '',
    end3: '',
    start4: '',
    end4: '',
    id: '14',
    title: 'Alpha',
    style1:false,
    style2:false,
    style3:false,
    style4:false
  }
]

export default {
  clsjOptions,
  jsqjOptions,
  sylzdhcData,
  cpzs,
  dateShortcutMap,
  orzScaleOptions,
  companyState,
  recordsState,
  strategyType,
  companyType
}
