/* 数据管理接口 */
import { post, get, excelGet } from '@/utils/request'
import { FILE_URL } from '@/utils/request'
import { getToken } from '@/utils/auth'

import { commonUrl } from '@/utils'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }
// 文件类型
let isFile = { 'Content-Type': 'multipart/form-data' }

export default {
  //查询产品信息
  fun_selectFundInfoList: async function (params) {
    return post('/api/dataManage/FundInfo/selectFundList', qs.stringify(params), isForm)
  },
  //查询产品信息-不关联经理
  fun_selectFundListNotManager: async function (params) {
    return post('/api/dataManage/FundInfo/selectFundListNotManager', qs.stringify(params), isForm)
  },
  //查询全部产品信息 - 权限
  fun_selectFundListAll: async function (params) {
    return post('/api/dataManage/FundInfo/selectFundListAll', qs.stringify(params), isForm)
  },
  //查询一个产品信息
  fun_selectFundInfo: async function (params) {
    return get('/api/dataManage/FundInfo/selectFundInfo?fundCode=' + params)
  },
  //查询一个产品信息
  fun_selectFundStrInfo: async function (params) {
    return get('/api/dataManage/FundInfo/selectFundStrInfo?fundCode=' + params)
  },

  //查询产品编号是否存在
  fun_findRepeatFundCode: async function (params) {
    return post('/api/dataManage/FundInfo/findRepeatFundCode',qs.stringify(params), isForm)
  },
  //添加产品信息
  fun_insertFundInfo: async function (params) {
    return post('/api/dataManage/FundInfo/insertFundInfo',qs.stringify(params), isForm)
  },
  //添加产品信息
  fun_updateFundInfo: async function (params) {
    return post('/api/dataManage/FundInfo/updateFundInfo',qs.stringify(params), isForm)
  },
  //删除产品信息
  fun_deleteFundInfo: async function (params) {
    return post('/api/dataManage/FundInfo/deleteFundInfo',qs.stringify(params), isForm)
  },

  //查询产品附件
  fun_selectFundFiles: async function (params) {
    return post('/api/docCommon/fileCommon/selectFundFiles', qs.stringify(params), isForm)
  },
  //查询产品附件
  downloadFileUrl: async function () {
    return `${FILE_URL}/api/docCommon/fileCommon/downloadFile`
  },
  //查询产品信息列表_销售中心
  fun_selectFundInfoForXSList: async function (params) {
    return post('/api/fundAnalysis/fundInfoForXS/selectFundList', qs.stringify(params), isForm)
  },
  //查询投资经理
  fun_selectFundInvestManager: async function (fundCode,incumbent) {
    return get('/api/dataManage/FundInfo/selectFundInvestManager?fundCode=' + fundCode + '&incumbent=' + incumbent)
  },
  //查询对外投资经理
  fun_selectFundOutInvestManager: async function (fundCode) {
    return get('/api/dataManage/FundInfo/selectFundOutInvestManager?fundCode=' + fundCode)
  },

  //查询账户信息
  fun_selectAccountInfo: async function (params) {
    return get('/api/dataManage/accountInfo/selectById?fundCode=' + params)
  },
  //基金交易席位
  fun_selectFoundationTransaction: async function (params) {
    return get('/api/dataManage/accountInfo/selectFoundationTransaction?fundCode=' + params)
  },
  //存款户席位
  fun_selectDepositTransaction: async function (params) {
    return get('/api/dataManage/accountInfo/selectDepositTransaction?fundCode=' + params)
  },
  //股指期货席位
  fun_selectStockTransaction: async function (params) {
    return get('/api/dataManage/accountInfo/selectStockTransaction?fundCode=' + params)
  },
  //查询合同信息
  fun_selectContractInfo: async function (params) {
    return get('/api/dataManage/contractInfo/selectById?fundCode=' + params)
  },
  //省中心保存合同信息
  fun_saveContractInfoByProvince: async function (params) {
    return post('/api/dataManage/contractInfo/saveContractInfoByProvince', qs.stringify(params), isForm)
  },
  //查询三方映射信息
  fun_selectExtsysMapping: async function (fundCode) {
    return get('/api/dataManage/extsysMapping/selectById?fundCode=' + fundCode)
  },
  //根据产品代码查找外部联系人信息
  fun_selectOutpersonInfo: async function (fundCode) {
    return get('/api/dataManage/outpersonInfo/selectById?fundCode='+fundCode)
  },
  //根据产品代码查找外部联系人变更历史
  fun_selectHistoryById: async function (params) {
    return post('/api/dataManage/outpersonInfo/selectHistoryById', qs.stringify(params), isForm)
  },
  //保存产品基本信息-省中心
  fun_saveBaseInfoByProvice: async function (params) {
    return post('/api/dataManage/FundInfo/saveBaseInfoByProvice', qs.stringify(params), isForm)
  },
  //保存产品外部联系人-省中心
  fun_saveOutPersonByProvice: async function (params) {
    return post('/api/dataManage/FundInfo/saveOutPersonByProvice', qs.stringify(params), isForm)
  },
  //获取组合扩展信息
  fun_getFundExtInfoByCode: async function (fundCode) {
    return get('/api/dataManage/fundExtInfo/getFundExtInfoByCode?fundCode='+fundCode)
  },
  //获取销售部门
  fun_getAgencydeptInfoList: async function () {
    return get('/api/dataManage/fundExtInfo/getAgencydeptInfoList')
  },
  //资金到账情况列表查询
  fun_selectArrivalListPage: async function (params) {
    return post('/api/dataManage/fundArrival/selectListPage', qs.stringify(params), isForm)
  },
  //资金到账情况新增
  fun_insertFundArrival: async function (params) {
    return post('/api/dataManage/fundArrival/insert', qs.stringify(params), isForm)
  },
  //资金到账情况删除
  fun_deleteFundArrival: async function (fId) {
    return post('/api/dataManage/fundArrival/delete?fId='+fId)
  },
  //投资观点新增
  fun_managePerspectiveInsert: async function (params) {
    return post('/api/dataManage/managePerspective/insert', qs.stringify(params), isForm)
  },
  //投资观点编辑
  fun_managePerspectiveUpdate: async function (params) {
    return post('/api/dataManage/managePerspective/update', qs.stringify(params), isForm)
  },
  //投资观点删除
  fun_managePerspectiveDelete: async function (fId) {
    return post('/api/dataManage/managePerspective/delete?fId='+fId)
  },
  //投资观点单个查询
  fun_managePerspectiveSelectById: async function (fId) {
    return post('/api/dataManage/managePerspective/selectById?fId='+fId)
  },
  //投资观点列表
  fun_managePerspectiveSelectListPage: async function (params) {
    return post('/api/dataManage/managePerspective/selectListPage',qs.stringify(params), isForm)
  },
  //投资观点单个查询
  fun_managePerspectiveSelectByCode: async function (params) {
    return post('/api/dataManage/managePerspective/getPerspectiveByCode',qs.stringify(params), isForm)
  },
  //业绩排名新增
  fun_fundPlanExtDataInsert: async function (params) {
    return post('/api/dataManage/fundPlanExtData/insert',qs.stringify(params), isForm)
  },
  //业绩排名修改
  fun_fundPlanExtDataUpdate: async function (params) {
    return post('/api/dataManage/fundPlanExtData/update',qs.stringify(params), isForm)
  },
  //业绩排名删除
  fun_fundPlanExtDataDelete: async function (fundCode,endDate) {
    return post('/api/dataManage/fundPlanExtData/delete?fundCode='+fundCode+'&endDate='+endDate)
  },
  //业绩排名单个数据
  fun_fundPlanExtDataSelectById: async function (fundCode,planCode,endDate) {
    return post('/api/dataManage/fundPlanExtData/selectById?fundCode='+fundCode+'&planCode='+planCode+'&endDate='+endDate)
  },
  //业绩排名列表查询
  fun_fundPlanExtDataSelectListPage: async function (params) {
    return post('/api/dataManage/fundPlanExtData/selectListPage',qs.stringify(params), isForm)
  },
  //查询计划内组合
  fun_fundPlanExtDataSelectPlanFund: async function (fundCode) {
    return post('/api/dataManage/fundPlanExtData/selectPlanFund?fundCode='+fundCode)
  },
  //查询管理人信息(分类信息)
  fun_selectFundManagerList: async function () {
    return post('/api/fundManager/selectListData')
  },
  //查询产品信息-内外部穿透
  fun_selectFundListCT: async function (params) {
    return post('/api/dataManage/FundInfo/selectFundListCT', qs.stringify(params), isForm)
  },
  //查询产品信息-查询产品分类信息
  fun_selectFundClassificationList: async function (params) {
    return post('/api/dataManage/FundInfo/selectFundClassificationList', qs.stringify(params), isForm)
  },


}













