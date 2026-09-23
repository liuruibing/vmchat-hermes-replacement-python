import request from '@/utils/request'
import qs from 'qs'
export  default {
   
  // 查询列表
  warnRuleManageList: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/list',
      method: 'post',
      data: params,
    })
  },
  // 指标列表
  itemList: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/itemList',
      method: 'post',
      data: params,
    })
  },
  // 机构列表
  companyList: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/companyList',
      method: 'post',
      data: params,
    })
  },
  // 新增
  insert: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/insert',
      method: 'post',
      data: params,
    })
  },
  // 编辑
  update: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/update',
      method: 'post',
      data: params,
    })
  },
  // 删除/批量删除
  delete: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/delete',
      method: 'post',
      data: params,
    })
  },
  // 批量停止
  updateDisableStatus: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/updateDisableStatus',
      method: 'post',
      data: params,
    })
  },
  // 适用产品/机构-更新确认
  objSettings: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/objSettings',
      method: 'post',
      data: params,
    })
  },
  // 适用产品/机构-弹框
  objList: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/objList',
      method: 'post',
      data: params,
    })
  },
  // 邮箱设置-更新确认
  emailSettings: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/emailSettings',
      method: 'post',
      data: params,
    })
  },
  // 邮箱设置-弹框
  emailList: async function (params) {
    return request({
      url: '/api/afterManage/warnRuleManage/emailList',
      method: 'post',
      data: params,
    })
  },


}