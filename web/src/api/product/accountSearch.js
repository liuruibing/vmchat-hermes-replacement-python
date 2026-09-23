import request from '@/utils/request'
import qs from 'qs'

export  default {
  // 托管
  getTgAccList: async function (params) {
    return request({
      url: '/api/trade/acco/list?accoType=fiduciary&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 证券
  getZqAccList: async function (params) {
    return request({
      url: '/api/trade/stock/pageStocks.do' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 期货
  getQhAccList: async function (params) {
    return request({
      url: '/api/trade/future/pageFutures.do?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 银行间债券
  getYhjAccList: async function (params) {
    return request({
      url: '/api/trade/bond/pageBonds.do?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 其他
  getQtAccList: async function (params) {
    return request({
      url: '/api/trade/acco/list?accoType=other&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 募集 托管 证券 期货 银行间 其他
  getAllAccList: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 账户管理-全部账户
  getAllAccListPage: async function (params) {
    return request({
      url: '/api/trade/acco/selectDataPage?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 托管
  getTgAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=fiduciary&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 证券
  getZqAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=zq&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 期货
  getQhAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=qh&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 银行间
  getYhjAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=yhj&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 银行间-上清
  getYhjSqAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=yhjsq&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 银行间-中债
  getYhjZzAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=yhjzz&' + qs.stringify(params),
      method: 'post',
    })
  },
  // 其他
  getQtAccList2: async function (params) {
    return request({
      url: '/api/trade/acco/selectData?accoType=other&' + qs.stringify(params),
      method: 'post',
    })
  },


}
// 托管
// /api/trade/acco/list?accoType=fiduciary&pageSize=50&pageNum=1
// 证券
// /api/trade/stock/pageStocks.do?pageSize=50&pageNum=1
// 期货
// /api/trade/future/pageFutures.do?pageSize=50&pageNum=1
// 银行间债券
// /api/trade/bond/pageBonds.do?pageSize=50&pageNum=1
// 其他
// /api/trade/acco/list?accoType=other&pageSize=50&pageNum=1