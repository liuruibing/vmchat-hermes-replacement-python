<template>
  <div class="apiApply-manager">
    <!-- 查询条件表单 -->
    <el-form :inline="true" :model="queryParams" class="demo-form-inline">
      <el-form-item prop="vcUseUsername">
        <el-input v-model="queryParams.vcUseUsername" placeholder="请输入姓名" size="small" clearable></el-input>
      </el-form-item>
      <el-form-item prop="vcPhone">
        <el-input v-model="queryParams.vcPhone" placeholder="请输入手机号" size="small" clearable></el-input>
      </el-form-item>
      <el-form-item prop="vcIpAddr">
        <el-input v-model="queryParams.vcIpAddr" placeholder="请输入IP地址" size="small" clearable></el-input>
      </el-form-item>
      <el-form-item prop="vcAuditorStatus">
        <el-select v-model="queryParams.vcAuditorStatus" placeholder="请选择审批状态" size="small" clearable>
          <el-option v-for="item in statusList" :key="item.dimCde" :label="item.dimNme"
            :value="item.dimCde"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="handleQuery">查询</el-button>
        <el-button type="info" icon="el-icon-refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <div style="margin-bottom: 15px;">
      <el-button type="success" icon="el-icon-check" :disabled="selection.length === 0"
        @click="handleBatchApprove">批量通过</el-button>
      <el-button type="danger" icon="el-icon-close" :disabled="selection.length === 0"
        @click="handleBatchReject">批量拒绝</el-button>
    </div>

    <!-- 数据表格 -->
    <div class="apiApplyManager-table" id="standard-table">
      <vxe-table height="auto" border auto-resize show-overflow ref="xTable" :data="tableData" :loading="loading"
        :checkbox-config="{ checkMethod: checkSelectable, strict: true }"
        @checkbox-change="checkboxChangeEvent" @checkbox-all="checkboxChangeEvent">
        <vxe-table-column type="checkbox" width="60" align="center" fixed="left"></vxe-table-column>
        <vxe-table-column field="vcReqUsername" title="申请人" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.vcReqUsername | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="fUseDeptname" title="申请人部门" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.fUseDeptname | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcUseUsername" title="成员名称" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.vcUseUsername | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcCompanyName" title="成员机构" min-width="150" align="center">
          <template slot-scope="{row}">
            {{ row.vcCompanyName | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcDeptname" title="成员部门" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.vcDeptname | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcPhone" title="成员手机号" min-width="120" align="center"></vxe-table-column>
        <vxe-table-column field="vcUseCondition" title="成员在职状态" min-width="120" align="center">
          <template #default="{ row }">
            <span v-if="row.vcUseCondition == '0'">在职</span>
            <span v-else-if="row.vcUseCondition == '1'" style="color: #F56C6C;">离职</span>
            <span v-else>-</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcStatus" title="成员账号状态" min-width="120" align="center">
          <template #default="{ row }">
            <span v-if="row.vcStatus == '0'">启用</span>
            <span v-else-if="row.vcStatus == '1'" style="color: #F56C6C;">禁用</span>
            <span v-else>-</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcDelete" title="成员是否删除" min-width="120" align="center">
          <template #default="{ row }">
            <span v-if="row.vcDelete == '0'">有效账号</span>
            <span v-else-if="row.vcDelete == '1'" style="color: #F56C6C;">已删除</span>
            <span v-else>-</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcIpAddr" title="IP地址" min-width="150" align="center">
          <template #default="{ row }">
            <div v-if="row.vcAuditorStatus === 'P'"
              style="display: flex; align-items: center; justify-content: center;">
              <span :title="row.vcIpAddr"
                style="text-overflow: ellipsis; overflow: hidden; white-space: nowrap; margin-right: 5px;">{{
                  row.vcIpAddr }}</span>
              <el-tooltip :content="'更改前IP: ' + row.vcIpAddrOld" placement="top" effect="dark">
                <i class="el-icon-info"></i>
              </el-tooltip>
            </div>
            <span v-else>{{ row.vcIpAddr }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="dReqDatetime" title="申请时间" min-width="180" align="center"></vxe-table-column>
        <vxe-table-column field="vcAuditorStatus" title="审批状态" min-width="150" align="center">
          <template #default="{ row }">
            <span :style="{ color: getStatusColor(row.vcAuditorStatus), fontWeight: 'bold' }">{{
              getStatusName(row.vcAuditorStatus) }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="操作" width="240" align="center" fixed="right">
          <template #default="{ row }">
            <span class="table-operation">
              <el-button v-if="['W', 'P'].includes(row.vcAuditorStatus)" type="info" plain size="small"
                @click="handleApprove(row)">通过</el-button>
              <el-button v-if="['W', 'P'].includes(row.vcAuditorStatus)" type="info" plain size="small"
                @click="handleReject(row)">拒绝</el-button>
              <el-button v-if="row.vcAuditorStatus === 'S'" type="info" plain size="small"
                @click="handleForceReject(row)">强制驳回</el-button>
              <el-button v-if="['F', 'PF'].includes(row.vcAuditorStatus)" type="info" plain size="small"
                @click="handleForceApprove(row)">强制通过</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <Pagination :total="total" :limit="queryParams.pageSize" :page="queryParams.pageNum" @pagination="pagination">
    </Pagination>
  </div>
</template>

<script>
import Pagination from '@/components/NewPagination'
import api from './api'

export default {
  name: 'ApiApplyManager',
  components: {
    Pagination
  },
  data() {
    return {
      queryParams: {
        vcUseUsername: '',
        vcPhone: '',
        vcIpAddr: '',
        vcAuditorStatus: '',
        pageNum: 1,
        pageSize: 20
      },
      statusList: [
        { dimCde: 'S', dimNme: '审批通过', color: '#67C23A' },
        { dimCde: 'F', dimNme: '不通过', color: '#F56C6C' },
        { dimCde: 'W', dimNme: '待审批', color: '#409EFF' },
        { dimCde: 'P', dimNme: 'IP变更待审批', color: '#409EFF' },
        { dimCde: 'PF', dimNme: 'IP变更审批不通过', color: '#F56C6C' },
        { dimCde: 'C', dimNme: '取消申请', color: '#909399' },
      ],
      loading: false,
      tableData: [],
      total: 0,
      selection: []
    }
  },
  created() {
    this.getList()
  },
  methods: {
    checkSelectable({ row }) {
      return ['W', 'P'].includes(row.vcAuditorStatus)
    },
    async getList() {
      this.loading = true
      this.selection = []
      try {
        const params = {
          vcUseUsername: this.queryParams.vcUseUsername || undefined,
          vcPhone: this.queryParams.vcPhone || undefined,
          vcIpAddr: this.queryParams.vcIpAddr || undefined,
          vcAuditorStatus: this.queryParams.vcAuditorStatus || undefined,
          pageNum: this.queryParams.pageNum,
          pageSize: this.queryParams.pageSize
        }
        const res = await api.reqPage(params)
        const { status, data } = res.data;
        if (status === 200 && data) {
          this.total = data.total || 0
          this.tableData = data.list || []
        }
      } catch (e) {
        console.error('查询列表失败', e)
      } finally {
        this.loading = false
      }
    },
    getStatusColor(status) {
      const item = this.statusList.find(x => x.dimCde === status)
      return item ? item.color : '#909399'
    },
    getStatusName(status) {
      const item = this.statusList.find(x => x.dimCde === status)
      return item ? item.dimNme : '--'
    },
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getList()
    },
    resetQuery() {
      this.queryParams = {
        vcUseUsername: '',
        vcPhone: '',
        vcIpAddr: '',
        vcAuditorStatus: '',
        pageNum: 1,
        pageSize: 20
      }
      this.getList()
    },
    pagination(val) {
      let { page, limit } = val
      this.queryParams.pageNum = page
      this.queryParams.pageSize = limit
      this.getList()
    },
    checkboxChangeEvent({ records }) {
      this.selection = records || []
    },
    async doAudit(row, targetStatus) {
      try {
        const res = await api.updateAudit({
          vcRecordIds: [row.vcRecordId],
          vcAuditorStatus: targetStatus
        })
        const { status, message } = res.data;
        if (status === 200) {
          return true
        } else {
          this.$message.error(message || '操作失败')
          return false
        }
      } catch (e) {
        console.error('审批操作失败', e)
        this.$message.error('操作失败')
        return false
      }
    },
    handleApprove(row) {
      this.$confirm('确定要通过该API申请吗？', '审批提示', {
        confirmButtonText: '通过',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const ok = await this.doAudit(row, 'S')
        if (ok) {
          this.$message.success('已审批通过')
          this.getList()
        }
      }).catch(() => { })
    },
    handleReject(row) {
      this.$confirm('确定要拒绝该申请吗？', '审批提示', {
        confirmButtonText: '拒绝',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const targetStatus = row.vcAuditorStatus === 'P' ? 'PF' : 'F'
        const ok = await this.doAudit(row, targetStatus)
        if (ok) {
          this.$message.success('已审批拒绝')
          this.getList()
        }
      }).catch(() => { })
    },
    handleForceReject(row) {
      this.$confirm('确定要强制驳回该API申请吗？', '强制驳回提示', {
        confirmButtonText: '强制驳回',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const ok = await this.doAudit(row, 'F')
        if (ok) {
          this.$message.success('已强制驳回')
          this.getList()
        }
      }).catch(() => { })
    },
    handleForceApprove(row) {
      this.$confirm('确定要强制通过该API申请吗？', '强制通过提示', {
        confirmButtonText: '强制通过',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        const ok = await this.doAudit(row, 'S')
        if (ok) {
          this.$message.success('已强制通过')
          this.getList()
        }
      }).catch(() => { })
    },
    handleBatchApprove() {
      const pendingList = this.selection.filter(item => ['W', 'P'].includes(item.vcAuditorStatus))
      if (pendingList.length === 0) {
        this.$message.warning('所选记录中没有待审批的数据')
        return
      }
      this.$confirm(`确定要批量通过选中的 ${pendingList.length} 条API申请吗？`, '批量审批提示', {
        confirmButtonText: '全部通过',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.updateAudit({
            vcRecordIds: pendingList.map(item => item.vcRecordId),
            vcAuditorStatus: 'S'
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success(message || '批量审批通过操作成功')
            this.$refs.xTable.clearCheckboxRow()
            this.selection = []
            this.getList()
          } else {
            this.$message.error(message || '操作失败')
          }
        } catch (e) {
          console.error('批量审批失败', e)
          this.$message.error('操作失败')
        }
      }).catch(() => { })
    },
    handleBatchReject() {
      const pendingList = this.selection.filter(item => ['W', 'P'].includes(item.vcAuditorStatus))
      if (pendingList.length === 0) {
        this.$message.warning('所选记录中没有待审批的数据')
        return
      }
      this.$confirm(`确定要批量拒绝选中的 ${pendingList.length} 条API申请吗？`, '批量审批提示', {
        confirmButtonText: '全部拒绝',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.updateAudit({
            vcRecordIds: pendingList.map(item => item.vcRecordId),
            vcAuditorStatus: 'F'
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success(message || '批量审批拒绝操作成功')
            this.$refs.xTable.clearCheckboxRow()
            this.selection = []
            this.getList()
          } else {
            this.$message.error(message || '操作失败')
          }
        } catch (e) {
          console.error('批量审批失败', e)
          this.$message.error('操作失败')
        }
      }).catch(() => { })
    }
  }
}
</script>

<style lang="scss" scoped>
.apiApply-manager {
  height: 100%;
  padding: 12px 10px;

  .apiApplyManager-table {
    height: calc(100% - 170px);
  }
}
</style>
