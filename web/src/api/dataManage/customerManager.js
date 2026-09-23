import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {


  // 经理列表
  fun_selectList: async function (params) {
    return post('/api/dataManage/customerInfo/selectList',qs.stringify(params), isForm)
  },
  // 根据ID查单个经理
  fun_selectById: async function (fId) {
    return get('/api/dataManage/customerInfo/selectInfoById?fId='+fId)
  },
  // 查询产品客户经理历史 分页
  fun_selectHisttoryByFund: async function (params) {
    return post('/api/dataManage/customerInfo/selectHisttoryByFund',qs.stringify(params), isForm)
  },
  // 查询产品客户经理
  fun_selectFundCustomers: async function (fundCode) {
    return post('/api/dataManage/customerInfo/selectFundCustomers?fundCode='+fundCode)
  },
  // 经理列表 分页
  fun_selectListPage: async function (params) {
    return post('/api/dataManage/customerInfo/selectListPage',qs.stringify(params), isForm)
  },
  // 经理列表 导出
  fun_selectListPageExport: async function (ex_tmp_name,params) {
    return post('/api/dataManage/customerInfo/selectListPage?ex_tmp_name='+ex_tmp_name,qs.stringify(params), isForm)
  },
  // 新增经理
  fun_insertManger: async function (params) {
    return post('/api/dataManage/customerInfo/insert',qs.stringify(params), isForm)
  },
  // 修改经理
  fun_updateManger: async function (params) {
    return post('/api/dataManage/customerInfo/update',qs.stringify(params), isForm)
  },
  // 删除经理
  fun_deleteManager: async function (fId) {
    return get('/api/dataManage/customerInfo/delete?fId='+fId)
  }





}
