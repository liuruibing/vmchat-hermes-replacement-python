<template>
  <div class="gfindicator-page standard-form-margin">
    <el-form ref="queryForm" :model="form" :rules="queryRules" :inline="true" class="standard-form"
      @submit.native.prevent>
      <el-form-item label="起止日期" prop="dateRange" required>
        <el-date-picker v-model="form.dateRange" type="daterange" range-separator="-" start-placeholder="开始日期"
          end-placeholder="结束日期" value-format="yyyy-MM-dd" :picker-options="pickerOptions" size="small"
          style="width: 280px" />
      </el-form-item>
      <el-form-item label="指标类型" prop="indicatorCode">
        <el-select v-model="form.indicatorCode" class="indicator-type-select" filterable placeholder="请选择" size="small"
          @change="onIndicatorChange">
          <el-option v-for="item in indicatorTypes" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
        </el-select>
      </el-form-item>
      <el-form-item label="产品名称" prop="fundCodes">
        <ProductSelectInputMultiple v-model="selectedProducts" placeholder="请选择产品" :input-width="'260px'" />
      </el-form-item>
      <el-form-item>
        <el-button v-btn="'BT.MSG.INDICATOR.SEARCH'" type="primary" size="small" icon="el-icon-search"
          :loading="tableLoading" @click="handleSearch(true)">查询</el-button>
        <el-button v-btn="'BT.MSG.INDICATOR.EXPORT'" type="info" size="small" plain
          icon="el-icon-download" :loading="exportLoading" @click="handleExport">导出</el-button>
        <el-button v-btn="'BT.MSG.INDICATOR.DATA'" type="info" size="small" plain
          icon="el-icon-refresh" :loading="executeLoading" @click="handleExecuteData">重跑数据</el-button>
        <el-button v-btn="'BT.MSG.INDICATOR.LOG'" type="info" size="small" plain
          icon="el-icon-document" @click="mainLogVisible = true">日志列表</el-button>
      </el-form-item>
    </el-form>

    <el-tabs v-model="indicatorTabPlaceholder" type="card">
      <el-tab-pane :label="currentIndicatorName" name="current"></el-tab-pane>
    </el-tabs>

    <div class="table-wrap table-content" id="gfindicator-table">
      <vxe-table ref="refsTable" v-loading="tableLoading" :data="tableData" :height="tableHeight" auto-resize stripe
        border resizable sync-resize show-overflow="tooltip" style="width: 100%" :sort-config="{ remote: true }"
        @sort-change="onVxeSortChange">
        <vxe-table-column v-for="col in tableColumns" :key="col.prop" :field="col.prop" :title="col.label"
          :min-width="col.minWidth" :align="col.align || 'left'" header-align="center" sortable />
      </vxe-table>
      <vxe-pager class="standard-vxe-pager pagination-bar" :current-page="pageNum" :page-size="pageSize" :total="total"
        :page-sizes="pagerConfig.pageSizes"
        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']" border size="medium"
        @page-change="pagination" />
    </div>

    <!-- 主日志 -->
    <el-dialog title="日志列表" :visible.sync="mainLogVisible" width="85% !important" top="8vh" append-to-body @open="onMainLogOpen">
      <el-form :inline="true" size="small" class="log-filter">
        <el-form-item label="编码">
          <el-input v-model="mainLogQuery.vcCode" clearable style="width: 120px" />
        </el-form-item>
        <el-form-item label="开始执行时间">
          <el-date-picker v-model="mainLogQuery.dExecBeginDate" type="date" value-format="yyyy-MM-dd" placeholder="开始执行时间"
            style="width: 140px" />
        </el-form-item>
        <el-form-item label="结束执行时间">
          <el-date-picker v-model="mainLogQuery.dExecEndDate" type="date" value-format="yyyy-MM-dd" placeholder="结束执行时间"
            style="width: 140px" />
        </el-form-item>
        <el-form-item label="执行结果">
          <el-select v-model="mainLogQuery.vcStatus" clearable placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="成功" value="0" />
            <el-option label="失败" value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="loadMainLog(true)">查询</el-button>
        </el-form-item>
      </el-form>
      <vxe-table v-loading="mainLogLoading" :data="mainLogRows" :height="420" border stripe resizable
        show-overflow="tooltip" style="width: 100%">
        <vxe-table-column field="fId" title="序号" min-width="80" header-align="center" align="center" />
        <vxe-table-column field="vcCode" title="编码" min-width="200" header-align="center" align="center" />
        <vxe-table-column field="vcName" title="名称" min-width="120" header-align="center" align="center" />
        <vxe-table-column field="dBusiBeginDate" title="业务开始日期" min-width="100" header-align="center" align="center" />
        <vxe-table-column field="dBusiEndDate" title="业务结束日期" min-width="100" header-align="center" align="center" />
        <vxe-table-column field="dExecBeginDate" title="开始执行时间" min-width="150" header-align="center" align="center" />
        <vxe-table-column field="dExecEndDate" title="结束执行时间" min-width="150" header-align="center" align="center" />
        <vxe-table-column field="vcRunStatusName" title="运行状态" min-width="100" header-align="center" align="center" />
        <vxe-table-column title="执行结果" min-width="100" header-align="center" align="center">
          <template slot-scope="{ row }">
            <span v-if="row.vcStatus === '0'">执行成功</span>
            <span v-else-if="row.vcStatus === '1'" style="color:#f56c6c">执行失败</span>
            <span v-else>--</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="明细" width="90" fixed="right" header-align="center" align="center">
          <template slot-scope="{ row }">
            <el-button type="text" size="small" @click="openDetailLog(row.fId)">查看</el-button>
          </template>
        </vxe-table-column>
      </vxe-table>
      <vxe-pager class="standard-vxe-pager pagination-bar" :current-page="mainLogPage.pageNum"
        :page-size="mainLogPage.pageSize" :total="mainLogTotal"
        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'Total']" border size="medium"
        @page-change="onMainLogPageChange" />
    </el-dialog>

    <!-- 明细日志 -->
    <el-dialog title="日志明细列表" :visible.sync="detailLogVisible" width="70% !important" append-to-body @open="onDetailLogOpen">
      <el-form :inline="true" size="small" class="log-filter">
        <el-form-item label="产品代码">
          <el-input v-model="detailLogQuery.vcFundCode" clearable style="width: 140px" />
        </el-form-item>
        <el-form-item label="执行结果">
          <el-select v-model="detailLogQuery.vcStatus" clearable placeholder="全部">
            <el-option label="全部" value="" />
            <el-option label="成功" value="0" />
            <el-option label="失败" value="1" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="el-icon-search" @click="loadDetailLog(true)">查询</el-button>
        </el-form-item>
      </el-form>
      <vxe-table v-loading="detailLogLoading" :data="detailLogRows" :height="380" border stripe resizable
        show-overflow="tooltip" style="width: 100%">
        <vxe-table-column field="fId" title="序号" min-width="80" header-align="center" align="center" />
        <vxe-table-column field="vcCode" title="编码" min-width="200" header-align="center" align="center" />
        <vxe-table-column field="vcName" title="名称" min-width="120" header-align="center" align="center" />
        <vxe-table-column field="vcFundCode" title="产品代码" min-width="100" header-align="center" align="center" />
        <vxe-table-column field="dBusiBeginDate" title="业务开始日期" min-width="100" header-align="center" align="center" />
        <vxe-table-column field="dBusiEndDate" title="业务结束日期" min-width="100" header-align="center" align="center" />
        <vxe-table-column field="dExecBeginDate" title="开始执行时间" min-width="150" header-align="center" align="center" />
        <vxe-table-column field="dExecEndDate" title="结束执行时间" min-width="150" header-align="center" align="center" />
        <vxe-table-column title="执行结果" min-width="100" header-align="center" align="center">
          <template slot-scope="{ row }">
            <span v-if="row.vcStatus === '0'">执行成功</span>
            <span v-else-if="row.vcStatus === '1'" style="color:#f56c6c">执行失败</span>
            <span v-else>--</span>
          </template>
        </vxe-table-column>
      </vxe-table>
      <vxe-pager class="standard-vxe-pager pagination-bar" :current-page="detailLogPage.pageNum"
        :page-size="detailLogPage.pageSize" :total="detailLogTotal"
        :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'Total']" border size="medium"
        @page-change="onDetailLogPageChange" />
    </el-dialog>
  </div>
