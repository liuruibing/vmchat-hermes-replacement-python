<template>
  <div class="DdPosition ddportal-ui">
    <el-form ref="formInline"  :inline="true" :model="formInline" style="margin-bottom: 8px" class="standard-form demo-form-inline form_inline_search">
      <el-row>
        <el-col :span="16">
          <div style="width: 100%">
            <el-form-item label="机构编码" prop="companyCode">
              <el-input v-model="formInline.companyCode" clearable size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
            <el-form-item label="机构名称" prop="companyName">
              <el-input v-model="formInline.companyName" clearable size="small" placeholder="请输入内容"></el-input>
            </el-form-item>
          </div>
        </el-col>
        <el-col :span="8">
          <el-form-item class="search_button_com">
            <el-button type="primary" style="margin-bottom: 5px" size="small" @click="onSubmit('formInline', true)">
              <i class="el-icon-search"></i>
              查询
            </el-button>
            <el-button type="info" plain style="margin-bottom: 5px" size="small" @click="restForm()">
              <i class="el-icon-delete"></i>
              重置
            </el-button>
            <el-button type="primary" plain style="margin-bottom: 5px" size="small" @click="addData()">
              <i class="el-icon-circle-plus-outline"></i>
              添加
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <el-table
      v-loading="tableLoading"
      ref="eleTable"
      :data="tableData"
      id="standard-table"
      :cell-style="{ height: '40px', fontSize: '14px' }"
      :header-cell-style="{ color: '#333', height: '60px', fontSize: '14px' }"
      stripe
      style="width: 100%"
      max-height="500px"
    >
      <el-table-column prop="companyCode" show-overflow-tooltip label="机构编码" min-width="100" algin="center" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyCode | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="companyName" show-overflow-tooltip label="机构名称" min-width="100" algin="center" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyName | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="companyDesc" show-overflow-tooltip label="描述" min-width="70" algin="center" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyDesc | noDataFilter }}</span>
        </template>
      </el-table-column>
      <el-table-column prop="companyRemark" show-overflow-tooltip label="备注" min-width="70" algin="center" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.companyRemark | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column prop="updateTime" show-overflow-tooltip label="更新时间" min-width="70" algin="center" header-align="center">
        <template slot-scope="scope">
          <span>{{ scope.row.updateTime | noDataFilter }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="380" align="center">
        <template slot-scope="scope">
          <div class="dialog-footer standard-form">
            <el-button type="info" plain size="small" @click="editData(scope.row)">编辑</el-button>
            <el-button type="info" plain size="small" @click="delData(scope.row)" :loading="deleteSubmitLoading">删除</el-button>
            <el-button type="info" plain size="small" @click="handleDepartMentClick(scope.row)">部门管理</el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>

    <Pagination :total="total" :page="formInline.pageNum" :limit="formInline.pageSize" @pagination="pagination"></Pagination>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      :visible.sync="institutionDialogVisible"
      :title="dialogTitle"
      @close="
        () => {
          this.institutionDialogVisible = false
        }
      "
    >
      <el-row type="flex" justify="center">
        <el-form label-position="right" label-width="100px" :model="formDialog">
          <el-form-item label="机构编码" prop="companyCode">
            <el-input v-model="formDialog.companyCode" style="width: 100%" :disabled="dialogTitle === '机构编辑'"></el-input>
          </el-form-item>
          <el-form-item label="机构名称" prop="companyName">
            <el-input v-model="formDialog.companyName"></el-input>
          </el-form-item>
          <el-form-item label="描述" prop="companyDesc">
            <el-input v-model="formDialog.companyDesc" type="textarea" placeholder="请输入内容" maxlength="30" show-word-limit rows="4"></el-input>
          </el-form-item>
          <el-form-item label="备注" prop="companyRemark">
            <el-input v-model="formDialog.companyRemark" type="textarea" placeholder="请输入内容" maxlength="30" show-word-limit rows="4"></el-input>
          </el-form-item>
        </el-form>
      </el-row>
      <template slot="footer">
        <el-row style="text-align: center">
          <el-button type="primary" size="small" @click="handleDialogSave" :loading="dialogSubmitLoading">提 交</el-button>
          <el-button
            type="info"
            plain
            size="small"
            @click="
              () => {
                this.institutionDialogVisible = false
              }
            "
          >
            取 消
          </el-button>
        </el-row>
      </template>
    </el-dialog>
    <el-drawer title="" v-if="departmentVisible" :visible.sync="departmentVisible" :append-to-body="true" direction="rtl" size="100%">
      <dd-dept-backup :current-row="currentRow"></dd-dept-backup>
    </el-drawer>
  </div>
</template>

<script>
import Pagination from '@/components/Pagination'
import pageApi from '@/api/ddportal/deptSelf.js'
import ddDeptBackup from './ddDeptBackup'
export default {
  name: 'DdDept',
  components: { Pagination, ddDeptBackup },
  data() {
    return {
      // 部门管理
      departmentVisible: false,

      // 机构编辑
      institutionDialogVisible: false,
      dialogTitle: '',
      dialogSubmitLoading: false,

      deleteSubmitLoading: false,

      tableData: [],
      tableLoading: false,
      formInline: {
        companyCode: '',
        companyName: '',
        orderString: 'updateTime desc',
        pageNum: 1,
        pageSize: 10
      },
      formDialog: {
        companyCode: '',
        companyName: '',
        companyDesc: '',
        companyId: '',
        companyRemark: ''
      },
      currentRow: null,
      total: 0
    }
  },
  mounted() {
    this.onSubmit(true)
  },
  methods: {
    handleDepartMentClick(row) {
      this.currentRow = row
      this.departmentVisible = true
    },
    pagination(val) {
      this.formInline.pageSize = val.limit //页面条数
      this.formInline.pageNum = val.page //页面
      this.onSubmit(false)
    },
    onSubmit(flag) {
      if (flag) {
        this.formInline.pageNum = 1
      }
      const params = {
        limit: this.formInline.pageSize,
        offset: (this.formInline.pageNum - 1) * this.formInline.pageSize,
        ...this.formInline
      }
      this.tableLoading = true
      pageApi
        .getInstitutionList(params)
        .then(res => {
          this.tableLoading = false
          const { status, data } = res.data
          if (status == 200) {
            this.tableData = data.list
            this.total = data.total

            // this.tableData = data.list
            // this.total = data.total
          } else {
            this.tableData = []
            this.total = 0
          }
        })
        .catch(err => {
          this.total = 0
          this.tableData = []
          this.tableLoading = false
        })
    },
    restForm() {
      this.formInline.companyCode = ''
      this.formInline.companyName = ''
    },
    addData() {
      this.formDialog.companyId = ''
      this.formDialog.companyName = ''
      this.formDialog.companyDesc = ''
      this.formDialog.companyCode = ''
      this.formDialog.companyRemark = ''
      this.dialogTitle = '机构新增'
      this.institutionDialogVisible = true
    },
    editData(row) {
      this.$nextTick(() => {
        this.formDialog.companyDesc = row.companyDesc
        this.formDialog.companyName = row.companyName
        this.formDialog.companyCode = row.companyCode
        this.formDialog.companyId = row.companyId
        this.formDialog.companyRemark = row.companyRemark
        this.dialogTitle = '机构编辑'
      })
      this.institutionDialogVisible = true
    },
    /**
     * @Description: 编辑/新增保存
     * @author Liu Rui Bing
     * @date 2023/10/16
     */
    handleDialogSave() {
      if (this.dialogTitle == '机构编辑') {
        let params = Object.assign({}, this.formDialog)
        this.dialogSubmitLoading = true
        pageApi
          .updateInstitution(params)
          .then(res => {
            this.dialogSubmitLoading = false
            let { status } = res.data
            if (status == 200) {
              this.$message.closeAll()
              this.$message.success('机构信息更新成功')
              this.institutionDialogVisible = false
              this.$nextTick(() => {
                this.onSubmit(false)
              })
            } else {
              this.$message.closeAll()
              this.$message.warning('机构信息更新失败')
            }
          })
          .catch(err => {
            this.dialogSubmitLoading = false
            this.$message.closeAll()
            this.$message.warning('机构信息更新失败')
          })
      } else {
        let params = Object.assign({}, this.formDialog)
        delete params.companyId
        this.dialogSubmitLoading = true
        pageApi
          .insertInstitution(params)
          .then(res => {
            this.dialogSubmitLoading = false
            let { status } = res.data
            if (status == 200) {
              this.$message.closeAll()
              this.$message.success('机构信息新增成功')
              this.institutionDialogVisible = false
              this.$nextTick(() => {
                this.onSubmit(true)
              })
            } else {
              this.$message.closeAll()
              this.$message.warning('机构信息新增失败')
            }
          })
          .catch(err => {
            this.dialogSubmitLoading = false
            this.$message.closeAll()
            this.$message.warning('机构信息新增失败')
          })
      }
    },

    delData(row) {
      let params = { companyId: row.companyId }
      this.deleteSubmitLoading = true
      pageApi
        .deletetInstitution(params)
        .then(res => {
          this.deleteSubmitLoading = false
          let { status } = res.data
          if (status == 200) {
            this.$message.closeAll()
            this.$message.success('删除成功')
            this.onSubmit(false)
          } else {
            this.$message.closeAll()
            this.$message.warning('删除失败')
          }
        })
        .catch(err => {
          this.deleteSubmitLoading = false
          this.$message.closeAll()
          this.$message.warning('删除失败')
        })
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-button.el-button--info {
  background-color: #fff;
  color: #612d10;
}
::v-deep .el-table .el-table__body tr > td {
    background-color: transparent!important; /* 例如，设置为浅灰色 */
}
</style>
