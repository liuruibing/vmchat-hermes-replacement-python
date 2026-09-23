import request from '@/utils/request'
import qs from 'qs'
export default {
  selectCompanyListAndDates: async function () {
    return request.get('/api/gfhomepage/selectCompanyListAndDates')
  },
  selectFundListAndDates: async function (companyId) {
    return request.get('/api/gfhomepage/selectFundListAndDates?companyId=' + companyId)
  },
}