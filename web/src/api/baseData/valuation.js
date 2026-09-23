import request from '@/utils/request'
import qs from 'qs'
// const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
  // 估值表
  // 查询
  list: async function (params) {
    return request({
      url: '/api/gzb/v1.0/list',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  
}