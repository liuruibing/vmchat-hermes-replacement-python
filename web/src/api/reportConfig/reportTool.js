import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export default {
  // 获取报表工具配置列表数据
  list: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 报表工具配置新增
  // add: async function (params) {
  //   return request({
  //     url: '/api/reportTool/v1.0/add',
  //     method: 'post',
  //     data: qs.stringify(params)
  //   })
  // },
  // 删除列表行数据
  delete: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/delete',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 报表工具配置状态修改 启用/禁用
  update: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/update',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 编辑回显
  editEcho: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/editEcho',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 新增/修改   修改-传参加上id
  edit: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/edit',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  
  // 获取报表名称列表数据
  dictList: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/dictList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 获取执行记录列表数据
  logList: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/logList'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // 批量下载
  batchDownload: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/batchDownload',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // "邮件配置条件查询"
  mailList: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/mailList'+'?'+qs.stringify(params),
      method: 'get',
      
    })
  },
  // 邮件发送
  sendMail: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/sendMail',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 获取邮件收件人信息  id,type(MAILBCC-密送 MAILCC-抄送 MAILTO-收件人)
  listReceiver: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/listReceiver',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 获取联系人
  contactList: async function (params) {
    return request({
      url: '/api/reportTool/v1.0/contactList',
      method: 'get',
    })
  },


}