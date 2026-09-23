<template>
  <div class="setData ddportal-ui">
    <el-form :inline="true" class="formQuery">
      <el-row>
        <el-col :span="16">
          <div style="width:100%;height:50px;"></div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" plain size="small" icon="el-icon-circle-plus-outline" @click="addDate">
              新增
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
    <span class="title-style">数据源设置信息</span>

    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      v-loading="tableLoading"
      :default-sort="{ prop: 'vcBeDate', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      style="width: 100%"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
    >
      <el-table-column type="selection" width="35" align="center"></el-table-column>

      <el-table-column prop="dbsNme" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="数据源名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dbsNme | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="dbsTyp" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="数据源类别" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dbsTyp | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="dbsUse" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="数据源用户名" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dbsUse | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="dbsDri" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="驱动程序类" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dbsDri | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="dbsUrl" show-overflow-tooltip label="连接字符串" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.dbsUrl | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="120" align="center">
        <template slot-scope="scope">
         <div class="dialog-footer standard-form">
          <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
          <el-button type="info" plain size="small" @click="delData(scope.row)">删除</el-button>
         </div>
        </template>
      </el-table-column>
    </el-table>
    <!-- <div style="margin-top:10px;font-size:14px">总共{{total}}条数据</div> -->
    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="数据源维护" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="数据源名称" prop="dbsNme" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.dbsNme" clearable placeholder="请输入"></el-input>
            </el-form-item>
            <el-form-item label="数据源类别" prop="dbsTyp" class="mb20" :label-width="formLabelWidth">
              <!-- <el-input v-model.trim="formDialog.dbsTyp" clearable placeholder="请输入"></el-input> -->

              <el-select v-model.trim="formDialog.dbsTyp" placeholder="请选择">
                <el-option label="ORACLE" value="ORACLE"></el-option>
                <el-option label="SQL SERVER" value="SQL SERVER"></el-option>
                <el-option label="MYSQL" value="MYSQL"></el-option>
                <el-option label="OceanBase" value="OceanBase"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="数据源密码" prop="dbsPas" class="mb20" :label-width="formLabelWidth">
              <el-input type="password" v-model.trim="formDialog.dbsPas" clearable placeholder="请输入"></el-input>
            </el-form-item>
            <el-form-item label="用户名" prop="dbsUse" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.dbsUse" clearable placeholder="请输入"></el-input>
            </el-form-item>
            <el-form-item label="驱动程序类" prop="dbsDri" class="mb20" :label-width="formLabelWidth" style="width:100%">
              <el-input type="textarea" v-model.trim="formDialog.dbsDri" clearable placeholder="请输入" class="textarea"></el-input>
            </el-form-item>
            <br />
            <el-form-item label="连接字符串" prop="dbsUrl" class="mb20" :label-width="formLabelWidth">
              <el-input type="textarea" v-model.trim="formDialog.dbsUrl" clearable placeholder="请输入" class="textarea"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <el-row>
        <div style="float:right;margin-bottom:10px">
          <el-button type="primary" plain size="small" @click="testData">测试连接</el-button>
        </div>
      </el-row>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealData">提 交</el-button>
        <el-button type="info" size="small" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/setData'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'

