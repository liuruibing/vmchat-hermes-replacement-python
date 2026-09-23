import request from '@/utils/request'
import qs from 'qs'
export default {
  //收益率
  doPerformanceFundYieldList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceFundYieldList', params)
  },
  //年化波动率
  doPerformanceYearVolatilityList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceYearVolatilityList', params)
  },
  //α系数
  doPerformanceAlphaList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceAlphaList', params)
  },
  //β系数
  doPerformanceBetaList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceBetaList', params)
  },
  //Sharpe指数
  doPerformanceSharpeList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceSharpeList', params)
  },
  //特雷诺比率
  doPerformanceTreynorList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceTreynorList', params)
  },
  //信息比率
  doPerformanceInfoRateList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceInfoRateList', params)
  },
  //跟踪误差
  doPerformanceTeList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceTeList', params)
  },
  //索提诺比率
  doPerformanceSortinoList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceSortinoList', params)
  },
  //卡玛比率
  doPerformanceCalmarList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceCalmarList', params)
  },
  //欧米茄比率
  doPerformanceOmegaList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceOmegaList', params)
  },
  //卡帕比率
  doPerformanceKappaList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceKappaList', params)
  },
  //上行捕获率
  doPerformanceUcrList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceUcrList', params)
  },
  //下行捕获率
  doPerformanceDcrList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceDcrList', params)
  },
  //下行标准差
  doPerformanceDescVolatilityList: async function (params) {
    return request.post('/api/gfhomepage/doPerformanceDescVolatilityList', params)
  },
}