import request from '@/utils/request'

/**
 * @description 查询列表
 * @param {*} data 查询入参
 * @returns
 */
export const findList = data => {
  return request({
    url: '/api/manager/select',
    method: 'POST',
    data
  })
}

/**
 * @description 取消所有分组关注 - 管理人
 */
export const deleteAllFocus = data => {
  return request({
    url: '/api/managerConcern/delProductConcern',
    method: 'POST',
    data
  })
}
