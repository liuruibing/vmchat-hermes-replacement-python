import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData2 = { 'Content-Type': 'application/json' }
const formIs = { 'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
export default {
  // 根据sql配置的vc_code配置sql查询
  getDataBysqlCode: async function(param) {
    return request({
      headers: ContentTypeFormData2,
      url: '/api/report/v1.0/data/sql/' + param.indexCode,
      data: param,
      method: 'post'
    })
  },

  // 字典查询 ME_DIM 表 返回map 对象
  edimsDdiaCommon: async function(dimType) {
    return request({
      url: '/api/common/edimDdiaCommon/listEdims/' + dimType,
      method: 'get'
    })
  },
  // 字典查询 ME_DIM 表 返回Medim 对象
  edimsSelectType: async function(dimType) {
    return request({
      url: '/api/common/edim/' + dimType,
      method: 'get'
    })
  },

  // 字典查询  e_dim_portal 表
  edimsCommon: async function(dimType) {
    return request({
      url: '/api/common/edimsCommon/listEdims/' + dimType,
      method: 'get'
    })
  },

  // 根据编码查询 用来做说明
  edimsCommonHint: async function(dimCode, dimType) {
    return request({
      url: '/api/common/edimsCommon/listEdims/' + dimType + '/' + dimCode,
      method: 'get'
    })
  },
  //字典查询
  getTransferType: async function(params) {
    return request({
      url: '/api/edims/v1.0/listEdims.do?dimType=' + params,
      method: 'get'
    })
  },
  getProductsAll: async function() {
    return request({
      url: '/api/fund/v1.0/getProductsAll',
      method: 'get'
    })
  },
  // 查询基金经理信息
  getFundManagerInfo: async function() {
    return request.get('/api/foundManager/v1.0/getManagerAll')
  },
  // 查询机构信息
  getDeptInfoSel: async function() {
    return request.post('/api/deptInfo/v1.0/deptInfoSel')
  },
  //字典查询
  getEdims: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get'
    })
  },
  getEdims2: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 查找用户部门
  fun_getUserDept: async function () {
    return request({
      url: '/api/common/deptCommon/userDept',
      method: 'get',
    })
  },
  // 获取机构信息 sys_dept中级别为1的
  fun_getCompanyIdArrs: async function () {
    return request({
      url: '/api/common/deptCommon/getFundMechanismInfo',
      method: 'get',
    })
  },
  //查询fileList
  getFileList: async function(relaId, relaType) {
    return request.get('/api/file/v1.0/filesGet?relaId=' + relaId + '&relaType=' + relaType)
  },
  //查询fileList
  delFileList: async function(id) {
    return request.get('/api/file/v1.0/delFile?id=' + id)
  },
  //获取连接状态
  getConStatus: async function() {
    return request.post('/api/transfer/v1.0/connectToGtja')
  },
  // 获取bpmn流程图
  get_processdefine_xml: async function(bpmnId) {
    return request.get('/api/process/v1.0/processdefine/xml/' + bpmnId)
  },
  // 获取bpmn流程图
  getHandleHtml: async function(params) {
    return request({
      url: '/api/processpoint/v1.0/info' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 获取bpmn流程图
  saveHandleHtml: async function(params) {
    return request({
      url: '/api/processpoint/v1.0/saveOrModify.do',
      method: 'post',
      data: qs.stringify(params)
    })
  },
  // 预览文件
  downloadFile: async function(params) {
    return request({
      url: '/api/file/v1.0/downloadFile' + '?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 预览文件 previewFile
  previewFile: async function(params) {
    return request({
      url: '/api/file/v1.0/previewFile' + '?' + qs.stringify(params),
      method: 'get'
    })
  },

  // 获取字典分类编码
  getEdimTypeList: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimTypeList?' + qs.stringify(params),
      method: 'get'
    })
  },
  // 根据对应分类编码，获取字典数组
  getEdimList: async function(params) {
    return request({
      url: '/api/edimExt/v1.0/edimList?' + qs.stringify(params),
      method: 'get'
    })
  },
  getaaaa: async function(params) {
    return request({
      url: '/api/template/v1.0/downloadByType?id=f3154059-bf66-4d98-96ec-427fd3b67257',
      method: 'get'
    })
  },
  // 根据templateCode获取只需要展示的指标
  selectIndexInfos: async function(param) {
    return request({
      headers: ContentTypeFormData2,
      url: '/api/template/selectIndexInfos',
      data: param,
      method: 'post'
    })
  },
  // 多附件打包zip下载 传参 ids--附件id数组 fileName--下载的文件名
  batchDownload: async function(params) {
    return request({
      url: '/api/file/v1.0/batchDownload',
      method: 'get'
    })
  },
  manageUpload: async function(params) {
    return request({
      url: '/api/article/manage/upload',
      headers: formIs,
      method: 'post',
      data: params
    })
  },
  manageS3SelectFile:async function(S3FileUUID) {
    return request({
      url: '/api/s3client/selectS3File/'+S3FileUUID,
      method: 'get',
      responseType:'blob'
    })
  },
  manageS3SelectFileVueBlob:async function(S3FileUUID) {
    try {
      const resData =  await this.manageS3SelectFile(S3FileUUID);
      const blob = new Blob([resData.data], { type: 'application/octet-stream' });
      return URL.createObjectURL(blob);
    } catch (error) {
      console.error('加载失败:', error);
      return ''
    }
  },

}
