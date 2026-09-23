import request from '@/utils/request'

export const selectArticle = data => {
  return request({
    url: '/api/article/selectArticle',
    method: 'POST',
    data
  })
}
