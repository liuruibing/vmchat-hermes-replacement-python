// 报表订阅查询 - 表格列配置
const TABLE_COLUMNS = [
  {
    label: '服务平台日期',
    prop: 'fyptUpdateDate',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '执行状态',
    prop: 'statusName',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '报告生成状态',
    prop: 'reportStatusName',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '产品名称',
    prop: 'fundName',
    align: 'left',
    width: '250px',
    showtooltip: true
  },
  {
    label: '产品代码',
    prop: 'fundCode',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '管理人名称',
    prop: 'glrName',
    align: 'left',
    width: '250px',
    showtooltip: true
  },
  {
    label: '报告开始日期',
    prop: 'beginDate',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '报告结束日期',
    prop: 'endDate',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '模板名称',
    prop: 'templateName',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '模板编码',
    prop: 'templateId',
    align: 'left',
    width: '300px',
    showtooltip: true
  },
  {
    label: '脱敏标志',
    prop: 'desensitizationFlag',
    align: 'left',
    width: '100px',
    showtooltip: true
  },
  {
    label: '脱敏方法',
    prop: 'desensitizationFun',
    align: 'left',
    width: '100px',
    showtooltip: true
  }
]

// 扩展列（有REPORTDATA权限时显示）
const TABLE_COLUMNS_EXTEND = [
  {
    label: '开始执行时间',
    prop: 'reportExecBeginDate',
    align: 'left',
    width: '180px',
    showtooltip: true
  },
  {
    label: '结束执行时间',
    prop: 'reportExecEndDate',
    align: 'left',
    width: '180px',
    showtooltip: true
  },
  {
    label: '报告结果状态',
    prop: 'reportResultName',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '报告执行结果',
    prop: 'reportReason',
    align: 'left',
    width: '130px',
    showtooltip: true
  },
  {
    label: '文件状态',
    prop: 'reportPdfValidName',
    align: 'left',
    width: '100px',
    showtooltip: true
  }
]

// 执行状态
const STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '已执行', value: '1' },
  { label: '未执行', value: '0' }
]

// 报告生成状态
const REPORT_STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '已生成', value: '1' },
  { label: '未生成', value: '0' },
  { label: '执行中', value: '2' }
]

// 报告结果状态
const REPORT_RESULT_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '0' },
  { label: '失败', value: '1' }
]

// 文件状态
const REPORT_PDF_VALID_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '1' },
  { label: '损坏', value: '0' }
]

// 日期状态
const DATE_STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '0' },
  { label: '非法', value: '1' }
]

export default {
  TABLE_COLUMNS,
  TABLE_COLUMNS_EXTEND,
  STATUS_LIST,
  REPORT_STATUS_LIST,
  REPORT_RESULT_LIST,
  REPORT_PDF_VALID_LIST,
  DATE_STATUS_LIST
}
