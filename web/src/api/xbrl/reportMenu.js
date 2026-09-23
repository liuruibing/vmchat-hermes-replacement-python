/* 转账指令流程发起接口 */
import request from '@/utils/request'
import qs from 'qs'
export default {

  // 查询批次信息
  selectBatch: async function() {
    return request({
      url: '/api/ann/v1.0/batch',
      method: 'post'
    })
  },
  // 查询组合
  queryBatchCollateFund: async function() {
    return request({
      url: '/api/ann/v1.0/report/batch/fundcodes',
      method: 'post'
    })
  },

  // 查询tree
  getResultElementItems: async function(params) {
    return request.post('/api/ann/v1.0/report/chapters?reportType=' + params.reportType +
      '&reportYear=' + params.reportYear +
      '&fundType=' + params.fundType +
      '&typeIn=' + params.typeIn +
      '&fundCodeStr=' + params.fundCodeStr +
      '&collateFlag=' + params.collateFlag +
      '&relationType=' + params.relationType +
      '&secondNum=' + params.secondNum +
      '&result=' + params.resultData +
      '&resultContent=' + params.resultContent
    )
  },
  // 获取提交的组合
  getFundCodes: async function(params) {
    return request.post('/api/ann/v1.0/report/chapters/fundcodes?reportType=' + params.reportType +
      '&order=' + params.order +
      '&offset=' + params.offset +
      '&limit=' + params.limit +
      '&elementCname=' + params.elementCname +
      '&elementName=' + params.elementName +
      '&rptId=' + params.rptId +
      '&reportYear=' + params.reportYear +
      '&fundType=' + params.fundType +
      '&typeIn=' + params.typeIn +
      '&fundCodeStr=' + params.fundCodeStr +
      '&collateFlag=' + params.collateFlag +
      '&paramFlag=' + params.paramFlag +
      '&relationType=' + params.relationType +
      '&secondNum=' + params.secondNum +
      '&result=' + params.resultData +
      '&resultContent=' + params.resultContent +
      '&isParent=' + params.isParent +
      '&totalFundType=' + params.totalFundType
    )
  },
  // 获取tree点击列表
  getResultElementPageDatas: async function(params) {
    return request.post('/api/ann/v1.0/report/chapters/fundcode?order=' + params.order +
      '&offset=' + params.offset +
      '&limit=' + params.limit +
      '&elementCname=' + params.elementCname +
      '&elementName=' + params.elementName +
      '&rptId=' + params.rptId +
      '&reportType=' + params.reportType +
      '&reportYear=' + params.reportYear +
      '&fundType=' + params.fundType +
      '&typeIn=' + params.typeIn +
      '&fundCodeStr=' + params.fundCodeStr +
      '&fundCode=' + params.fundCode +
      '&fundName=' + params.fundName +
      '&collateFlag=' + params.collateFlag +
      '&paramFlag=' + params.paramFlag +
      '&relationType=' + params.relationType +
      '&secondNum=' + params.secondNum +
      '&result=' + params.resultData +
      '&resultContent=' + params.resultContent +
      '&isParent=' + params.isParent +
      '&totalFundType=' + params.totalFundType +
      '&difference=' + params.difference
    )
  },
  // 获取dialog-tree
  getFundCodeTree: async function(params) {
    return request.post('/api/ann/v1.0/report/chapters/fundcodes-tree?' +
      '&elementCname=' + params.elementCname +
      '&elementName=' + params.elementName +
      '&rptId=' + params.rptId +
      '&reportType=' + params.reportType +
      '&reportYear=' + params.reportYear +
      '&fundType=' + params.fundType +
      '&typeIn=' + params.typeIn +
      '&fundCodeStr=' + params.fundCodeStr +
      '&fundCode=' + params.fundCode +
      '&fundName=' + params.fundName +
      '&collateFlag=' + params.collateFlag +
      '&paramFlag=' + params.paramFlag +
      '&relationType=' + params.relationType +
      '&secondNum=' + params.secondNum +
      '&result=' + params.resultData +
      '&resultContent=' + params.resultContent +
      '&isParent=' + params.isParent +
      '&totalFundType=' + params.totalFundType +
      '&difference=' + params.difference +
      '&batchName=' + params.batchName +
      '&batchId=' + params.batchId

    )
  }

}

