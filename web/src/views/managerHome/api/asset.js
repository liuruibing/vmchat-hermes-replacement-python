import request from '@/utils/request'
import qs from 'qs'
export default {
  assetEndTablePie: async function (params) {
    return request.post('/api/gfhomepage/assetEndTablePie',params)
  },
}