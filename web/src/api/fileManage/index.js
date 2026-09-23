import request from '@/utils/request'
import qs from 'qs'
export  default {
  
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/file/v1.0/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  //删除
  deleteDataSource: async function (params) {
    return request({
      url: '/api/file/v1.0/delFile' + '?' + qs.stringify(params),
      method: 'get',
    })
  }


}