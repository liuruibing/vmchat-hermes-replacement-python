<template>
  <el-dialog :visible.sync="productSelectDialogVisible" append-to-body width="80%" @close="handleDialogClose">
    <div style="font-size: 18px; color: #20201f; margin-bottom: 16px; text-align: center">产品选择</div>
    <el-row>
      <el-col :span="24" class="center-padding-left" v-if="multiple">
        <div class="center-dialog">
          <el-form :model="formQuery" class="center-form-bg standard-form">
            <el-input v-model="formQuery.productName" placeholder="基金简称/拼音/备案号" style="width: 180px !important" />
            <el-button :loading="searchLoading" size="small" type="primary" @click="handleSelect(true)">搜索</el-button>
          </el-form>
          <div id="standard-table">
            <el-table
              ref="table"
              v-loading="searchLoading"
              :cell-style="{ height: '50px', fontSize: '14px' }"
              :header-cell-style="{ color: '#333', height: '54px', background: '#edf3fd!important' }"
              :data="tableData"
              max-height="385px"
              stripe
              style="width: 100%"
              @select="handleSelectionChange"
            >
              <el-table-column align="center" header-align="center" type="selection" width="55">
                <template slot-scope=""></template>
              </el-table-column>
              <template v-for="item in columns">
                <el-table-column :key="item.key" :align="item.align" :label="item.label" :min-width="item.width" :prop="item.prop" header-align="center" show-overflow-tooltip="">
                  <template slot-scope="scope">
                    <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                  </template>
                </el-table-column>
              </template>
            </el-table>
            <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="Pagination"></Pagination>
          </div>
        </div>
      </el-col>
      <el-col :span="24" class="center-padding-left" v-else>
        <div class="center-dialog">
          <el-form :model="formQuery" class="center-form-bg standard-form">
            <el-input v-model="formQuery.productName" placeholder="基金简称/拼音/备案号" style="width: 180px !important" />
            <el-button :loading="searchLoading" size="small" type="primary" @click="handleSelect(true)">搜索</el-button>
          </el-form>
          <div id="standard-table">
            <el-table
              ref="table"
              v-loading="searchLoading"
              :cell-style="{ height: '50px', fontSize: '14px' }"
              :header-cell-style="{ color: '#333', height: '54px', background: '#edf3fd!important' }"
              :data="tableData"
              max-height="385px"
              stripe
              style="width: 100%"
              @select="handleSelectionChange"
            >
              <el-table-column align="center" header-align="center" type="selection" width="55">
                <template slot-scope=""></template>
              </el-table-column>
              <template v-for="item in columns">
                <el-table-column :key="item.key" :align="item.align" :label="item.label" :min-width="item.width" :prop="item.prop" header-align="center" show-overflow-tooltip="">
                  <template slot-scope="scope">
                    <span v-if="item.filter == 'normal'">{{ scope.row[item.prop] | noDataFilter }}</span>
                  </template>
                </el-table-column>
              </template>
            </el-table>
            <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="Pagination"></Pagination>
          </div>
        </div>
      </el-col>
    </el-row>
    <div slot="footer" class="dialog-footer-center standard-form">
      <el-button size="small" type="info" plain @click="handleDialogClose">取 消</el-button>
      <el-button size="small" type="primary" @click="handleSubmit">确定</el-button>
    </div>
  </el-dialog>
</template>
<script>
import Pagination from '@/components/Pagination'
import draggable from 'vuedraggable'
import commonApi from '@/api/common'
import lodash from 'lodash'

