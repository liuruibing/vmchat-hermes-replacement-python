import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {

  //新增
  addFofSun: async function (params) {
    return request({
      url: '/api/fofSun/fofSunAddInfo' + '?' + qs.stringify(params),
      method: 'post',
      data:params
    })
  },

  //编辑
  editFofSun: async function (params) {
    return request({
      url: '/api/fofSun/fofSunEditInfo' + '?' + qs.stringify(params),
      method: 'post',
      data:params
    })
  },

  //删除
  deleteFofSun: async function (params) {
    return request({
      url: '/api/fofSun/delFundPool' + '?' + qs.stringify(params),
      method: 'post',
      data:params
    })
  },

}
