import request from '@/utils/request'
import store from '@/store'
import qs from 'qs'

export default {
  selectAllOptions() {
    return request({
      url: '/api/optionbacktrader/selectAllOptions',
      method: 'post'
    })
  },

  getBackTraderList(params) {
    return request({
      url: '/api/optionbacktrader/doBackTraderParamsList',
      method: 'post',
      data: params
    })
  },

  addBackTrader(params) {
    return request({
      url: '/api/optionbacktrader/doOptionBackTradeAdd',
      method: 'post',
      data: params
    })
  },

  editBackTrader(params) {
    return request({
      url: '/api/optionbacktrader/doOptionBackTradeEdit',
      method: 'post',
      data: params
    })
  },

  copyBackTrader(params) {
    return request({
      url: '/api/optionbacktrader/doOptionBackTradeCopy',
      method: 'post',
      data: params
    })
  },

  deleteBackTrader(fid) {
    return request({
      url: '/api/optionbacktrader/deleteOptionBackTrade',
      method: 'post',
      data: qs.stringify({ fid })
    })
  },

  executeBackTrader(fid) {
    return request({
      url: '/api/optionbacktradercompute/executeBackTrader',
      method: 'post',
      data: qs.stringify({ fid })
    })
  },

  getBackTraderResultUrl(fid, programmeName) {
    const baseApi = store.state.setting.baseApi || process.env.BASE_API || ''
    return `${baseApi}/api/optionbacktrader/initBackTraderResult.do?fid=${fid}&programmeName=${encodeURIComponent(programmeName || '')}`
  }
}
