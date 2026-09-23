import request from '@/utils/request'

/**
 * @description 标准化需求管理 - 功能后台 - 列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/standArd/needManage/adminSelect',
    method: 'POST',
    data
  })
}

/**
 * @description 标准化需求管理 - 功能后台 - 详情获取文件列表
 * @param {*} data
 * @returns
 */
export const getUplodFile = data => {
  return request({
    url: '/api/standArd/needManage/selectEdit',
    method: 'POST',
    data
  })
}

/**
 * @description 标准化需求管理 - 功能后台 - 处理
 * @param {*} data
 * @returns
 */
export const handleDispose = data => {
  return request({
    contentType: false, //这里不要落下
    dataType: 'json',
    url: '/api/standArd/needManage/adminDispose',
    method: 'POST',
    data
  })
}
