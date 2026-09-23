import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {


  // 投资经理列表
  managerList: async function (params) {
    return post('/api/managerView/investManager/managerList',qs.stringify(params), isForm)
  },
  // 根据ID查单个经理
  fun_selectById: async function (fId) {
    return get('/api/managerView/investManager/selectById?fId='+fId)
  },
  // 根据ID查单个经理
  fun_selectByCode: async function (managerCode) {
    return get('/api/managerView/investManager/selectByCode?managerCode='+managerCode)
  },
  // 投资经理列表 分页
  managerListPage: async function (params) {
    return post('/api/managerView/investManager/managerListPage',qs.stringify(params), isForm)
  },
  // 投资经理列表 导出
  managerListPageExport: async function (ex_tmp_name,params) {
    return post('/api/managerView/investManager/managerListPage?ex_tmp_name='+ex_tmp_name,qs.stringify(params), isForm)
  },
  // 新增投资经理
  fun_insertManger: async function (params) {
    return post('/api/managerView/investManager/insertManager',qs.stringify(params), isForm)
  },
  // 修改投资经理
  fun_updateManger: async function (params) {
    return post('/api/managerView/investManager/updateManager',qs.stringify(params), isForm)
  },
  // 投资经理分析通用列表
  fun_selectInvestManagerListAnalysis: async function (params) {
    return post('/api/managerView/investManager/selectInvestManagerListAnalysis',qs.stringify(params), isForm)
  },
  // 组合查看列表
  fun_selectCheckFund: async function (params) {
    return post('/api/managerView/investManager/selectCheckFund',qs.stringify(params), isForm)
  },
  // 删除投资经理
  fun_deleteManager: async function (fId) {
    return get('/api/managerView/investManager/deleteManager?fId='+fId)
  },
  // 验证重复编码
  fun_selectAlreadyCode: async function (vcManagerCode) {
    return get('/api/managerView/investManager/selectAlreadyCode?vcManagerCode='+vcManagerCode)
  },





}
