// 后台请求封装
import request from '@/utils/request'
// URL序列化
import qs from 'qs'
// 文件下载根地址
import { FILE_URL } from '@/utils/request'
// Form Data 格式
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' };
export default {
  // 均值方差模型下载模版
  downloadTemplateUrl: function () {
    return `${FILE_URL}/api/assetAllocation/downloadExcel.do`
  },

  // 均值方差模型下载模版
  runScat: async function (params) {
    let d = new Date()
    let t = d.getTime()
    return request({
      headers: ContentTypeFormData,
      // url: '/api/assetAllocation/runScat.do?_v=' + t,
      url: '/api/virtualfof/runScat.do?_v=' + t,
      method: 'POST',
      traditional: true,
      data: qs.stringify(params, { arrayFormat: 'repeat' }),
    })
  }
}
