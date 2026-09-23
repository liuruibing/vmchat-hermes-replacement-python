import request from "@/utils/request";
import qs from "qs";
import store from "@/store";
export default {
  //字典查询
  getTabData: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/tabInfo",
      method: "post",
      data: params
    });
  },

  getTabData2: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/newReportShow/v1.0/tabInfo",
      method: "post",
      data: params
    });
  },

  // 查询所有 数据源设置
  getDataTableNameList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/tabData",
      method: "post",
      data: params
    });
  },

  getDataTableNameList2: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/newReportShow/v1.0/tabData",
      method: "post",
      data: params
    });
  },
  // 查询所有 数据源设置
  addDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/add",
      method: "post",
      data: params
    });
  },
  // 查询所有 数据源设置
  updateDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/update",
      method: "post",
      data: params
    });
  },
  // 删除
  deleteDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/delete",
      method: "post",
      data: params
    });
  },
  // 批量删除
  deleteBatch: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/deleteBatch",
      method: "post",
      data: params
    });
  },
  // 查询所有 数据源设置
  getSelectData: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/selectOptions",
      method: "post",
      data: params
    });
  },

  // 配置页面-编辑
  editOnPage: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/editOnPage",
      method: "post",
      data: params
    });
  },
  // 配置页面-导出
  exportExcel: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/exportExcel",
      method: "post",
      data: params
    });
  },
  // 配置页面-定期报告记录-文本编辑
  editOnPageTxt: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/reportShow/v1.0/editOnPageTxt",
      method: "post",
      data: params
    });
  }
};
