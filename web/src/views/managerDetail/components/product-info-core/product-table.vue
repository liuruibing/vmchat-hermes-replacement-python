<template>
  <div class="tabletable">
    <!-- <el-row justify="space-around" type="flex">
      <el-col :span="12">
        <div style="vertical-align: middle;display: inline-block">
          <div class="color-box"></div>
        </div>
        <div class="title-style">旗下产品</div>
      </el-col>
      <el-col :span="12">
        <div style="display: flex;float: right;">
          <el-button size="small" type="info" @click="onContrast">对比</el-button>
          <el-button size="small" type="info" @click="handleBatchFocus">
            批量关注
          </el-button>
          <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" size="small" type="info" @click="handleExcelExport">
            导出Excel
          </el-button>
          <el-button size="small" type="info" @click="productSelectDialogVisible = true">
            自定义指标
          </el-button>
        </div>
      </el-col>
    </el-row> -->
    <ToolBarSlot>
      <template slot="left">
        <el-button size="small" type="info" plain @click="onContrast">对比</el-button>
        <el-button size="small" type="info" plain @click="handleBatchFocus">
          批量关注
        </el-button>
      </template>
      <template slot="right">
        <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" size="small" type="info" plain @click="handleExcelExport">
          导出Excel
        </el-button>
        <el-button size="small" type="info" plain @click="productSelectDialogVisible = true">
          自定义指标
        </el-button>
      </template>
    </ToolBarSlot>
    <div v-if="basicCheckArr && basicCheckArr.length">
      已选产品:
      <el-tag v-for="item in basicCheckArr" :key="item.id" :disable-transitions="false" closable @close="handleCloseBasic(item)">
        <!--        <span>{{ item.fundCode }}</span>-->
        <span>{{ item.fundName }}</span>
      </el-tag>
    </div>
    <table-body
      ref="tableBody"
      :check-array="basicCheckArr"
      :column="column"
      :table-data="tableData"
      :table-loading="tableLoading"
      @checkbox="handleCheckBoxChange"
      @focusstatus="handleFocus"
      @linkto="jumpToSingle"
      @sorttable="handleSortTable"
    ></table-body>
    <table-head :table-column="column" :table-column-selector-visible="productSelectDialogVisible" @dialogclose="handleCloseDialog" @submit="handleSubmit"></table-head>
    <focus-dialog :is-show-focus="isShowFocus" :select-row-data="selectRowData" :title="title" @updateFocusStatus="updateFocusStatus"></focus-dialog>
  </div>
</template>

<script>
import tableBody from './tableBodyComponent'
import tableHead from './tableHeadComponent'
import focusDialog from '@/components/Bussiness/focusDialog'
import { deleteAllFocus } from './scripts/api'
import ToolBarSlot from '@/components/toolBarSlot'

