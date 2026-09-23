import request from '@/utils/request'
import qs from 'qs'

const baseURL = "/api/reportConfig/v1.0/"
export default {
    //查询报表信息    路径  findReport
	//需要数据:reportCode   报表编码
	//返回数据:一个map集合,第一个是对象,后面是list集合
	

    //findReport
    findReport:  function (params) {
      return request({
        url: baseURL+'findReport',
        method: 'post',
        data: params
        //data:qs.stringify(params)
      })
    },

    
  
  
  
  }