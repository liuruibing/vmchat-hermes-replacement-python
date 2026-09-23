import request from '@/utils/request'
const FileFormData = { 'Content-Type': 'multipart/form-data' }

/**
 * @description 指数分类列表
 * @param {*} data
 * @returns
 */
export const selectPrivateIndexClassifyList = data => {
  return request({
    url: '/api/gfprivateindex/selectPrivateIndexClassifyList',
    method: 'POST',
    data
  })
}

/**
 * @description 指数分页查询
 * @param {*} data
 * @returns
 */
export const selectPrivateIndexByPage = data => {
  return request({
    url: '/api/gfprivateindex/selectPrivateIndexByPage',
    method: 'POST',
    data
  })
}

/**
 * @description 新增指数
 * @param {*} data
 * @returns
 */
export const insertPrivateIndex= data => {
  return request({
    url: '/api/gfprivateindex/insertPrivateIndex',
    method: 'POST',
    data
  })
}

/**
 * @description 修改指数
 * @param {*} data
 * @returns
 */
export const updatePrivateIndex= data => {
  return request({
    url: '/api/gfprivateindex/updatePrivateIndex',
    method: 'POST',
    data
  })
}

/**
 * @description 生成私募指数代码
 * @param {*} data
 * @returns
 */
export const generatePrivateIndexCode= data => {
  return request({
    url: '/api/gfprivateindex/generatePrivateIndexCode',
    method: 'POST',
    data
  })
}

/**
 * @description 私募指数代码校验
 * @param {*} data
 * @returns
 */
export const checkPrivateIndexCode= data => {
  return request({
    url: '/api/gfprivateindex/checkPrivateIndexCode',
    method: 'POST',
    data
  })
}

/**
 * @description 私募指数名称校验
 * @param {*} data
 * @returns
 */
export const checkPrivateIndexName= data => {
  return request({
    url: '/api/gfprivateindex/checkPrivateIndexName',
    method: 'POST',
    data
  })
}


/**
 * @description 停用私募指数
 * @param {*} data
 * @returns
 */
export const setPrivateIndexDisable= data => {
  return request({
    url: '/api/gfprivateindex/setPrivateIndexDisable',
    method: 'POST',
    data
  })
}

/**
 * @description 启用私募指数
 * @param {*} data
 * @returns
 */
export const setPrivateIndexAble= data => {
  return request({
    url: '/api/gfprivateindex/setPrivateIndexAble',
    method: 'POST',
    data
  })
}


/**
 * @description 首页显示
 * @param {*} data
 * @returns
 */
export const setPrivateIndexHomePageShowStatus= data => {
  return request({
    url: '/api/gfprivateindex/setPrivateIndexHomePageShowStatus',
    method: 'POST',
    data
  })
}


/**
 * @description 首页隐藏
 * @param {*} data
 * @returns
 */
export const setPrivateIndexHomePageHideStatus= data => {
  return request({
    url: '/api/gfprivateindex/setPrivateIndexHomePageHideStatus',
    method: 'POST',
    data
  })
}


/**
 * @description 删除私募指数
 * @param {*} data
 * @returns
 */
export const deletePrivateIndex= data => {
  return request({
    url: '/api/gfprivateindex/deletePrivateIndex',
    method: 'POST',
    data
  })
}

/**
 * @description 生成分类代码
 * @param {*} data
 * @returns
 */
export const generatePrivateIndexClassifyCode= data => {
  return request({
    url: '/api/gfprivateindex/generatePrivateIndexClassifyCode',
    method: 'POST',
    data
  })
}


/**
 * @description 分类代码校验
 * @param {*} data
 * @returns
 */
export const checkPrivateIndexClassifyCode= data => {
  return request({
    url: '/api/gfprivateindex/checkPrivateIndexClassifyCode',
    method: 'POST',
    data
  })
}


/**
 * @description 分类名称校验
 * @param {*} data
 * @returns
 */
export const checkPrivateIndexClassifyName= data => {
  return request({
    url: '/api/gfprivateindex/checkPrivateIndexClassifyName',
    method: 'POST',
    data
  })
}

/**
 * @description 新增分类
 * @param {*} data
 * @returns
 */
export const insertPrivateIndexClassify= data => {
  return request({
    url: '/api/gfprivateindex/insertPrivateIndexClassify',
    method: 'POST',
    data
  })
}

/**
 * @description 修改分类
 * @param {*} data
 * @returns
 */
export const updatePrivateIndexClassify= data => {
  return request({
    url: '/api/gfprivateindex/updatePrivateIndexClassify',
    method: 'POST',
    data
  })
}

/**
 * @description 删除指数分类
 * @param {*} data
 * @returns
 */
export const deletePrivateIndexClassify= data => {
  return request({
    url: '/api/gfprivateindex/deletePrivateIndexClassify',
    method: 'POST',
    data
  })
}


/**
 * @description 私募指数列表
 * @param {*} data
 * @returns
 */
export const selectPrivateIndexList= data => {
  return request({
    url: '/api/gfprivateindexcomponent/selectPrivateIndexList',
    method: 'POST',
    data
  })
}

/**
 * @description 私募指数成分分页查询
 * @param {*} data
 * @returns
 */
export const selectPrivateIndexComponentByPage= data => {
  return request({
    url: '/api/gfprivateindexcomponent/selectPrivateIndexComponentByPage',
    method: 'POST',
    data
  })
}


/**
 * @description 私募指数成分删除
 * @param {*} data
 * @returns
 */
export const deletePrivateIndexComponent= data => {
  return request({
    url: '/api/gfprivateindexcomponent/deletePrivateIndexComponent',
    method: 'POST',
    data
  })
}


/**
 * @description 私募指数成分批量删除
 * @param {*} data
 * @returns
 */
export const deleteBatchPrivateIndexComponent= data => {
  return request({
    url: '/api/gfprivateindexcomponent/deleteBatchPrivateIndexComponent',
    method: 'POST',
    data
  })
}

/**
 * @description 私募指数成分新增
 * @param {*} data
 * @returns
 */
export const insertPrivateIndexComponent= data => {
  return request({
    url: '/api/gfprivateindexcomponent/addPrivateIndexComponent',
    method: 'POST',
    data
  })
}


/**
 * @description 私募指数成分修改
 * @param {*} data
 * @returns
 */
export const updatePrivateIndexComponent= data => {
  return request({
    url: '/api/gfprivateindexcomponent/editPrivateIndexComponent',
    method: 'POST',
    data
  })
}


/**
 * @description 上传私募指数成分excle 文件
 * @param {*} data
 * @returns
 */
export const uploadPrivateIndexComponentFile = data => {
  return request({
    headers: FileFormData,
    url: '/api/gfprivateindexcomponent/importExportPrivateIndexComponentUpload',
    method: 'post',
    data: data
  })
}

/**
 * @description 私募指数行情-开始结束日期查询
 * @returns
 */
export const selectDate= () => {
  return request({
    url: '/api/gfprivateindexmarket/selectDate',
    method: 'POST'
  })
}

/**
 * @description 私募指数行情-分页查询
 * @param {*} data
 * @returns
 */
export const selectPrivateIndexMarketByPage= data => {
  return request({
    url: '/api/gfprivateindexmarket/selectPrivateIndexMarketByPage',
    method: 'POST',
    data
  })
}
/**
 * @description 私募指数行情-重新计算
 * @param {*} data
 * @returns
 */
export const recalculatePrivateIndexMarket= data => {
  return request({
    url: '/api/gfprivateindexmarket/reExecutePrivateIndexMarket',
    method: 'POST',
    data
  })
}









