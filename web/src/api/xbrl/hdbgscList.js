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
      url: '/api/ann/v1.0/batchCollateData/queryBatchCollateFund.do' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //新增
  addDataSource: async function (params) {
    return request({
      url: '/api/fund/v1.0/insertFundModel',
      method: 'post',
      data:params
    })
  },
  
  //一键生成结果
  yjscResult: async function (params) {
    return request({
      url: '/api/ann/v1.0/batchCollateData/oneKeyResultData.do',
      method: 'post',
      data:params
    })
  },
  //数值生成
  szscData: async function (params) {
    return request({
      url: '/api/ann/v1.0/batchCollateData/batchResultCreate.do',
      method: 'post',
      data:params
    })
  },
  //数值校对
  szjdData: async function (params) {
    return request({
      url: '/api/ann/v1.0/batchCollateData/batchResultCollate.do',
      method: 'post',
      data:params
    })
  },
  //文本生成
  wbscData: async function (params) {
    return request({
      url: '/api/ann/v1.0/batchCollateData/batchTxtCreate.do',
      method: 'post',
      data:params
    })
  },
  //文本校对
  wbhdData: async function (params) {
    return request({
      url: '/api/ann/v1.0/batchCollateData/batchTxtCollate.do',
      method: 'post',
      data:params
    })
  },
  
  
  

}