import request, { post ,get} from '@/utils/request'

import qs from 'qs'
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectAuditLogs: async function (params) {
    return post('/api/AuditLogs/select',qs.stringify(params), isForm)
  },
  fun_selectAuditLogsxx: async function (params) {
    return post('/api/AuditLogs/xx/select',qs.stringify(params), isForm)
  },
}
