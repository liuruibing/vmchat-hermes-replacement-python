import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/foundManager/v1.0/getManager' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/foundManager/v1.0/editManager',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/foundManager/v1.0/domanagerAdd',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/foundManager/v1.0/deleteManager' + '?' + qs.stringify(params),
      method: 'post',
    })
  }
   


}