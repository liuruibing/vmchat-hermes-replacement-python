/* 跟踪代办接口 */
import request from '@/utils/request'
import qs from 'qs'
const url = '/api/process/v1.0/processInstance/';
export  default {
  // 查询所有的信息
  selectALLInfoUrl: async function (params) {
    return request({
      url: '/api/transfer/v1.0/taTaskList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 查询所有的信息
  taDealtList: async function (params) {
    return request({
      url: '/api/transfer/v1.0/taDealtList?' + qs.stringify(params),
      method: 'get',
    })
  },
  
  // 跟踪代办分页
  searchPageList: async function (params) {
    return request.get('/api/transfer/trackingAgent/searchPageList', params)
  },
  //修改跟踪代办状态
  updateStatus: async function (params) {
    return request.post('/api/transfer/trackingAgent/searchPageList', params)
  },
  //查询产品信息
  getProductInfo: async function () {
    return request.get('/api/product/v1.0/getProductsAll')
  },
  //查询划款状态
  getTransferStatus: async function () {
    return request.get('/api/transfer/trackingAgent/getTransferStatus')
  },
  //查询付款方账户类型
  getAccountType: async function () {
    return request.get('/api/transfer/trackingAgent/getAccountType')
  },
  //查询付款方账户类型
  getResultDatas: async function (id) {
    return request.get("/api/ta/v1.0/getTransFlowById?id="+id)
  },
  //查询fileList
  getFileList: async function (relaId) {
    return request.get("/api/file/v1.0/filesGet?relaId="+relaId)
  }

}

