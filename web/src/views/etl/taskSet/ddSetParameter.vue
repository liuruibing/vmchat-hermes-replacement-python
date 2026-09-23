<template>
  <div class="setParameter ddportal-ui">
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
    <span class="title-style">参数列表</span>
    <el-table
      ref="multipleTable"
      @selection-change="handleSelectionChange"
      :data="tableData"
      :default-sort="{ prop: 'vcBeDate', order: 'descending' }"
      stripe
      @sort-change="handleSortChange"
      v-loading="tableLoading"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      style="width: 100%"
    >
      <el-table-column type="selection" width="35" align="center"></el-table-column>

      <el-table-column prop="paramCde" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="参数编码" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramCde | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="paramNme" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="参数名称" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramNme | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="paramTyp" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="参数类型" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramTyp | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="paramClass" sortable="custom" :sort-orders="['ascending', 'descending']" show-overflow-tooltip label="类名" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramClass | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="paramMethod" show-overflow-tooltip label="方法名" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramMethod | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="paramCmt" show-overflow-tooltip label="说明" min-width="100" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.paramCmt | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="120" align="center">
        <template slot-scope="scope">
          <div class="dialog-footer standard-form">
            <el-button type="info" size="small" plain @click="editData(scope.row)">编辑</el-button>
            <el-button type="info"  size="small" plain @click="delData(scope.row)">删除</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
    <!-- <div style="margin-top:10px;font-size:14px">总共{{total}}条数据</div> -->
    <!-- 分页 -->
    <Pagination :total="total" :limit="formQuery.pageSize" :page="formQuery.pageNum" @pagination="pagination"></Pagination>

    <!-- 新增/修改 参数弹窗 -->
    <el-dialog title="参数维护" center :visible.sync="dialogMask" :close-on-click-modal="false">
      <el-container class="hg100">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formDialog" :model="formDialog" :rules="dialogRules" label-position="right">
            <el-form-item label="参数编码" prop="paramCde" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.paramCde" disabled clearable placeholder="请输入" size="small" v-if="operationType == 2"></el-input>
              <el-input v-model.trim="formDialog.paramCde" clearable placeholder="请输入" size="small" v-else></el-input>
            </el-form-item>
            <el-form-item label="参数名称" prop="paramNme" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.paramNme" disabled clearable placeholder="请输入" size="small" v-if="operationType == 2"></el-input>
              <el-input v-model.trim="formDialog.paramNme" v-else clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>

            <el-form-item label="类名" prop="paramClass" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.paramClass" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="方法名" prop="paramMethod" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.paramMethod" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <el-form-item label="参数类型" prop="paramTyp" class="mb20" :label-width="formLabelWidth">
              <el-input v-model.trim="formDialog.paramTyp" clearable placeholder="请输入" size="small"></el-input>
            </el-form-item>
            <br />
            <el-form-item label="说明" prop="paramCmt" class="mb20" :label-width="formLabelWidth" style="width:100%">
              <el-input type="textarea" v-model.trim="formDialog.paramCmt" clearable placeholder="请输入" style="width:500px"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="dealData">提 交</el-button>
        <el-button size="small" type="info" plain @click="dialogMask = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonApi from '@/api/etl/setParameter'
import Pagination from '@/components/Pagination'
import fun from '@/filters/common'

export default {
  name: 'DdSetParameter',
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
        // 排序条件
        // sort: "paramCde",
        // 排序方式
        orderBy: 'paramCde desc',
        // 起始页
        pageNum: 1,
        // 每页数量
        pageSize: 10
      },
      // 弹窗查询参数
      formDialog: {
        // 参数名称
        paramNme: '',
        // 参数编号
        paramCde: '',
        // 类名
        paramClass: '',
        // 方法名
        paramMethod: '',
        // 参数类型
        paramTyp: '',
        // 说明
        paramCmt: ''
      },
      // 弹窗验证规则
      dialogRules: {
        // 参数名称
        paramNme: [{ required: true, message: '请填写参数名称', trigger: 'change' }],
        // 参数编号
        paramCde: [{ required: true, message: '请填写参数编号', trigger: 'change' }]
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
        .getParamSetList(this.formQuery)
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
            this.onlyCode()
          } else {
            // 修改
            this.updateParamSet()
          }
        }
      })
    },
    // 添加代码需要唯一性
    onlyCode() {
      let params = { paramCode: this.formDialog.paramCde }
      commonApi
        .selectParamSetByCode(params)
        .then(res => {
          if (res.data.status == 200) {
            this.$message.closeAll()

            this.$message.error('编码已经存在，请勿重复添加！')
          } else {
            this.addParamSet()
          }
        })
        .catch(() => {})
    },

    // 添加参数
    addParamSet() {
      let params = Object.assign({}, this.formDialog)
      commonApi
        .addParamSet(params)
        .then(res => {
          if (res.data.status === 200) {
            this.$message.closeAll()

            this.$message({
              type: 'success',
              message: res.data.message
            })
            this.dialogMask = false
            this.onQuery(true)
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
        .updateParamSet(params)
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
    deleteParamSet(paramCde) {
      let params = { paramCde: paramCde }
      commonApi
        .deleteParamSet(params)
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

            this.multipleSelection.forEach(item => {
              arr.push(item.paramCde)
            })
            str.paramCodes = arr.join(',')

            commonApi
              .batchDeleteParamSet(str)
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

        let { paramNme, paramCde, paramClass, paramMethod, paramTyp, paramCmt } = row

        this.formDialog.paramNme = paramNme
        this.formDialog.paramCde = paramCde
        this.formDialog.paramClass = paramClass
        this.formDialog.paramMethod = paramMethod
        this.formDialog.paramTyp = paramTyp
        this.formDialog.paramCmt = paramCmt
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
          this.deleteParamSet(row.paramCde)
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
.setParameter {
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
    width: 54% !important;
    .el-form {
      width: 100% !important;
      font-size: 0;
    }
    .el-form-item {
      min-width: 50%;
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
  background-color: transparent !important; //修改成自己想要的颜色即可
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
