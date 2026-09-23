import request, { post ,get} from '@/utils/request'
// 公共处理函数
import { commonUrl } from '@/utils'
import { FILE_URL } from '@/utils/request'

import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {


  // 列表查询
  fun_selectListPage: async function (params) {
    return post('/api/dataManage/fundFile/selectListPage',qs.stringify(params), isForm)
  },
  // 列表查询-关联政策文件
  fun_selectPolicyListPage: async function (params) {
    return post('/api/dataManage/fundFile/selectPolicyListPage',qs.stringify(params), isForm)
  },

  // 单个查询
  fun_selectById: async function (fId) {
    return post('/api/dataManage/fundFile/selectById?fId='+fId)
  },

  // 新增
  fun_insert: async function (params) {
    return post('/api/dataManage/fundFile/insert',qs.stringify(params), isForm)
  },
  // 修改
  fun_update: async function (params) {
    return post('/api/dataManage/fundFile/update',qs.stringify(params), isForm)
  },
  // 删除
  fun_delete: async function (fId) {
    return post('/api/dataManage/fundFile/delete?fId='+fId)
  },

  //下载附件
  downloadFileUrl: async function () {
    return `${FILE_URL}/api/dataManage/fundFile/downloadFile`
  },

  // 修改
  fun_selectLogListPage: async function (params) {
    return post('/api/dataManage/fundFileLog/selectListPage',qs.stringify(params), isForm)
  },
}
