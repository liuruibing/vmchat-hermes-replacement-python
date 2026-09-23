import request from '@/utils/request'
import qs from 'qs'

const FormDataHeader = { 'Content-Type': 'multipart/form-data' }
const JsonHeader = { 'Content-Type': 'application/json' }

export default {
  selectFrontReportList(reportType) {
    return request({
      url: '/api/reportZone/selectFrontReportList',
      method: 'POST',
      data: qs.stringify({ reportType }), // 表单格式传参
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  selectManageReportList(dto) {
    return request({
      url: '/api/reportZone/manage/selectReportList',
      method: 'POST',
      data: dto,
      headers: JsonHeader
    })
  },

  insertReport(formData) {
    return request({
      url: '/api/reportZone/manage/insertReport',
      method: 'POST',
      data: formData,
      headers: FormDataHeader,
      transformRequest: [function(data) {
        return data
      }]
    })
  },

  updateReport(formData) {
    return request({
      url: '/api/reportZone/manage/updateReport',
      method: 'POST',
      data: formData,
      headers: FormDataHeader,
      transformRequest: [function(data) {
        return data
      }]
    })
  },

  deleteReport(fid) {
    return request({
      url: '/api/reportZone/manage/deleteReport',
      method: 'POST',
      data: qs.stringify({ fid }),
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })
  },

  downloadReport(fid) {
    return request({
      url: '/api/reportZone/manage/downloadReport',
      method: 'GET',
      params: { fid },
      responseType: 'blob' // 二进制流
    })
  },

}
