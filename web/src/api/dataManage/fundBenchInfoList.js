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
  //列表查询
  fun_selectListPage: async function (params) {
    return post('/api/dataManage/fundBenchInfo/selectListPage', qs.stringify(params), isForm)
  },
  //单个查询
  fun_selectById: async function (params) {
    return post('/api/dataManage/fundBenchInfo/selectById', qs.stringify(params), isForm)
  },
  //根据fundCode查找
  fun_selectBenchByFund: async function (params) {
    return post('/api/dataManage/fundBenchInfo/selectBenchByFund', qs.stringify(params), isForm)
  },
  //新增
  fun_insert: async function (params) {
    return post('/api/dataManage/fundBenchInfo/insert', qs.stringify(params), isForm)
  },
  //更新
  fun_update: async function (params) {
    return post('/api/dataManage/fundBenchInfo/update', qs.stringify(params), isForm)
  },
  //删除
  fun_delete: async function (params) {
    return post('/api/dataManage/fundBenchInfo/delete', qs.stringify(params), isForm)
  },
}













