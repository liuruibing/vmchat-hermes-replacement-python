/* 数据管理接口 */
import { post, get, excelGet } from '@/utils/request'
import { FILE_URL } from '@/utils/request'
import { getToken } from '@/utils/auth'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

// 公共excel下载
export function downloadExcelUrl (params) {
  return `${FILE_URL}/api/system/v1.0/file/download/${params}?token=${getToken()}`
}

// 投委会会议明细
export function nvestmentCommitteeListUrl (params) {
  return get('/api/manageView/nvestmentCommittee/list', params)
}

// 投委会会议明细（导出excel）
export function nvestmentCommitteeListEcxelUrl (params) {
  // return excelGet('/api/manageView/nvestmentCommittee/list', params)
  return get('/api/manageView/nvestmentCommittee/list', params)
}

// 投委会最新数据日期
export function nvestmentCommitteeMaxDateUrl () {
  return get('/api/manageView/nvestmentCommittee/maxDate')
}

// 添加投委会
export function nvestmentCommitteeInsertUrl (params) {
  return post('/api/manageView/nvestmentCommittee/insert', params)
}

// 修改投委会
export function nvestmentCommitteeUpdateUrl (params) {
  return post('/api/manageView/nvestmentCommittee/update', params)
}

// 删除投委会
export function nvestmentCommitteeDeleteUrl (params) {
  return post('/api/manageView/nvestmentCommittee/delete', params)
}

// 投委会文件下载
export function downloadCommitteeFileUrl (params) {
  // return `${FILE_URL}/api/manageView/nvestmentCommittee/touweihui/downloadFile?fileName=${encodeURIComponent(params.fileName)}&filePath=${encodeURIComponent(params.filePath)}&token=${params.token}`
  return `${FILE_URL}/api/manageView/nvestmentCommittee/touweihui/downloadFile`
}

// 产品信息维护-产品基础信息的展示
export function fundInfoListUrl (params) {
  return post('/api/dataManage/fundInfo/fundInfoList', qs.stringify(params), isForm)
}

// 查询组合辅助信息
export function selectDimFundInfoAssitUrl (params) {
  return post('/api/manageView/dimFundInfoAssit/select', qs.stringify(params), isForm)
}

// 添加组合辅助信息
export function insertDimFundInfoAssitUrl (params) {
  return post('/api/manageView/dimFundInfoAssit/insert', params)
}

// 修改组合辅助信息
export function updateDimFundInfoAssitUrl (params) {
  return post('/api/manageView/dimFundInfoAssit/update', params)
}

// 删除组合辅助信息
export function deleteDimFundInfoAssitUrl (params) {
  return post('/api/manageView/dimFundInfoAssit/delete', qs.stringify(params), isForm)
}

// 查询产品基准信息
export function selectBaseFundBenchInfoUrl (params) {
  return post('/api/manageView/baseFundBenchInfo/select', qs.stringify(params), isForm)
}

// 添加产品基准信息
export function insertBaseFundBenchInfoUrl (params) {
  return post('/api/manageView/baseFundBenchInfo/insert', params)
}

// 修改产品基准信息
export function updateBaseFundBenchInfoUrl (params) {
  return post('/api/manageView/baseFundBenchInfo/update', params)
}

// 删除产品基准信息
export function deleteBaseFundBenchInfoUrl (params) {
  return post('/api/manageView/baseFundBenchInfo/delete', qs.stringify(params), isForm)
}

// 查询所有的基准信息
export function selectALLbaseFundBenchInfoUrl () {
  return post('/api/manageView/baseFundBenchInfo/selectALL')
}

// 查询文档表的文件上传信息
export function selectDocInfoUrl (params) {
  return post('/api/manageView/doc/select', qs.stringify(params), isForm)
}

// 删除文档表的文件上传信息
export function deleteByIdUrl (params) {
  return post('/api/manageView/doc/deleteById', qs.stringify(params), isForm)
}

