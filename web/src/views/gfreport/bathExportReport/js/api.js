import request from '@/utils/request'
import store from '@/store'
import qs from 'qs'
import { getToken } from '@/utils/auth'

export default {
  // 列表查询（BootstrapTable格式：limit, offset, sort, order + 表单参数）
  doBatchExportReportList(params) {
    return request({
      url: '/api/batchExportReport/doBatchExportReportList',
      method: 'post',
      data: params
    })
  },

  // 报告模板列表
  getTemplateList(params = {}) {
    return request({
      url: '/api/batchExportReport/selectDynamicTemplateList',
      method: 'post',
      data: params
    })
  },

  // 预览PDF（新窗口打开）
  getPreviewPdfUrl(fileId) {
    const baseApi = store.state.setting.baseApi || process.env.BASE_API || ''
    return `${baseApi}/api/batchExportReport/previewPdf?token=${getToken()}&fileId=${encodeURIComponent(fileId)}`
  },

  // 单个PDF下载
  downLoadPdf(fileId) {
    return request({
      url: '/api/batchExportReport/downLoadPdf',
      method: 'get',
      params: { fileId },
      responseType: 'blob'
    })
  },

  // 批量PDF下载（zip）
  batchDownLoadPdf(fileIds) {
    return request({
      url: '/api/batchExportReport/batchDownLoadPdf',
      method: 'get',
      params: { fileIds },
      responseType: 'blob'
    })
  },

  // 新增（fundcodes[] 为数组）
  doExportReportAdd(payload) {
    return request({
      url: '/api/batchExportReport/doExportReportAdd',
      method: 'post',
      data: payload,
    })
  },

  // 修改
  doExportReportEdit(payload) {
    return request({
      url: '/api/batchExportReport/doExportReportEdit',
      method: 'post',
      data: payload,
    })
  },

  // 单条删除
  deleteExportReport(fileId) {
    return request({
      url: '/api/batchExportReport/deleteExportReport',
      method: 'post',
      data: { fileId: fileId },
    })
  },

  // 批量删除
  deleteBatchExportReport(fileIds) {
    return request({
      url: '/api/batchExportReport/deleteBatchExportReport',
      method: 'post',
      data: qs.stringify({ fileIds }),
    })
  },

  // 批量生成报告
  executeBatchExportReportData(fileIds) {
    return request({
      url: '/api/batchExportReport/executeBatchExportReportData',
      method: 'post',
      data: qs.stringify({ fileIds }),
    })
  },

  // 批量服务平台展示
  addBatchFwptRecordShow(fileIds) {
    return request({
      url: '/api/batchExportReport/addBatchFwptRecordShow',
      method: 'post',
      data: qs.stringify({ fileIds }),
    })
  },

  // 批量服务平台隐藏
  addBatchFwptRecordHide(fileIds) {
    return request({
      url: '/api/batchExportReport/addBatchFwptRecordHide',
      method: 'post',
      data: qs.stringify({ fileIds }),
    })
  },

  // 下载导入模板
  downLoadImportExample() {
    return request({
      url: '/api/batchExportReport/downLoadImportExample',
      method: 'get',
      responseType: 'blob'
    })
  },

  // 下载报告模板清单
  downLoadTemplateReport() {
    return request({
      url: '/api/batchExportReport/downLoadTemplateReport',
      method: 'get',
      responseType: 'blob'
    })
  },

  // 批量导入上传（字段名必须是 uploadImportBatchExportFile）
  importExportReportUpload(file) {
    const form = new FormData()
    form.append('uploadImportBatchExportFile', file)
    return request({
      url: '/api/batchExportReport/importExportReportUpload',
      method: 'post',
      data: form,
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}
