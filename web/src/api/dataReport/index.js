/* 应急预案接口 */
import request from '@/utils/request'
import qs from 'qs'
export  default {

 
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/generalquery/v1.0/getQueryResult.do' + '?' + qs.stringify(params),
      method: 'get',
    })
  }

}

