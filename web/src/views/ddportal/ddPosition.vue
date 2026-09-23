<template>
  <div class="DdPosition ddportal-ui">
    <el-form :inline="true" ref="formInline" :model="formInline" style="margin-bottom: 8px" class="demo-form-inline form_inline_search">
      <el-row>
        <el-col :span="16">
          <div style="width: 100%">
            <el-form-item label="岗位编码" prop="positionCode">
              <el-input v-model="formInline.positionCode" clearable size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="岗位名称" prop="positionName">
              <el-input v-model="formInline.positionName" clearable size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="岗位类型" prop="positionType">
              <el-select size="small" clearable v-model="formInline.positionType" placeholder="请选择">
                <el-option v-for="item in positionTypeArr" :key="item.type" :label="item.name" :value="item.type"></el-option>
              </el-select>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" @click="onSubmit('formInline', true)" style="margin-bottom: 5px" size="small">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <el-button type="info" @click="restForm()" style="margin-bottom: 5px" size="small">
              <i class="el-icon-delete"></i>
              重置
            </el-button>
            <el-button type="primary" plain @click="addData()" style="margin-bottom: 5px" size="small">
              <i class="el-icon-circle-plus-outline"></i>
              添加
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <div style="vertical-align: middle; display: inline-block">
      <div class="color-box"></div>
    </div>
    <span class="title-style">岗位列表信息</span>
    <el-table
      ref="multipleTable"
      @selection-change="handleAddSelectionChange"
      :data="tableData"
      stripe
      v-loading="addTableLoading"
      style="width: 100%"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
    >
      <el-table-column prop="positionCode" show-overflow-tooltip label="岗位编码" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.positionCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="posiAndDept" show-overflow-tooltip label="岗位名称" min-width="100" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.posiAndDept | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="positionType" show-overflow-tooltip label="岗位类型" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ dataStatus(scope.row.positionType) | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="remark" show-overflow-tooltip label="描述" min-width="70" algin="left" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.remark | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" min-width="80" align="center">
        <template slot-scope="scope">
          <el-button type="primary" size="small" @click="editData(scope.row)">编辑</el-button>
          <el-button type="danger" plain size="small" @click="delData(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination="PaginationAdd"></Pagination>

    <!-- 新增 -->
    <el-dialog :title="countTitle" v-dialogDrag center :visible.sync="countDialog" :close-on-click-modal="false">
      <el-container style="height: 140px">
        <el-main class="mainBox">
          <el-form :inline="true" ref="formCount" :model="formCount" :rules="countRules" label-position="right">
            <el-form-item label="岗位编码" prop="positionCode" :label-width="formLabelWidth">
              <el-input v-if="this.operationType == 1" v-model="formCount.positionCode" maxlength="16" size="small" placeholder="请输入内容"></el-input>
              <el-input v-else disabled v-model="formCount.positionCode" maxlength="16" size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="岗位名称" prop="positionName" :label-width="formLabelWidth">
              <el-input v-model="formCount.positionName" size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="岗位类型" prop="positionType" :label-width="formLabelWidth">
              <el-select size="small" v-model="formCount.positionType" placeholder="请选择">
                <el-option v-for="item in positionTypeArr" :key="item.type" :label="item.name" :value="item.type"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="岗位备注" prop="remark" :label-width="formLabelWidth">
              <el-input style="width: 400px !important" type="textarea" v-model.trim="formCount.remark" clearable :rows="2" placeholder="请输入" size="small"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="countDialog = false">取 消</el-button>
        <el-button type="primary" size="small" :loading="countSubmit_btn" @click="countSubmit('formCount')">确 定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import commonFun from '@/filters/common.js'
