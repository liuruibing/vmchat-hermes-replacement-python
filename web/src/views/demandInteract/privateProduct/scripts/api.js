import request from '@/utils/request'

/**
 * @description 需求互动 - 私有产品列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/afterManage/selectPrivateProduct',
    method: 'POST',
    data
  })
}

/**
 * @description 需求互动 - 私有产品列表删除
 * @param {*} data
 * @returns
 */
export const deleteTableList = data => {
  return request({
    url: '/api/afterManage/delete',
    method: 'POST',
    data
  })
}

/**
 * @description 需求互动 - 估值模板配置
 * @param {*} data
 * @returns
 */
export const saveTemplate = data => {
  return request({
    url: '/api/afterManage/saveTemplate',
    method: 'POST',
    data
  })
}

/**
 * @description 需求互动 - 新增 | 编辑
 * @param {*} data
 * @returns
 */
export const saveFund = data => {
  return request({
    url: '/api/afterManage/save',
    method: 'POST',
    data
  })
}
/**
 * @description 新增前校验产品代码是否已存在
 * @returns data 为 true 表示已存在
 */
export const checkFundCodeExists = data => {
  return request({
    url: '/api/afterManage/checkFundCode',
    method: 'POST',
    data
  })
}

/**
 * @description 私有产品 授权用户树
 * @param {*} data
 * @returns
 */
export const userZtrees = data => {
  return request({
    url: '/api/afterManage/userZtrees',
    method: 'POST',
    data
  })
}

/**
 * @description 私有产品 授权
 * @param {*} data
 * @returns
 */
export const authorization = data => {
  return request({
    url: '/api/afterManage/authorization',
    method: 'POST',
    data
  })
}

