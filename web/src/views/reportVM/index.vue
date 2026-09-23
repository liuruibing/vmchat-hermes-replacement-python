<template>
  <div v-if="!isShowReport" style="height: 100%; overflow: hidden">
    <div v-if="isShowTable">
      <div class="standard-form-margin">
        <div class="inner-margin">
          <el-form :inline="true" class="standard-form" :model="formQuery">
            <el-form-item label="">
              <el-input v-model="formQuery.templateName" placeholder="请输入报告名称" size="small" />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" size="small" icon="el-icon-search" @click="onQuery(true)">查询</el-button>
              <el-button type="info" size="small" plain icon="el-icon-refresh-left" @click="reset">重置</el-button>
            </el-form-item>
          </el-form>
          <ToolBarSlot>
            <template slot="left">
              <span class="standard-form">
                <el-button v-btn="'reportDefault'" type="info" size="small" plain icon="el-icon-circle-plus-outline" @click="handleNewReport('0')">默认报告</el-button>
                <el-button type="info" size="small" plain icon="el-icon-circle-plus-outline" @click="handleNewReport('1')">自定义报告</el-button>
              </span>
            </template>
          </ToolBarSlot>
        </div>
      </div>
      <div id="standard-table" class="standard-table">
        <div id="standard-table-margin">
          <vxe-table
            v-loading="tableLoading"
            ref="vxetable"
            :cell-style="{ height: '50px' }"
            :checkbox-config="{ checkStrictly: true }"
            :data="tableData"
            :height="tableHeight"
            :sort-config="{ remote: true, defaultSort: { field: 'm1_return', order: 'desc' } }"
            border="inner"
            auto-resize
            stripe=""
            show-overflow="tooltip"
            style="width: 100%"
            sync-resize
          >
            <vxe-table-column
              v-for="item in tableColumns"
              :key="item.id"
              :align="item.align"
              :field="item.id"
              :min-width="item.width"
              :show-overflow-tooltip="item.noshowoverflowtooltip"
              :sortable="item.sortable"
              :title="item.label"
              header-align="center"
            >
              <template slot-scope="scope">
                <span v-if="item.filter === 'fVmType-filter'">{{ scope.row[item.id] | fVmTypeToStr }}</span>
                <span v-else-if="item.filter === 'vcReportType-filter'">{{ scope.row[item.id] | vcReportTypeStr }}</span>
                <span v-else>{{ scope.row[item.id] | noDataFilter }}</span>
              </template>
            </vxe-table-column>
            <vxe-table-column align="center" fixed="right" title="操作" width="400px">
              <template slot-scope="scope">
                <span class="table-operation">
                  <span v-if="scope.row.fVmType == '0'">
                    <el-button type="info" plain size="small" @click="editRow(scope.row)" v-btn="'reportDefault'">编辑</el-button>
                  </span>
                  <span v-else>
                    <el-button type="info" plain size="small" @click="editRow(scope.row)">编辑</el-button>
                  </span>
                  <span>
                    <el-button type="info" plain size="small" @click="copyRow(scope.row)">复制</el-button>
                  </span>
                  <span v-if="scope.row.fVmType == '0'">
                    <el-popconfirm
                      v-btn="'reportDefault'"
                      confirm-button-text="确定"
                      cancel-button-text="取消"
                      icon="el-icon-info"
                      icon-color="red"
                      title="确实删除当前数据吗？"
                      @confirm="delRow(scope.row)"
                    >
                      <el-button slot="reference" plain type="info" size="small">删除</el-button>
                    </el-popconfirm>
                  </span>
                  <span v-else>
                    <el-popconfirm
                      confirm-button-text="确定"
                      cancel-button-text="取消"
                      icon="el-icon-info"
                      icon-color="red"
                      title="确实删除当前数据吗？"
                      @confirm="delRow(scope.row)"
                    >
                      <el-button slot="reference" plain type="info" size="small">删除</el-button>
                    </el-popconfirm>
                  </span>
                  <span>
                    <el-button type="info" plain size="small" @click="preViewRow(scope.row)">预览</el-button>
                  </span>
                  <span>
                    <el-button type="info" plain size="small" @click="selectRow(scope.row)">查询</el-button>
                  </span>
                </span>
              </template>
            </vxe-table-column>
          </vxe-table>
          <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="formQuery.total" @pagination="pagination" />
        </div>
      </div>
    </div>
    <div v-if="!isShowTable" style="height: 100%">
      <report
        v-if="!isShowTable"
        ref="report"
        :new-report-config="newReportConfig"
        :row-info="rowInfo"
        @return="
          () => {
            isShowTable = true
            onQuery(false)
          }
        "
      ></report>
    </div>
    <el-dialog
      :title="dialogTitle"
      :visible="dialogVisible"
      width="30% !important"
      center
      @close="
        () => {
          dialogVisible = false
        }
      "
    >
      <el-form ref="dialogFormRef" class="standard-form" :model="newReportConfig" :rules="dialogRules" label-width="120px">
        <el-form-item label="报告名称" prop="templateName">
          <el-input v-model="newReportConfig.templateName" size="small"></el-input>
        </el-form-item>
        <el-form-item label="维度类型" prop="vcReportType">
          <el-select v-model="newReportConfig.vcReportType" size="small" placeholder="请选择报告维度类型" style="width: 160px !important">
            <el-option v-for="(item, index) in vcReportTypeArray" :key="item.dimCde + index" :label="item.dimNme" :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <div slot="footer">
        <div class="standard-form">
          <el-button type="primary" size="small" @click="nextStep">下一步</el-button>
          <el-button
            type="info"
            size="small"
            plain
            @click="
              () => {
                dialogVisible = false
              }
            "
          >
            取消
          </el-button>
        </div>
      </div>
    </el-dialog>
  </div>
  <div v-else style="height: 100%; width: 100%; position: relative">
    <div title="返回列表" style="font-size: 28px; position: absolute; right: 10px; top: 5px; z-index: 1000 !important; cursor: pointer" @click="handleReturnIcon">
      <svg-icon class-name="size-icon" icon-class="return"></svg-icon>
    </div>
    <div style="height: 100%">
      <report-template :report-config-extern="reportConfig"></report-template>
    </div>
  </div>
