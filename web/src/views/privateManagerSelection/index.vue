<template>
  <div class="manager-selection">
    <manager-search
      ref="managerSearch"
      :page-list="pageList"
      :order-list="orderList"
      @resetPage="resetPageList"
      @updateLoading="getTableLoading"
      @updateTable="getTabelData"
      @updateheight="updateHeight"
    ></manager-search>
    <manager-table
      ref="manTable"
      :table-data="tableData"
      :table-loading="tableLoading"
      :export-loading="exportLoading"
      :is-disabled="isDisabled"
      @excelexport="handleExcelExport"
      @sorttable="handleSortTable"
      @updatelist="updatelist"
    ></manager-table>
    <el-row style="padding-left: 25px;">
      <!-- <div style="display: inline-block;line-height: 56px;">
        <el-button
          type="info"
          size="small"
          @click="
            () => {
              $refs.manTable.handleBatchFocus()
            }
          "
        >
          批量关注
        </el-button>
        <el-button
          :disabled="isDisabled"
          :icon="exportLoading ? 'el-icon-loading' : ''"
          type="info"
          size="small"
          @click="
            () => {
              $refs.manTable.handleExcelExport()
            }
          "
        >
          导出Excel
        </el-button>
        <el-button
          type="info"
          size="small"
          @click="
            () => {
              $refs.manTable.productSelectDialogVisible = true
            }
          "
        >
          自定义指标
        </el-button>
      </div> -->
      <Pagination :limit="pageList._pageSize" :page="pageList._pageNum" :total="total" @pagination="pagination" />
    </el-row>
    <!-- <div style="height: 12px;"></div> -->
  </div>
</template>

<script>
import managerSearch from './components/searchQuery.vue'
import managerTable from './components/managerTable.vue'
import Pagination from '@/components/Pagination'
import { downLoadFileByUrl } from '@/utils'
export default {
  name: 'ManagerSelection',
  components: {
    managerSearch,
    managerTable,
    Pagination
  },
  data() {
    return {
      exportLoading: false,
      isDisabled: false,
      pageList: {
        _pageNum: 1,
        _pageSize: 20
      },
      total: 0,
      tableLoading: false,
      tableData: [],
      orderList: {
        orderString: 'navDate desc'
      }
    }
  },
  methods: {
    updateHeight() {
      this.$refs.manTable.$refs.tableBody.handleTableHeight()
    },
    handleExcelExport() {
      // 获取当前查询条件
      let params = this.$refs.managerSearch.getParamsObject()
      params = this.$refs.managerSearch.parameterSrc(params)
      const fileName = '管理人列表-导出.xls'
      const url = '/api/manager/export'
      this.exportLoading = true
      this.isDisabled = true
      downLoadFileByUrl(url, params, fileName, this)
    },
    /**
     * @description 设置排序字段
     */
    handleSortTable(val) {
      this.orderList.orderString = this.$fun.queryOrderBy_vxe_template(val)
      if (val.order) {
        this.$refs.managerSearch.handleQueryParams()
      }
    },
    /**
     * @description 回传重置分页
     */
    resetPageList() {
      this.pageList._pageNum = 1
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.$refs.managerSearch.handleQueryParams()
    },
    /**
     * @description 回传表格loading状态
     */
    getTableLoading(flag) {
      this.tableLoading = flag
    },
    /**
     * @description 回传表格数据
     */
    getTabelData(table) {
      this.tableData = table.rows
      this.total = table.total
    },
    /**
     * @description 关注完刷新列表
     */
    updatelist() {
      this.$refs.managerSearch.handleQueryParams()
    }
  }
}
</script>

<style></style>
