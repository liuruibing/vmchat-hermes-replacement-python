<template>
  <div class="tabletable">
    <ToolBarSlot>
      <template slot="left">
        <el-button type="info" plain size="small" @click="handleBatchFocus()">批量关注</el-button>
      </template>
      <template slot="right">
        <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" type="info" size="small" plain @click="handleExcelExport">导出Excel</el-button>
        <el-button type="info" plain size="small" @click="productSelectDialogVisible = true">自定义指标</el-button>
      </template>
    </ToolBarSlot>
    <div v-if="basicCheckArr && basicCheckArr.length">
      已选管理人:
      <el-tag v-for="item in basicCheckArr" :key="item.fundCode" :disable-transitions="false" closable @close="handleCloseBasic(item)">
        <!--        <span>{{ item.company_id }}</span>-->
        <span>{{ item.manager_name }}</span>
      </el-tag>
    </div>
    <table-body-provate-component
      ref="tableBody"
      :check-array="basicCheckArr"
      :column="column"
      :table-data="tableData"
      :table-loading="tableLoading"
      pageType="filter"
      @focusstatus="handleFocus"
      @sorttable="handleSortTable"
      @checkbox="handleCheckBoxChange"
      @linkto="jumpToManager"
    ></table-body-provate-component>
    <table-head-provate-component
      :table-column="column"
      :table-column-selector-visible="productSelectDialogVisible"
      @dialogclose="handleCloseDialog"
      @submit="handleSubmit"
    ></table-head-provate-component>
    <focus-manager-dialog
      :is-show-focus="isShowFocus"
      :select-row-data="selectRowData"
      :title="title"
      :page="pageType"
      @updateFocusStatus="updateFocusStatus"
    ></focus-manager-dialog>
  </div>
</template>

<script>
import tableHeadProvateComponent from '@/components/tableHeadPrivateComponent'
import tableBodyProvateComponent from '@/components/tableBodyPrivateComponent'
import { deleteAllFocus } from '../scripts/api'
import focusManagerDialog from '@/components/Bussiness/focusManagerDialog'
import ToolBarSlot from '@/components/toolBarSlot'
export default {
  name: 'ManagerTable',
  components: { tableHeadProvateComponent, tableBodyProvateComponent, focusManagerDialog, ToolBarSlot },
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
      basicCheckArr: [],
      productSelectDialogVisible: false,
      column: [
        {
          label: '备案编码',
          disabled: true,
          id: 'reg_code',
          type: 'leftTreeData',
          align: 'center',
          fix: 'left',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '管理人名称',
          disabled: true,
          id: 'manager_full_name',
          type: 'leftTreeData',
          align: 'center',
          fix: 'left',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'manager',
          sortable: true
        },
        {
          label: '公司类型',
          disabled: true,
          id: 'company_type',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '注册城市',
          disabled: true,
          id: 'register_city',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '备案状态',
          disabled: true,
          id: 'record_status',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '员工人数',
          disabled: true,
          id: 'employee_count',
          type: 'centerTreeDataLeft',
          align: 'center',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '核心人物',
          disabled: true,
          id: 'key_person',
          type: 'centerTreeDataLeft',
          align: 'center',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        // {
        //   label: '业务日期',
        //   disabled: false,
        //   id: 'endDate',
        //   type: 'leftTreeData',
        //   align: 'center',
        //   fix: '',
        //   width: '110px',
        //   noshowoverflowtooltip: true,
        //   filter: '',
        //   sortable: true
        // },
        {
          label: '近一年收益率',
          id: 'y1_return',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年波动率',
          id: 'y1_stdev',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年最大回撤',
          id: 'y1_max_retracement',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Sharpe比率',
          id: 'y1_sharpe',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Sortino比率',
          id: 'y1_sortino',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '130px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Treynor比率',
          id: 'y1_terynor',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '130px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Calmar比率',
          id: 'y1_calmar',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Alpha',
          id: 'y1_alpha',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Beta',
          id: 'y1_beta',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年投资胜率',
          id: 'y1_winrate',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年信息比率',
          id: 'y1_info',
          type: 'rightTreeData',
          align: 'right',
          fix: '',
          width: '120px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        }
      ],
      selectRowData: [],
      isShowFocus: false,
      title: '关注',
      pageType: 'MANAGER'
    }
  },
  methods: {
    handleCheckBoxChange({ row, checked }) {
      if (checked) {
        let index = this.basicCheckArr.findIndex((item) => item.company_id == row.company_id)
        if (index == -1) {
          this.basicCheckArr.push(row)
        }
      } else {
        let index = this.basicCheckArr.findIndex((item) => item.company_id == row.company_id)
        if (index != -1) {
          this.basicCheckArr.splice(index, 1)
        }
      }
    },

    // 勾选列表的取消删除逻辑
    handleCloseBasic(item) {
      let index = this.basicCheckArr.findIndex((sitem) => sitem.company_id == item.company_id)
      if (index != -1) {
        this.basicCheckArr.splice(index, 1)
        this.$refs.tableBody.setCheckBoxFalse(item)
      }
    },
    handleSubmit(arr) {
      this.column = arr
    },
    handleCloseDialog() {
      this.productSelectDialogVisible = false
    },
    isColorStr(str) {
      const titleStr = ['近一月收益率', '近一月最大回撤', '近一月Sharpe比率', '今年以来收益率', '今年以来最大回撤', '今年以来Sharpe比率']
      if (titleStr.indexOf(str) === -1) {
        return false
      } else {
        return true
      }
    },
    getParamsObject() {},

    handleExcelExport() {
      this.$emit('excelexport')
    },
    handleSortTable(val) {
      this.$emit('sorttable', val)
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
        this.$confirm('此操作将取消该管理人所有关注分组, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            const params = {
              mgrCode: row.company_id || ''
            }
            deleteAllFocus(params).then((res) => {
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
     * @description 批量关注
     */
    handleBatchFocus() {
      const _arr = this.basicCheckArr
      // const _arr = this.$refs.tableBody.getTableDataCheckRows()
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
     * @description 跳转管理人详情
     */
    jumpToManager(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: row }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.tabletable {
  margin: 0px 20px 12px 16px;
}
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
  margin-top: 15px;
  padding-left: 10px;

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
  background-color: #0f65dd;
}

.title-style {
  color: #0f65dd;
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
