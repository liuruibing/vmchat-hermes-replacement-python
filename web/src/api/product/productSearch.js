import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   //字典查询
   getTransferType: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/fund/v1.0/fundList' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      url: '/api/fund/v1.0/insertFundModel',
      method: 'post',
      data:params
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/fund/v1.0/updateFundModel',
      method: 'post',
      data:params
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/seal/v1.0/deleteSeal' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  
  //查看详情
  getDataSourceDetail: async function (params) {
    return request({
      url: '/api/fund/v1.0/findFundModel' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  
  //修改。复制新增查看详情接口
  getDataSourceEdit: async function (path,params) {
    return request({
      url: `/api/fund/v1.0/${path}` + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //获取渠道名称接口
  getSallerData: async function (params) {
    return request({
      url: '/api/saller/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //查询产品信息
  getProductInfo: async function () {
    return request.get('/api/product/v1.0/getProductsAll')
  },
  /*
    @GetMapping("getFundType")
    @ApiOperation(value = "查询基金类型详情")
  */
  // 查询基金类型详情
  getFundType: async function (params) {
    return request({
      url: '/api/fund/v1.0/getFundType',
      method: 'get',
    })
  },
  //删除
  volidFundCode: async function (params) {
    return request({
      url: '/api/fund/v1.0/volidFundCode' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 查询基金经理信息
  getFundManagerInfo: async function() {
    return request.get('/api/foundManager/v1.0/getManagerAll')
  },
  saveDataSource: async function (params) {
    return request({
      url: '/api/fund/v1.0/saveFundCache',
      method: 'post',
      data:params
    })
  },
  // 查询机构信息
  // getDeptInfoSel: async function() {
  //   return request.post('/api/deptInfo/v1.0/deptInfoSel')
  // },
  // “管理人名称”、“托管人名称”、“基金服务机构”
  getDeptInfoSel: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/deptInfo/v1.0/getListByInstTypeDim',
      method: 'post',
      data: qs.stringify(params),
    })
  }
  

}