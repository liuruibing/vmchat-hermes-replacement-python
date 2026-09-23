import request, { post ,get} from '@/utils/request'
import qs from 'qs'
// Form Data 格式
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  // 组合数调度监控记录
  fun_selectCombTreeRecord: async function (params) {
    return post('/rest/dimFundTrigger/mainLogList.do',qs.stringify(params), isForm)
  },
  // 删除
  fun_deleteEtlFundTriggerLog: async function (params) {
    return post('/rest/dimFundTrigger/deleteEtlFundTriggerLog.do',qs.stringify(params), isForm)
  },
  // 跑数
  fun_dimFundTriggerLogList: async function (params) {
    return post('/rest/dimFundTrigger/reExecuteFundTriggerMission.do',qs.stringify(params), isForm)
  },
  // 明细
  fun_detailLogList: async function (params) {
    return post('/rest/dimFundTrigger/detailLogList.do',qs.stringify(params), isForm)
  },
}
