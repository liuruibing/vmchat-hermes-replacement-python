/* 首页获取数据接口 */
import request from '@/utils/request'
import qs from 'qs'

export  default {

  //获取数据
  getCmdCounts: async function () {
    return request.post('/api/transfer/v1.0/getCmdCounts')
  },
  getEmergency: async function () {
    return request.post('/api/emergency/v1.0/getCmdCounts')
  },
  //查询经纪商
  getBrokerInfo: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  getRemminds(){
    return request({
      url: '/api/remind/v1.0/listRemminds',
      method: 'get',
    })
  },
  // 首页自定义待办数量
  getCustomCmdCounts(){
    return request({
      url: '/api/customTransfer/v1.0/getCmdCounts',
      method: 'post',
    })
  },
  // 首页账户审核待办数量
  getTradeAccoCounts(){
    return request({
      url: '/api/trade/acco/getCmdCounts',
      method: 'post',
    })
  },
  



}

