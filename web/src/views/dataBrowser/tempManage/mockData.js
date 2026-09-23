// indexDetailInfoTree_list接口的mock数据
export const INDEX_LIST = [
  // 指标数据
  {
    vcId: 'index_001',
    vcPid: '',
    vcIndexName: '业绩指标',
    isIndexOrType: '1',
    fOrder: 1,
    vcTypeCode: 'yjzb',
    vcTypeName: '业绩指标',
    fDimensionMode: '1',
    vcInfoDefineId: 'info_001'
  },
  {
    vcId: 'index_002',
    vcPid: 'index_001',
    vcIndexName: '收益率',
    isIndexOrType: '1',
    fOrder: 2,
    vcTypeCode: 'yjzb',
    vcTypeName: '业绩指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_002'
  },
  {
    vcId: 'index_003',
    vcPid: 'index_001',
    vcIndexName: '波动率',
    isIndexOrType: '1',
    fOrder: 3,
    vcTypeCode: 'yjzb',
    vcTypeName: '业绩指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_003'
  },
  {
    vcId: 'index_004',
    vcPid: '',
    vcIndexName: '风险指标',
    isIndexOrType: '1',
    fOrder: 4,
    vcTypeCode: 'fxzb',
    vcTypeName: '风险指标',
    fDimensionMode: '1',
    vcInfoDefineId: 'info_004'
  },
  {
    vcId: 'index_005',
    vcPid: 'index_004',
    vcIndexName: '最大回撤',
    isIndexOrType: '1',
    fOrder: 5,
    vcTypeCode: 'fxzb',
    vcTypeName: '风险指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_005'
  },
  {
    vcId: 'index_006',
    vcPid: 'index_004',
    vcIndexName: '夏普比率',
    isIndexOrType: '1',
    fOrder: 6,
    vcTypeCode: 'fxzb',
    vcTypeName: '风险指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_006'
  },
  {
    vcId: 'index_007',
    vcPid: 'index_001',
    vcIndexName: '相对收益率',
    isIndexOrType: '1',
    fOrder: 7,
    vcTypeCode: 'yjzb',
    vcTypeName: '业绩指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_007'
  },
  {
    vcId: 'index_008',
    vcPid: 'index_001',
    vcIndexName: '胜率',
    isIndexOrType: '1',
    fOrder: 8,
    vcTypeCode: 'yjzb',
    vcTypeName: '业绩指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_008'
  },
  {
    vcId: 'index_009',
    vcPid: 'index_004',
    vcIndexName: '贝塔系数',
    isIndexOrType: '1',
    fOrder: 7,
    vcTypeCode: 'fxzb',
    vcTypeName: '风险指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_009'
  },
  {
    vcId: 'index_010',
    vcPid: 'index_004',
    vcIndexName: '特雷诺比率',
    isIndexOrType: '1',
    fOrder: 8,
    vcTypeCode: 'fxzb',
    vcTypeName: '风险指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_010'
  },
  {
    vcId: 'index_011',
    vcPid: '',
    vcIndexName: '估值指标',
    isIndexOrType: '1',
    fOrder: 9,
    vcTypeCode: 'gzzb',
    vcTypeName: '估值指标',
    fDimensionMode: '1',
    vcInfoDefineId: 'info_011'
  },
  {
    vcId: 'index_012',
    vcPid: 'index_011',
    vcIndexName: '市盈率(PE)',
    isIndexOrType: '1',
    fOrder: 10,
    vcTypeCode: 'gzzb',
    vcTypeName: '估值指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_012'
  },
  {
    vcId: 'index_013',
    vcPid: 'index_011',
    vcIndexName: '市净率(PB)',
    isIndexOrType: '1',
    fOrder: 11,
    vcTypeCode: 'gzzb',
    vcTypeName: '估值指标',
    fDimensionMode: '2',
    vcInfoDefineId: 'info_013'
  },
  // 时间维度数据
  {
    vcId: 'time_001',
    vcPid: 'index_002',
    vcIndexName: '近一个月',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_001'
  },
  {
    vcId: 'time_002',
    vcPid: 'index_002',
    vcIndexName: '近三个月',
    isIndexOrType: '2',
    fOrder: 2,
    vcTimeId: 'timeid_002'
  },
  {
    vcId: 'time_003',
    vcPid: 'index_002',
    vcIndexName: '近六个月',
    isIndexOrType: '2',
    fOrder: 3,
    vcTimeId: 'timeid_003'
  },
  {
    vcId: 'time_004',
    vcPid: 'index_003',
    vcIndexName: '近一个月',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_001'
  },
  {
    vcId: 'time_005',
    vcPid: 'index_003',
    vcIndexName: '近三个月',
    isIndexOrType: '2',
    fOrder: 2,
    vcTimeId: 'timeid_002'
  },
  {
    vcId: 'time_006',
    vcPid: 'index_005',
    vcIndexName: '近一年',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_004'
  },
  {
    vcId: 'time_007',
    vcPid: 'index_006',
    vcIndexName: '近一年',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_004'
  },
  {
    vcId: 'time_008',
    vcPid: 'index_002',
    vcIndexName: '近一年',
    isIndexOrType: '2',
    fOrder: 4,
    vcTimeId: 'timeid_004'
  },
  {
    vcId: 'time_009',
    vcPid: 'index_002',
    vcIndexName: '成立以来',
    isIndexOrType: '2',
    fOrder: 5,
    vcTimeId: 'timeid_005'
  },
  {
    vcId: 'time_010',
    vcPid: 'index_005',
    vcIndexName: '近六个月',
    isIndexOrType: '2',
    fOrder: 2,
    vcTimeId: 'timeid_003'
  },
  {
    vcId: 'time_011',
    vcPid: 'index_007',
    vcIndexName: '近一个月',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_001'
  },
  {
    vcId: 'time_012',
    vcPid: 'index_007',
    vcIndexName: '近三个月',
    isIndexOrType: '2',
    fOrder: 2,
    vcTimeId: 'timeid_002'
  },
  {
    vcId: 'time_013',
    vcPid: 'index_008',
    vcIndexName: '近一年',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_004'
  },
  {
    vcId: 'time_014',
    vcPid: 'index_009',
    vcIndexName: '近一年',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_004'
  },
  {
    vcId: 'time_015',
    vcPid: 'index_012',
    vcIndexName: '最新',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_006'
  },
  {
    vcId: 'time_016',
    vcPid: 'index_013',
    vcIndexName: '最新',
    isIndexOrType: '2',
    fOrder: 1,
    vcTimeId: 'timeid_006'
  },
  // 明细维度数据
  {
    vcId: 'detail_001',
    vcPid: 'index_002',
    vcIndexName: '基金',
    isIndexOrType: '3',
    fOrder: 1,
    vcItemId: 'detailid_001'
  },
  {
    vcId: 'detail_002',
    vcPid: 'index_002',
    vcIndexName: '债券',
    isIndexOrType: '3',
    fOrder: 2,
    vcItemId: 'detailid_002'
  },
  {
    vcId: 'detail_003',
    vcPid: 'index_003',
    vcIndexName: '基金',
    isIndexOrType: '3',
    fOrder: 1,
    vcItemId: 'detailid_001'
  },
  {
    vcId: 'detail_004',
    vcPid: 'index_003',
    vcIndexName: '债券',
    isIndexOrType: '3',
    fOrder: 2,
    vcItemId: 'detailid_002'
  },
  {
    vcId: 'detail_005',
    vcPid: 'index_002',
    vcIndexName: '股票',
    isIndexOrType: '3',
    fOrder: 3,
    vcItemId: 'detailid_003'
  },
  {
    vcId: 'detail_006',
    vcPid: 'index_002',
    vcIndexName: '现金',
    isIndexOrType: '3',
    fOrder: 4,
    vcItemId: 'detailid_004'
  },
  {
    vcId: 'detail_007',
    vcPid: 'index_007',
    vcIndexName: '基金',
    isIndexOrType: '3',
    fOrder: 1,
    vcItemId: 'detailid_001'
  },
  {
    vcId: 'detail_008',
    vcPid: 'index_009',
    vcIndexName: '基金',
    isIndexOrType: '3',
    fOrder: 1,
    vcItemId: 'detailid_001'
  },
  // 单位维度数据
  {
    vcId: 'unit_001',
    vcPid: 'index_002',
    vcIndexName: '%',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_001',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_002',
    vcPid: 'index_003',
    vcIndexName: '%',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_001',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_003',
    vcPid: 'index_005',
    vcIndexName: '%',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_001',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'original',
    vcPid: 'index_006',
    vcIndexName: '原值',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_002',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_004',
    vcPid: 'index_007',
    vcIndexName: '%',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_001',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_005',
    vcPid: 'index_008',
    vcIndexName: '%',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_001',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_006',
    vcPid: 'index_009',
    vcIndexName: '原值',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_002',
    vcFormat: '0.0000',
    vcScale: '4'
  },
  {
    vcId: 'unit_007',
    vcPid: 'index_010',
    vcIndexName: '原值',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_002',
    vcFormat: '0.0000',
    vcScale: '4'
  },
  {
    vcId: 'unit_008',
    vcPid: 'index_012',
    vcIndexName: '倍',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_003',
    vcFormat: '0.00',
    vcScale: '2'
  },
  {
    vcId: 'unit_009',
    vcPid: 'index_013',
    vcIndexName: '倍',
    isIndexOrType: '4',
    fOrder: 1,
    vcUnitId: 'unitid_003',
    vcFormat: '0.00',
    vcScale: '2'
  }
]


