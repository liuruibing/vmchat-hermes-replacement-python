/* 模板接口 */
import request from '@/utils/request'
import qs from 'qs'
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
      url: '/api/emergency/v1.0/listPageConfigs' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 修改 数据源设置
  updateDataSource: async function (params) {
    return request({
      url: '/api/emergency/v1.0/updateConfig' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 删除单个  数据源设置
  deleteDataSource: async function (params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: '/api/index/indPara/dict/del' + '?' + qs.stringify(params),
      method: 'post',
    })
  }


}

