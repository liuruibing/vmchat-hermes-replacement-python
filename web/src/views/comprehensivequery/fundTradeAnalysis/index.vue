<template>
  <div class="fundTradeAnalysis analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="fundCode">
              <ProductSelectInput
                v-model="selectedProduct"
                placeholder="请选择产品"
                :input-width="'260px'"
                @select="handleProductSelect"
                @clear="handleProductClear"
              />
            </el-form-item>
            <el-form-item prop="ddate_" label="" class="mb20">
              <el-date-picker
                v-model="formQuery.ddate_"
                type="daterange"
                value-format="yyyy-MM-dd"
                align="left"
                size="small"
                unlink-panels
                range-separator="至"
                start-placeholder="请选择开始日期"
                end-placeholder="请选择结束日期"
                popper-class="popperDateShortTP"
                :picker-options="dateShortTP()"
              />
            </el-form-item>
            <el-form-item prop="assetType">
              <el-select v-model="formQuery.assetType" clearable size="small" placeholder="请选择资产类别" @change="handleAssetTypeChange">
                <el-option v-for="item in assetTypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
            <el-form-item prop="assetTypeDetail">
              <el-select v-model="formQuery.assetTypeDetail" clearable size="small" placeholder="请选择分类">
                <el-option v-for="item in assetTypeDetailList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
            <el-form-item prop="symbolCode">
              <el-input v-model.trim="formQuery.symbolCode" clearable placeholder="请输入证券代码" size="small" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" icon="el-icon-search" @click="onSubmit('formQuery')">查询</el-button>
              <el-button type="info" size="small" icon="el-icon-refresh" plain @click="resetForm('formQuery')">重置</el-button>
              <el-button
                type="info"
                size="small"
                plain
                :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'"
                :disabled="isDisabled"
                @click="downloadMainExcel"
              >
                {{ downLoadText }}
              </el-button>
            </el-form-item>
          </el-row>
        </el-form>
      </div>
    </div>

    <el-row>
      <el-col :span="16">
        <div class="page-model-title">
          <div class="title-icon"><div class="color-box"></div></div>
          <span class="title-txt">证券交易及收益明细</span>
        </div>
      </el-col>
      <el-col :span="8">
        <div style="float: right">
          <vxe-toolbar ref="tableToolbar" class="standard-vxe-toolbar" :custom="{ immediate: true }" custom />
        </div>
      </el-col>
    </el-row>

    <el-row id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="table1"
          :sort-config="{ remote: true, defaultSort: { field: 'totalMoneyAfterFee', order: 'desc' } }"
          :loading="tableLoading"
          :custom-config="{ storage: true }"
          :data="tableData"
          :height="tableHeight"
          :cell-style="{ height: '50px' }"
          show-header-overflow
          auto-resize
          show-overflow
          stripe
          resizable
          @sort-change="handleSortChange"
        >
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" align="center" />
          <vxe-table-column field="symbolCode" title="证券代码" min-width="100" header-align="center" align="center" sortable>
            <template slot-scope="scope">
              <a class="link-cell" @click="handleSymbolClick(scope.row)">{{ scope.row.symbolCode }}</a>
            </template>
          </vxe-table-column>
          <vxe-table-column field="symbolName" title="证券名称" min-width="120" header-align="center" align="center" sortable />
          <vxe-table-column field="symbolExchangeName" title="交易市场" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="assetTypeName" title="资产类别" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="assetTypeDetailName" title="分类" min-width="120" header-align="center" align="left" sortable />
          <template v-if="!isQhAsset">
            <vxe-table-column field="endHldAmount" title="期末持仓数量" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="endHldPrice" title="期末持仓市值(元)" min-width="130" header-align="center" align="center" sortable />
            <vxe-table-column field="buyAmount" title="买入数量" min-width="100" header-align="center" align="center" sortable />
            <vxe-table-column field="buyMoney" title="买入金额(元)" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="sellAmount" title="卖出数量" min-width="100" header-align="center" align="center" sortable />
            <vxe-table-column field="sellMoney" title="卖出金额(元)" min-width="110" header-align="center" align="center" sortable />
          </template>
          <template v-else>
            <vxe-table-column field="dtEndHldAmount" title="期末持仓多头数量" min-width="120" header-align="center" align="center" sortable />
            <vxe-table-column field="dtEndHldPrice" title="期末持仓多头市值(元)" min-width="140" header-align="center" align="center" sortable />
            <vxe-table-column field="ktEndHldAmount" title="期末持仓空头数量" min-width="120" header-align="center" align="center" sortable />
            <vxe-table-column field="ktEndHldPrice" title="期末持仓空头市值(元)" min-width="140" header-align="center" align="center" sortable />
            <vxe-table-column field="dtBuyAmount" title="多头买入数量" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="dtBuyMoney" title="多头买入金额(元)" min-width="130" header-align="center" align="center" sortable />
            <vxe-table-column field="dtSellAmount" title="多头卖出数量" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="dtSellMoney" title="多头卖出金额(元)" min-width="130" header-align="center" align="center" sortable />
            <vxe-table-column field="ktBuyAmount" title="空头买入数量" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="ktBuyMoney" title="空头买入金额(元)" min-width="130" header-align="center" align="center" sortable />
            <vxe-table-column field="ktSellAmount" title="空头卖出数量" min-width="110" header-align="center" align="center" sortable />
            <vxe-table-column field="ktSellMoney" title="空头卖出金额(元)" min-width="130" header-align="center" align="center" sortable />
          </template>
          <vxe-table-column field="hldTime" title="持仓周期" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="tradeIncome" title="交易性收益(元)" min-width="120" header-align="center" align="center" sortable />
          <vxe-table-column field="hldIncome" title="持有性收益(元)" min-width="120" header-align="center" align="center" sortable />
          <vxe-table-column field="totalMoney" title="总收益(未扣费)(元)" min-width="130" header-align="center" align="center" sortable />
          <vxe-table-column field="fee" title="交易费用(元)" min-width="110" header-align="center" align="center" sortable />
          <vxe-table-column field="totalMoneyAfterFee" title="总收益(费后)(元)" min-width="120" header-align="center" align="center" sortable />
        </vxe-table>
        <p class="description">
          注:持仓周期划分：在起止时间范围内按照估值表的持仓天数来判断<br>
          短周期：&lt;2周<br>
          中周期：2周 至 12周<br>
          长周期：&gt;12周
        </p>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :page-sizes="[10, 20, 50, 100, 500]"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </el-row>

    <SymbolChartSection
      :visible="showSymbolCharts"
      :price-option="symbolCharts.price"
      :yield-option="symbolCharts.yield"
      :income-option="symbolCharts.income"
      :trade-left-option="symbolCharts.tradeLeft"
      :trade-right-option="symbolCharts.tradeRight"
      :show-trade-money-time="symbolCharts.showTradeMoneyTime"
    />

    <SummaryTables
      ref="summaryTables"
      :show-qh-category="isQhAsset"
      :qh-category-data="qhCategoryData"
      :detail-data="detailData"
      :asset-data="assetData"
      :industry-description="industryDescription"
      @export-qh-category="exportTable('qhCategoryTable', '期货品种汇总')"
      @export-detail="exportTable('detailTable', '分类汇总')"
      @export-asset="exportTable('assetTable', '大类汇总')"
      @industry-click="handleIndustryClick"
      @asset-click="handleAssetClick"
      @qh-category-click="handleQhCategoryClick"
    />

    <TradeCycleCharts
      :visible="industryCharts.visible"
      left-id="industryTradeLeft"
      right-id="industryTradeRight"
      :left-option="industryCharts.left"
      :right-option="industryCharts.right"
    />

    <TradeCycleCharts
      :visible="assetCharts.visible"
      left-id="assetTradeLeft"
      right-id="assetTradeRight"
      :left-option="assetCharts.left"
      :right-option="assetCharts.right"
    />

    <TradeCycleCharts
      :visible="qhCategoryCharts.visible"
      left-id="qhCategoryTradeLeft"
      right-id="qhCategoryTradeRight"
      :left-option="qhCategoryCharts.left"
      :right-option="qhCategoryCharts.right"
    />
  </div>
