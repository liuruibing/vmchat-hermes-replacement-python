<template>
  <div class="productorFilterSingle" v-auto-enter>
    <div v-if="false" class="template-tab-container">
      <div class="tabs-btn-wrap">
        <el-tabs
          v-model="activeTemplateKey"
          type="card"
          @tab-click="handleTabClick"
          @tab-remove="deleteTemplate"
          :key="templateList.length"
          class="custom-tabs"
        >
          <el-tab-pane
            label="基础模板"
            name="baseTemplate"
            :closable="false"
          ></el-tab-pane>
          <el-tab-pane
            v-for="item in templateList"
            :key="item.templateKey"
            :label="item.templateName"
            :name="item.templateKey"
            closable
          ></el-tab-pane>
        </el-tabs>
        <el-button
          type="text"
          icon="el-icon-plus"
          class="add-template-btn"
          @click="openAddTemplateDialog"
          @mousedown.stop
        >
          新增模板
        </el-button>
      </div>
    </div>

    <el-dialog
      title="新增条件模板"
      :visible.sync="templateDialogVisible"
      class="custom-dialog"
      @close="resetNewTemplateName"
    >
      <el-form :model="templateForm" :rules="templateRules" ref="templateForm">
        <el-form-item prop="name">
          <el-input
            v-model="templateForm.name"
            placeholder="请输入模板名称"
            maxlength="20"
            show-word-limit
            style="width: 80% !important"
          ></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="templateDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="addTemplate">保存</el-button>
      </div>
    </el-dialog>

<!--    <div class="condition-btn-container">
      <el-button size="small" type="primary" @click="saveCurrentCondition">保存当前模版查询条件</el-button>
      <el-button size="small" type="default" @click="clearCurrentCondition">清除当前模版查询条件</el-button>
    </div>-->

    <all-market-query
      ref="allMarketQuery"
      :page-list="pageList"
      :order-list="orderList"
      :table-loading="tableLoading"
      :export-disabled="isDisabled"
      @resetPage="resetPageList"
      @updateLoading="getTableLoading"
      @updateTable="getTabelData"
      @radioSource="getRadioSource"
      @updateheight="updateHeight"
      :simpleSearchPro="parentJson"
      @grandChildObj="function(newObj, source) { handleSimpleSearch(newObj, source); }"
      @clearCurrentCondition="clearCurrentCondition"
      @excelexport="handleExcelExport"
    ></all-market-query>
    <smjj-table
      ref="smjjTable"
      :table-data="tableData"
      :table-loading="tableLoading"
      :selected-conditions="parentJson.dynamicTags"
      @updatelist="updatelist"
      @sorttable="handleSortTable"
      @removecondition="removeCondition"
    ></smjj-table>
    <div style="margin: 0 10px 0px 10px;">
    <vxe-pager
      :current-page="pageList._pageNum"
      :page-size="pageList._pageSize"
      :total="total"
      :layouts="['PrevPage', 'JumpNumber', 'NextPage', 'FullJump', 'Sizes', 'Total']"
      border
      size="medium"
      class="standard-vxe-pager"
      @page-change="pagination"
    />
    </div>
  </div>
</template>
<script>
import AllMarketQuery from './components/searchQuery'
import smjjTable from './components/smjjTable'
import Pagination from '@/components/Pagination'

