import request from '@/utils/request'

/**
 * @description 查询列表
 * @param {*} data 查询入参
 * @returns
 */
export const findList = data => {
  return request({
    url: '/api/fund2/selectFund',
    method: 'POST',
    data
  })
}

/**
 * @description 取消所有分组关注
 */
export const deleteAllFocus = data => {
  return request({
    url: '/api/myConcern/delProductConcern',
    method: 'POST',
    data
  })
}

// 下载产品清单模板
export const downloadFundTemplate= async function () {
  return request({
    url: '/api/common/fundInfoCommon/downloadFundTemplate',
    method: 'get',
    responseType: 'blob'
  })
}

// 上传解析产品清单Excel
export const parseFundExcel = async function (formData) {
  return request({
    url: '/api/common/fundInfoCommon/parseFundExcel',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data' // 表单上传格式
    }
  })
}
