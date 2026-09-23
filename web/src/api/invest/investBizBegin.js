/* 投资指令流程发起接口 */
import request from '@/utils/request'
import qs from 'qs'
const url = '/api/process/v1.0/processInstance/';
export  default {

  //查询产品信息
  getProductInfo: async function () {
    return request.get('/api/product/v1.0/getProductsAll')
  },
  //查询销售机构
  getSaleMechanism: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  //查询银行
  getBank: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  //查询转账类型
  // getTransferType: async function () {
  //   return request.get('/api/transfer/bizBegin/getProductInfo')
  // },
  //获取defineId
  getDefineId: async function (key) {
    return request.get(url+key)
  },
  //提交流程
  sendBiz: async function (id,params) {
    return request.post('/api/process/v1.0/processInstance/'+id,params)
  },
  //转账类型
  getTransferType: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })

  },

  getInitTransFlow: async function () {
    return request.get('/api/transFlow/v1.0/initTransFlow')
  },
  // 查询所有 数据源设置
  startInvest: async function (params) {
    return request({
      url: '/api/transfer/v1.0/startInvest',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  }

}

