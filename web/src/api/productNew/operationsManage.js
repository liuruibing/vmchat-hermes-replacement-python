import request from '@/utils/request'
import qs from 'qs'
export default {
  // 产品日常运营管理

  // 列表查询-综合业务办理
  fundList:async function (params) {
    return request({
      url: '/api/newConduct/v1.0/fundList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // @GetMapping("downloadTemplate")
  // @ApiOperation(value = "下载模板")反洗钱
  downloadTemplate:async function (params) {
    return request({
      url: '/api/newConduct/v1.0/downloadTemplate?' + qs.stringify(params),
      method: 'get',
    })
  },

  // 产品分红
  // @RequestMapping("/api/dividends/v1.0/")
  // @CrossOrigin(origins = "*", maxAge = 3600)
  // @Api(value = "产品分红", tags = "产品分红")
  // @GetMapping("dividendsList")
  // @ApiOperation(value = "产品分红查询")
  // @PostMapping("dividendsLaunch")
  // @ApiOperation(value = "产品分红发起流程")
  // @PostMapping("/updateDividendsChange")
  // @ApiOperation(value = "产品分红[重新发起]")

  // 产品分红查询
  dividendsList:async function (params) {
    return request({
      url: '/api/dividends/v1.0/dividendsList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 产品分红流程发起
  dividendsLaunch:async function (params) {
    return request({
      url: '/api/dividends/v1.0/dividendsLaunch',
      method: 'post',
      data: params
    })
  },
  // 产品分红[重新发起]
  updateDividendsChange:async function (params) {
    return request({
      url: '/api/dividends/v1.0/updateDividendsChange',
      method: 'post',
      data: params
    })
  },

  

}