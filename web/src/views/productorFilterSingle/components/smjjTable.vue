<template>
  <div class="tabletable">
    <!--    <el-row justify="space-around" type="flex" class="mb8">
      <el-col :span="12">
        &lt;!&ndash;        <div style="vertical-align: middle; display: inline-block">
          <div class="color-box"></div>
        </div>
        <div class="title-style">
          私募产品
          &lt;!&ndash;          <el-tooltip class="table_header_icon" effect="dark" placement="top">&ndash;&gt;
          &lt;!&ndash;            <span slot="content">&ndash;&gt;
          &lt;!&ndash;              CMS代表广发托管/外包产品，对于市场产品点击其名称进入单产品分析页面后可发起验证请求，有用户提交验证申请后会显示待验证标记，后台人员进行验证处理后将显示已验证标记。&ndash;&gt;
          &lt;!&ndash;            </span>&ndash;&gt;
          &lt;!&ndash;            <i class="el-icon-question" style="cursor: pointer;"></i>&ndash;&gt;
          &lt;!&ndash;          </el-tooltip>&ndash;&gt;
        </div>&ndash;&gt;
      </el-col>
      <el-col :span="12">
        <div style="display: flex; float: right">
          &lt;!&ndash; <el-button size="small" type="primary" @click="handleCreateComb">创建模拟组合</el-button> &ndash;&gt;
          &lt;!&ndash; <el-button size="small" type="info" @click="onContrast">对比</el-button>
          <el-button size="small" type="info" @click="handleBatchFocus">
            批量关注
          </el-button>
          <el-button :disabled="isDisabled" size="small" type="info" @click="handleExcelExport">
            导出Excel
          </el-button>
          <el-button size="small" type="info" @click="productSelectDialogVisible = true">
            自定义指标
          </el-button> &ndash;&gt;
        </div>
      </el-col>
    </el-row>-->
    <div class="standard-form" style="display: flex; justify-content: space-between; margin: 10px 0">
      <span>
        <el-button size="small" type="primary" @click="handleCreateComb">创建模拟组合</el-button>
        <el-button size="small" type="info" plain @click="onContrast">对比</el-button>
        <el-button size="small" type="info" plain @click="handleBatchFocus">批量关注</el-button>
      </span>
      <span>
        <el-button :disabled="isDisabled" size="small" type="info" plain @click="handleExcelExport">导出Excel</el-button>
        <el-button size="small" type="info" plain @click="productSelectDialogVisible = true">自定义指标</el-button>
      </span>
    </div>
    <div v-if="basicCheckArr && basicCheckArr.length" class="mb10">
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
      pageType="filter"
      @checkbox="handleCheckBoxChange"
      @focusstatus="handleFocus"
      @linkto="jumpToSingle"
      @sorttable="handleSortTable"
    ></table-body>
    <table-head :table-column="column" :table-column-selector-visible="productSelectDialogVisible" @dialogclose="handleCloseDialog" @submit="handleSubmit"></table-head>
    <focus-dialog
      :is-show-focus="isShowFocus"
      :page="pageType"
      :select-row-data="selectRowData"
      :soucre="soucre"
      :title="title"
      @updateFocusStatus="updateFocusStatus"
    ></focus-dialog>
  </div>
</template>

<script>
import tableBody from '@/components/tableBodyComponent'
import tableHead from '@/components/tableHeadComponent'
import focusDialog from '@/components/Bussiness/focusDialog'
import { deleteAllFocus } from '../scripts/api'

