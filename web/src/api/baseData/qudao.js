import request from '@/utils/request'
import qs from 'qs'
// const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
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
      url: '/api/saller/v1.0/page' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      url: '/api/saller/v1.0/insert',
      method: 'post',
      data:params
     
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/saller/v1.0/update',
      method: 'post',
      data:params
    })
  },
  
  //查看详情
  getDataSourceDetail: async function (params) {
    return request({
      url: '/api/saller/v1.0/info' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/saller/v1.0/del' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //校验编码
  volidSallerInfo: async function (params) {
    return request({
      url: '/api/saller/v1.0/volidCode' + '?' + qs.stringify(params),
      method: 'post',
    })
  }
  
  
  

}