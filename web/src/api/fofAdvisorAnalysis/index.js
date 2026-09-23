import request, { post ,get} from '@/utils/request'

import qs from 'qs'
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectFofAssetExcessReturnAnalysis: async function (params) {
    return post('/api/fofAdvisorAnalysis/select',qs.stringify(params), isForm)
  },
  fun_selectAssetExcessReturnAnalysis: async function (params) {
    return post('/api/fofAdvisorAnalysis/fofSelect',qs.stringify(params), isForm)
  },
  fun_fundSelectAnalysis: async function (params) {
    return post('/api/fofAdvisorAnalysis/fund/select',qs.stringify(params), isForm)
  },
  fun_fundTypeAnalysis: async function (params) {
    return post('/api/fofAdvisorAnalysis/fund/selectType',qs.stringify(params), isForm)
  },
  fun_fundUpdateAnalysis: async function (params) {
    return post('/api/fofAdvisorAnalysis/fund/EditInfo',qs.stringify(params), isForm)
  },

}
