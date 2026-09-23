import request from '@/utils/request'
import qs from 'qs'
export default {
  assetTimeEchartRatioData: async function (params) {
    return request.post('/api/gfhomepage/assetTimeEchartRatioData',params)
  },
  assetTimeEchartHldData: async function (params) {
    return request.post('/api/gfhomepage/assetTimeEchartHldData',params)
  },
}