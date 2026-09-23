import request from '@/utils/request'

/**
 * @description 个性化需求管理 - 列表查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/standArd/indivduation/select',
    method: 'POST',
    data
  })
}

/**
 * @description 个性化需求管理 - 新增
 * @param {*} data
 * @returns
 */
export const insertDemand = params => {
  return request({
    contentType: false, //这里不要落下
    dataType: 'json',
    url: '/api/standArd/indivduation/insertUpload',
    data: params,
    method: 'post'
  })
}

/**
 * @description 个性化需求管理 - 编辑
 * @param {*} data
 * @returns
 */
export const uploadDemand = params => {
  return request({
    contentType: false, //这里不要落下
    dataType: 'json',
    url: '/api/standArd/indivduation/updateUpload',
    data: params,
    method: 'post'
  })
}

/**
 * @description 个性化需求管理 - 删除
 * @param {*} data
 * @returns
 */
export const deleteDemand = data => {
  return request({
    url: '/api/standArd/indivduation/delete',
    method: 'POST',
    data
  })
}

/**
 * @description 个性化需求管理 - 提交
 * @param {*} data
 * @returns
 */
export const submitDemand = data => {
  return request({
    url: '/api/standArd/indivduation/submit',
    method: 'POST',
    data
  })
}

/**
 * @description 个性化需求管理 - 详情获取文件列表
 * @param {*} data
 * @returns
 */
export const getUplodFile = data => {
  return request({
    url: '/api/standArd/indivduation/selectEdit',
    method: 'POST',
    data
  })
}
