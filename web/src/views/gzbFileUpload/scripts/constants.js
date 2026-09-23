export const TABLE_COLUMNS = [
  {
    title: '上传时间',
    prop: 'uploadTime',
    align: 'center',
    width: '160px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '上传人',
    prop: 'vcOperator',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '文件状态',
    prop: 'vcStatus',
    align: 'center',
    width: '130px',
    showtooltip: true,
    sortable:true

  },
  {
    title: '上传文件名',
    prop: 'vcFilenameOld',
    align: 'center',
    width: '200px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '文件导入明细',
    prop: 'flag',
    align: 'center',
    width: '110px',
    showtooltip: true,
  },
  {
    title: '匹配成功条数',
    prop: 'matchCount',
    align: 'center',
    width: '130px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '匹配失败条数',
    prop: 'noMatchCount',
    align: 'center',
    width: '130px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '数据处理异常',
    prop: 'dataExeStatus',
    align: 'center',
    width: '140px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '数据处理完成时间',
    prop: 'dataExeCompleteTime',
    align: 'center',
    width: '200px',
    showtooltip: true,
    sortable:true
  },
]

export const FILE_RAR_TYPE_OPTIONS=[
  {
    dimCde: '',
    dimNme: '全部'
  },
  /* {
    dimCde: 'GZB',
    dimNme: '估值文件'
  }, */
  {
    dimCde: 'NET',
    dimNme: '净值文件'
  }
]

export const UPLOAD_TIME_OPTIONS= [
  {
    dimCde: 'zero',
    dimNme: '1小时之内'
  },
  {
    dimCde: 'one',
    dimNme: '2小时之内'
  },
  {
    dimCde: 'two',
    dimNme: '今天'
  },
  {
    dimCde: 'three',
    dimNme: '昨天以来'
  },
  {
    dimCde: 'four',
    dimNme: '一星期以来'
  }
]

export const VC_RUN_STATUS_OPTIONS=[
  {
    dimCde: '',
    dimNme: '全部'
  },
  {
    dimCde: 'RUNNING',
    dimNme: '正在执行中'
  },
  {
    dimCde: 'COMPLETED',
    dimNme: '已完成'
  }
]

export const VC_RESULT_FLAG_OPTIONS=[
  {
    dimCde: '',
    dimNme: '全部'
  },
  {
    dimCde: '0',
    dimNme: '成功'
  },
  {
    dimCde: '1',
    dimNme: '失败'
  }
]

export const TABLE_DATA_CLEAR_LOG_COLUMNS = [
  {
    title: '产品代码',
    prop: 'fundCode',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '产品名称',
    prop: 'fundName',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '压缩文件名称',
    prop: 'fileNameRar',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true

  },
  {
    title: '操作人',
    prop: 'operator',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '业务开始日期',
    prop: 'dBusiBeginDate',
    align: 'center',
    width: '125px',
    showtooltip: true,
  },
  {
    title: '业务结束日期',
    prop: 'dBusiEndDate',
    align: 'center',
    width: '125px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '开始执行时间',
    prop: 'dExecBeginDate',
    align: 'center',
    width: '180px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '结束执行时间',
    prop: 'dExecEndDate',
    align: 'center',
    width: '180px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '执行状态',
    prop: 'vcRunStatus',
    align: 'center',
    width: '100px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '执行结果',
    prop: 'vcResultFlag',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
]


export const VC_STATUS_OPTIONS=[
  {
    dimCde: '',
    dimNme: '全部'
  },
  {
    dimCde: '0',
    dimNme: '成功'
  },
  {
    dimCde: '1',
    dimNme: '失败'
  }
]

export const TABLE_DATA_DETAIL_LOG_COLUMNS = [
  {
    title: '产品代码',
    prop: 'vcFundCode',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '编码',
    prop: 'vcCode',
    align: 'center',
    width: '350px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '名称',
    prop: 'vcName',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true

  },
  {
    title: '业务开始日期',
    prop: 'dBusiBeginDate',
    align: 'center',
    width: '125px',
    showtooltip: true,
  },
  {
    title: '业务结束日期',
    prop: 'dBusiEndDate',
    align: 'center',
    width: '125px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '开始执行时间',
    prop: 'dExecBeginDate',
    align: 'center',
    width: '180px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '结束执行时间',
    prop: 'dExecEndDate',
    align: 'center',
    width: '180px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '执行结果',
    prop: 'vcStatus',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
]


export const TABLE_DATA_CHECK_INFO_COLUMNS = [
  {
    title: '产品代码',
    prop: 'fundCode',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '产品名称',
    prop: 'fundName',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '估值日期',
    prop: 'gzDate',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true

  },
  {
    title: '异常类型',
    prop: 'exception',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '异常信息',
    prop: 'exceptioninfo',
    align: 'center',
    width: '125px',
    showtooltip: true,
  },
  {
    title: '完成时间',
    prop: 'completeTime',
    align: 'center',
    width: '125px',
    showtooltip: true,
    sortable:true
  },
]


export const TABLE_DATA_IMPORT_FILE_LOG_COLUMNS = [
  {
    title: '上传时间',
    prop: 'uploadTime',
    align: 'center',
    width: '160px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '产品代码',
    prop: 'vcFundcode',
    align: 'center',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '产品名称',
    prop: 'fundName',
    align: 'center',
    width: '130px',
    showtooltip: true,
    sortable:true

  },
  {
    title: '估值日期',
    prop: 'busiDate',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '估值文件名称',
    prop: 'vcFilenameOld',
    align: 'center',
    width: '200px',
    showtooltip: true,
    sortable:true
  },

  {
    title: '匹配规则',
    prop: 'matchRule',
    align: 'center',
    width: '200px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '匹配状态',
    prop: 'vcStatus',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '导入状态',
    prop: 'impStatus',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '导入异常',
    prop: 'impMsg',
    align: 'center',
    width: '120px',
    showtooltip: true,
    sortable:true
  },
]


export const TABLE_DATA_IMPORT_GZB_DETAIL_LOG_COLUMNS = [
  {
    title: '产品代码',
    prop: 'fundCode',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '估值日期',
    prop: 'gzDate',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '科目编码',
    prop: 'fkmbm',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '科目名称',
    prop: 'fkmmc',
    align: 'left',
    width: '200px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '行情价格',
    prop: 'fhqjg',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '行情标志',
    prop: 'fhqbz',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '证券数量',
    prop: 'fzqsl',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '成本(本位币)',
    prop: 'fzqcb',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '市值(本位币)',
    prop: 'fzqsz',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },

  {
    title: '估值增值(本位币)',
    prop: 'fgzZz',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },

  {
    title: '成本占净值比例',
    prop: 'fcbJzBl',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '市值占净值比例',
    prop: 'fszJzBl',
    align: 'left',
    width: '150px',
    showtooltip: true,
    sortable:true
  },
  {
    title: '停牌信息',
    prop: 'ftpxx',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  },
  {
    title: '权益信息',
    prop: 'fqyxx',
    align: 'left',
    width: '100px',
    showtooltip: true,
    sortable:false
  }


]