import Pagination from '@/components/Pagination'
import pageApi from '@/api/ddportal/position.js'
export default {
  name: 'DdPosition',
  components: {
    Pagination
  },
  data() {
    return {
      //查询列表数据
      formInline: {
        positionCode: '', //岗位编码
        positionName: '', //岗位名称
        positionType: '', //岗位类型
        orderStr: 'positionCode desc nulls last', //列表排序
        pageSize: 10,
        pageNum: 1
      },
      total: 0, //列表条数
      addTableLoading: false, //列表加载
      positionTypeArr: [], //岗位类型
      tableData: [], //列表
      tableMultipleSelection: [], //表格选择数据集合
      countDialog: false, // 弹窗
      countTitle: '', //标题
      countFormList: '', //是新增还是编辑
      formLabelWidth: '120px',
      // 新增 编辑岗位表单
      formCount: {
        positionCode: '', //岗位编码
        positionName: '', //岗位名称
        positionType: '', //岗位类型
        remark: '' //备注
      },

      // 操作类型 1、添加 2、编辑
      operationType: 1,
      countSubmit_btn: false,
      //新增，编辑必填
      countRules: {
        positionCode: [
          {
            required: true,
            type: 'string',
            message: '请输入岗位编码',
            trigger: 'change'
          }
        ],
        positionName: [
          {
            required: true,
            type: 'string',
            message: '请输入岗位名称',
            trigger: 'change'
          }
        ],
        positionType: [
          {
            required: true,
            message: '请选择岗位类型',
            trigger: 'change'
          }
        ]
      },
      positionTypeArrs: {} //岗位类型数据字典
    }
  },
  mounted() {
    this.getPositionType()
    this.onSubmit('formInline', true)
  },
  methods: {
    // 查询
    onSubmit(formName, flag) {
      this.addTableLoading = true

      let params = commonFun.parameterSrc(this.formInline)

      pageApi
        .getDataSourceList(params)
        .then((response) => {
          if (!response.data.error) {
            this.tableData = response.data.data.list
            // 页面总条数
            this.total = response.data.data.total
          } else {
            this.tableData = []
            this.total = 0
            this.formInline.pageSize = 10
            this.formInline.pageNum = 1
          }
          this.addTableLoading = false
        })
        .catch(() => {
          this.tableData = []
          this.total = 0
          this.formInline.pageSize = 10
          this.formInline.pageNum = 1
          this.addTableLoading = false
        })
    },
    handleAddSelectionChange(val) {
      this.tableMultipleSelection = val
    },

    PaginationAdd(val) {
      this.formInline.pageSize = val.limit //页面条数
      this.formInline.pageNum = val.page //页面
      this.onSubmit('formInline', false)
    },
    //新增数据
    addData() {
      this.countTitle = '新增岗位'
      this.countFormList = 'add'
      this.countDialog = true
      this.operationType = 1

      // 清除
      this.$nextTick(() => {
        this.$refs['formCount'].resetFields()

        this.formCount.positionCode = ''
        this.formCount.positionName = ''
        this.formCount.positionType = ''
        this.formCount.remark = ''
      })
    },
    //新增岗位确认
    countSubmit(formName) {
      var self = this
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$message.closeAll()
          if (this.operationType === 1) {
            // 添加
            this.ckeckPositionType()
          } else {
            // 修改
            this.updateParamSet()
          }
        } else {
          return false
        }
      })
    },
    ckeckPositionType() {
      this.$confirm('确定新增?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params.postionCode = this.formCount.positionCode
          this.countSubmit_btn = true
          pageApi
            .ckeckPositionType(params)
            .then((response) => {
              if (!response.data.error) {
                this.saveData()
              } else {
                // 关闭移动指标弹框
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '校验失败',
                  type: 'warning'
                })
                this.countSubmit_btn = false
              }
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countSubmit_btn = false
              this.$message.closeAll()
              this.$message({
                message: '校验失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.countSubmit_btn = false
        })
    },
    saveData() {
      let params = {}
      params = commonFun.parameterSrc(this.formCount)
      this.countSubmit_btn = true
      pageApi
        .addDataSource(params)
        .then((response) => {
          if (!response.data.error) {
            // 关闭移动指标弹框
            this.countDialog = false
            this.$message.closeAll()
            this.$message({
              message: '新增成功',
              type: 'success'
            })
            // 刷新列表

            this.onSubmit('formInline', true)
          } else {
            // 关闭移动指标弹框
            this.countDialog = false
            this.$message.closeAll()
            this.$message({
              message: response.data.error || '新增失败',
              type: 'warning'
            })
          }
          this.countSubmit_btn = false
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.countDialog = false
          this.countSubmit_btn = false
          this.$message.closeAll()
          this.$message({
            message: '新增失败',
            type: 'warning'
          })
        })
    },
    updateParamSet() {
      this.$confirm('确定修改?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params = commonFun.parameterSrc(this.formCount)
          this.countSubmit_btn = true
          pageApi
            .updateDataSource(params)
            .then((response) => {
              if (!response.data.error) {
                // 关闭移动指标弹框
                this.countDialog = false
                this.$message.closeAll()
                this.$message({
                  message: '修改成功',
                  type: 'success'
                })
                // 刷新树列表
                this.onSubmit('formInline', false)
              } else {
                // 关闭移动指标弹框
                this.countDialog = false
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '修改失败',
                  type: 'warning'
                })
              }
              this.countSubmit_btn = false
            })
            .catch(() => {
              // 关闭移动指标弹框
              this.countDialog = false
              this.countSubmit_btn = false
              this.$message.closeAll()
              this.$message({
                message: '修改失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {
          // 关闭移动指标弹框
          this.countDialog = false
          this.countSubmit_btn = false
        })
    },
    //修改数据
    modifierData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要修改的数据',
          type: 'warning'
        })
      } else if (this.tableMultipleSelection.length > 1) {
        this.$message.closeAll()
        this.$message({
          message: '只能选择一行数据',
          type: 'warning'
        })
      } else {
        this.editData(this.tableMultipleSelection[0])
      }
    },
    // 行编辑数据
    editData(row) {
      this.countTitle = '编辑岗位值'
      this.countFormList = 'edit'
      this.countDialog = true
      this.operationType = 2

      this.$nextTick(() => {
        this.$refs['formCount'].resetFields()
        let { positionCode, positionName, positionType, remark } = row

        this.formCount.positionCode = positionCode
        this.formCount.positionName = positionName
        this.formCount.positionType = positionType

        this.formCount.remark = remark
      })
    },
    // 按钮批量删除
    deleteData() {
      if (this.tableMultipleSelection.length === 0) {
        this.$message.closeAll()
        this.$message({
          message: '请选择要删除的数据',
          type: 'warning'
        })
      } else {
        this.delData(this.tableMultipleSelection)
      }
    },
    // 行删除数据
    delData(row) {
      this.$confirm('确定删除?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
      })
        .then(() => {
          let params = {}
          params.positionCode = row.positionCode
          pageApi
            .deleteDataSource(params)
            .then((response) => {
              if (!response.data.error) {
                this.$message.closeAll()
                this.$message({
                  message: '删除成功',
                  type: 'success'
                })
                // 刷新树列表
                this.onSubmit('formInline', false)
              } else {
                this.$message.closeAll()
                this.$message({
                  message: response.data.error || '删除失败',
                  type: 'warning'
                })
              }
            })
            .catch(() => {
              // 关闭移动指标弹框

              this.$message.closeAll()
              this.$message({
                message: '删除失败',
                type: 'warning'
              })
            })
        })
        .catch(() => {})
    },
    //获取岗位类型
    getPositionType() {
      pageApi
        .getPositionType()
        .then((response) => {
          if (!response.data.error) {
            let arr = response.data.data
            for (let i = 0; i < arr.length; i++) {
              let type = parseInt(arr[i].type)
              this.positionTypeArrs[type] = arr[i].name
              arr[i].type = type
            }
            this.positionTypeArr = arr
          } else {
            this.$message({
              message: '初始化岗位类型失败',
              type: 'warning'
            })
          }
        })
        .catch(() => {
          this.$message({
            message: '初始化岗位类型失败',
            type: 'warning'
          })
        })
    },
    //数据字典转换
    dataStatus(statusCode) {
      return this.positionTypeArrs[statusCode]
    },
    restForm() {
      //查询列表数据
      this.formInline.positionCode = '' //岗位编码
      this.formInline.positionName = '' //岗位名称
      this.formInline.positionType = '' //岗位类型
    }
  }
}
</script>

<style lang="scss" scoped>
.DdPosition {
  padding-left: 8px;
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
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}
::v-deep .el-table tbody .el-table__row:hover > td {
  background-color: #fff !important; //修改成自己想要的颜色即可
}

::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background: #f7f7f7 !important;
}

::v-deep .el-dialog__wrapper .el-dialog__header span {
  color: #333 !important;
}
</style>
