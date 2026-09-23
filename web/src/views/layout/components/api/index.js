import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }

export const getPwdStrategy = data => {
  return request({
    url: '/api/system/passwordPolicy/getPwdStrategy',
    method: 'get'
  })
}
