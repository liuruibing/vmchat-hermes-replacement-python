import request from "@/utils/request";
import qs from "qs";
import store from "@/store";
const ContentTypeFormData = { "Content-type": "application/x-www-form-urlencoded" };
export default {
  //字典查询
  getTransferType: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?dimTypecode=" + params,
      method: "get"
    });
  },
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/listPageRemminds" + "?" + qs.stringify(params),
      method: "get"
    });
  },
  // 查询所有 数据源设置
  getDataSourceList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/listPageRemminds" + "?" + qs.stringify(params),
      method: "get"
    });
  },
  //新增
  addDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/insertRemmind" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  //更新
  updateDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/updateRemmind" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  //删除
  deleteDataSource: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/deleteRemmind" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  //删除
  getRemindTypes: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/remind/v1.0/listRemindTypes",
      method: "get"
    });
  },
  // 查询联系人 数据源设置
  getContactList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/contact/v1.0/list" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  // 查询联系人 数据源设置
  getSayList: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/saying/v1.0/list",
      method: "post"
    });
  },
  //  获取服务端的时间
  getTime: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      header: ContentTypeFormData,
      url: "/api/taskcenter/v1.0/getTime",
      data: params,
      method: "post"
    });
  },
  // 获取右侧待办指令
  getOrder: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      header: ContentTypeFormData,
      url: "/api/cmdtask/v1.0/list",
      data: qs.stringify(params),
      method: "post"
    });
  },
  getSubmitOrder: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      header: ContentTypeFormData,
      url: "/api/pfom/v1.0/order",
      method: "get"
    });
  },
  initBackground: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      header: ContentTypeFormData,
      url: "/api/background/v1.0/initBackground?" + qs.stringify(params),
      method: "get"
      // data: qs.stringify(params),
    });
  },
  updateBackground: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      header: ContentTypeFormData,
      url: "/api/background/v1.0/updateBackground",
      method: "post",
      data: qs.stringify(params)
    });
  }
};
