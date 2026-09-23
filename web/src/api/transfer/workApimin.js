import request from '@/utils/request'
export default{

// 创建流程定义
  post_processdefine: async function (appkey,deployName) {
    var url = "/api/process/v1.0/processdefine/file?appKey="+appkey+"&deployName="+deployName;
    return request({
      url: url,
      method: 'post',
    })
  },

// 获取流程定义
  get_processdefine: async function (appkey) {
    return request({
      url: '/api/process/v1.0/processdefine/'+appkey,
      method: 'get',
    })
    
  },
  // 获取流程定义任务显示节点对象
  get_processdefine_taskIndex: async function (appkey) {
    return request({
      url: "/api/process/v1.0/processdefine/"+appkey+"/taskIndex?isGtja=1",
      method: 'get',
    })
   
  },
  // 获取bpmn流程图
  get_processdefine_xml: async function (bpmnId) {
    return request({
      url: "/api/process/v1.0/processdefine/xml/"+bpmnId,
      method: 'get',
    })
   
  }

  
}
