import request from '@/utils/request'

/**
 * @description 所有下拉数据
 * @param {*} data
 * @returns
 */
export const allOptionsList = data => {
  return request({
    url: '/api/fundinfo/allOptions',
    method: 'POST',
    data
  })
}

/**
 * @description 产品信息维护列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/fundinfo/fundInfoList',
    method: 'POST',
    data
  })
}
/**
 * 新增前校验产品代码是否已存在
 */
export const checkFundCodeExists = data => {
  return request({
    url: '/api/fundinfo/checkFundCode',
    method: 'POST',
    data
  })
}

/**
 * @description 生成代码接口
 * @param {*} data
 * @returns
 */
export const generateList = data => {
  return request({
    url: '/api/fundinfo/generateFundCode',
    method: 'POST',
    data
  })
}
/**
 * @description 管理人弹窗
 * @param {*} data
 * @returns
 */
export const managerList = data => {
  return request({
    url: '/api/simplemanager/managerList',
    method: 'POST',
    data
  })
}

/**
 * @description 产品列表删除
 * @param {*} data
 * @returns
 */
export const deleteTableList = data => {
  return request({
    url: '/api/fundinfo/deleteFundInfo',
    method: 'POST',
    data
  })
}

/**
 * @description 估值模板配置
 * @param {*} data
 * @returns
 */
export const updateTemplate = data => {
  return request({
    url: '/api/fundinfo/updateTemplate',
    method: 'POST',
    data
  })
}

/**
 * @description 新增
 * @param {*} data
 * @returns
 */
export const insertFund = data => {
  return request({
    url: '/api/fundinfo/insertFundInfo',
    method: 'POST',
    data
  })
}
/**
 * @description  编辑
 * @param {*} data
 * @returns
 */
export const updateFund = data => {
  return request({
    url: '/api/fundinfo/updateFundInfo',
    method: 'POST',
    data
  })
}


