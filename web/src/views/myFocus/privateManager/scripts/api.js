import request from '@/utils/request'

/**
 * @description 查询列表
 * @param {*} data 查询入参
 * @returns
 */
export const findList = data => {
  return request({
    url: '/api/manager/concern/select',
    method: 'POST',
    data
  })
}

/**
 * @description 批量取消关注-管理人
 * @param {*} data 分组信息
 * @returns
 */
export const handleBatchCancelFocusGroup = data => {
  return request({
    url: '/api/managerConcern/unfollows',
    method: 'POST',
    data: data
  })
}

/**
 * @description 单个取消关注
 * @param {*} data 分组信息
 * @returns
 */
export const handleCancelFocusGroup = data => {
  return request({
    url: '/api/managerConcern/unfollow',
    method: 'POST',
    data: data
  })
}
