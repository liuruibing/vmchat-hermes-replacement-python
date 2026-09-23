import request from '@/utils/request'
import qs from 'qs'
export default {
  thisYearCard: async function (params) {
    return request.post('/api/gfhomepage/thisYearCard',params)
  },
  thisSeasonCard: async function (params) {
    return request.post('/api/gfhomepage/thisSeasonCard',params)
  },
  thisMonthCard: async function (params) {
    return request.post('/api/gfhomepage/thisMonthCard',params)
  },
}