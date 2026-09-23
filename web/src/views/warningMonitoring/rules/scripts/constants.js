const TABLE_COLUMNS = [
  {
    label: '指标名称',
    prop: 'itcode',
    align: 'left',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '预警规则名称',
    prop: 'rulename',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '监控对象类型',
    prop: 'ittype',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '预警规则',
    prop: 'ruleDesc',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '风险等级',
    prop: 'warnLevel',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '邮件提醒规则',
    prop: 'emailRule',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '备注',
    prop: 'itremark',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '是否启用',
    prop: 'itdisable',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: 'dict'
  },
  {
    label: '修改时间',
    prop: 'updatetime',
    align: 'center',
    width: '100px',
    showtooltip: true
  }
]

// 指标适用类型
const ittypeList = [
  { dimNme: '产品', dimCde: '1' },
  { dimNme: '机构', dimCde: '2' }
]

// 风险等级
const warnLevelList = [
  { dimNme: '低', dimCde: '1', color: '#606266' },
  { dimNme: '中', dimCde: '2', color: '#E6A23C' },
  { dimNme: '高', dimCde: '3', color: '#F56C6C' }
]

// 是否启用
const itdisableList = [
  { dimNme: '是', dimCde: 1 },
  { dimNme: '否', dimCde: 0 }
]

// 邮件提醒规则
const emailRuleList = [
  { dimNme: '首次触发', dimCde: '1' },
  { dimNme: '每次触发', dimCde: '2' }
]

// 运算符
const warnOpList = [
  { dimNme: '大于', dimCde: 1 },
  { dimNme: '大于等于', dimCde: 2 },
  { dimNme: '小于', dimCde: 3 },
  { dimNme: '小于等于', dimCde: 4 },
  { dimNme: '等于', dimCde: 5 }
]

export default {
  TABLE_COLUMNS,
  ittypeList,
  warnLevelList,
  itdisableList,
  emailRuleList,
  warnOpList
}
