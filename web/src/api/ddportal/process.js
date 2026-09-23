import request from '../../utils/request'
import store from '@/store'
const qs = require('qs')
export default {
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/system/operlogs' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 查询所属机构
  getCompanyIdList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/dept/companys',
      method: 'get'
    })
  }
}
