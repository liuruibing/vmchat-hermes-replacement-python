import request from '@/utils/request'
import qs from 'qs'
export default {
  selectIndexList: async function () {
    return request.get('/api/gfhomepage/selectIndexList')
  },
  //管理人日收益率曲线/产品/私募指数、市场指数
  doCompanyFundAndIndexChart: async function (params) {
    return request.post('/api/report/v1.0/data/sql/7db73307-f551-46f7-a8d5-d9582cdff872', params)
  },

}
