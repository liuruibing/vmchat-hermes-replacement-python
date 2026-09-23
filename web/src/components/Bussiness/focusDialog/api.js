import request from '@/utils/request'

/**
 * @description 保存单个关注分组
 * @param {*} data 分组信息
 * @returns
 */
export const handleFocusGroup = data => {
  return request({
    url: '/api/myConcern/concern',
    method: 'POST',
    data
  })
}

/**
 * @description 保存批量关注分组
 * @param {*} data 分组信息
 * @returns
 */
export const handleBatchFocusGroup = data => {
  return request({
    url: '/api/myConcern/batchConcern',
    method: 'POST',
    data: data
  })
}

/**
 * @description 移动复制分组
 * @param {*} data 分组信息
 * @returns
 */
export const removeMyConcern = data => {
  return request({
    url: '/api/myConcern/removeMyConcern',
    method: 'POST',
    data: data
  })
}
