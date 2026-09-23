import request from '@/utils/request'

const qs = require('qs');
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
const ContentTypeJson = {'Content-Type': 'application/json'};
export default {

  // 查询所有 数据源设置
  getDataSourceList: async function (params) {
    return request({
      url: '/api/user/users' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
  getDeptSourceList: async function () {
    return request({
      url: '/api/dept/depts',
      method: 'get',
    })
  },

  getDeptSourceListByAdd: async function (params) {
    return request({
      url: '/api/company/v1.0/listDept',
      method: 'POST',
      data: params
    })
  },
//新增用户
  addDataSource: async function (params) {
    return request({
      url: '/api/user/users',
      method: 'post',
      data: params
    })
  },
//检查账户是否可用
  checkAccount: async function (params) {
    return request({
      url: '/api/user/checkAccount' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
//检查员工编号是否可用
  checkUserNo: async function (params) {
    return request({
      url: '/api/user/checkUserNo' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
//获取字典数据
  getEdims: async function (dimType) {
    return request({
      url: '/api/common/edimsCommon/listEdims/' + dimType,
      method: 'get',
    })
  },
//获取机构数据
  getCompanys: async function () {
    return request({
      url: '/api/dept/companys',
      method: 'get',
    })
  },
//获取角色数据
  getRoles: async function () {
    return request({
      url: '/api/role/dialogRoles',
      method: 'get',
    })
  },
//获取用户详情信息
  getEditDetail: async function (params) {
    return request({
      url: '/api/user/getEditDetail' + '?' + qs.stringify(params),
      method: 'get',
    })
  },
//启用
  updateEnableStatus: async function (params) {
    return request({
      url: '/api/user/userAble',
      method: 'post',
      data: params
    })
  },
//禁用
  updateDisableStatus: async function (params) {
    return request({
      url: '/api/user/userDisable',
      method: 'post',
      data: params
    })
  },
//修改用户信息
  updateDataSource: async function (params) {
    return request({
      url: '/api/user/usersNew',
      method: 'post',
      data: params
    })
  },
//重置密码
  resetPwd: async function (params) {
    return request({
      url: '/api/user/resetPwd' + '?' + qs.stringify(params),
      method: 'post',
    })
  },
// 获取密码策略设置信息
  getPwdStrategy: async function () {
    return request({
      url: '/api/system/passwordPolicy/getPwdStrategy',
      method: 'get',
    })
  },
// 密码策略信息提交
  postPwdStrategy: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/system/passwordPolicy/updatePwdStrategy',
      method: 'post',
      data: qs.stringify(params)
    })
  },
// 密码验证
  checkPassword: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/system/passwordPolicy/checkPassword',
      method: 'post',
      data: qs.stringify(params)
    })
  },
// 获取锁定用户
  getLockingUser: async function (params) {
    return request({
      // url: '/api/system/passwordPolicy/lockingUser?' + qs.stringify(params),
      url: '/api/userlock/v1.0/list?' + qs.stringify(params),
      method: 'get',
    })
  },
// 解锁用户
  postManualUnlock: async function (params) {
    return request({
      headers: ContentTypeJson,
      // url: '/api/system/passwordPolicy/manualUnlock',
      url: '/api/userlock/v1.0/unlock',
      method: 'post',
      data: params
    })
  }


}
