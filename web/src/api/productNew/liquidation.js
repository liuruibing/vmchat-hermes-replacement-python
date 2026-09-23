import request from '@/utils/request'
import qs from 'qs'
export default {
  // 产品清盘管理
  // @RequestMapping("/api/liquidation/v1.0/")
  // @CrossOrigin(origins = "*", maxAge = 3600)
  // @Api(value = "产品清盘", tags = "产品清盘")
  // @GetMapping("liquidationList")
  // @ApiOperation(value = "产品清盘查询")
  // @PostMapping("liquidationLaunch")
  // @ApiOperation(value = "产品清盘发起流程")
  // @PostMapping("/updateLiquidationChange")
  // @ApiOperation(value = "产品清盘[重新发起]")

  // 列表查询
  liquidationList:async function (params) {
    return request({
      url: '/api/liquidation/v1.0/liquidationList?' + qs.stringify(params),
      method: 'get',
    })
  },
  // 产品清盘发起流程
  liquidationLaunch:async function (params) {
    return request({
      url: '/api/liquidation/v1.0/liquidationLaunch',
      method: 'post',
      data: params
    })
  },
  // 产品清盘[重新发起]
  updateLiquidationChange:async function (params) {
    return request({
      url: '/api/liquidation/v1.0/updateLiquidationChange',
      method: 'post',
      data: params
    })
  },



  

}