import request from '@/utils/request'

export default {
  // 1. 查询模板列表（分页）
  getTempList(params) {
    return request({
      url: '/api/browser/templateInfo_list',
      method: 'post',
      data: params
    })
  },

  // 2. 查询模板指标列信息
  getTemplateIndexInfoList(params) {
    return request({
      url: '/api/browser/templateIndexInfo_list',
      method: 'post',
      data: params
    })
  },

  // 3. 删除模板
  deleteTemplate(params) {
    return request({
      url: '/api/browser/templateInfo_delete',
      method: 'post',
      data: params
    })
  },

  // 4. 更新模板基本信息
  updateTemplateInfo(params) {
    return request({
      url: '/api/browser/templateInfo_update',
      method: 'post',
      data: params
    })
  },

  // 5. 新增模板
  insertTemplateInfo(params) {
    return request({
      url: '/api/browser/templateInfo_insert',
      method: 'post',
      data: params
    })
  },

  // 6. 更新模板指标列配置
  updateTemplateDetail(params) {
    return request({
      url: '/api/browser/templateInfoDetail_update',
      method: 'post',
      data: params
    })
  },

  // 7. 查询单产品绩效指标树
  getIndexDetailInfoTreeList(params) {
    return request({
      url: '/api/browser/indexDetailInfoTree_list',
      method: 'post',
      data: params
    })
  },

  // 8. 查询汇总穿透指标树
  getIndexDetailInfoTreeZHList(params) {
    return request({
      url: '/api/browser/indexDetailInfoTree_zh_list',
      method: 'post',
      data: params
    })
  },

  // 9. 查询个券指标树
  getIndexDetailInfoTreeGQList(params) {
    return request({
      url: '/api/browser/indexDetailInfoTree_gq_list',
      method: 'post',
      data: params
    })
  },

  // 10. 查询字典列表
  getDictionaryList(params) {
    return request({
      url: '/api/browser/getDictionaryList',
      method: 'post',
      data: params
    })
  },

  // 11. 获取股票指数代码和名称
  getDimNmeAndCodeGP(params) {
    return request({
      url: '/api/browser/getDimNmeAndCodeGP',
      method: 'post',
      data: params
    })
  },

  // 12. 获取多个基金净值日期的交集
  getFundsNetDateIntersection(params) {
    return request({
      url: '/api/browser/get_funds_netDate_intersection',
      method: 'post',
      data: params
    })
  },

  // 13. 获取多个基金净值日期的并集
  getFundsNetDate(params) {
    return request({
      url: '/api/browser/get_funds_netDate',
      method: 'post',
      data: params
    })
  },

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
