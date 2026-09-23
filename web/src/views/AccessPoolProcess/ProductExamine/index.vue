<template>
  <div class="product-examine" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form">
          <el-form-item label="" prop="fundCode">
            <el-input v-model="formQuery.fundCode" placeholder="请输入产品代码/拼音首字母" style="width: 210px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fundName">
            <el-input v-model="formQuery.fundName" placeholder="请输入产品名称/拼音首字母" style="width: 210px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="managerName">
            <el-input v-model="formQuery.managerName" placeholder="请输入管理人名称/拼音首字母" style="width: 220px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="status">
            <el-select v-model="formQuery.status" placeholder="请选择审核状态" size="small" clearable>
              <el-option v-for="item in statusOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="queryExamineList" icon="el-icon-search">查询</el-button>
            <el-button type="info" plain size="small" @click="resetForm()" icon="el-icon-refresh-left">重置</el-button>
            <el-button type="info" plain size="small" icon="el-icon-plus" @click="addProduct('ADD')">新增准入审批</el-button>
          </el-form-item>
        </el-form>
<!--        <ToolBarSlot>
          <template slot="left">

          </template>
        </ToolBarSlot>-->
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
          resizable
        >
          <vxe-table-column align="center" fixed="left" title="序号" type="seq" width="50"></vxe-table-column>
          <vxe-table-column
            v-for="(col, i) in tableColumns"
            :key="i"
            :field="col.prop"
            :label="col.label"
            :width="col.width"
            :align="col.align"
            show-overflow-tooltip
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="col.prop === 'status'">
                <el-tag size="mini" :type="setStatusColor(scope.row[col.prop])">{{ scope.row[col.prop] | statusFilter(that) }}</el-tag>
              </span>
              <span v-else-if="col.prop === 'strategy'">{{ scope.row[col.prop] | strategyFilter(that) }}</span>
              <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="480" align="left" header-align="center">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" size="small" plain @click="editProduct(scope.row, 'EDIT')">编辑</el-button>
                <el-button type="info" size="small" plain @click="handleExamine(scope.row)">提交/审批</el-button>
                <el-button type="info" size="small" plain @click="handleFileManage(scope.row)">文件管理</el-button>
                <el-button type="info" size="small" plain v-if="['0', '5'].includes(scope.row.status)" @click="deleteFund(scope.row)">删除</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          class="standard-vxe-pager"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          @page-change="pagination"
        />
      </div>
    </div>
<!--
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination" />-->
    <el-dialog
      :title="editTitle"
      :visible.sync="editDialog"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      custom-class="saveAsDialog"
      @close="closeEdit"
    >
      <product-edit :strategy-type-options="strategyTypeOptions" :current-row="currentRow" :dialog-status="dialogStatus" @closeEdit="closeEdit"></product-edit>
    </el-dialog>
  </div>
</template>

