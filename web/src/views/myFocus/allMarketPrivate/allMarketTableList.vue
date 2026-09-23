<template>
  <div class="tabletable">
    <ToolBarSlot>
      <template slot="left">
        <el-button size="small" type="primary" @click="handleCreateComb">创建模拟组合</el-button>
        <el-button size="small" type="info" plain @click="handleCancelBatchFocus">取消关注</el-button>
        <el-button size="small" type="info" plain @click="removeGroup">移动分组</el-button>
        <el-button size="small" type="info" plain @click="onContrast">对比</el-button>
      </template>
      <template slot="right">
        <el-button :disabled="isDisabled" :icon="exportLoading ? 'el-icon-loading' : ''" size="small" type="info" plain @click="handleExcelExport">导出Excel</el-button>
        <el-button size="small" type="info" plain @click="productSelectDialogVisible = true">自定义指标</el-button>
      </template>
    </ToolBarSlot>
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
      pageType="focus"
      @checkbox="handleCheckBoxChange"
      @focusstatus="handleFocus"
      @linkto="jumpToSingle"
      @linktomanger="jumpToManager"
      @sorttable="handleSortTable"
      @remarkRow="handleRemarkEmit"
    ></table-body>
    <table-head :table-column="column" :table-column-selector-visible="productSelectDialogVisible" @dialogclose="handleCloseDialog" @submit="handleSubmit"></table-head>
    <focus-dialog
      :current-group-id="currentGroupId"
      :is-show-focus="isShowFocus"
      :page="pageType"
      :select-row-data="selectRowData"
      :soucre="soucre"
      :title="title"
      @updateFocusStatus="updateFocusStatus"
    ></focus-dialog>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      title="备注"
      :visible.sync="remarkDialogVisible"
      width="40%"
      @close="
        () => {
          remarkDialogVisible = false
        }
      "
    >
      <el-row type="flex" justify="center">
        <el-form :model="remarkDialogFormQuery" :rules="remarkDialogRules" ref="remarkDialogRef">
          <el-form-item label="备注" prop="remark">
            <el-input type="textarea" :rows="4" placeholder="请输入内容" v-model="remarkDialogFormQuery.remark" :maxlength="100" show-word-limit></el-input>
          </el-form-item>
        </el-form>
      </el-row>
      <div slot="footer" class="standard-form dialog-footer" style="text-align: center">
        <el-button
          type="info"
          plain
          size="small"
          @click="
            () => {
              remarkDialogVisible = false
            }
          "
        >
          取 消
        </el-button>
        <el-button type="primary" size="small" @click="handleRemarkSubmit">提 交</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import tableBody from '@/components/tableBodyComponent'
