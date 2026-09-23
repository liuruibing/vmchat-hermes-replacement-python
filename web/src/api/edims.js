import request from '@/utils/request'
/**
 * 获取服务器的当前时间
 */
export function getEdimsAll() {
  return request({
    url: '/api/edimExt/v1.0/edimDetailList',
    method: 'get'
  })
}