<script>
import { TABLE_COLUMNS, STATUS_COLOR_MAP } from './scripts/constant'
import productEdit from './components/productEdit'
import Pagination from '@/components/Pagination'
import commonAPI from '@/api/common.js'
import { getExamineAll, deleteFund } from './scripts/api'
import ToolBarSlot from '@/components/toolBarSlot'
export default {
  name: 'ProductExamine',
  components: {
    productEdit,
    Pagination,
    ToolBarSlot
  },
  filters: {
    statusFilter(value, that) {
      const obj = that.statusOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    },
    strategyFilter(value, that) {
      const obj = that.strategyTypeOptions.find((item) => item.DIM_CDE === value)
      return (obj && obj.DIM_NME) || '-'
    }
  },
  data() {
    return {
      that: this,
      formQuery: {
        fundCode: '',
        fundName: '',
        managerName: '',
        status: '',
        pageSize: 20,
        pageNum: 1
      },
      total: 0,
      statusOptions: [],
      strategyTypeOptions: [],
      tableColumns: TABLE_COLUMNS,
      tableData: [],
      statusColor: STATUS_COLOR_MAP,
      editDialog: false,
      editTitle: '',
      currentRow: null,
      dialogStatus: 'ADD',
      tableLoading: false,
      tableHeight: 0
    }
  },
  mounted() {
    this.initData()
  },
  methods: {
    // 重置
    resetForm() {
      this.$refs['formQuery'].resetFields()
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
      })
    },
    async initData() {
      this.handleTableHeight()
      await this.getExamineStatusOptions()
      await this.queryExamineList()
      await this.queryStrategyOptions()
    },
    async getExamineStatusOptions() {
      const data = {
        indexCode: '86606acb-4ec7-4c39-97ef-e15453860bb4'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          this.statusOptions = res.data.data || []
        }
      } catch (e) {
        this.statusOptions = []
      }
    },
    async queryStrategyOptions() {
      const data = {
        indexCode: '6c7d78c7-aced-487b-8310-a9ad7e09c3f8'
      }
      try {
        const res = await commonAPI.getDataBysqlCode(data)
        if (res.data.status === 0) {
          this.strategyTypeOptions = res.data.data || []
        }
      } catch (e) {
        this.strategyTypeOptions = []
      }
    },
    async queryExamineList() {
      const params = {
        limit: this.formQuery.pageSize,
        offset: (this.formQuery.pageNum - 1) * this.formQuery.pageSize,
        ...this.formQuery
      }
      delete params.pageNum
      delete params.pageSize
      this.tableLoading = true
      try {
        const res = await getExamineAll(params)
        if (res.data.rows && res.data.rows.length > 0) {
          const resultData = res.data.rows || []
          this.tableData = resultData
          this.total = res.data.total
          this.tableLoading = false
        } else {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        }
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },

    setStatusColor(val) {
      const colorObj = this.statusColor.find((item) => item.value === val)
      return colorObj && colorObj.status
    },
    addProduct(status) {
      this.editDialog = true
      this.editTitle = '新增'
      this.dialogStatus = status
    },
    editProduct(row, status) {
      const deepRow = JSON.parse(JSON.stringify(row)) || {}
      // 判断如果该产品代码以ZR开头则判断去除，否则会回显出来
      if (deepRow.fundCode.startsWith('ZR')) {
        deepRow.fundCode = deepRow.fundCode.slice(2, deepRow.fundCode.length)
        deepRow.isPrefix = true
      }
      this.currentRow = deepRow
      this.dialogStatus = status
      this.editDialog = true
      this.editTitle = '编辑'
    },
    async deleteFund(row) {
      const data = {
        fid: row.fid || '',
        fundCode: row.fundCode || ''
      }
      this.$confirm('是否删除该条准入记录？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          deleteFund(data)
            .then((res) => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '删除成功',
                  customClass: 'message-success'
                })
                this.queryExamineList()
              } else {
                this.$message({
                  customClass: 'message-error',
                  type: 'error',
                  message: '删除失败'
                })
              }
            })
            .catch((e) => {
              this.$message({
                customClass: 'message-error',
                type: 'error',
                message: '删除失败'
              })
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    },
    closeEdit(status) {
      this.editDialog = false
      if (status === 'refesh') {
        this.queryExamineList()
      }
      for (const key in this.currentRow) {
        this.currentRow[key] = ''
      }
    },
    handleExamine(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: `/tzgl/zrlcgl/tjsp`,
        query: row
      })
    },
    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum  = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      /* const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit */
      this.queryExamineList()
    },
    handleFileManage(row) {
      this.$router.push({
        path: '/tzgl/zrlcgl/wjgl',
        query: row
      })
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
@import './styles/index';
.product-examine {
  // padding: 10px;
  ::v-deep .saveAsDialog {
    width: 55% !important;
    .el-dialog__body {
      overflow: visible !important;
    }
  }
  .el-dialog__body {
    overflow: visible !important;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #e03d3e;
  }
  ::v-deep .el-dialog__wrapper .el-dialog__header span {
    color: #333 !important;
  }
  ::v-deep .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
::v-deep .el-button--danger {
  color: #F56C6C;
   background-color: #fff;
  border-color: #F56C6C;
}
</style>
