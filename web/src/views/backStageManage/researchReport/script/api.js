import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }

export const reportList = data => {
  return request({
    url: '/api/article/manage/selectArticleList',
    method: 'POST',
    data
  })
}

export const saveReport = data => {
  return request({
    headers: FileFormData,
    url: '/api/article/manage/saveArticle',
    method: 'POST',
    data
  })
}

export const deleteReport = data => {
  return request({
    url: '/api/article/manage/deleteArticle',
    method: 'POST',
    data
  })
}

export const editArticle = data => {
  return request({
    url: '/api/article/manage/editArticle',
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