export default {
  components: { Pagination, draggable },
  props: {
    title: {
      type: String,
      required: false,
      default: '产品范围'
    },
    limit: {
      type: Number,
      required: false,
      default: -1
    },
    dialogVisible: {
      type: Boolean,
      required: true,
      default: false
    },
    selectList: {
      type: Array,
      required: true,
      default: () => {
        return []
      }
    },
    multiple: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      searchLoading: false,
      formQuery: {
        productName: '',
        pageNum: 1,
        pageSize: 20
      },
      defaultProps: {
        children: 'children',
        label: 'label'
      },
      total: 0,
      selectProductStr: '',
      productSelectDialogVisible: false,
      columns: [
        {
          label: '产品代码',
          prop: 'VC_FUNDCODE',
          align: 'center',
          width: '80px',
          filter: 'normal'
        },
        {
          label: '产品名称',
          prop: 'VC_FUNDNAME',
          align: 'left',
          width: '150px',
          filter: 'normal'
        },
        {
          label: '成立日期',
          prop: 'D_CREATE_DATE',
          align: 'center',
          width: '100px',
          filter: 'normal'
        },
        {
          label: '子策略类型',
          prop: 'VC_STRATEGY',
          align: 'center',
          width: '100px',
          filter: 'normal'
        }
      ],
      selectListDialog: [],
      tableData: [],
      treeData: []
    }
  },
  watch: {
    selectList: {
      handler(val) {
        this.selectListDialog && (this.selectListDialog = [...val]) && (this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`)
      },
      deep: true,
      immediate: true
    },
    dialogVisible: {
      handler(val) {
        this.productSelectDialogVisible = val
        if (this.productSelectDialogVisible === true) {
          this.$nextTick(() => {
            this.handleSelect(true)
          })
        }
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    if (this.limit !== -1) {
      this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
    }
  },
  methods: {
    handleDelete(element) {
      const index = this.selectListDialog.findIndex((item) => item.VC_FUNDCODE === element.VC_FUNDCODE)
      if (index !== -1) {
        this.selectListDialog.splice(index, 1)
      }
      // 删除 表格的数据
      for (let i = 0; i < this.tableData.length; i++) {
        if (element.VC_FUNDCODE === this.tableData[i].VC_FUNDCODE) {
          this.$refs.table.toggleRowSelection(this.tableData[i], false)
          break
        }
      }
      if (this.limit !== -1) {
        this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
      }
    },
    // 点击确定按钮
    handleSubmit() {
      this.$emit('submitdialog', this.selectListDialog)
    },
    // 处理搜索按钮的逻辑
    handleSelect(flag) {
      const params = {}
      params.indexCode = '5235512d-1c76-4af3-8d2b-9ad93225588e'
      params.userInput = this.formQuery.productName
      params._pageNum = this.formQuery.pageNum
      params._pageSize = this.formQuery.pageSize
      params._pageFlag = true
      this.searchLoading = true
      commonApi
        .getDataBysqlCode(params)
        .then((res) => {
          const { status, data } = res.data
          if (status === 0) {
            this.tableData = data.rows
            this.total = data.total
            if (this.tableData.length > 0) {
              this.handleSameStatus()
            }
          } else {
            this.total = 0
          }
          this.searchLoading = false
        })
        .catch((err) => {
          this.searchLoading = false
          this.total = 0
        })
    },
    // 同步选中状态
    handleSameStatus() {
      if (!this.multiple) {
        if (this.selectListDialog.length > 1) {
          this.selectListDialog = this.selectListDialog.slice(0, 1)
        }
      }
      this.selectListDialog.forEach((item) => {
        const row = this.tableData.find((sitem) => sitem.VC_FUNDCODE === item.VC_FUNDCODE)
        this.$nextTick(() => {
          this.$refs.table && this.$refs.table.toggleRowSelection(row, true)
        })
      })
    },
    Pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.handleSelect(false)
    },
    handleSelectionChange(selection, row) {
      const selected = selection.length && selection.indexOf(row) !== -1
      if (selected) {
        if (!this.multiple) {
          if (this.selectListDialog.length > 0) {
            this.$refs.table.toggleRowSelection(selection[0], false)
            this.selectListDialog = []
            // this.$message.closeAll()
            // this.$message.warning('此页面为产品单选')
            // 取消当前勾选
            // return
          }
        }
        if (this.limit !== -1 && this.selectListDialog.length >= this.limit) {
          this.$message.closeAll()
          this.$message.warning(`产品最多${this.limit}个`)

          //把tableData里面check状态改为false
          this.$refs.table.toggleRowSelection(row, false)
          return
        }
        this.selectListDialog.push({ ...row })
      } else {
        const index = this.selectListDialog.findIndex((item) => item.VC_FUNDCODE === row.VC_FUNDCODE)
        if (index !== -1) {
          this.selectListDialog.splice(index, 1)
        }
      }

      if (this.limit !== -1) {
        this.selectProductStr = `(${this.selectListDialog.length}/${this.limit})`
      }
    },
    handleDialogClose() {
      this.productSelectDialogVisible = false
      this.$emit('closedialog')
    }
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-table--striped .el-table__body tr.el-table__row--striped td {
  background-color: #f9fafe !important;
}

::v-deep .el-table tbody .el-table__row:hover > td {
  background-color: transparent !important;
}

::v-deep .el-table tbody .el-table__row.el-table__row--striped:hover > td {
  background-color: #f9fafe !important;
}

// 隐藏全选框
::v-deep .el-table__header-wrapper .el-checkbox {
  display: none;
}

::v-deep .el-dialog {
  width: 85% !important;
}

::v-deep .el-tree-node__expand-icon.is-leaf {
  display: block !important;
}

::v-deep .el-form {
  width: 100% !important;
}

.left-title-bg {
  line-height: 46px;
  background: #fafafa;

  span {
    margin-left: 5px;
  }
}

.right-title-bg {
  line-height: 46px;
  background: #fafafa;
}

.center-form-bg {
  padding: 5px 5px;
  background: #fafafa;
}

.center-padding-left {
  padding-left: 5px;
  background-color: #f4f6fa;
  padding-right: 5px;
}

.center-dialog::after {
  content: '';
  clear: both;
  display: block;
  height: 0;
  visibility: hidden;
}

.center-dialog,
.right-dialog,
.left-dialog {
  height: 500px;
  overflow: auto;
  border: 1px solid #cccccc;
}

.dialog-footer-center {
  text-align: center;
}

.drag-element-style {
  text-align: left;
  line-height: 20px;
}

.drag-element-style:hover {
  cursor: pointer;
  background: #e6edfc;
  color: #4a8ce8;
}
</style>
