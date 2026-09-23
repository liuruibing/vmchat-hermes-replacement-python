<template>
  <div class="hotOrgMaintenance">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
          <el-row>
            <el-col :span="24">
              <el-form-item label="" prop="regManageCode">
                <el-input v-model="formInline.regManageCode" size="medium" clearable placeholder="请输入登记编号/机构名称" style="width:250px"></el-input>
              </el-form-item>

              <el-form-item label="左侧状态" prop="leftStatus">
                <el-select v-model="formInline.leftStatus" size="small" clearable filterable placeholder="请选择左侧状态">
                  <el-option v-for="item in statusArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item label="右侧状态" prop="leftStatus">
                <el-select v-model="formInline.rightStatus" size="small" clearable filterable placeholder="请选择右侧状态">
                  <el-option v-for="item in statusArr" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>

              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="handleResetForm">重置</el-button>
                <el-button v-btn="'hotorgmaintenanceadd'" type="primary" size="small" icon="el-icon-plus" @click="handleAddHotReg">新增</el-button>

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
                <span v-if="item.prop === 'leftStatus'">
                  <el-tag size="mini" type="success" v-if="row[item.prop] == '1'">推送</el-tag>
                  <el-tag size="mini" type="danger" v-else>禁推</el-tag>
                </span>
               <span v-else-if="item.prop === 'rightStatus'">
                  <el-tag size="mini" type="success" v-if="row[item.prop] == '1'">推送</el-tag>
                  <el-tag size="mini" type="danger" v-else>禁推</el-tag>
                </span>
               <div v-else>
                <span> {{ row[item.prop] | noDataFilter }}</span>
              </div>

            </template>
          </vxe-table-column>
          <vxe-table-column title="操作" align="center" width="250px" fixed="right">
            <template slot-scope="scope">
              <span class="table-operation" style="color:#A15008">

                 <el-button  v-btn="'hotorgmaintenanceupdate'"  type="info" plain size="small" @click="handleEditHotReg(scope.row)">修改</el-button>
                 <el-button  v-btn="'hotorgmaintenancedelete'"  type="info" plain size="small" @click="handleDeleteHotReg(scope.row)">删除</el-button>

              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formInline.pageNum"
          :page-size="formInline.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          :page-sizes="pagerConfig.pageSizes"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"

        />
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
      <edit-hot-org
        v-if="dialogVisibleEdit"
        :is-edit="isEdit"
        :cur-row="curRow"
        @closeDialog="closeDialog"
      ></edit-hot-org>
    </el-dialog>




  </div>
</template>

<script>
import { TABLE_COLUMNS,STATUS_LIST } from './scripts/constants'
import Pagination from '@/components/Pagination'
import { selectHotOrgMaintenaceByPage,deleteHotReg } from './scripts/api'
import commonFun from '@/filters/common.js'
import editHotOrg from './components/edit-hot-org.vue'


export default {
  name: 'hotOrgMaintenance',
  components: {
    Pagination,
    editHotOrg
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        regManageCode: '',
        leftStatus:'',
        rightStatus:'',
        orderString: '',
        pageSize: 20,
        pageNum: 1
      },
      pagerConfig: {
        pageSizes: [10,20,50,100,500], // 每页显示条目数的选项
      },
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,
      statusArr:STATUS_LIST,

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

      this.handleSearchTable(false)
    },

    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },


    /**
     * @description 表单重置
     */
    handleResetForm() {

      this.$refs['formInline'].resetFields()
    },

    /**
     * @description 监听分页
     */
    pagination(val) {
      /*  let { page, limit } = val
       this.formInline.pageNum = page
       this.formInline.pageSize = limit
  */
      const { currentPage, pageSize } = val;
      // 起始页
      this.formInline.pageNum = currentPage;
      // 每页数量
      this.formInline.pageSize = pageSize;
      this.handleSearchTable(false)
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
    handleSearchTable(flag) {
      if (flag) {
        this.formInline.pageNum = 1
      }
      const params = Object.assign({}, this.formInline)

      const data = this.parameterSrc(params)
      // console.log("data:"+JSON.stringify(data))
      this.tableLoading = true
      this.tableData = []
      selectHotOrgMaintenaceByPage(data)
        .then((res) => {

          const {data, status} = res.data
          if (status === 200 && data) {
            this.tableData = data.list || []
            this.total = data.total || 0

          } else {
            this.tableData = []
            this.total = 0
          }
          this.tableLoading = false
        })
        .catch((e) => {
          this.tableLoading = false
        })
    },



    /**
     * @description 新增热点推荐机构
     */
    handleAddHotReg() {
      this.dialogTitleEdit = '新增热点推荐机构'
      this.dialogVisibleEdit = true
     // this.curRow={"leftStatus":"1","rightStatus":"1","id":0,"leftOrder":100,"rightOrder":50}
      this.curRow={}
      this.isEdit = false
    },
    /**
     * @description 修改热点推荐机构
     */
    handleEditHotReg(row) {
      this.dialogTitleEdit = '编辑热点推荐机构'
      this.dialogVisibleEdit = true
      this.curRow = JSON.parse(JSON.stringify(row))
      this.isEdit = true
    },





    /**
     * @description 删除私募指数
     */
    handleDeleteHotReg(row) {
      this.$confirm('是否确定删除热点推荐机构?', '提示', {
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
          deleteHotReg(params).then((res) => {
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


  },


}
</script>
<style lang="scss" scoped>
#hotOrgMaintenance .pagination-container {
  .el-input {
    width: 100px !important;
  }
}
::v-deep .el-dialog.customClass {
  width:45% !important;
}
.customClass .el-dialog__body .hotOrgMaintenance .el-form {
  width: 100% !important;
}
</style>


