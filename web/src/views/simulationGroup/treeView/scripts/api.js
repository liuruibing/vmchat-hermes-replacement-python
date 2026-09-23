import request from '@/utils/request'

/**
 * @description 查询节点
 * @param {*} data 查询入参
 * @returns
 */
export const getNodeList = data => {
  return request({
    url: '/api/warehouse/findNode',
    method: 'POST',
    data
  })
}

/**
 * @description 查询节点
 * @param {*} data 查询入参
 * @returns
 */
export const getTreeData = data => {
  return request({
    url: '/api/warehouse/selectNodeByTree',
    method: 'POST',
    data
  })
}
