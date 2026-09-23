import request from '@/utils/request'
import qs from 'qs'
const ContentTypeFormData = {'Content-type' : 'application/x-www-form-urlencoded'}

export  default {

  // 删除
  delAccountTypeInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/taAccountType/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addAccountTypeInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/taAccountType/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  getAccountTypeInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/taAccountType/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  editAccountTypeInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/taAccountType/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  
  // 删除
  delBankInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/yhckxx/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addBankInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/yhckxx/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  getBankInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/yhckxx/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  editBankInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/yhckxx/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },


  // 删除
  delFispInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispFin/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addFispInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispFin/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  getFispInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispFin/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  editFispInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispFin/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  
  // 删除
  delInvestInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispTycd/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addInvestInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispTycd/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  getInvestInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispTycd/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  editInvestInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispTycd/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  
  addRebuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/mdRebuySet/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  delRebuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/mdRebuySet/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  editRebuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/mdRebuySet/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  getRebuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/mdRebuySet/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  // 删除
  delAdminInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/zgcpInfo/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addAdminInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/zgcpInfo/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  getAdminInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/zgcpInfo/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  editAdminInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/zgcpInfo/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  // 删除产品文件信息
  delFileInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/dimFileInfo/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  // 新增产品文件信息
  addFileInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/dimFileInfo/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  // 查询产品文件信息
  getFileInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/dimFileInfo/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  // 更新产品文件信息
  editFileInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/dimFileInfo/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  
  addLayersInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispIExcel/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  delLayersInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispIExcel/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  editLayersInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispIExcel/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  getLayersInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/fispIExcel/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  addBuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/productPartyBuy/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  delBuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/productPartyBuy/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  editBuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/productPartyBuy/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  getBuyInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/productPartyBuy/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  addSpecialAccInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/ydyzhxx/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  delSpecialAccInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/ydyzhxx/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  editSpecialAccInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/ydyzhxx/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  getSpecialAccInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/ydyzhxx/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },

  
  addSymbolInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/industrySymbol/v1.0/insertInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  delSymbolInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/industrySymbol/v1.0/delInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  editSymbolInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/industrySymbol/v1.0/updateInfo',
      method: 'POST',
      data: qs.stringify( params )
    })
  },
  getSymbolInfo: async function ( params ) {
    return request({
      header: ContentTypeFormData,
      url: '/api/industrySymbol/v1.0/list',
      method: 'POST',
      data: qs.stringify( params )
    })
  },


}