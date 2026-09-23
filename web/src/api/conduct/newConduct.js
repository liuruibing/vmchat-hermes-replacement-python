/* 综合办理接口 */
import request from '@/utils/request'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
import qs from 'qs'
export  default {

  //  获取业务类型
  getBusinessType: async function () {
    return request({
      url: '/api/newConduct/v1.0/getBusinessType',
      method: 'get',
    })
  },
  //  获取业务场景
  getBusinessNames: async function (params) {
    return request({
      url: '/api/newConduct/v1.0/getBusinessNames?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 待办查询
  selectALLInfoUrl:async function (params) {
    return request({
      url: '/api/newConduct/v1.0/taskList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 已办查询
  dealtList:async function (params) {
    return request({
      url: '/api/newConduct/v1.0/dealtList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 流程发起提交
  addNewList: async function (params) {
    return request({
      contentType: false,//这里不要落下
      dataType: 'json',
      url: '/api/newConduct/v1.0/startConduct',
      data: params,
      method: 'post',
    })
  },


  // tape步骤信息
  getStapeInfo: async function (params) {
    return request({
      url: '/api/process/v1.0/processInstance/' + params + '/taskIndex',
      method: 'get',
    })
  },
  
  // 修改的file文件上传
  senChangeFileUrl: async function (params) {
    return request({
      contentType: false,//这里不要落下
      dataType: 'json',
      url: '/api/newConduct/v1.0/updateConduct',
      data: params,
      method: 'post',
    })
  },
  //查询产品信息
  getProductInfo: async function () {
    return request.get('/api/product/v1.0/getProductsAll')
  },
  //字典查询
  getTransferType: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  },
  //获取defineId
  getDefineId: async function (key) {
    return request.get("/api/process/v1.0/processInstance/"+key)
  },
  //提交流程
  sendBiz: async function (id,params) {
    return request.post('/api/process/v1.0/processInstance/'+id,params)
  },
  selectALL:async function (params) {
    return request({
      url: '/api/newConduct/v1.0/transFlowGet?' + qs.stringify(params),
      method: 'get',
    })
  },
  
  getInitTransFlow: async function () {
    return request.get('/api/newConduct/v1.0/initTransFlow')
  },
  getDetail:async function (taskId) {
    return request.get('/api/process/v1.0/processInstance/task/'+taskId)
  },
  //修改跟踪代办状态
  updateStatus: async function (taskId,params) {
    return request.post('/api/process/v1.0/processdefine/'+taskId, params)
  },
  getRelation:async function (conductId,relationType) {
    return request.get('/api/newConduct/v1.0/getConductRelations?conductId='+conductId+'&relationType='+relationType)
  },
  getFileList:async function (relaId,relaType) {
    return request.get("/api/file/v1.0/filesGet?relaId="+relaId+"&relaType="+relaType)
  },
  deleteFile:async function (id) {
    return request.post("/api/system/v1.0/file/deleteById?id="+id)
  },
  getDetails:async function (procInstId,xmlId) {
    return request.get('/api/newConduct/v1.0/'+procInstId+'/'+xmlId+'/getParallelTask')
  },
  // 获取当前step的信息
  getUsrINfo:async function (data) {
    return request.get('/api/taskuser/v1.0/list?procInstId='+data.procInstId+'&taskXmlId='+data.taskXmlId)
  }
}

