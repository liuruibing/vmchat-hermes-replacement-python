import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-type' : 'application/x-www-form-urlencoded'}

export default{
  // 准入池查询产品
  selectFund:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fundAccess/approve/selectFund',
      method: 'post',
      data: params
    })
  },



  // 标准化-查询产品
  needManageSelect:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/standArd/needManage/select',
      method: 'post',
      data: params
    })
  },
  // 标准化-申请上传文件
  needManageInsertUpload: async function (params) {
    return request({
      contentType: false,//这里不要落下
      dataType: 'json',
      url: '/api/standArd/needManage/insertUpload',
      data: params,
      method: 'post',
    })
  },
  // 标准化-提交
  needManageSubmit:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/standArd/needManage/submit',
      method: 'post',
      data: params
    })
  },
  //标准化-编辑-通过列表id 查询文件id和文件名
  needManageSelectEdit:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/standArd/needManage/selectEdit',
      method: 'post',
      data: params
    })
  },
  // 标准化-编辑/上传文件
   needManageUpdateUpload: async function (params) {
    return request({
      contentType: false,//这里不要落下
      dataType: 'json',
      url: '/api/standArd/needManage/updateUpload',
      data: params,
      method: 'post',
    })
  },
  // 标准化-删除产品
  needManageDeleteFund:async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/standArd/needManage/deleteFund',
      method: 'post',
      data: params
    })
  },
}