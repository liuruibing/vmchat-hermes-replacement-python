import request from '@/utils/request'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const qs = require('qs');
export default {

  checkPassword: async function (params) {
    return request({
      headers:ContentTypeFormData,
      url: '/api/system/passwordPolicy/checkPassword',
      method: 'post',
      data: qs.stringify(params)
    })
  },

}
