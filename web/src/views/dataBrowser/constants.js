// 模板类型
const TEMPTYPE = [
  { dimCde: "A", dimNme: "单产品" },
  // { dimCde: "B", dimNme: "组合汇总" },
  { dimCde: "C", dimNme: "组合对比" },
  { dimCde: "D", dimNme: "个券模板" },
]
// 时间频率
const TIMEFREQUENCY = [
  { dimCde: "day", dimNme: "日度", weight: 1 },
  { dimCde: "week", dimNme: "周度", weight: 2 },
  { dimCde: "month", dimNme: "月度", weight: 3 },
  { dimCde: "quarter", dimNme: "季度", weight: 4 },
]
// 数据频率
const DATAFREQUENCY = [
  { dimCde: "day", dimNme: "日频", weight: 1 },
  { dimCde: "week", dimNme: "周频", weight: 2 },
  { dimCde: "month", dimNme: "月频", weight: 3 },
  { dimCde: "quarter", dimNme: "季频", weight: 4 },
]
// 日期类型
const DATETYPE = [
  { dimCde: "workDate", dimNme: "交易日" },
]

const EXPORTTYPE = [
  { dimCde: '1', dimNme: 'sheet展示' },
  { dimCde: '2', dimNme: '排列展示' },
  { dimCde: '3', dimNme: '独立excel' },
]

const EXPORTTYPE_D = [
  { dimCde: '2', dimNme: '排列展示' },
  { dimCde: '3', dimNme: '独立excel' },
]

const TEMPCOLBEFORE1 = [
  {
    title: '日期',
    // dataIndex: 'before_date',
    dataIndex: 'TDATE',
    vcInfoDefineId: 'before_date_id',
    pId: 'before_code',
    unit: '',
    vcUnitDefineId: 'before_date_unit_id',
    vcFormat: '',
    vcScale: '',
    vcItemId: 'before_date_item_id',
    vcTimeId: 'before_date_time_id',
    vcTypeCode: '',
    vcTypeName: ''
  },
  {
    title: '产品',
    // dataIndex: 'before_fund_name',
    dataIndex: 'FCODE',
    vcInfoDefineId: 'before_fund_name_id',
    pId: 'before_code',
    unit: '',
    vcUnitDefineId: 'before_fund_name_unit_id',
    vcFormat: '',
    vcScale: '',
    vcItemId: 'before_fund_name_item_id',
    vcTimeId: 'before_fund_name_time_id',
    vcTypeCode: '',
    vcTypeName: ''
  },
]

const TEMPCOLBEFORE = [
  {
    title: '产品',
    dataIndex: 'FCODE',
    vcInfoDefineId: 'before_fund_code_id',
    pId: 'before_code',
    unit: '',
    vcUnitDefineId: 'before_fund_code_unit_id',
    vcFormat: '',
    vcScale: '',
    vcItemId: 'before_fund_code_item_id',
    vcTimeId: 'before_fund_code_time_id',
    vcTypeCode: '',
    vcTypeName: ''
  },
  // {
  //   title: '产品名称',
  //   dataIndex: 'before_fund_name',
  //   vcInfoDefineId: 'before_fund_name_id',
  //   pId: 'before_code',
  //   unit: '',
  //   vcUnitDefineId: 'before_fund_name_unit_id',
  //   vcFormat: '',
  //   vcScale: '',
  //   vcItemId: 'before_fund_name_item_id',
  //   vcTimeId: 'before_fund_name_time_id',
  //   vcTypeCode: '',
  //   vcTypeName: ''
  // },
]

