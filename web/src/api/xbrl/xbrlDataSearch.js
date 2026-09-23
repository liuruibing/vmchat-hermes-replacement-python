import request from '@/utils/request'
import qs from 'qs'
export  default {
   //字典查询
   getTransferType: async function (params) {
    return request({
      url: '/api/edims/v1.0/listEdims.do?dimType=' + params,
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/ann/v1.0/dataElement/elementQuery.do' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },

  // 查询所有 数据源设置
  getDataTableNameList: async function (params) {
    return request({
      url: '/api/commonTableManager/v1.0/loadListValueByTableName.do' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  download: async function (params) {
    return request({
      url: '/api/ann/v1.0/dataElement/exportElement.do' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  getProductsAll: async function() {
    return request({
      url: '/api/fund/v1.0/getProductsAll',
      method: 'get'
    })
  }


  

  

}