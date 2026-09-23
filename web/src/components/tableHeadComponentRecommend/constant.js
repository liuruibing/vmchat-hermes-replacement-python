// 维护动态列头的固定数据

export const leftTreeData = [
  {
    label: '基本信息',
    id: 'jbxx',
    type: 'leftTreeData',
    children: [
      {
        label: '产品代码',
        disabled: true,
        id: 'fundCode',
        type: 'leftTreeData',
        align: 'center',
        fix: 'left',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '产品名称',
        disabled: false,
        id: 'fundFullName',
        type: 'leftTreeData',
        align: 'left',
        fix: 'left',
        width: '150px',
        noshowoverflowtooltip: true,
        filter: 'fund',
        sortable: true
      },
      {
        label: '产品管理人',
        id: 'companyFullName',
        disabled: false,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '150px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '产品入选日期',
        disabled: true,
        id: 'rankDate',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '130px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '近六月走势',
        id: 'options',
        disabled: true,
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: 'echarts',
        sortable: false
      },
      {
        label: '产品简称',
        id: 'fundName',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '150px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '管理人简称',
        id: 'companyName',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '150px',
        noshowoverflowtooltip: true,
        filter: 'manager',
        sortable: true
      },
      {
        label: '策略类型',
        id: 'type',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '基金经理',
        id: 'managerName',
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '成立日期',
        id: 'foundDate',
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '运行状态',
        id: 'status',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '120px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '是否分级',
        id: 'isTier',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '资产净值',
        id: 'price',
        type: 'leftTreeData',
        align: 'right',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: 'moneyYuan2Yuan',
        sortable: true
      },
      {
        label: '净值频率',
        id: 'navfrequency',
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      }
    ]
  }
]

export const centerTreeDataLeft = [
  {
    label: '机构信息',
    id: 'jgxx',
    children: [
      {
        label: '管理规模区间',
        id: 'managerAsset',
        type: 'centerTreeDataLeft',
        align: 'right',
        fix: '',
        width: '130px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '注册资本',
        id: 'capital',
        type: 'centerTreeDataLeft',
        align: 'right',
        fix: '',
        width: '120px',
        noshowoverflowtooltip: true,
        filter: 'moneyYuanStrW',
        sortable: true
      },
      {
        label: '机构成立日期',
        id: 'company_found_date',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '130px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      }
    ]
  }
]

export const centerTreeDataCenter = [
  {
    label: '净值指标',
    id: 'jzzb',
    children: [
      {
        label: '净值日期',
        id: 'navDate',
        type: 'centerTreeDataCenter',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '单位净值',
        id: 'unitNav',
        type: 'centerTreeDataCenter',
        align: 'right',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: 'moneyYuan4Yuan',
        sortable: true
      },
      {
        label: '累计净值',
        id: 'addedNav',
        type: 'centerTreeDataCenter',
        align: 'right',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: 'moneyYuan4Yuan',
        sortable: true
      }
    ]
  }
]

export const centerTreeDataRight = [
  {
    label: '业绩指标',
    id: 'yjzb',
    children: [
      {
        label: '近一月',
        id: 'j1y',
        children: [
          {
            label: '近一月收益率',
            id: 'm1_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一月波动率',
            id: 'm1_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一月最大回撤',
            id: 'm1_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一月Sharpe比率',
            id: 'm1_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一月Sortino比率',
            id: 'm1_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一月Treynor比率',
            id: 'm1_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      },
      {
        label: '近三月',
        id: 'j3y',
        children: [
          {
            label: '近三月收益率',
            id: 'm3_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近三月波动率',
            id: 'm3_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近三月最大回撤',
            id: 'm3_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近三月Sharpe比率',
            id: 'm3_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近三月Sortino比率',
            id: 'm3_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近三月Treynor比率',
            id: 'm3_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      },
      {
        label: '近六月',
        id: 'j6y',
        children: [
          {
            label: '近六月收益率',
            id: 'm6_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月波动率',
            id: 'm6_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月最大回撤',
            id: 'm6_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Sharpe比率',
            id: 'm6_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Sortino比率',
            id: 'm6_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Treynor比率',
            id: 'm6_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      },
      {
        label: '近一年',
        id: 'j1year',
        children: [
          {
            label: '近一年收益率',
            id: 'y1_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年波动率',
            id: 'y1_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年最大回撤',
            id: 'y1_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Sharpe比率',
            id: 'y1_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Sortino比率',
            id: 'y1_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Calmar比率',
            id: 'y1_calmar',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Alpha',
            id: 'y1_alpha',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Beta',
            id: 'y1_beta',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年信息比率',
            id: 'y1_info',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年投资胜率',
            id: 'y1_winrate',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Treynor比率',
            id: 'y1_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      },
      {
        label: '今年以来',
        id: 'jnyl',
        children: [
          {
            label: '今年以来收益率',
            id: 'ytd_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来波动率',
            id: 'ytd_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来最大回撤',
            id: 'ytd_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Sharpe比率',
            id: 'ytd_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Sortino比率',
            id: 'ytd_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Calmar比率',
            id: 'ytd_calmar',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Alpha',
            id: 'ytd_alpha',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Beta',
            id: 'ytd_beta',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来信息比率',
            id: 'ytd_info',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来投资胜率',
            id: 'ytd_winrate',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Treynor比率',
            id: 'ytd_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      },
      {
        label: '成立以来',
        id: 'clyl',
        children: [
          {
            label: '成立以来收益率',
            id: 'total_return',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来波动率',
            id: 'total_stdev',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来最大回撤',
            id: 'total_max_retracement',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Sharpe比率',
            id: 'total_sharpe',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Sortino比率',
            id: 'total_sortino',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Calmar比率',
            id: 'total_calmar',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Alpha',
            id: 'total_alpha',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Beta',
            id: 'total_beta',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来信息比率',
            id: 'total_info',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来投资胜率',
            id: 'total_winrate',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '成立以来Treynor比率',
            id: 'total_terynor',
            type: 'centerTreeDataRight',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
        ]
      }
    ]
  }
]

export const rightTreeData = [
  {
    label: '更多指标',
    id: 'qtzb',
    children: [
      {
        label: '成立以来股票占净值比(平均值)',
        id: 'stock_ratio',
        type: 'rightTreeData',
        align: 'right',
        fix: '',
        width: '200px',
        noshowoverflowtooltip: true,
        filter: 'numberToFixedStr',
        sortable: true
      },
      {
        label: '成立以来债券占净值比(平均值)',
        id: 'bond_ratio',
        type: 'rightTreeData',
        align: 'right',
        fix: '',
        width: '200px',
        noshowoverflowtooltip: true,
        filter: 'numberToFixedStr',
        sortable: true
      },
      {
        label: '成立以来基金占净值比(平均值)',
        id: 'fund_ratio',
        type: 'rightTreeData',
        align: 'right',
        fix: '',
        width: '200px',
        noshowoverflowtooltip: true,
        filter: 'numberToFixedStr',
        sortable: true
      },
      {
        label: '成立以来期货占净值比(平均值)',
        id: 'futures_ratio',
        type: 'rightTreeData',
        align: 'right',
        fix: '',
        width: '200px',
        noshowoverflowtooltip: true,
        filter: 'numberToFixedStr',
        sortable: true
      }
    ]
  }
]
