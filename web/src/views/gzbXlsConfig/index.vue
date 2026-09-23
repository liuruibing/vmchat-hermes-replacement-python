<template>
  <div class="gzbTemplateConfig">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" class="standard-form" :inline="true" :model="formInline">
          <el-row>
            <el-col :span="24">
              <el-form-item label="模板名称">
                <el-input v-model="formInline.templateName" size="small" placeholder="请输入模板名称"></el-input>
              </el-form-item>
              <el-form-item class="mb20" label="创建日期" prop="ddate_">
                <el-date-picker
                  v-model="formInline.ddate_"
                  :picker-options="dateShortTPCTA()"
                  popper-class="popperDateShortTP"
                  range-separator="至"
                  size="small"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  type="daterange"
                  unlink-panels
                  value-format="yyyy-MM-dd"
                ></el-date-picker>
              </el-form-item>
              <el-form-item label="创建人">
                <el-input v-model="formInline.creator" size="small" placeholder="请输入创建人"></el-input>
              </el-form-item>

              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button type="info" icon="el-icon-refresh" size="small" plain @click="handleResetForm">重置</el-button>
                <el-button type="primary" size="small" icon="el-icon-plus" @click="handleAddGzbTemplateConfig">新增</el-button>
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
          <vxe-table-column title="序号" type="seq" align="center" width="150"></vxe-table-column>
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
            <template slot-scope="scope">
              <span>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column title="操作" align="center" width="200px" fixed="right">
            <template slot-scope="scope">
              <span class="table-operation">

                 <el-button  v-btn="'gzbxlsconfigupdate'"  type="info" plain size="small" @click="handleEditGzbXlsConfig(scope.row)">编辑</el-button>
                 <el-button  v-btn="'gzbxlsconfigdelete'"  type="info" plain size="small" @click="handleDeleteGzbXlsConfig(scope.row)">删除</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <div id="gzbTemplateConfig" class="table-footer">
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
      <edit-gzb-xls-config
        v-if="dialogVisibleEdit"
        :is-edit="isEdit"
        :cur-gzb-xls-config-row="curGzbXlsConfigRow"
        @closeDialog="closeDialog"
      ></edit-gzb-xls-config>
    </el-dialog>

  </div>
</template>

<script>
import { TABLE_COLUMNS } from './scripts/constants'
import Pagination from '@/components/Pagination'
import { deleteGzbXlsConfig, queryTableList } from './scripts/api'
import commonFun from '@/filters/common.js'
import editGzbXlsConfig from './components/edit-gzb-xls-config'
import moment from 'moment/moment'
export default {
  name: 'gzbXlsConfig',
  components: {
    editGzbXlsConfig,
    Pagination
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        ddate_: [],
        templateName: '',
        creator: '',
        date: [],
        orderString: ''
      },
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
        _pageSize: 20,
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
      // 当前编辑行数据
      curGzbXlsConfigRow: {},
    }
  },
  mounted() {
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
      // 查询表格
      this.handleSearchTable()
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },
    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [{
          text: '本周',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本月',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '本季度',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
            picker.$emit('pick', [start, end])
          }
        }, {
          text: '今年以来',
          onClick(picker) {
            const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
            const start = moment(end).year() + '-01-01'
            picker.$emit('pick', [start, end])
          }
        },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard();
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = self.timDate
              picker.$emit('pick', [start, end])

            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          },]
      }
      return pickerOptions
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
      if (this.formInline.ddate_ && this.formInline.ddate_.length) {
        params.beginDate = this.formInline.ddate_[0]
        params.endDate = this.formInline.ddate_[1]
      } else {
        params.beginDate = ''
        params.endDate = ''
      }
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      delete params.ddate_
      const data = this.parameterSrc(params)
      // console.log("data:"+JSON.stringify(data))
      this.tableLoading = true
      this.tableData = []
      queryTableList(data)
        .then((res) => {
          if (res.data.status === 200) {
            this.tableData = res.data.data.rows || []
            console.log('tableData', this.tableData)
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
     * @description 新增模板配置
     */
    handleAddGzbTemplateConfig() {
      this.dialogTitleEdit = '新增模板配置'
      this.dialogVisibleEdit = true
      this.curGzbXlsConfigRow={}
      this.isEdit = false
    },
    /**
     * @description 编辑模板配置
     */
    handleEditGzbXlsConfig(row) {
      this.dialogTitleEdit = '编辑模板配置'
      this.dialogVisibleEdit = true
      this.curGzbXlsConfigRow = JSON.parse(JSON.stringify(row))
      this.isEdit = true
    },

    /**
     * @description 删除模板配置
     */
    handleDeleteGzbXlsConfig(row) {
      this.$confirm('是否确定删除当模板配置?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {
            fId: row.fId
          }
          deleteGzbXlsConfig(params).then((res) => {
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
#gzbTemplateConfig .pagination-container {
  .el-input {
    width: 100px !important;
  }
}
::v-deep .el-dialog.customClass {
  width:45% !important;
}
.customClass .el-dialog__body .edit-gzb-xls-config .el-form {
  width: 100% !important;
}
</style>


