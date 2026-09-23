<template>
  <div class="fofSun" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form analyse-page" label-width="auto">
          <el-form-item label="" prop="fofCode">
            <el-input v-model="formQuery.fofCode" placeholder="请输入母基金产品代码" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fofName">
            <el-input v-model="formQuery.fofName" placeholder="请输入母基金产品名称" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fofSunFzCode">
            <el-input v-model="formQuery.fofSunFzCode" placeholder="请输入子基金辅助代码" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fofSunFzName">
            <el-input v-model="formQuery.fofSunFzName" placeholder="请输入子基金辅助名称" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fofSunCode">
            <el-input v-model="formQuery.fofSunCode" placeholder="请输入子基金产品代码" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fofSunName">
            <el-input v-model="formQuery.fofSunName" placeholder="请输入子基金产品名称" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="queryExamineList">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh" @click="resetForm('formQuery')">重置</el-button>
            <el-button type="primary" size="small" icon="el-icon-plus" @click="addProduct('ADD')">新增</el-button>
          </el-form-item>


        </el-form>
      </div>
    </div>
    <div id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
          resizable
        >
          <vxe-table-column type="index" width="50" header-align="cener" align="center" label="序号"></vxe-table-column>
          <vxe-table-column field="fofCode" show-overflow-tooltip label="母基金产品代码" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFCODE | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fofName" show-overflow-tooltip label="母基金产品名称" min-width="220" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fofSunFzCode" show-overflow-tooltip label="子基金辅助代码" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFSUNFZCODE | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fofSunFzName" show-overflow-tooltip label="子基金辅助名称" min-width="220" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFSUNFZNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fofSunCode" show-overflow-tooltip label="子基金产品代码" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFSUNCODE | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="fofSunName" show-overflow-tooltip label="子基金产品名称" min-width="220" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FOFSUNNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="操作" width="200" align="right" header-align="center">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button :underline="false" size="small" type="info" plain @click="editProduct(scope.row, 'EDIT')">编辑</el-button>
                <el-button  size="small" type="info" plain @click="deleteFund(scope.row)">删除</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery._pageNum"
          :page-size="formQuery._pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          class="standard-vxe-pager"
          size="medium"
          @page-change="pagination"
        />
      </div>
    </div>
    <el-dialog :title="dialogTitle" v-dialogDragWidth @close="handleClose" width="33% !important" center :visible.sync="visible" >
      <div slot="title">
        <span style="font-size: 14px">{{ dialogTitle }}</span>
      </div>
      <el-container>
        <el-main>
          <el-form label-position="right" label-width="140px" class="standard-form" :model="formInline" ref="formInline" :rules="formRules" style="width: 100% !important">
            <el-form-item label="母基金产品代码" prop="fofCode">
              <ProductSelectInput
                v-model="formInline.product"
                placeholder="请选择母基金产品"
                :input-width="'260px'"
                @select="handleMotherFundSelect"
                @clear="handleMotherFundClear"
              />
            </el-form-item>
            <el-form-item label="子基金产品代码" prop="fofSunCode">
              <ProductSelectInput
                v-model="formInline.product2"
                placeholder="请选择子基金产品"
                :input-width="'260px'"
                @select="handleChildFundSelect"
                @clear="handleChildFundClear"
              />
            </el-form-item>

            <el-form-item label="子基金辅助代码" prop="fofSunFzCode" title="此处须填写该基金在FOF基金估值表中对应证券代码，以便FOF构建时能正确找到该基金信息">
              <el-input clearable placeholder="请输入" size="small" v-model="formInline.fofSunFzCode"></el-input>
            </el-form-item>
            <el-form-item label="子基金辅助名称" prop="fofSunFzName">
              <el-input clearable placeholder="请输入" size="small" v-model="formInline.fofSunFzName"></el-input>
            </el-form-item>
          </el-form>
        </el-main>
      </el-container>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" :loading="tableLoading" @click="dealData()">提 交</el-button>
        <el-button size="small" type="info" plain @click="visible = false" :loading="tableLoading">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import commonAPI from '@/api/common.js'
