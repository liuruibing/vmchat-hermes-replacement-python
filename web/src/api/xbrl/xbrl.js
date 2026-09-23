import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {
   //字典查询
   getTransferType: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/xbrlReport/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //更新
  updateDataSource: async function (params) {
    return request({
      url: '/api/xbrlReport/v1.0/updateStatus',
      method: 'post',
      data:params
    })
  },
  getSelects: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  getProductsAll: async function () {
    return request({
      url: '/api/fund/v1.0/getProductsAll',
      method: 'get',
    })
  },
  // 查询操作日志 数据源设置
  getDataLogSourceList: async function (params) {
    return request({
      url: '/api/xbrlReportLog/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 查询操作日志 数据源设置
  downloadFile: async function (params) {
    return request({
      url: '/api/xbrlReport/v1.0/download' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 查询所有 数据源设置
  getAnnDataSourceList: async function (params) {
    return request({
      url: '/api/annreport/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 查询所有 数据源设置
  geVerifyDetail: async function (params) {
    return request({
      url: '/api/annreport/v1.0/listVerifyDetail' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  // 查询所有 数据源设置
  getLogInfo: async function (params) {
    return request({
      url: '/api/annreportlog/v1.0/list' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
  //一键生成
  yjscData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/createFile',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //勾稽校验
  gjjyData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/validData',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //与外包核对
  ywbhdData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/verifyFile',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  //确认复核
  qrfhData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/reportConfirm',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
    //确认复核
  reportConfirmCancelData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/reportConfirmCancel',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },
  
  //一键上报
  yjsbData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/reportSubmit',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },

  // 数据传送
  sjcsData: async function (params) {
    return request({
      url: '/api/annreport/v1.0/sendData',
      method: 'post',
      contentType: false,//这里不要落下
      dataType: 'json',
      data:params
    })
  },

  // ——————————————————————
  // 定期报告记录
  // 数据录入-获取树形控件数据
  getTreeData: async function (params) {
    return request({
      url: '/api/annreportInput/v1.0/findInput' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 数据录入-获取章节文本；
  getTreeTxt: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/findValue' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 数据录入-编辑文本；
  updateTxt: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/insertTxt',
      method: 'post',
      Headers:ContentTypeFormData,
      data:qs.stringify(params)
    })
  },
  // 数据录入-锁定文本；
  lockTxt: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/addlock',
      method: 'post',
      Headers:ContentTypeFormData,
      data:qs.stringify(params)
    })
  },
  // 数据录入-解锁；
  unlockTxt: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/unlock',
      method: 'post',
      Headers:ContentTypeFormData,
      data:qs.stringify(params)
    })
  },
  // 数据录入-计算
  createTxt: async function (params) {
    return request({
      url: '/api/annreportCount/v1.0/createTxt',
      method: 'post',
      Headers:ContentTypeFormData,
      data:qs.stringify(params)
    })
  },
  // 文本录入-文件上传
  fileUpload: async function (params) {
    return request({
      url: '/api/annreportInput/v1.0/uploadExcel',
      method: 'post',
      // Headers:ContentTypeFormData,
      data:params
    })
  },

  // 核对明细-获取树形控件数据
  getCheckTree: async function (params) {
    return request({
      url: '/api/annreportInput/v1.0/findCheck' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 校验明细
  findCheckInfo: async function (params) {
    return request({
      url: '/api/annreportCheck/v1.0/findCheckInfo',
      method: 'post',
      Headers:ContentTypeFormData,
      data:qs.stringify(params)
    })
  },

  // 批量解锁
  unlockBatch: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/unlockBatch',
      method: 'post',
      data:qs.stringify(params)
    })
  },
  // 批量锁定
  addLockBatch: async function (params) {
    return request({
      url: '/api/annreportTxt/v1.0/addLockBatch',
      method: 'post',
      data:qs.stringify(params)
    })
  },


}