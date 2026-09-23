/* 应急预案接口 */
import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};
export  default {

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
  sendBiz: async function (params) {
    // console.log(params)
    // let data = params.getAll('file')
    // let dat2a = params.getAll('datastr')
    // console.log(data)
    // console.log(dat2a)
    // return request.post('/api/process/v1.0/processInstance/'+id,params)
    return request({
      headers: ContentTypeFormData,
      url: '/api/emergency/v1.0/startEmergency',
      data: params,
      method: 'post',
    })
  },
  selectALLInfoUrl:async function (orderByString,pageSize,offset,procStatusArr,cmdType,source) {
    let url = '/api/emergency/v1.0/transFlowGet?limit=' + pageSize +"&offset="  +offset;
    if(orderByString != "0"){
      url = url  +"&orderString="+orderByString;
    }
    // if(procStatusArr.length !== 0){
    //   url = url  +"&procStatusArr="+procStatusArr;
    // }

    if(cmdType != "0"){
      url = url  +"&cmdType="+cmdType;
    }
    if(source != "0"){
      url = url  +"&source="+source;
    }
    return request.get(url)
  },
  taskList:async function (orderByString,pageSize,offset,procStatusArr,cmdType,source) {
    let url = '/api/emergency/v1.0/taskList?limit=' + pageSize +"&offset="  +offset;
    if(orderByString != "0"){
      url = url  +"&orderString="+orderByString;
    }
    // if(procStatusArr.length !== 0){
    //   url = url  +"&procStatusArr="+procStatusArr;
    // }

    if(cmdType != "0"){
      url = url  +"&cmdType="+cmdType;
    }
    if(source != "0"){
      url = url  +"&source="+source;
    }
    return request.get(url)
  },
  dealtList:async function (orderByString,pageSize,offset,procStatusArr,cmdType,source) {
    let url = '/api/emergency/v1.0/dealtList?limit=' + pageSize +"&offset="  +offset;
    if(orderByString != "0"){
      url = url  +"&orderString="+orderByString;
    }
    // if(procStatusArr.length !== 0){
    //   url = url  +"&procStatusArr="+procStatusArr;
    // }

    if(cmdType != "0"){
      url = url  +"&cmdType="+cmdType;
    }
    if(source != "0"){
      url = url  +"&source="+source;
    }
    return request.get(url)
  },
  getInitTransFlow: async function () {
    return request.get('/api/emergency/v1.0/initTransFlow')
  },
  getDetail:async function (taskId) {
    return request.get('/api/process/v1.0/processInstance/task/'+taskId)
  },
  //修改跟踪代办状态
  updateStatus: async function (taskId,params) {
    return request.post('/api/process/v1.0/processdefine/'+taskId, params)
  },
  getRelation:async function (conductId,relationType) {
    return request.get('/api/emergency/v1.0/getConductRelations?conductId='+conductId+'&relationType='+relationType)
  },
  getFileList:async function (relaId,relaType) {
    return request.get("/api/file/v1.0/filesGet?relaId="+relaId+"&relaType="+relaType)
  },
  deleteFile:async function (id) {
    return request.post("/api/system/v1.0/file/deleteById?id="+id)
  },
  getDetails:async function (procInstId,xmlId) {
    return request.get('/api/emergency/v1.0/'+procInstId+'/'+xmlId+'/getParallelTask')
  },
  getTemplates:async function () {
    return request.get('/api/emergency/v1.0/listConfigs')
  }

}

