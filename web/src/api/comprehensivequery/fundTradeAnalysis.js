import { post } from '@/utils/request'
import qs from 'qs'

const isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  initData() {
    return post('/api/fundTradeAnalysis/initData', qs.stringify({}), isForm)
  },
  findFundMaxDate(fundCode) {
    return post('/api/fundTradeAnalysis/findFundMaxDate', qs.stringify({ fundCode }), isForm)
  },
  assetTypeDetailByAssetType(params) {
    return post('/api/fundTradeAnalysis/assetTypeDetailByAssetType', qs.stringify(params), isForm)
  },
  queryList(params) {
    return post('/api/fundTradeAnalysis/doFundTradeAnalysis', qs.stringify(params), isForm)
  },
  doSymbolPriceChartData(params) {
    return post('/api/fundTradeAnalysis/doSymbolPriceChartData', qs.stringify(params), isForm)
  },
  doQHSymbolPriceChartData(params) {
    return post('/api/fundTradeAnalysis/doQHSymbolPriceChartData', qs.stringify(params), isForm)
  },
  doFundYieldChartData(params) {
    return post('/api/fundTradeAnalysis/doFundYieldChartData', qs.stringify(params), isForm)
  },
  doSymbolIncomeChartData(params) {
    return post('/api/fundTradeAnalysis/doSymbolIncomeChartData', qs.stringify(params), isForm)
  },
  doQHSymbolIncomeChartData(params) {
    return post('/api/fundTradeAnalysis/doQHSymbolIncomeChartData', qs.stringify(params), isForm)
  },
  doQHFundYieldChartData(params) {
    return post('/api/fundTradeAnalysis/doQHFundYieldChartData', qs.stringify(params), isForm)
  },
  doSymbolTradeMoneyTimeChartData(params) {
    return post('/api/fundTradeAnalysis/doSymbolTradeMoneyTimeChartData', qs.stringify(params), isForm)
  },
  doAssetTypeDetailTableData(params) {
    return post('/api/fundTradeAnalysis/doAssetTypeDetailTableData', qs.stringify(params), isForm)
  },
  doAssetTypeDetailDescriptionData(params) {
    return post('/api/fundTradeAnalysis/doAssetTypeDetailDescriptionData', qs.stringify(params), isForm)
  },
  doAssetTypeTableData(params) {
    return post('/api/fundTradeAnalysis/doAssetTypeTableData', qs.stringify(params), isForm)
  },
  doIndustryTradeMoneyTimeChartData(params) {
    return post('/api/fundTradeAnalysis/doIndustryTradeMoneyTimeChartData', qs.stringify(params), isForm)
  },
  doAssetTradeMoneyTimeChartData(params) {
    return post('/api/fundTradeAnalysis/doAssetTradeMoneyTimeChartData', qs.stringify(params), isForm)
  },
  doQHCategoryTableData(params) {
    return post('/api/fundTradeAnalysis/doQHCategoryTableData', qs.stringify(params), isForm)
  },
  doQHCategoryTradeMoneyTimeChartData(params) {
    return post('/api/fundTradeAnalysis/doQHCategoryTradeMoneyTimeChartData', qs.stringify(params), isForm)
  }
}
