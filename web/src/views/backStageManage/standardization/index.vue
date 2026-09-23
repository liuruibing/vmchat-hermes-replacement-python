<template>
  <div class="standardization">
    <div class="search-bar">
      <el-form :inline="true" :model="formQuery" ref="formQuery" :rules="searchRules" label-width="120px;">
        <el-row>
          <el-col :span="18">
            <el-form-item label="机构/产品名称" prop="fundName">
              <el-input v-model="formQuery.fundName" placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="需求类型" prop="type">
              <el-select v-model="formQuery.type" placeholder="请选择" size="small" clearable>
                <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="处理状态" prop="status">
              <el-select v-model="formQuery.status" placeholder="请选择" size="small" clearable>
                <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="申请日期" prop="beginDate">
              <el-date-picker v-model="formQuery.beginDate" type="date" size="small" value-format="yyyy-MM-dd" placeholder="开始日期"></el-date-picker>
            </el-form-item>
            <span style="line-height: 32px; padding-right: 5px">-</span>
            <el-form-item label="" prop="endDate">
              <el-date-picker v-model="formQuery.endDate" type="date" size="small" value-format="yyyy-MM-dd" placeholder="结束日期"></el-date-picker>
            </el-form-item>
            <el-form-item label="申请人机构" prop="deptName">
              <el-input v-model="formQuery.deptName" placeholder="请输入" size="small"></el-input>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <div style="text-align: right">
              <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable">查询</el-button>
              <el-button type="info" size="small" icon="el-icon-refresh" @click="handleResetForm">重置</el-button>
              <el-button type="info" size="small" v-btn="'demandAllot'" icon="el-icon-set-up" @click="handleAllot({}, 'BATCH')">批量分配</el-button>
            </div>
          </el-col>
        </el-row>
      </el-form>
    </div>
    <vxe-table
      ref="refsTable"
      v-loading="tableLoading"
      :cell-style="{ height: '40px' }"
      :header-cell-style="{ color: '#333', height: '60px', background: '#fff', fontFamily: 'Microsoft Yahei' }"
      :cell-class-name="setCellClassName"
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
      <vxe-table-column label="序号" type="index" align="center" width="50"></vxe-table-column>
      <vxe-table-column
        v-for="item in tableColumns"
        :key="item.prop"
        :prop="item.prop"
        :label="item.label"
        :min-width="item.minWidth || '100'"
        :width="item.width"
        header-align="center"
        :align="item.align"
        :sortable="item.sortable"
        show-overflow-tooltip
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
      <vxe-table-column label="操作" width="260" align="center">
        <template slot-scope="scope">
          <el-button type="info" size="small" @click="handleDemandRow(scope.row)">处理</el-button>
          <el-button size="small" type="info" @click="handleOpenDetail(scope.row)">详情</el-button>
          <el-button type="info" size="small" v-btn="'demandAllot'" v-if="scope.row.status === '待处理'" @click="handleAllot(scope.row, 'SINGLE')">分配</el-button>
        </template>
      </vxe-table-column>
    </vxe-table>
    <div class="table-footer">
      <Pagination :total="total" :limit="pageList._pageSize" :page="pageList._pageNum" @pagination="pagination" />
    </div>
    <el-dialog :title="dialogTitle" width="50%" :visible.sync="dialogVisible" :close-on-click-modal="false" :append-to-body="true" @close="closeDialog">
      <detailForm v-if="detailFormShow" :curDemandRow="curDemandRow"></detailForm>
      <handle-demand v-if="isShowHandle" @closeDialog="closeDialog" :curHandleRow="curHandleRow"></handle-demand>
      <allot-data v-if="allotVisible" :allotData="allotData" @closeDialog="closeDialog"></allot-data>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import detailForm from './components/detailForm.vue'
