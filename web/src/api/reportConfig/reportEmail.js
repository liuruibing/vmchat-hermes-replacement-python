import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export default {
  // 获取报表邮件配置列表数据
  getReportEmailList: async function (params) {
    return request({
      url: 'api/reportEmail/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 查询模板
  findTemplate: async function (params) {
    return request({
      url: 'api/reportEmail/v1.0/findTemplate'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 新增、修改
  addEmail: async function (params) {
    return request({
      url: 'api/reportEmail/v1.0/addEmail',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 状态管理-启用、禁用"updateEmail"
  updateEmail: async function (params) {
    return request({
      url: 'api/reportEmail/v1.0/updateEmail',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 编辑前获取 邮件配置 详情
  getMailInfo: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/reportEmail/v1.0/info',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  // 删除配置
  deleteEmail: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/reportEmail/v1.0/deleteEmail',
      method: 'post',
      data: qs.stringify(params),
    })
  },


}