const TEMPCOLBEFORE2 = {
  "ggzb": [
    {
      title: '标的代码',
      dataIndex: 'VC_SYMBOL_ggzb',
      vcInfoDefineId: 'ggzb_bd_code_id',
      pId: 'ggzb',
      unit: '',
      vcUnitDefineId: 'ggzb_bd_code_unit_id',
      vcFormat: '',
      vcScale: '',
      vcItemId: 'ggzb_bd_code_item_id',
      vcTimeId: 'ggzb_bd_code_time_id',
      vcTypeCode: 'ggzb',
      vcTypeName: '个股指标'
    },
    // {
    //   title: '标的名称',
    //   dataIndex: 'symbolName_ggzb',
    //   vcInfoDefineId: 'ggzb_bd_name_id',
    //   pId: 'ggzb',
    //   unit: '',
    //   vcUnitDefineId: 'ggzb_bd_name_unit_id',
    //   vcFormat: '',
    //   vcScale: '',
    //   vcItemId: 'ggzb_bd_name_item_id',
    //   vcTimeId: 'ggzb_bd_name_time_id',
    //   vcTypeCode: 'ggzb',
    //   vcTypeName: '个股指标'
    // },
  ],
  "gzzb": [
    {
      title: '标的代码',
      dataIndex: 'VC_SYMBOL_gzzb',
      vcInfoDefineId: 'gzzb_bd_code_id',
      pId: 'gzzb',
      unit: '',
      vcUnitDefineId: 'gzzb_bd_code_unit_id',
      vcFormat: '',
      vcScale: '',
      vcItemId: 'gzzb_bd_code_item_id',
      vcTimeId: 'gzzb_bd_code_time_id',
      vcTypeCode: 'gzzb',
      vcTypeName: '个债指标'
    },
    // {
    //   title: '标的名称',
    //   dataIndex: 'symbolName_gzzb',
    //   vcInfoDefineId: 'gzzb_bd_name_id',
    //   pId: 'gzzb',
    //   unit: '',
    //   vcUnitDefineId: 'gzzb_bd_name_unit_id',
    //   vcFormat: '',
    //   vcScale: '',
    //   vcItemId: 'gzzb_bd_name_item_id',
    //   vcTimeId: 'gzzb_bd_name_time_id',
    //   vcTypeCode: 'gzzb',
    //   vcTypeName: '个债指标'
    // },
  ],
  "pzzb": [
    {
      title: '标的代码',
      dataIndex: 'VC_SYMBOL_pzzb',
      vcInfoDefineId: 'pzzb_bd_code_id',
      pId: 'pzzb',
      unit: '',
      vcUnitDefineId: 'pzzb_bd_code_unit_id',
      vcFormat: '',
      vcScale: '',
      vcItemId: 'pzzb_bd_code_item_id',
      vcTimeId: 'pzzb_bd_code_time_id',
      vcTypeCode: 'pzzb',
      vcTypeName: '品种指标'
    },
    // {
    //   title: '标的名称',
    //   dataIndex: 'symbolName_pzzb',
    //   vcInfoDefineId: 'pzzb_bd_name_id',
    //   pId: 'pzzb',
    //   unit: '',
    //   vcUnitDefineId: 'pzzb_bd_name_unit_id',
    //   vcFormat: '',
    //   vcScale: '',
    //   vcItemId: 'pzzb_bd_name_item_id',
    //   vcTimeId: 'pzzb_bd_name_time_id',
    //   vcTypeCode: 'pzzb',
    //   vcTypeName: '品种指标'
    // },
  ],
  "gjzb": [
    {
      title: '标的代码',
      dataIndex: 'VC_SYMBOL_gjzb',
      vcInfoDefineId: 'gjzb_bd_code_id',
      pId: 'gjzb',
      unit: '',
      vcUnitDefineId: 'gjzb_bd_code_unit_id',
      vcFormat: '',
      vcScale: '',
      vcItemId: 'gjzb_bd_code_item_id',
      vcTimeId: 'gjzb_bd_code_time_id',
      vcTypeCode: 'gjzb',
      vcTypeName: '个基指标'
    },
    // {
    //   title: '标的名称',
    //   dataIndex: 'symbolName_gjzb',
    //   vcInfoDefineId: 'gjzb_bd_name_id',
    //   pId: 'gjzb',
    //   unit: '',
    //   vcUnitDefineId: 'gjzb_bd_name_unit_id',
    //   vcFormat: '',
    //   vcScale: '',
    //   vcItemId: 'gjzb_bd_name_item_id',
    //   vcTimeId: 'gjzb_bd_name_time_id',
    //   vcTypeCode: 'gjzb',
    //   vcTypeName: '个基指标'
    // },
  ],
  "more": [
    {
      title: '标的代码',
      dataIndex: 'VC_SYMBOL_more',
      vcInfoDefineId: 'more_bd_code_id',
      pId: 'more',
      unit: '',
      vcUnitDefineId: 'more_bd_code_unit_id',
      vcFormat: '',
      vcScale: '',
      vcItemId: 'more_bd_code_item_id',
      vcTimeId: 'more_bd_code_time_id',
      vcTypeCode: 'more',
      vcTypeName: '其他'
    },
    // {
    //   title: '标的名称',
    //   dataIndex: 'symbolName_more',
    //   vcInfoDefineId: 'more_bd_name_id',
    //   pId: 'more',
    //   unit: '',
    //   vcUnitDefineId: 'more_bd_name_unit_id',
    //   vcFormat: '',
    //   vcScale: '',
    //   vcItemId: 'more_bd_name_item_id',
    //   vcTimeId: 'more_bd_name_time_id',
    //   vcTypeCode: 'more',
    //   vcTypeName: '其他'
    // },
  ],
}

export default {
  TEMPTYPE,
  TIMEFREQUENCY,
  DATAFREQUENCY,
  DATETYPE,
  EXPORTTYPE,
  EXPORTTYPE_D,
  TEMPCOLBEFORE,
  TEMPCOLBEFORE1,
  TEMPCOLBEFORE2
}