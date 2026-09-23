import request from '@/utils/request'
export default {

  // 权益中枢偏离度监控
  equityDeviation: async function (endDate,fundCodes,pageNum,pageSize,startDate,vcTypes,orderBy) {

    return request({
      url: '/api/manageView/equityDeviation/select?endDate=' + endDate +
      '&fundCodes=' + fundCodes +
      '&pageNum=' + pageNum +
      '&pageSize=' + pageSize +
      '&startDate=' + startDate +
      '&vcTypes=' + vcTypes +
      '&orderBy=' + orderBy,
      method: 'post',
    })
  },
  // 权益中枢偏离度监控 导出
  equityDeviationExport: async function (endDate,fundCodes,pageNum,pageSize,startDate,vcTypes,orderBy,name) {

    return request({
      url: '/api/manageView/equityDeviation/select?endDate=' + endDate +
      '&fundCodes=' + fundCodes +
      '&pageNum=' + pageNum +
      '&pageSize=' + pageSize +
      '&startDate=' + startDate +
      '&vcTypes=' + vcTypes +
      '&orderBy=' + orderBy
      + "&ex_tmp_name=" + name,
      method: 'post',
    })
  },

  // 股票池管理
  selectStockManager: async function (fundParam,fundTypes,pageNum,pageSize,stockParam,stockPoolTypes,orderBy) {

    return request({
      url: '/api/manageView/stockAningysis/selectStockManager?' +
      'fundParam=' + fundParam +
      '&fundTypes=' + fundTypes +
      '&pageNum=' + pageNum +
       '&pageSize=' + pageSize +
      '&stockParam=' + stockParam +
      '&stockPoolTypes=' + stockPoolTypes +
      '&orderBy=' + orderBy,
      method: 'post',
    })
  },

  // 股票池管理 导出
  selectStockManagerExport1: async function (fundParam,fundTypes,pageNum,pageSize,stockParam,stockPoolTypes,orderBy,name) {

    return request({
      url: '/api/manageView/stockAningysis/selectStockManager?' +
      'fundParam=' + fundParam +
      '&fundTypes=' + fundTypes +
      '&pageNum=' + pageNum +
       '&pageSize=' + pageSize +
      '&stockParam=' + stockParam +
      '&stockPoolTypes=' + stockPoolTypes +
      '&orderBy=' + orderBy +
      '&ex_tmp_name=' + name,
      method: 'post',
    })
  },


}