</template>

<script>
import moment from 'moment'
import XLSX from 'xlsx'
import store from '@/store'
import { excelPost } from '@/utils/request'
import fundTradeAnalysisApi from '@/api/comprehensivequery/fundTradeAnalysis'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'
import SymbolChartSection from './components/SymbolChartSection'
import SummaryTables from './components/SummaryTables'
import TradeCycleCharts from './components/TradeCycleCharts'
import {
  initSymbolPriceAndTradeDataEchart,
  initQHSymbolPriceAndTradeDataEchart,
  initFundYieldAndTradeDataEchart,
  initFundYieldAndQHTradeDataEchart,
  initSymbolIncomeAndTradeDataEchart,
  initQHSymbolIncomeAndTradeDataEchart,
  initSymbolTradeMoneyTimeDataLeftEchart,
  initSymbolTradeMoneyTimeDataRightEchart,
  initIndustryTradeMoneyTimeDataLeftEchart,
  initIndustryTradeMoneyTimeDataRightEchart,
  initAssetTradeMoneyTimeDataLeftEchart,
  initAssetTradeMoneyTimeDataRightEchart,
  initQHCategoryTradeMoneyTimeDataLeftEchart,
  initQHCategoryTradeMoneyTimeDataRightEchart
} from './scripts/chartOptions'