import tableHead from '@/components/tableHeadComponent'
import focusDialog from '@/components/Bussiness/focusDialog'
import { handleBatchCancelFocusGroup, handleCancelFocusGroup, handleRemark } from './scripts/api'
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
      required: true,
      default: false
    },
    isDisabled: {
      type: Boolean,
      required: true,
      default: false
    },
    tableLoading: {
      type: Boolean,
      required: true,
      default: false
    },
    soucre: {
      type: String,
      default: ''
    },
    currentGroupId: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      remarkDialogVisible: false,
      remarkRow: null,
      remarkDialogFormQuery: {
        remark: ''
      },
      remarkDialogRules: {
        remark: [{ required: true, message: '备注不能为空', trigger: 'blur' }]
      },
      basicCheckArr: [],
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
          label: '近六月走势',
          id: 'options',
          disabled: true,
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '110px',
          noshowoverflowtooltip: true,
          filter: 'echarts',
          sortable: false
        },
        {
          label: '投资策略',
          id: 'fofMainStrategyName',
          type: 'leftTreeData',
          align: 'left',
          fix: '',
          width: '100px',
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
          width: '100px',
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
          width: '100px',
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
        /*{
          label: '绩效评级',
          id: 'frating',
          type: 'leftTreeData',
          align: 'center',
          fix: '',
          width: '150px',
          noshowoverflowtooltip: true,
          filter: 'star',
          sortable: true
        },*/
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
          label: '复权累计净值',
          id: 'cumulativeNav',
          type: 'centerTreeDataCenter',
          align: 'right',
          fix: '',
          width: '130px',
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
        // ,
        // {
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
      pageType: 'MYFOCUS'
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
    handleRemarkSubmit() {
      this.$refs.remarkDialogRef.validate(valid => {
        if (valid) {
          if (this.remarkRow && this.remarkRow.fundCode) {
            let params = {
              fundCode: this.remarkRow.fundCode,
              remark: this.remarkDialogFormQuery.remark
            }
            handleRemark(params)
              .then(res => {
                let { status } = res.data
                if (status == 0) {
                  this.$message.closeAll()
                  this.$message({
                    type: 'success',
                    message: '更新备注成功',
                    customClass: 'message-success'
                  })
                  this.$nextTick(() => {
                    this.$emit('updatelist')
                  })
                  this.remarkDialogVisible = false
                } else {
                  this.$message.closeAll()
                  this.$message({
                    type: 'warning',
                    message: '更新备注失败',
                    customClass: 'message-warning'
                  })
                }
              })
              .catch(err => {
                this.$message.closeAll()
                this.$message({
                  type: 'warning',
                  message: '更新备注失败',
                  customClass: 'message-warning'
                })
              })
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '产品代码不存在，保存错误',
              customClass: 'message-warning'
            })
          }
        } else {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '请按照提示修改',
            customClass: 'message-warning'
          })
        }
      })
    },
    handleRemarkEmit(row) {
      this.remarkRow = row
      if (row.remark) {
        this.remarkDialogFormQuery.remark = row.remark
      } else {
        this.remarkDialogFormQuery.remark = ''
      }
      this.remarkDialogVisible = true
    },
    handleCreateComb() {
      let _arr = this.basicCheckArr
      if (_arr.length <= 0) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请选择产品',
          customClass: 'message-warning'
        })
        return
      }

      // 判断是否存在没有权限的产品情况
      for (let i = 0; i < this.basicCheckArr.length; i++) {
        let temp = this.basicCheckArr[i]
        if (temp.isPermission == '' || temp.isPermission == null || temp.isPermission == undefined) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '您所选的产品中包含无权限的产品，请重新选择。',
            customClass: 'message-warning'
          })
          return
        } else if (temp.isPermission == '0') {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '您所选的产品中包含无权限的产品，请重新选择。',
            customClass: 'message-warning'
          })
          return
        }
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
    onContrast() {
      const list = this.basicCheckArr
      if (list.length > 5) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '对比产品不能超过5个',
          customClass: 'message-warning'
        })
        return
      }
      if (list.length >= 2) {
        // 判断是否存在没有权限的产品情况
        for (let i = 0; i < this.basicCheckArr.length; i++) {
          let temp = this.basicCheckArr[i]
          if (temp.isPermission == '' || temp.isPermission == null || temp.isPermission == undefined) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '您所选的产品中包含无权限的产品，请重新选择。',
              customClass: 'message-warning'
            })
            return
          } else if (temp.isPermission == '0') {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '您所选的产品中包含无权限的产品，请重新选择。',
              customClass: 'message-warning'
            })
            return
          }
        }

        this.$store.commit('SET_FROMPAGEJUMP', true)
        this.$router.push({
          path: '/tqgl/smcpxx',
          query: { list: list }
        })
      } else {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '请至少选择两个产品',
          customClass: 'message-warning'
        })
      }
    },
    handleCloseDialog() {
      this.productSelectDialogVisible = false
    },
    handleSubmit(arr) {
      this.column = arr
    },
    /**
     * @description 批量取消关注
     */
    handleCancelBatchFocus() {
      const _arr = this.basicCheckArr
      // const _arr = this.$refs.tableBody.getTableDataCheckRows()
      if (_arr && _arr.length) {
        const params = {}
        params.myConcernList = _arr.map(item => {
          return {
            fundCode: item.fundCode,
            flag: item.source
          }
        })
        // params.fundCodes = _arr.map(item => item.fundCode).join(',')
        params.poolCode = this.currentGroupId
        // params.flags = _arr.map(item => item.source).join(',')
        this.$confirm('此操作将批量取消产品关注, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
          cancelButtonClass: 'standard-cancel'
        })
          .then(() => {
            handleBatchCancelFocusGroup(params).then(res => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '取消成功',
                  customClass: 'message-success'
                })
                this.updateFocusStatus('refesh')
              } else {
                this.$message({
                  type: 'error',
                  message: res.data.message || '取消失败',
                  customClass: 'message-error'
                })
              }
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消操作'
            })
          })
      } else {
        this.selectRowData = []
        this.$message({
          type: 'warning',
          message: '请选择产品',
          customClass: 'message-warning'
        })
      }
    },
    /**
     * @description 单个关注/取消关注
     */
    handleFocus(row) {
      if (row.isConcern === '1') {
        const params = {}
        params.fundCode = row.fundCode
        params.poolCode = this.currentGroupId
        params.flag = row.source
        this.$confirm('此操作将取消对该产品关注, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
          cancelButtonClass: 'standard-cancel'
        })
          .then(() => {
            handleCancelFocusGroup(params).then(res => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '取消成功',
                  customClass: 'message-success'
                })
                this.updateFocusStatus('refesh')
              } else {
                this.$message({
                  type: 'error',
                  message: res.data.message || '取消失败',
                  customClass: 'message-error'
                })
              }
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消操作'
            })
          })
      } else {
        this.selectRowData = [row]
        this.isShowFocus = true
      }
    },
    /**
     * @description 移动分组
     */
    removeGroup() {
      const _arr = this.basicCheckArr
      // const _arr = this.$refs.tableBody.getTableDataCheckRows()
      if (_arr && _arr.length) {
        this.isShowFocus = true
        this.selectRowData = _arr
        this.title = '移动分组'
      } else {
        this.selectRowData = []
        this.$message({
          type: 'warning',
          message: '请选择产品',
          customClass: 'message-warning'
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
      // 判断产品是否有权限
      if (row.isPermission == '' || row.isPermission == null || row.isPermission == undefined) {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '您无此产品查看权限。',
          customClass: 'message-warning'
        })
        return
      } else if (row.isPermission == '0') {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '您无此产品查看权限。',
          customClass: 'message-warning'
        })
        return
      }

      this.$store.commit('SET_FROMPAGEJUMP', true)
      this.$router.push({
        path: '/tqgl/dcpfx',
        query: { list: row }
      })
    },
    /**
     * @description 跳转管理人详情
     */
    jumpToManager(row) {
      this.$store.commit('SET_FROMPAGEJUMP', true)
      let newObj = {
        company_id: row.company_id,
        manager_name: row.companyName
      }
      this.$router.push({
        path: '/tqgl/glrxq',
        query: { managerList: newObj }
      })
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

::v-deep .el-button.el-button--info {
  color: #404040;
  background-color: #ffffff;
  border-color: #d1d3d6;
}
::v-deep .el-button.el-button--info:hover {
  color: #0f65dd;
  background-color: #ffffff;
  border-color: #0f65dd;
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
</style>
