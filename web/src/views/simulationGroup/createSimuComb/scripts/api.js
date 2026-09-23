import request from '@/utils/request'

const form_headers = {
  'Content-Type': 'multipart/form-data', // 表单数据类型
};
/**
 * @description 新增模拟组合
 * @param {*} data
 * @returns
 */
export const saveComb = data => {
  return request({
    url: '/api/simulate/combine/saveAll',
    method: 'POST',
    data
  })
}

/**
 * @description 模拟组合信息-编辑
 * @param {*} data 查询入参
 * @returns
 */
export const saveEditComb = data => {
  return request({
    url: '/api/simulate/combine/save',
    method: 'POST',
    data
  })
}

/**
 * @description 模拟组合产品-编辑
 * @param {*} data 查询入参
 * @returns
 */
export const saveEditFund = data => {
  return request({
    url: '/api/warehouse/updateSubProduct',
    method: 'POST',
    data
  })
}

/**
 * @description 模拟组合权重-查询
 * @param beginDate ：开始日期(string)
 * @param endDate ：结束日期(string)
 * @param frequent ：频率(string) D\W\M
 * @param vcParentCode： 组合代码(string)
 * @param version ：版本(string)
 * @returns
 */

export const fofMeanSearch = data => {
  return request({
    // url: '/api/assetAllocation/fofMeanSearch',
    url: '/api/virtualfof/fofMeanSearch.do',
    method: 'POST',
    headers:form_headers,
    data
  })
}
