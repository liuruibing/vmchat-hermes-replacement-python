import request from '@/utils/request'
import qs from 'qs'

const ContentTypeFormData = {'Content-type': 'application/x-www-form-urlencoded'}


export default {
  // 查询表格数据
  getTableData: async function (params) {
    return request({
      url: '/api/reportQuickConfig/v1.0/page',
      method: 'POST',
      data: params,
      params: params
    })
  },

  // 删除表格数据
  deleteRow: async function (params) {
    return request({
      url: '/api/reportQuickConfig/v1.0/delete',
      method: 'POST',
      data: params,
      params: params
    })
  },


  // 更新表格数据
  updateRow: async function (params) {
    return request({
      url: '/api/reportQuickConfig/v1.0/update',
      method: 'POST',
      data: params,
      params: params
    })
  },

  // 获取行数据 详情
  getVersionRow: async function (params) {
    return request({
      url: '/api/reportQuickConfig/v1.0/getVersion',
      method: 'GET',
      params: params
    })
  },
  // 导入数据
  uploadFile: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/reportQuickConfig/v1.0/upload',
      method: 'post',
      data: params
    })
  },
}


