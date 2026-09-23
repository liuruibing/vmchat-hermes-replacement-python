import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};

export default{
  // 指令配置信息查询
  getDataList: async function (params) {
    return request({
      url: '/api/allocation/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 指令配置收件人查看
  getListReceiver: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/allocation/v1.0/listReceiver',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  // 新增邮件配置
  // addConfig: async function (params) {
  //   return request({
  //     headers: ContentTypeFormData,
  //     url: '/api/allocation/v1.0/addMile',
  //     method: 'post',
  //     data: qs.stringify(params),
  //   })
  // },
  // 新增邮件配置
  addMail: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/allocation/v1.0/add',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  // 编辑前获取 邮件配置 详情
  getMailInfo: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/allocation/v1.0/info',
      method: 'post',
      data: qs.stringify(params),
    })
  },





  // 指令模板配置信息列表查询
  getTDataList: async function (params) {
    return request({
      url: '/api/template/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 新增指令模板配置
  addTemplate: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/template/v1.0/add',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  // 获取指令模板信息
  listTemplate: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/template/v1.0/listTemplate',
      method: 'post'
    })
  },
  // 获取指令模板信息
  getTemplate: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/template/v1.0/getTemplateHtml',
      method: 'post',
      data: qs.stringify(params),
    })
  },
  // /api/template/v1.0/templateInfo
  
  // 获取管理人签章
  getListSeals: async function (params) {
    return request({
      // headers: ContentTypeFormData,
      url: '/api/seal/v1.0/listSeals?'+qs.stringify(params),
      method: 'get',
    })
  },
  
  // 根据产品代码和业务id获取产品相关信息接口（数据替换）
  getFundInfo: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/fund/v1.0/getFundInfo',
      method: 'post',
      data: qs.stringify(params),
    })
  },
}