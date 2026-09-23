import request from '@/utils/request'
import qs from 'qs'
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
      url: '/api/ann/v1.0/xbrl/record' + '?' + qs.stringify(params),
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
  getFileName:async function (params) {
    return request({
      url: '/api/ann/v1.0/xbrl/filename'+ '?' + qs.stringify(params),
      method: 'post',
    })
  },
  getProductsAll: async function() {
    return request({
      url: '/api/fund/v1.0/getProductsAll',
      method: 'get'
    })
  }
 
  

}