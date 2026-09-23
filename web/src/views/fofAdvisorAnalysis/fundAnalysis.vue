<template>
  <div class="fundAnalysis" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formQuery" :inline="true" :model="formQuery" class="standard-form analyse-page" label-width="auto">
          <el-form-item label="" prop="fundCode">
            <el-input v-model="formQuery.fundCode" placeholder="请输入产品代码" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="" prop="fundName">
            <el-input v-model="formQuery.fundName" placeholder="请输入产品名称" style="width: 175px !important;" size="small" />
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.typeDl" size="small" clearable filterable placeholder="请选择资产大类"  @change="handleDlChange">
              <el-option v-for="item in assetClass" :key="item.CODE" :label="item.NAME" :value="item.CODE" />
            </el-select>
          </el-form-item>
          <el-form-item label="">
            <el-select v-model="formQuery.typeZl" size="small" clearable filterable placeholder="请选择资产子类" :disabled="!formQuery.typeDl">
              <el-option v-for="item in filteredSubClass" :key="item.CODE" :label="item.NAME" :value="item.CODE" />
            </el-select>
          </el-form-item>
<!--          <el-form-item label="">-->
<!--            <el-select v-model="formQuery.source" size="small" clearable filterable placeholder="请选择数据来源">-->
<!--              <el-option v-for="item in sourceType" :key="item.CODE" :label="item.NAME" :value="item.CODE" />-->
<!--            </el-select>-->
<!--          </el-form-item>-->
          <el-form-item>
            <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh" @click="resetForm('formQuery')">重置</el-button>
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
          <vxe-table-column field="FUNDCODE" show-overflow-tooltip label="产品代码" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FUNDCODE | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="FUNDNAME" show-overflow-tooltip label="产品名称" min-width="220" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.FUNDNAME | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="NAMEDL" show-overflow-tooltip label="资产大类" min-width="120" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.NAMEDL | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="NAMEZL" show-overflow-tooltip label="资产子类" min-width="220" algin="left" header-align="center">
            <template slot-scope="scope">
              <span>{{ scope.row.NAMEZL | noDataFilter }}</span>
            </template>
          </vxe-table-column>
