import request from '@/utils/request'

const selectPayRate = data => {
  return request({
    url: '/api/warehouse/selectPayRate',
    method: 'POST',
    data
  })
}

const updatePayRate = data => {
  return request({
    url: '/api/warehouse/updatePayRate',
    method: 'POST',
    data
  })
}

export default {
  selectPayRate,
  updatePayRate
}
