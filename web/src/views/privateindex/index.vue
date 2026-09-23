<template>
  <div class="privateIndex">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
          <el-row>
            <el-col :span="24">
              <el-form-item label="指数代码" prop="indexCode">
                <el-input v-model="formInline.indexCode" size="small" clearable placeholder="请输入指数代码"></el-input>
              </el-form-item>
              <el-form-item label="指数名称" prop="indexName">
                <el-input v-model="formInline.indexName" size="small" clearable placeholder="请输入指数名称"></el-input>
              </el-form-item>

              <el-form-item label="分类" prop="indexClassify">
                <el-select v-model="formInline.indexClassify" size="small" clearable filterable placeholder="请选择指数分类">
                  <el-option v-for="item in indexClassifyOptions" :key="item.indexClassify" :label="item.indexClassifyName" :value="item.indexClassify" />
                </el-select>
              </el-form-item>

              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="handleResetForm">重置</el-button>
                <el-button v-btn="'privateindexadd'" type="primary" size="small" icon="el-icon-plus" @click="handleAddPrivateIndex">新增指数</el-button>
                <el-button v-btn="'privateindexclassifyadd'" type="info" size="small" icon="el-icon-plus" @click="handleAddPrivateIndexClassify">新增分类</el-button>
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
                <span v-if="item.prop === 'indexStatus'">
                  <el-tag size="mini" type="success" v-if="row[item.prop] == '0'">启用</el-tag>
                  <el-tag size="mini" type="danger" v-else>停用</el-tag>
                </span>
              <div v-else-if="item.prop === 'homePageShow'">
                <span  v-if="row[item.prop] == '1'">首页显示</span>
                <span  v-else>首页隐藏</span>
              </div>
              <div v-else>
              <span> {{ row[item.prop] | noDataFilter }}</span>
              </div>

            </template>
          </vxe-table-column>
          <vxe-table-column title="操作" align="center" width="450px" fixed="right">
            <template slot-scope="scope">
              <span class="table-operation" style="color:#A15008">
                 <span v-if="scope.row['indexStatus'] ==='0'">
                   <a  v-btn="'privateindexdisable'"  type="info" plain size="small" @click="handlePrivateIndexDisable(scope.row)">停用</a>
                 </span>
                 <span v-else>
                   <a  v-btn="'privateindexable'"  type="info" plain size="small" @click="handlePrivateIndexAble(scope.row)">启用</a>
                 </span>

                 <span v-if="scope.row['homePageShow'] === '1'">
                   <a  v-btn="'privateindexhomepagehide'"  type="info" plain size="small" @click="handleHideHomePage(scope.row)">首页隐藏</a>
                 </span>
                 <span v-else>
                   <a  v-btn="'privateindexhomepageshow'"  type="info" plain size="small" @click="handleShowHomePage(scope.row)">首页显示</a>
                 </span>

                 <a  v-btn="'privateindexupdate'"  type="info" plain size="small" @click="handleEditPrivateIndex(scope.row)">修改指数</a>
                 <a  v-btn="'privateindexdelete'"  type="info" plain size="small" @click="handleDeletePrivateIndex(scope.row)">删除指数</a>
                 <a  v-btn="'privateindexclassifyupdate'"  type="info" plain size="small" @click="handleEditPrivateIndexClassify(scope.row)">修改分类</a>
                 <a  v-btn="'privateindexclassifydelete'"  type="info" plain size="small" @click="handleDeletePrivateIndexClassify(scope.row)">删除分类</a>
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
      <edit-private-index
        v-if="dialogVisibleEdit"
        :is-edit="isEdit"
        :cur-row="curRow"
        @closeDialog="closeDialog"
      ></edit-private-index>
    </el-dialog>


    <el-dialog
      v-if="classifyDialogVisibleEdit"
      :title="classifyDialogTitleEdit"
      :visible.sync="classifyDialogVisibleEdit"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      custom-class="customClass"
      @close="closeClassifyDialog"
    >
      <edit-private-index-classify
        v-if="classifyDialogVisibleEdit"
        :is-edit="classifyIsEdit"
        :cur-row="curRow"
        @closeDialog="closeClassifyDialog"
      ></edit-private-index-classify>
    </el-dialog>

  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import { selectPrivateIndexByPage, selectPrivateIndexClassifyList,deletePrivateIndex,deletePrivateIndexClassify } from './scripts/api'
