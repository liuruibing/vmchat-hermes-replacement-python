import request from '@/utils/request'

/**
 * @description 取消所有分组关注
 */
export const deleteAllFocus = data => {
  return request({
    url: '/api/myConcern/delProductConcern',
    method: 'POST',
    data
  })
}

/**
 * @description 查询列表
 * @param {*} data 查询入参
 * @returns
 */
export const findList = data => {
  return request({
    url: '/api/fund2/selectFund',
    method: 'POST',
    data
  })
}
