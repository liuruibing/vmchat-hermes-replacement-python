<template>
  <div class="batchExportReport" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <!-- 基础筛选 -->
          <el-row>
            <el-col :span="24">
              <el-form-item label="报告区间">
                <el-date-picker
                  v-model="reportDateRange"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  size="small"
                  unlink-panels
                  range-separator="-"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  style="width: 240px"
                />
              </el-form-item>
              <el-form-item label="报告模板">
                <el-select v-model="formInline.templateId" size="small" clearable filterable placeholder="全部">
                  <el-option v-for="item in templateList" :key="item.fTemplateID" :label="item.vcTemplatEname" :value="item.fTemplateID" />
                </el-select>
              </el-form-item>
              <el-form-item label="产品代码">
                <el-input v-model="formInline.fundCode" size="small" clearable placeholder="请输入" />
              </el-form-item>
              <el-form-item label="产品名称">
                <el-input v-model="formInline.fundName" size="small" clearable placeholder="请输入"  />
              </el-form-item>
              <el-form-item label="服务平台状态">
                <el-select v-model="formInline.reportFwptStatus" size="small" clearable placeholder="全部">
                  <el-option v-for="item in CONSTANTS.REPORT_FWPT_STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 更多筛选 -->
          <el-row v-show="showMoreCondition">
            <el-col :span="24">
              <el-form-item label="创建日期">
                <el-date-picker
                  v-model="createDateRange"
                  type="daterange"
                  value-format="yyyy-MM-dd"
                  size="small"
                  range-separator="-"
                  start-placeholder="开始时间"
                  end-placeholder="结束时间"
                  style="width: 240px"
                />
              </el-form-item>
              <el-form-item label="报告生成状态">
                <el-select v-model="formInline.reportStatus" size="small" clearable placeholder="全部" >
                  <el-option v-for="item in CONSTANTS.REPORT_STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item label="管理人名称">
                <el-input v-model="formInline.glrName" size="small" clearable placeholder="请输入"  />
              </el-form-item>
              <el-form-item label="创建人">
                <el-input v-model="formInline.creatorName" size="small" clearable placeholder="请输入"  />
              </el-form-item>
              <el-form-item label="备注">
                <el-input v-model="formInline.remark" size="small" clearable placeholder="请输入"  />
              </el-form-item>
            </el-col>
          </el-row>

          <el-row v-show="showMoreCondition">
            <el-col :span="24">
              <el-form-item label="执行时间">
                <el-date-picker
                  v-model="execDateRange"
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
                <el-select v-model="formInline.dateStatus" size="small" clearable placeholder="全部" >
                  <el-option v-for="item in CONSTANTS.DATE_STATUS_LIST" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <!-- 操作按钮 -->
          <el-row>
            <el-col :span="24">
              <el-form-item>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.SEARCH'" type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.REPORTDATA'" type="primary" size="small" @click="showMoreCondition = !showMoreCondition">
                  <i :class="showMoreCondition ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  {{ showMoreCondition ? '收起筛选' : '展示更多筛选' }}
                </el-button>

                <el-button v-btn="'BT.BATCHEXPORTREPORT.BATCHDOWN'" type="primary" size="small" icon="el-icon-download" @click="handleBatchDownload">批量下载</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.BATCHADD'" type="primary" size="small" icon="el-icon-plus" @click="openImportDialog">批量新增</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.ADD'" type="primary" size="small" icon="el-icon-plus" @click="openAddDialog">新增</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.BATCHDELTE'" type="primary" size="small" icon="el-icon-delete" @click="handleBatchDelete">批量删除</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.REPORTDATA'" type="primary" size="small" icon="el-icon-caret-right" @click="handleBatchGenerate">批量生成报告</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.BATCHFWPTSHOW'" type="primary" size="small" icon="el-icon-folder-checked" @click="handleBatchFwptShow">批量服务平台展示</el-button>
                <el-button v-btn="'BT.BATCHEXPORTREPORT.BATCHFWPTHIDE'" type="primary" size="small" icon="el-icon-folder-delete"@click="handleBatchFwptHide">批量服务平台隐藏</el-button>
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
          <vxe-table-column type="checkbox" width="60" header-align="center" />
          <vxe-table-column label="操作" align="center" width="450" header-align="center">
            <template slot-scope="{ row }">
              <el-button v-btn="'BT.BATCHEXPORTREPORT.PREVIEW'" type="info" v-if="canPreviewOrDown(row)"  size="small" @click="handlePreview(row)">预览</el-button>
              <el-button v-btn="'BT.BATCHEXPORTREPORT.DOWN'" type="info" v-if="canPreviewOrDown(row)"  size="small" @click="handleDownload(row)">下载</el-button>
              <el-button v-btn="'BT.BATCHEXPORTREPORT.EDIT'" type="info" size="small" @click="openEditDialog(row)">修改</el-button>
              <el-button v-btn="'BT.BATCHEXPORTREPORT.DELETE'" type="info" size="small" @click="handleDelete(row)">删除</el-button>
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

          <!-- 隐藏列：visible:false -->
          <vxe-table-column field="benchmarks" title="基准类型" :visible="false"></vxe-table-column>
          <vxe-table-column field="benchmarkA" title="基准A" :visible="false"></vxe-table-column>
          <vxe-table-column field="benchmarkAValue" title="基准A权重" :visible="false"></vxe-table-column>
          <vxe-table-column field="benchmarkB" title="基准B" :visible="false"></vxe-table-column>
          <vxe-table-column field="benchmarkBValue" title="基准B权重" :visible="false"></vxe-table-column>
          <vxe-table-column field="industryType" title="行业类型" :visible="false"></vxe-table-column>
          <vxe-table-column field="factorType" title="因子类型" :visible="false"></vxe-table-column>

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

    <!-- 新增/编辑弹框 -->
    <el-dialog :title="editDialog.isEdit ? '编辑报告' : '新增报告'" :visible.sync="editDialog.visible" width="55%" :close-on-click-modal="false">
      <el-form :model="editDialog.form" label-width="120px">
        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item label="报告模板" required>
              <el-select v-model="editDialog.form.templateId" size="small" filterable placeholder="请选择" @change="handleTemplateChange">
                <el-option v-for="item in templateList" :key="item.fTemplateID" :label="item.vcTemplatEname" :value="item.fTemplateID" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="备注">
              <el-input v-model="editDialog.form.remark" size="small" clearable />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item label="报告开始日期" required>
              <el-date-picker v-model="editDialog.form.beginDate" type="date" value-format="yyyy-MM-dd" size="small" placeholder="请选择" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="报告结束日期" required>
              <el-date-picker v-model="editDialog.form.endDate" type="date" value-format="yyyy-MM-dd" size="small" placeholder="请选择" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item label="脱敏标志">
              <el-select v-model="editDialog.form.desensitizationFlag" size="small" clearable placeholder="请选择">
                <el-option v-for="item in CONSTANTS.DESENSITIZATION_FLAG_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="脱敏方法">
              <el-select
                v-model="editDialog.form.desensitizationFun"
                size="small"
                clearable
                placeholder="请选择"
                :disabled="editDialog.form.desensitizationFlag !== 'true'"
              >
                <el-option v-for="item in CONSTANTS.DESENSITIZATION_FUN_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item label="行业类型">
              <el-select v-model="editDialog.form.industryType" size="small" clearable placeholder="请选择">
                <el-option v-for="item in CONSTANTS.INDUSTRY_TYPE_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="因子类型">
              <el-select
                v-model="editDialog.form.factorType"
                size="small"
                clearable
                placeholder="请选择"
              >
                <el-option v-for="item in CONSTANTS.FACTOR_TYPE_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="10">
          <el-col :span="12">
            <el-form-item label="频率">
              <el-select v-model="editDialog.form.dataFreq" size="small" clearable placeholder="请选择">
                <el-option v-for="item in CONSTANTS.DATA_FREQ_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>

          <el-col :span="12">
            <el-form-item label="基准类型">
              <el-select
                v-model="editDialog.form.benchmarks"
                size="small"
                clearable
                placeholder="请选择"
              >
                <el-option v-for="item in CONSTANTS.BENCH_TYPE_LIST" :key="item.value" :label="item.label" :value="item.value" />
              </el-select>
            </el-form-item>
          </el-col>



        </el-row>
        <el-row :gutter="10">
        <div v-show="editDialog.form.benchmarks == '1'" style="display: inline-block">
          <el-form-item label="选择基准">
            <el-select v-model="editDialog.form.benchmarkA" placeholder="请选择" size="small" filterable>
              <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
        </div>
        </el-row>
        <div v-show="editDialog.form.benchmarks == '2'" style="display: inline-block">
        <el-row :gutter="10">
          <el-col :span="12">
          <el-form-item label="基准 A">
            <el-select v-model="editDialog.form.benchmarkA" placeholder="请选择" size="small" filterable>
              <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          </el-col>
          <el-col :span="12">
          <el-form-item label="比例">
            <el-input v-model="editDialog.form.benchmarkAValue" size="small" style="width: 85px !important"></el-input>%
          </el-form-item>
          </el-col>

        </el-row>

        <el-row :gutter="10">
          <el-col :span="12">
          <el-form-item label="基准 B">
            <el-select v-model="editDialog.form.benchmarkB" placeholder="请选择" size="small" filterable>
              <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
            </el-select>
          </el-form-item>
          </el-col>
          <el-col :span="12">
          <el-form-item label="比例">
            <el-input v-model="editDialog.form.benchmarkBValue" size="small" style="width: 85px !important" ></el-input>%
          </el-form-item>
          </el-col>

        </el-row>
        </div>
        <el-form-item v-if="!editDialog.isEdit" label="产品代码(多条)" required>
          <el-input v-model="editDialog.fundCodesText" type="textarea" :rows="4" placeholder="输入多个产品代码，逗号/空格/换行分隔" />
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="editDialog.visible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="editDialog.loading" @click="submitEditDialog">保存</el-button>
      </span>
    </el-dialog>

    <!-- 批量导入弹框 -->
    <el-dialog title="批量导入" :visible.sync="importDialog.visible" width="45%" :close-on-click-modal="false" @close="handleDialogClose">
      <div style="margin-bottom: 10px;">
        <el-button size="small" type="primary" @click="downloadImportExample">导入模板下载</el-button>
        <el-button size="small" type="primary" @click="downloadTemplateReport">报告模板清单下载</el-button>
      </div>

      <el-upload  ref="uploadRef" action="" :auto-upload="false" :show-file-list="true" :on-change="handleImportFileChange" accept=".xls,.xlsx">
        <el-button size="small" type="primary">选择文件</el-button>
        <div slot="tip" class="el-upload__tip">仅支持 .xls/.xlsx</div>
      </el-upload>

      <span slot="footer" class="dialog-footer">
        <el-button size="small" @click="importDialog.visible = false">取消</el-button>
        <el-button type="primary" size="small" :loading="importDialog.loading" @click="submitImport">上传</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import CONSTANTS from './js/constants'
