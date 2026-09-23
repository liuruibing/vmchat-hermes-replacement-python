import request from '@/utils/request'

const selectAssigner = () => {
  return request({
    url: '/api/standArd/needManage/selectAssigner',
    method: 'POST'
  })
}

const updateAssigner = data => {
  return request({
    url: '/api/standArd/needManage/updateAssigner',
    method: 'POST',
    data
  })
}

export default {
  selectAssigner,
  updateAssigner
}
