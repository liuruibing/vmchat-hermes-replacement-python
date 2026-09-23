import request from '@/utils/request'
import qs from 'qs'
export default {
  // 发行新产品
  issueProducts: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/issueProducts',
      method: 'post',
      data: params
    })
  },
  // 列表查询
  list: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/list'+'?'+qs.stringify(params),
      method: 'get',
      // data: params
    })
  },

  // 发行新产品 流程节点退回到业务发起的提交接口
  updateReleaseChange: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/updateReleaseChange',
      method: 'post',
      data: params
    })
  },
  
  // 附件查询
  filesGet: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/filesGet'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

  // 查询托管户状态
  checkAccountStatus: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/checkAccountStatus'+'?'+qs.stringify(params),
      method: 'get',
    })
  },


  // @GetMapping("findRaiseDetail")
  // @ApiOperation(value = "募集情况查询明细")
  findRaiseDetail: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/findRaiseDetail'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // @GetMapping("findRaiseSum")
  // @ApiOperation(value = "募集情况查询总额")
  findRaiseSum: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/findRaiseSum'+'?'+qs.stringify(params),
      method: 'get',
    })
  },
  // @GetMapping("findRaise")
  // @ApiOperation(value = "参数募集查询")
  findRaise: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/findRaise'+'?'+qs.stringify(params),
      method: 'get',
    })
  },


  // 产品发行管理-设置募集参数
  // @PostMapping("raiseLaunch")
  // @ApiOperation(value = "募集参数设置发起流程")
  // @PostMapping("/updateSetRaise")
  // @ApiOperation(value = "募集参数设置[重新发起]")
  // @GetMapping("checkDate")
  // @ApiOperation(value = "校验日期")
  
  // 募集参数设置发起流程
  raiseLaunch: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/raiseLaunch',
      method: 'post',
      data: params
    })
  },
  // 募集参数设置[重新发起]
  updateSetRaise: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/updateSetRaise',
      method: 'post',
      data: params
    })
  },
  // 校验日期
  checkDate: async function (params) {
    return request({
      url: '/api/setRaise/v1.0/checkDate'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

  // @RequestMapping("/api/changeRaise/v1.0/")
  // @CrossOrigin(origins = "*", maxAge = 3600)
  // @Api(value = "募集参数变更", tags = "募集参数变更")
  // @PostMapping("raiseLaunch")
  // @ApiOperation(value = "募集参数变更发起流程")
  // @PostMapping("/updateChangeRaise")
  // @ApiOperation(value = "募集参数变更[重新发起]")

  // 募集参数变更发起流程
  changeRaise: async function (params) {
    return request({
      url: '/api/changeRaise/v1.0/raiseLaunch',
      method: 'post',
      data: params
    })
  },

  // 募集参数变更[重新发起]
  updateChangeRaise: async function (params) {
    return request({
      url: '/api/changeRaise/v1.0/updateChangeRaise',
      method: 'post',
      data: params
    })
  },


  // @GetMapping("findNotice")
  // @ApiOperation(value = "资金到账通知书查询")
  findNotice: async function (params) {
    return request({
      url: '/api/productRelease/v1.0/findNotice'+'?'+qs.stringify(params),
      method: 'get',
    })
  },

}