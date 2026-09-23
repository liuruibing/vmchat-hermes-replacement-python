<template>
  <div class="admin-org-auth-apply" v-auto-enter>
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="queryForm" :model="formInline" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item label="">
                <el-input v-model="formInline.vcOrgUserName" size="small" placeholder="申请人姓名" clearable style="width: 160px;" />
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.vcOrgName" size="small" placeholder="机构名称" clearable style="width: 180px;" />
              </el-form-item>
              <el-form-item label="">
                <el-date-picker
                  v-model="applyDateRange"
                  type="daterange"
                  size="small"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  value-format="yyyy-MM-dd"
                  style="width: 380px !important;"
                />
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.vcStatus" size="small" clearable placeholder="状态" >
                  <el-option label="待处理" value="0" />
                  <el-option label="同意" value="1" />
                  <el-option label="拒绝" value="-1" />
                </el-select>
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.nameKeyword" size="small" placeholder="管理人名称/产品代码/产品名称" clearable style="width: 260px !important;" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearch(true)">查询</el-button>
                <el-button type="primary" size="small" :loading="batchApproveLoading" :disabled="batchDisabled || anyActionLoading" @click="handleBatchApprove">批量同意</el-button>
                <el-button type="primary" size="small" plain :loading="batchRejectLoading" :disabled="batchDisabled || anyActionLoading" @click="handleBatchReject">批量拒绝</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :checkbox-config="{ checkMethod: checkSelectable }"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          resizable
          @checkbox-change="handleSelectionChange"
          @checkbox-all="handleSelectionChange"
        >
          <vxe-table-column type="checkbox" width="50" align="center" />
          <vxe-table-column field="vcOrgUserName" title="申请人" min-width="100" align="center" />
          <vxe-table-column field="vcOrgName" title="资方机构名称" min-width="140" align="center" />
          <vxe-table-column field="vcFundCode" title="产品代码" min-width="100" align="center" />
          <vxe-table-column field="vcFundName" title="产品名称" min-width="180" align="center" />
          <vxe-table-column field="vcMgrName" title="管理人名称" min-width="180" align="center" />
          <vxe-table-column field="vcApplyIntention" title="申请意向" min-width="180" align="center" />
          <vxe-table-column field="vcApplyAuthLevel" title="申请授权等级" width="180" align="center" />
          <vxe-table-column field="vcApplyFrequency" title="申请数据频率" width="110" align="center" />
          <vxe-table-column field="dApplyDatetime" title="申请授权时间" min-width="200" align="center" />
          <vxe-table-column title="状态" width="90" align="center">
            <template slot-scope="{ row }">
              <span>{{ formatStatus(row.vcStatus) }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column field="vcApproverName" title="审批人名称" min-width="100" align="center" />
          <vxe-table-column field="dUpdatetime" title="更新时间" min-width="200" align="center" />
          <vxe-table-column title="操作" width="200" align="center" fixed="right">
            <template slot-scope="{ row }">
              <span v-if="row.vcStatus === '0'">
                <el-button
                  type="info"
                  plain
                  size="small"
                  :loading="isRowApproveLoading(row.fId)"
                  :disabled="anyActionLoading && !isRowApproveLoading(row.fId)"
                  @click="rowApprove(row)"
                >
                  同意
                </el-button>
                <el-button
                  type="info"
                  plain
                  size="small"
                  :loading="isRowRejectLoading(row.fId)"
                  :disabled="anyActionLoading && !isRowRejectLoading(row.fId)"
                  @click="rowReject(row)"
                >
                  拒绝
                </el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
        <vxe-pager
          :current-page="formInline.pageNum"
          :page-size="formInline.pageSize"
          :total="total"
          :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
          :page-sizes="[10, 20, 50, 100]"
          border
          size="medium"
          class="standard-vxe-pager"
          @page-change="pagination"
        />
      </div>
    </div>
  </div>
</template>

<script>
import pageApi from './scripts/api.js'

export default {
  name: 'AdminOrgAuthApplyProcess',
  data() {
    return {
      formInline: {
        vcOrgUserName: '',
        vcOrgName: '',
        beginApplyDate: '',
        endApplyDate: '',
        vcStatus: '0',
        nameKeyword: '',
        pageNum: 1,
        pageSize: 20
      },
      applyDateRange: [],
      tableLoading: false,
      batchApproveLoading: false,
      batchRejectLoading: false,
      rowApproveLoadingIds: [],
      rowRejectLoadingIds: [],
      tableData: [],
      total: 0,
      tableHeight: 400,
      selectedRecords: []
    }
  },
  computed: {
    batchDisabled() {
      return !this.selectedRecords || this.selectedRecords.length === 0
    },
    anyActionLoading() {
      return this.batchApproveLoading ||
        this.batchRejectLoading ||
        (this.rowApproveLoadingIds && this.rowApproveLoadingIds.length > 0) ||
        (this.rowRejectLoadingIds && this.rowRejectLoadingIds.length > 0)
    }
  },
  mounted() {
    this.handleTableHeight()
    this.handleSearch(true)
  },
  methods: {
    formatStatus(status) {
      if (status === '0') return '待处理'
      if (status === '1') return '同意'
      if (status === '-1') return '拒绝'
      return status || ''
    },
    handleTableHeight() {
      this.$nextTick(() => {
        if (this.$refs.refsTable && this.$refs.refsTable.$el) {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 165
        }
        const self = this
        window.onresize = function() {
          if (self.$refs.refsTable && self.$refs.refsTable.$el) {
            self.tableHeight = window.innerHeight - self.$refs.refsTable.$el.offsetTop - 165
          }
        }
      })
    },
    syncDateRange() {
      if (this.applyDateRange && this.applyDateRange.length === 2) {
        this.formInline.beginApplyDate = this.applyDateRange[0]
        this.formInline.endApplyDate = this.applyDateRange[1]
      } else {
        this.formInline.beginApplyDate = ''
        this.formInline.endApplyDate = ''
      }
    },
    handleSearch(resetPage) {
      if (resetPage) {
        this.formInline.pageNum = 1
      }
      this.syncDateRange()
      this.tableLoading = true
      const params = Object.assign({}, this.formInline)
      pageApi.pageList(params).then((res) => {
        this.tableLoading = false
        const body = res.data || {}
        const status = body.status
        const data = body.data || {}
        if (status === 200 && data) {
          this.tableData = data.list || []
          this.total = data.total != null ? data.total : 0
          this.selectedRecords = []
        } else {
          this.tableData = []
          this.total = 0
          this.selectedRecords = []
          if (body.message) {
            this.$message.warning(body.message)
          }
        }
      }).catch(() => {
        this.tableLoading = false
      })
    },
    pagination(val) {
      this.formInline.pageNum = val.currentPage
      this.formInline.pageSize = val.pageSize
      this.handleSearch(false)
    },
    handleSelectionChange() {
      const t = this.$refs.refsTable
      if (!t || typeof t.getCheckboxRecords !== 'function') {
        this.selectedRecords = []
        return
      }
      this.selectedRecords = t.getCheckboxRecords() || []
    },
    isRowApproveLoading(fId) {
      if (fId == null) return false
      return Array.isArray(this.rowApproveLoadingIds) && this.rowApproveLoadingIds.includes(fId)
    },
    isRowRejectLoading(fId) {
      if (fId == null) return false
      return Array.isArray(this.rowRejectLoadingIds) && this.rowRejectLoadingIds.includes(fId)
    },
    checkSelectable({ row }) {
      return row.vcStatus === '0'
    },
    collectSelectedIds(rows) {
      const ids = []
      if (!rows || !rows.length) return ids
      for (let i = 0; i < rows.length; i++) {
        const r = rows[i]
        if (r && r.fId != null) ids.push(r.fId)
      }
      return ids
    },
    handleBatchApprove() {
      const rows = this.selectedRecords || []
      const ids = this.collectSelectedIds(rows)
      if (!ids.length) {
        this.$message.warning('请选择待处理记录')
        return
      }
      this.doApprove(ids, 'batch')
    },
    handleBatchReject() {
      const rows = this.selectedRecords || []
      const ids = this.collectSelectedIds(rows)
      if (!ids.length) {
        this.$message.warning('请选择待处理记录')
        return
      }
      this.doReject(ids, 'batch')
    },
    rowApprove(row) {
      if (!row || row.fId == null) return
      this.doApprove([row.fId], 'row')
    },
    rowReject(row) {
      if (!row || row.fId == null) return
      this.doReject([row.fId], 'row')
    },
    doApprove(ids, mode) {
      const self = this
      this.$confirm('确认同意所选申请并推送服务平台？', '提示', {
        type: 'warning'
      }).then(function() {
        const isBatchApprove = mode === 'batch'
        if (isBatchApprove) {
          self.batchApproveLoading = true
        } else {
          // mode === 'row'：仅让对应行“同意”按钮转圈
          self.rowApproveLoadingIds = ids.slice()
        }

        pageApi.approve(ids).then(function(res) {
          const body = res.data || {}
          if (body.status === 200) {
            self.$message.success(body.message || '操作成功')
            self.handleSearch(true)
          } else {
            self.$message.error(body.message || '操作失败')
          }
        }).catch(function() {
          self.$message.error('操作失败')
        }).finally(function() {
          self.batchApproveLoading = false
          self.rowApproveLoadingIds = []
        })
      }).catch(function() {})
    },
    doReject(ids, mode) {
      const self = this
      this.$confirm('确认拒绝所选申请？', '提示', {
        type: 'warning'
      }).then(function() {
        const isBatchReject = mode === 'batch'
        if (isBatchReject) {
          self.batchRejectLoading = true
        } else {
          // mode === 'row'：仅让对应行“拒绝”按钮转圈
          self.rowRejectLoadingIds = ids.slice()
        }

        pageApi.reject(ids).then(function(res) {
          const body = res.data || {}
          if (body.status === 200) {
            self.$message.success(body.message || '操作成功')
            self.handleSearch(true)
          } else {
            self.$message.error(body.message || '操作失败')
          }
        }).catch(function() {
          self.$message.error('操作失败')
        }).finally(function() {
          self.batchRejectLoading = false
          self.rowRejectLoadingIds = []
        })
      }).catch(function() {})
    },
    beforeDestroy() {
      window.onresize = null
    }
  }
}
</script>

<style lang="scss" scoped>
.admin-org-auth-apply {
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
}
</style>
