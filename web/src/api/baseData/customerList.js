import request from '@/utils/request'
import qs from 'qs'
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/customerInfo/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  updateDataSource: async function (params) {
    return request({
      url: '/api/customerInfo/v1.0/customerInfoSavOrEdit' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //更新
  addDataSource: async function (params) {
    return request({
      url: '/api/customerInfo/v1.0/customerInfoSavOrEdit' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/customerInfo/v1.0/delCustomerInfo' + '?' + qs.stringify(params),
      method: 'GET',
    })
  },
  getSelects: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  getQuDaoList: async function () {
    return request({
      url: '/api/saller/v1.0/list',
      method: 'get',
    })
  }

  
   


}