import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-type' : 'application/x-www-form-urlencoded'}

export default{

  // 查询获取列表
  cmdnotice_list:async function ( params ) {
    return request({
      // header: ContentTypeFormData,
      url: '/api/cmdnotice/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
      // data: params 
    })
  },
  // 指令通知规则-新增
  cmdnotice_add:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/cmdnotice/v1.0/add',
      method: 'post',
      data: qs.stringify(params) 
    })
  },
  // 指令通知规则-编辑  需传配置id - noticeId
  cmdnotice_info:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/cmdnotice/v1.0/info',
      method: 'post',
      data: qs.stringify(params) 
    })
  },
  // 启用、禁用按钮，使用编辑接口，noticeStatus 1启用0禁用


  // ------------------------------


}