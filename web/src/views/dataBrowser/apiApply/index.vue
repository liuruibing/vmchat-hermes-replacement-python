<template>
  <div class="apiApply-container">
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
        <el-button type="primary" icon="el-icon-plus" @click="handleApply">发起申请</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <div class="apiApply-table" id="standard-table">
      <vxe-table height="auto" border show-overflow auto-resize :data="tableData" :loading="loading">
        <vxe-table-column field="vcUseUsername" title="姓名" min-width="120" align="center" fixed="left"></vxe-table-column>
        <vxe-table-column field="vcPhone" title="手机号" min-width="150" align="center">
          <template slot-scope="{row}">
            {{ row.vcPhone | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcCompanyName" title="成员机构" min-width="150" align="center">
          <template slot-scope="{row}">
            {{ row.vcCompanyName | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcDeptname" title="成员部门" min-width="150" align="center">
          <template slot-scope="{row}">
            {{ row.vcDeptname | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcIpAddr" title="IP地址" min-width="150" align="center">
          <template slot-scope="{row}">
            {{ row.vcIpAddr | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcAuditorStatus" title="审批状态" min-width="120" align="center">
          <template #default="{ row }">
            <span :style="{ color: getStatusColor(row.vcAuditorStatus), fontWeight: 'bold' }">{{
              getStatusName(row.vcAuditorStatus) }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcAuditorUsername" title="审批人" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.vcAuditorUsername | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcToken" title="Token" min-width="120" align="center">
          <template slot-scope="{row}">
            {{ row.vcToken | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="dReqDatetime" title="操作时间" min-width="180" align="center">
          <template slot-scope="{row}">
            {{ row.dReqDatetime | noDataFilter }}
          </template>
        </vxe-table-column>
        <vxe-table-column title="操作" width="600" align="center" fixed="right">
          <template #default="{ row }">
            <span class="table-operation">
              <el-button type="info" plain size="small" :disabled="row.vcAuditorStatus != 'C'" @click="deleteRow(row)">删除</el-button>
              <el-button type="info" plain size="small" :disabled="row.vcAuditorStatus == 'C'" @click="cancelApply(row)">取消申请</el-button>
              <el-button type="info" plain size="small" :disabled="row.vcAuditorStatus != 'S'" @click="ipChangeApply(row)">IP变更申请</el-button>
              <el-button type="info" plain size="small" :disabled="row.vcAuditorStatus != 'S'" @click="tokenUpdate(row)">更新Token</el-button>
              <el-button type="info" plain size="small" :disabled="row.vcAuditorStatus != 'S'" @click="tokenLogout(row)">注销Token</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>
    <Pagination :total="total" :limit="queryParams.pageSize" :page="queryParams.pageNum" @pagination="pagination">
    </Pagination>

    <!-- 发起申请弹窗 -->
    <el-dialog title="发起申请" :visible.sync="dialogVisible" width="60% !important" :close-on-click-modal="false"
      @close="handleClose">
      <div style="margin-bottom: 15px;">
        <el-button type="info" size="small" icon="el-icon-plus" @click="insertEvent">新增一行</el-button>
      </div>

      <vxe-table border ref="xTable" show-overflow keep-source auto-resize :data="applyData">
        <vxe-table-column type="seq" width="60" align="center"></vxe-table-column>
        <vxe-table-column field="vcUseUsername" title="姓名">
          <template #default="{ row }">
            <el-select v-model="row.vcUseUsername" placeholder="请选择姓名" filterable style="width: 100%"
              @change="handleNameChange(row)">
              <el-option v-for="item in nameOptions" :key="item.userId" :label="item.userName" :value="item.userName"
                :disabled="isNameDisabled(item.userName, row.vcUseUsername)"></el-option>
            </el-select>
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcPhone" title="手机号"></vxe-table-column>
        <vxe-table-column field="vcCompanyName" title="机构"></vxe-table-column>
        <vxe-table-column field="vcDeptname" title="部门"></vxe-table-column>
        <vxe-table-column field="vcIpAddr" title="IP地址">
          <template #default="{ row }">
            <el-input v-model="row.vcIpAddr" placeholder="请输入IP地址" style="width: 100%"></el-input>
          </template>
        </vxe-table-column>
        <vxe-table-column title="操作" width="100" align="center">
          <template slot-scope="scope">
            <el-button type="text" style="color: #f56c6c;" @click="removeEvent(scope.row)">删除</el-button>
          </template>
        </vxe-table-column>
      </vxe-table>

      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitApply">提 交</el-button>
      </span>
    </el-dialog>

    <!-- IP变更申请弹窗 -->
    <el-dialog title="IP变更申请" :visible.sync="ipDialogVisible" width="40% !important" :close-on-click-modal="false"
      @close="handleIpDialogClose">
      <el-form ref="ipForm" :model="ipForm" :rules="ipFormRules" label-width="100px">
        <el-form-item label="姓名" prop="vcUseUsername">
          <el-input v-model="ipForm.vcUseUsername" disabled></el-input>
        </el-form-item>
        <el-form-item label="手机号" prop="vcPhone">
          <el-input v-model="ipForm.vcPhone" disabled></el-input>
        </el-form-item>
        <el-form-item label="机构" prop="vcCompanyName">
          <el-input v-model="ipForm.vcCompanyName" disabled></el-input>
        </el-form-item>
        <el-form-item label="部门" prop="vcDeptname">
          <el-input v-model="ipForm.vcDeptname" disabled></el-input>
        </el-form-item>
        <el-form-item label="IP地址" prop="vcIpAddr">
          <el-input v-model="ipForm.vcIpAddr" type="textarea" :rows="3" placeholder="请输入IP地址(多IP用|隔开)"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="ipDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitIpChange">提 交</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import Pagination from '@/components/NewPagination'
import api from './api'

export default {
  name: 'ApiApply',
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

      dialogVisible: false,
      applyData: [],
      ipDialogVisible: false,
      ipForm: {
        vcRecordId: '',
        vcUseUsername: '',
        vcPhone: '',
        vcCompanyName: '',
        vcDeptname: '',
        vcIpAddr: '',
        originalIp: ''
      },
      ipFormRules: {
        vcIpAddr: [
          { required: true, message: 'IP地址不能为空', trigger: 'blur' },
          {
            validator: (rule, value, callback) => {
              if (!value) {
                return callback()
              }
              const ipRegex = /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?:\/(?:\d|[1-2]\d|3[0-2]))?$/
              const ipParts = value.split('|')
              const isIpValid = ipParts.every(ip => ipRegex.test(ip.trim()))
              if (!isIpValid) {
                callback(new Error('IP地址格式不正确'))
              } else {
                callback()
              }
            },
            trigger: 'blur'
          }
        ]
      },

      nameOptions: []
    }
  },
  created() {
    this.getList()
    this.fetchUserList()
  },
  methods: {
    async fetchUserList() {
      try {
        const res = await api.listUser()
        const { status, data } = res.data;
        if (status === 200 && data) {
          this.nameOptions = data || []
        }
      } catch (e) {
        console.error('获取用户列表失败', e)
      }
    },
    async getList() {
      this.loading = true
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
    handleApply() {
      this.dialogVisible = true
      this.applyData = []
      this.$nextTick(() => {
        this.insertEvent()
      })
    },
    isNameDisabled(name, currentName) {
      if (!name) return false
      if (name === currentName) return false
      const tableData = this.$refs.xTable ? this.$refs.xTable.getTableData().tableData : []
      return tableData.some(item => item.vcUseUsername === name)
    },
    handleNameChange(row) {
      const selected = this.nameOptions.find(item => item.userName === row.vcUseUsername)
      if (selected) {
        this.$set(row, 'vcPhone', selected.phone)
        this.$set(row, 'vcUseUserid', selected.userId)
        this.$set(row, 'fDeptid', selected.deptId)
        this.$set(row, 'vcDeptname', selected.deptName)
        this.$set(row, 'fCompanyid', selected.companyId)
        this.$set(row, 'vcCompanyName', selected.companyName)
      } else {
        this.$set(row, 'vcPhone', '')
        this.$set(row, 'vcUseUserid', '')
        this.$set(row, 'fDeptid', '')
        this.$set(row, 'vcDeptname', '')
        this.$set(row, 'fCompanyid', '')
        this.$set(row, 'vcCompanyName', '')
      }
      if (this.$refs.xTable) {
        this.$refs.xTable.updateStatus(row)
        this.$refs.xTable.reloadRow(row, null, 'vcPhone')
        this.$refs.xTable.reloadRow(row, null, 'vcDeptname')
      }
      this.$forceUpdate()
    },
    handleClose() {
      if (this.$refs.xTable) {
        this.$refs.xTable.clearData()
      }
    },
    async insertEvent() {
      const $table = this.$refs.xTable
      if ($table) {
        const record = {
          vcUseUsername: '',
          vcPhone: '',
          vcDeptname: '',
          vcIpAddr: '',
          vcUseUserid: '',
          fDeptid: '',
          fCompanyid: '',
          vcCompanyName: ''
        }
        const { row: newRow } = await $table.insertAt(record, -1)
        await $table.setActiveRow(newRow)
      }
    },
    removeEvent(row) {
      if (this.$refs.xTable) {
        this.$refs.xTable.remove(row)
      }
    },
    async submitApply() {
      const $table = this.$refs.xTable
      const { tableData } = $table.getTableData()

      if (!tableData || tableData.length === 0) {
        this.$message.warning('请至少添加一条申请记录')
        return
      }

      const ipRegex = /^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)(?:\/(?:\d|[1-2]\d|3[0-2]))?$/

      for (let i = 0; i < tableData.length; i++) {
        const item = tableData[i]
        if (!item.vcUseUsername || !item.vcIpAddr) {
          this.$message.warning(`第 ${i + 1} 行数据未填写完整，请补充。`)
          return
        }
        const ipParts = item.vcIpAddr.split('|')
        const isIpValid = ipParts.every(ip => ipRegex.test(ip.trim()))
        if (!isIpValid) {
          this.$message.warning(`第 ${i + 1} 行的IP地址格式不正确，支持如 127.0.0.1、127.0.0.1/20 或用 "|" 拼接多个IP`)
          return
        }
      }

      try {
        const paramsArray = tableData.map(item => ({
          vcUseUserid: item.vcUseUserid,
          vcUseUsername: item.vcUseUsername,
          vcPhone: item.vcPhone,
          vcIpAddr: item.vcIpAddr,
          // fUseDeptid: item.fDeptid,
          // fUseDeptname: item.vcDeptname,
          fCompanyid: item.fCompanyid,
          vcCompanyName: item.vcCompanyName,
          fDeptid: item.fDeptid,
          vcDeptname: item.vcDeptname,
          vcAuditorStatus: 'W'
        }))

        const res = await api.reqInsertBatch(paramsArray)
        const { status, message } = res.data;
        if (status === 200) {
          this.$message.success('申请提交成功')
          this.dialogVisible = false
          this.getList()
        } else {
          this.$message.error(message || '提交失败')
        }
      } catch (e) {
        console.error('提交申请失败', e)
        this.$message.error('提交失败')
      }
    },
    deleteRow(row) {
      this.$confirm('确定要删除该申请吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.reqDelete({
            vcRecordId: row.vcRecordId
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success('删除成功')
            this.getList()
          } else {
            this.$message.error(message || '删除失败')
          }
        } catch (e) {
          console.error('删除失败', e)
          this.$message.error('删除失败')
        }
      }).catch(() => {
        this.$message.info('已取消删除')
      })
    },
    cancelApply(row) {
      this.$confirm('确定要取消该申请吗?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.reqUpdate({
            vcRecordId: row.vcRecordId,
            vcAuditorStatus: 'C'
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success('申请已取消')
            this.getList()
          } else {
            this.$message.error(message || '操作失败')
          }
        } catch (e) {
          console.error('取消申请失败', e)
          this.$message.error('操作失败')
        }
      }).catch(() => {
        this.$message.info('已取消操作')
      })
    },
    ipChangeApply(row) {
      this.ipForm = {
        vcRecordId: row.vcRecordId,
        vcUseUsername: row.vcUseUsername,
        vcPhone: row.vcPhone,
        vcCompanyName: row.vcCompanyName,
        vcDeptname: row.vcDeptname,
        vcIpAddr: row.vcIpAddr,
        originalIp: row.vcIpAddr
      }
      this.ipDialogVisible = true
    },
    handleIpDialogClose() {
      for (let key in this.ipForm) {
        this.ipForm[key] = ''
      }
    },
    submitIpChange() {
      this.$refs.ipForm.validate(async (valid) => {
        if (!valid) {
          return
        }

        if (this.ipForm.vcIpAddr === this.ipForm.originalIp) {
          this.$message.warning('IP地址未发生更改，请修改后再提交')
          return
        }

        try {
          const res = await api.reqUpdate({
            vcRecordId: this.ipForm.vcRecordId,
            vcAuditorStatus: 'P',
            vcIpAddr: this.ipForm.vcIpAddr,
            vcIpAddrOld: this.ipForm.originalIp
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success('IP变更申请提交成功')
            this.ipDialogVisible = false
            this.getList()
          } else {
            this.$message.error(message || '提交失败')
          }
        } catch (e) {
          console.error('IP变更申请失败', e)
          this.$message.error('提交失败')
        }
      })
    },
    tokenUpdate(row) {
      this.$confirm('Token更新后，原先的Token将无法再继续使用，需要更换为新的Token。是否确定更新？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.freshToken({
            vcRecordId: row.vcRecordId
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success('更新成功')
            this.getList()
          } else {
            this.$message.error(message || '更新失败')
          }
        } catch (e) {
          console.error('更新Token失败', e)
          this.$message.error('操作失败')
        }
      }).catch(() => { })
    },
    tokenLogout(row) {
      this.$confirm('Token注销后，原先的Token将无法再继续使用。是否确定注销？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.cancelToken({
            vcRecordId: row.vcRecordId
          })
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success('注销成功')
            this.getList()
          } else {
            this.$message.error(message || '注销失败')
          }
        } catch (e) {
          console.error('注销Token失败', e)
          this.$message.error('操作失败')
        }
      }).catch(() => { })
    }
  }
}
</script>

<style lang="scss" scoped>
.apiApply-container {
  height: 100%;
  padding: 12px 10px;

  .apiApply-table {
    height: calc(100% - 110px);
  }
}
</style>
