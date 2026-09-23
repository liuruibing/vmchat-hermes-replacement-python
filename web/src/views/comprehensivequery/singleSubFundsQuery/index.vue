<template>
  <!-- 单子基金查询 -->
  <div class="singleSubFundsQuery analyse-page">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :rules="searchRules" :model="formQuery" class="standard-form">
          <el-row>
            <el-form-item prop="fundNames">
              <ProductSelectInputMultiple
                v-model="selectedProducts"
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
                :picker-options="dateShortTPCTA()"
              />
            </el-form-item>
            <el-form-item prop="singleSubFund">
              <el-select
                v-model="formQuery.singleSubFund"
                filterable
                clearable
                size="small"
                placeholder="请选择子基金"
                style="width: 200px"
              >
                <el-option
                  v-for="item in subFundList"
                  :key="item.symbolCode"
                  :label="item.symbolName"
                  :value="item.symbolCode"
                />
              </el-select>
              <el-button
                type="info"
                size="small"
                plain
                icon="el-icon-refresh"
                title="子基金列表刷新"
                style="margin-left: 8px"
                @click="refreshSubFundList"
              />
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
                @click="downloadTableExcel"
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
          <div class="title-icon">
            <div class="color-box"></div>
          </div>
          <span class="title-txt">子基金持仓列表</span>
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
          :sort-config="{ remote: true, defaultSort: { field: 'tDate', order: 'asc' } }"
          :loading="tableLoading"
          :custom-config="{ storage: true }"
          :data="tableData"
          :max-height="tableMaxHeight"
          :cell-style="{ height: '50px' }"
          show-header-overflow
          auto-resize
          show-overflow
          stripe
          resizable
          @sort-change="handleSortChange"
        >
<!--          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />-->
          <vxe-table-column field="tDate" title="日期" min-width="100" header-align="center" align="left"  />
          <vxe-table-column field="symbolCode" title="证券代码" min-width="130" header-align="center" align="left" />
          <vxe-table-column field="symbolName" title="证券名称" min-width="130" header-align="center" align="left" />
          <vxe-table-column field="symbolShare" title="份额" min-width="130" header-align="center" align="right" />
          <vxe-table-column field="symbolPrice" title="市值(元)" min-width="130" header-align="center" align="right" />
          <vxe-table-column field="symbolCost" title="成本(元)" min-width="130" header-align="center" align="right" />
          <vxe-table-column field="symbolYield" title="收益率(%)" min-width="130" header-align="center" align="right" />
          <vxe-table-column field="symbolContribute" title="日净值贡献(%)" min-width="130" header-align="center" align="right" />
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :page-sizes="[10, 20, 50, 100, 500, 10000]"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </el-row>

    <div class="chart-content">
      <myChart v-if="chartOption" id="singleSubFundsChart" :options="chartOption" class="echarts_box" resize-dom="cmbfof" />
    </div>

    <p class="description">
      注:子基金持有的份额,成本、市值是选择的多产品的汇总之和。<br>
      收益率=收益额/成本。<br>
      日净值贡献=sum(子基金收益额/产品份额)。<br>
    </p>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import singleSubFundsApi from '@/api/comprehensivequery/singleSubFunds'
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'
import { buildSingleSubFundsChartOption } from './scripts/chartOptions'
import moment from 'moment'
import store from '@/store'

