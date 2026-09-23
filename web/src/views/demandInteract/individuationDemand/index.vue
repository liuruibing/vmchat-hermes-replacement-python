<template>
  <div class="individuation-demand">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" class="standard-form" :model="formInline" :rules="searchRules">
          <el-row>
            <el-col :span="20">
              <el-form-item label="" prop="beginDate">
                <el-date-picker v-model="formInline.beginDate" type="date" placeholder="选择开始日期" value-format="yyyy-MM-dd" size="small" />
              </el-form-item>
              <el-form-item label="" prop="endDate">
                <el-date-picker v-model="formInline.endDate" type="date" placeholder="选择结束日期" value-format="yyyy-MM-dd" size="small" />
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.fcode" placeholder="产品代码" size="small" />
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.fname" placeholder="产品名称" size="small" />
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.status" size="small" clearable filterable placeholder="请选择处理状态">
                  <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
              </el-form-item>
              <el-form-item style="">
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
                <el-button type="info" plain size="small" icon="el-icon-refresh" @click="handleReset">重置</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <ToolBarSlot>
          <template slot="left">
            <el-button type="info" plain size="small" icon="el-icon-plus" @click="handleAddDemand">新增</el-button>
          </template>
        </ToolBarSlot>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          resizable
        >
          <vxe-table-column align="center" title="序号" type="seq" width="50"></vxe-table-column>
          <vxe-table-column
            v-for="item in column"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :width="item.width"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="item.prop == 'status'">
                <span v-if="scope.row[item.prop] === '待提交'">
                  <el-tag size="mini">待提交</el-tag>
                </span>
                <span v-else-if="scope.row[item.prop] === '待处理'">
                  <el-tag size="mini" type="warning">待处理</el-tag>
                </span>
                <span v-else-if="scope.row[item.prop] === '处理完毕'">
                  <el-tag size="mini" type="success">处理完毕</el-tag>
                </span>
                <span v-else>{{ scope.row[item.prop] }}</span>
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" align="center" fixed="right" width="350px">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button v-if="scope.row['status'] === '待提交'" type="info" plain size="small" @click="handleSubmitDemand(scope.row)">提交</el-button>
                <el-button v-if="scope.row['status'] === '待提交'" type="info" plain size="small" @click="handleEditDemand(scope.row)">编辑</el-button>
                <el-button v-if="scope.row['status'] === '待提交'" type="info" plain size="small" @click="handleDeleteDemand(scope.row)">删除</el-button>
                <el-button type="info" size="small" plain @click="handleDetailDemand(scope.row)">详情</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </div>
    <div class="table-footer">
      <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
    </div>
    <el-dialog :title="editTitle" :visible.sync="editDialog" :close-on-click-modal="false" :close-on-press-escape="false" :destroy-on-close="true" @close="closeEdit">
      <edit-demand v-if="isShowEdit" @closeEdit="closeEdit" :curDemandRow="curDemandRow" :isEdit="isEdit"></edit-demand>
      <detail-demand v-if="isShowDetail" :curDemandRow="curDemandRow"></detail-demand>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { TABLE_COLUMNS } from './scripts/constants'
