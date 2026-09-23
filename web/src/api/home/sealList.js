import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-type' : 'application/x-www-form-urlencoded'}
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
      url: '/api/seal/v1.0/listPageSeals' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      url: '/api/seal/v1.0/insertSeal',
      method: 'post',
      data:params
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/seal/v1.0/updateSeal',
      method: 'post',
      data:params
    })
  },
  //校验是否已存在人名章
  validate: async function (params) {
    return request({
      header: ContentTypeFormData,
      url: '/api/seal/v1.0/validate',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/seal/v1.0/deleteSeal' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
   //删除
   getRemindTypes: async function () {
    return request({
      url: '/api/remind/v1.0/listRemindTypes',
      method: 'get',
    })
  }


}