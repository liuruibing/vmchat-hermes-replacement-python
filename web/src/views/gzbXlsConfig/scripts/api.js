import request from '@/utils/request'


/**
 * @description 估值表模板配置查询
 * @param {*} data
 * @returns
 */
export const queryTableList = data => {
  return request({
    url: '/api/gzrest/doGzbXlsConfigList',
    method: 'POST',
    data
  })
}

/**
 * @description 新增
 * @param {*} data
 * @returns
 */
export const insertGzbXlsConfig= data => {
  return request({
    url: '/api/gzrest/doAddGzbXlsConfig',
    method: 'POST',
    data
  })
}

/**
 * @description 修改
 * @param {*} data
 * @returns
 */
export const updateGzbXlsConfig= data => {
  return request({
    url: '/api/gzrest/doEditGzbXlsConfig',
    method: 'POST',
    data
  })
}

/**
 * @description 删除
 * @param {*} data
 * @returns
 */
export const deleteGzbXlsConfig = data => {
  return request({
    url: '/api/gzrest/doDelGzbXlsConfig',
    method: 'POST',
    data
  })
}




