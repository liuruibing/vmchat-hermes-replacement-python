import request from '@/utils/request'

export function loginByUsername() {
    return request({
    url: '/api/report/v1.0/data/preview/4D84EABB6F2649759E711C9DE17AD322',
    method: 'get',
  })
}


