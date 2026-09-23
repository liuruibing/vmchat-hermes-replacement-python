import request from '@/utils/request'

/**
 * @description 获取用户指定模块的模板列表
 * @returns
 */
export const getTemplateList = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/getTemplateList',
    method: 'POST',
    data
  })
}

/**
 * @description 获取模板内容
 * @returns
 */
export const getTemplateContent = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/getTemplateContent',
    method: 'POST',
    data
  })
}

/**
 * @description 新增模板
 * @returns
 */
export const addTemplate = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/addTemplate',
    method: 'POST',
    data
  })
}

/**
 * @description 更新模板内容
 * @returns
 */
export const updateTemplateContent = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/updateTemplateContent',
    method: 'POST',
    data
  })
}

/**
 * @description 删除模板
 * @returns
 */
export const deleteTemplate = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/deleteTemplate',
    method: 'POST',
    data
  })
}

/**
 * @description 清除模板内容
 * @returns
 */
export const clearTemplateContent = data => {
  return request({
    url: '/api/cmbblfof/sysTemplate/clearTemplateContent',
    method: 'POST',
    data
  })
}
