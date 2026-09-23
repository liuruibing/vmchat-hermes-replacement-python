import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }

export const getExamineAll = data => {
  return request({
    url: '/api/fundAccess/approve/selectFund',
    method: 'POST',
    data
  })
}

export const saveNewFund = data => {
  return request({
    url: '/api/fundAccess/approve/saveFund',
    method: 'POST',
    data
  })
}

export const uploadFile = data => {
  return request({
    headers: FileFormData,
    url: '/api/fundAccess/approve/upload',
    method: 'post',
    data: data
  })
}

export const getSubmitAll = data => {
  return request({
    url: '/api/fundAccess/approve/selectApproveFiles',
    method: 'POST',
    data
  })
}

export const submitExamine = data => {
  return request({
    url: '/api/fundAccess/approve/submit',
    method: 'POST',
    data
  })
}

export const deleteFile = data => {
  return request({
    url: '/api/fundAccess/approve/deletefile',
    method: 'POST',
    data
  })
}

export const saveNote = data => {
  return request({
    url: '/api/fundAccess/approve/saveNote',
    method: 'POST',
    data
  })
}

export const saveRemark = data => {
  return request({
    url: '/api/fundAccess/approve/saveRemark',
    method: 'POST',
    data
  })
}

export const saveExamine = data => {
  return request({
    url: '/api/fundAccess/approve/approve',
    method: 'POST',
    data
  })
}

export const deleteFund = data => {
  return request({
    url: '/api/fundAccess/approve/deleteFund',
    method: 'POST',
    data
  })
}