import commonFun from '@/filters/new_common'
import fofSunApi from '@/api/FofSun/fofSun.js'
// 导入ProductSelectInput悬浮选择框组件
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'fofSun',
  components: {
    Pagination,
    ProductSelectInput // 注册悬浮选择框组件
  },
  data() {
    return {
      tableHeight: 0,
      fId: '',
      formQuery: {
        fofCode: '',
        fofName: '',
        fofSunFzCode:'',
        fofSunFzName:'',
        fofSunCode: '',
        fofSunName: '',
        _pageSize: 20,
        _pageNum: 1
      },
      formInline: {
        product:null,
        product2:null,
        fofCode: '',
        fofName: '',
        fofSunCode: '',
        fofSunName: '',
        fofSunFzCode: '',
        fofSunFzName: '',
        fId: ''
      },
      formRules: {
        fofCode: [{ required: true, message: '请填写母基金产品代码', trigger: 'blur ' }],
        fofSunCode: [{ required: true, message: '请填写子基金产品代码', trigger: 'blur ' }]
      },
      total: 0,
      tableData: [],
      visible: false,
      dialogTitle: '',
      currentRow: null,
      dialogStatus: 'ADD',
      tableLoading: false
    }
  },
  mounted() {
    this.handleTableHeight()
    this.initData()
  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 175
        }
      })
    },
    /**
     * 母基金产品选择事件
     * @param {Object} product 选中的产品对象
     */
    handleMotherFundSelect(product) {
      console.log('选中母基金产品：', product)
      this.formInline.fofCode = product.VC_FUNDCODE || ''
      this.formInline.fofName = product.VC_FUNDNAME || '' // 自动填充母基金名称
    },
    /**
     * 母基金产品清除事件
     */
    handleMotherFundClear() {
      console.log('清除母基金产品选择')
      this.formInline.fofCode = ''
      this.formInline.fofName = ''
    },
    /**
     * 子基金产品选择事件
     * @param {Object} product 选中的产品对象
     */
    handleChildFundSelect(product) {
      console.log('选中子基金产品：', product)
      this.formInline.fofSunCode = product.VC_FUNDCODE || ''
      this.formInline.fofSunName = product.VC_FUNDNAME || '' // 自动填充子基金名称
    },
    /**
     * 子基金产品清除事件
     */
    handleChildFundClear() {
      console.log('清除子基金产品选择')
      this.formInline.fofSunCode = ''
      this.formInline.fofSunName = ''
    },
    async initData() {
      await this.queryExamineList()
    },
    async queryExamineList() {
      this.tableLoading = true
      try {
        const data = {
          indexCode: '66b47f40-e8f3-4d4b-b6b4-bc1c90233e8e',
          fofCode: this.formQuery.fofCode,
          fofName: this.formQuery.fofName,
          fofSunCode: this.formQuery.fofSunCode,
          fofSunName: this.formQuery.fofSunName,
          fofSunFzCode: this.formQuery.fofSunFzCode,
          fofSunFzName: this.formQuery.fofSunFzName,
          _pageNum: this.formQuery._pageNum,
          _pageSize: this.formQuery._pageSize,
          _pageFlag: true
        }
        if (this.$route.path.includes('/sjwh/fofzjjwhzf')) {
          data.indexCode = '6c9a52f2-ec64-415d-ac1e-78fb471d5e1a'
        }
        const res = await commonAPI.getDataBysqlCode(data)
        let { status } = res.data
        if (status == 0) {
          this.tableData = res.data.data.rows
          this.total = res.data.data.total
          this.tableLoading = false
        } else {
          this.tableData = []
          this.total = 0
          this.tableLoading = false
        }
      } catch (e) {
        this.tableData = []
        this.total = 0
        this.tableLoading = false
      }
    },
    addProduct(status) {
      this.visible = true
      this.dialogTitle = '新增'
      this.dialogStatus = status
      // 新增时清空表单
      this.formInline = {
        fofCode: '',
        fofName: '',
        fofSunCode: '',
        fofSunName: '',
        fofSunFzCode: '',
        fofSunFzName: '',
        fId: ''
      }
    },
    dealData() {
      var self = this
      self.$refs['formInline'].validate((valid) => {
        if (valid) {
          if (this.dialogStatus === 'ADD') {
            this.insert()
          } else {
            this.update()
          }
        }
      })
    },
    //新增接口
    insert() {
      let params = {}
      params = commonFun.parameterSrc(this.formInline)
      new Promise((resolve, reject) => {
        fofSunApi
          .addFofSun(params)
          .then((res) => {
            let { status, data } = res
            if (status === 200) {
              this.$message({
                message: '新增成功',
                type: 'success',
                customClass: 'message-success'
              })
            } else {
              this.$message({
                message: res.message,
                type: 'warning',
                customClass: 'message-warning'
              })
            }
            this.tableLoading = false
            this.visible = false
            this.queryExamineList()
          })
          .catch((error) => {
            reject(error)
            this.tableLoading = false
            this.visible = false
            this.$message({
              message: '新增失败',
              type: 'warning',
              customClass: 'message-warning'
            })
          })
      })
    },
    editProduct(row, status) {
      this.dialogStatus = status
      this.visible = true
      this.dialogTitle = '编辑'
      this.$nextTick(() => {
        this.formInline.fofCode = row.FOFCODE
        this.formInline.fofName = row.FOFNAME // 回显母基金名称
        this.formInline.fofSunCode = row.FOFSUNCODE
        this.formInline.fofSunName = row.FOFSUNNAME // 回显子基金名称
        this.formInline.fofSunFzCode = row.FOFSUNFZCODE
        this.formInline.fofSunFzName = row.FOFSUNFZNAME
        this.fId = row.ID
        this.formInline.product = {
          VC_FUNDCODE:row.FOFCODE,
          VC_FUNDNAME:row.FOFNAME

        }
        this.formInline.product2 = {
          VC_FUNDCODE:row.FOFSUNCODE,
          VC_FUNDNAME:row.FOFSUNNAME

        }
      })
    },
    //修改接口
    update() {
      let params = {}
      params = commonFun.parameterSrc(this.formInline)
      params.id = this.fId
      new Promise((resolve, reject) => {
        fofSunApi
          .editFofSun(params)
          .then((res) => {
            let { status, data } = res
            if (status === 200) {
              this.$message({
                message: '修改成功',
                type: 'success',
                customClass: 'message-success'
              })
            } else {
              this.$message({
                message: res.message,
                type: 'warning',
                customClass: 'message-warning'
              })
            }
            this.tableLoading = false
            this.visible = false
            this.queryExamineList()
          })
          .catch((error) => {
            reject(error)
            this.tableLoading = false
            this.visible = false
            this.$message({
              message: '修改失败',
              type: 'warning',
              customClass: 'message-warning'
            })
          })
      })
    },
    async deleteFund(row) {
      const params = {
        id: row.ID || ''
      }
      this.$confirm('是否删除该条记录？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          fofSunApi
            .deleteFofSun(params)
            .then((res) => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '删除成功',
                  customClass: 'message-success'
                })
                this.queryExamineList()
              } else {
                this.$message({
                  type: 'error',
                  message: '删除失败',
                  customClass: 'message-error'
                })
              }
            })
            .catch((e) => {
              this.$message({
                type: 'error',
                message: '删除失败',
                customClass: 'message-error'
              })
            })
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消操作'
          })
        })
    },
    handleClose() {
      // 关闭弹窗时清空表单
      this.formInline.fofCode = ''
      this.formInline.fofName = ''
      this.formInline.fofSunCode = ''
      this.formInline.fofSunName = ''
      this.formInline.fofSunFzCode = ''
      this.formInline.fofSunFzName = ''
      this.fId = ''
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    pagination(val) {
      const { currentPage, pageSize } = val;
      this.formQuery._pageNum = currentPage;
      this.formQuery._pageSize = pageSize;
      this.queryExamineList()
    }
  }
}
</script>

<style lang="scss" scoped>
.fofSun {
  .funds-filter {
    width: 100%;
  }
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
}

.search_button_com::after {
  content: '';
  clear: both;
}
::v-deep .vxe-table .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .el-button--danger {
  color: #F56C6C;
  background-color: #fff;
  border-color: #F56C6C;
}
::v-deep .el-dialog__body {
  overflow: visible !important;
}
::v-deep .el-main {
  overflow: visible !important;
}
</style>