export default {
  components: { tableBody, tableHead, focusDialog },
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
          width: '250px',
          noshowoverflowtooltip: true,
          filter: 'fund',
          sortable: true
        },
        {
          label: '投资策略',
          id: 'fofMainStrategyName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '子策略',
          id: 'fofSubStrategyName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '三级策略',
          id: 'fofThirdStrategyName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },
        {
          label: '产品管理人',
          id: 'companyName',
          type: 'centerTreeDataLeft',
          align: 'left',
          fix: '',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: '',
          sortable: true
        },

        // {
        //   label: '基金经理',
        //   id: 'managerName',
        //   type: 'leftTreeData',
        //   align: 'left',
        //   fix: '',
        //   width: '100px',
        //   noshowoverflowtooltip: true,
        //   filter: '',
        //   sortable: true
        // },
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
          label: '累计净值',
          id: 'addedNav',
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
          label: '近一月最大回撤',
          id: 'm1_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一月Sharpe比率',
          id: 'm1_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
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
          label: '近三月最大回撤',
          id: 'm3_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近三月Sharpe比率',
          id: 'm3_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
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
          label: '近六月最大回撤',
          id: 'm6_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近六月Sharpe比率',
          id: 'm6_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
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
          label: '近一年最大回撤',
          id: 'y1_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '近一年Sharpe比率',
          id: 'y1_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
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
          label: '今年以来最大回撤',
          id: 'ytd_max_retracement',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '100px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        },
        {
          label: '今年以来Sharpe比率',
          id: 'ytd_sharpe',
          type: 'centerTreeDataRight',
          align: 'right',
          fix: '',
          width: '140px',
          noshowoverflowtooltip: true,
          filter: 'numberToFixedStr',
          sortable: true
        }
        // ,{
        //   label: '管理规模区间',
        //   id: 'managerAsset',
        //   type: 'centerTreeDataLeft',
        //   align: 'right',
        //   fix: '',
        //   width: '130px',
        //   noshowoverflowtooltip: true,
        //   filter: '',
        //   sortable: true
        // }
      ],
      selectRowData: [],
      isShowFocus: false,
      title: '关注',
      pageType: 'ALLMARKET',
      soucre: ''
    }
  },
  mounted() {
    // const xTable = this.$refs.vxetable
    // xTable.connect(this.$refs.xToolbar)
  },
  methods: {
    getSelectedColumnIds() {
      return this.column.map(col => col.id);
    },
    formatFundName(row) {
     if(row.gfSelling=='代销') {
       return "<span>"+ row.fundName+"</span><span style=\"padding-left: 10px;\"><span className=\"greenGfSelling\">代销</span></span>"
     }else{
       return "<span>"+ row.fundName+"</span>"
     }

    },
    handleCreateComb() {
      let _arr = this.basicCheckArr
      if (_arr.length <= 0) {
        this.$message.closeAll()
        this.$message.warning('请选择产品')
        return
      }

      this.$store.commit('SET_FROMCREATESUMUCOMB', true)
      this.$router.push({
        path: '/tqgl/cjmnzh',
        query: {
          checkArr: _arr
        }
      })
    },
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

    // 对比产品
    onContrast() {
      // 直接从
      // const list = this.$refs.tableBody.getTableDataCheckRows()
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
    },
    handleCloseDialog() {
      this.productSelectDialogVisible = false
      this.$refs.tableBody.$refs.vxetable.refreshColumn()
      this.$forceUpdate()
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
      this.soucre = row.source
      if (row.isConcern === '0') {
        this.selectRowData = [row]
        this.isShowFocus = true
        this.title = '关注'
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
              fundCode: row.fundCode || '',
              flag: row.source || ''
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
      console.log(row, 'row')
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: { fundCode: row.fundCode, source: row.source, fundName: row.fundName } }
      })
    },
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      const manager_name = row.companyName
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: { company_id: row.company_id, manager_name } }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.tabletable {
  margin: 0 10px 0px 0px;
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
  //margin-top: 10px;
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
::v-deep .el-tag {
  border: none;
  background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  span {
    color: #612d10 !important;
  }
  .el-tag__close {
    color: #612d10 !important;
  }
  .el-tag__close:hover {
    background-color: transparent;
  }
}
::v-deep .vxe-table--render-default .vxe-cell--checkbox:not(.is--disabled):hover .vxe-checkbox--icon:before {
  border-color: #e9c5a5!important
}

</style>
