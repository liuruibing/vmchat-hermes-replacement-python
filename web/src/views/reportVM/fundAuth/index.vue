<template>
  <div class="manager-auth">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :model="formQuery" inline class="standard-form">
          <el-form-item label="">
            <el-input v-model="formQuery.indexName" placeholder="指标名称" size="small"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button size="small" type="primary" @click="onQuery(true)" icon="el-icon-search">查询</el-button>
            <el-button size="small" plain type="info" @click="reset" icon="el-icon-refresh-left">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
    <div id="standard-table" class="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          v-loading="tableLoading"
          ref="vxetable"
          :cell-style="{ height: '50px' }"
          :checkbox-config="{ checkStrictly: true }"
          :data="tableData"
          :height="tableHeight"
          :sort-config="{ remote: true, defaultSort: { field: 'm1_return', order: 'desc' } }"
          border="inner"
          auto-resize
          stripe=""
          show-overflow="tooltip"
          style="width: 100%"
          sync-resize
        >
          <vxe-table-column
            v-for="item in tableColumns"
            :key="item.id"
            :align="item.align"
            :field="item.id"
            :min-width="item.width"
            :show-overflow-tooltip="item.noshowoverflowtooltip"
            :sortable="item.sortable"
            :title="item.label"
            header-align="center"
          >
            <template slot-scope="scope">
              <span v-if="item.filter === 'fVmType-filter'">{{ scope.row[item.id] | fVmTypeToStr }}</span>
              <span v-else>{{ scope.row[item.id] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column align="center" fixed="right" title="操作" width="260px">
            <template slot-scope="scope">
              <span class="operate-btn table-operation">
                <el-button type="info" plain size="small" @click="fundAuth(scope.row)">机构授权</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </div>
    <Pagination :limit="formQuery.pageSize" :page="formQuery.pageNum" :total="formQuery.total" @pagination="pagination" />
    <el-dialog title="复制权限" center :visible.sync="copyDialogVisible" :close-on-click-modal="false">
      <vxe-table
        v-loading="dialogTableLoading"
        ref="dialogTableRef"
        :cell-style="{ height: '40px' }"
        :checkbox-config="{ checkStrictly: true }"
        :data="dialogTable"
        :header-cell-style="{ color: '#333', height: '60px', background: '#fff', fontFamily: 'Microsoft Yahei' }"
        max-height="250px"
        border="inner"
        auto-resize
        show-overflow="tooltip"
        sync-resize
      >
        <vxe-table-column type="checkbox" width="60"></vxe-table-column>
        <vxe-table-column align="center" header-align="center" min-width="100px" prop="deptId" title="机构编码"></vxe-table-column>
        <vxe-table-column align="center" header-align="center" min-width="100px" prop="deptName" title="机构名称"></vxe-table-column>
      </vxe-table>
      <div slot="footer" class="dialog-footer">
        <el-button size="small" @click="copyDialogVisible = false">取 消</el-button>
        <el-button type="primary" size="small" @click="handleCopySubmit" :loading="dialogBtnLoading">确 定</el-button>
      </div>
    </el-dialog>

    <el-dialog :title="fundDialogTitle" center width="1100px !important" :visible.sync="fundDialogVisible" :close-on-click-modal="false">
      <el-transfer
        v-loading="dialogTableLoading"
        filterable
        :filter-method="filterMethod"
        :button-texts="['到左边', '到右边']"
        :titles="['未授权', '已授权']"
        filter-placeholder="请输入机构名称"
        v-model="dialogFundCheckArray"
        :format="{
          noChecked: '${total}',
          hasChecked: '${checked}/${total}'
        }"
        :data="dialogFundTable"
      >
        <span slot-scope="{ option }">
          <el-tooltip :content="`${option.deptId} - ${option.deptName}`">
            <span>
              <span>{{ option.deptName }}</span>
            </span>
          </el-tooltip>
        </span>
      </el-transfer>
      <div slot="footer" class="dialog-footer standard-form">
        <el-button type="primary" size="small" @click="handleFundSubmit" :loading="dialogBtnLoading">提 交</el-button>
        <el-button size="small" type="info" plain @click="fundDialogVisible = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { TABLECOLUMNS_FUNDAUTH } from '../constant/index'
import Pagination from '@/components/Pagination'
import pageApi from '../api'

export default {
  components: { Pagination },
  data() {
    return {
      fundDialogTitle: '',
      fundDialogVisible: false,
      dialogFundTable: [],
      dialogFundCheckArray: [],
      dialogFundRightDefaultCheckedArray: [],
      // 指标功能分类
      typeBusArr: [
        { dimCde: '0', dimNme: '普通指标' },
        { dimCde: '1', dimNme: '自定义指标' },
        { dimCde: '2', dimNme: '查询条件指标' }
      ],

      dialogTable: [],
      dialogTableLoading: false,
      copyDialogVisible: false,
      dialogBtnLoading: false,
      currentSetRow: null,

      tableData: [],
      tableHeight: '',
      tableLoading: false,
      tableColumns: TABLECOLUMNS_FUNDAUTH,
      formQuery: {
        indexName: '',
        pageNum: 1,
        pageSize: 10,
        total: 0
      }
    }
  },
  methods: {
    filterMethod(query, item) {
      return item.queryStr.indexOf(query) > -1
    },
    handleFundSubmit() {
      let params = {}
      params.indexCode = this.currentSetRow.indexCode
      params.targetDeptIds = this.dialogFundCheckArray
      this.dialogBtnLoading = true
      pageApi.grantDeptByIndex(params).then((res) => {
        let { status, message } = res.data
        this.dialogBtnLoading = false
        if (status === 200) {
          this.$message.closeAll()
          this.$message.success(message || '机构授权成功')
          this.fundDialogVisible = false
          this.$nextTick(() => {
            this.onQuery(false)
          })
        } else {
          this.$message.closeAll()
          this.$message.warning(message || '机构授权失败')
        }
      })
    },
    // 拷贝确定按钮
    handleCopySubmit() {
      let checkArray = this.$refs.dialogTableRef.getCheckboxRecords(true)
      if (checkArray && checkArray.length > 0) {
        let params = {}
        params.deptId = this.currentSetRow.deptId
        params.targetDeptIds = checkArray.map((item) => item.deptId)
        this.dialogBtnLoading = true
        pageApi.copyPermission(params).then((res) => {
          this.dialogBtnLoading = false
          let { status, message } = res.data
          if (status === 200) {
            this.$message.closeAll()
            this.$message.success(message || '复制成功')
            this.copyDialogVisible = false
            this.$nextTick(() => {
              this.onQuery(false)
            })
          } else {
            this.$message.closeAll()
            this.$message.warning(message || '复制失败')
          }
        })
      } else {
        this.$message.closeAll()
        this.$message.warning('机构不能为空')
        return
      }
    },

    // 机构授权
    fundAuth(row) {
      this.currentSetRow = row
      this.fundDialogTitle = `选择机构，将${row.indexName}授权给下方所勾选的机构`
      this.fundDialogVisible = true
      this.dialogFundCheckArray = []
      this.dialogFundTable = []
      this.$nextTick(() => {
        let params = {}
        params.indexCode = row.indexCode
        this.dialogTableLoading = true
        pageApi.deptDialogList(params).then((res) => {
          this.dialogTableLoading = false
          let { status, data } = res.data
          if (status == 200) {
            let tempArray = []
            data.forEach((item) => {
              item.key = item.deptId
              item.label = item.deptName
              item.queryStr = `${item.deptName}${item.deptId}`
              if (item.isCheck == '1') {
                tempArray.push(item.deptId)
              }
            })
            this.dialogFundCheckArray = tempArray
            this.dialogFundTable = data
          }
        })
      })
    },
    // 复制授权
    copyAuth(row) {
      this.currentSetRow = row
      this.copyDialogVisible = true
      this.$nextTick(() => {
        this.dialogTableLoading = true
        let params = {}
        params.excludeDeptId = row.deptId
        // 请求 数据
        pageApi.companyDialogList(params).then((res) => {
          this.dialogTableLoading = false
          let { status, data } = res.data
          if (status === 200) {
            this.dialogTable = data
          } else {
            this.dialogTable = []
          }
        })
      })
    },
    pagination(val) {
      const { page, limit } = val
      this.formQuery.pageNum = page
      this.formQuery.pageSize = limit
      this.onQuery(false)
    },
    reset() {
      this.formQuery.indexName = ''
    },
    onQuery(flag) {
      if (flag) {
        this.formQuery.pageNum = 1
      }
      const params = Object.assign({}, this.formQuery)
      this.tableLoading = true
      pageApi.indexPageList(params).then((res) => {
        this.tableLoading = false
        const { status, data } = res.data
        if (status === 200) {
          this.tableData = data.list
          this.formQuery.total = data.total
        } else {
          this.tableData = []
          this.formQuery.total
        }
      })
    },

    handleTableHeight() {
      setTimeout(() => {
        const appMain = document.getElementById('app').offsetHeight
        const ddQuery = document.getElementById('dd-query').offsetHeight
        const diff = appMain - ddQuery - 10 - 120 - 100
        if (diff < 300) {
          this.tableHeight = 300
        } else {
          this.tableHeight = diff
        }
      }, 150)
    }
  },
  activated() {
    this.handleTableHeight()
  },
  mounted() {
    this.handleTableHeight()
    this.onQuery(true)
  }
}
</script>
<style lang="scss" scoped>
::v-deep .el-tag.el-tag--medium.el-tag--light {
  border: none;
  background: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  color: #612d10!important
}
::v-deep .el-checkbox__input.is-checked+.el-checkbox__label {
  color: #612d10!important
}
::v-deep .el-transfer__button span {
  color: #612d10!important
}
.manager-auth {
  // padding: 10px;
}
::v-deep .el-transfer__button span {
  font-size: 14px;
  color: #fff;
}
::v-deep .el-dialog__footer {
  text-align: center !important;
}

::v-deep .el-dialog__wrapper .el-dialog__header {
  text-align: left !important;
}
::v-deep .el-dialog--center {
  text-align: left;
}

::v-deep .el-transfer-panel__ite {
  height: 40px;
}
::v-deep .el-tag {
  margin-right: 5px;
}
::v-deep .el-transfer {
  padding-left: 30px;
}

::v-deep .el-transfer-panel {
  width: 400px;
}
::v-deep .el-transfer-panel__list {
  height: 400px;
}
::v-deep .el-transfer-panel__body {
  height: 450px;
}
::v-deep .el-transfer-panel__item {
  height: 35px;
}
</style>
