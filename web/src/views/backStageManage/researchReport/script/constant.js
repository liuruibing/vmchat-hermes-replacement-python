import common from '../../../../api/common'
export const TABLE_COLUMNS = [
  {
    prop: 'title',
    label: '标题',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'summary',
    label: '摘要',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'author',
    label: '作者',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'type',
    label: '资讯类型',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'norgan',
    label: '所属机构',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'flag',
    label: '文章类型',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'arearType',
    label: '研报页面区域',
    width: 150,
    sortable: true,
    align: 'center'
  },
  {
    prop: 'orderId',
    label: '置顶排序',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'isHdleft',
    label: '首页展示',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'status',
    label: '状态',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'ndate',
    label: '发布日期',
    sortable: true,
    align: 'center'
  },
  {
    prop: 'updateTime',
    label: '更新时间',
    sortable: true,
    align: 'center'
  }
]

export const STATUS_COLOR_MAP = [
  {
    color: '#FFC000',
    value: '0'
  },
  {
    color: '#FFC000',
    value: '1'
  },
  {
    color: '#70AD47',
    value: '4'
  },
  {
    color: '#FF0000',
    value: '5'
  }
]

export const STATUS_TYPE = [
  {
    DIM_CDE: '1',
    DIM_NME: '启用'
  },
  {
    DIM_CDE: '0',
    DIM_NME: '禁用'
  }
]

export const FLAG_TYPE = [
  {
    DIM_CDE: '1',
    DIM_NME: '图片文字类'
  },
  {
    DIM_CDE: '2',
    DIM_NME: '视频类'
  },
  {
    DIM_CDE: '3',
    DIM_NME: '公众号文章类'
  }
]
export const ZX_TYPE = [
  {
    DIM_CDE: '2',
    DIM_NME: '广发资讯'
  },
  {
    DIM_CDE: '3',
    DIM_NME: '私募观点'
  }
]
//{
//     DIM_CDE: '1',
//     DIM_NME: '监管动态'
//   },备份
export const AREAR_TYPE = [
  {
    DIM_CDE: '1',
    DIM_NME: '行业动态-上'
  },
  {
    DIM_CDE: '2',
    DIM_NME: '行业动态-下'
  },
]

export let TYPE_LIST = []
export let NORGEN_LIST = []

export function getTypeList(type){
  let params = type === '0' ? 'NEWTYPEDETAIL' : 'NEWORGAN'
  commonApi.edimsDdiaCommon(params).then((res) => {
    if (res.data.status === 0) {
      if (type === '0') {
        TYPE_LIST = res.data.data
      } else {
        NORGEN_LIST = res.data.data
      }
    }
  })

}
