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
  //产品投资经理关联列表
  fun_selectFundManagerList: async function (params) {
    return post('/api/dataManage/fundInvestManager/selectFundManagerList', qs.stringify(params), isForm)
  },
  //新增产品经理关联
  fun_insertFundManager: async function (params) {
    return post('/api/dataManage/fundInvestManager/insertFundManager', qs.stringify(params), isForm)
  },
  //修改产品经理关联
  fun_updateFundManager: async function (params) {
    return post('/api/dataManage/fundInvestManager/updateFundManager', qs.stringify(params), isForm)
  },
  //删除产品经理关联
  fun_deleteFundManager: async function (params) {
    return post('/api/dataManage/fundInvestManager/deleteFundManager', qs.stringify(params), isForm)
  },
  //查询产品投资经理信息
  fun_selectFundManager: async function (params) {
    return post('/api/dataManage/fundInvestManager/selectFundManager', qs.stringify(params), isForm)
  },
}