<!--          <vxe-table-column field="SJLY" show-overflow-tooltip label="数据来源" min-width="120" algin="left" header-align="center">-->
<!--            <template slot-scope="scope">-->
<!--              <span>{{ scope.row.SJLY | noDataFilter }}</span>-->
<!--            </template>-->
<!--          </vxe-table-column>-->
          <vxe-table-column label="操作" width="200" align="center" header-align="center">
            <template slot-scope="scope">
              <span class="table-operation">
                <el-button size="small" type="info" plain @click="editProduct(scope.row, 'EDIT')">编辑</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formQuery.pageNum"
          :page-size="formQuery.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </div>
    <el-dialog :title="dialogTitle" @close="handleClose" width="33% !important" center :visible.sync="visible">
      <div slot="title">
        <span style="font-size: 14px">{{ dialogTitle }}</span>
      </div>
      <el-container>
        <el-main>
          <el-form label-position="right" label-width="140px" class="standard-form" :model="formInline" ref="formInline" style="width: 100% !important">
            <el-form-item label="资产大类">
              <el-select v-model="formInline.typeDl" size="small" clearable filterable placeholder="请选择资产大类" @change="handleDlChangeEDIT">
                <el-option v-for="item in assetClass" :key="item.CODE" :label="item.NAME" :value="item.CODE" />
              </el-select>
            </el-form-item>
            <el-form-item label="资产子类">
              <el-select v-model="formInline.typeZl" size="small" clearable filterable placeholder="请选择资产子类" :disabled="!formInline.typeDl">
                <el-option v-for="item in filteredSubClassEDIT" :key="item.CODE" :label="item.NAME" :value="item.CODE" />
              </el-select>
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
import commonFun from '@/filters/new_common'
import selectApi from "@/api/fofAdvisorAnalysis/index"
export default {
  name: 'fundAnalysis',
  components: {
    Pagination,
  },
  data() {
    return {
      tableHeight: 0,
      assetSubClass:[],
      assetClass:[],
      sourceType:[],
      formQuery: {
        fundCode: '',
        fundName: '',
        typeDl: '',
        typeZl: '',
        source: '',
        pageSize: 20,
        pageNum: 1
      },
      formInline: {
        fundCode: '',
        typeDl: '',
        typeZl: ''
      },

      total: 0,
      tableData: [],
      visible: false,
      dialogTitle: '',
      currentRow: null,
      dialogStatus: '',
      tableLoading: false
    }
  },
  mounted() {
    this.handleTableHeight()
    this.handleSearchTable(true)
    this.selectType()
  },
  computed: {
    // 动态过滤子类数据
    filteredSubClass() {
      if (!this.formQuery.typeDl) return [];
      return this.assetSubClass.filter(
        item => item.CODED === this.formQuery.typeDl
      );
    },
    filteredSubClassEDIT() {
      if (!this.formInline.typeDl) return [];
      return this.assetSubClass.filter(
        item => item.CODED === this.formInline.typeDl
      );
    }
  },
  methods: {
    handleDlChange() {
      this.formQuery.typeZl = '';
    },
    handleDlChangeEDIT() {
      this.formInline.typeZl = '';
    },
    handleSearchTable(flag) {
      this.tableLoading = true
      var self = this;
      if (flag) {
        this.formQuery.pageNum = 1
      }
      const params = Object.assign({}, this.formQuery, {});
      new Promise((resolve, reject) => {
        selectApi
          .fun_fundSelectAnalysis(params)
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                const { list, total } = data;
                this.tableData = list;
                this.total = total;
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
            this.tableLoading = false;

          })
          .catch((error) => {
            this.tableLoading = false;
            reject(error);
          });
      });


    },
    selectType() {
      var self = this;
      new Promise((resolve, reject) => {
        selectApi
          .fun_fundTypeAnalysis()
          .then((res) => {
            const { status, data } = res;
            if (status === 0) {
              if (data != null && data != undefined) {
                this.assetSubClass = data.assetSubClass
                  this.assetClass = data.assetClass
                  this.sourceType = data.sourceType
              }
            } else {
              self.$message({
                message: "系统异常",
                type: "warning"
              });
            }
          })
          .catch((error) => {
            reject(error);
          });
      });


    },
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

    dealData() {
      var self = this
      self.$refs['formInline'].validate((valid) => {
        if (valid) {
            this.update()
        }
      })
    },

    editProduct(row, status) {
      this.dialogStatus = status
      this.visible = true
      this.dialogTitle = '编辑'
      this.$nextTick(() => {
        this.formInline.fundCode = row.FUNDCODE
        this.formInline.typeDl = row.TYPEDL
        this.formInline.typeZl = row.TYPEZL
      })
    },
    //修改接口
    update() {
      let params = {}
      params = commonFun.parameterSrc(this.formInline)
      new Promise((resolve, reject) => {
        selectApi
          .fun_fundUpdateAnalysis(params)
          .then((res) => {
            if (res.status === 0) {
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
            this.handleSearchTable(true)
            this.tableLoading = false
            this.visible = false
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

    handleClose() {
      // // self.$refs['formInline'].resetFields()
      this.formInline.fundCode = ''
      this.formInline.typeDl = ''
      this.formInline.typeZl = ''
      console.log('关闭弹窗')
    },
    resetForm(formName) {
      this.formQuery.fundCode= ''
        this.formQuery.fundName= ''
        this.formQuery.typeDl= ''
        this.formQuery.typeZl = ''
        this.formQuery.source = ''
    },

    pagination(val) {
      const { currentPage, pageSize } = val;
      // 起始页
      this.formQuery.pageNum = currentPage;
      // 每页数量
      this.formQuery.pageSize = pageSize;
      this.handleSearchTable(false)
    }
  }
}
</script>

<style lang="scss" scoped>
.fundAnalysis {
  .funds-filter {
    width: 100%;
    // border-bottom: 1px solid #e1e0e0;
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
</style>
