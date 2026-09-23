import request from '@/utils/request'
import store from '@/store'
import qs from 'qs'
import { getToken } from '@/utils/auth'

export default {
  // 报告订阅查询列表（BootstrapTable格式：limit, offset, sort, order + 表单参数）
  doReportSubscriptionList(params) {
    return request({
      url: '/api/batchReportSubscription/doReportSubscriptionList',
      method: 'post',
      data: params
    })
  },

  // 预览PDF（新窗口打开）
  getPreviewPdfUrl(fileId) {
    const baseApi = store.state.setting.baseApi || process.env.BASE_API || ''
    return `${baseApi}/api/batchReportSubscription/previewPdf?token=${getToken()}&fileId=${encodeURIComponent(fileId)}`
  },

  // 单个PDF下载（后端接收form参数）
  downLoadPdf(fileId) {
    return request({
      url: '/api/batchReportSubscription/downLoadPdf',
      method: 'post',
      data: qs.stringify({ fileId }),
      responseType: 'blob'
    })
  },

  // 批量PDF下载（后端接收form参数，fileIds为逗号分隔字符串）
  batchDownLoadPdf(fileIds) {
    return request({
      url: '/api/batchReportSubscription/batchDownLoadPdf',
      method: 'post',
      data: qs.stringify({ fileIds }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      responseType: 'blob'
    })
  },

  // 重新生成报告
  executeBatchReportSubscriptionData(params) {
    return request({
      url: '/api/batchReportSubscription/executeBatchReportSubscriptionData',
      method: 'post',
      data: params
    })
  },

  // 获取报告模板列表
  getTemplateList(params = {}) {
    return request({
      url: '/api/batchReportSubscription/selectDynamicTemplateList',
      method: 'post',
      data: params
    })
  }
}
