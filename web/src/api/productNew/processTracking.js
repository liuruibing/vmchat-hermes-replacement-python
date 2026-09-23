import request from '@/utils/request'
import qs from 'qs'
export default {
  // 流程跟踪处理

  // 查询待办
  taskList: async function (params) {
    return request({
      url: '/api/lifecycle/v1.0/taskList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 查询所有
  allList: async function (params) {
    return request({
      url: '/api/lifecycle/v1.0/dealtList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  
  //  获取业务类型
  getBusinessType: async function (params) {
    return request({
      url: '/api/lifecycle/v1.0/getBusinessType',
      method: 'get',
    })
  },
  //  获取业务场景
  getBusinessNames: async function (params) {
    return request({
      url: '/api/lifecycle/v1.0/getBusinessNames?'+qs.stringify(params),
      method: 'get',
    })
  },
  //  产品概览查询
  list: async function (params) {
    return request({
      url: '/api/lifecycle/v1.0/list?'+qs.stringify(params),
      method: 'get',
    })
  },

}