import commonFun from '@/filters/common'
import pageApi from './js/api'
import store from '@/store'

export default {
  name: 'BathExportReport',
  data() {
    return {
      CONSTANTS,
      formInline: {
        beginDate: '',
        endDate: '',
        templateId: '',
        fundCode: '',
        fundName: '',
        reportFwptStatus: '',
        createBeginDate: '',
        createEndDate: '',
        reportStatus: '',
        glrName: '',
        creatorName: '',
        remark: '',
        execBeginDate: '',
        execEndDate: '',
        reportResult: '',
        reportPdfValid: '',
        dateStatus: '',
        orderString: 'createDate desc',
        pageSize: 20,
        pageNum: 1
      },
      tableColumns: [],
      reportDateRange: null,
      createDateRange: null,
      execDateRange: null,
      showMoreCondition: false,
      tableHeight: 0,
      tableLoading: false,
      tableData: [],
      total: 0,
      templateList: [],
      pagerConfig: { pageSizes: [10, 20, 50, 100, 500, 10000] },
      editDialog: {
        visible: false,
        isEdit: false,
        loading: false,
        fundCodesText: '',
        form: {
          fileId: '',
          fundCode:'',
          templateId: '',
          templateName: '',
          beginDate: '',
          endDate: '',
          remark: '',
          desensitizationFlag: 'false',
          desensitizationFun: '',
          benchmarks:'1',      //基准类型 0 无基准 1  单基准  2 复合基准
          benchmarkA:'000300', //基准A
          benchmarkAValue:'0.0000', //基准A权重
          benchmarkB:'000300',    //基准B
          benchmarkBValue:'0.0000',  //基准B权重
          industryType:'SWSR',  //行业类型，SWSR 申万一级行业  ZXSR 中信一级行业
          factorType:'CNE5',   //因子类型  CNE5 和CNE6
          dataFreq:'1',//数据频率 1 日频 2 周频 3 月频
        }
      },
      importDialog: {
        visible: false,
        loading: false,
        file: null
      }
    }
  },
  computed: {
  },
  mounted() {
    this.initData()
  },
  beforeDestroy() {
    window.onresize = null
  },
  methods: {
    initData() {
      this.initColumns()
      this.handleTableHeight()
      this.fetchTemplateList()
      this.handleSearchTable(true)
    },
    initColumns(){
      let arr = store.state.btnData.filter(item => item === 'BT.BATCHEXPORTREPORT.REPORTDATA');
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
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] !== '' && data[key] !== undefined && data[key] !== null && JSON.stringify(data[key]) !== '[]') {
          newData[key] = data[key]
        }
      }
      return newData
    },
    handleSearchTable(resetPage) {
      if (resetPage) this.formInline.pageNum = 1

      const params = { ...this.formInline }
      if (this.reportDateRange && this.reportDateRange.length === 2) {
        params.beginDate = this.reportDateRange[0]
        params.endDate = this.reportDateRange[1]
      }
      if (this.createDateRange && this.createDateRange.length === 2) {
        params.createBeginDate = this.createDateRange[0]
        params.createEndDate = this.createDateRange[1]
      }
      if (this.execDateRange && this.execDateRange.length === 2) {
        params.execBeginDate = this.execDateRange[0]
        params.execEndDate = this.execDateRange[1]
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

      this.tableLoading = true
      pageApi.doBatchExportReportList(this.parameterSrc(params)).then((res) => {
        this.tableLoading = false
        const data = res.data || res
        this.tableData = data.rows || data.list || []
        this.total = data.total || 0
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
    canPreviewOrDown(row) {
      return row.reportStatus === '1' && row.reportResult === '0' && row.reportPdfValid === '1'
    },
    handlePreview(row) {
      if (!row.fileId) return this.$message.warning('文件ID不能为空')
      window.open(pageApi.getPreviewPdfUrl(row.fileId), '_blank')
    },
    handleDownload(row) {
      if (!row.fileId) return this.$message.warning('下载文件的ID不能为空')
      pageApi.downLoadPdf(row.fileId).then((res) => {
        const blob = new Blob([res.data], { type: 'application/pdf' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = (row.reportFileName && !row.reportFileName.endsWith('.pdf')) ? row.reportFileName + '.pdf' : (row.reportFileName || 'report.pdf')
        a.click()
        window.URL.revokeObjectURL(url)
      })
    },
    handleBatchDownload() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) return this.$message.warning('请选择导出行')
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      if (!fileIds) return this.$message.warning('所选行没有可下载的文件')
      pageApi.batchDownLoadPdf(fileIds).then((res) => {
        const blob = new Blob([res.data], { type: 'application/zip' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '批量报告.zip'
        a.click()
        window.URL.revokeObjectURL(url)
      })
    },
    handleDelete(row) {
      if (!row.fileId) return this.$message.warning('文件ID不能为空')
      this.$confirm(`确定删除文件ID为 [ ${row.fileId} ] 的记录？`, '提示', { type: 'warning' })
        .then(() => pageApi.deleteExportReport(row.fileId))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('删除成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '删除失败，请重试')
          }
        })
        .catch(() => {})
    },
    handleBatchDelete() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) return this.$message.warning('请选择删除行')
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      this.$confirm('确定批量删除选中的记录？', '提示', { type: 'warning' })
        .then(() => pageApi.deleteBatchExportReport(fileIds))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('批量删除成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '批量删除失败，请重试')
          }
        })
        .catch(() => {})
    },
    handleBatchGenerate() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) return this.$message.warning('请选择行')
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      this.$confirm('确定批量生成选中记录的报告？', '提示', { type: 'warning' })
        .then(() => pageApi.executeBatchExportReportData(fileIds))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('批量报告生成成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '批量生成失败，请重试')
          }
        })
        .catch(() => {})
    },
    handleBatchFwptShow() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) return this.$message.warning('请选择行')
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      this.$confirm('确定批量选中的记录，在服务平台上显示？', '提示', { type: 'warning' })
        .then(() => pageApi.addBatchFwptRecordShow(fileIds))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('批量显示状态修改成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '批量显示状态修改失败，请重试')
          }
        })
        .catch(() => {})
    },
    handleBatchFwptHide() {
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) return this.$message.warning('请选择行')
      const fileIds = list.map(r => r.fileId).filter(Boolean).join(',')
      this.$confirm('确定批量选中的记录，在服务平台上隐藏？', '提示', { type: 'warning' })
        .then(() => pageApi.addBatchFwptRecordHide(fileIds))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('批量隐藏状态修改成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '批量隐藏状态修改失败，请重试')
          }
        })
        .catch(() => {})
    },
    openAddDialog() {
      this.editDialog.isEdit = false
      this.editDialog.loading = false
      this.editDialog.fundCodesText = ''
      this.editDialog.form = {
        fileId: '',
        fundCode:'',
        templateId: '',
        templateName: '',
        beginDate: '',
        endDate: '',
        remark: '',
        desensitizationFlag: 'false',
        desensitizationFun: '',
        benchmarks:'1',      //基准类型 0 无基准 1  单基准  2 复合基准
        benchmarkA:'000300', //基准A
        benchmarkAValue:'0.0000', //基准A权重
        benchmarkB:'000300',    //基准B
        benchmarkBValue:'0.0000',  //基准B权重
        industryType:'SWSR',  //行业类型，SWSR 申万一级行业  ZXSR 中信一级行业
        factorType:'CNE5',   //因子类型  CNE5 和CNE6
        dataFreq:'1'   //频率  1 日频 2 周频 3 月频
      }
      this.editDialog.visible = true
    },
    openEditDialog(row) {
      this.editDialog.isEdit = true
      this.editDialog.loading = false
      this.editDialog.fundCodesText = ''
      this.editDialog.form = {
        fileId: row.fileId,
        fundCode:row.fundCode|| '',
        templateId: row.templateId || '',
        templateName: row.templateName || '',
        beginDate: row.beginDate || '',
        endDate: row.endDate || '',
        remark: row.remark || '',
        desensitizationFlag: row.desensitizationFlag || 'false',
        desensitizationFun: row.desensitizationFun || '',
        benchmarks:row.benchmarks || '',      //基准类型 0 无基准 1  单基准  2 复合基准
        benchmarkA:row.benchmarkA || '', //基准A
        benchmarkAValue:row.benchmarkAValue || '', //基准A权重
        benchmarkB:row.benchmarkB || '',    //基准B
        benchmarkBValue:row.benchmarkBValue || '',  //基准B权重
        industryType:row.industryType || '',  //行业类型，SWSR 申万一级行业  ZXSR 中信一级行业
        factorType:row.factorType || '' ,  //因子类型  CNE5 和CNE6
        dataFreq:row.dataFreq || ''  //频率  1 日频 2 周频 3 月频
      }
      this.editDialog.visible = true
    },
    handleTemplateChange(val) {
      const item = this.templateList.find(t => t.fTemplateID === val)
      this.editDialog.form.templateName = item ? item.vcTemplatEname : ''
    },
    parseFundCodes(text) {
      if (!text) return []
      return text.split(/[\s,，]+/g).map(s => s.trim()).filter(Boolean)
    },
    submitEditDialog() {
      const f = this.editDialog.form
      if (!f.templateId) return this.$message.warning('请选择报告模板')
      if (!f.beginDate || !f.endDate) return this.$message.warning('请选择报告开始/结束日期')
      if (f.benchmarks==="2" && (Number(f.benchmarkAValue) + Number(f.benchmarkBValue) > 100)) return this.$message.warning('基金A、B权重不能超过100%')
      this.editDialog.loading = true
      if (this.editDialog.isEdit) {
        pageApi.doExportReportEdit({
          fileId: f.fileId,
          templateId: f.templateId,
          templateName: f.templateName,
          beginDate: f.beginDate,
          endDate: f.endDate,
          remark: f.remark,
          fundCode:f.fundCode,
          desensitizationFlag: f.desensitizationFlag,
          desensitizationFun: f.desensitizationFun,
          benchmarks:f.benchmarks,      //基准类型 0 无基准 1  单基准  2 复合基准
          benchmarkA:f.benchmarkA, //基准A
          benchmarkAValue:f.benchmarkAValue, //基准A权重
          benchmarkB:f.benchmarkB,    //基准B
          benchmarkBValue:f.benchmarkBValue,  //基准B权重
          industryType:f.industryType,  //行业类型，SWSR 申万一级行业  ZXSR 中信一级行业
          factorType:f.factorType,   //因子类型  CNE5 和CNE6
          dataFreq:f.dataFreq
        }).then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('保存成功')
            this.editDialog.visible = false
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '保存失败')
          }
        }).finally(() => {
          this.editDialog.loading = false
        })
      } else {
        const fundcodes = this.parseFundCodes(this.editDialog.fundCodesText)
        if (!fundcodes.length) {
          this.editDialog.loading = false
          return this.$message.warning('请输入至少一个产品代码')
        }
        pageApi.doExportReportAdd({
          templateId: f.templateId,
          templateName: f.templateName,
          beginDate: f.beginDate,
          endDate: f.endDate,
          remark: f.remark,
          desensitizationFlag: f.desensitizationFlag,
          desensitizationFun: f.desensitizationFun,
          fundCodes:fundcodes,
          benchmarks:f.benchmarks,      //基准类型 0 无基准 1  单基准  2 复合基准
          benchmarkA:f.benchmarkA, //基准A
          benchmarkAValue:f.benchmarkAValue, //基准A权重
          benchmarkB:f.benchmarkB,    //基准B
          benchmarkBValue:f.benchmarkBValue,  //基准B权重
          industryType:f.industryType,  //行业类型，SWSR 申万一级行业  ZXSR 中信一级行业
          factorType:f.factorType,   //因子类型  CNE5 和CNE6
          dataFreq:f.dataFreq

        }).then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 0) {
            this.$message.success('新增成功')
            this.editDialog.visible = false
            this.handleSearchTable(true)
          } else {
            this.$message.error(data.message || '新增失败')
          }
        }).finally(() => {
          this.editDialog.loading = false
        })
      }
    },
    openImportDialog() {
      this.importDialog.visible = true
      this.importDialog.loading = false
      this.importDialog.file = null
    },
    handleImportFileChange(file) {
      this.importDialog.file = file.raw
    },
    submitImport() {
      if (!this.importDialog.file) return this.$message.warning('请选择文件')
      this.importDialog.loading = true
      pageApi.importExportReportUpload(this.importDialog.file).then((res) => {
        const data = res.data || res
        const result = data.result || {}
        const ok = result.messageCode === '1' || result.messageCode === 1
        if (ok) {
          this.$message.success(result.message || '上传成功')
          this.importDialog.visible = false
          this.handleSearchTable(true)
        } else {
          this.$message.error(result.message || '上传失败')
        }
      }).finally(() => {
        this.importDialog.loading = false
      })
    },
    downloadImportExample() {
      pageApi.downLoadImportExample().then((res) => {
        const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '导入模板.xls'
        a.click()
        window.URL.revokeObjectURL(url)
      })
    },
    downloadTemplateReport() {
      pageApi.downLoadTemplateReport().then((res) => {
        const blob = new Blob([res.data], { type: 'application/vnd.ms-excel' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = '报告模板.xls'
        a.click()
        window.URL.revokeObjectURL(url)
      })
    },
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.editDialog.form.benchmarkAValue)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.editDialog.form.benchmarkAValue = '0.0000'
          return
        }
        if (this.editDialog.form.benchmarkBValue != '') {
          if (Number(this.editDialog.form.benchmarkAValue) + Number(this.editDialog.form.benchmarkBValue) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100%')
            this.editDialog.form.benchmarkAValue = '0'
          } else {
            this.editDialog.form.benchmarkAValue = '' + Number(this.editDialog.form.benchmarkBValue).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.editDialog.form.benchmarkBValue)) {
          this.$message.closeAll()
          this.$message.warning('只能输入大于等于0的数')
          this.editDialog.form.benchmarkBValue = '0.0000'
          return
        }
        if (this.editDialog.form.benchmarkAValue != '') {
          if (Number(this.editDialog.form.benchmarkAValue) + Number(this.editDialog.form.benchmarkBValue) > 100) {
            this.$message.closeAll()
            this.$message.warning('基金A、B权重不能超过100')
            this.editDialog.form.benchmarkBValue = '0'
          } else {
            this.editDialog.form.benchmarkBValue = '' + Number(this.editDialog.form.benchmarkBValue).toFixed(4)
          }
        }
      }
    },

    handleDialogClose() {
      // 关键：清空上传组件的文件列表
      if (this.$refs.uploadRef) {
        this.$refs.uploadRef.clearFiles();
      }
    },
  }
}
</script>

<style lang="scss" scoped>
.batchExportReport {
  .dd-style-table {
    padding: 10px 0;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>
