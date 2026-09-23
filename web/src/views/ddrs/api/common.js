import request, { excelGet, excelPost } from "@/utils/request";
import qs from "qs";
import Vue from "vue";
import store from "@/store";
function getFileNameFromResponseHeader(response) {
  const contentDisposition = response.headers["content-disposition"];
  const fileNameMatch = contentDisposition && contentDisposition.match(/fileName=(.+)$/);
  if (fileNameMatch && fileNameMatch[1]) {
    const encodedFileName = fileNameMatch[1];
    const decodedFileName = decodeURIComponent(encodedFileName);
    return decodedFileName;
  }
  debugger;
  // If the file name could not be extracted from the response header, provide a default name.
  return null;
}

export default {
  // 字典查询
  edimsCommon: async function(dimType) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/common/edimsCommon/listEdims/" + dimType,
      method: "get"
    });
  },
  // 根据编码查询 用来做说明
  edimsCommonHint: async function(dimCode, dimType) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/common/edimsCommon/listEdims/" + dimType + "/" + dimCode,
      method: "get"
    });
  },
  // 字典查询
  getTransferType: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edims/v1.0/listEdims.do?dimType=" + params,
      method: "get"
    });
  },
  getProductsAll: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/fund/v1.0/getProductsAll",
      method: "get"
    });
  },
  // 查询基金经理信息
  getFundManagerInfo: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/foundManager/v1.0/getManagerAll",
      method: "get"
    });
    // return request.get('/api/foundManager/v1.0/getManagerAll')
  },
  // 查询机构信息
  getDeptInfoSel: async function() {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/deptInfo/v1.0/deptInfoSel",
      method: "post"
    });
    // return request.post('/api/deptInfo/v1.0/deptInfoSel')
  },
  // 字典查询
  getEdims: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?dimTypecode=" + params,
      method: "get"
    });
  },
  getEdims2: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimsGet?" + qs.stringify(params),
      method: "get"
    });
  },
  // 查询fileList
  getFileList: async function(relaId, relaType) {
    // return request.get('/api/file/v1.0/filesGet?relaId=' + relaId + '&relaType=' + relaType)
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/file/v1.0/filesGet?relaId=" + relaId + "&relaType=" + relaType,
      method: "get"
    });
  },
  // 查询fileList
  delFileList: async function(id) {
    // return request.get('/api/file/v1.0/delFile?id=' + id)
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/file/v1.0/delFile?id=" + id,
      method: "get"
    });
  },
  // 获取连接状态
  getConStatus: async function() {
    // return request.post('/api/transfer/v1.0/connectToGtja')
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/transfer/v1.0/connectToGtja",
      method: "POST"
    });
  },
  // 获取bpmn流程图
  get_processdefine_xml: async function(bpmnId) {
    // return request.get('/api/process/v1.0/processdefine/xml/' + bpmnId)
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/process/v1.0/processdefine/xml/" + bpmnId,
      method: "get"
    });
  },
  // 获取bpmn流程图
  getHandleHtml: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/processpoint/v1.0/info" + "?" + qs.stringify(params),
      method: "get"
    });
  },
  // 获取bpmn流程图
  saveHandleHtml: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/processpoint/v1.0/saveOrModify.do",
      method: "post",
      data: qs.stringify(params)
    });
  },
  // 预览文件
  downloadFile: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/file/v1.0/downloadFile" + "?" + qs.stringify(params),
      method: "get"
    });
  },
  // 预览文件 previewFile
  previewFile: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/file/v1.0/previewFile" + "?" + qs.stringify(params),
      method: "get"
    });
  },

  // 获取字典分类编码
  getEdimTypeList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimTypeList?" + qs.stringify(params),
      method: "get"
    });
  },
  // 根据对应分类编码，获取字典数组
  getEdimList: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/edimExt/v1.0/edimList?" + qs.stringify(params),
      method: "get"
    });
  },
  getaaaa: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/template/v1.0/downloadByType?id=f3154059-bf66-4d98-96ec-427fd3b67257",
      method: "get"
    });
  },
  // 多附件打包zip下载 传参 ids--附件id数组 fileName--下载的文件名
  batchDownload: async function(params) {
    return request({
      baseURL: store.state.setting.baseApi, // api 的 base_url
      url: "/api/file/v1.0/batchDownload",
      method: "get"
    });
  },

  // 导出
  downLoadFileByUrlPost(url, params, fileName, callback = () => {}) {
    excelPost(url, params, { "Content-Type": "application/json;charset=UTF-8" })
      .then((res) => {
        if (typeof callback === "function") {
          callback();
        }
        fileName = getFileNameFromResponseHeader(res);
        console.log("fileName--------------------", fileName);
        const blob = new Blob([res.data]);
        if (fileName == null) {
          // 取不到fileName说明有错误，把BLOB流转成JSON对象
          const reader = new FileReader();
          reader.onload = function(event) {
            try {
              // 读取完成后，解析为JSON对象
              const jsonData = JSON.parse(event.target.result);
              // 取不到fileName 有错误，提示
              if (jsonData.message) {
                Vue.prototype.$message.closeAll();
                Vue.prototype.$message.warning(jsonData.message);
              } else {
                Vue.prototype.$message.closeAll();
                Vue.prototype.$message.warning("导出失败");
              }
            } catch (e) {
              Vue.prototype.$message.closeAll();
              Vue.prototype.$message.warning("导出失败");
            }
          };
          reader.readAsText(blob);
        } else {
          const fileUrl = window.URL.createObjectURL(blob);
          const link = document.createElement("a");
          link.href = fileUrl;

          link.download = fileName;
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
        }
      })
      .catch((err) => {
        if (typeof callback === "function") {
          callback();
        }
      });
  }
};
