import request from '@/utils/request'
import qs from 'qs'
export  default {
   
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/trade/acco/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  updateDataSource: async function (params) {
    return request({
      url: '/api/trade/acco/saveOrModify.do',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //更新
  addDataSource: async function (params) {
    return request({
      url: '/api/trade/acco/saveOrModify.do',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/trade/acco/deleteById.do' + '?' + qs.stringify(params),
      method: 'post',
    })
  },

  // 审核
  pass: async function (params) {
    return request({
      url: '/api/trade/acco/pass' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 反审核
  unpass: async function (params) {
    return request({
      url: '/api/trade/acco/unpass' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  

  
   


}