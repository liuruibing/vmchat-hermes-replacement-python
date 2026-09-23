import request from '../../utils/request'
const ContentTypeFormData = { 'Content-Type': 'application/x-www-form-urlencoded' };
const qs = require('qs');
// const base_url = 'http://192.168.10.135:8090/pfom'
export default {

  // 查询 
  attrmatchList: async function (params) {
    return request({
      url: '/api/zhsuperviseref/v1.0/doSuperviseRefList.do' + '?' + qs.stringify(params),
      method: 'get',
      // data:qs.stringify(params)
    })
  },


  // 新增
  addList: async function (params) {
    return request({
      url: '/api/zhsuperviseref/v1.0/doSuperviseRefAdd.do',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // 修改
  updateTaskSet: async function (params) {
    return request({
      url: '/api/zhsuperviseref/v1.0/doSuperviseRefEdit.do',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  
  // 删除
  deleteCode: async function (params) {
    return request({
      url: '/api/zhsuperviseref/v1.0/deleteSuperviseRef.do',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // "基金与机构关系维护_新增_关系获取"
  selectOrgantype: async function (params) {
    return request({
      url: '/api/zhsuperviseref/v1.0/selectOrgantype.do',
      method: 'get',
    })
  },

  // 获取基金列表
  selectProductAll: async function (params) {
    return request({
      url: '/api/ann/v1.0/zhfund/list' + '?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 获取机构列表
  doTxtOrgList: async function (params) {
    return request({
      url: '/api/ann/v1.0/zhtxtorg/doTxtOrgList.do',
      method: 'post',
      data:qs.stringify(params)
    })
  },

  // 导出数据
  doSuperviseRefDownload: async function (params) {
    return request({
      headers:ContentTypeFormData,
      url: '/api/zhsuperviseref/v1.0/doSuperviseRefDownload.do',
      method: 'post',
      data:qs.stringify(params)
    })
  },

}