</template>

<script>
import moment from 'moment'
import commonFun from '@/filters/common'
import { getColumnsForIndicator } from './scripts/columns'
import * as api from './scripts/api'
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'

function parseExportFileName(disposition) {
  if (!disposition) return null
  const m = disposition.match(/filename=([^;]+)/i)
  if (!m) return null
  const raw = m[1].trim().replace(/^"+|"+$/g, '')
  try {
    return decodeURIComponent(raw.replace(/\+/g, ' '))
  } catch (e) {
    return raw
  }
}

export default {
  name: 'GfIndicator',
  components: {
    ProductSelectInputMultiple
  },
  data() {
    const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
    const begin = moment(end).startOf('month').format('YYYY-MM-DD')
    return {
      form: {
        dateRange: [begin, end],
        indicatorCode: '',
        fundCodes:[]
      },
      queryRules: {
        dateRange: [{ required: true, message: "请选择日期", trigger: "change" }],
        indicatorCode: [{ required: true, message: '请选择指标类型', trigger: 'change' }],
        fundCodes: [{ required: true, message: '请选择产品', trigger: 'change' }]
      },
      selectedProducts: [],
      indicatorTypes: [],
      tableColumns: [],
      tableData: [],
      tableLoading: false,
      tableHeight: 520,
      pagerConfig: {
        pageSizes: [10, 20, 50, 100]
      },
      pageNum: 1,
      pageSize: 20,
      total: 0,
      sortProp: '',
      sortOrder: '',
      exportLoading: false,
      executeLoading: false,
      mainLogVisible: false,
      mainLogLoading: false,
      mainLogRows: [],
      mainLogTotal: 0,
      mainLogQuery: {
        vcCode: '',
        dExecBeginDate: '',
        dExecEndDate: '',
        vcStatus: ''
      },
      mainLogPage: { pageNum: 1, pageSize: 10 },
      detailLogVisible: false,
      detailLogParentId: '',
      detailLogLoading: false,
      detailLogRows: [],
      detailLogTotal: 0,
      detailLogQuery: {
        vcFundCode: '',
        vcStatus: ''
      },
      detailLogPage: { pageNum: 1, pageSize: 10 },
      pickerOptions: commonFun.dateShortcut(),
      indicatorTabPlaceholder: 'current'
    }
  },
  computed: {
    currentIndicatorName() {
      const t = this.indicatorTypes.find((x) => String(x.dimCde) === String(this.form.indicatorCode))
      return t ? t.dimNme : '指标'
    }
  },
  watch: {
    // 监听选中产品变化，自动更新查询参数
    selectedProducts: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.form.fundCodes = newVal.map((item) => item.VC_FUNDCODE)
        } else {
          this.form.fundCodes = []
        }
      },
      immediate: true
    }
  },
  mounted() {
    this.handleTableHeight()
    this.loadIndicatorTypes()
  },
  beforeDestroy() {
    window.onresize = null
  },
  methods: {
    handleTableHeight() {
      this.$nextTick(() => {
        const el = this.$refs.refsTable && this.$refs.refsTable.$el
        if (el) {
          this.tableHeight = window.innerHeight - el.offsetTop - 165
        }
        window.onresize = () => {
          const t = this.$refs.refsTable && this.$refs.refsTable.$el
          if (t) {
            this.tableHeight = window.innerHeight - t.offsetTop - 165
          }
        }
      })
    },
    loadIndicatorTypes() {
      api.getIndicatorType().then((res) => {
        const raw = res && res.data !== undefined ? res.data : res
        const list = Array.isArray(raw) ? raw : (raw && raw.data) || []
        this.indicatorTypes = list
        if (list.length && !this.form.indicatorCode) {
          this.form.indicatorCode = list[0].dimCde
        }
        this.refreshColumns()
      }).catch(() => {
        this.$message.error('获取指标类型失败')
      })
    },
    refreshColumns() {
      this.tableColumns = getColumnsForIndicator(this.form.indicatorCode)
    },
    onIndicatorChange() {
      this.sortProp = ''
      this.sortOrder = ''
      this.$nextTick(() => {
        if (this.$refs.refsTable) {
          this.$refs.refsTable.clearSort()
        }
      })
      this.refreshColumns()
      this.tableData = []
      this.total = 0
      this.handleSearch(true)
    },
    buildListParams() {
      const [beginDate, endDate] = this.form.dateRange || []
      const params = {
        beginDate,
        endDate,
        indicatorCode: this.form.indicatorCode,
        fundCodes: this.form.fundCodes,
        offset: (this.pageNum - 1) * this.pageSize,
        limit: this.pageSize
      }
      if (this.sortProp && this.sortOrder) {
        params.sort = this.sortProp
        params.order = this.sortOrder
      }
      return params
    },
    handleSearch(resetPage) {
      this.$refs.queryForm.validate((valid) => {
        if (!valid) return
        if (resetPage) this.pageNum = 1
        this.tableLoading = true
        api.fetchIndicatorList(this.buildListParams()).then((res) => {
          this.tableLoading = false
          const { rows, total } = api.parseBootstrapPage(res)
          this.tableData = rows
          this.total = total
        }).catch(() => {
          this.tableLoading = false
          this.tableData = []
          this.total = 0
        })
      })
    },
    onVxeSortChange(val) {
      const orderStr = commonFun.queryOrderBy_vxe_template(val)
      if (!orderStr) {
        this.sortProp = ''
        this.sortOrder = ''
      } else {
        const parts = orderStr.trim().split(/\s+/)
        this.sortProp = parts[0] || ''
        this.sortOrder = (parts[1] || '').toLowerCase()
      }
      this.handleSearch(true)
    },
    pagination(val) {
      const { currentPage, pageSize } = val
      this.pageNum = currentPage
      this.pageSize = pageSize
      this.handleSearch(false)
    },
    handleExport() {
      this.$refs.queryForm.validate((valid) => {
        if (!valid) return
        this.$confirm('确认是否要导出？', '提示', { type: 'warning' }).then(() => {
        const [beginDate, endDate] = this.form.dateRange || []
        const orderString = this.sortProp && this.sortOrder
          ? `${this.sortProp} ${this.sortOrder}`
          : ''
        const params = {
          beginDate,
          endDate,
          indicatorCode: this.form.indicatorCode,
          fundCodes: this.form.fundCodes,
          orderString
        }
        this.exportLoading = true
        api.exportIndicatorList(params).then((res) => {
          this.exportLoading = false
          const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
          const dispo = (res.headers && (res.headers['content-disposition'] || res.headers['Content-Disposition'])) || ''
          const fileName = parseExportFileName(dispo) || `export_${beginDate}_${endDate}.csv`
          const url = window.URL.createObjectURL(blob)
          const a = document.createElement('a')
          a.href = url
          a.download = fileName
          a.click()
          window.URL.revokeObjectURL(url)
        }).catch(() => {
          this.exportLoading = false
          this.$message.error('导出失败')
        })
      }).catch(() => { })
      })
    },
    handleExecuteData() {
      this.$refs.queryForm.validate((valid) => {
        if (!valid) return
        this.$confirm('确定要重跑数据吗?', '提示', { type: 'warning' }).then(() => {
        const [beginDate, endDate] = this.form.dateRange || []
        const params = {
          beginDate,
          endDate,
          indicatorCode: this.form.indicatorCode,
          fundCodes: this.form.fundCodes
        }
        this.executeLoading = true
        api.executeIndicatorData(params).then((res) => {
          this.executeLoading = false
          const body = api.parseApiResult(res)
          if (api.isApiSuccess(body)) {
            this.$message.success(body.message || '执行成功，可在日志列表查看明细')
            this.handleSearch(true)
          } else {
            this.$message.error(body.message || '执行失败')
          }
        }).catch((err) => {
          this.executeLoading = false
          const msg = err && err.response && err.response.data && err.response.data.message
          this.$message.error(msg || '执行失败')
        })
      }).catch(() => { })
      })
    },
    onMainLogOpen() {
      this.mainLogPage.pageNum = 1
      this.loadMainLog(true)
    },
    loadMainLog(reset) {
      if (reset) this.mainLogPage.pageNum = 1
      this.mainLogLoading = true
      const p = {
        ...this.mainLogQuery,
        offset: (this.mainLogPage.pageNum - 1) * this.mainLogPage.pageSize,
        limit: this.mainLogPage.pageSize
      }
      api.queryIndicatorMainLog(p).then((res) => {
        this.mainLogLoading = false
        const { rows, total } = api.parseBootstrapPage(res)
        this.mainLogRows = rows
        this.mainLogTotal = total
      }).catch(() => {
        this.mainLogLoading = false
      })
    },
    onMainLogPageChange({ currentPage, pageSize }) {
      this.mainLogPage.pageNum = currentPage
      this.mainLogPage.pageSize = pageSize
      this.loadMainLog(false)
    },
    openDetailLog(fId) {
      this.detailLogParentId = fId
      this.detailLogVisible = true
    },
    onDetailLogOpen() {
      this.detailLogPage.pageNum = 1
      this.loadDetailLog(true)
    },
    loadDetailLog(reset) {
      if (reset) this.detailLogPage.pageNum = 1
      this.detailLogLoading = true
      const p = {
        fParentId: this.detailLogParentId,
        vcFundCode: this.detailLogQuery.vcFundCode,
        vcStatus: this.detailLogQuery.vcStatus,
        offset: (this.detailLogPage.pageNum - 1) * this.detailLogPage.pageSize,
        limit: this.detailLogPage.pageSize
      }
      api.queryIndicatorDetailLog(p).then((res) => {
        this.detailLogLoading = false
        const { rows, total } = api.parseBootstrapPage(res)
        this.detailLogRows = rows
        this.detailLogTotal = total
      }).catch(() => {
        this.detailLogLoading = false
      })
    },
    onDetailLogPageChange({ currentPage, pageSize }) {
      this.detailLogPage.pageNum = currentPage
      this.detailLogPage.pageSize = pageSize
      this.loadDetailLog(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.gfindicator-page {
  padding: 12px 16px;
}

.table-wrap {
  background: #fff;
}

.pagination-bar {
  margin-top: 12px;
  text-align: right;
}

.log-filter {
  margin-bottom: 10px;
}

.indicator-type-select {
  width: 230px;
}

.indicator-type-select ::v-deep .el-input.el-input--small {
  width: 100% !important;
}

::v-deep .el-tabs__header {
  margin: 0 0 0 0 !important;
}
</style>
