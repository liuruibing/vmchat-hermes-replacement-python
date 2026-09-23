import request from '@/utils/request'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const qs = require('qs');
export default {

  //查询组合
  combineSelect: async function (data) {
    return request({
      url: '/api/simulate/combine/select',
      method: 'post',
      data: data
    })
  },
  //新增/编辑组合
  combineSave: async function (data) {
    return request({
      url: '/api/simulate/combine/save',
      method: 'post',
      data: data
    })
  },
  //模拟组合-导出
  combineExport: async function (data) {
    return request({
      url: '/api/simulate/combine/export',
      method: 'post',
      data: data
    })
  },
  //删除组合
  combineDelete: async function (data) {
    return request({
      url: '/api/simulate/combine/delete',
      method: 'post',
      data: data
    })
  },

  //图形模式：查询组合的净值走势
  combineSelectNetWorth: async function (data) {
    return request({
      url: '/api/simulate/combine/selectNetWorth',
      method: 'post',
      data: data
    })
  },
}
