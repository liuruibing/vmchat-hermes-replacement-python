import request from '@/utils/request'
import qs from 'qs'
export  default {

  // 查询列表
  warnRuleManageList: async function (params) {
    return request({
      url: '/api/invitationApply/list',
      method: 'post',
      data: params,
    })
  },
  // 刷新流程状态
  refreshProcessStatus: async function(param) {
    return request({
      url: '/api/invitationApply/refreshProcessStatus',
      data: param,
      method: 'post'
    })
  },
  //系统消息：授权申请记录标记已读
  markAuthApplyMessageRead: async function(param) {
    return request({
      url: '/api/invitationApply/markAuthApplyMessageRead',
      data: param,
      method: 'post'
    })
  },
  authApply: async function(param) {
    return request({
      url: '/api/invitationApply/submit',
      data: param,
      method: 'post'
    })
  },

  // 下载产品清单模板
  downloadFundTemplate: async function () {
    return request({
      url: '/api/common/fundInfoCommon/downloadFundTemplate',
      method: 'get',
      responseType: 'blob'
    })
  },

  // 上传解析产品清单Excel
  parseFundExcel: async function (formData) {
    return request({
      url: '/api/common/fundInfoCommon/parseFundExcel',
      method: 'post',
      data: formData,
      headers: {
        'Content-Type': 'multipart/form-data' // 表单上传格式
      }
    })
  }
}
