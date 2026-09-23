import request from '@/utils/request'

/**
 * @description 模拟组合列表-编辑
 * @param {*} data 查询入参
 * @returns
 */
export const saveEditComb = data => {
  return request({
    url: '/api/simulate/combine/save',
    method: 'POST',
    data
  })
}
