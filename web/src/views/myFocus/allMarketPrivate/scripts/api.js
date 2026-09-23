import request from '@/utils/request'

export const findList = data => {
  return request({
    url: '/api/fund2/selectFund',
    method: 'POST',
    data
  })
}

/**
 * @description 单个取消关注
 * @param {*} data 分组信息
 * @returns
 */
export const handleCancelFocusGroup = data => {
  return request({
    url: '/api/myConcern/unfollow',
    method: 'POST',
    data: data
  })
}

/**
 * @description 批量取消关注
 * @param {*} data 分组信息
 * @returns
 */
export const handleBatchCancelFocusGroup = data => {
  return request({
    url: '/api/myConcern/unfollows',
    method: 'POST',
    data: data
  })
}

/**
* @Description: 备注信息保存
* @author Liu Rui Bing
* @date 2024/1/11
*/

export const handleRemark = data => {
  return request({
    url: '/api/myConcern/saveRemark',
    method: 'POST',
    data: data
  })
}
