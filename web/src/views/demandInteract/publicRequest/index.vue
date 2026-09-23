<!--
 * @Description:
 * @Author:
 * @Date: 2023-02-06 09:43:19
 * @LastEditors: zhaojirui zhaojirui@datadriver.com.cn
 * @LastEditTime: 2023-04-17 17:54:01
-->
<template>
  <div class="publicRequest" v-auto-enter>
    <!-- 查询表单 -->
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" :model="formQuery" class="standard-form" ref="formQuery" :rules="searchRules" label-width="120px;">
          <el-form-item label="" prop="fundName">
            <el-input v-model="formQuery.fundName" placeholder="请输入机构名称/拼音首字母" style="width: 210px !important;" size="small"></el-input>
          </el-form-item>
          <!--          <el-form-item label="需求类型" prop="type">-->
          <!--            <el-select v-model="formQuery.type" placeholder="请选择" size="small" clearable>-->
          <!--              <el-option v-for="item in typeOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>-->
          <!--            </el-select>-->
          <!--          </el-form-item>-->
          <el-form-item label="" prop="status">
            <el-select v-model="formQuery.status" placeholder="请选择处理状态" size="small" clearable>
              <el-option v-for="item in statusOptions" :key="item.value" :label="item.label" :value="item.value"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="" prop="deptName">
            <el-input v-model="formQuery.deptName" placeholder="请输入申请人机构" size="small"></el-input>
          </el-form-item>
          <div style="display: inline-block">
            <el-form-item label="" prop="beginDate">
              <el-date-picker v-model="formQuery.beginDate" type="date" size="small" value-format="yyyy-MM-dd" placeholder="请选择开始日期"></el-date-picker>
            </el-form-item>
            <span style="line-height: 32px; padding-right: 5px;color:#fff">-</span>
            <el-form-item label="" prop="endDate">
              <el-date-picker v-model="formQuery.endDate" type="date" size="small" value-format="yyyy-MM-dd" placeholder="请选择结束日期"></el-date-picker>
            </el-form-item>
            <el-form-item label="">
              <el-button type="primary" size="small" :icon="searchIcon" :disabled="searchDisabled" @click="onQuery(true)">查询</el-button>
              <el-button type="info" plain size="small" icon="el-icon-refresh" @click="resetForm">重置</el-button>
              <el-button type="info" plain size="small" icon="el-icon-plus" @click="openAdd('3')">尽调申请</el-button>
            </el-form-item>
          </div>
        </el-form>
        <!--        <ToolBarSlot>
          <template slot="left">
            <el-button type="info" plain size="small" icon="el-icon-plus" @click="openAdd('3')">尽调申请</el-button>
          </template>
        </ToolBarSlot>-->
      </div>
    </div>
    <!-- 表格 -->
    <div id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :data="tableData"
          auto-resize
          :height="tableHeight"
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          resizable
          sync-resize
        >
          <vxe-table-column label="序号" type="index" align="center" width="50"></vxe-table-column>
          <vxe-table-column
            v-for="item in Columns"
            :key="item.prop"
            :field="item.prop"
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
                <span v-if="scope.row[item.prop] === '1'" style="color: #409eff">
                  <el-tag size="mini">待提交</el-tag>
                </span>
                <span v-else-if="scope.row[item.prop] === '2'" style="color: #ffc000">
                  <el-tag size="mini" type="warning">待处理</el-tag>
                </span>
                <span v-else-if="scope.row[item.prop] === '3'" style="color: #70ad47">
                  <el-tag size="mini" type="success">处理完毕</el-tag>
                </span>
                <span v-else>{{ scope.row[item.prop] }}</span>
              </span>
              <span v-else-if="item.prop == 'type'">
                <span v-if="scope.row[item.prop] === '1'">产品信息验证</span>
                <span v-else-if="scope.row[item.prop] === '2'">产品数据质检</span>
                <span v-else-if="scope.row[item.prop] === '3'">机构尽调</span>
                <span v-else>{{ scope.row[item.prop] }}</span>
              </span>
              <span v-else>{{ scope.row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="400" align="center">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button :style="scope.row.status !== '1' ? { visibility: 'hidden' } : ''" size="small" type="info" plain @click="openSubmit(scope.row)">提交</el-button>
                <el-button :style="scope.row.status !== '1' ? { visibility: 'hidden' } : ''" size="small" type="info" plain @click="openEdit(scope.row)">编辑</el-button>
                <el-button :style="scope.row.status !== '1' ? { visibility: 'hidden' } : ''" size="small" type="info" plain @click="openDelete(scope.row)">删除</el-button>
                <el-button size="small" type="info" plain @click="openDetail(scope.row)">详情</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery._pageNum"
          :page-size="formQuery._pageSize"
          :total="total"
          class="standard-vxe-pager"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          @page-change="pagination"
        />
      </div>
      <!--      <div style="height: 50px">
        <Pagination :total="total" :limit="formQuery._pageSize" :page="formQuery._pageNum" @pagination="pagination" />
      </div>-->
    </div>

    <!-- 新申请/编辑/详情 -->
    <el-dialog width="50%" custom-class="" :visible.sync="dialogVisible" :close-on-click-modal="false" @closed="dialogClosed">
      <div slot="title">
        <span style="color: #333333 !important; font-weight: normal !important; font-size: 16px !important">{{ dialogTitle }}</span>
      </div>
      <addForm ref="addForm" v-if="addFormShow" @close="close"></addForm>
      <detailForm ref="detailForm" v-if="detailFormShow" @close="dialogVisible = false"></detailForm>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import addForm from './components/addForm.vue'
import detailForm from './components/detailForm.vue'
import accessPoolApi from '@/api/AccessPoolProcess/accessPool'
import commonApi from '@/api/common'
import treeToArray from '../../../components/TreeTable/eval'
import ToolBarSlot from '@/components/toolBarSlot'
export default {
  components: {
    Pagination,
    addForm,
    detailForm,
    ToolBarSlot
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
      formQuery: {
        beginDate: '',
        endDate: '',
        fundName: '',
        status: '',
        // type: '',
        deptName: '',
        _pageSize: 20,
        _pageNum: 1,
        _pageFlag: true
      },
      typeOptions: [{ label: '产品信息验证', value: '1' }, { label: '产品数据质检', value: '2' }, { label: '机构尽调', value: '3' }],
      statusOptions: [{ label: '待提交', value: '1' }, { label: '待处理', value: '2' }, { label: '处理完毕', value: '3' }],
      searchRules: {
        beginDate: [{ validator: validateStartDate, trigger: 'blur' }],
        endDate: [{ validator: validateEndDate, trigger: 'blur' }]
      },
      tableHeight: 0,
      tableData: [
        // {
        //   fundName: "测试机构",
        //   type: "3",
        //   state: "说明。。。",
        //   fileName: "",
        //   applyDate: "2023-01-01",
        //   userName: "admin",
        //   status: "1",
        //   result: ""
        // },
        // {
        //   fundName: "测试产品一号",
        //   type: "1",
        //   state: "说明。。。",
        //   fileName: "",
        //   applyDate: "2023-01-01",
        //   userName: "admin",
        //   status: "1",
        //   result: ""
        // },
        // {
        //   fundName: "测试产品003",
        //   type: "2",
        //   state: "说明。。。",
        //   fileName: "",
        //   applyDate: "2023-01-01",
        //   userName: "admin",
        //   status: "1",
        //   result: ""
        // },
        // {
        //   fundName: "测试机构X",
        //   type: "3",
        //   state: "说明。。。",
        //   fileName: "",
        //   applyDate: "2023-01-01",
        //   userName: "admin",
        //   status: "2",
        //   result: "处理结果处理结果"
        // }
      ],
      Columns: [
        { prop: 'fundName', label: '机构名称', align: '' },
        // { prop: 'type', label: '需求类型', align: 'center' },
        { prop: 'state', label: '说明', align: '' },
        { prop: 'fileName', label: '需求附件', align: '' },
        { prop: 'fallName', label: '结果附件', align: '' },
        { prop: 'applyDate', label: '申请日期', align: 'center' },
        { prop: 'deptName', label: '申请人机构', align: 'center' },
        { prop: 'userName', label: '申请人', align: 'center' },
        { prop: 'status', label: '处理状态', align: 'center' },
        { prop: 'result', label: '处理结果', align: '' }
      ],
      total: 0,
      tableLoading: false,
      dialogTitle: '',
      dialogVisible: false,
      addFormShow: false,
      detailFormShow: false,
      homeParams: {},
      searchIcon: 'el-icon-search',
      searchDisabled: false
    }
  },
  activated() {
    if (this.$route.query) {
      let params = JSON.parse(JSON.stringify(this.$route.query))
      this.homeParams = params
      if (params.company) {
        this.openAdd('3', false)
      }
      if (params.flag) {
        this.openAdd('1', true)
      } else {
        this.formQuery.fundName = params.fundName
      }
    }
  },
  mounted() {
    const path = this.$route.path
    if (path === '/xqhd/bzhxqgl/xxyzsq') {
      this.formQuery.type = '1'
    } else if (path === '/xqhd/bzhxqgl/jdsq') {
      this.formQuery.type = '3'
    } else if (path === '/xqhd/bzhxqgl/sjzj') {
      this.formQuery.type = '2'
    }
    this.handleTableHeight()
    this.onQuery(true)
  },
  methods: {
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
      })
    },
    // 重置
    resetForm() {
      this.$refs['formQuery'].resetFields()
    },
    // 查询
    onQuery(flag) {
      if (flag) {
        this.formQuery._pageNum = 1
      }
      this.tableData = []
      // this.total = 0
      this.tableLoading = true
      this.searchIcon = 'el-icon-loading'
      this.searchDisabled = true
      let params = Object.assign({}, this.formQuery, {})
      params.limit = this.formQuery._pageSize
      params.offset = (this.formQuery._pageNum - 1) * this.formQuery._pageSize
      delete params._pageFlag
      delete params._pageSize
      delete params._pageNum
      accessPoolApi
        .needManageSelect(params)
        .then(res => {
          this.tableLoading = false
          this.searchIcon = 'el-icon-search'
          this.searchDisabled = false
          let { status, data, message } = res.data
          if (status === 0) {
            this.total = data.total
            data.rows.forEach(element => {
              if (element.status == '待提交') {
                element.status = '1'
              } else if (element.status == '待处理' || element.status == '处理中') {
                element.status = '2'
              } else if (element.status == '处理完毕') {
                element.status = '3'
              }
              if (element.type == '产品信息验证') {
                element.type = '1'
              } else if (element.type == '产品数据质检') {
                element.type = '2'
              } else if (element.type == '机构尽调') {
                element.type = '3'
              }
            })
            this.converTableData(data.rows)
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: message || '查询失败'
            })
          }
        })
        .catch(() => {
          this.tableLoading = false
          this.searchIcon = 'el-icon-search'
          this.searchDisabled = false
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '查询失败'
          })
        })
    },
    /**
     * @description 表格数据分组降序
     */
    converTableData(data) {
      const convertData = data.map(item => {
        return {
          ...item,
          applyDate: this.$moment(item.applyDate).valueOf()
        }
      })
      let todoList = []
      let todoDoneList = []
      let todoSubList = []
      convertData.forEach(item => {
        if (item.status === '1') {
          todoSubList.push(item)
        }
        if (item.status === '2') {
          todoList.push(item)
        }
        if (item.status === '3') {
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
      this.tableData = sortData.map(item => {
        return {
          ...item,
          applyDate: this.$moment(item.applyDate).format('YYYY-MM-DD')
        }
      })
    },
    // 分页
    pagination(val) {
      c /* onst { page, limit } = val
      this.formQuery._pageNum = page
      this.formQuery._pageSize = limit */
      const { currentPage, pageSize } = val
      // 起始页
      this.formQuery._pageNum = currentPage
      // 每页数量
      this.formQuery._pageSize = pageSize
      this.onQuery()
    },

    // 提交
    openSubmit(data) {
      this.$confirm('是否提交当前需求?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
         confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          this.onSubmit(data)
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    onSubmit(data) {
      this.$message.success('提交成功')
      accessPoolApi
        .needManageSubmit({
          id: data.id
        })
        .then(res => {
          let { status, message } = res.data
          if (status === 0) {
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: message || '提交成功'
            })
            this.onQuery()
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: message || '提交失败'
            })
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '提交失败'
          })
        })
    },
    // 删除
    openDelete(data) {
      this.$confirm('您是否确认删除此条申请?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          this.onDelete(data)
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '已取消'
          })
        })
    },
    onDelete(data) {
      accessPoolApi
        .needManageDeleteFund({
          id: data.id
        })
        .then(res => {
          let { status, message } = res.data
          if (status === 0) {
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: message || '删除成功'
            })
            this.onQuery()
          } else {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: message || '删除失败'
            })
          }
        })
        .catch(() => {
          this.$message.closeAll()
          this.$message({
            type: 'error',
            message: '删除失败'
          })
        })
    },
    // 新申请
    openAdd(type, flag) {
      if (type === '1') {
        this.dialogTitle = '验证申请'
      } else if (type === '2') {
        this.dialogTitle = '质检申请'
      } else if (type === '3') {
        this.dialogTitle = '尽调申请'
      } else {
        this.dialogTitle = '新申请'
      }
      this.dialogVisible = true
      this.addFormShow = true
      this.$nextTick(() => {
        this.$refs.addForm.setDefaultType(type)
      })
      if (flag) {
        this.$nextTick(() => {
          this.$refs.addForm.addInit(this.homeParams)
        })
      } else {
        this.$nextTick(() => {
          this.$refs.addForm.addInitManager(this.homeParams)
        })
      }
    },
    // 编辑
    openEdit(row) {
      this.dialogTitle = '编辑'
      this.dialogVisible = true
      this.addFormShow = true
      this.$nextTick(() => {
        this.$refs.addForm.setDefaultType(row.type)
      })
      this.$nextTick(() => {
        this.$refs.addForm.editInit(row)
      })
    },
    // 详情
    openDetail(row) {
      this.dialogTitle = '详情'
      this.dialogVisible = true
      this.detailFormShow = true
      this.$nextTick(() => {
        this.$refs.addForm.setDefaultType(type)
      })
      this.$nextTick(() => {
        this.$refs.detailForm.init(row)
      })
    },
    // 关闭dialog
    dialogClosed() {
      this.addFormShow = false
      this.detailFormShow = false
    },
    close(refresh) {
      this.dialogVisible = false
      if (refresh) {
        this.onQuery(true)
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.publicRequest {
  // padding-left: 16px;
  // padding-top: 16px;
  // padding-right: 20px;
  .title-style {
    color: #0f65dd;
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
    background-color: #0f65dd;
  }
  .caret-wrapper {
    height: 22px !important;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
::v-deep .el-button--danger {
  color: #f56c6c;
  background-color: #fff;
  border-color: #f56c6c;
}
</style>