import EditDemand from './components/edit-demand'
import detailDemand from './components/detail-demand'
import { queryTableList, deleteDemand, submitDemand } from './scripts/api'
import productSelect from './components/productSelect'
import ToolBarSlot from '@/components/toolBarSlot'
export default {
  name: 'individuationDemand',
  components: {
    Pagination,
    EditDemand,
    detailDemand,
    productSelect,
    ToolBarSlot
  },
  data() {
    /** 开始日期校验 */
    const validateStartDate = (rule, value, callback) => {
      if (this.formInline.endDate !== null || this.formInline.endDate !== undefined || this.formInline.endDate !== '') {
        const startTime = new Date(value)
        const endTime = new Date(this.formInline.endDate)
        if (startTime > endTime) {
          callback(new Error('开始日期不能大于结束日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    /** 结束日期校验 */
    const validateEndDate = (rule, value, callback) => {
      if (this.formInline.beginDate !== null || this.formInline.beginDate !== undefined || this.formInline.beginDate !== '') {
        const startTime = new Date(this.formInline.beginDate)
        const endTime = new Date(value)
        if (startTime > endTime) {
          callback(new Error('结束日期不能小于开始日期'))
        } else {
          callback()
        }
      } else {
        callback()
      }
    }
    return {
      productSelectorVisible: false,

      // form表单绑定
      formInline: {
        fcode: '',
        fname: '',
        status: '',
        beginDate: '',
        endDate: ''
      },
      // 校验规则
      searchRules: {
        beginDate: [{ validator: validateStartDate, trigger: 'blur' }],
        endDate: [{ validator: validateEndDate, trigger: 'blur' }]
      },
      // 处理状态下拉
      statusOptions: [
        { label: '待提交', value: '1' },
        { label: '待处理', value: '2' },
        { label: '处理完毕', value: '3' }
      ],
      // 动态表格高度
      tableHeight: 0,
      // 表格加载状态
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: TABLE_COLUMNS,
      // 分页数据
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // 新增 | 编辑标题
      editTitle: '',
      // 弹窗状态
      editDialog: false,
      // 当前编辑需求行数据
      curDemandRow: {},
      // 新增 | 编辑弹窗状态
      isShowEdit: false,
      // 详情弹窗状态
      isShowDetail: false,
      // 组件是否为编辑状态
      isEdit: false
    }
  },
  mounted() {
    this.initData()
  },
  activated() {
    if (this.$store.getters.fromPageJump) {
      this.$store.commit('SET_FROMPAGEJUMP', false)
      if (this.$route.query && this.$route.query.path && this.$route.query.path == 'dashboard') {
        return
      }
      if (this.$route.query) {
        this.editDialog = true
        this.isShowEdit = true
        this.isEdit = false
        this.editTitle = '新增'
        this.curDemandRow = {
          fcode: this.$route.query.fcode,
          fname: this.$route.query.fname
        }
      }
    }
  },
  methods: {
    handleReset() {
      this.formInline = {
        fcode: '',
        fname: '',
        status: '',
        beginDate: '',
        endDate: ''
      }
    },
    /**
     * @description 初始化调用
     */
    initData() {
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable()
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        }
      })
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      let { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    /**
     * @description 表格数据查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formInline)
      params.limit = this.pageList._pageSize
      params.offset = (this.pageList._pageNum - 1) * this.pageList._pageSize
      this.tableLoading = true
      queryTableList(params).then((res) => {
        if (res.data.status === 0) {
          const resultData = res.data.data.rows || []
          this.converTableData(resultData)
          this.total = res.data.data.total || 0
          this.tableLoading = false
        } else {
          this.$message.error(res.data.message || '查询失败')
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        }
      })
    },
    /**
     * @description 表格数据分组降序
     */
    converTableData(data) {
      const convertData = data.map((item) => {
        return {
          ...item,
          applyDate: this.$moment(item.applyDate).valueOf()
        }
      })
      let todoList = []
      let todoDoneList = []
      let todoSubList = []
      convertData.forEach((item) => {
        if (item.status === '待提交') {
          todoSubList.push(item)
        }
        if (item.status === '待处理') {
          todoList.push(item)
        }
        if (item.status === '处理完毕') {
          todoDoneList.push(item)
        }
      })

      todoSubList = todoSubList.sort((a, b) => {
        return Number(b['applyDate']) - Number(a['applyDate'])
      })
      todoList = todoList.sort((a, b) => {
        return Number(b['applyDate']) - Number(a['applyDate'])
      })
      todoDoneList = todoDoneList.sort((a, b) => {
        return Number(b['applyDate']) - Number(a['applyDate'])
      })
      const sortData = [...todoSubList, ...todoList, ...todoDoneList]
      this.tableData = sortData.map((item) => {
        return {
          ...item,
          applyDate: this.$moment(item.applyDate).format('YYYY-MM-DD')
        }
      })
    },
    /**
     * @description 关闭新增/编辑弹窗
     */
    closeEdit(status) {
      this.editDialog = false
      this.isShowEdit = false
      this.isShowDetail = false
      this.isEdit = false
      this.editTitle = ''
      if (status === 'REFESH') {
        this.handleSearchTable()
      }
    },
    /**
     * @description 新增需求
     */
    handleAddDemand() {
      this.editDialog = true
      this.isShowEdit = true
      this.isEdit = false
      this.editTitle = '新增'
      this.curDemandRow = {}
    },
    /**
     * @description 编辑需求
     */
    handleEditDemand(row) {
      this.editDialog = true
      this.isShowEdit = true
      this.isEdit = true
      this.editTitle = '编辑'
      this.curDemandRow = JSON.parse(JSON.stringify(row))
    },
    /**
     * @description 删除需求
     */
    handleDeleteDemand(row) {
      this.$confirm('是否确认删除此条需求？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {}
          params.id = row.id
          deleteDemand(params).then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                customClass: 'message-error',
                type: 'error',
                message: res.data.message || '删除失败'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    },
    /**
     * @description 提交需求
     */
    handleSubmitDemand(row) {
      this.$confirm('是否提交当前需求？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          const params = {}
          params.id = row.id
          submitDemand(params).then((res) => {
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '提交成功',
                customClass: 'message-success'
              })
              this.handleSearchTable()
            } else {
              this.$message({
                customClass: 'message-error',
                type: 'error',
                message: res.data.message || '提交失败'
              })
            }
          })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    },
    /**
     * @description 查看详情
     */
    handleDetailDemand(row) {
      this.editTitle = '详情'
      this.editDialog = true
      this.isShowDetail = true
      this.curDemandRow = JSON.parse(JSON.stringify(row))
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.individuation-demand {
  .search-bar {
    margin-top: 12px;
    // border-bottom: 1px solid #e1e0e0;
    margin-bottom: 8px;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>
