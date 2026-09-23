import request from '@/utils/request'
import qs from 'qs'
export default {
  // 列表查询
  list: async function (params) {
    return request({
      url: '/api/positionConf/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },
  
  // 流程岗位新增
  add: async function (params) {
    return request({
      url: '/api/positionConf/v1.0/add',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  
  // 流程岗位编辑
  edit: async function (params) {
    return request({
      url: '/api/positionConf/v1.0/edit',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 流程岗位删除
  delete: async function (params) {
    return request({
      url: '/api/positionConf/v1.0/delete',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  


}