export default {
  components: { tableBody, tableHead, focusDialog, ToolBarSlot },
  props: {
    tableData: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    exportLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    isDisabled: {
      type: Boolean,
      default: false,
      required: true
    },
    tableLoading: {
      type: Boolean,
      required: true,
      default: false
    }
  },
  data() {
    return {
      basicCheckArr: [], // 已选产品
      productSelectDialogVisible: false,
      column: [
        {
          label: '产品代码',
          disabled: true,
          id: 'fundCode',
          type: 'leftTreeData',
          align: 'center',
          fix: 'left',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '产品名称',
          id: 'fundName',
          disabled: true,
          type: 'leftTreeData',
          align: 'left',
          fix: 'left',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: 'fund',
          sortable: true
        },
        {
          label: '投资策略',
          id: 'type',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '基金经理',
          id: 'managerName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '成立日期',
          id: 'foundDate',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          // TODO 是否需要单独做过滤
          label: '运行状态',
          id: 'status',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '净值日期',
          id: 'navDate',
          type: 'centerTreeDataCenter',
          align: 'left',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '单位净值',
          id: 'unitNav',
          type: 'centerTreeDataCenter',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'moneyYuan4Yuan',
          sortable: true
        },
        {
          label: '近一月收益率',
          id: 'm1_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近三月收益率',
          id: 'm3_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月收益率',
          id: 'm6_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年收益率',
          id: 'y1_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来收益率',
          id: 'ytd_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '成立以来收益率',
          id: 'total_return',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        }
      ],
      selectRowData: [],
      isShowFocus: false,
      title: '关注'
    }
  },
  methods: {
    handleCheckBoxChange({ row, checked }) {
      if (checked) {
        let index = this.basicCheckArr.findIndex(item => item.fundCode == row.fundCode)
        if (index == -1) {
          this.basicCheckArr.push(row)
        }
      } else {
        let index = this.basicCheckArr.findIndex(item => item.fundCode == row.fundCode)
        if (index != -1) {
          this.basicCheckArr.splice(index, 1)
        }
      }
    },

    // 勾选列表的取消删除逻辑
    handleCloseBasic(item) {
      let index = this.basicCheckArr.findIndex(sitem => sitem.fundCode == item.fundCode)
      if (index != -1) {
        this.basicCheckArr.splice(index, 1)
        this.$refs.tableBody.setCheckBoxFalse(item)
      }
    },
    handleExcelExport() {
      this.$emit('excelexport')
    },

    handleSortTable(val) {
      this.$emit('sorttable', val)
    },

    handleCloseDialog() {
      this.productSelectDialogVisible = false
    },
    handleNodeClick() {},
    handleSubmit(arr) {
      this.column = arr
    },
    /**
     * @description 批量关注
     */
    handleBatchFocus() {
      // const _arr = this.$refs.tableBody.getTableDataCheckRows()
      const _arr = this.basicCheckArr
      if (_arr && _arr.length) {
        this.selectRowData = _arr
        this.isShowFocus = true
        this.title = '批量关注'
      } else {
        this.selectRowData = []
        this.$message({
          type: 'warning',
          message: '请选择产品'
        })
      }
    },
    /**
     * @description 单个关注/取消关注
     */
    handleFocus(row) {
      if (row.isConcern === '0') {
        this.selectRowData = [row]
        this.isShowFocus = true
      } else {
        // 取消关注
        this.$confirm('此操作将取消该产品所有关注分组, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            const params = {
              fundCode: row.fundCode || ''
            }
            deleteAllFocus(params).then(res => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '取消成功'
                })
                this.$emit('updatelist')
              }
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '取消操作'
            })
          })
      }
    },
    /**
     * @description 保存关注关闭弹窗
     * @param { String } status refesh关闭弹窗刷新列表  norefesh仅关闭弹窗
     */
    updateFocusStatus(status) {
      this.isShowFocus = false
      if (status === 'refesh') {
        this.$emit('updatelist')
      }
    },
    /**
     * @description 跳转单产品页面
     */
    jumpToSingle(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: row }
      })
    },
    /**
     * @description 跳转多产品页面
     */
    onContrast() {
      const list = this.basicCheckArr
      if (list.length > 5) {
        this.$message.closeAll()
        this.$message.warning('对比产品不能超过5个')
        return
      }
      if (list.length >= 2) {
        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/smcpxx',
          query: { list: list }
        })
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请至少选择两个产品'
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.icon-style {
  margin-bottom: 0px !important;
  font-size: 14px;
}

.color_4f95dd {
  color: #4f95dd;
  cursor: pointer;
}

.color_e6a23c {
  color: #e6a23c;
}

.fund_cell {
  display: flex;
  align-items: center;

  .fund_name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    margin-right: 5px;
  }
}

.tabletable {
  margin-top: 10px;

  .tabletable_top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
  }
}

.color-box {
  display: inline-block;
  height: 30px;
  width: 2px;
  background-color: #0F65DD;
}

.title-style {
  color: #0F65DD;
  vertical-align: middle;
  height: 35px;
  line-height: 35px;
  font-size: 16px;
  margin-left: 5px;
  display: inline-block;
}

::v-deep .vxe-table--render-default .vxe-cell {
  white-space: normal;
}
</style>
