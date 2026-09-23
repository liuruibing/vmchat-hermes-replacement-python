import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }

/**
 * @description 热点推荐机构分页查询
 * @param {*} data
 * @returns
 */
export const selectHotOrgMaintenaceByPage = data => {
  return request({
    url: '/api/hotorg/list',
    method: 'POST',
    data
  })
}


/**
 * @description 删除热点机构
 * @param {*} data
 * @returns
 */
export const deleteHotReg = data => {
  return request({
    url: '/api/hotorg/deleteHotReg',
    method: 'POST',
    data
  })
}

/**
 * @description 新增热点机构
 * @param {*} data
 * @returns
 */
export const insertHotReg = data => {
  return request({
    headers: FileFormData,
    url: '/api/hotorg/insertHotReg',
    method: 'POST',
    data
  })
}

/**
 * @description 修改热点机构
 * @param {*} data
 * @returns
 */
export const updateHotReg = data => {
  return request({
    headers: FileFormData,
    url: '/api/hotorg/updateHotReg',
    method: 'POST',
    data
  })
}


/**
 * @description 机构查询
 * @param {*} data
 * @returns
 */
export const selectOrgInstListByPage = data => {
  return request({
    url: '/api/hotorg/orgInstList',
    method: 'POST',
    data
  })
}