export const EDIT_COL_LIST = [
  {
    "fColOrder": 1,
    "vcColName": "收益率_基金_近一个月(%)",
    "vcColCode": "index_002_detail_001_time_001",
    "vcInfoDefineId": "info_002",
    "vcIndexCode": "index_002",
    "vcUnitType": "unit_001",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_001",
    "vcTimeDefineId": "timeid_001",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 2,
    "vcColName": "收益率_债券_近一个月(%)",
    "vcColCode": "index_002_detail_002_time_001",
    "vcInfoDefineId": "info_002",
    "vcIndexCode": "index_002",
    "vcUnitType": "unit_001",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_002",
    "vcTimeDefineId": "timeid_001",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 3,
    "vcColName": "波动率_基金_近一个月(%)",
    "vcColCode": "index_003_detail_003_time_004",
    "vcInfoDefineId": "info_003",
    "vcIndexCode": "index_003",
    "vcUnitType": "unit_002",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_001",
    "vcTimeDefineId": "timeid_001",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 4,
    "vcColName": "收益率_基金_近三个月(%)",
    "vcColCode": "index_002_detail_001_time_002",
    "vcInfoDefineId": "info_002",
    "vcIndexCode": "index_002",
    "vcUnitType": "unit_001",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_001",
    "vcTimeDefineId": "timeid_002",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 5,
    "vcColName": "收益率_债券_近三个月(%)",
    "vcColCode": "index_002_detail_002_time_002",
    "vcInfoDefineId": "info_002",
    "vcIndexCode": "index_002",
    "vcUnitType": "unit_001",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_002",
    "vcTimeDefineId": "timeid_002",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 6,
    "vcColName": "波动率_基金_近三个月(%)",
    "vcColCode": "index_003_detail_003_time_005",
    "vcInfoDefineId": "info_003",
    "vcIndexCode": "index_003",
    "vcUnitType": "unit_002",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "detailid_001",
    "vcTimeDefineId": "timeid_002",
    "vcTypeCode": "yjzb",
    "vcTypeName": "业绩指标",
    "vcModelValue": ""
  },
  {
    "fColOrder": 7,
    "vcColName": "最大回撤_近一年(%)",
    "vcColCode": "index_005_time_006",
    "vcInfoDefineId": "info_005",
    "vcIndexCode": "index_005",
    "vcUnitType": "unit_003",
    "vcUnitDefineId": "unitid_001",
    "vcFormat": "0.00",
    "vcScale": "2",
    "vcItemDefineId": "",
    "vcTimeDefineId": "timeid_004",
    "vcTypeCode": "fxzb",
    "vcTypeName": "风险指标",
    "vcModelValue": ""
  }
]