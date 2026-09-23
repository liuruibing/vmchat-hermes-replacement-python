import request from '@/utils/request'
import qs from 'qs'
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/trade/future/pageFutures.do' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  updateDataSource: async function (params) {
    return request({
      url: '/api/trade/future/saveOrModify.do',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //更新
  addDataSource: async function (params) {
    return request({
      url: '/api/trade/future/saveOrModify.do',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/trade/future/deleteById.do' + '?' + qs.stringify(params),
      method: 'post',
    })
  },

  // 审核
  pass: async function (params) {
    return request({
      url: '/api/trade/future/pass' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 反审核
  unpass: async function (params) {
    return request({
      url: '/api/trade/future/unpass' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  

  
   


}