export default {
  name: 'DdSetData',
  components: {
    Pagination
  },

  data() {
    return {
      tableData: [], //表格数据
      tableLoading: false, //表格加载
      dialogMask: false, // 弹窗
      //总条数
      total: 0,

      // 查询参数
      formQuery: {
        // 排序方式
        orderBy: 'dbsCde desc',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      // 弹窗查询参数
      formDialog: {
        // 数据源名称
        dbsNme: '',
        // 数据源类别
        dbsTyp: 'ORACLE',
        // 数据源用户名
        dbsUse: '',
        // 驱动程序类
        dbsDri: '',
        // 连接字符串
        dbsUrl: '',
        // 数据源密码
        dbsPas: ''
      },
      // 弹窗验证规则
      dialogRules: {
        // 数据源名称
        dbsNme: [{ required: true, message: '请填写数据源名称', trigger: 'change' }],
        // 数据源类别
        dbsTyp: [{ required: true, message: '请填写数据源类别', trigger: 'change' }],
        // 数据源用户名
        dbsUse: [{ required: true, message: '请填写数据源用户名', trigger: 'change' }],
        // 驱动程序类
        dbsDri: [{ required: true, message: '请填写驱动程序类', trigger: 'change' }],
        // 连接字符串
        dbsUrl: [{ required: true, message: '请填写连接字符串', trigger: 'change' }],
        // 数据源密码
        dbsPas: [{ required: true, message: '请填写数据源密码', trigger: 'change' }]
      },
      // 操作类型 1、添加 2、编辑
      operationType: 1,
      formLabelWidth: '150px',
      // 批量删除的数据
      multipleSelection: []
    }
  },

  mounted() {
    this.onQuery(true)
  },
  methods: {
    // 查询
    onQuery(flag) {
      this.tableLoading = true
      if (flag) {
        this.formQuery.pageNum = 1
      }
      commonApi
        .getDataSourceList(this.formQuery)
        .then(res => {
          this.tableLoading = false

          let { list, total } = res.data.data
          // 总条数
          this.total = total
          this.tableData = []
          list.forEach(item => {
            this.tableData.push(item)
          })
        })
        .catch(() => {})
    },
    // 新增按钮
    addDate() {
      this.dialogMask = true
      this.operationType = 1
      this.$nextTick(() => {
        this.$refs['formDialog'].resetFields()
      })
    },
    // 处理数据
    dealData() {
      this.$refs['formDialog'].validate(valid => {
        if (valid) {
          if (this.operationType === 1) {
            // 添加
            this.addParamSet()
          } else {
            // 修改
            this.updateParamSet()
          }
        }
      })
    },
    // 添加参数
    addParamSet() {
      let params = Object.assign({}, this.formDialog)

      commonApi
        .addDataSource(params)
        .then(res => {
          if (res.data.status === 200) {
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.onQuery(true)
            this.dialogMask = false
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 修改参数
    updateParamSet() {
      let params = Object.assign({}, this.formDialog)

      commonApi
        .updateDataSource(params)
        .then(res => {
          if (res.data.status === 200) {
            this.onQuery(false)
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
          } else {
            this.$message.closeAll()

            this.$message.error(res.data.message)
          }
        })
        .catch(() => {})
    },
    // 单个删除
    deleteParamSet(dbsCde) {
      let params = { dbsCde: dbsCde }

      commonApi
        .deleteDataSource(params)
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
            // this.$emit("deletall", this.multipleSelection);
            let arr = []
            let str = {}

            this.multipleSelection.forEach(item => {
              arr.push(item.dbsCde)
            })
            str.dbsCdes = arr.join(',')

            commonApi
              .batchDeleteDataSource(str)
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
    // 测试连接
    testData() {
      let params = Object.assign({}, this.formDialog)

      commonApi
        .testDataSource(params)
        .then(res => {
          if (res.data.status == 200) {
            this.$message.closeAll()
            this.$message({
              type: 'success',
              message: '连接成功'
            })
          } else {
            this.$message.error('连接失败')
          }
        })
        .catch(() => {})
    },
    //列表点击排序
    handleSortChange(val) {
      this.formQuery.orderBy = fun.etlqueryOrderBy(val)
      // 查询
      this.onQuery(false)
    },
    // 行编辑
    editData(row) {
      this.dialogMask = true
      this.operationType = 2
      this.$nextTick(() => {
        // 清除
        this.$refs['formDialog'].resetFields()

        let { dbsDri, dbsTyp, dbsUrl, dbsUse, dbsNme, dbsPas, dbsCde } = row

        this.formDialog.dbsDri = dbsDri
        this.formDialog.dbsTyp = dbsTyp
        this.formDialog.dbsUrl = dbsUrl
        this.formDialog.dbsUse = dbsUse
        this.formDialog.dbsNme = dbsNme
        this.formDialog.dbsPas = dbsPas
        this.formDialog.dbsCde = dbsCde
      })
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
          this.deleteParamSet(row.dbsCde)
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
    }
  }
}
</script>

<style lang="scss" scoped>
.setData {
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
    width: 60% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-form-item {
      min-width: 50%;
      margin-right: 0;
      margin-bottom: 18px !important;
    }
    .el-input--suffix {
      margin-bottom: 3px !important;
    }

    .mr5 {
      margin-right: 5px;
    }
  }

  .mb20 {
    margin-bottom: 15px;
  }
  .textarea {
    width: 500px;
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

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
::v-deep .el-button--info {
  background-color: #f4f4f5;
}
</style>
