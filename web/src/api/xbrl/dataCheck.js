import request from '@/utils/request'
import qs from 'qs'

const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' }
export default {
  //字典查询
  getTransferType: async function(params) {
    return request({
      url: '/api/edims/v1.0/listEdims.do?dimType=' + params,
      method: 'get'
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/list' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },

  // 规则-查询
  getIndParaThemeList: async function(params) {
    return request({
      url: '/api/warnConfig/v1.0/doWarnConfigList.do' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  //规则-编辑、新增
  postIndParaThemeEdit: async function(params) {
    return request({
      url: '/api/warnConfig/v1.0/addWarnConfig.do' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  //添加规则到
  addData: async function(ids) {
    return request({
      url: '/api/dataMonitor/v1.0/insert?ids=' + ids,
      method: 'POST'
    })
  },
  //删除校验配置
  deleteDataSource: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/delete' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  //修改状态和执行顺序
  updateDataSource: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/update' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  //修改状态
  updateStatus: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/updateStatus' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  getDaLei: async function() {
    return request({
      url: '/api/warnConfig/v1.0/getCheckDaLeiList',
      method: 'post'
    })
  },
  getDataSourceList2: async function() {
    return request({
      url: '/api/warnConfig/v1.0/getDataSourceList',
      method: 'post'
    })
  },
  getCheckDataList: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/checkDataList' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  getCheckSpecilDataList: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/checkBusyList' + '?' + qs.stringify(params),
      method: 'POST'
    })
  },
  // 查询业务主题表名
  getDetail: async function(params) {
    return request({
      url: '/api/warnConfig/v1.0/doWarnErrorDetailList.do?' + qs.stringify(params),
      method: 'post'
    })
  },

  // 新增
  riskAdd: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/insert',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 编辑
  riskEdit: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/edit',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 禁用、启用
  modifyStatus: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/modifyStatus',
      method: 'post',
      data: qs.stringify(params)
    })
  },

  // 提交
  submit: async function(params) {
    return request({
      url: '/api/indexManager/v1.0/submit',
      method: 'post',
      data: qs.stringify(params)
    })
  },

//  批量复合
  listSubmit: async function(params) {
    return request({
      url: '/api/indexManager/v1.0/batchReview',
      method: 'post',
      data: qs.stringify(params)
    })
  },

//  取消复核，批量取消
  cancelSubmit: async function(params) {
    return request({
      url: '/api/indexManager/v1.0/reviewCancel',
      method: 'post',
      data: qs.stringify(params)
    })
  },
//  查看操作日志
  getOperateList: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/findLog?'+qs.stringify(params),
      method: 'get'
    })
  },

//  查看参数设置列表
  getParamsSetList: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/findList?'+qs.stringify(params),
      method: 'get'
    })
  },
//  查看指标条件
  getIndexTypeList: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/findIndexList?indexType=' + params,
      method: 'get'
    })
  },

  //  查看联系人列表
  getContactList: async function(params) {
    return request({
      url: '/api/reportTool/v1.0/contactList?'+qs.stringify(params),
      method: 'get'
    })
  },

  //  查看岗位信息列表
  getJobInfoList: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/findPosition' + '?' + qs.stringify(params),
      method: 'get'
    })
  },

//  查询异常数据
  getAbnormalData: async function(params) {
    return request({
      url: '/api/paramSetting/v1.0/findList?' + qs.stringify(params),
      method: 'post'
    })
  },

// 一键校验
  checkAll: async function(params) {
    return request({
      url: '/api/dataMonitor/v1.0/checkAll?' + qs.stringify(params),
      method: 'post'
    })
  },
// 特殊row校验
  checkRow: async function(params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/businessCheck/v1.0/singleBusCheck',
      data: qs.stringify(params),
      method: 'post'
    })
  },
  sendInfo: async function(params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/indexManager/v1.0/updateRmark',
      data: qs.stringify(params),
      method: 'post'
    })
  },
  checkRowTop: async function(params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/dataMonitor/v1.0/singleDataCheck',
      data: qs.stringify(params),
      method: 'post'
    })
  },
  BeformCheck: async function(params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/dataMonitor/v1.0/checkHaveData',
      data: qs.stringify(params),
      method: 'post'
    })
  },
  // /api/dataMonitor/v1.0/infoOverview
  infoOverview: async function(params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/dataMonitor/v1.0/infoOverview'+'?'+qs.stringify(params),
      method: 'get'
    })
  },

}
