/* 管理人复核接口 */
import request from '@/utils/request'
import qs from 'qs'

const url = '/api/process/v1.0/processdefine/';
export  default {
  // 查询所有的信息
  selectALLInfoUrl: async function () {
    return request.get('/api/transfer/managerCheck/selectALL')
  },
  //管理人复核分页
  searchPageList: async function (params) {
    return request.get('/api/transfer/managerCheck/searchPageList', params)
  },

  //查询账户信息
  searchHeadInfo: async function () {
    return request.get('/api/transfer/managerCheck/getAccountInfo')
  },
  //修改跟踪代办状态
  updateStatus: async function (taskId,params) {
    return request.post(url+taskId, params)
  },
  taUpdateStatus:async function (id,opinion,status) {
    return request.post("/api/ta/v1.0/managerCheck?id="+id+"&operation="+status+"&opinion="+opinion)
  }
}

