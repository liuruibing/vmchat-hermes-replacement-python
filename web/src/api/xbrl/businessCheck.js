import request from '@/utils/request'
import qs from 'qs'
export  default {
   //字典查询
   getTransferType: async function (params) {
    return request({
      url: '/api/edims/v1.0/listEdims.do?dimType=' + params,
      method: 'get',
    })
  },
  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/businessCheck/v1.0/list' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },

  // 规则-查询
  getIndParaThemeList: async function (params) {
    return request({
      url: '/api/warnConfig/v1.0/doWarnSpecialList.do' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  //规则-编辑、新增
  postIndParaThemeEdit: async function (params) {
    return request({
      url: '/api/warnConfig/v1.0/addWarnSpecial.do' + '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  //添加规则到
  addData: async function (ids) {
    return request({
      url: '/api/businessCheck/v1.0/insert?ids='+ids,
      method: 'POST',
    })
  },
  //删除校验配置
  deleteDataSource: async function (params) {
    return request({
      url: '/api/businessCheck/v1.0/delete'+ '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  //执行顺序
  updateDataSource: async function (params) {
    return request({
      url: '/api/businessCheck/v1.0/update'+ '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  //修改状态
  updateStatus: async function (params) {
    return request({
      url: '/api/businessCheck/v1.0/updateStatus'+ '?' + qs.stringify(params),
      method: 'POST',
    })
  },
  getDaLei: async function() {
    return request({
        url: '/api/warnConfig/v1.0/getCheckDaLeiList',
        method: 'post',
    })
},
getDataSourceList2: async function() {
  return request({
      url: '/api/warnConfig/v1.0/getDataSourceList',
      method: 'post',
  })
}
  

}