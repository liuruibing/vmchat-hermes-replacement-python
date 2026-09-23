import request from '@/utils/request'

/**
 * @description 查询回测分析数据
 * @param {*} data 查询入参
 * @returns
 */
export const queryBackTestData = data => {
  return request({
    url: '/api/simulate/backtest/getBackTestData',
    method: 'POST',
    data
  })
}
