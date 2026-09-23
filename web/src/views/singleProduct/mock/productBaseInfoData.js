export const productBaseInfoData = [
  {
    label: '产品名称',
    value: '',
    field: 'YDATE1'
  },
  {
    label: '投资经理',
    value: '',
    field: 'YDATE2'
  },
  {
    label: '产品简称',
    value: '',
    field: 'YDATE3'
  },
  {
    label: '投资顾问',
    value: '',
    field: 'YDATE4'
  },
  {
    label: '备案编号',
    value: '',
    field: 'YDATE5'
  },
  {
    label: '发行机构',
    value: '',
    field: 'YDATE6'
  },
  {
    label: '备案日期',
    value: '',
    field: 'YDATE7'
  },
  {
    label: '托管机构',
    value: '',
    field: 'YDATE8'
  },
  {
    label: '成立日期',
    value: '',
    field: 'YDATE9'
  },
  {
    label: '证券经纪人',
    value: '',
    field: 'YDATE10'
  },
  {
    label: '运行状态',
    value: '',
    field: 'YDATE11'
  },
  {
    label: '期货经理人',
    value: '',
    field: 'YDATE12'
  },
  {
    label: '净值披露频率',
    value: '',
    field: 'YDATE13'
  },
  {
    label: '外包机构',
    value: '',
    field: 'YDATE'
  },
  {
    label: '一级策略',
    value: '',
    field: 'YDATE14'
  },
  {
    label: '基金管理公司',
    value: '',
    field: 'YDATE15'
  },
  {
    label: '二级策略',
    value: '',
    field: 'YDATE16'
  },
  {
    label: '行政管理人',
    value: '',
    field: 'YDATE17'
  },
  {
    label: '开放日',
    value: '',
    field: 'YDATE18'
  },
  {
    label: '法律顾问',
    value: '',
    field: 'YDATE19'
  },
  {
    label: '封闭期',
    value: '',
    field: 'YDATE20'
  },
  {
    label: '审计机构',
    value: '',
    field: 'YDATE21'
  },
  {
    label: '募集方式',
    value: '',
    field: 'YDATE22'
  },
  {
    label: '是否分级',
    value: '',
    field: 'YDATE23'
  },
  {
    label: '管理类型',
    value: '',
    field: 'YDATE24'
  },
  {
    label: '基金形式',
    value: '',
    field: 'YDATE25'
  }
]

export const productBaseRateData = {
  a: [
    {
      label: '产品简称',
      valie: '',
      field: 'YDATE1'
    },
    {
      label: '初始规模（万元）',
      valie: '',
      field: 'YDATE2'
    },
    {
      label: '最低认购额（万元）',
      valie: '',
      field: 'YDATE3'
    },
    {
      label: '最低追加额（万元）',
      valie: '',
      field: 'YDATE4'
    },
    {
      label: '最高认购费（%）',
      valie: '',
      field: 'YDATE5'
    },
    {
      label: '最高赎回费（%）',
      valie: '',
      field: 'YDATE6'
    },
    {
      label: '认（申）购费说明',
      valie: '',
      field: 'YDATE7'
    }
  ],
  b: [
    {
      label: '赎回费说明',
      valie: '',
      field: 'YDATE8'
    }
  ],
  c: [
    {
      label: '申购费率',
      valie: '',
      field: 'YDATE9'
    },
    {
      label: '业绩报酬（%）',
      valie: '',
      field: 'YDATE10'
    },
    {
      label: '申购费率说明',
      valie: '',
      field: 'YDATE11'
    }
  ],
  d: [
    {
      label: '业绩报酬说明',
      valie: '',
      field: 'YDATE12'
    }
  ],
  e: [
    {
      label: '投资顾问费（%）',
      valie: '',
      field: 'YDATE13'
    },
    {
      label: '管理人管理费（%）',
      valie: '',
      field: 'YDATE14'
    },
    {
      label: '托管费（%）',
      valie: '',
      field: 'YDATE15'
    },
    {
      label: '分红方式',
      valie: '',
      field: 'YDATE16'
    }
  ]
}

