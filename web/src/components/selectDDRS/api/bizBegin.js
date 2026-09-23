/* 转账指令流程发起接口 */
import request from "@/utils/request";
import store from "@/store";
import qs from "qs";
const url = "/api/process/v1.0/processInstance/";
const ContentTypeFormData = { "Content-Type": "application/x-www-form-urlencoded" };
export default {
  getProductFund: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/fund/v1.0/getProductsAll",
      method: "get"
    });
    // return request.get('/api/fund/v1.0/getProductsAll')
  },
  // 查询产品信息
  getProductInfo: async function() {
    // return request.get('/api/product/v1.0/getProductsAll')
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/product/v1.0/getProductsAll",
      method: "get"
    });
  },
  // 查询经纪商
  getBrokerInfo: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?dimTypecode=" + params,
      method: "get"
    });
  },
  // 查询转账类型
  getTransferType: async function() {
    // return request.get('/api/transfer/bizBegin/getProductInfo')
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/transfer/bizBegin/getProductInfo",
      method: "get"
    });
  },
  // 获取defineId
  getDefineId: async function(key) {
    // return request.get(url + key)
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: url + key,
      method: "get"
    });
  },
  // 提交流程
  sendBiz: async function(id, params) {
    // return request.post(url + id, params)
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: url + id,
      method: "post",
      params: params
    });
  },
  // 转账类型
  getTransferType: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?dimTypecode=" + params,
      method: "get"
    });
  },
  // 转账类型-二级
  getAccountTypes: async function(dimTypecode, parentId) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?dimTypecode=" + dimTypecode + "&parentId=" + parentId,
      method: "get"
    });
  },
  getInitTransFlow: async function() {
    // return request.get('/api/transFlow/v1.0/initTransFlow')
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/transFlow/v1.0/initTransFlow",
      method: "get"
    });
  },
  // 转账流程发起
  startTransfer: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/transfer/v1.0/startTransfer",
      method: "post",
      contentType: false, // 这里不要落下
      dataType: "json",
      data: qs.stringify(params)
    });
  },
  // 查询期货账户
  getQhAccount: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/trade/future/findAll.do" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  // 查询证券账户
  getZqAccount: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/trade/stock/findAll.do" + "?" + qs.stringify(params),
      method: "post"
    });
  },
  // 根据产品名称选择经济商
  getZqAccountSELECT: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      headers: ContentTypeFormData,
      url: "/api/trade/stock/findAll.do",
      data: qs.stringify(params),
      method: "post"
    });
  },
  // 根据产品名称选择经济商--银行间
  getZqAccountSELECTYH: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      headers: ContentTypeFormData,
      url: "/api/trade/future/findAll.do",
      data: qs.stringify(params),
      method: "post"
    });
  },
  // 流转岗位的分组数据
  getFZAccount: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      headers: ContentTypeFormData,
      url: "/api/position/listTree",
      data: params,
      method: "post"
    });
  },
  //
  getpmList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      // headers: ContentTypeFormData,
      url: "/api/pm/v1.0/list?" + qs.stringify(params),
      // data: qs.stringify(params),
      method: "get"
    });
  }
};
