<template>
  <div class="custom-report-temp-manage">
    <!-- 搜索 -->
    <el-form :inline="true" ref="queryForm" :model="queryForm" label-width="auto" class="standard-form">
      <el-row>
        <el-col :span="24">
          <el-form-item prop="templateName">
            <el-input v-model.trim="queryForm.templateName" clearable placeholder="请输入模板名称" size="small"></el-input>
          </el-form-item>
          <el-form-item prop="vcTempType">
            <el-select v-model="queryForm.vcTempType" clearable placeholder="请选择模板类型" size="small">
              <el-option label="标准模板" value="0"></el-option>
              <el-option label="自定义模板" value="1"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="onQuery" class="mb5" icon="el-icon-search"
              :loading="loading">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh" @click="handleReset('queryForm')"
              :disabled="loading">重置</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="onAddTemp"
              :disabled="loading">新增</el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <!-- 列表展示 -->
    <div class="custom-report-temp-manage-table" id="standard-table">
      <vxe-table v-loading="loading" :data="tableData" height="auto" stripe auto-resize sync-resize resizable
        show-overflow show-header-overflow highlight-hover-rows header-align="center" @sort-change="handleSortChange"
        :sort-config="{ remote: true }">
        <!-- <vxe-table-column type="checkbox" width="60" align="center"></vxe-table-column> -->
        <vxe-table-column type="seq" title="序号" width="60" align="center"></vxe-table-column>
        <vxe-table-column field="vcTemplatEname" title="模板名称" min-width="120"></vxe-table-column>
        <vxe-table-column field="vcTempType" title="模板类型" min-width="120" align="center">
          <template slot-scope="{ row }">
            <span v-if="row.vcTempType == '1'">自定义模板</span>
            <span v-if="row.vcTempType == '0'">标准模板</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="fCreateID" title="创建人" min-width="120" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.fCreateID || '-' }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="dCreateTime" title="创建时间" min-width="120" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.dCreateTime || '-' }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="fUpdateID" title="修改人" min-width="120" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.fUpdateID || '-' }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="dUpdateTime" title="修改时间" min-width="120" align="center">
          <template slot-scope="{ row }">
            <span>{{ row.dUpdateTime || '-' }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="操作" width="440" align="center">
          <template slot-scope="{ row }">
            <span class="table-operation">
              <!-- <el-dropdown @command="(command) => handleCommand(command, row)" style="margin-right: 8px">
                <el-button type="info" plain size="small">
                  编辑
                  <i class="el-icon-arrow-down el-icon--right"></i>
                </el-button>
                <el-dropdown-menu slot="dropdown">
                  <el-dropdown-item command="2">编辑模板</el-dropdown-item>
                  <el-dropdown-item command="3">复制新增</el-dropdown-item>
                </el-dropdown-menu>
              </el-dropdown> -->
              <el-button :disabled="btnDisabled" type="info" plain size="small" @click="getInfo(row, '2')"
                v-if="row.vcTempType == '1'">编辑</el-button>
              <el-button :disabled="btnDisabled" type="info" plain size="small"
                @click="getInfo(row, '3')">复制</el-button>
              <el-button :disabled="btnDisabled" type="info" plain size="small"
                @click="getInfo(row, '4')">预览</el-button>
              <el-button :disabled="btnDisabled" type="info" plain size="small"
                @click="handleView(row)">查看报告</el-button>
              <el-button :disabled="btnDisabled" type="info" plain size="small" @click="deleteRow(row)"
                v-if="row.vcTempType == '1'">删除</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <Pagination :total="total" :limit="PageSize" :page="CurrentPage" @pagination="pagination"></Pagination>

    <!-- 弹窗配置 -->
    <el-dialog :title="ReportTempConfigModelTitle" :visible.sync="ReportTempConfigModel" fullscreen
      custom-class="temp-config-dialog" :close-on-click-modal="false" @close="handleCancel">
      <TempConfig v-if="ReportTempConfigModel" ref="ReportTempConfig" :modelType="modelType"
        :vcTemplateId="vcTemplateId" :rowData="rowData" @closeModal="handleCancel" @refresh="refreshData"></TempConfig>
    </el-dialog>
  </div>
</template>

<script>
import TempConfig from './components/tempConfig.vue'
import Pagination from '@/components/NewPagination'
import pageApi from './scripts/api'
import commonFunOld from '@/filters/common'

export default {
  name: 'CustomReportTempManage',
  components: {
    TempConfig,
    Pagination
  },
  data() {
    return {
      queryForm: {
        templateName: '',
        vcTempType: '',
        orderString: ''
      },
      tableData: [],
      loading: false,
      btnDisabled: false,

      PageSize: 20,
      CurrentPage: 1,
      total: 0,

      // Dialog props
      ReportTempConfigModel: false,
      ReportTempConfigModelTitle: '新增模板',
      modelType: '', // 1(新增)、2(编辑)、3(复制新增)、4(预览)
      vcTemplateId: '',
      rowData: {}
    }
  },
  created() {
    this.getTableData(true)
  },
  methods: {
    onQuery() {
      this.getTableData(true)
    },
    handleReset(formName) {
      if (this.$refs[formName]) {
        this.$refs[formName].resetFields()
      } else {
        this.queryForm.templateName = ''
        this.queryForm.vcTempType = ''
      }
      this.getTableData(true)
    },
    pagination(val) {
      let { page, limit } = val
      this.CurrentPage = page
      this.PageSize = limit
      this.getTableData(false)
    },
    handleSortChange(val) {
      this.queryForm.orderString = commonFunOld.queryOrderBy_vxe_template(val)
      this.getTableData()
    },
    getTableData(isResetPage = false) {
      if (isResetPage) {
        this.CurrentPage = 1
      }
      const params = {
        pageNum: this.CurrentPage,
        pageSize: this.PageSize,
        type: '1', // 固定参数
        templateName: this.queryForm.templateName,
        vcTempType: this.queryForm.vcTempType || "",
        orderString: this.queryForm.orderString
      }

      this.loading = true
      pageApi.getTempList(params).then(res => {
        const { status, data, message } = res.data;
        if (status === 200 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.$message.error(message || '查询失败')
        }
      }).finally(() => {
        this.loading = false
      })
    },
    onAddTemp() {
      this.modelType = '1'
      this.ReportTempConfigModelTitle = '新增模板'
      this.ReportTempConfigModel = true
    },
    handleView(row) {
      this.$router.push({
        path: '/jxbg/bgzq/customReportView',
        query: {
          templateCode: row.fTemplateID
        }
      })
    },
    deleteRow(row) {
      this.$confirm(`是否删除 【${row.vcTemplatEname}】 模板？`, '确定删除', {
        confirmButtonText: '删除',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        pageApi.deleteTemp({
          templateId: row.fTemplateID
        }).then(res => {
          const { status, data, message } = res.data;
          if (status === 200) {
            this.$message.success('删除成功')
            this.getTableData(true)
          } else {
            this.$message.error(message || '删除失败')
          }
        })
      }).catch(() => { })
    },
    getInfo(row, type) {
      this.btnDisabled = true
      const params = {
        templateId: row.fTemplateID
      }
      pageApi.getRelatedIndex(params).then(res => {
        const { status, data, message } = res.data;
        if (status === 200 && data) {
          this.rowData = {
            indexData: data || [],
            templateName: row.vcTemplatEname || '',
            templateId: row.fTemplateID
          }
          if (type === '2') {
            this.modelType = '2'
            this.ReportTempConfigModelTitle = '编辑模板'
            this.vcTemplateId = row.fTemplateID
            this.ReportTempConfigModel = true
          } else if (type === '3') {
            this.modelType = '3'
            this.ReportTempConfigModelTitle = '新增模板'
            this.ReportTempConfigModel = true
          } else if (type === '4') {
            this.modelType = '4'
            this.ReportTempConfigModelTitle = `预览模板【${row.vcTemplatEname}】`
            this.ReportTempConfigModel = true
          }
        } else {
          this.$message.error(message || '查询失败')
        }
      }).finally(() => {
        this.btnDisabled = false
      })
    },
    handleCommand(command, row) {
      this.getInfo(row, command)
    },
    handleCancel() {
      this.ReportTempConfigModel = false
      this.removeScripts()
    },
    refreshData() {
      this.getTableData(true)
    },
    removeScripts() {
      const tagElements = document.getElementsByTagName('script')
      const tagClass = 'customScript'
      for (let m = tagElements.length - 1; m >= 0; m--) {
        if (tagElements[m].className === tagClass) {
          tagElements[m].parentNode.removeChild(tagElements[m])
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.custom-report-temp-manage {
  height: 100%;
  padding: 12px 10px;

  .custom-report-temp-manage-table {
    height: calc(100% - 110px);
  }

  ::v-deep .temp-config-dialog {
    width: 100% !important;

    .el-dialog__body {
      height: calc(100vh - 70px);
      padding: 0;
      overflow: hidden;
      max-height: none !important;
    }
  }
}
</style>
