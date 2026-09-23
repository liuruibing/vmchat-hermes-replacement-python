
/* 产品信息接口 */
import request from '@/utils/request'
import qs from 'qs'
const url = '/api/process/v1.0/processInstance/';
export  default {

  //查询产品信息
  getAll: async function (fundName,fundCode,orderByString,limit,offset) {
    let urls = '/api/product/v1.0/productsGet?offset='+ offset +'&limit='+ limit;

    if(fundName != "0"){
      urls = urls  +"&fundName="+fundName;
    }
    if(fundCode != "0"){
      urls = urls  +"&fundCode="+fundCode;
    }
    if(orderByString != "0"){
      urls = urls  +"&orderByString="+orderByString;
    }

    return request.get(urls)

  },
  //查看详情
  getDetailById: async function (id) {
    return request({
      url: '/api/product/v1.0/getProductById?id=' + id,
      method: 'get',
    })
  },
  getSelects: async function (params) {
    return request({
      url: '/api/edimExt/v1.0/edimsGet?dimTypecode=' + params,
      method: 'get',
    })
  }


}

