import request from "@/utils/request";

import qs from "qs";

const ContentTypeFormData = {
  "Content-Type": "application/x-www-form-urlencoded",
};
export default {
  // 获取导出报告code列表
  getTemplateCodeList: async function (params) {
    return request({
      url: "/api/report/template/v1.0/page",
      method: "POST",
      data: params,
    });
  },

  // 查询表格数据
  getSelectTableData: async function (params) {
    return request({
      url: "/api/reportQuickConfig/v1.0/page",
      method: "POST",
      data: params,
      params: params,
    });
  },

  // 查询所有 数据源设置
  execSQL: async function (params) {
    return request({
      url: "/api/reportQuickConfig/v1.0/execSQL",
      header: ContentTypeFormData,
      method: "post",
      data: params,
    });
  },

  edimTypeList: async function () {
    return request({
      // url: '/api/edim/v1.0/listEdimConf?&pageNum=1&pageSize=999999',
      url: "/api/reportQuickConfig/v1.0/listEdims",
      method: "GET",
    });
  },

  // 获取菜单数据 findTree
  getMenu: async function (params) {
    return request({
      // url: '/api/reportConfig/v1.0/findTree',
      // url: '/api/reportQuickConfig/v1.0/menuTree',
      url: "/api/system/v1.0/getMenuAll",
      method: "get",
    });
  },

  buildConfig: async function (params) {
    return request({
      url: "/api/reportQuickConfig/v1.0/buildConfig",
      method: "post",
      data: params,
    });
  },

  // 字典SQL测试 checkDicSql
  checkDicSql: async function (params) {
    return request({
      url: "/api/reportConfig/v1.0/checkDicSql",
      method: "post",
      data: qs.stringify(params),
    });
  },

  // 获取所有的版本信息
  getVersionList: async function (params) {
    return request({
      url: "/api/reportQuickConfig/v1.0/versionList",
      method: "post",
      data: params,
      params: params,
    });
  },

  // 报告配置-删除配置版本
  deleteVersion: async function (params) {
    return request({
      url: "/api/reportQuickConfig/v1.0/deleteVersion",
      method: "post",
      data: params,
      params: params,
    });
  },
};
