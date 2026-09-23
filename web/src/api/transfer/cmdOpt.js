/* 指令经办接口 */
import request from '@/utils/request'
import qs from 'qs'
const url = '/api/process/v1.0/processdefine/';
export  default {
  // 查询所有的信息
  selectALLInfoUrl: async function () {
    return request.get('/api/transfer/cmdOpt/selectALL')
  },
  //指令经办分页
  searchPageList: async function (params) {
    return request.get('/api/transfer/cmdOpt/searchPageList', params)
  },

  //查询账户信息
  searchHeadInfo: async function () {
    return request.get('/api/transfer/cmdOpt/getAccountInfo')
  },
  //修改跟踪代办状态
  updateStatus: async function (taskId,params) {
    return request.post(url+taskId, params)
  }

}

