<template>
  <div class="optionBackTrader" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item label="方案名称">
                <el-input v-model="formInline.programmeName" size="small" clearable placeholder="请输入方案名称"
                  style="width: 350px" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search"
                  @click="handleSearchTable(true)">查询</el-button>
                <el-button type="primary" size="small" icon="el-icon-caret-right" @click="handleExecute">开始回测</el-button>
                <el-button type="primary" size="small" icon="el-icon-plus" @click="openAdd">新增</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>

    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table ref="refsTable" v-loading="tableLoading" :checkbox-config="{ checkStrictly: true }"
          :cell-style="{ height: '50px' }" :data="tableData" :height="tableHeight" auto-resize stripe sync-resize
          show-overflow="tooltip" style="width: 100%" :sort-config="{ remote: true }" @sort-change="customSortMethod"
          resizable>
          <vxe-table-column type="radio" width="60" align="center" header-align="center" />
          <vxe-table-column v-for="item in tableColumns" :key="item.prop" :align="item.align" :field="item.prop"
            :show-overflow-tooltip="item.showtooltip" :title="item.label" :min-width="item.width" header-align="center"
            sortable></vxe-table-column>
          <vxe-table-column title="操作" min-width="300" align="center" header-align="center">
            <template slot-scope="{ row }">
              <el-button type="text" size="small" @click="openLook(row)">查看</el-button>
              <el-button type="text" size="small" @click="openEdit(row)">修改</el-button>
              <el-button type="text" size="small" @click="handleCopy(row)">复制</el-button>
              <el-button type="text" size="small" @click="handleDelete(row)">删除</el-button>
              <el-button v-if="row.resultFlag === '1'" type="text" size="small"
                @click="openResult(row)">回测结果</el-button>
            </template>
          </vxe-table-column>
        </vxe-table>

        <vxe-pager :current-page="formInline.pageNum" :page-size="formInline.pageSize" :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          :page-sizes="pagerConfig.pageSizes" border size="medium" class="standard-vxe-pager"
          @page-change="pagination" />
      </div>
    </div>

    <BacktraderDialog
      v-if="dialogVisible"
      :mode="dialogMode"
      :row="selectedRow"
      @closeDialog="closeDialog"
      @saveSuccess="handleSearchTable(false)"
    />
  </div>
</template>

<script>
import commonFun from '@/filters/common'
import pageApi from './scripts/api'
import constants from './scripts/constants'
import BacktraderDialog from './components/dialog.vue'

export default {
  name: 'OptionBackTrader',
  components: { BacktraderDialog },
  data() {
    return {
      formInline: {
        programmeName: '',
        orderString: 'fid desc',
        pageSize: 20,
        pageNum: 1
      },
      tableColumns: constants.TABLE_COLUMNS,
      tableHeight: 0,
      tableLoading: false,
      tableData: [],
      total: 0,
      pagerConfig: {
        pageSizes: [10, 20, 50, 100, 500]
      },
      dialogVisible: false,
      dialogMode: { mode: 'add' },
      selectedRow: null
    }
  },
  mounted() {
    this.handleTableHeight()
    this.handleSearchTable(true)
  },
  beforeDestroy() {
    window.onresize = null
  },
  methods: {
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
    handleSearchTable(resetPage) {
      if (resetPage) this.formInline.pageNum = 1
      const params = { ...this.formInline }
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
      pageApi.getBackTraderList(params).then((res) => {
        this.tableLoading = false
        const data = res.data || res
        if (data.rows !== undefined) {
          this.tableData = data.rows || []
          this.total = data.total || 0
        } else if (data.data && data.data.rows !== undefined) {
          this.tableData = data.data.rows || []
          this.total = data.data.total || 0
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
    getBaseApi() {
      return (this.$store && this.$store.state.setting.baseApi) || process.env.BASE_API || ''
    },
    handleExecute() {
      const row = this.$refs.refsTable.getRadioRecord()
      if (!row) {
        this.$message.warning('请选择一条方案')
        return
      }
      this.$confirm('确定开始回测选中的方案？', '提示', { type: 'warning' })
        .then(() => pageApi.executeBackTrader(row.fid))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 1) {
            this.$message.success('回测执行成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '回测执行失败，请重试')
          }
        })
        .catch(() => { })
    },
    closeDialog(){
      this.dialogVisible = false
    },
    openAdd() {
      this.dialogVisible = true
      this.dialogMode = 'add'
      this.selectedRow = null
    },
    openEdit(row) {
      this.dialogVisible = true
      this.dialogMode = 'edit'
      this.selectedRow = { ... row }
    },
    handleCopy(row) {
      this.dialogVisible = true
      this.dialogMode = 'copy'
      this.selectedRow = { ... row }
    },
    openLook(row) {
      this.dialogVisible = true
      this.dialogMode = 'view'
      this.selectedRow = { ... row }
    },
    openResult(row) {
      const routeUrl = this.$router.resolve({
        path: '/optionbacktraderResult',
        query: {
          fid: row.fid,
          programmeName: row.programmeName || ''
        }
      })
      window.open(routeUrl.href, '_blank')
    },
    handleDelete(row) {
      this.$confirm(`确定删除序号为 [${row.fid}] 的记录？`, '提示', { type: 'warning' })
        .then(() => pageApi.deleteBackTrader(row.fid))
        .then((res) => {
          const data = res.data || res
          if (data.resultCode === '1' || data.resultCode === 1) {
            this.$message.success('删除成功')
            this.handleSearchTable(false)
          } else {
            this.$message.error(data.message || '删除失败，请重试')
          }
        })
        .catch(() => { })
    },
    submitEditDialog(form, mode) {
      if (mode === 'add') {
        return pageApi.addBackTrader(form).then(this.checkResult)
      }
      if (mode === 'edit') {
        return pageApi.editBackTrader(form).then(this.checkResult)
      }
      if (mode === 'copy') {
        const { fid, ...rest } = form
        return pageApi.copyBackTrader(rest).then(this.checkResult)
      }
      return Promise.resolve()
    },
    checkResult(res) {
      const data = res.data || res
      if (data.resultCode === '1' || data.resultCode === 1) return res
      return Promise.reject(new Error(data.message || '保存失败，请重试'))
    }
  }
}
</script>

<style lang="scss" scoped>
.optionBackTrader {
  .dd-style-table {
    padding: 10px 0;

    .dd-table-title {
      font-weight: bold;
    }
  }

  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>
