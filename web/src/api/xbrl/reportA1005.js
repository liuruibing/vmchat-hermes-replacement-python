import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   //列表查询
  findProductFile: async function (params) {
    return request({
      url: 'api/productFileInfo/v1.0/findProductFile'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
   //新增
  addProductFile: async function (params) {
    return request({
      url: 'api/productFileInfo/v1.0/addProductFile',
      method: 'post',
      data:params
    })
  },
   //修改
   updateProductFile: async function (params) {
    return request({
      url: 'api/productFileInfo/v1.0/updateProductFile',
      method: 'post',
      data:params
    })
  },
   //删除
   delProductFile: async function (params) {
    return request({
      url: 'api/productFileInfo/v1.0/delProductFile',
      method: 'post',
      data:qs.stringify(params)
    })
  },


}