import request from '@/utils/request'

export const selectArticle = data => {
  return request({
    url: '/api/article/selectArticle',
    method: 'POST',
    data
  })
}
export const selectArticleList = data => {
  return request({
    url: '/api/article/selectArticleList',
    method: 'POST',
    data
  })
}

export const replaceHtmlS3ImageSrcToBase64 = data => {
  return request({
    url: '/api/article/replaceHtmlS3ImageSrcToBase64',
    method: 'POST',
    data
  })
}


