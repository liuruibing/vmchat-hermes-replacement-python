import request from '@/utils/request'

export default {
  // 14. 执行指标浏览器查询
  indexBrowserQuery(params) {
    return request({
      url: '/api/browser/index_browser',
      method: 'post',
      data: params
    })
  },

  // 15. 下载指标浏览器数据为Excel
  indexBrowserDownload(params) {
    return request({
      url: '/api/browser/indexBrowser_download',
      method: 'post',
      data: params,
      responseType: 'blob'
    })
  },

  // 16. 保存图表配置数据
  savePicData(params) {
    return request({
      url: '/api/browser/save_pic_data',
      method: 'post',
      data: params
    })
  },

  // 17. 查询图表配置数据
  queryPicConfig(params) {
    return request({
      url: '/api/browser/query_pic_config',
      method: 'post',
      data: params
    })
  },

  // 18. 查询节假日列表
  getHoliday(params) {
    return request({
      url: '/api/browser/get_holiday',
      method: 'post',
      data: params
    })
  }
}