export default {
  components: { AllMarketQuery, smjjTable, Pagination },
  data() {
    return {
      moduleCode: "productroFilterSingle",
      // 原有变量
      tableLoading: false,
      tableData: [],
      pageList: {
        _pageNum: 1,
        _pageSize: 20
      },
      orderList: {
        orderString: 'm1_return desc'
      },
      total: 0,
      exportLoading: false,
      isDisabled: false,
      // 查询条件
      parentJson: {
        simpleSearch: {
          fundName: '',
          managerName: '',
          asset_list: ['不限'],
          endDate: ''
        },
        dynamicTags:[]
      },

      // 模板管理变量
      templateList: [],
      activeTemplateKey: 'baseTemplate',
      templateDialogVisible: false,
      // 初始化表单对象，确保响应式
      templateForm: {
        name: ''
      },
      templateRules: {
        name: [{ required: true, message: '请输入模板名称', trigger: 'blur' }]
      },
      storagePrefix: 'privateFundConditionTemplate_'
    }
  },
  methods: {
    handleSimpleSearch: function(newObj, source) {
      if (source === 'child') {
        this.parentJson.simpleSearch = newObj
      }
      if (source === 'grandChild') {
        this.parentJson.dynamicTags = newObj
      }
    },
    updateHeight() {
      setTimeout(() => {
        this.$refs.smjjTable.$refs.tableBody.handleTableHeight()
      }, 100)
    },
    // 页面导出
    handleExcelExport() {
      let selectedColumnIds = [];
      if (this.$refs.smjjTable && typeof this.$refs.smjjTable.getSelectedColumnIds === 'function') {
        selectedColumnIds = this.$refs.smjjTable.getSelectedColumnIds();
      }
      if (!selectedColumnIds || selectedColumnIds.length === 0) {
        this.$message.warning('请至少选择一列后再导出');
        return;
      }

      const columns = this.$refs.smjjTable.column.filter(column => selectedColumnIds.includes(column.id))
      const csvRows = [
        columns.map(column => column.label).join(','),
        ...this.tableData.map(row => columns.map(column => {
          const value = row[column.id] === undefined || row[column.id] === null ? '' : row[column.id]
          return `"${String(value).replace(/"/g, '""')}"`
        }).join(','))
      ]
      const blob = new Blob(['\ufeff' + csvRows.join('\n')], { type: 'text/csv;charset=utf-8' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = '产品详情-静态测试数据.csv'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(link.href)
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
     * @description 设置排序字段
     */
    handleSortTable(val) {
      this.orderList.orderString = this.$fun.queryOrderBy_vxe_template(val)
      if (val.order) {
        this.$refs.allMarketQuery.handleQueryParams()
      }
    },
    /**
     * @description 回传表格数据
     */
    getTabelData(table) {
      this.tableData = table.rows
      this.total = table.total
    },
    /**
     * @description 回传表格loading状态
     */
    getTableLoading(flag) {
      this.tableLoading = flag
    },
    /**
     * @description 回传重置分页
     */
    resetPageList() {
      this.pageList._pageNum = 1
    },
    getRadioSource(val) {},

    removeCondition(tag) {
      if (this.$refs.allMarketQuery) {
        this.$refs.allMarketQuery.removeCondition(tag)
      }
    },

    pagination(val) {
      var currentPage = val.currentPage
      var pageSize = val.pageSize
      this.pageList._pageNum  = currentPage
      this.pageList._pageSize = pageSize
      if (this.$refs.allMarketQuery) {
        this.$refs.allMarketQuery.handleQueryParams()
      }
    },
    // 刷新列表
    updatelist() {
      if (this.$refs.allMarketQuery) {
        this.$refs.allMarketQuery.handleQueryParams()
      }
    },


    openAddTemplateDialog() {
      this.templateDialogVisible = true
      this.templateForm.name = ''
    },

    handleTabClick(tab) {},

    /**
     * 加载模板列表
     */
    loadTemplates() {
      this.templateList = []
    },

    /**
     * 加载模板条件
     */
    loadTemplateCondition() {
      this.resetParentJson()
    },

    /**
     * 重置查询条件
     */
    resetParentJson() {
      this.parentJson = {
        simpleSearch: {
          fundName: '',
          managerName: '',
          asset_list: ['不限'],
          endDate: ''
        },
        dynamicTags:[]
      }
    },

    /**
     * 新增模板
     */
    addTemplate() {
      if (!this.templateForm.name) {
        this.$message.warning('请输入模板名称')
        return
      }
      this.templateList.push({
        templateKey: `demo-${Date.now()}`,
        templateName: this.templateForm.name
      })
      this.templateDialogVisible = false
      this.resetNewTemplateName()
      this.$message.success('已新增本地测试模板')
    },

    /**
     * 删除模板
     */
    deleteTemplate(templateKey) {
      this.templateList = this.templateList.filter(item => item.templateKey !== templateKey)
      this.activeTemplateKey = 'baseTemplate'
    },

    /**
     * 清除当前条件
     */
    clearCurrentCondition() {
      var self = this
      this.$confirm('确定清除所有条件吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(function() {
        self.resetParentJson()
        self.$message.success('清除条件成功')
      }).catch(function() {
        self.$message.info('已取消清除')
      })
    },

    /**
     * 重置新增模板名称
     */
    resetNewTemplateName: function() {
      this.templateForm.name = ''
      if (this.$refs.templateForm) {
        this.$refs.templateForm.resetFields()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.productorFilterSingle {
  margin-bottom: 20px;
}

.template-tab-container {
  margin: 0 10px 0px 10px;

  .tabs-btn-wrap {
    display: inline-flex;
    align-items: stretch;
    //border: 1px solid #e4e7ed;
    border-radius: 4px;
    overflow: hidden;
  }

  .custom-tabs {
    :deep(.el-tabs--card) {
      border: none !important;
      .el-tabs__nav {
        border-bottom: none !important;
        padding: 0 !important;
      }
      .el-tabs__item {
        border-radius: 0 !important;
        margin: 0 !important;
      }
      .el-tabs__item.is-active {
        background-color: #fff;
        color: #612d10;
      }
    }
  }
  ::v-deep .el-tabs--card>.el-tabs__header .el-tabs__item.is-active {
    background-image: linear-gradient(to right, #f5d7bc, #e0b794) !important;
  }
  .add-template-btn {
    height: 37px;
    line-height: 37px;
    padding: 0 15px;
    border: 1px solid #e4e7ed;
    border-left:0px;
    background-color: #fff;
    color: #612d10;
    margin: 0;
    cursor: pointer;
    border-radius: 0 !important;

    &:hover {
      background-color: #ecf5ff;
      color: #612d10;
      border-left-color: #c6e2ff;
    }
  }
}

.condition-btn-container {
  margin: 0 10px 16px 10px;
  button {
    margin-right: 8px;
  }
}
::v-deep .custom-dialog .el-dialog {
  width: 35% !important;
}
</style>
