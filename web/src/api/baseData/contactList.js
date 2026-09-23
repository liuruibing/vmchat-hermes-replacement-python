import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/contact/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  updateDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/contact/v1.0/updateContactInfo',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //更新
  addDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/contact/v1.0/insertContactInfo',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/contact/v1.0/delContactInfo' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //批量删除
  deleteSelect: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/contact/v1.0/batchDel',
      data: qs.stringify(params),
      method: 'post',
    })
  }
  

  
   


}