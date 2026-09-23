<template>
  <div class="batchReportSubscription" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <!-- 第一行：基础筛选 -->
          <el-row>
            <el-col :span="24">
              <el-form-item label="执行时间">
                <el-date-picker
                  v-model="execDateRange"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  align="left"
                  size="small"
                  unlink-panels
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  popper-class="popperDateShortTP"
                  style="width: 240px"
                />
              </el-form-item>
              <el-form-item label="执行状态">
                <el-select v-model="formInline.status" size="small" clearable placeholder="全部">
                  <el-option v-for="item in CONSTANTS.STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item label="产品代码">
                <el-input v-model="formInline.fundCode" size="small" placeholder="请输入" clearable />
              </el-form-item>
              <el-form-item label="产品名称">
                <el-input v-model="formInline.fundName" size="small" placeholder="请输入" clearable  />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 第二行：更多筛选（可折叠） -->
          <el-row v-show="showMoreCondition">
            <el-col :span="24">
              <el-form-item label="报告区间">
                <el-date-picker
                  v-model="reportDateRange"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  size="small"
                  range-separator="-"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  style="width: 240px"
                />
              </el-form-item>
              <el-form-item label="报告生成状态">
                <el-select v-model="formInline.reportStatus" size="small" clearable placeholder="全部">
                  <el-option v-for="item in CONSTANTS.REPORT_STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item label="报告模板">
                <el-select v-model="formInline.templateId" size="small" clearable filterable placeholder="全部" >
                  <el-option v-for="item in templateList" :key="item.fTemplateID" :label="item.vcTemplatEname" :value="item.fTemplateID" />
                </el-select>
              </el-form-item>
              <el-form-item label="管理人名称">
                <el-input v-model="formInline.glrName" size="small" placeholder="请输入" clearable  />
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 第三行：更多筛选-服务平台相关 -->
          <el-row v-show="showMoreCondition">
            <el-col :span="24">
              <el-form-item label="服务平台生成日期">
                <el-date-picker
                  v-model="fwptDateRange"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  size="small"
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  style="width: 240px"
                />
              </el-form-item>
              <el-form-item label="报告结果状态">
                <el-select v-model="formInline.reportResult" size="small" clearable placeholder="全部" >
                  <el-option v-for="item in CONSTANTS.REPORT_RESULT_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item label="文件状态">
                <el-select v-model="formInline.reportPdfValid" size="small" clearable placeholder="全部" >
                  <el-option v-for="item in CONSTANTS.REPORT_PDF_VALID_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item label="日期状态">
                <el-select v-model="formInline.dateStatus" size="small" clearable placeholder="全部">
                  <el-option v-for="item in CONSTANTS.DATE_STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 第四行：操作按钮 -->
          <el-row>
            <el-col :span="24">
              <el-form-item>
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.SEARCH'" type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.SEARCH'" type="primary" size="small" @click="showMoreCondition = !showMoreCondition">
                  <i :class="showMoreCondition ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  {{ showMoreCondition ? '收起筛选' : '展示更多筛选' }}
                </el-button>
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.BATCHDOWN'" type="primary" size="small" icon="el-icon-download" @click="handleBatchDownload">批量下载</el-button>
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.REPORTDATA'" type="primary" size="small" icon="el-icon-refresh" @click="handleRegenerateReport">重新生成报告</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :checkbox-config="{ checkStrictly: false }"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          :sort-config="{ remote: true }"
          @sort-change="customSortMethod"
          resizable
        >
          <vxe-table-column header-align="center" type="checkbox" width="60" />
          <vxe-table-column header-align="center" label="操作" align="left" width="220">
            <template slot-scope="{ row }">
              <span v-if="canShowOperate(row)">
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.PREVIEW'" type="info" size="small" @click="handlePreview(row)">预览</el-button>
                <el-button v-btn="'BT.BATCHREPORTSUBSCRIPTION.DOWN'" type="info" size="small" @click="handleDownload(row)">下载</el-button>
              </span>
              <span v-else>-</span>
            </template>
          </vxe-table-column>
          <vxe-table-column
            v-for="item in tableColumns"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            :min-width="item.width"
            header-align="center"
            sortable
          >
            <template slot-scope="{ row }">
              <span v-if="item.prop === 'desensitizationFlag'">{{ row.desensitizationFlag === 'true' ? '脱敏' : '不脱敏' }}</span>
              <span v-else-if="item.prop === 'desensitizationFun'">
                {{ row.desensitizationFlag === 'false' ? '-' : (row.desensitizationFun === 'ALL' ? '不显示名称、代码' : '仅屏蔽部分字符') }}
              </span>
              <span v-else>{{ row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formInline.pageNum"
          :page-size="formInline.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          :page-sizes="pagerConfig.pageSizes"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </div>
  </div>
</template>

<script>
import CONSTANTS from './js/constants'
import commonFun from '@/filters/common'
import pageApi from './js/api.js'
import store from '@/store'

export default {
  name: 'BatchReportSubscription',
  data() {
    return {
      CONSTANTS,
      formInline: {
        execBeginDate: '',
        execEndDate: '',
        status: '0',
        fundCode: '',
        fundName: '',
        beginDate: '',
        endDate: '',
        reportStatus: '',
        templateId: '',
        glrName: '',
        fwptUpdateBeginDate: '',
        fwptUpdateEndDate: '',
        reportResult: '',
        reportPdfValid: '',
        dateStatus: '',
        orderString: 'fyptUpdateDate desc',
        pageSize: 20,
        pageNum: 1
      },
      tableColumns: [],
      execDateRange: null,
      reportDateRange: null,
      fwptDateRange: null,
      showMoreCondition: false,
      tableHeight: 0,
      tableLoading: false,
      tableData: [],
      total: 0,
      templateList: [], // 报告模板列表，可从 batchReportSubscriptionInit 或独立接口获取
      pagerConfig: {
        pageSizes: [10, 20, 50, 100, 500, 10000]
      },
    }
  },
  computed: {
  },
  mounted() {
    this.initData()
  },
  methods: {
    initData() {
      this.initColumns()
      this.handleTableHeight()
      this.initDefaultDateRange()
      this.fetchTemplateList()
      this.handleSearchTable(true)
    },
    initColumns(){
      let arr = store.state.btnData.filter(item => item === 'BT.BATCHREPORTSUBSCRIPTION.REPORTDATA');
      if(arr.length == 0){
        this.tableColumns = CONSTANTS.TABLE_COLUMNS
      }else{
        this.tableColumns = [...CONSTANTS.TABLE_COLUMNS, ...CONSTANTS.TABLE_COLUMNS_EXTEND]
      }
    },
    fetchTemplateList() {
      pageApi.getTemplateList({ limit: 9999, offset: 0 }).then((res) => {
        const data = res.data || res
        const rows = data.data || []
        this.templateList = Array.isArray(rows) ? rows : []
      }).catch(() => {
        this.templateList = []
      })
    },
    initDefaultDateRange() {
      const now = new Date()
      const oneMonthAgo = new Date(now)
      oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 12)
      this.fwptDateRange = [this.formatDate(oneMonthAgo), this.formatDate(now)]
    },
    formatDate(d) {
      const y = d.getFullYear()
      const m = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      return `${y}-${m}-${day}`
    },
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] !== '' && data[key] !== undefined && data[key] !== null && JSON.stringify(data[key]) !== '[]') {
          newData[key] = data[key]
        }
      }
      return newData
    },
    handleTableHeight() {
      this.$nextTick(() => {
        if (this.$refs.refsTable && this.$refs.refsTable.$el) {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
        window.onresize = () => {
          if (this.$refs.refsTable && this.$refs.refsTable.$el) {
            this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
          }
        }
      })
    },
    handleSearchTable(flag) {
      if (flag) {
        this.formInline.pageNum = 1
      }
      const params = { ...this.formInline }
      if (this.execDateRange && this.execDateRange.length === 2) {
        params.execBeginDate = this.execDateRange[0]
        params.execEndDate = this.execDateRange[1]
      }
      if (this.reportDateRange && this.reportDateRange.length === 2) {
        params.beginDate = this.reportDateRange[0]
        params.endDate = this.reportDateRange[1]
      }
      if (this.fwptDateRange && this.fwptDateRange.length === 2) {
        params.fwptUpdateBeginDate = this.fwptDateRange[0]
        params.fwptUpdateEndDate = this.fwptDateRange[1]
      }
      params.limit = this.formInline.pageSize
      params.offset = (this.formInline.pageNum - 1) * this.formInline.pageSize
      if (this.formInline.orderString) {
        const parts = this.formInline.orderString.trim().split(/\s+/)
        if (parts.length >= 2) {
          params.sort = parts[0]
          params.order = parts[1]
        }
      }
      const cleanParams = this.parameterSrc(params)
      this.tableLoading = true
      pageApi.doReportSubscriptionList(cleanParams).then((res) => {
        this.tableLoading = false
        const data = res.data || res
        if (data.rows !== undefined) {
          this.tableData = data.rows || []
          this.total = data.total || 0
        } else if (data.list !== undefined) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
        }
      }).catch(() => {
        this.tableLoading = false
        this.tableData = []
        this.total = 0
      })
    },
    pagination(val) {
      const { currentPage, pageSize } = val
      this.formInline.pageNum = currentPage
      this.formInline.pageSize = pageSize
      this.handleSearchTable(false)
    },
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template ? commonFun.queryOrderBy_vxe_template(val) : ''
      this.handleSearchTable(false)
    },
    canShowOperate(row) {
      return true;
      // return row.reportStatus === '1' && row.reportResult === '0' && row.reportPdfValid === '1'
    },
    handlePreview(row) {
      if (!row.fileId) {
        this.$message.warning('文件ID不能为空')
        return
      }
      const url = pageApi.getPreviewPdfUrl(row.fileId)
      window.open(url, '_blank')
    },
    handleDownload(row) {
      if (!row.fileId) {
        this.$message.warning('下载文件的ID不能为空')
        return
      }
      pageApi.downLoadPdf(row.fileId).then((res) => {
        const blob = new Blob([res.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = (row.reportFileName && !row.reportFileName.endsWith('.pdf')) ? row.reportFileName + '.pdf' : (row.reportFileName || 'report.pdf')
        a.click()
        window.URL.revokeObjectURL(url)
        this.$message.success('下载成功')
      }).catch(() => {
        this.$message.error('下载失败')
      })
    },
    handleBatchDownload() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (list.length < 1) {
        this.$message.warning('请选择导出行')
        return
      }
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      if (!fileIds) {
        this.$message.warning('所选行没有可下载的文件')
        return
      }
      pageApi.batchDownLoadPdf(fileIds).then((res) => {
        const blob = new Blob([res.data], { type: 'application/zip' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '批量报告.zip'
        a.click()
        window.URL.revokeObjectURL(url)
        this.$message.success('下载成功')
      }).catch(() => {
        this.$message.error('批量下载失败')
      })
    },
    handleRegenerateReport() {
      const rows = this.$refs.refsTable.getCheckboxRecords() || []
      if (rows.length === 0) {
        this.$message.warning('请选择要重新生成报告的数据')
        return
      }
      const fileIds = rows.map(item => item.fileId);
      this.$confirm('确定根据服务平台生成日期重新生成报告？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const params = {
          fileIds,
          fwptUpdateBeginDate: this.fwptDateRange && this.fwptDateRange[0] ? this.fwptDateRange[0] : '',
          fwptUpdateEndDate: this.fwptDateRange && this.fwptDateRange[1] ? this.fwptDateRange[1] : '',
          execBeginDate: this.execDateRange && this.execDateRange[0] ? this.execDateRange[0] : '',
          execEndDate: this.execDateRange && this.execDateRange[1] ? this.execDateRange[1] : '',
          status: this.formInline.status
        }
        pageApi.executeBatchReportSubscriptionData(params).then((res) => {
          const data = res.data || res
          if (data.status === 200) {
            this.$message.success('批量报告重新生成成功')
            this.handleSearchTable(true)
          } else {
            this.$message.error(data.resultMsg || '批量报告重新生成失败，请重试')
          }
        }).catch(() => {
          this.$message.error('操作失败')
        })
      }).catch(() => {})
    },
    beforeDestroy() {
      window.onresize = null
    }
  }
}
</script>

<style lang="scss" scoped>
.batchReportSubscription {
  .dd-style-table {
    padding: 10px 0;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .el-button.el-button--mini {
    padding: 7px !important;
  }
}
</style>
