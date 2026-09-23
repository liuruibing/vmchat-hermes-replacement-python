// 后台请求封装
// 文件下载根地址
import request, { FILE_URL } from '@/utils/request'
// URL序列化
import qs from 'qs'
// Form Data 格式
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
export default {
  // 均值方差模型下载模版
  downloadTemplateUrl: function() {
    return `${FILE_URL}/api/assetAllocation/downloadExcel.do`
  },

  // 均值方差模型下载模版
  runBL: async function(params) {
    let d = new Date()
    let t = d.getTime()
    return request({
      headers: ContentTypeFormData,
      // url: '/api/assetAllocation/runBL.do?_v=' + t,
      url: '/api/virtualfof/runBL.do?_v=' + t,
      method: 'POST',
      traditional: true,
      data: qs.stringify(params, { arrayFormat: 'repeat' })
    })
  }
}
