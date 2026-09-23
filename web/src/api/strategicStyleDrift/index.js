import request, { post ,get} from '@/utils/request'

import qs from 'qs'
let isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  fun_selectStrategicStyleDrift: async function (params) {
    return post('/api/strategicStyleDrift/select',qs.stringify(params, { arrayFormat: 'repeat' }), isForm)
  },

}
