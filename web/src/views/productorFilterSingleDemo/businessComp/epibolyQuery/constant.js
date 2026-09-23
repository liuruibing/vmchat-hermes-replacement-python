import moment from 'moment'

// 运行状态
const yxztData = [
  {
    title: '运行状态',
    mid: 1,
    checked: 1,
    options: [
      {
        id: 2,
        label: '不限'
      },
      {
        id: 1,
        label: '运作中'
      },
      {
        id: 0,
        label: '已终止'
      }
    ]
  }
]

// 是否分级
const sffjData = [
  {
    title: '是否分级',
    mid: 2,
    checked: 2,
    options: [
      {
        id: 2,
        label: '不限'
      },
      {
        id: 1,
        label: '分级'
      },
      {
        id: 0,
        label: '不分级'
      }
    ]
  }
]



// 净值频率
const jzplOptions = [
  {
    title: '净值频率',
    mid: 3,
    selected: 3,
    width: '70px',
    options: [
      {
        label: '不限',
        value: 3
      },
      {
        label: '日频',
        value: 0
      },
      {
        label: '周频',
        value: 1
      },
      {
        label: '月频',
        value: 2
      }
    ]
  }
]

// 是否代销
const sfdxData = [
  {
    title: '是否代销',
    mid: 0,
    checked: 0,
    options: [
      {
        id: 0,
        label: '不限'
      },
      {
        id: 1,
        label: '代销产品'
      },
      {
        id: 2,
        label: '非代销产品'
      }
    ]
  }
]

// 绩效评级
const jxpjOptions = [
  {
    mid: 4,
    selected: 0,
    placeholder: '绩效评级',
    selectOptions: [
      {
        label: '不限',
        value: 0
      },
      {
        label: '1星',
        value: 1
      },
      {
        label: '2星',
        value: 2
      },
      {
        label: '3星',
        value: 3
      },
      {
        label: '4星',
        value: 4
      },
      {
        label: '5星',
        value: 5
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

// 资产净值
const zcjz = [
  {
    title: '单位净值',
    mid: 1,
    start: '',
    end: '',
    style:false
  }
]
// 累计净值
const ljjz = [
  {
    title: '累计净值',
    mid: 20,
    start: '',
    end: '',
    style:false
  }
]
// 资产净值
const zcjzs = [
  {
    title: '资产净值',
    mid: 21,
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

// 成立以来大类资产占比
const sinceThe = [
  {
    id: '15',
    name: 'clyl',
    isShow: false,
    title: '股票占净值比(平均值%)',
    start: '',
    end: '',
    index: '0',
    style: false
  },
  {
    id: '16',
    name: 'clyl',
    isShow: false,
    title: '基金占净值比(平均值%)',
    start: '',
    end: '',
    index: '1',
    style: false
  },
  {
    id: '17',
    name: 'clyl',
    isShow: false,
    title: '期货占净值比(平均值%)',
    start: '',
    end: '',
    index: '2',
    style: false
  },
  {
    id: '18',
    name: 'clyl',
    isShow: false,
    title: '债券占净值比(平均值%)',
    start: '',
    end: '',
    index: '3',
    style: false
  }
]

export default {
  sffjData,
  sfdxData,
  clsjOptions,
  jzplOptions,
  yxztData,
  jsqjOptions,
  sylzdhcData,
  jxpjOptions,
  zcjz,
  ljjz,
  zcjzs,
  sinceThe,
  dateShortcutMap
}
