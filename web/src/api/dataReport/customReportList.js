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
  getDataTableNameList: async function (params) {
    return request({
      url: '/api/customReport/v1.0/sqlDataList' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  downloadData: async function (params) {
    return request({
      url: '/api/customReports/v1.0/dodownload' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
 getDataSourceListAll: async function (params) {
    return request({
      url: '/api/customReport/v1.0/findListAll' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  
  getDataSourceList: async function (params) {
    return request({
      url: '/api/customReport/v1.0/findList' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  addDataSource: async function (params) {
    return request({
      url: '/api/customReport/v1.0/reportSave' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  reportSearchTable: async function (params) {
    return request({
      url: '/api/customReport/v1.0/reportSearch' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/customReport/v1.0/reportUpdate'+ '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/customReport/v1.0/reportDel' + '?' + qs.stringify(params),
      method: 'post',
    })
  }
  
  
  

}