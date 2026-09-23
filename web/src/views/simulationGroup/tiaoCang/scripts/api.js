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
 * @description 删除节点
 * @param {*} data 删除入参
 * @returns
 */
export const deleteNodeById = data => {
  return request({
    url: '/api/warehouse/delWarehouseNodeNode',
    method: 'POST',
    data: data
  })
}

/**
 * @description 新增节点
 * @param {*} data 新增入参
 * @returns
 */
export const insertNode = data => {
  return request({
    url: '/api/warehouse/saveWarehouseNodeNode',
    method: 'POST',
    data: data
  })
}

/**
 * @description 节点调仓表格查询
 * @param {*} data 新增入参
 * @returns
 */
export const getNodeTable = data => {
  return request({
    url: '/api/warehouse/selectFund',
    method: 'POST',
    data: data
  })
}

/**
 * @description 模拟组合调仓-编辑
 * @param {*} data 查询入参
 * @returns
 */
export const saveEditFund = data => {
  return request({
    url: '/api/warehouse/updateSubProduct',
    method: 'POST',
    data
  })
}
