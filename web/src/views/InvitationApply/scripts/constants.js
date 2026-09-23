const TABLE_COLUMNS = [
  {
    label: '产品代码',
    prop: 'fundCode',
    align: 'left',
    width: '70px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '产品名称',
    prop: 'fundName',
    align: 'left',
    width: '200px',
    showtooltip: true
  },
  {
    label: '产品管理人',
    prop: 'nameGlr',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '投资策略',
    prop: 'fofMainStrategyName',
    align: 'center',
    width: '80px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '子策略',
    prop: 'fofSubStrategyName',
    align: 'center',
    width: '80px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '产品成立日期',
    prop: 'createDate',
    align: 'center',
    width: '90px',
    showtooltip: true
  },
  {
    label: '申请意向',
    prop: 'applyIntention',
    align: 'center',
    width: '90px',
    showtooltip: true
  },
  {
    label: '数据频率',
    prop: 'fundFrequency',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '产品运行状态',
    prop: 'operateStatus',
    align: 'center',
    width: '90px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '等级权限',
    prop: 'fundLevel',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '状态',
    prop: 'authStatus',
    align: 'center',
    width: '90px',
    showtooltip: true
  }
]

// 指标适用类型
const ittypeList = [
  { dimNme: '无', dimCde: '0' },
  { dimNme: '已拥有', dimCde: '1' },
  { dimNme: '待审批', dimCde: '2' },
  { dimNme: '已拒绝', dimCde: '3' }
]


export default {
  TABLE_COLUMNS,
  ittypeList,
}
