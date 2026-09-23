import request from '@/utils/request'
import qs from 'qs'
export  default {
   
  // 查询列表
  warnResultList: async function (params) {
    return request({
      url: '/api/afterManage/warnResult/list',
      method: 'post',
      data: params,
    })
  },

  
  
}