export default {
  name: 'SingleSubFundsQuery',
  components: { myChart, ProductSelectInputMultiple },
  data() {
    return {
      selectedProducts: [],
      subFundList: [],
      formQuery: {
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCodes: [],
        fundNames: '',
        singleSubFund: '',
        vc_type: '',
        vc_symbol: '',
        vc_name: '',
        pageNum: 1,
        pageSize: 10,
        orderString: 'tDate asc'
      },
      searchRules: {
        ddate_: [{ required: true, message: '请选择日期', trigger: 'change' }],
        fundNames: [{ required: true, message: '请选择产品', trigger: 'change' }]
      },
      tableData: [],
      tableMaxHeight: 320,
      tableLoading: false,
      total: 0,
      chartOption: null,
      timDate: '',
      exportLoading: false,
      isDisabled: false,
      downLoadText: '导出'
    }
  },
  watch: {
    selectedProducts: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.formQuery.fundCodes = newVal.map(item => item.VC_FUNDCODE)
          this.formQuery.fundNames = newVal.map(item => item.VC_FUNDNAME).join(',')
          if (newVal[0] && newVal[0].D_CREATE_DATE) {
            this.timDate = newVal[0].D_CREATE_DATE
          }
        } else {
          this.formQuery.fundCodes = []
          this.formQuery.fundNames = ''
          this.timDate = ''
        }
      },
      immediate: true
    }
  },
  mounted() {
    this.scrollPageToTop()
    const baseTime = store.state.edims.baseTime
    if (baseTime && (!this.formQuery.ddate_ || !this.formQuery.ddate_.length)) {
      this.formQuery.ddate_ = [baseTime.beginDate, baseTime.endDate]
      this.formQuery.beginDate = baseTime.beginDate
      this.formQuery.endDate = baseTime.endDate
    }
    this.$nextTick(() => {
      if (this.$refs.table1 && this.$refs.tableToolbar) {
        this.$refs.table1.connect(this.$refs.tableToolbar)
      }
    })
  },
  activated() {
    this.scrollPageToTop()
  },
  methods: {
    handleProductSelect() {
      this.$refs.formQuery && this.$refs.formQuery.validateField('fundNames')
    },
    handleProductClear() {
      this.selectedProducts = []
      this.subFundList = []
      this.formQuery.singleSubFund = ''
    },
    scrollPageToTop() {
      const appMain = document.getElementById('appMain')
      if (appMain) {
        appMain.scrollTop = 0
      }
    },
    updateTableMaxHeight() {
      const rowCount = Math.max(this.tableData.length, 1)
      const headerHeight = 48
      const rowHeight = 50
      const contentHeight = headerHeight + rowCount * rowHeight
      this.tableMaxHeight = Math.min(360, Math.max(200, contentHeight))
    },
    buildQueryParams(extra = {}) {
      const params = Object.assign({}, this.formQuery, extra)
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0]
        params.endDate = params.ddate_[1]
      }
      delete params.ddate_
      this.applySubFundParams(params)
      return params
    },
    applySubFundParams(params) {
      const value = params.singleSubFund
      if (!value) {
        params.vc_type = ''
        params.vc_symbol = ''
        params.vc_name = ''
        return false
      }
      const parts = value.split('_')
      params.vc_type = parts[0]
      params.vc_symbol = parts[1]
      const selected = this.subFundList.find(item => item.symbolCode === value)
      params.vc_name = selected ? selected.symbolName : ''
      return true
    },
    validateSubFund() {
      if (!this.formQuery.singleSubFund) {
        this.$message.warning('子基金不能为空')
        return false
      }
      return true
    },
    refreshSubFundList() {
      this.$refs.formQuery.validate(valid => {
        if (!valid) return
        const params = this.buildQueryParams()
        delete params.singleSubFund
        delete params.vc_type
        delete params.vc_symbol
        delete params.vc_name
        singleSubFundsApi.getAllSubFundsListByMultiFundCodes(params).then(res => {
          const { status, data } = res
          if (status === 0 && data) {
            this.subFundList = data || []
            if (this.subFundList.length > 0) {
              this.formQuery.singleSubFund = this.subFundList[0].symbolCode
            } else {
              this.formQuery.singleSubFund = ''
              this.$message.warning('未查询到子基金，请确认日期范围内有持仓，且当前用户有产品权限')
            }
          } else {
            this.subFundList = []
            this.formQuery.singleSubFund = ''
            this.$message.warning(res.message || '子基金列表刷新失败')
          }
        })
      })
    },
    onSubmit(formName) {
      this.formQuery.pageNum = 1
      this.$refs[formName].validate(valid => {
        if (valid && this.validateSubFund()) {
          this.onQuery()
          this.loadChart()
        }
      })
    },
    onQuery() {
      this.tableLoading = true
      const params = this.buildQueryParams()
      singleSubFundsApi.queryList(params).then(res => {
        const { status, data } = res
        if (status === 0 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
          this.updateTableMaxHeight()
        } else {
          this.tableData = []
          this.total = 0
          this.updateTableMaxHeight()
        }
      }).finally(() => {
        this.tableLoading = false
      })
    },
    loadChart() {
      const params = this.buildQueryParams()
      singleSubFundsApi.queryChart(params).then(res => {
        const { status, data } = res
        if (status === 0) {
          this.chartOption = buildSingleSubFundsChartOption(data || [])
        } else {
          this.chartOption = null
        }
      })
    },
    downloadTableExcel() {
      this.$refs.formQuery.validate(valid => {
        if (!valid || !this.validateSubFund()) return
        this.$confirm('确认是否要导出？', '提示', { type: 'warning' }).then(() => {
          this.exportLoading = true
          this.isDisabled = true
          this.downLoadText = '导出中...'
          const params = this.buildQueryParams()
          singleSubFundsApi.exportList(params).then(res => {
            const blob = new Blob([res.data])
            const link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = '子基金持仓列表.xls'
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.selectedProducts = []
      this.subFundList = []
      this.formQuery.fundCodes = []
      this.formQuery.fundNames = ''
      this.formQuery.singleSubFund = ''
      this.tableData = []
      this.total = 0
      this.chartOption = null
      this.timDate = ''
      this.updateTableMaxHeight()
    },
    pagination({ currentPage, pageSize }) {
      this.formQuery.pageNum = currentPage
      this.formQuery.pageSize = pageSize
      this.onQuery()
    },
    handleSortChange(val) {
      const fieldMap = {
        tDate: 'tDate',
        symbolCode: 'symbolCode',
        symbolName: 'symbolName',
        symbolShare: 'symbolShare',
        symbolPrice: 'symbolPrice',
        symbolCost: 'symbolCost',
        symbolYield: 'symbolYield',
        symbolContribute: 'symbolContribute'
      }
      if (fieldMap[val.property]) {
        val.property = fieldMap[val.property]
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val) || 'tDate asc'
      this.onQuery()
    },
    dateShortTPCTA() {
      const self = this
      return {
        shortcuts: [
          {
            text: '近一周',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(6, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(1, 'months').add(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(3, 'months').add(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近六个月',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(6, 'months').add(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近1年',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(1, 'years').add(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近3年',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).subtract(3, 'years').add(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '本月',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).startOf('month').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '本季度',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).startOf('quarter').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '本年以来',
            onClick(picker) {
              const end = moment().format('YYYY-MM-DD')
              const start = moment(end).startOf('year').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard()
              const end = moment().format('YYYY-MM-DD')
              picker.$emit('pick', [self.timDate, end])
            }
          }
        ]
      }
    },
    getStandard() {
      if (!this.formQuery.fundCodes.length || !this.formQuery.fundNames) {
        this.timDate = ''
        this.$message({ message: '请先选择产品！', type: 'warning', customClass: 'message-warning' })
        return
      }
      if (this.formQuery.fundCodes.length > 1) {
        this.timDate = ''
        this.$message({ message: '请选择单个产品！', type: 'warning', customClass: 'message-warning' })
        return
      }
      if (!this.timDate) {
        this.$message({ message: '未获取到成立日！', type: 'warning', customClass: 'message-warning' })
      }
    }
  }
}
</script>

<style lang="scss">
.singleSubFundsQuery {
  padding-bottom: 48px;
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  .page-model-title {
    margin: 0 10px 8px;
  }
  .chart-content {
    margin: 16px 10px 0;
  }
  .echarts_box {
    width: 100%;
    height: 380px;
  }
  .description {
    margin: 12px 10px 0;
    color: #666;
    font-size: 12px;
    line-height: 1.8;
  }
}
</style>
