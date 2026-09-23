<template>
  <div class="privateIndexComponent">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
          <el-row>
            <el-col :span="24">
              <el-form-item label="私募指数" prop="indexCode">
                <el-select v-model="formInline.indexCode" size="small" clearable filterable placeholder="请选择私募指数">
                  <el-option v-for="item in indexListOptions" :key="item.indexCode" :label="item.indexName" :value="item.indexCode" />
                </el-select>
              </el-form-item>
              <el-form-item label="证券代码" prop="symbolCode">
                <el-input v-model="formInline.symbolCode" size="small" clearable placeholder="请输入证券代码"></el-input>
              </el-form-item>
              <el-form-item label="证券名称" prop="symbolName">
                <el-input v-model="formInline.symbolName" size="small" clearable placeholder="请输入证券名称"></el-input>
              </el-form-item>



              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="handleResetForm">重置</el-button>
                <el-button v-btn="'privateindexcomponentadd'" type="primary" size="small" icon="el-icon-plus" @click="handleAddPrivateIndexComponent">新增</el-button>
                <el-button v-btn="'privateindexcomponentbatchadd'" type="info" size="small" icon="el-icon-plus" @click="handleAddBatchPrivateIndexComponent">批量导入</el-button>
                <el-button v-btn="'privateindexcomponentbatchdel'" type="info" size="small" icon="el-icon-delete" @click="handleDeleteBatchPrivateIndexComponent">批量删除</el-button>
                <el-button v-btn="'privateindexcomponentexcel'" type="info" size="small"  :icon="exportLoading ? 'el-icon-loading' : 'el-icon-download'" :disabled="isDisabled" @click="exportData">
                  {{ downLoadText }}
                </el-button>

              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          v-loading="tableLoading"
          ref="refsTable"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          :seq-config="{seqMethod}"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          :sort-config="{ remote: true }"
          style="width: 100%"
          @sort-change="customSortMethod"
          resizable

        >
          <vxe-table-column type="selection" width="35" align="center"></vxe-table-column>
          <vxe-table-column
            v-for="(item, index) in column"
            :key="item.prop + index"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.title"
            :min-width="item.width"
            header-align="center"
            :sortable="item.sortable"
          >
            <template slot-scope="{ row }">

              <div v-if="item.prop === 'symbolType'">
                <span  v-if="row[item.prop] == 'PRODUCT'">产品类型</span>
                <span  v-else>指数类型</span>
              </div>
              <div v-else>
              <span> {{ row[item.prop] | noDataFilter }}</span>
              </div>

            </template>
          </vxe-table-column>
          <vxe-table-column title="操作" align="center" width="250px" fixed="right">
            <template slot-scope="scope">
              <span class="table-operation" style="color:#A15008">

                 <el-button  v-btn="'privateindexcomponentupdate'"  type="info" plain size="small" @click="handleEditPrivateIndexComponent(scope.row)">修改</el-button>
                 <el-button  v-btn="'privateindexcomponentdelete'"  type="info" plain size="small" @click="handleDeletePrivateIndexComponent(scope.row)">删除</el-button>

              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <div class="table-footer">
          <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
        </div>
      </div>
    </div>

    <el-dialog
      v-if="dialogVisibleEdit"
      :title="dialogTitleEdit"
      :visible.sync="dialogVisibleEdit"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeDialog"
    >
      <edit-private-index-component
        v-if="dialogVisibleEdit"
        :is-edit="isEdit"
        :cur-row="curRow"
        @closeDialog="closeDialog"
      ></edit-private-index-component>
    </el-dialog>


    <el-dialog
      v-if="addBatchDialogVisible"
      :title="addBatchDialogTitle"
      :visible.sync="addBatchDialogVisible"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeAddBatchDialog"
    >
      <import-private-index-component
        v-if="addBatchDialogVisible"
        @closeDialog="closeAddBatchDialog"
      ></import-private-index-component>
    </el-dialog>

  </div>
</template>

