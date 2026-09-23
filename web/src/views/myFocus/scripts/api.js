import request from '@/utils/request'

/**
 * @description 查询列表
 * @param {*} data 查询入参
 * @returns
 */
export const findList = data => {
  return request({
    url: '/api/fund2/concern/selectFund',
    method: 'POST',
    data
  })
}

export const delFundPool = data => {
  return request({
    url: '/api/myConcern/delFundPool',
    method: 'POST',
    data
  })
}

export const saveFundPool = data => {
  return request({
    url: '/api/myConcern/saveFundPool',
    method: 'POST',
    data
  })
}

export const renameFundPool = data => {
  return request({
    url: '/api/myConcern/renameFundPool',
    method: 'POST',
    data
  })
}

export const delManagerPool = data => {
  return request({
    url: '/api/managerConcern/delManagerPool',
    method: 'POST',
    data
  })
}

export const saveManagerPool = data => {
  return request({
    url: '/api/managerConcern/saveManagerPool',
    method: 'POST',
    data
  })
}

export const renameManagerPool = data => {
  return request({
    url: '/api/managerConcern/renameManagerPool',
    method: 'POST',
    data
  })
}
