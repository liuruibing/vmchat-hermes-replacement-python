import request from '@/utils/request'
export default {

  // vm导出   先用提交form 表单方式
  exportPdf: async function (templateCode,beginDate,endDate,fundCode) {

    return request({
      url: '/rest/report/export.do?templateCode=' + templateCode + '&beginDate=' + beginDate + '&endDate=' + endDate + '&fundCode=' + fundCode,
      method: 'get',
    })
  },
}
