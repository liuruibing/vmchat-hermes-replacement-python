import request from '@/utils/request'
import qs from 'qs'
export default {
    //字典查询
    getTransferType: async function(params) {
        return request({
            url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
            method: 'get',
        })
    },
    // 查询所有 数据源设置
    getDataSourceList: async function(params) {
        return request({
              url: '/api/generalquery/v1.0/getQueryResult.do' + '?' + qs.stringify(params)+'&pageable=true&generalName=survivalPeriod',
            method: 'get',
        })
    },


}