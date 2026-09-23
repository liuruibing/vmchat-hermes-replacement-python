import request from '@/utils/request'

/**
 * @description 投后管理 - 我的组合列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/afterManage/selectCombine',
    method: 'POST',
    data
  })
}
