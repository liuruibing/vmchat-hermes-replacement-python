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
      url: '/api/fund/v1.0/getFundApproveList' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //复制新增
  getDataSourceDetail: async function (params) {
    return request({
      url: '/api/fund/v1.0/getFundApprove' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //审核
  updateDataStatus: async function (params) {
    return request({
      url: '/api/fund/v1.0/approveFundInfo',
      method: 'post',
      data:params
    })
  }
  

}