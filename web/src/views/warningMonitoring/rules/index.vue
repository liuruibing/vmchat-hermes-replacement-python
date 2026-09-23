<!--
 * @Description:
 * @Author:
 * @Date: 2024-07-11 13:35:18
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2024-07-23 09:49:28
-->
<template>
  <div class="warningMonitoringRules">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form :inline="true" ref="formInline" :model="formInline" class="standard-form">
          <el-row>
            <el-col :span="24">
              <el-form-item label="">
                <el-input v-model="formInline.itname" size="small" placeholder="指标名称" clearable></el-input>
              </el-form-item>
              <el-form-item label="">
                <el-input v-model="formInline.rulename" size="small" placeholder="预警规则名称" clearable></el-input>
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.ittype" size="small" clearable filterable placeholder="监控对象类型">
                  <el-option v-for="item in ittypeList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.warnLevel" size="small" clearable filterable placeholder="风险等级">
                  <el-option v-for="item in warnLevelList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item label="">
                <el-select v-model="formInline.itdisable" size="small" clearable filterable placeholder="是否启用">
                  <el-option v-for="item in itdisableList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                </el-select>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" size="small" icon="el-icon-search" @click="handleSearchTable(true)">查询</el-button>
                <el-button type="info" plain size="small" icon="el-icon-plus" @click="openAddFromDialog('add')">新增</el-button>
              </el-form-item>
            </el-col>
          </el-row>
        </el-form>
        <ToolBarSlot>
          <template slot="left">
            <el-button size="small" type="info" plain icon="el-icon-delete" @click="batchDelete">批量删除</el-button>
            <el-button size="small" type="info" plain icon="el-icon-video-pause" @click="batchStop">批量停止</el-button>
          </template>
        </ToolBarSlot>
      </div>
    </div>
    <div class="table-content" id="standard-table">
      <div id="standard-table-margin">
        <vxe-table
          ref="refsTable"
          v-loading="tableLoading"
          :cell-style="{ height: '50px' }"
          :data="tableData"
          :height="tableHeight"
          auto-resize
          stripe
          sync-resize
          show-overflow="tooltip"
          style="width: 100%"
          :sort-config="{ remote: true }"
          @sort-change="customSortMethod"
          resizable
        >
          <vxe-table-column type="checkbox" width="60" align="center"></vxe-table-column>
          <vxe-table-column
            v-for="item in column"
            :key="item.prop"
            :align="item.align"
            :field="item.prop"
            :show-overflow-tooltip="item.showtooltip"
            :title="item.label"
            :min-width="item.width"
            header-align="center"
            sortable
          >
            <template slot-scope="{ row }">
              <span v-if="item.format === 'dict'" :style="{ color: transf(`${row[item.prop]}_color`, item.prop) }">
                <span v-if="item.prop === 'warnLevel'">
                  <el-tag size="mini" type="danger" v-if="row[item.prop] == '3'">{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
                  <el-tag size="mini" type="warning" v-else-if="row[item.prop] == '2'">{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
                  <el-tag size="mini" type="success" v-else>{{ transf(row[item.prop], item.prop) || '-' }}</el-tag>
                </span>
                <span v-else>{{ transf(row[item.prop], item.prop) || '-' }}</span>
              </span>

              <span v-else>{{ row[item.prop] | noDataFilter }}</span>
            </template>
          </vxe-table-column>
          <vxe-table-column label="详情" align="center" width="400px" fixed="right">
            <template slot-scope="{ row }">
              <span class="table-operation">
                <el-button :disabled="czlDisabled" type="info" plain size="small" @click="openAddFromDialog('edit', row)">编辑</el-button>
                <el-button :disabled="czlDisabled" type="info" plain size="small" @click="openCpOrJgConfig(row)">
                  <span v-if="row.ittype == '1'">适用产品</span>
                  <span v-if="row.ittype == '2'">适用机构</span>
                </el-button>
                <el-button :disabled="czlDisabled" type="info" plain size="small" @click="openEmailConfig(row)">邮箱设置</el-button>
                <el-button :disabled="czlDisabled" type="info" plain size="small" @click="deleteRow(row)">删除</el-button>
              </span>
            </template>
          </vxe-table-column>
        </vxe-table>
      </div>
    </div>
    <div class="table-footer">
      <Pagination :total="total" :limit="formInline.pageSize" :page="formInline.pageNum" @pagination="pagination" />
    </div>
    <!-- 新增、编辑 -->
    <addFormDialog ref="addFormRef" v-if="addFormShow" :indexList="indexList" @close="addFormShow = false" @refresh="handleSearchTable(true)"></addFormDialog>
    <!-- 邮件设置 -->
    <emailConfigDialog ref="emailConfigRef" v-if="emailConfigShow" @close="emailConfigShow = false"></emailConfigDialog>
    <!-- 机构选择 -->
    <department-component
      v-if="jgConfigShow"
      ref="departmentRef"
      :department-visible="jgConfigShow"
      :company-list="companyList"
      @dialogclose="handleCloseJgDialog"
      @submit="handleSubmitJg"
      multiple
    ></department-component>
    <!-- 产品选择 -->
    <product-selector
      v-if="cpConfigShow"
      ref="productSelectorRef"
      :multiple="true"
      :leftList="left"
      :dialog-visible="cpConfigShow"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="zstgwb"
      @closedialog="handleDialogCpClosed"
      @submitdialog="handleSubmitCp"
    ></product-selector>
  </div>
</template>

<script>
import CONSTANTS from './scripts/constants'
import Pagination from '@/components/Pagination'
import { downLoadFileByUrl } from '@/utils'
import commonFun from '@/filters/common'
import pageApi from './scripts/api.js'
import addFormDialog from './components/addFormDialog.vue'
import emailConfigDialog from './components/emailConfigDialog.vue'
import productSelector from './components/productSelector'
import departmentComponent from './components/departmentComponent'
import ToolBarSlot from '@/components/toolBarSlot'
import store from "../../../store";
export default {
  name: 'warningMonitoringRules',
  components: {
    Pagination,
    addFormDialog,
    emailConfigDialog,
    productSelector,
    departmentComponent,
    ToolBarSlot
  },
  data() {
    return {
      that: this,
      // form表单绑定
      formInline: {
        itname: '',
        rulename: '',
        ittype: '',
        warnLevel: '',
        itdisable: '',
        orderString: '',
        pageSize: 20,
        pageNum: 1
      },
      // 表格高度
      tableHeight: 0,
      // 表格loading
      tableLoading: false,
      // 表格数据
      tableData: [],
      // 表格列
      column: CONSTANTS.TABLE_COLUMNS,
      // 总条数
      total: 0,
      // 监控对象类型
      ittypeList: CONSTANTS.ittypeList,
      ittypeMap: {},
      // 风险等级选项
      warnLevelList: CONSTANTS.warnLevelList,
      warnLevelMap: {},
      // 是否启用选项
      itdisableList: CONSTANTS.itdisableList,
      itdisableMap: {},
      // 邮件提醒规则
      emailRuleList: CONSTANTS.emailRuleList,
      emailRuleMap: {},
      // 新增 | 编辑状态
      isEdit: false,
      exportButton2: false, // 导出
      exportIcon2: 'el-icon-download',
      exportText2: '导出',
      addFormShow: false,
      emailConfigShow: false,
      currentRow: {},
      cpConfigShow: false,
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        },
        {
          label: '私有产品',
          code: 'sycp'
        }
      ],
      left:false,
      showTreeKeyArray: ['产品列表','我的关注'],
      selectList: [],
      jgConfigShow: false,
      companyList: [],
      indexList: [],
      indexMap: {},
      czlDisabled: false
    }
  },
  computed: {
    transf() {
      return (val, type) => {
        if (!(val || val === 0)) return
        if (type === 'ittype') {
          return this.ittypeMap[val] || val
        }
        if (type === 'warnLevel') {
          return this.warnLevelMap[val] || val
        }
        if (type === 'emailRule') {
          return this.emailRuleMap[val] || val
        }
        if (type === 'itdisable') {
          return this.itdisableMap[val] || val
        }
        if (type === 'itcode') {
          return this.indexMap[val] || val
        }
      }
    }
  },
  mounted() {
    if(store.state.edims.userType == '2' || store.state.edims.userType == 2){
      this.left = true;
      this.showTreeKeyArray = ['产品列表'];
    }
    this.initData()
  },
  methods: {
    /**
     * @description 初始化数据
     */
    initData() {
      this.getIndexList()
      this.setDictMap()
      // 动态设置表格高度
      this.handleTableHeight()
      // 查询表格
      this.handleSearchTable(true)
    },
    setDictMap() {
      this.ittypeList.forEach((item) => {
        this.$set(this.ittypeMap, item.dimCde, item.dimNme)
      })
      this.warnLevelList.forEach((item) => {
        this.$set(this.warnLevelMap, item.dimCde, item.dimNme)
        this.$set(this.warnLevelMap, `${item.dimCde}_color`, item.color)
      })
      this.itdisableList.forEach((item) => {
        this.$set(this.itdisableMap, item.dimCde, item.dimNme)
      })
      this.emailRuleList.forEach((item) => {
        this.$set(this.emailRuleMap, item.dimCde, item.dimNme)
      })
    },
    // 获取指标数据
    getIndexList() {
      pageApi.itemList({}).then((res) => {
        const { data, status } = res.data
        if (status === 0) {
          this.indexList = data || []
          this.indexList.forEach((item) => {
            this.$set(this.indexMap, item.itcode, item.itname)
          })
        }
      })
    },
    /**
     * @description 去除无值字段，包含数组
     */
    parameterSrc(data) {
      const newData = {}
      for (const key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null || JSON.stringify(data[key]) === '[]') {
        } else {
          newData[key] = data[key]
        }
      }
      return newData
    },
    /**
     * @description 动态设置表格高度
     */
    handleTableHeight() {
      this.$nextTick(() => {
        // 根据浏览器高度设置初始高度
        this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        // 监听浏览器高度变化，修改表格高度
        window.onresize = () => {
          this.tableHeight = window.innerHeight - this.$refs.refsTable.$el.offsetTop - 185
        }
      })
    },
    /**
     * @description 表格查询
     */
    handleSearchTable(flag) {
      if (flag) {
        this.formInline.pageNum = 1
      }
      let params = Object.assign({}, this.formInline)
      delete params.date
      params = this.parameterSrc(params)
      this.tableLoading = true
      this.tableData = []
      this.total = 0
      pageApi.warnRuleManageList(params).then((res) => {
        this.tableLoading = false
        const { data, status } = res.data
        if (status === 0 && data) {
          this.tableData = data.list || []
          this.total = data.total || 0
        } else {
          this.tableData = []
          this.total = 0
        }
      })
    },
    /**
     * @description 监听分页
     */
    pagination(val) {
      let { page, limit } = val
      this.formInline.pageNum = page
      this.formInline.pageSize = limit
      this.handleSearchTable(false)
    },
    // 排序的公共方法
    customSortMethod(val) {
      this.formInline.orderString = commonFun.queryOrderBy_vxe_template(val)
      this.handleSearchTable(false)
    },
    // 新增/编辑
    openAddFromDialog(type, row) {
      if (type === 'add') {
        this.addFormShow = true
      }
      if (type === 'edit') {
        this.addFormShow = true
        this.$nextTick(() => {
          this.$refs.addFormRef.init(row)
        })
      }
    },
    // 批量删除
    batchDelete() {
      this.$message.closeAll()
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) {
        return this.$message.warning('请至少选择一条数据')
      }
      this.$confirm('此操作将删除勾选数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          let params = { ids: list.map((item) => item.id) }
          pageApi.delete(params).then((res) => {
            const { status, message } = res.data
            if (status === 200) {
              this.$message({
                type: 'success',
                message: message || '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable(true)
            } else {
              this.$message({
                customClass: 'message-error',
                type: 'error',
                message: message || '删除失败'
              })
            }
          })
        })
        .catch(() => {})
    },
    // 删除
    deleteRow(row) {
      this.$message.closeAll()
      this.$confirm('此操作将删除改数据, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
        confirmButtonClass: 'standard-confirm',
        cancelButtonClass: 'standard-cancel'
      })
        .then(() => {
          this.czlDisabled = true
          let params = { ids: [row.id] }
          pageApi.delete(params).then((res) => {
            this.czlDisabled = false
            const { status, message } = res.data
            if (status === 200) {
              this.$message({
                type: 'success',
                message: message || '删除成功',
                customClass: 'message-success'
              })
              this.handleSearchTable(true)
            } else {
              this.$message({
                customClass: 'message-error',
                type: 'error',
                message: message || '删除失败'
              })
            }
          })
        })
        .catch(() => {})
    },
    // 批量停止
    batchStop() {
      this.$message.closeAll()
      const list = this.$refs.refsTable.getCheckboxRecords() || []
      if (!list.length) {
        return this.$message.warning('请至少选择一条数据')
      }
      let params = { ids: list.map((item) => item.id) }
      pageApi.updateDisableStatus(params).then((res) => {
        const { status, message } = res.data
        if (status === 200) {
          this.$message({
            type: 'success',
            message: message || '操作成功',
            customClass: 'message-success'
          })
          this.handleSearchTable(true)
        } else {
          this.$message({
            customClass: 'message-error',
            type: 'error',
            message: message || '操作失败'
          })
        }
      })
    },
    // 邮箱设置
    openEmailConfig(row) {
      this.$message.closeAll()
      this.czlDisabled = true
      pageApi.emailList({ id: row.id }).then((res) => {
        this.czlDisabled = false
        const { status, data, message } = res.data
        if (status === 0) {
          this.emailConfigShow = true
          this.$nextTick(() => {
            this.$refs.emailConfigRef.init({ row, data })
          })
        } else {
          this.$message.error(message)
        }
      })
    },
    // 机构/产品配置
    openCpOrJgConfig(row) {
      this.currentRow = JSON.parse(JSON.stringify(row))
      this.companyList = []
      this.selectList = []
      this.czlDisabled = true
      pageApi.objList({ id: row.id }).then((res) => {
        const { status, data } = res.data
        if (status === 0) {
          if (row.ittype == '1') {
            this.selectList = (data || []).map((item) => ({ VC_FUNDCODE: item.objcode, VC_FUNDNAME: item.objName }))
            this.cpConfigShow = true
          }
          if (row.ittype == '2') {
            this.companyList = (data || []).map((item) => ({ objcode: item.objcode, COMPANY_NAME: item.objName }))
            this.jgConfigShow = true
          }
        }
        this.czlDisabled = false
      })
    },
    // 关闭机构弹窗
    handleCloseJgDialog(data) {
      this.jgConfigShow = false
    },
    // 提交机构选择
    handleSubmitJg(data) {
      const params = {
        id: this.currentRow.id,
        rkWrulesObjsModelList: (data || []).map((item) => ({ objcode: item.objcode }))
      }
      pageApi.objSettings(params).then((res) => {
        const { status, message } = res.data
        if (status === 200) {
          this.$message({
            type: 'success',
            message: message || '操作成功',
            customClass: 'message-success'
          })
          this.jgConfigShow = false
        } else {
          this.$refs.departmentRef.setDisabled(false)
          this.$message({
            customClass: 'message-error',
            type: 'error',
            message: message || '操作失败'
          })
        }
      })
    },
    // 关闭产品弹窗
    handleDialogCpClosed() {
      this.cpConfigShow = false
    },
    // 提交产品选择
    handleSubmitCp(data) {
      const params = {
        id: this.currentRow.id,
        rkWrulesObjsModelList: (data || []).map((item) => ({ objcode: item.VC_FUNDCODE }))
      }
      pageApi.objSettings(params).then((res) => {
        const { status, message } = res.data
        if (status === 200) {
          this.$message({
            type: 'success',
            message: message || '操作成功',
            customClass: 'message-success'
          })
          this.cpConfigShow = false
        } else {
          this.$message({
            customClass: 'message-error',
            type: 'error',
            message: message || '操作失败'
          })
          this.$refs.productSelectorRef.setDisabled(false)
        }
      })
    }
  },
  beforeDestroy() {
    // 组件销毁移除监听事件
    window.onresize = null
  }
}
</script>

<style lang="scss" scoped>
.warningMonitoringRules {
  // padding: 10px;
  .search-bar {
    // border-bottom: 1px solid #e1e0e0;
  }
  ::v-deep .el-form-item {
    margin-bottom: 0;
  }
  ::v-deep .vxe-table .vxe-body--row.row--stripe {
    background-color: #f9fafe !important;
  }
  ::v-deep .el-button.el-button--mini {
    padding: 7px !important;
  }
}
::v-deep .el-dialog.customClass {
  width: 55% !important;
}
</style>
<style>
.customClass .el-dialog__body .edit-product .el-form {
  width: 100% !important;
}
</style>
