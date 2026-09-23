<template>
  <div class="individuation-demand">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" :rules="searchRules" class="standard-form">
          <el-form-item label="开始日期" prop="beginDate">
            <el-date-picker v-model="formInline.beginDate" type="date" placeholder="选择开始日期" value-format="yyyy-MM-dd" size="small" />
          </el-form-item>
          <el-form-item label="结束日期" prop="endDate">
            <el-date-picker v-model="formInline.endDate" type="date" placeholder="选择结束日期" value-format="yyyy-MM-dd" size="small" />
          </el-form-item>
          <el-form-item label="处理状态" prop="status">
            <el-select v-model="formInline.status" size="small" clearable filterable placeholder="请选择处理状态">
              <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh" @click="handleResetForm">重置</el-button>
            <el-button type="info" size="small" plain v-btn="'demandAllot'" icon="el-icon-set-up" @click="handleAllot({}, 'BATCH')">批量分配</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :checkbox-config="{ checkStrictly: true }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          @checkbox-change="handleCheckBoxClick"
        >
          <vxe-table-column v-if="isShowCheckBox" align="center" fixed="left" type="checkbox" width="50"></vxe-table-column>
          <vxe-table-column align="center" title="序号" type="seq" width="50"></vxe-table-column>
          <vxe-table-column
            v-for="item in tableColumns"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="item.prop == 'status'">
                <span v-if="scope.row[item.prop] === '待提交'" style="color: #409eff">待提交</span>
                <span v-else-if="scope.row[item.prop] === '待处理'" style="color: #ffc000">待处理</span>
                <span v-else-if="scope.row[item.prop] === '处理完毕'" style="color: #70ad47">处理完毕</span>
                <span v-else>{{ scope.row[item.prop] }}</span>
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" align="center" width="300px">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" plain size="small" @click="handleDemandRow(scope.row)">处理</el-button>
                <el-button type="info" plain size="small" @click="handleDetailDemand(scope.row)">详情</el-button>
                <el-button type="info" plain size="small" v-btn="'demandAllot'" v-if="scope.row.status === '待处理'" @click="handleAllot(scope.row, 'SINGLE')">分配</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </div>
    <div class="table-footer">
      <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
    </div>
    <el-dialog :title="editTitle" :visible.sync="editDialog" :close-on-click-modal="false" :close-on-press-escape="false" :destroy-on-close="true" @close="closeDialog">
      <detail-demand v-if="isShowDetail" :curDemandRow="curDemandRow"></detail-demand>
      <handle-demand v-if="isShowHandle" @closeDialog="closeDialog" :curHandleRow="curHandleRow"></handle-demand>
      <allot-data v-if="allotVisible" :allotData="allotData" @closeDialog="closeDialog"></allot-data>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import { TABLE_COLUMNS } from './scripts/constants'
import detailDemand from './components/detail-demand'
import handleDemand from './components/handle-demand'
import AllotData from '@/components/allot-data'
import { queryTableList } from './scripts/api'
export default {
  name: 'individuationDemand',
  components: {
    Pagination,
    detailDemand,
    handleDemand,
    AllotData
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
      // form表单绑定
      formInline: {
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
      // 当前需求详情行数据
      curDemandRow: {},
      // 详情弹窗状态
      isShowDetail: false,
      // 处理弹窗状态
      isShowHandle: false,
      // 处理需求id
      curHandleRow: {},
      // 表格行选中数据
      selectRowData: [],
      // 分配弹窗
      allotVisible: false,
      // 需分配数据
      allotData: []
    }
  },
  mounted() {
    this.initData()
  },
  computed: {
    isShowCheckBox() {
      if (!this.$store.state.btnData.includes('demandAllot')) {
        return false
      } else {
        return true
      }
    },
    tableColumns() {
      if (!this.$store.state.btnData.includes('demandAllot')) {
        return this.column.filter((item) => item.prop !== 'assignerName')
      } else {
        return this.column
      }
    }
  },
  methods: {
    /**
     * @description 单个分配/批量分配
     */
    handleAllot(row, status) {
      this.allotData = []
      if (status === 'BATCH') {
        if (this.selectRowData.length < 2) {
          this.$message.warning('批量分配数据不得小于2条')
          return
        }
        this.allotData = this.selectRowData
      } else if (status === 'SINGLE') {
        this.allotData = [row]
      }
      this.editDialog = true
      this.allotVisible = true
      this.editTitle = '分配'
    },
    /**
     * @description 动态控制checkbox是否显示
     */
    setCellClassName({ row, rowIndex, $rowIndex, column, columnIndex, $columnIndex }) {
      if (row.status !== '待处理') {
        return 'disabledCheckBox'
      }
    },
    /**
     * @description 监听选中表格数据
     */
    handleCheckBoxClick({ checked, row }) {
      const index = this.selectRowData.findIndex((item) => item.id === row.id)
      if (checked) {
        index === -1 && this.selectRowData.push(row)
      } else {
        index !== -1 && this.selectRowData.splice(index, 1)
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
      convertData.forEach((item) => {
        if (item.status === '待处理') {
          todoList.push(item)
        }
        if (item.status === '处理完毕') {
          todoDoneList.push(item)
        }
      })
      todoList = todoList.sort((a, b) => {
        return Number(b['applyDate']) - Number(a['applyDate'])
      })
      todoDoneList = todoDoneList.sort((a, b) => {
        return Number(b['applyDate']) - Number(a['applyDate'])
      })
      const sortData = [...todoList, ...todoDoneList]
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
    closeDialog(status) {
      this.editDialog = false
      this.isShowDetail = false
      this.isShowHandle = false
      this.allotVisible = false
      this.editTitle = ''
      if (status === 'REFESH') {
        this.handleSearchTable()
      }
    },
    /**
     * @description 查看详情
     */
    handleDetailDemand(row) {
      this.editTitle = '详情'
      this.editDialog = true
      this.isShowDetail = true
      this.curDemandRow = JSON.parse(JSON.stringify(row))
    },
    /**
     * @description 处理需求
     */
    handleDemandRow(row) {
      this.editTitle = '处理'
      this.editDialog = true
      this.isShowHandle = true
      this.curHandleRow = JSON.parse(JSON.stringify(row))
    },
    /**
     * @description 表单重置
     */
    handleResetForm() {
      this.$refs['formInline'].resetFields()
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
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .disabledCheckBox .vxe-cell--checkbox {
    display: none;
  }
}
</style>
