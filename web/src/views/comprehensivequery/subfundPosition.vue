<template>
  <!-- 子基金持仓查询 -->
  <div class="subfundPosition analyse-page">
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
            <el-form-item prop="subCode">
              <el-input v-model.trim="formQuery.subCode" clearable placeholder="请输入子基金代码" size="small" />
            </el-form-item>
            <el-form-item prop="subName">
              <el-input v-model.trim="formQuery.subName" clearable placeholder="请输入子基金名称" size="small" />
            </el-form-item>
            <el-form-item label="" prop="policyType">
              <el-select v-model="formQuery.policyType" class="clll" clearable size="small" placeholder="请选择策略类型">
                <el-option v-for="item in policyTypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
            </el-form-item>
            <el-form-item prop="subPolicyType">
              <el-select v-model="formQuery.subPolicyType" class="cllxchild" clearable size="small" placeholder="请选择子策略类型">
                <el-option v-for="item in subPolicyTypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
              </el-select>
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
          <span class="title-txt">子基金持仓查询</span>
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
          :sort-config="{ remote: true, defaultSort: { field: 'priceRatio', order: 'desc' } }"
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
          <vxe-table-column type="seq" title="序号" width="60" header-align="center" />
          <vxe-table-column field="fundCode" title="产品代码" min-width="80" header-align="center" align="center" />
          <vxe-table-column field="fundName" title="产品名称" min-width="250" header-align="center" align="center" />
          <vxe-table-column field="newDate" title="日期" min-width="100" header-align="center" align="center" sortable />
          <vxe-table-column field="subCode" title="子基金代码" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="subName" title="子基金名称" min-width="100" header-align="center" align="center" />
          <vxe-table-column field="policyType" title="策略类型" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="subPolicyType" title="子策略类型" min-width="120" header-align="center" align="center" />
          <vxe-table-column field="amount" title="数量" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.amount | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="unitCost" title="单位成本(元)" min-width="150" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.unitCost | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="cost" title="成本(元)" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.cost | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="costRatio" title="成本占净值比（%）" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.costRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="price" title="市价(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.price | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="priceValue" title="市值(元)" min-width="120" header-align="center" sortable align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.priceValue | moneyYuan }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="priceRatio" title="市值占净值比（%）" min-width="120" header-align="center" align="right">
            <template slot-scope="scope">
              <span>{{ scope.row.priceRatio | baifenlvS }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </el-row>
  </div>
</template>

<script type="text/ecmascript-6">
import commonApi from '@/api/common'
import subfundPositionApi from '@/api/comprehensivequery/subfundPosition'
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'
import moment from 'moment'
import store from '@/store'

export default {
  name: 'SubfundPositionQuery',
  components: { ProductSelectInputMultiple },
  data() {
    return {
      selectedProducts: [],
      formQuery: {
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCodes: [],
        fundNames: '',
        policyType: '',
        subPolicyType: '',
        subCode: '',
        subName: '',
        pageNum: 1,
        pageSize: 10,
        orderString: 'k.f_price_ratio desc'
      },
      searchRules: {
        ddate_: [{ required: true, message: '请选择日期', trigger: 'change' }],
        fundNames: [{ required: true, message: '请选择产品', trigger: 'change' }]
      },
      policyTypeList: [],
      subPolicyTypeList: [],
      tableData: [],
      tableHeight: 0,
      tableLoading: false,
      total: 0,
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
    this.handleTableHeight()
    this.initRouteQuery()
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
      this.getPolicyTypeListEdims('strategy_type')
      this.getSubPolicyTypeListEdims('fundinvesttype')
    })
  },
  methods: {
    initRouteQuery() {
      const q = this.$route.query
      if (q.endDate) this.formQuery.endDate = q.endDate
      if (q.beginDate) this.formQuery.beginDate = q.beginDate
      else if (q.endDate) this.formQuery.beginDate = q.endDate
      if (this.formQuery.beginDate && this.formQuery.endDate) {
        this.formQuery.ddate_ = [this.formQuery.beginDate, this.formQuery.endDate]
      }
      if (q.subCode) this.formQuery.subCode = q.subCode
      if (q.subName) this.formQuery.subName = q.subName
      if (q.fundCode) {
        this.selectedProducts = [{
          VC_FUNDCODE: q.fundCode,
          VC_FUNDNAME: q.fundName || q.fundCode
        }]
      }
      if (q.fundcodes) {
        const codes = Array.isArray(q.fundcodes) ? q.fundcodes : [q.fundcodes]
        this.selectedProducts = codes.map(code => ({
          VC_FUNDCODE: code,
          VC_FUNDNAME: code
        }))
      }
    },
    handleProductSelect() {
      this.$refs.formQuery && this.$refs.formQuery.validateField('fundNames')
    },
    handleProductClear() {
      this.selectedProducts = []
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.selectedProducts = []
      this.formQuery.fundCodes = []
      this.formQuery.fundNames = ''
      this.timDate = ''
    },
    onSubmit(formName) {
      this.formQuery.pageNum = 1
      this.$refs[formName].validate(valid => {
        if (valid) {
          this.onQuery()
          this.$fun.searchButtonDisabled('issearchButton', this)
        }
      })
    },
    onQuery(flag) {
      const params = Object.assign({}, this.formQuery)
      if (params.ddate_ && params.ddate_.length) {
        params.beginDate = params.ddate_[0]
        params.endDate = params.ddate_[1]
      }
      delete params.ddate_
      if (flag) {
        this.downLoadText = '导出中...'
        this.exportLoading = true
        this.isDisabled = true
        params.pageNum = 1
        params.pageSize = 999999
        params.ex_tmp_name = '子基金持仓查询-导出.xlsx'
      } else {
        this.tableLoading = true
      }
      subfundPositionApi.queryList(params).then(res => {
        const { status, data } = res
        if (status === 0) {
          if (data != null && data !== undefined) {
            if (!flag) {
              this.tableData = data.list || []
              this.total = data.total || 0
            } else if (data) {
              this.$fun.commonDownloadUrl(data)
            }
          }
        } else {
          this.$message({ message: '系统异常', type: 'warning' })
        }
      }).finally(() => {
        this.tableLoading = false
        this.exportLoading = false
        this.isDisabled = false
        this.downLoadText = '导出'
      })
    },
    downloadTableExcel() {
      this.onQuery(true)
    },
    getPolicyTypeListEdims(type) {
      commonApi.edimsDdiaCommon(type).then(res => {
        const { status, data } = res.data
        if (status === 0 && type === 'strategy_type') {
          this.policyTypeList = data
        }
      })
    },
    getSubPolicyTypeListEdims(type) {
      commonApi.edimsDdiaCommon(type).then(res => {
        const { status, data } = res.data
        if (status === 0 && type === 'fundinvesttype') {
          this.subPolicyTypeList = data
        }
      })
    },
    pagination({ currentPage, pageSize }) {
      this.formQuery.pageNum = currentPage
      this.formQuery.pageSize = pageSize
      this.onQuery()
    },
    handleSortChange(val) {
      const fieldMap = {
        amount: 'k.f_amount',
        unitCost: 'k.f_unitprice',
        price: 'k.f_szprice',
        priceValue: 'k.f_price',
        priceRatio: 'k.f_price_ratio',
        costRatio: 'k.f_cost_ratio',
        newDate: 'k.d_date'
      }
      if (fieldMap[val.property]) {
        val.property = fieldMap[val.property]
      }
      this.formQuery.orderString = this.$fun.queryOrderBy_vxe(val) || 'k.f_price_ratio desc'
      this.onQuery()
    },
    dateShortTPCTA() {
      const self = this
      return {
        shortcuts: [
          {
            text: '本周',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '本月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '本季度',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '今年以来',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard()
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [self.timDate, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
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
.subfundPosition {
  .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
}
</style>
