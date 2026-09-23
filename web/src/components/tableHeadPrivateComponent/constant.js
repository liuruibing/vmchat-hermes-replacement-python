// 维护动态列头的固定数据

export const leftTreeData = [
  {
    label: '基本信息',
    id: 'jbxx',
    type: 'leftTreeData',
    children: [
      // {
      //   label: '业务日期',
      //   disabled: false,
      //   id: 'endDate',
      //   type: 'leftTreeData',
      //   align: 'center',
      //   fix: '',
      //   width: '110px',
      //   noshowoverflowtooltip: true,
      //   filter: '',
      //   sortable: true
      // },
      {
        label: '备案编码',
        disabled: true,
        id: 'reg_code',
        type: 'leftTreeData',
        align: 'center',
        fix: 'left',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '管理人简称',
        id: 'manager_name',
        disabled: false,
        type: 'leftTreeData',
        align: 'center',
        fix: 'left',
        width: '120px',
        noshowoverflowtooltip: true,
        filter: 'manager',
        sortable: true
      },
      {
        label: '公司ID',
        id: 'company_id',
        disabled: false,
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '120px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '统一社会信用代码',
        id: 'credit_code',
        disabled: false,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '160px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '管理人名称',
        id: 'manager_full_name',
        disabled: true,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '150px',
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
        fix: 'left',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: 'echarts',
        sortable: false
      },
      {
        label: '公司类型',
        id: 'company_type',
        disabled: false,
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '120px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '成立日期',
        id: 'company_found_date',
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
        label: '注册城市',
        id: 'register_city',
        disabled: false,
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '公司注册资本(万)',
        id: 'capital',
        disabled: false,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '180px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '备案日期',
        id: 'record_date',
        disabled: false,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '备案状态',
        id: 'record_status',
        disabled: false,
        type: 'leftTreeData',
        align: 'center',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '办公城市',
        id: 'work_city',
        disabled: false,
        type: 'leftTreeData',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      }
    ]
  }
]

export const centerTreeDataLeft = [
  {
    label: '公司概况',
    id: 'gsgk',
    children: [
      {
        label: '公司状态',
        id: 'company_status',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '员工人数',
        id: 'employee_count',
        type: 'centerTreeDataLeft',
        align: 'center',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '核心人物',
        id: 'key_person',
        type: 'centerTreeDataLeft',
        align: 'center',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '是否会员',
        id: 'is_member',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '会员类型',
        id: 'member_type',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '管理规模区间',
        id: 'managerAsset',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '130px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '产品总数',
        id: 'fund_count',
        type: 'centerTreeDataLeft',
        align: 'left',
        fix: '',
        width: '100px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      }
    ]
  }
]

export const centerTreeDataRight = [
  {
    label: '净值指标',
    id: 'jzzb',
    children: [
      {
        label: '策略类型',
        id: 'policy_type',
        type: 'centerTreeDataRight',
        align: 'left',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '净值日期',
        id: 'navDate',
        type: 'centerTreeDataRight',
        align: 'left',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: '',
        sortable: true
      },
      {
        label: '单位净值',
        id: 'unitNav',
        type: 'centerTreeDataRight',
        align: 'left',
        fix: '',
        width: '110px',
        noshowoverflowtooltip: true,
        filter: 'moneyYuan4',
        sortable: true
      }
    ]
  }
]

export const rightTreeData = [
  {
    label: '业绩指标',
    id: 'yjzb',
    children: [
      // {
      //   label: '近一月',
      //   id: 'j1y',
      //   children: [
      //     {
      //       label: '近一月收益率',
      //       id: 'm1_return',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     },
      //     {
      //       label: '近一个月波动率',
      //       id: 'm1_stdev',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     },
      //     {
      //       label: '近一月最大回撤',
      //       id: 'm1_max_retracement',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     },
      //     {
      //       label: '近一月Sharpe比率',
      //       id: 'm1_sharpe',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     },
      //     {
      //       label: '近一月Sortino比率',
      //       id: 'm1_sortino',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     },
      //     {
      //       label: '近一月Treynor比率',
      //       id: 'm1_terynor',
      //       type: 'rightTreeData',
      //       align: 'right',
      //       fix: '',
      //       width: '100px',
      //       noshowoverflowtooltip: true,
      //       filter: 'numberToFixedStr',
      //       sortable: true
      //     }
      //   ]
      // },
      {
        label: '近六月',
        id: 'j6y',
        children: [
          {
            label: '近六月收益率',
            id: 'm6_return',
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Calmar比率',
            id: 'm6_calmar',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Alpha',
            id: 'm6_alpha',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Beta',
            id: 'm6_beta',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月信息比率',
            id: 'm6_info',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '140px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月投资胜率',
            id: 'm6_winrate',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '100px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近六月Treynor比率',
            id: 'm6_terynor',
            type: 'rightTreeData',
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
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年波动率',
            id: 'y1_stdev',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年最大回撤',
            id: 'y1_max_retracement',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Sharpe比率',
            id: 'y1_sharpe',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Sortino比率',
            id: 'y1_sortino',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Calmar比率',
            id: 'y1_calmar',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Alpha',
            id: 'y1_alpha',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Beta',
            id: 'y1_beta',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年信息比率',
            id: 'y1_info',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年投资胜率',
            id: 'y1_winrate',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '近一年Treynor比率',
            id: 'y1_terynor',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '130px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          }
          // {
          //   label: '近一年Jenson指数',
          //   id: 'y1_jensen',
          //   type: 'centerTreeDataRight',
          //   align: 'right',
          //   fix: '',
          //   width: '100px',
          //   noshowoverflowtooltip: true,
          //   filter: 'numberToFixedStr',
          //   sortable: true
          // },
        ]
      },
      {
        label: '今年以来',
        id: 'jnyl',
        children: [
          {
            label: '今年以来收益率',
            id: 'ytd_return',
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Beta',
            id: 'ytd_beta',
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来信息比率',
            id: 'ytd_info',
            type: 'rightTreeData',
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
            type: 'rightTreeData',
            align: 'right',
            fix: '',
            width: '120px',
            noshowoverflowtooltip: true,
            filter: 'numberToFixedStr',
            sortable: true
          },
          {
            label: '今年以来Treynor比率',
            id: 'ytd_terynor',
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
            type: 'rightTreeData',
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