import { setPrivateIndexDisable,setPrivateIndexAble,setPrivateIndexHomePageShowStatus,setPrivateIndexHomePageHideStatus } from './scripts/api'
import commonFun from '@/filters/common.js'
import editPrivateIndex from './components/edit-private-index'
import editPrivateIndexClassify from './components/edit-private-index-classify.vue'

export default {
  name: 'privateIndex',
  components: {
    editPrivateIndex,
    editPrivateIndexClassify,
    Pagination
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        indexCode: '',
        indexName: '',
        indexClassify:'',
        orderString: ''
      },
      indexClassifyOptions:[],
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,

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
      //分类

      classifyDialogTitle: '',
      // 模板配置弹窗状态
      classifyDialogVisible: false,
      // 编辑弹窗标题
      classifyDialogTitleEdit: '',
      // 编辑弹窗状态
      classifyDialogVisibleEdit: false,
      classifyIsEdit: false,
      // 当前编辑行数据
      curRow: {},
    }
  },
  mounted() {
    // 查询表格
    this.getIndexClassifyOptions();
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
    getIndexClassifyOptions(){

      selectPrivateIndexClassifyList({}).then(res => {
        let { status, data } = res.data
        if (status === 200) {
          this.indexClassifyOptions = data
        }
      })
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
      selectPrivateIndexByPage(data)
        .then((res) => {
          if (res.data.status === 200) {
            this.tableData = res.data.data.rows || []
            //console.log('tableData', this.tableData)
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
    handlePrivateIndexDisable(row){
      this.$confirm('是否确定停用', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexCode: row.indexCode
          }
          setPrivateIndexDisable(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '停用成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '停用失败',
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
    handlePrivateIndexAble(row){
      this.$confirm('是否确定启用', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexCode: row.indexCode
          }
          setPrivateIndexAble(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '启用成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '启用失败',
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
    handleHideHomePage(row){
      this.$confirm('是否确定首页隐藏', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexCode: row.indexCode
          }
          setPrivateIndexHomePageHideStatus(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '首页隐藏成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '首页隐藏失败',
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
    handleShowHomePage(row){
      this.$confirm('是否确定首页显示', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexCode: row.indexCode
          }
          setPrivateIndexHomePageShowStatus(params).then((res) => {
            if (res.data.status === 200) {
              this.$message({
                type: 'success',
                message: '首页显示成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                type: 'error',
                message: '首页显示失败',
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
     * @description 新增指数
     */
    handleAddPrivateIndex() {
      this.dialogTitleEdit = '新增指数'
      this.dialogVisibleEdit = true
      this.curRow={}
      this.isEdit = false
    },
    /**
     * @description 修改指数
     */
    handleEditPrivateIndex(row) {
      this.dialogTitleEdit = '编辑指数'
      this.dialogVisibleEdit = true
      this.curRow = JSON.parse(JSON.stringify(row))
      this.isEdit = true
    },


    /**
     * @description 新增分类
     */
    handleAddPrivateIndexClassify() {
      this.classifyDialogTitleEdit = '新增分类'
      this.classifyDialogVisibleEdit = true
      this.curRow={}
      this.classifyIsEdit = false
    },
    /**
     * @description 修改指数
     */
    handleEditPrivateIndexClassify(row) {
      this.classifyDialogTitleEdit = '编辑分类'
      this.classifyDialogVisibleEdit = true
      this.curRow = JSON.parse(JSON.stringify(row))
      this.classifyIsEdit = true
    },




    /**
     * @description 删除私募指数
     */
    handleDeletePrivateIndex(row) {
      this.$confirm('是否确定删除私募指数?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexCode: row.indexCode
          }
          deletePrivateIndex(params).then((res) => {
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
     * @description 删除分类
     */
    handleDeletePrivateIndexClassify(row) {
      this.$confirm('是否确定删除分类?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            indexClassify: row.indexClassify
          }
          deletePrivateIndexClassify(params).then((res) => {
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
    closeClassifyDialog(status) {
      this.classifyDialogTitle = ''
      this.classifyDialogVisible = false
      this.classifyDialogTitleEdit = ''
      this.classifyDialogVisibleEdit = false
      if (status === 'REFESH') this.handleSearchTable()
    },
  },


}
</script>
<style lang="scss" scoped>
#privateIndex .pagination-container {
  .el-input {
    width: 100px !important;
  }
}
::v-deep .el-dialog.customClass {
  width:45% !important;
}
.customClass .el-dialog__body .privateIndex .el-form {
  width: 100% !important;
}
</style>