export const productLevelData = [
  {
    id: 'line01',
    time: '一年',
    fundLevel: 2,
    earnLevel: 2,
    riskLevel: 'R',
    styleCategory: 'B'
  },
  {
    id: 'line02',
    time: '两年',
    fundLevel: 2,
    earnLevel: 2,
    riskLevel: 'R',
    styleCategory: 'B'
  },
  {
    id: 'line03',
    time: '三年',
    fundLevel: 2,
    earnLevel: 2,
    riskLevel: 'R',
    styleCategory: 'B'
  },
  {
    id: 'line04',
    time: '四年',
    fundLevel: 2,
    earnLevel: 2,
    riskLevel: 'R',
    styleCategory: 'B'
  },
  {
    id: 'line05',
    time: '五年',
    fundLevel: 2,
    earnLevel: 2,
    riskLevel: 'R',
    styleCategory: 'B'
  }
]

const levelFilter = val => {
  switch (val) {
    case 5:
      return 1
    case 4:
      return 2
    case 3:
      return 3
    case 2:
      return 4
    case 1:
      return 5
    default:
      return 0
  }
}

export const handleProductLevelData = data => {
  productLevelData[0].fundLevel = levelFilter(Number(data.YDATE1)) || 0
  productLevelData[0].earnLevel = levelFilter(Number(data.YDATE2)) || 0
  productLevelData[0].riskLevel = data.YDATE3 || '-'
  productLevelData[0].styleCategory = data.YDATE4 || '-'

  productLevelData[1].fundLevel = levelFilter(Number(data.YDATE5)) || 0
  productLevelData[1].earnLevel = levelFilter(Number(data.YDATE6)) || 0
  productLevelData[1].riskLevel = data.YDATE7 || '-'
  productLevelData[1].styleCategory = data.YDATE8 || '-'

  productLevelData[2].fundLevel = levelFilter(Number(data.YDATE9)) || 0
  productLevelData[2].earnLevel = levelFilter(Number(data.YDATE10)) || 0
  productLevelData[2].riskLevel = data.YDATE11 || '-'
  productLevelData[2].styleCategory = data.YDATE12 || '-'

  productLevelData[3].fundLevel = levelFilter(Number(data.YDATE17)) || 0
  productLevelData[3].earnLevel = levelFilter(Number(data.YDATE18)) || 0
  productLevelData[3].riskLevel = data.YDATE19 || '-'
  productLevelData[3].styleCategory = data.YDATE20 || '-'

  productLevelData[4].fundLevel = levelFilter(Number(data.YDATE13)) || 0
  productLevelData[4].earnLevel = levelFilter(Number(data.YDATE14)) || 0
  productLevelData[4].riskLevel = data.YDATE15 || '-'
  productLevelData[4].styleCategory = data.YDATE16 || '-'
}

export const handleBaseRateData = data => {
  productBaseRateData.a[0].valie = data[productBaseRateData.a[0].field] || '-'
  productBaseRateData.a[1].valie = data[productBaseRateData.a[1].field] || '-'
  productBaseRateData.a[2].valie = data[productBaseRateData.a[2].field] || '-'
  productBaseRateData.a[3].valie = data[productBaseRateData.a[3].field] || '-'
  productBaseRateData.a[4].valie = data[productBaseRateData.a[4].field] || '-'
  productBaseRateData.a[5].valie = data[productBaseRateData.a[5].field] || '-'
  productBaseRateData.a[6].valie = data[productBaseRateData.a[6].field] || '-'
  productBaseRateData.b[0].valie = data[productBaseRateData.b[0].field] || '-'
  productBaseRateData.c[0].valie = data[productBaseRateData.c[0].field] || '-'
  productBaseRateData.c[1].valie = data[productBaseRateData.c[1].field] || '-'
  productBaseRateData.c[2].valie = data[productBaseRateData.c[2].field] || '-'
  productBaseRateData.d[0].valie = data[productBaseRateData.d[0].field] || '-'
  productBaseRateData.e[0].valie = data[productBaseRateData.e[0].field] || '-'
  productBaseRateData.e[1].valie = data[productBaseRateData.e[1].field] || '-'
  productBaseRateData.e[2].valie = data[productBaseRateData.e[2].field] || '-'
  productBaseRateData.e[3].valie = data[productBaseRateData.e[3].field] || '-'
}
