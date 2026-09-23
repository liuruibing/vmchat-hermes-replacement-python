import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-Type': 'application/x-www-form-urlencoded'};

export default {
  // 新增
  creatRow: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/indexManager/v1.0/insert',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  // 获取列表
  getTabableList: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/indexManager/v1.0/list',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  // 删除
  handelDeleteList: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/indexManager/v1.0/delete',
      data: qs.stringify(params),
      method: 'post',
    })
  },
  // 更新
  handelUpdata: async function (params) {
    return request({
      headers: ContentTypeFormData,
      url: '/api/indexManager/v1.0/update',
      data: qs.stringify(params),
      method: 'post',
    })
  }
}