const isForm = { 'Content-Type': 'application/x-www-form-urlencoded' }

export default {
  name: 'FundTradeAnalysis',
  components: { ProductSelectInput, SymbolChartSection, SummaryTables, TradeCycleCharts },
  data() {
    return {
      selectedProduct: null,
      assetTypeList: [],
      assetTypeDetailList: [],
      formQuery: {
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
        assetType: '',
        assetTypeDetail: '',
        symbolCode: '',
        pageNum: 1,
        pageSize: 10,
        orderString: 'totalMoneyAfterFee desc'
      },
      searchRules: {
        fundCode: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [{ required: true, message: '请选择日期', trigger: 'change' }],
        assetType: [{ required: true, message: '请选择资产类别', trigger: 'change' }]
      },
      tableData: [],
      tableHeight: 0,
      tableLoading: false,
      total: 0,
      exportLoading: false,
      isDisabled: false,
      downLoadText: '导出',
      showSymbolCharts: false,
      symbolCharts: { price: null, yield: null, income: null, tradeLeft: null, tradeRight: null, showTradeMoneyTime: false },
      detailData: {},
      assetData: {},
      qhCategoryData: {},
      industryDescription: '',
      industryCharts: { visible: false, left: null, right: null },
      assetCharts: { visible: false, left: null, right: null },
      qhCategoryCharts: { visible: false, left: null, right: null },
      fundStartDate: '',
      fundEndDate: ''
    }
  },
  computed: {
    isQhAsset() {
      return this.formQuery.assetType === 'QH'
    }
  },
  watch: {
    selectedProduct(val, oldVal) {
      if (val && val.VC_FUNDCODE) {
        this.formQuery.fundCode = val.VC_FUNDCODE
        this.formQuery.fundName = val.VC_FUNDNAME
        if (!oldVal || oldVal.VC_FUNDCODE !== val.VC_FUNDCODE) {
          this.loadFundMaxDate(val.VC_FUNDCODE)
        }
      } else {
        this.formQuery.fundCode = ''
        this.formQuery.fundName = ''
      }
    }
  },
  mounted() {
    this.handleTableHeight()
    this.initRouteQuery()
    const baseTime = store.state.edims.baseTime
    if (baseTime && (!this.formQuery.ddate_ || !this.formQuery.ddate_.length)) {
      this.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
    }
    this.$nextTick(() => {
      if (this.$refs.table1 && this.$refs.tableToolbar) {
        this.$refs.table1.connect(this.$refs.tableToolbar)
      }
      this.loadInitData()
    })
  },
  methods: {
    applyBaseTimeDefault() {
      const baseTime = store.state.edims.baseTime
      if (baseTime && baseTime.beginDate && baseTime.endDate) {
        this.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
      } else {
        this.formQuery.ddate_ = []
      }
    },
    resolveFundEndDate(endDate) {
      if (endDate) return endDate
      const baseTime = store.state.edims.baseTime
      if (baseTime && baseTime.endDate) return baseTime.endDate
      return moment().subtract(1, 'days').format('YYYY-MM-DD')
    },
    applyFundDefaultDateRange() {
      if (!this.fundEndDate) return
      let beginDate = this.fundEndDate.substring(0, 7) + '-01'
      if (this.fundStartDate && moment(beginDate).isBefore(this.fundStartDate)) {
        beginDate = this.fundStartDate
      }
      this.formQuery.ddate_ = [beginDate, this.fundEndDate]
    },
    resetFundDateRange() {
      this.fundStartDate = ''
      this.fundEndDate = ''
      this.applyBaseTimeDefault()
    },
    loadFundMaxDate(fundCode) {
      if (!fundCode) {
        this.resetFundDateRange()
        return
      }
      fundTradeAnalysisApi.findFundMaxDate(fundCode).then(res => {
        if (res.status === 0 && res.data && res.data.startDate) {
          this.fundStartDate = res.data.startDate
          this.fundEndDate = this.resolveFundEndDate(res.data.endDate)
          const q = this.$route.query
          if (q.beginDate && q.endDate) {
            this.formQuery.ddate_ = this.clampShortcutRange(q.beginDate, q.endDate)
          } else {
            this.applyFundDefaultDateRange()
          }
        } else {
          this.resetFundDateRange()
        }
      }).catch(() => {
        this.resetFundDateRange()
      })
    },
    clampShortcutRange(start, end) {
      let s = start
      let e = end
      if (this.fundStartDate && moment(s).isBefore(this.fundStartDate)) {
        s = this.fundStartDate
      }
      if (this.fundEndDate && moment(e).isAfter(this.fundEndDate)) {
        e = this.fundEndDate
      }
      if (this.fundStartDate && moment(s).isBefore(this.fundStartDate)) {
        s = this.fundStartDate
      }
      if (moment(s).isAfter(e)) {
        s = this.fundStartDate || s
      }
      return [s, e]
    },
    initRouteQuery() {
      const q = this.$route.query
      if (q.beginDate && q.endDate) this.formQuery.ddate_ = [q.beginDate, q.endDate]
      if (q.fundCode) {
        this.selectedProduct = { VC_FUNDCODE: q.fundCode, VC_FUNDNAME: q.fundName || q.fundCode }
      }
      if (q.assetType) {
        this.formQuery.assetType = q.assetType
        if (this.formQuery.fundCode) this.handleAssetTypeChange(q.assetType)
      }
      if (q.symbolCode) this.formQuery.symbolCode = q.symbolCode
    },
    loadInitData() {
      fundTradeAnalysisApi.initData().then(res => {
        const { status, data } = res
        if (status === 0 && data) {
          this.assetTypeList = data.assetType || []
        }
      })
    },
    handleProductSelect() {
      this.$refs.formQuery && this.$refs.formQuery.validateField('fundCode')
      this.formQuery.assetType = ''
      this.formQuery.assetTypeDetail = ''
      this.formQuery.symbolCode = ''
      this.assetTypeDetailList = []
    },
    handleProductClear() {
      this.selectedProduct = null
      this.assetTypeDetailList = []
      this.formQuery.assetTypeDetail = ''
      this.formQuery.assetType = ''
      this.formQuery.symbolCode = ''
      this.resetFundDateRange()
    },
    handleAssetTypeChange(val) {
      this.formQuery.assetTypeDetail = ''
      this.assetTypeDetailList = []
      if (!val || !this.formQuery.fundCode) return
      fundTradeAnalysisApi.assetTypeDetailByAssetType({
        assetType: val,
        fundCode: this.formQuery.fundCode
      }).then(res => {
        const { status, data } = res
        if (status === 0) this.assetTypeDetailList = data || []
      })
    },
    buildQueryParams(extra = {}) {
      const params = Object.assign({}, this.formQuery, extra)
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0]
        params.endDate = params.ddate_[1]
      }
      delete params.ddate_
      return params
    },
    resetCharts() {
      this.showSymbolCharts = false
      this.symbolCharts = { price: null, yield: null, income: null, tradeLeft: null, tradeRight: null, showTradeMoneyTime: false }
      this.industryCharts = { visible: false, left: null, right: null }
      this.assetCharts = { visible: false, left: null, right: null }
      this.qhCategoryCharts = { visible: false, left: null, right: null }
    },
    onSubmit(formName) {
      this.formQuery.pageNum = 1
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.resetCharts()
          this.onQuery()
          this.loadSummaryData()
        }
      })
    },
    onQuery() {
      this.tableLoading = true
      const params = this.buildQueryParams()
      fundTradeAnalysisApi.queryList(params).then(res => {
        const { status, data } = res
        if (status === 0 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
          this.$message.warning(res.message || '查询失败')
        }
      }).finally(() => {
        this.tableLoading = false
      })
    },
    loadSummaryData() {
      const params = this.buildQueryParams()
      fundTradeAnalysisApi.doAssetTypeDetailTableData(params).then(res => {
        if (res.status === 0) this.detailData = res.data || {}
      })
      fundTradeAnalysisApi.doAssetTypeDetailDescriptionData(params).then(res => {
        if (res.status === 0 && res.data) {
          this.industryDescription = `注:股票-A股和可转债的基准为[${res.data.indexName}-${res.data.indexCode}];股票-港股的基准为[恒生指数-HSI001]。`
        } else {
          this.industryDescription = ''
        }
      })
      fundTradeAnalysisApi.doAssetTypeTableData(params).then(res => {
        if (res.status === 0) this.assetData = res.data || {}
      })
      if (this.isQhAsset) {
        fundTradeAnalysisApi.doQHCategoryTableData(params).then(res => {
          if (res.status === 0) this.qhCategoryData = res.data || {}
        })
      } else {
        this.qhCategoryData = {}
      }
    },
    chartBaseParams(row) {
      return {
        beginDate: this.formQuery.ddate_[0],
        endDate: this.formQuery.ddate_[1],
        fundCode: this.formQuery.fundCode,
        assetType: row.assetType,
        assetTypeDetail: row.assetTypeDetail,
        symbolCode: row.symbolCode,
        symbolExchange: row.symbolExchange
      }
    },
    handleSymbolClick(row) {
      this.symbolCharts = { price: null, yield: null, income: null, tradeLeft: null, tradeRight: null, showTradeMoneyTime: false }
      this.showSymbolCharts = true
      const params = this.chartBaseParams(row)
      const isGpLike = ['GP', 'ZQ_KZZ', 'JJ_ETF'].includes(row.assetType)
      if (isGpLike) {
        fundTradeAnalysisApi.doSymbolPriceChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.price = initSymbolPriceAndTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
        fundTradeAnalysisApi.doSymbolIncomeChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.income = initSymbolIncomeAndTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
        fundTradeAnalysisApi.doFundYieldChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.yield = initFundYieldAndTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
      } else if (row.assetType === 'QH') {
        fundTradeAnalysisApi.doQHSymbolPriceChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.price = initQHSymbolPriceAndTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
        fundTradeAnalysisApi.doQHSymbolIncomeChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.income = initQHSymbolIncomeAndTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
        fundTradeAnalysisApi.doQHFundYieldChartData(params).then(res => {
          if (res.status === 0) {
            this.symbolCharts.yield = initFundYieldAndQHTradeDataEchart(row.assetTypeName, row.symbolCode, row.symbolName, res.data || [])
          }
        })
      }
      fundTradeAnalysisApi.doSymbolTradeMoneyTimeChartData(params).then(res => {
        const list = res.status === 0 ? (res.data || []) : []
        this.symbolCharts.showTradeMoneyTime = list.length > 0
        if (list.length) {
          this.symbolCharts.tradeLeft = initSymbolTradeMoneyTimeDataLeftEchart(row.assetTypeName, row.symbolCode, row.symbolName, list)
          this.symbolCharts.tradeRight = initSymbolTradeMoneyTimeDataRightEchart(row.assetTypeName, row.symbolCode, row.symbolName, list)
        } else {
          this.symbolCharts.tradeLeft = null
          this.symbolCharts.tradeRight = null
        }
      })
    },
    handleIndustryClick(row) {
      this.industryCharts = { visible: false, left: null, right: null }
      const params = {
        beginDate: this.formQuery.ddate_[0],
        endDate: this.formQuery.ddate_[1],
        fundCode: this.formQuery.fundCode,
        assetType: row.assetType,
        assetTypeDetail: row.assetTypeDetail
      }
      fundTradeAnalysisApi.doIndustryTradeMoneyTimeChartData(params).then(res => {
        const list = res.status === 0 ? (res.data || []) : []
        this.industryCharts.visible = list.length > 0
        if (list.length) {
          this.industryCharts.left = initIndustryTradeMoneyTimeDataLeftEchart(row.assetTypeName, row.assetTypeDetailName, list)
          this.industryCharts.right = initIndustryTradeMoneyTimeDataRightEchart(row.assetTypeName, row.assetTypeDetailName, list)
        } else {
          this.industryCharts.left = null
          this.industryCharts.right = null
        }
      })
    },
    handleAssetClick(group) {
      this.assetCharts = { visible: false, left: null, right: null }
      const params = {
        beginDate: this.formQuery.ddate_[0],
        endDate: this.formQuery.ddate_[1],
        fundCode: this.formQuery.fundCode,
        assetType: group.assetType
      }
      fundTradeAnalysisApi.doAssetTradeMoneyTimeChartData(params).then(res => {
        const list = res.status === 0 ? (res.data || []) : []
        this.assetCharts.visible = list.length > 0
        if (list.length) {
          this.assetCharts.left = initAssetTradeMoneyTimeDataLeftEchart(group.assetTypeName, list)
          this.assetCharts.right = initAssetTradeMoneyTimeDataRightEchart(group.assetTypeName, list)
        } else {
          this.assetCharts.left = null
          this.assetCharts.right = null
        }
      })
    },
    handleQhCategoryClick(row) {
      this.qhCategoryCharts = { visible: false, left: null, right: null }
      const params = {
        beginDate: this.formQuery.ddate_[0],
        endDate: this.formQuery.ddate_[1],
        fundCode: this.formQuery.fundCode,
        assetType: row.assetType,
        assetTypeDetail: row.assetTypeDetail,
        futDetailCode: row.futDetailCode,
        futDetailName: row.futDetailName
      }
      fundTradeAnalysisApi.doQHCategoryTradeMoneyTimeChartData(params).then(res => {
        const list = res.status === 0 ? (res.data || []) : []
        this.qhCategoryCharts.visible = list.length > 0
        if (list.length) {
          this.qhCategoryCharts.left = initQHCategoryTradeMoneyTimeDataLeftEchart(row.futDetailName, list)
          this.qhCategoryCharts.right = initQHCategoryTradeMoneyTimeDataRightEchart(row.futDetailName, list)
        } else {
          this.qhCategoryCharts.left = null
          this.qhCategoryCharts.right = null
        }
      })
    },
    downloadMainExcel() {
      this.$refs.formQuery.validate(valid => {
        if (!valid) return
        this.$confirm('确认是否要导出？', '提示', { type: 'warning' }).then(() => {
          this.exportLoading = true
          this.isDisabled = true
          this.downLoadText = '导出中...'
          const params = this.buildQueryParams()
          excelPost('/api/fundTradeAnalysis/downFundTradeAnalysis', params, isForm).then(res => {
            const blob = new Blob([res.data])
            const link = document.createElement('a')
            const beginDate = params.beginDate.replace(/-/g, '')
            const endDate = params.endDate.replace(/-/g, '')
            link.href = window.URL.createObjectURL(blob)
            link.download = `证券交易及收益明细_${params.fundCode}_${params.fundName}_${params.assetType}_${beginDate}_${endDate}.xls`
            link.click()
            window.URL.revokeObjectURL(link.href)
          }).finally(() => {
            this.exportLoading = false
            this.isDisabled = false
            this.downLoadText = '导出'
          })
        }).catch(() => {})
      })
    },
    exportTable(refName, label) {
      this.$confirm('确认是否要导出？', '提示', { type: 'warning' }).then(() => {
        const comp = this.$refs.summaryTables
        const table = comp && comp.$refs[refName]
        if (!table) return
        const sheet = XLSX.utils.table_to_book(table)
        const beginDate = this.formQuery.ddate_[0].replace(/-/g, '')
        const endDate = this.formQuery.ddate_[1].replace(/-/g, '')
        XLSX.writeFile(sheet, `${this.formQuery.fundCode}_${this.formQuery.fundName}_${label}_${beginDate}_${endDate}.xlsx`)
      }).catch(() => {})
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.selectedProduct = null
      this.assetTypeDetailList = []
      this.tableData = []
      this.total = 0
      this.resetCharts()
      this.detailData = {}
      this.assetData = {}
      this.qhCategoryData = {}
      this.industryDescription = ''
      this.resetFundDateRange()
    },
    pagination({ currentPage, pageSize }) {
      this.formQuery.pageNum = currentPage
      this.formQuery.pageSize = pageSize
      this.onQuery()
    },
    handleSortChange(val) {
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val) || 'totalMoneyAfterFee desc'
      this.onQuery()
    },
    handleTableHeight() {
      this.$nextTick(() => {
        if (!this.$refs.table1) return
        this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
        window.onresize = () => {
          if (this.$refs.table1) {
            this.tableHeight = window.innerHeight - this.$refs.table1.$el.offsetTop - 325
          }
        }
      })
    },
    dateShortTP() {
      const self = this
      const maxEnd = () => self.fundEndDate || moment().subtract(1, 'days').format('YYYY-MM-DD')
      const pickRange = (start, end) => self.clampShortcutRange(start, end)
      return {
        disabledDate(time) {
          if (!self.fundStartDate || !self.fundEndDate) return false
          const cur = moment(time).format('YYYY-MM-DD')
          return cur < self.fundStartDate || cur > self.fundEndDate
        },
        shortcuts: [
          { text: '近一周', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(6, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '近一个月', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(1, 'month').add(1, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '近三个月', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(3, 'month').add(1, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '近六个月', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(6, 'month').add(1, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '近1年', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(1, 'years').add(1, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '近3年', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).subtract(3, 'years').add(1, 'days').format('YYYY-MM-DD'), end)) } },
          { text: '本月', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).startOf('month').format('YYYY-MM-DD'), end)) } },
          { text: '本季度', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).startOf('quarter').format('YYYY-MM-DD'), end)) } },
          { text: '本年以来', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(moment(end).startOf('year').format('YYYY-MM-DD'), end)) } },
          { text: '成立以来', onClick(picker) { const end = maxEnd(); picker.$emit('pick', pickRange(self.fundStartDate || end, end)) } }
        ]
      }
    }
  }
}
</script>

<style lang="scss">
.fundTradeAnalysis {
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  .link-cell {
    color: #409eff;
    cursor: pointer;
  }
  .description {
    margin: 8px 0;
    color: #666;
    font-size: 12px;
    line-height: 1.6;
  }
  .echarts_box {
    width: 100%;
  }
}
</style>
