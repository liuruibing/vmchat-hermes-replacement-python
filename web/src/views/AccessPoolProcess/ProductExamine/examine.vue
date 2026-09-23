<template>
  <div class="examine">
    <!-- <div class="title-style">提交/审批列表</div> -->
    <div id="standard-table">
      <vxe-table
        ref="refsTable"
        :cell-style="{ height: '50px' }"
        :data="tableData"
        :height="tableHeight"
        auto-resize
        stripe=""
        show-overflow="tooltip"
        style="width: 100%"
        sync-resize
      >
        <vxe-table-column label="序号" type="index" align="center" width="50"></vxe-table-column>
        <vxe-table-column v-for="(col, i) in tableColumns" :key="i" :align="col.align" :label="col.label" :field="col.prop" :width="col.width" header-align="center" stripe>
          <template slot-scope="scope">
            <span v-if="col.prop == 'fileName'" style="position: relative">
              <el-link :underline="false" type="primary" @click="downloadFile(scope.row)">
                {{ scope.row[col.prop] }}
              </el-link>
              <i
                v-if="['0', '5'].includes(currentFund.status)"
                class="el-icon-close"
                style="color: #409eff; cursor: pointer; position: absolute; right: -17px; top: 6px; font-size: 14px"
                @click="deleteFile(scope.row)"
              ></i>
            </span>
            <span v-else>{{ scope.row[col.prop] | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column align="center" header-align="center" label="操作" width="300">
          <template slot-scope="scope">
            <span class="table-operation">
              <el-button
                v-btn="'examinenote'"
                v-if="row && (row.status == '1' || row.status == '0' || row.status == '5' || row.status == '4')"
                :underline="false"
                size="small"
                type="info"
                plain
                @click="handleAddExplain(scope.row)"
              >
                补充说明
              </el-button>
              <el-button
                v-btn="'examinecomment'"
                v-if="row && (row.status == '1' || row.status == '4')"
                :underline="false"
                size="small"
                type="info"
                plain
                @click="handleAddOpinion(scope.row)"
              >
                审批意见
              </el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <el-row type="flex" align="middle" justify="space-between">
      <span class="standard-form">
        <el-button
          v-btn="'examineupload'"
          v-if="row && (row.status == '0' || row.status == '5' || row.status == '1' || row.status == '4')"
          size="small"
          type="info"
          plain
          @click="handleUpload"
        >
          准入材料上传
        </el-button>
        <el-button
          plain
          v-btn="'examinesubmit'"
          v-if="row && (row.status == '0' || row.status == '5' || row.status == '1' || row.status == '4')"
          size="small"
          type="info"
          @click="handleSubmit"
        >
          提交
        </el-button>
        <el-button plain v-btn="'examineapprove'" v-if="row && (row.status == '1' || row.status == '4')" size="small" type="info" @click="handleExamine">审批</el-button>
      </span>
      <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="total" @pagination="pagination" />
    </el-row>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      :visible.sync="examineDialog"
      custom-class="saveAsDialog"
      title="审批"
      @close="closeExamine"
    >
      <examine-dialog :current-fund="currentFund" @closeExamine="closeExamine"></examine-dialog>
    </el-dialog>
    <el-dialog
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :destroy-on-close="true"
      :visible.sync="uploadDialog"
      custom-class="saveAsDialog"
      title="准入材料上传"
      @close="closeUpload"
    >
      <file-upload-dialog :current-fund="currentFund" @closeUpload="closeUpload"></file-upload-dialog>
    </el-dialog>
  </div>
</template>

<script>
import { EXAMINE_TABLE_COLUMNS } from './scripts/constant'
import ExamineDialog from './components/examineDialog.vue'
import FileUploadDialog from './components/fileUpload.vue'
import Pagination from '@/components/Pagination'
import { deleteFile, getSubmitAll, saveNote, saveRemark, submitExamine } from './scripts/api'
import commonFun from '@/filters/new_common'

export default {
  name: 'Examine',
  components: {
    ExamineDialog,
    FileUploadDialog,
    Pagination
  },
  data() {
    return {
      row: null,
      tableColumns: EXAMINE_TABLE_COLUMNS,
      tableData: [],
      examineDialog: false,
      uploadDialog: false,
      formQuery: {
        pageSize: 20,
        pageNum: 1
      },
      total: 0,
      currentFund: {},
      tableHeight: 0
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initData()
      this.handleTableHeight()
    })
  },
  activated() {
    if (this.$store.getters.fromPageJump) {
      this.$store.commit('SET_FROMPAGEJUMP', false)
      if (this.$route.query) {
        this.row = this.$route.query
      }
    }
  },
  methods: {
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 200
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 200
        }
      })
    },
    initData() {
      this.currentFund = this.$route.query || {}
      // 动态修改tag-views dom标签
      document.querySelector('.tags-view-item.active .tag-title') &&
        (document.querySelector('.tags-view-item.active .tag-title').innerText = this.currentFund.fundName || '提交/审批')
      this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
    },
    async querySubmitList(fundCode, fid) {
      const data = {
        fundCode,
        fid,
        limit: this.formQuery.pageSize,
        offset: (this.formQuery.pageNum - 1) * this.formQuery.pageSize
      }
      try {
        const res = await getSubmitAll(data)
        this.tableData = res.data.rows || []
        this.total = res.data.total || 0
      } catch (e) {
        this.tableData = []
        this.total = 0
      }
    },
    handleSubmit() {
      if (this.row && this.row.status == '4') {
        this.$message.closeAll()
        this.$message({
          type: 'warning',
          message: '产品已准入勿重复提交',
          customClass: 'message-warning'
        })
        return
      }
      this.$alert('是否就当前材料提交审批？', '提交', {
        confirmButtonText: '确定',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel',
        callback: async (action) => {
          if (action === 'cancel') return
          const data = {
            fid: this.currentFund.fid || ''
          }
          try {
            const res = await submitExamine(data)
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: res.data.message || '提交成功',
                customClass: 'message-success'
              })
              this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
            } else if (res.data.status === -2) {
              this.$message({
                type: 'warning',
                message: res.data.message || '已提交，勿重复提交。',
                customClass: 'message-warning'
              })
            } else if (res.data.status === -3) {
              this.$message({
                type: 'warning',
                message: res.data.message || '产品已准入勿重复提交。',
                customClass: 'message-warning'
              })
            }
          } catch (e) {
            this.$message({
              type: 'error',
              message: '提交失败',
              customClass: 'message-error'
            })
          }
        }
      })
    },
    async deleteFile(row) {
      const data = {
        id: row.id || ''
      }

      this.$confirm('是否删除该条准入材料？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          deleteFile(data)
            .then((res) => {
              if (res.data.status === 0) {
                this.$message({
                  type: 'success',
                  message: res.data.message || '删除成功',
                  customClass: 'message-success'
                })
                this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
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
    handleAddExplain(row) {
      this.$prompt('材料补充说明：', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: row.note || '',
        customClass: 'standard-confirm-input',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(({ value }) => {
          if (value === null) {
            this.$message({
              type: 'error',
              message: '输入值不能为空，请重新输入',
              customClass: 'message-error'
            })
          } else {
            const data = {
              id: row.id || '',
              note: value.replace(/\s+/g, '')
            }
            saveNote(data).then((res) => {
              console.log(res)
              this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          })
        })
    },
    handleAddOpinion(row) {
      this.$prompt('审批意见：', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        inputValue: row.remark || '',
        customClass: 'standard-confirm-input',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(({ value }) => {
          if (value === null) {
            this.$message({
              type: 'error',
              message: '输入值不能为空，请重新输入',
              customClass: 'message-error'
            })
          } else {
            const data = {
              id: row.id || '',
              remark: value.replace(/\s+/g, '')
            }
            saveRemark(data).then((res) => {
              console.log(res)
              this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
            })
          }
        })
        .catch(() => {
          this.$message({
            type: 'info',
            message: '取消输入'
          })
        })
    },
    downloadFile(row) {
      const data = {
        id: row.id || '',
        token: this.$store.getters.token
      }
      const action = this.$store.state.setting.baseApi + `/api/fundAccess/approve/download`
      commonFun.formDownloadFile(data, action, 'POST')
    },
    handleExamine() {
      this.examineDialog = true
    },
    handleUpload() {
      this.uploadDialog = true
    },
    closeExamine(status) {
      this.examineDialog = false
      if (status === 'refesh') {
        this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
      }
    },
    closeUpload(status) {
      this.uploadDialog = false
      if (status === 'refesh') {
        this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
      }
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.querySubmitList(this.currentFund.fundCode, this.currentFund.fid)
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>
,
<style lang="scss" scoped>
.examine {
  padding: 10px;
}
@import './styles/index';
::v-deep .vxe-body--row.row--stripe {
  background-color: #f9fafe !important;
}
::v-deep .el-table .el-table__row--striped {
  background-color: #f9fafe !important;
}
::v-deep .saveAsDialog.el-dialog .el-dialog__title {
  color: #0F65DD !important;
}
</style>
