import request from '@/utils/request'
import qs from 'qs'
export default {
  netPriceTimeData: async function (params) {
    return request.post('/api/gfhomepage/netPriceTimeData',params)
  },
}