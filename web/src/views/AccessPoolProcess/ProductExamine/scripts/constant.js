export const STATUS_COLOR_MAP = [
  {
    color: '#FFC000',
    value: '0',
    status: 'warning'
  },
  {
    color: '#FFC000',
    value: '1'
  },
  {
    color: '#70AD47',
    value: '4',
    status: 'success'
  },
  {
    color: '#FF0000',
    value: '5',
    status: 'danger'
  }
]

export const TABLE_COLUMNS = [
  {
    prop: 'fundCode',
    label: '产品代码',
    align: 'center'
  },
  {
    prop: 'fundName',
    label: '产品名称',
    align: 'left',
    width: '200px'
  },
  {
    prop: 'managerName',
    label: '管理人名称',
    align: 'left'
  },
  {
    prop: 'amount',
    label: '规模（万元）',
    align: 'right',
    width: '150px'
  },
  {
    prop: 'createDate',
    label: '成立日期',
    align: 'center'
  },
  {
    prop: 'strategy',
    label: '策略类型',
    align: 'center'
  },
  {
    prop: 'status',
    label: '审批状态',
    align: 'center'
  },
  {
    prop: 'creatorName',
    label: '提交人',
    align: 'center'
  },
  {
    prop: 'submitDate',
    label: '提交时间',
    align: 'center'
  },
  {
    prop: 'remark',
    label: '备注',
    align: 'center'
  }
]

export const EXAMINE_TABLE_COLUMNS = [
  {
    prop: 'fileName',
    align: 'center',
    label: '文件名称',
    width: ''
  },
  {
    prop: 'note',
    align: 'center',
    label: '补充说明',
    width: ''
  },
  {
    prop: 'remark',
    align: 'center',
    label: '审批意见',
    width: ''
  }
]

export const EXAMINE_TABLE_DATA = [
  {
    index: '1',
    fileName: 'xeqsqd.doc',
    explain: '对该产品提出补充说明',
    opinion: '对该产品的审批意见'
  }
]

export const EXAMINE_RESULT_OPTIONS = [
  {
    DIM_CDE: '4',
    DIM_NME: '准入'
  },
  {
    DIM_CDE: '5',
    DIM_NME: '退回'
  }
]
