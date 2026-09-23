// 批量报告导出查询 - 表格列配置
const TABLE_COLUMNS = [
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
    width: '140px',
    showtooltip: true
  },
  {
    label: '创建人',
    prop: 'creatorName',
    align: 'left',
    width: '110px',
    showtooltip: true
  },
  {
    label: '创建日期',
    prop: 'createDate',
    align: 'left',
    width: '180px',
    showtooltip: true
  },
  {
    label: '服务平台状态',
    prop: 'reportFwptStatusName',
    align: 'left',
    width: '140px',
    showtooltip: true
  },
  {
    label: '备注',
    prop: 'remark',
    align: 'left',
    width: '160px',
    showtooltip: true
  }
]

// 扩展列（有 REPORTDATA 权限时显示）
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
    width: '140px',
    showtooltip: true
  },
  {
    label: '报告执行结果',
    prop: 'reportReason',
    align: 'left',
    width: '140px',
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

const REPORT_FWPT_STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '显示', value: '1' },
  { label: '隐藏', value: '0' }
]

const REPORT_STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '已生成', value: '1' },
  { label: '未生成', value: '0' },
  { label: '执行中', value: '2' }
]

const REPORT_RESULT_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '0' },
  { label: '失败', value: '1' }
]

const REPORT_PDF_VALID_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '1' },
  { label: '损坏', value: '0' }
]

const DATE_STATUS_LIST = [
  { label: '全部', value: '' },
  { label: '正常', value: '0' },
  { label: '非法', value: '1' }
]

const DESENSITIZATION_FLAG_LIST = [
  { label: '脱敏', value: 'true' },
  { label: '不脱敏', value: 'false' }
]

const DESENSITIZATION_FUN_LIST = [
  { label: '不显示名称、代码', value: 'ALL' },
  { label: '仅屏蔽部分字符', value: 'PART' }
]

const BENCH_TYPE_LIST = [
  { label: '无基准', value: '0' },
  { label: '单基准', value: '1' },
  { label: '复合基准', value: '2' }
]
const INDUSTRY_TYPE_LIST = [
  { label: '申万行业', value: 'SWSR' },
  { label: '中信行业', value: 'ZXSR' }
]
const FACTOR_TYPE_LIST = [
  { label: 'CNE5', value: 'CNE5' },
  { label: 'CNE6', value: 'CNE6' }
]

const DATA_FREQ_LIST = [
  { label: '日频', value: '1' },
  { label: '周频', value: '2' },
  { label: '月频', value: '3' }
]


export default {
  TABLE_COLUMNS,
  TABLE_COLUMNS_EXTEND,
  REPORT_FWPT_STATUS_LIST,
  REPORT_STATUS_LIST,
  REPORT_RESULT_LIST,
  REPORT_PDF_VALID_LIST,
  DATE_STATUS_LIST,
  DESENSITIZATION_FLAG_LIST,
  DESENSITIZATION_FUN_LIST,
  BENCH_TYPE_LIST,
  INDUSTRY_TYPE_LIST,
  FACTOR_TYPE_LIST,
  DATA_FREQ_LIST
}
