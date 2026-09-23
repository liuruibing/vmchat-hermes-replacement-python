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
      url: '/api/productdisc/v1.0/listPageProductDisc' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      url: '/api/productdisc/v1.0/insertProductDisc',
      method: 'post',
      data:params
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/productdisc/v1.0/updateProductDisc',
      method: 'post',
      data:params
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/productdisc/v1.0/deleteProductDisc' + '?' + qs.stringify(params),
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
  getDataSourceEdit: async function (params) {
    return request({
      url: '/api/fund/v1.0/getFundModel' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //配置提醒回显
  getAnnInfo: async function (params) {
    return request({
      Headers:ContentTypeFormData,
      url: '/api/cmdnotice/v1.0/getAnnInfo',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 配置提醒 新增/编辑
  cmdnotice_add:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/cmdnotice/v1.0/add',
      method: 'post',
      data: qs.stringify(params) 
    })
  },
  

}