const TABLE_COLUMNS = [
  {
    label: '监控对象代码',
    prop: 'objcode',
    align: 'left',
    width: '120px',
    showtooltip: true
  },
  {
    label: '监控对象名称',
    prop: 'objname',
    align: 'left',
    width: '120px',
    showtooltip: true
  },
  {
    label: '管理人名称',
    prop: 'mgrname',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '预警规则名称',
    prop: 'rulesname',
    align: 'left',
    width: '120px',
    showtooltip: true
  },
  {
    label: '业务日期',
    prop: 'fdate',
    align: 'center',
    width: '100px',
    showtooltip: true
  },
  {
    label: '风险等级',
    prop: 'warnLevel',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: "dict"
  },
  {
    label: '触发状态',
    prop: 'warnStatus',
    align: 'center',
    width: '100px',
    showtooltip: true,
    format: "dict"
  },
  {
    label: '连续预警天数',
    prop: 'warnDays',
    align: 'center',
    width: '120px',
    showtooltip: true
  },
  {
    label: '邮件提醒',
    prop: 'sendemail',
    align: 'center',
    width: '100px',
    showtooltip: true,
    // format: "dict"
  },
  {
    label: '生成时间',
    prop: 'createdate',
    align: 'center',
    width: '100px',
    showtooltip: true
  },
];
// 触发状态
const warnStatusList = [
  { dimNme: "正常", dimCde: "0", color: "#67C23A" },
  { dimNme: "预警", dimCde: "1", color: "#F56C6C" },
]
// 风险等级
const warnLevelList = [
  { dimNme: "高", dimCde: "3", color: "#F56C6C" },
  { dimNme: "中", dimCde: "2", color: "#E6A23C" },
  { dimNme: "低", dimCde: "1", color: "#606266" },
]
// 监控对象类型
const ittypeList = [
  { dimNme: "产品", dimCde: "1" },
  { dimNme: "机构", dimCde: "2" },
]
// 邮件提醒
const sendemailList = [
  { dimCde: "0", dimNme: "否" },
  { dimCde: "1", dimNme: "是" },
]

export default {
  TABLE_COLUMNS,
  warnStatusList,
  warnLevelList,
  ittypeList,
  sendemailList,
}