</template>
<script>
import pageApi from './api/index'
import commonApi from '@/api/common'
import { TABLECOLUMNS } from './constant'
import Pagination from '@/components/Pagination'
import report from './components/report'
import reportTemplate from './components/reportTemplate'
import ToolBarSlot from '@/components/toolBarSlot'
export default {
  components: { Pagination, report, reportTemplate, ToolBarSlot },
  filters: {
    fVmTypeToStr(val) {
      if (val === '0') {
        return '默认报告'
      } else {
        return '自定义报告'
      }
    },
    vcReportTypeStr(val) {
      // const reportType = this.vcReportTypeArray.find(item => item.dimCde === val);
      // return reportType ? reportType.dimNme : '-';

      if (val == '1') {
        return '单产品'
      } else if (val == '2') {
        return '多产品(含对比基准)'
      } else if (val == '3') {
        return '多产品(不包含对比基准)'
      }else if (val == '4') {
        return '单产品(不包含对比基准)'
      }else if (val == '5') {
        return '策略私募报告'
      }else if (val == '6') {
        return '股衍互换分析报告'
      }else if (val == '7') {
        return '多因子-对比指数-分析报告'
      }else if (val == '8') {
        return '中性策略-多因子-分析报告'
      }else {
        return '-'
      }
    }
  },
  data() {
    return {
      // 查看报告的信息
      reportConfig: null,

      dialogVisible: false,
      dialogTitle: '',
      dialogRules: {
        templateName: [{ required: true, message: '报告名称不能为空', trigger: 'blur' }],
        vcReportType: [{ required: true, message: '报告名称不能为空', trigger: 'blur' }]
      },

      rowInfo: {},
      isShowTable: true,
      isShowReport: false,
      viewType: 'preview',
      tableHeight: '500px',
      tableData: [],
      tableColumns: TABLECOLUMNS,
      tableLoading: false,
      formQuery: {
        templateName: '',
        pageSize: 10,
        pageNum: 1,
        total: 0
      },
      // 新建自定义报告 配置信息
      vcReportTypeArray: [],
      newReportConfig: {
        templateName: '', // 报告名称
        fVmType: '', // 报告类型 0 默认报告， 1 自定义报告
        vcReportType: '' // 维度类型， 0 单产品报告， 1 多产品报告
      }
    }
  },

  created() {
    this.getEdimsBGWD()
  },
  activated() {
    this.handleTableHeight()
  },

  mounted() {
    this.getEdimsBGWD()
    this.handleTableHeight()
    this.onQuery(true)

  },
  methods: {
    /**
     * @Description: 获取报告维度字典
     * @author Liu Rui Bing
     * @date 2024/6/27
     */

    getEdimsBGWD() {
      commonApi.edimsCommon('INDEX_SIGN').then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          this.vcReportTypeArray = data
        } else {
          this.vcReportTypeArray = []
        }
      })
    },

    /**
     * @Description: 创建报告下一步
     * @author Liu Rui Bing
     * @date 2024/6/25
     */
    nextStep() {
      this.$refs.dialogFormRef.validate((valid) => {
        if (valid) {
          this.rowInfo = {}
          this.dialogVisible = false
          this.$nextTick(() => {
            this.isShowTable = false
          })
        } else {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '请按照提示信息修改',
            customClass: 'message-warning'
          })
        }
      })
    },

    /**
     * @Description: 退出预览
     * @author Liu Rui Bing
     * @date 2024/6/13
     */
    handleReturnIcon() {
      this.isShowReport = false
    },

    /**
     * @Description: 预览 报告
     * @author Liu Rui Bing
     * @date 2024/5/7
     */
    preViewRow(row) {
      // 组装预览的数组
      this.reportConfig = {
        // templateCode: row
        vcReportType: row.vcReportType,
        templateName: row.vcTemplatEname,
        templateCode: row.fTemplateID,
        type: 'preview'
      }
      this.isShowReport = !this.isShowReport
    },

    /**
     * @Description: 查询报告
     * @author Liu Rui Bing
     * @date 2024/5/7
     */
    selectRow(row) {
      // 组装预览的数组
      this.reportConfig = {
        vcReportType: row.vcReportType,
        templateName: row.vcTemplatEname,
        templateCode: row.fTemplateID,
        type: 'view'
      }
      this.isShowReport = !this.isShowReport
    },

    /**
     * @Description: 新建报表
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    handleNewReport(fVmtype) {
      this.newReportConfig = {
        templateName: '', // 报告名称
        fVmType: '', // 报告类型 0 默认报告， 1 自定义报告
        vcReportType: '' // 维度类型， 0 单产品报告， 1 多产品报告
      }
      fVmtype === '0' ? (this.dialogTitle = '新建默认报告') : (this.dialogTitle = '新建自定义报告')
      fVmtype === '0' ? (this.newReportConfig.fVmType = '0') : (this.newReportConfig.fVmType = '1')
      this.dialogVisible = true
    },
    /**
     * @Description: 复制当前数据
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    copyRow(row) {
      const params = { templateId: row.fTemplateID }
      pageApi.copy(params).then((res) => {
        const { status, message } = res.data
        if (status === 200) {
          this.$message.closeAll()
          this.$message({
            type: 'success',
            message: message || '复制成功',
            customClass: 'message-success'
          })
          this.onQuery(true)
        } else {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: message || '复制失败',
            customClass: 'message-warning'
          })
        }
      })
    },
    /**
     * @Description: 删除 当前 报告
     * @author Liu Rui Bing
     * @date 2024/4/29
     */
    delRow(row) {
      const params = { templateId: row.fTemplateID }
      pageApi.delete(params).then((res) => {
        const { status, message } = res.data
        if (status === 200) {
          this.$message.closeAll()
          this.$message({
            type: 'success',
            message: message || '删除成功',
            customClass: 'message-success'
          })
          this.onQuery(true)
        } else {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: message || '删除失败',
            customClass: 'message-warning'
          })
        }
      })
    },
    editRow(row) {
      // 进入 编辑模式
      // 查询 当前信息 对应的 指标数据
      const params = { templateId: row.fTemplateID }

      pageApi.relatedIndex(params).then((res) => {
        const { status, data } = res.data
        data.forEach((item) => {
          item.vcCode = item.indexCode
        })
        this.isShowTable = false
        this.$nextTick(() => {
          this.newReportConfig = {
            templateName: row.vcTemplatEname, // 报告名称
            fVmType: row.fVmType, // 报告类型 0 默认报告， 1 自定义报告
            vcReportType: row.vcReportType, // 维度类型， 0 单产品报告， 1 多产品报告
            templateId: row.fTemplateID
          }
          this.rowInfo = {
            row: row,
            data: data
          }
        })
      })
    },

    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.onQuery(false)
    },
    reset() {
      this.formQuery.templateName = ''
    },
    onQuery(flag) {
      if (flag) {
        this.formQuery.pageNum = 1
      }
      const params = Object.assign({}, this.formQuery)
      this.tableLoading = true
      pageApi.list(params).then((res) => {
        this.tableLoading = false
        const { status, data } = res.data
        if (status === 200) {
          this.tableData = data.list
          this.formQuery.total = data.total
        } else {
          this.tableData = []
          this.formQuery.total
        }
      })
    },
    handleTableHeight() {
      setTimeout(() => {
        const appMain = document.getElementById('app').offsetHeight
        const ddQuery = document.getElementById('dd-query').offsetHeight
        const diff = appMain - ddQuery - 10 - 120 - 100
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
    }
  }
}
</script>
<style scoped lang="scss"></style>