import { TABLE_COLUMNS } from './scripts/constants'
import handleDemand from './components/handle-demand'
import AllotData from '@/components/allot-data'
import { queryTableList } from './scripts/api'
export default {
  components: {
    Pagination,
    detailForm,
    handleDemand,
    AllotData
  },
  data() {
    /** 开始日期校验 */
    const validateStartDate = (rule, value, callback) => {
      if (this.formQuery.endDate !== null || this.formQuery.endDate !== undefined || this.formQuery.endDate !== '') {
        const startTime = new Date(value)
        const endTime = new Date(this.formQuery.endDate)
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
      if (this.formQuery.beginDate !== null || this.formQuery.beginDate !== undefined || this.formQuery.beginDate !== '') {
        const startTime = new Date(this.formQuery.beginDate)
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
      formQuery: {
        beginDate: '',
        endDate: '',
        fundName: '',
        status: '',
        deptName: '',
        type: ''
      },
      // 分页绑定
      pageList: {
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      // 总条数
      total: 0,
      // form校验规则
      searchRules: {
        beginDate: [{ validator: validateStartDate, trigger: 'blur' }],
        endDate: [{ validator: validateEndDate, trigger: 'blur' }]
      },
      // 表格数据
      tableData: [
        {
          fundName: '测试机构',
          type: '',
          state: '说明。。。',
          fileName: '',
          applyDate: '2023-01-01',
          userName: 'admin',
          status: '',
          result: ''
        }
      ],
      // 表格高度
      tableHeight: 0,
      // 表格列
      Columns: TABLE_COLUMNS,
      // 表格loading
      tableLoading: false,
      // 弹窗标题
      dialogTitle: '',
      // 弹窗状态
      dialogVisible: false,
      // 详情组件状态
      detailFormShow: false,
      // 处理组件状态
      isShowHandle: false,
      // 当前需求详情行数据
      curDemandRow: {},
      // 需求类型下拉
      typeOptions: [
        { label: '产品信息验证', value: '1' },
        { label: '产品数据质检', value: '2' }
      ],
      // 处理状态下拉
      statusOptions: [
        { label: '待处理', value: '2' },
        { label: '处理完毕', value: '3' }
      ],
      // 当前处理需求行
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
        return this.Columns.filter((item) => item.prop !== 'assignerName')
      } else {
        return this.Columns
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
      this.dialogVisible = true
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
     * @description 表单重置
     */
    handleResetForm() {
      this.$refs['formQuery'].resetFields()
    },
    /**
     * @description 表格查询
     */
    handleSearchTable() {
      const params = Object.assign({}, this.formQuery)
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
      const { page, limit } = val
      this.pageList._pageNum = page
      this.pageList._pageSize = limit
      this.handleSearchTable()
    },
    /**
     * @description 详情弹窗
     */
    handleOpenDetail(row) {
      this.dialogTitle = '详情'
      this.dialogVisible = true
      this.detailFormShow = true
      this.curDemandRow = JSON.parse(JSON.stringify(row))
    },
    /**
     * @description 关闭dialog
     */
    closeDialog(status) {
      this.dialogVisible = false
      this.detailFormShow = false
      this.isShowHandle = false
      this.allotVisible = false
      this.dialogTitle = ''
      if (status === 'REFESH') {
        this.handleSearchTable()
      }
    },
    /**
     * @description 处理需求
     */
    handleDemandRow(row) {
      this.dialogTitle = '处理'
      this.curHandleRow = JSON.parse(JSON.stringify(row))
      this.dialogVisible = true
      this.isShowHandle = true
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.standardization {
  padding-left: 10px;
  .search-bar {
    margin-top: 12px;
    // border-bottom: 1px solid #e1e0e0;
    margin-bottom: 8px;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0;
  }
  .title-style {
    color: #0F65DD;
    height: 35px;
    line-height: 35px;
    padding-left: 4px;
    font-size: 16px;
    //border-left: 4px solid #e03d3e;
    margin-bottom: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }
  .caret-wrapper {
    height: 22px !important;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .disabledCheckBox .vxe-cell--checkbox {
    display: none;
  }
}
</style>
