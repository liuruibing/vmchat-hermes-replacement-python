/* 跟踪代办接口 */
import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const url = '/api/process/v1.0/processInstance/';
export  default {
  // 查询所有的信息
  selectALLInfoUrl: async function (params) {
    return request({
      url: '/api/transfer/v1.0/all?' + qs.stringify(params),
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
  getResultDatas: async function (taskId) {
    return request.get(url+"task/"+taskId)
  },
  //查询详情信息
  newGetResultDatas: async function (taskId) {
    return request.get("/api/process/v1.0/processInstance/taskTest/"+taskId)
  },
  //查询fileList
  getFileList: async function (relaId) {
    return request.get("/api/file/v1.0/filesGet?relaId="+relaId)
  },
  // 查询所有 数据源设置
  getTransferList: async function (params) {
    return request({
      url: '/api/transfer/v1.0/trasnferTaskList?' + qs.stringify(params),
      method: 'get',
    })
  },
  getTrasnferDealtList: async function (params) {
    return request({
      url: '/api/transfer/v1.0/trasnferDealtList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getInvestList: async function (params) {
    return request({
      url: '/api/transfer/v1.0/investTaskList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getInveDealtstList: async function (params) {
    return request({
      url: '/api/transfer/v1.0/investDealtList?' + qs.stringify(params),
      method: 'get',
    })
  },
   // 查询所有 数据源设置
   startTransfer: async function (params) {
    return request({
      url: '/api/transfer/v1.0/startTransfer' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  
  // 处理人信息列表
  getTaskcomment: async function (params) {
    return request({
      url: '/api/taskcomment/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 获取发送邮件信息接口 需要传输参数为 id（当前业务数据的id，必传）
  getEmailInfo: async function (params) {
    return request({
      url: '/api/allocation/v1.0/getEmailInfo' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 发送邮件
  sendMessage: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/allocation/v1.0/sendMessage',
      method: 'post',
      data: params,
    })
  },

  // 获取旧数据
  getOldData: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/transfer/v1.0/getOldData',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  getFormData: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/transfer/v1.0/getFormData',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  saveFormData: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/transfer/v1.0/saveFormData',
      method: 'post',
      data: params,
    })
  },
  // 获取指令详情右侧表单数据（真实业务数据）传id
  getInfo: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/transfer/v1.0/info',
      method: 'post',
      data: qs.stringify(params),
    })
  },


}

