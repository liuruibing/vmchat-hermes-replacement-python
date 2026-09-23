<template>
  <div class="controlRecord ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <!-- 查询 -->
          <div class="grid-content bg-purple">
            <el-form-item label="任务编码" prop="vc_code">
              <el-input v-model.trim="formQuery.vc_code" clearable placeholder="请输入编码" size="small"></el-input>
            </el-form-item>
            <el-form-item label="名称" prop="vc_name">
              <el-input v-model.trim="formQuery.vc_name" clearable placeholder="请输入名称" size="small"></el-input>
            </el-form-item>
            <el-form-item label="执行结果" prop="vc_result">
              <el-select v-model="formQuery.vc_result" placeholder="请选择" size="small">
                <el-option label="全部" value></el-option>
                <el-option label="成功" value="成功"></el-option>
                <el-option label="失败" value="失败"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="运行状态" prop="vc_run_status">
              <el-select v-model="formQuery.vc_run_status" placeholder="请选择" size="small">
                <el-option label="全部" value></el-option>
                <el-option label="已完成" value="COMPLETED"></el-option>
                <el-option label="未执行" value="UNDO"></el-option>
                <el-option label="取消" value="DISABLE"></el-option>
                <el-option label="正在运行" value="RUNNING"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="业务开始时间" prop="d_busi_begin_date">
              <el-date-picker
                v-model="formQuery.d_busi_begin_date"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                :picker-options="dateShortDot()"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="业务结束时间" prop="d_busi_end_date">
              <el-date-picker
                v-model="formQuery.d_busi_end_date"
                type="date"
                size="small"
                value-format="yyyy-MM-dd"
                placeholder="选择日期"
                :picker-options="dateShortDot()"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="开始执行时间" prop="d_exec_begin_date">
              <el-date-picker
                v-model="formQuery.d_exec_begin_date"
                type="date"
                size="small"
                placeholder="选择日期"
                value-format="yyyy-MM-dd"
                :picker-options="dateShortDot()"
              ></el-date-picker>
            </el-form-item>
            <el-form-item label="结束执行时间" prop="d_exec_end_date">
              <el-date-picker
                v-model="formQuery.d_exec_end_date"
                type="date"
                size="small"
                placeholder="选择日期"
                value-format="yyyy-MM-dd"
                :picker-options="dateShortDot()"
              ></el-date-picker>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" :disabled="btnDisabled" class="mb5" icon="el-icon-search" size="small" @click="onQuery(true)">
              查询
            </el-button>
            <el-button type="primary" plain size="small" icon="el-icon-delete" @click="allDelete">
              全部删除
            </el-button>
            <el-button plain type="primary" icon="el-icon-delete" size="small" @click="deletall">
              批量删除
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle;display: inline-block;">
      <div class="color-box"></div>
    </div>
    <span class="title-style">任务列表</span>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'vc_code', order: 'descending' }"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      style="width: 100%"
      row-key="f_id"
      :expand-row-keys="expandRowKeys"
      :tree-props="{ children: 'children' }"
    >
      <el-table-column type="selection" width="35" align="center"></el-table-column>

      <el-table-column prop="vc_code" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="编码" min-width="210" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vc_code | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="vc_name" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.vc_name | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="vc_code_type_name"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="编码类型"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.vc_code_type_name | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="d_busi_begin_date"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="业务开始日期"
        min-width="120"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.d_busi_begin_date | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column
        prop="d_busi_end_date"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="业务结束日期"
        min-width="120"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.d_busi_end_date | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="d_exec_begin_date"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="开始执行时间"
        min-width="120"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.d_exec_begin_date | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="d_exec_end_date"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="结束执行时间"
        min-width="120"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.d_exec_end_date | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column
        prop="vc_run_status_name"
        sortable="custom"
        :sort-orders="['ascending', 'descending']"
        show-overflow-tooltip
        label="运行状态"
        min-width="100"
        header-align="center"
      >
        <template slot-scope="scope">
          <span>{{ scope.row.vc_run_status_name | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="vc_result" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="结果" min-width="90" header-align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.vc_result == '执行成功!' || scope.row.vc_run_status == 'DISABLE' || scope.row.vc_run_status == 'UNDO' || scope.row.vc_run_status == 'RUNNING'">
            {{ scope.row.vc_result | noDataFilter }}
          </span>
          <span v-else style="color:red">{{ scope.row.vc_result | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="100" align="center">
        <template slot-scope="scope">
          <div class="standard-form dialog-footer">
            <el-button type="info" plain size="small" @click="logCancle(scope.row)" v-if="scope.row.vc_run_status == 'RUNNING'">
            取消执行
          </el-button>
          <el-button v-else type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="明细" min-width="60" align="center">
        <template slot-scope="scope">
          <div class="standard-form dialog-footer">
            <el-button type="primary" plain size="small" @click="getDetail(scope.row)" v-if="scope.row.vc_code_type_name == '任务'">
              明细
            </el-button>
          </div>

        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 明细 参数弹窗 -->
    <el-dialog title="明细日志" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" class="formQuery">
            <el-row>
              <el-col :span="16">
                <!-- 查询 -->
                <div class="grid-content bg-purple">
                  <el-form-item label="执行结果" prop="vc_run_status">
                    <el-select v-model="formDialog.vc_run_status" placeholder="请选择" size="small">
                      <el-option label="全部" value></el-option>
                      <el-option label="成功" value="0"></el-option>
                      <el-option label="失败" value="1"></el-option>
                    </el-select>
                  </el-form-item>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="grid-content bg-purple-light">
                  <el-form-item class="search_button_com">
                    <el-button type="primary" :disabled="btnDisabled" class="mb5" style="float:right" size="small" @click="onQuery2(true)">
                      查询
                    </el-button>
                  </el-form-item>
                </div>
              </el-col>
            </el-row>
          </el-form>

          <div class="forms_table_title">
            <i class="el-icon-tickets"></i>
            明细列表
          </div>

          <el-table ref="multipleTable" :data="tableData2" border stripe v-loading="tableLoading2" style="width: 100%">
            <el-table-column prop="vc_code" show-overflow-tooltip label="任务编码" min-width="180" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vc_code | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="vc_name" show-overflow-tooltip label="任务名称" min-width="80" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vc_name | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="d_busi_begin_date" show-overflow-tooltip label="业务开始日期" min-width="60" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.d_busi_begin_date | noDataFilter }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="d_busi_end_date" show-overflow-tooltip label="业务结束日期" min-width="60" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.d_busi_end_date | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="d_exec_begin_date" show-overflow-tooltip label="开始执行时间" min-width="100" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.d_exec_begin_date | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="d_exec_end_date" show-overflow-tooltip label="结束执行时间" min-width="100" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.d_exec_end_date | noDataFilter }}</span>
              </template>
            </el-table-column>

            <el-table-column prop="vc_result" show-overflow-tooltip label="日志详情" min-width="100" header-align="center">
              <template slot-scope="scope">
                <span>{{ scope.row.vc_result | noDataFilter }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-main>
      </el-container>
      <el-row>
      <!-- 分页 -->
      <Pagination :total="total2" :limit="formDialog.pageSize" :page="formDialog.pageNum" @pagination="pagination2"></Pagination>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/controlRecord'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'

export default {
  name: 'DdControlRecord',
  components: {
    Pagination
  },
  data() {
    return {
      // 展开行的数据
      expandRowKeys: [],
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      tableData2: [], //表格数据
      tableLoading2: false, //表格加载
      //总条数
      total: 0,
      //内部总条数
      total2: 0,
      // 顶部查询条件
      formQuery: {
        // 任务编码
        vc_code: '',
        // 名称
        vc_name: '',
        // 执行结果
        vc_result: '',
        // 运行状态
        vc_run_status: '',
        // 业务开始时间
        d_busi_begin_date: '',
        // 业务结束时间
        d_busi_end_date: '',
        // 开始执行时间
        d_exec_begin_date: '',
        // 结束执行时间
        d_exec_end_date: '',
        // 每页大小
        pageSize: 10,
        // 起始页
        pageNum: 1,
        // 排序方式
        orderBy: 'f_id desc',

        // 日志类型
        vc_exec_type: 'SCH'
      },
      dialogMask: false, // 弹窗
      // 弹窗查询参数
      formDialog: {
        // 任务id
        f_id: '',
        // 运行状态
        vc_run_status: '',
        // 每页大小
        pageSize: 10,
        // 起始页
        pageNum: 1,
        // 排序方式
        orderBy: 'f_id  desc'
      },

      formLabelWidth: '100px',
      // 批量删除的数据
      multipleSelection: [],
      // 查询按钮禁用
      btnDisabled: false
    }
  },

  mounted() {
    // 默认获取 开始执行时间是今天
    this.formQuery.d_exec_begin_date = fun.get_newDate()
    // 默认查询
    this.onQuery(true)
  },
  methods: {
    // 日期快捷选项
    dateShortDot() {
      return fun.dateShortDot()
    },
    // 查询
    onQuery(flag) {
      this.tableLoading = true
      if (flag) {
        this.formQuery.pageNum = 1
      }
      let params = Object.assign({}, this.formQuery)

      if (params.d_busi_begin_date && params.d_busi_end_date) {
        let busibeDate = params.d_busi_begin_date.replace(/-/g, '')
        let busiendDate = params.d_busi_end_date.replace(/-/g, '')
        if (parseInt(busibeDate) > parseInt(busiendDate)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '业务开始时间不能大于业务结束时间'
          })
        }
      }

      if (params.d_exec_begin_date && params.d_exec_end_date) {
        let busibeDate = params.d_exec_begin_date.replace(/-/g, '')
        let busiendDate = params.d_exec_end_date.replace(/-/g, '')
        if (parseInt(busibeDate) > parseInt(busiendDate)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '开始执行时间不能大于结束执行时间'
          })
        }
      }

      commonApi
        .getETLLogList(params)
        .then(res => {
          this.tableLoading = false
          let { list, total } = res.data.data
          // // 总条数
          this.total = total

          // 树状结构
          this.tableData = fun.setLogTreeData(list, 0).data
          this.expandRowKeys = fun.setLogTreeData(list, 0).expandRowKeys
        })
        .catch(() => {})
    },
    // 明细
    getDetail(row) {
      this.dialogMask = true
      this.tableLoading2 = true

      this.formDialog.f_id = row.f_id
      let params = this.formDialog

      commonApi
        .getDetailLogList(params)
        .then(res => {
          this.tableLoading2 = false
          let { list, total } = res.data.data
          // 总条数
          this.total2 = total
          this.tableData2 = []
          list.forEach(item => {
            this.tableData2.push(item)
          })
        })
        .catch(() => {})
    },
    // 明细内查询
    onQuery2(flag) {
      this.tableLoading2 = true
      if (flag) {
        this.formDialog.pageNum = 1
      }
      let params = this.formDialog

      commonApi
        .getDetailLogList(params)
        .then(res => {
          this.tableLoading2 = false
          let { list, total } = res.data.data
          // 总条数
          this.total2 = total
          this.tableData2 = []
          list.forEach(item => {
            this.tableData2.push(item)
          })
        })
        .catch(() => {})
    },
    // 单个删除
    deleteParamSet(batchIdArr, vc_exec_type) {
      let params = { batchIdArr, vc_exec_type }
      commonApi
        .deleteEtlLog(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },

    // 批量删除
    deletall() {
      if (this.multipleSelection.length) {
        this.$confirm('确认删除这些数据吗?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
          confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        })
          .then(() => {
            // 批量删除
            let arr = []
            let str = {}
            let vc_exec_type = 'SCH'
            this.multipleSelection.forEach(item => {
              arr.push(item.f_id)
            })
            str = arr.join(',')

            let params = { batchIdArr: str, vc_exec_type: vc_exec_type }

            commonApi
              .deleteEtlLog(params)
              .then(res => {
                if (res.data.status === 200) {
                  this.onQuery(false)
                  this.$message.closeAll()

                  this.$message({
                    type: 'success',
                    message: res.data.message
                  })
                } else {
                  this.$message.closeAll()

                  this.$message.error(res.data.message)
                }
              })
              .catch(() => {})
          })
          .catch(() => {})
      } else if (this.multipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要批量删除的数据',
          type: 'warning'
        })
      }
    },
    // 批量删除数据
    handleSelectionChange(val) {
      this.multipleSelection = val
    },
    // 全部删除
    allDelete() {
      this.$confirm('确认删除这些数据吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 全部删除
          let params = { batchIdArr: '', vc_exec_type: 'SCH' }

          commonApi
            .deleteEtlLog(params)
            .then(res => {
              if (res.data.status === 200) {
                this.onQuery(false)
                this.$message.closeAll()

                this.$message({
                  type: 'success',
                  message: res.data.message
                })
              } else {
                this.$message.closeAll()

                this.$message.error(res.data.message)
              }
            })
            .catch(() => {})
        })
        .catch(() => {})
    },
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderBy = fun.etlqueryOrderBy(val)
      // // 查询
      this.onQuery(false)
    },

    // 行删除
    delData(row) {
      this.$confirm('确认删除该条数据?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          // 删除单个
          this.deleteParamSet(row.f_batch_id, row.vc_exec_type)
        })
        .catch(() => {})
    },

    // 取消调度
    logCancle(row) {
      this.$confirm('确认取消执行吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = { id: row.f_id }

          commonApi
            .mainLogCancle(params)
            .then(res => {
              if (res.data.status === 200) {
                this.onQuery(false)
                this.$message.closeAll()
                this.$message({
                  type: 'success',
                  message: res.data.message
                })
              } else {
                this.$message.closeAll()
                this.$message.error(res.data.message)
              }
            })
            .catch(() => {})
        })
        .catch(() => {})
    },

    //  分页
    pagination(val) {
      let { page, limit } = val
      // 起始页
      this.formQuery.pageNum = page
      // 每页数量
      this.formQuery.pageSize = limit
      // 查询
      this.onQuery(false)
    },
    //  分页2
    pagination2(val) {
      let { page, limit } = val
      // 起始页
      this.formDialog.pageNum = page
      // 每页数量
      this.formDialog.pageSize = limit
      // 查询
      this.onQuery2(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.controlRecord {
  padding-left: 10px;
  .title-style {
    color: #0F65DD;
    vertical-align: middle;
    height: 35px;
    line-height: 35px;
    font-size: 16px;
    margin-left: 5px;
  }
  .color-box {
    display: inline-block;
    height: 30px;
    width: 2px;
    background-color: #0F65DD;
  }
  .el-dialog {
    width: 80% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-input {
      // width: 120% !important;
    }
    .el-form-item {
      // min-width: 50%;
      margin-right: 0;
    }
    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 15px;
  }

  // 火狐移除
  input[type='number'] {
    -moz-appearance: textfield;
  }

  //谷歌下的移除
  input[type='number']::-webkit-inner-spin-button,
  input[type='number']::-webkit-outer-spin-button {
    -webkit-appearance: none;
  }
}
::v-deep .el-table tbody tr:hover > td {
  background: transparent !important; //修改成自己想要的颜色即可
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
::v-deep .el-button--danger.is-plain {
  background:#f4f4f5;
}
</style>
