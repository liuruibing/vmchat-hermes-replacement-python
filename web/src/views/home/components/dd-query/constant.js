// 机构规模
const orzScaleOptions = [
  {
    label: "0-5亿",
    value: "1",
    checkedState: false
  },
  {
    label: "5-10亿",
    value: "2",
    checkedState: false
  },
  {
    label: "10-20亿",
    value: "3",
    checkedState: false
  },
  {
    label: "20-50亿",
    value: "4",
    checkedState: false
  },
  {
    label: "100亿以上",
    value: "5",
    checkedState: false
  }
];
// 投资策略
const investStrategy = [
  {
    id: 1,
    label: "股票多头",
    checked: true
  },
  {
    id: 2,
    label: "股票市场中性",
    checked: false
  },
  {
    id: 3,
    label: "股票多空",
    checked: false
  },
  {
    id: 4,
    label: "债券基金",
    checked: true
  },
  {
    id: 5,
    label: "管理期货",
    checked: false
  },
  {
    id: 6,
    label: "套利策略",
    checked: false
  },
  {
    id: 7,
    label: "宏观策略",
    checked: true
  },
  {
    id: 8,
    label: "组合基金",
    checked: false
  },
  {
    id: 9,
    label: "定向增发 ",
    checked: false
  },
  {
    id: 10,
    label: "新三板",
    checked: false
  },
  {
    id: 11,
    label: "多策略",
    checked: false
  },
  {
    id: 12,
    label: "其他",
    checked: false
  }
];
// 是否量化 / 是否对冲 / 是否结构化
const line2Data = [
  {
    title: "是否量化",
    mid: 1,
    checked: 2,
    width: '70px',
    options: [
      {
        id: 0,
        label: "不限"
      },
      {
        id: 1,
        label: "量化"
      },
      {
        id: 2,
        label: "非量化"
      }
    ]
  },
  {
    title: "是否对冲",
    mid: 2,
    checked: 1,
    width: '70px',
    options: [
      {
        id: 0,
        label: "不限"
      },
      {
        id: 1,
        label: "对冲"
      },
      {
        id: 2,
        label: "非对冲"
      }
    ]
  },
  {
    title: "是否结构化",
    mid: 3,
    checked: 0,
    width: '120px',
    options: [
      {
        id: 0,
        label: "不限"
      },
      {
        id: 1,
        label: "结构化"
      },
      {
        id: 2,
        label: "非结构化"
      }
    ]
  }
];
// 成立时间
const clsjOptions = [
  {
    label: "不限",
    value: 1
  },
  {
    label: "6个月以下",
    value: 2
  },
  {
    label: "6个月~1年",
    value: 3
  },
  {
    label: "1-3年",
    value: 4
  },
  {
    label: "3-5年",
    value: 5
  },
  {
    label: "5年以上",
    value: 6
  },
  {
    label: "自定义",
    value: 7
  }
];
// 发行方式
const fxfsOptions = [
  {
    mid: 1,
    title: "发行方式：",
    selected: 2,
    selectOptions: [
      {
        label: "私募证券投资",
        value: 1
      },
      {
        label: "私募股权投资",
        value: 2
      },
      {
        label: "私募创业投资",
        value: 3
      },
      {
        label: "私募其他投资",
        value: 5
      }
    ],
    checkboxOptions: [
      {
        id: 1,
        label: "信托",
        checked: false
      },
      {
        id: 2,
        label: "公募专户",
        checked: true
      },
      {
        id: 3,
        label: "券商投管",
        checked: false
      },
      {
        id: 4,
        label: "期货资管",
        checked: true
      },
      {
        id: 5,
        label: "保险及子公司",
        checked: false
      }
    ]
  }
];
// 净值频率 / 净值完整度
const jzplOptions = [
  {
    title: "净值频率",
    mid: 1,
    selected: 1,
    width: "70px",
    options: [
      {
        label: "不限",
        value: 1
      },
      {
        label: "日频",
        value: 2
      },
      {
        label: "周频",
        value: 3
      },
      {
        label: "月频",
        value: 4
      },
      {
        label: "其他",
        value: 5
      }
    ]
  },
  {
    title: "净值完整度",
    mid: 2,
    selected: 1,
    width: "90px",
    options: [
      {
        label: "不限",
        value: 1
      },
      {
        label: "≥70%",
        value: 2
      }
    ]
  }
];
// 运行状态 / 备案状态
const line5Data = [
  {
    checkboxOptions: [
      {
        id: 1,
        label: "运作中",
        checked: true
      },
      {
        id: 2,
        label: "已终止",
        checked: false
      }
    ]
  },
  {
    title: "备案状态：",
    mid: 2,
    checkboxOptions: [
      {
        id: 1,
        label: "已备案",
        checked: false
      },
      {
        id: 2,
        label: "未备案",
        checked: true
      }
    ]
  }
];
// 收益风险区间 / 计算频率
const syfxOptions = [
  {
    title: "收益-风险区间",
    mid: 1,
    selected: 1,
    options: [
      {
        label: "今年以来",
        value: 1
      },
      {
        label: "近一月",
        value: 2
      },
      {
        label: "近三月",
        value: 3
      },
      {
        label: "近六月",
        value: 4
      },
      {
        label: "近一年",
        value: 5
      },
      {
        label: "近两年",
        value: 6
      },
      {
        label: "近三年",
        value: 7
      },
      {
        label: "成立以来年化",
        value: 8
      }
    ]
  },
  {
    title: "计算频率",
    mid: 2,
    selected: 1,
    options: [
      {
        label: "自适应",
        value: 1
      },
      {
        label: "日代替",
        value: 2
      },
      {
        label: "周频",
        value: 3
      },
      {
        label: "月频",
        value: 4
      }
    ]
  }
];
// 收益率 / 最大回撤
const line6Data = [
  {
    title: "收益率",
    mid: 1,
    selected: 4,
    start: "1",
    end: "5",
    options: [
      {
        value: 1,
        label: "收益排名10%"
      },
      {
        value: 2,
        label: "收益排名20%"
      },
      {
        value: 3,
        label: "收益排名30%"
      },
      {
        value: 4,
        label: "自定义"
      }
    ]
  },
  {
    title: "最大回撤",
    mid: 2,
    selected: 4,
    start: "5",
    end: "10",
    options: [
      {
        value: 1,
        label: "回撤排名10%"
      },
      {
        value: 2,
        label: "回撤排名20%"
      },
      {
        value: 3,
        label: "回撤排名30%"
      },
      {
        value: 4,
        label: "自定义"
      }
    ]
  }
];
// sharpe比率≥
const sharpeOptions = [
  {
    inputVal: "8",
    mid: 1,
    selected: 4,
    title: "sharpe比率≥",
    options: [
      {
        value: 1,
        label: "夏普比率排名10%"
      },
      {
        value: 2,
        label: "夏普比率排名20%"
      },
      {
        value: 3,
        label: "夏普比率排名30%"
      },
      {
        value: 4,
        label: "自定义"
      }
    ]
  }
];
// 风格评价
const fgpjOptions = [
  {
    mid: 1,
    selected: 3,
    placeholder: "风格偏好",
    selectOptions: [
      {
        label: "价值型",
        value: 1
      },
      {
        label: "成长型",
        value: 2
      },
      {
        label: "主题型",
        value: 3
      },
      {
        label: "平衡型",
        value: 5
      }
    ]
  },
  {
    mid: 2,
    selected: "",
    placeholder: "操作偏好",
    selectOptions: [
      {
        label: "择时型",
        value: 1
      },
      {
        label: "选股型",
        value: 2
      }
    ]
  },
  {
    mid: 3,
    selected: 2,
    placeholder: "市道适应性",
    selectOptions: [
      {
        label: "上升市道",
        value: 1
      },
      {
        label: "下跌市道",
        value: 2
      },
      {
        label: "盘整市道",
        value: 3
      }
    ]
  },
  {
    mid: 4,
    selected: "",
    placeholder: "绩效星级",
    selectOptions: [
      {
        label: "5星",
        value: 1
      },
      {
        label: "3星",
        value: 2
      },
      {
        label: "3星",
        value: 3
      }
    ]
  }
];
// 是否有深度分析
const sdfxOptions = [
  {
    selected: 1,
    mid: 1,
    placeholder: "是否有深度分析",
    selectOptions: [
      {
        label: "不限",
        value: 1
      },
      {
        label: "是",
        value: 2
      },
      {
        label: "否",
        value: 3
      }
    ]
  }
];
const dynamicTags = [
  {
    title: "投资策略：",
    value: "股票多投, 债券基金,宏观策略"
  },
  {
    title: "是否量化：",
    value: "非量化"
  },
  {
    title: "是否对冲：",
    value: "对冲"
  },
  {
    title: "发行方式：",
    value: "私募股权投资/公募专户/期货资管"
  },
  {
    title: "运行状态：",
    value: "存续中, 未备案"
  },
  {
    title: "收益-风险区间：",
    value: "今年以来"
  },
  {
    title: "计算频率：",
    value: "自适应"
  },
  {
    title: "收益率：",
    value: "1%~5%"
  },
  {
    title: "最大回撤：",
    value: "5%~10%"
  },
  {
    title: "sharpe比率≥：",
    value: "8%"
  },
  {
    title: "风格偏好：",
    value: "主题型/下跌市道"
  }
];
const tzfgOptions = [
  {
    title: "投资风格：",
    mid: 1,
    checked: 0,
    options: [
      {
        id: 0,
        label: "全部"
      },
      {
        id: 1,
        label: "成长"
      },
      {
        id: 2,
        label: "均衡"
      },
      {
        id: 3,
        label: "价值"
      }
    ]
  }
];
module.exports = {
  orzScaleOptions,
  investStrategy,
  line2Data,
  clsjOptions,
  fxfsOptions,
  jzplOptions,
  line5Data,
  syfxOptions,
  line6Data,
  sharpeOptions,
  fgpjOptions,
  sdfxOptions,
  dynamicTags,
  tzfgOptions,
};
