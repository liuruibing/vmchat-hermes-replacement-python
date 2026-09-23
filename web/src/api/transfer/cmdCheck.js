/* 指令复核接口 */
import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const url = '/api/process/v1.0/processdefine/';
// 自定义划款流程更新
const url1 = '/api/customTransfer/v1.0/updateAndSubmit/';
export  default {
  // 查询所有的信息
  selectALLInfoUrl: async function () {
    return request.get('/api/transfer/cmdCheck/selectALL')
  },
  //指令复核分页
  searchPageList: async function (params) {
    return request.get('/api/transfer/cmdCheck/searchPageList', params)
  },

  //查询账户信息
  searchHeadInfo: async function () {
    return request.get('/api/transfer/cmdCheck/getAccountInfo')
  },
  //修改跟踪代办状态
  updateStatus: async function (taskId,params) {
    return request.post(url+taskId, params)
  },
  //修改跟踪代办状态(自定义划款指令流程)
  // newUpdateStatus: async function (taskId,params) {
  //   return request.post(url1+taskId, params)
  // },
  newUpdateStatus: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/customTransfer/v1.0/updateAndSubmit',
      method: 'post',
      data: params,
    })
  },
  // /api/transfer/v1.0/updateAndSubmit
  updateAndSubmit:async function(params){
    return request({
      headers: ContentTypeFormData,
      url: '/api/transfer/v1.0/updateAndSubmit',
      method: 'post',
      data: params,
    })
  }

}

