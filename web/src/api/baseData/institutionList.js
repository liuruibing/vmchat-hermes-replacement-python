import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/deptInfo/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/deptInfo/v1.0/saveModify',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/deptInfo/v1.0/saveModify',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/deptInfo/v1.0/batchDelete' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
   //删除
   deleteData: async function (params) {
    return request({
      url: '/api/deptInfo/v1.0/delDeptInfo' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  getSelects: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  }
 

  
   


}