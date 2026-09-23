import request from '@/utils/request'
import qs from 'qs'
export default {
  totalDescription: async function (params) {
    return request.post('/api/gfhomepage/totalDescription',params)
  },
}