// 组合绩效总览信息维护文件下载
export function downloadFileUrl (params) {
  // return `${FILE_URL}/api/manageView/nvestmentCommittee/downloadFile?id=${params.id}&token=${params.token}`
  return `${FILE_URL}/api/manageView/nvestmentCommittee/downloadFile`
}

// 文件下载模板查询
export function listEdimsByNameAndLevelUrl (params) {
  return get('/api/manageView/nvestmentCommittee/listEdimsByNameAndLevel', params)
}

// 模板文件下载
export function downloadTemplateUrl (params) {
  // return `${FILE_URL}/api/manageView/nvestmentCommittee/template/download?fileName=${encodeURIComponent(params.fileName)}&token=${params.token}`
  return `${FILE_URL}/api/manageView/nvestmentCommittee/template/download`
}

// 基准信息维护-查询基准信息
export function selectBaseBenchMarkInfoUrl (params) {
  return post('/api/manageView/baseBenchMarkInfo/select', qs.stringify(params), isForm)
}

// 基准信息维护-添加基准信息
export function insertBaseBenchMarkInfoUrl (params) {
  return post('/api/manageView/baseBenchMarkInfo/insert', params)
}

// 基准信息维护-修改基准信息
export function updateBaseBenchMarkInfoUrl (params) {
  return post('/api/manageView/baseBenchMarkInfo/update', params)
}

// 基准信息维护-删除基准信息
export function deleteBaseBenchMarkInfoUrl (params) {
  return post('/api/manageView/baseBenchMarkInfo/delete', qs.stringify(params), isForm)
}

// 投资经理信息维护-基金相关人员列表展示
export function fundPersonInfoListUrl (params) {
  return post('/api/dataManage/fundPersonInfo/fundPersonInfoList', qs.stringify(params), isForm)
}

// 投资经理信息维护-投资经理下拉选
export function selectInvestManagerUrl () {
  return post('/api/dataManage/fundPersonInfo/selectInvestManager')
}

// 投资经理信息维护-增加投资经理信息
export function insertInvestManagerUrl (params) {
  return post('/api/dataManage/fundPersonInfo/insertInvestManager', qs.stringify(params), isForm)
}

// 投资经理信息维护-修改投资经理信息
export function updateInvestManagerUrl (params) {
  return post('/api/dataManage/fundPersonInfo/updateInvestManager', qs.stringify(params), isForm)
}

// 投资经理信息维护-根据id删除记录
export function deleteFundPersonByIdUrl (params) {
  return post('/api/dataManage/fundPersonInfo/deleteFundPersonById', qs.stringify(params), isForm)
}

// 持仓明细管理类型维护-持仓明细管理类型维护表展示
export function hldDetailMaintenanceListUrl (params) {
  return post('/api/dataManage/hldDetailMaintenance/list', qs.stringify(params), isForm)
}

// 持仓明细管理类型维护-添加持仓明细管理类型记录
export function insertHldDetailMaintenanceUrl (params) {
  return post('/api/dataManage/hldDetailMaintenance/insertHldDetailMaintenance', params)
}

// 持仓明细管理类型维护-修改持仓明细管理类型维护表
export function updateHldDetailMaintenanceUrl (params) {
  return post('/api/dataManage/hldDetailMaintenance/updateHldDetailMaintenance', qs.stringify(params), isForm)
}

// 持仓明细管理类型维护-查询持仓明细表
export function hldDetailListUrl (params) {
  return post('/api/dataManage/hldDetailMaintenance/hldDetailList', qs.stringify(params), isForm)
}

// 持仓明细管理类型维护-根据id删除记录
export function deleteHldByIdUrl (params) {
  return post('/api/dataManage/hldDetailMaintenance/deleteById', qs.stringify(params), isForm)
}

// 查询工作日T-1日和往前推一个月的日期（也为工作日）
export function selectStartEndDateUrl () {
  return get('/api/dataManage/startEndDate/select')
}