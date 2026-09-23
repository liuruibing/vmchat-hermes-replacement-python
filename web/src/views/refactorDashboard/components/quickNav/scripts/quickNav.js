import request from '@/utils/request'

/**
 * @description 获取用户快捷导航列表
 * @returns {Promise}
 */
export const getQuickNavList = (data = {}) => {
  return request({
    url: '/api/sysQuickNav/getQuickNavList',
    method: 'POST',
    data
  })
}

/**
 * @description 保存用户快捷导航配置
 * @returns {Promise}
 */
export const saveQuickNav = (data) => {
  return request({
    url: '/api/sysQuickNav/saveQuickNav',
    method: 'POST',
    data
  })
}
