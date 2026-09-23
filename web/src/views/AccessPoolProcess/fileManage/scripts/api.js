import request from '@/utils/request'

export const getUploadFileAll = data => {
  return request({
    url: '/api/fundAccess/approve/selectManage',
    method: 'POST',
    data
  })
}
