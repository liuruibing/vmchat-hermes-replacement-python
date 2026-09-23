import request from '@/utils/request'

export function getMenuAll() {
  return request({
    url: '/api/system/v1.0/getMenuAll',
    method: 'get',
  })
}
