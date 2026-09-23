import request from '@/utils/request'
export default {

  // 根据组合代码获取最新的估值日期
  fundNewGzDate: async function (fundCode) {

    return request({
      url: '/api/performance-detail/v1.0/fund-new-gz-date/'+ fundCode,
      method: 'post',
    })
  },

  // 根据组合代码和日期获取组合基本信息
  fundInformation: async function (fundCode,nowDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-information/'+ fundCode +'?nowDate='+ nowDate,
      method: 'post',
    })
  },
  // 组合收益率分析 组合业绩分析
  // 根据组合代码 开始时间 结束时间获取绩效详情
  fundAnalyse: async function (beginDate,endDate,data) {

    return request({
      url: '/api/performance-detail/v1.0/fundAnalyse?beginDate='+ beginDate + '&endDate='+ endDate,
      method: 'post',
      data
    })
  },
  // 组合收益率分析 组合业绩分析
  // 根据组合代码 开始时间 结束时间获取绩效详情  导出
  fundAnalyseExport: async function (beginDate,endDate,data,name) {

    return request({
      url: '/api/performance-detail/v1.0/fundAnalyse?beginDate='+ beginDate + '&endDate='+ endDate + "&ex_tmp_name=" + name,
      method: 'post',
      data
    })
  },
    //收益分解
    // 根据组合代码和日期获取 收益贡献的资产比例图
   fundAssetsRatioChart: async function (fundCode,beginDate,endDate) {

       return request({
         url: '/api/performance-detail/v1.0/fund-assets-ratio-chart/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
        method: 'post',
      })
  },
  //右侧资产table详情
  contribution: async function (beginDate,endDate,data) {

    return request({
      url: '/api/performance-detail/v1.0/contribution?beginDate='+ beginDate + '&endDate='+ endDate,
      method: 'post',
      data
    })
    // "beginData": "2018-12-02",
    //   "endData": "2018-12-30",
    //   "periodDays": 29,
    //   "fundcode": "200114",
    //   "fundManager": "",
    //   "fundGsManager": "",
    //   "Ratio_GP": 0,  股票占比
    //   "fundAsset_GP": 0, 资产净值
    //   "profitRate_GP": 0, 区间收益率
    //    "moneyRate_GP":0,资产加权收益率
    //    "periodIncome_GP":0,资产收益
    //   "Ratio_ZQ": 0,
    //   "fundAsset_ZQ": 0,
    //   "profitRate_ZQ": 0,
    //   "Ratio_EQUITY": 0,
    //   "fundAsset_EQUITY": 0,
    //   "profitRate_EQUITY": 0
  },

    // 根据组合代码和日期获取 收益贡献的资产收益金额接口
  fundAssetsMoneyChart: async function (fundCode,beginDate,endDate) {

       return request({
         url: '/api/performance-detail/v1.0/fund-assets-money-chart/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
        method: 'post',
      })
  },

    // 根据组合代码和日期获取 收益贡献的收益占比
  fundProfitRatio: async function (fundCode,beginDate,endDate) {

       return request({
         url: '/api/performance-detail/v1.0/fund-profit-ratio/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
        method: 'post',
      })
  },

   //绩效归因接口
  fundPerformanceChart: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-performance-chart/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
   //策略风格箱
  fundTermInvestStyle: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-term-invest-style/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
  //策略风格箱平均持股规模
  fundTermInvestStyleTable: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-term-invest-style-table/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
  //策略风格箱平均持股规模 导出
  fundTermInvestStyleTableExport: async function (fundCode,beginDate,endDate,name) {

    return request({
      url: '/api/performance-detail/v1.0/fund-term-invest-style-table/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate + "&ex_tmp_name=" + name,
      method: 'post',
    })
  },
   //投资风格时序
  fundInvestStyleTimeOrder: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-invest-style-time-order/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
   //期末持股行业占比
  fundTermIndustryRatio: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-term-industry-ratio/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
   //期末持股行业基准占比
  fundTermIndustryDatumRatio: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-term-industry-datum-ratio/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },
  //换手率

  fundChangeHandsRatio: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-detail/v1.0/fund-change-hands-ratio/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },


  //组合收益对比分析
  multipleFundRatio: async function (fundCode,beginDate,endDate) {

    return request({
      url: '/api/performance-multiple-fund-compare/v1.0/multiple-fund-ratio/'+ fundCode + '?beginDate=' + beginDate + '&endDate=' + endDate,
      method: 'post',
    })
  },

  // campisi归因table接口
  campisiList: async function (beginDate,endDate,fundCodes,yieldType) {

    return request({
      url: '/api/campisi/v1.0/list?beginDate='+ beginDate + '&endDate=' + endDate + '&fundCodes=' + fundCodes + '&yieldType=' + yieldType,
      method: 'get',
    })
  },

  // campisi归因table接口 导出
  campisiListExport: async function (beginDate,endDate,fundCodes,yieldType,name) {

    return request({
      url: '/api/campisi/v1.0/list?beginDate='+ beginDate
      + '&endDate=' + endDate
      + '&fundCodes=' + fundCodes
      + '&yieldType=' + yieldType
      + "&ex_tmp_name=" + name,
      method: 'get',
    })
  },

  // campisi归因图表接口
  campisiListDetailList: async function (beginDate,endDate,fundCodes,yieldType) {

    return request({
      url: '/api/campisi/v1.0/detail/list?beginDate='+ beginDate + '&endDate=' + endDate + '&fundCode=' + fundCodes + '&yieldType=' + yieldType,
      method: 'get',
    })
  },
  //brinson归因table 列表
  brinsonList: async function (beginDate,endDate,fundCodes,indexType) {

    return request({
      url: '/api/brinson/v1.0/list?beginDate=' + beginDate + '&endDate=' + endDate + '&fundCodes=' + fundCodes + '&indexType=' + indexType + '&industryDim=SWSR',
      method: 'get',
    })
  },
  //brinson归因table 列表 导出
  brinsonListExport: async function (beginDate,endDate,fundCodes,indexType,name,id_name,pid_name,prefix_name) {

    return request({
      url: '/api/brinson/v1.0/list?beginDate=' + beginDate
      + '&endDate=' + endDate
      + '&fundCodes=' + fundCodes
      + '&indexType=' + indexType
      + '&industryDim=SWSR'
      + "&ex_tmp_name=" + name
      + "&id_name=" + id_name
      + "&pid_name=" + pid_name
      + "&prefix_name=" + prefix_name,
      method: 'get',
    })
  },
  //brinson归因 图
  brinsonDetailList: async function (beginDate,endDate,fundCode,indexType) {

    return request({
      url: '/api/brinson/v1.0/brinsonDetail/list?beginDate=' + beginDate + '&endDate=' + endDate + '&fundCode=' + fundCode + '&indexType=' + indexType + '&industryDim=SWSR',
      method: 'get',
    })
  },








}
