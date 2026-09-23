import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export default {
  //sql查询 api/reportConfig/v1.0/doSql
  getFields: async function (params) {
    return request({
      url: '/api/reportConfig/v1.0/doSql',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // 获取菜单数据 findTree
  getMenu: async function (params) {
    return request({
      // url: '/api/role/roleActionSet?operationParam=false&roleId=929&roleName=【投资指令】管理人经办',
      url: '/api/reportConfig/v1.0/findTree',
      method: 'post',
    })
  },
  // 生成配置 buildConfig
  buildConfig: async function (params) {
    return request({
      url: '/api/reportConfig/v1.0/buildConfig',
      Headers:ContentTypeFormData,
      method: 'post',
      // data:qs.stringify(params),
      data:params
    })
  },
  // 字典SQL测试 checkDicSql
  checkDicSql: async function (params) {
    return request({
      url: '/api/reportConfig/v1.0/checkDicSql',
      Headers:ContentTypeFormData,
      method: 'post',
      data:qs.stringify(params),
    })
  },


}