<script>
import { TABLE_INDEXCOMPONENT_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import {
  selectPrivateIndexComponentByPage,
  deletePrivateIndexComponent,
  deleteBatchPrivateIndexComponent,
  selectPrivateIndexList,
} from './scripts/api'

import commonFun from '@/filters/common.js'
import editPrivateIndexComponent from './components/edit-private-index-component.vue'
import { downLoadFileByUrl } from '@/utils'
import importPrivateIndexComponent from './components/import-private-index-component.vue'

export default {
  name: 'privateIndexComponent',
  components: {
    editPrivateIndexComponent,
    importPrivateIndexComponent,
    Pagination
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        indexCode: '',
        symbolCode: '',
        symbolName:'',
        orderString: ''
      },
      indexListOptions:[],
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_INDEXCOMPONENT_COLUMNS,

      // 分页信息
      pageList: {
        _pageSize: 10,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 模板配置弹窗标题
      dialogTitle: '',
      // 模板配置弹窗状态
      dialogVisible: false,
      // 编辑弹窗标题
      dialogTitleEdit: '',
      // 编辑弹窗状态
      dialogVisibleEdit: false,
      // 新增 | 编辑状态

      isEdit: false,

      /* 按钮禁止与否 */
      isDisabled: false,
      // 导出图标
      downLoadIcon: "el-icon-download",
      // 导出提示文字
      downLoadText: "导出",
      exportLoading: false,
      //分类

      //批量导入窗口标题
      addBatchDialogTitle: '',
      // 批量导入窗口状态
      addBatchDialogVisible: false,
      // 编辑弹窗标题
      // 当前编辑行数据
      curRow: {},
    }
  },
  mounted() {
    // 查询表格
    this.getIndexListOptions();
    this.initData()
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  },
  methods: {

    /**
     * @description 初始化数据
     */
    initData() {

      this.handleSearchTable()
    },
    getIndexListOptions(){

      selectPrivateIndexList({}).then(res => {
        let { status, data } = res.data
        if (status === 200) {
          this.indexListOptions = data
        }
      })
    },

    // 批量删除数据
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },


    /* 自定义序号显示 */
    seqMethod({ rowIndex }) {
      return (
        (this.pageList._pageNum - 1) * this.pageList._pageSize + rowIndex + 1
      );
    },

    /**
     * @description 表单重置
     */
    handleResetForm() {

        // this.formInline.indexCode = ''
        // this.formInline.indexName = ''
        // this.formInline.indexClassify = ''
        // this.formInline.orderString = ''
      this.$refs['formInline'].resetFields()
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },


    /**
     * @description 表格查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)

      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      const data = this.parameterSrc(params)
      // console.log("data:"+JSON.stringify(data))
      this.tableLoading = true
      this.tableData = []
      selectPrivateIndexComponentByPage(data)
        .then((res) => {
          if (res.data.status === 200) {
            this.tableData = res.data.data.rows || []
           // console.log('tableData', this.tableData)
            this.total = res.data.data.total || 0
            this.tableLoading = false
          } else {
            this.tableLoading = false
            this.$message({
              type: 'error',
              message: res.data.message || '查询失败',
              customClass: 'message-error'
            })
          }
        })
        .catch((e) => {
          this.tableLoading = false
        })
    },



    /**
     * @description 新增指数
     */
    handleAddPrivateIndexComponent() {
      this.dialogTitleEdit = '新增私募指数成分'
      this.dialogVisibleEdit = true
      this.curRow={}
      this.isEdit = false
    },
    /**
     * @description 修改指数
     */
    handleEditPrivateIndexComponent(row) {
      this.dialogTitleEdit = '编辑私募指数成分'
      this.dialogVisibleEdit = true

      this.curRow = JSON.parse(JSON.stringify(row))
      this.isEdit = true
    },


    /**
     * @description 新增分类
     */
    handleAddBatchPrivateIndexComponent() {
      this.addBatchDialogTitle = '批量上传私募指数成分文件'
      this.addBatchDialogVisible = true
    },




    /**
     * @description 删除私募指数成分
     */
    handleDeletePrivateIndexComponent(row) {
      this.$confirm('是否确定删除私募指数成分?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            id: row.id
          }
          deletePrivateIndexComponent(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '删除失败',
                customClass: 'message-error'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },

    /**
     * @description 批量删除私募指数成分
     */
    handleDeleteBatchPrivateIndexComponent() {
      const selectedRecords = this.$refs.refsTable.getCheckboxRecords(); // 获取所有选中行数据
      let arr = []
      selectedRecords.map(item => arr.push(item.id)); // 获取选中行的ID数组
      if (arr.length >= 0) {
        this.$confirm('是否确定删除选中的私募指数成分?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
          cancelButtonClass: 'standard-cancel'
        })
          .then(() => {
            // 批量删除
            const params = {
              ids: arr.join(',')
            }
            deleteBatchPrivateIndexComponent(params).then((res) => {
              if (res.data.status === 200) {
                this.$message({
                  type: 'success',
                  message: '删除成功',
                  customClass: 'message-success'
                })
                this.handleSearchTable()
              } else {
                this.$message({
                  type: 'error',
                  message: '删除失败',
                  customClass: 'message-error'
                })
              }
            })
          })
          .catch(() => {
            this.$message({
              type: 'info',
              message: '已取消'
            })
          })
      }
      else if (arr.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量删除的数据',
          type: 'warning'
        })
      }
    },



    /**
     * @description 关闭弹窗
     */
    closeDialog(status) {
      this.dialogTitle = ''
      this.dialogVisible = false
      this.dialogTitleEdit = ''
      this.dialogVisibleEdit = false
      if (status === 'REFESH') this.handleSearchTable()
    },


    /**
     * @description 关闭弹窗
     */
    closeAddBatchDialog(status) {
      this.addBatchDialogTitle = ''
      this.addBatchDialogVisible = false

      if (status === 'REFESH') this.handleSearchTable()
    },
    //导出数据
    exportData() {
      this.downLoadText = "导出中...";
      this.exportLoading = true;
      this.isDisabled = true;
      const params = Object.assign({}, this.formInline, {});
      const fileName = '私募指数成分列表.xls'
      const url = '/api/gfprivateindexcomponent/downPrivateIndexComponent'
      downLoadFileByUrl(url, params, fileName, this)
      setTimeout(() => {
        this.tableLoading = false;
        this.exportLoading = false;
        this.isDisabled = false;
        this.downLoadText = "导出";
      }, 5000)


    },

  },




}
</script>
<style lang="scss" scoped>
.pagination-container {
  .el-input {
    width: 100px !important;
  }
}
::v-deep .el-dialog.customClass {
  width:45% !important;
}
.customClass .el-dialog__body .privateIndexComponent .el-form {
  width: 100% !important;
}
::v-deep .vxe-table--render-default .vxe-cell--checkbox:not(.is--disabled):hover .vxe-checkbox--icon:before {
  border-color: #e9c5a5!important
}
</style>


