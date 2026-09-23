<template>
  <div class="paramTemp-container">
    <!-- 查询条件表单 -->
    <el-form :inline="true" :model="queryParams" class="demo-form-inline">
      <!-- <el-form-item>
        <el-select v-model="queryParams.vcStrategyType" placeholder="请选择模板类型" size="small" multiple collapse-tags
          clearable>
          <el-option v-for="item in strategyTypeList" :key="item.dimCde" :label="item.dimNme"
            :value="item.dimCde"></el-option>
        </el-select>
      </el-form-item> -->
      <el-form-item>
        <el-input v-model="queryParams.vcInterfacceName" placeholder="请输入接口名称" size="small" clearable></el-input>
      </el-form-item>
      <el-form-item>
        <el-select v-model="queryParams.vcIndexType" placeholder="请选择接口类型" size="small" clearable>
          <el-option v-for="item in indexTypeList" :key="item.dimCde" :label="item.dimNme"
            :value="item.dimCde"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" size="small" @click="handleQuery">查询</el-button>
        <el-button type="info" icon="el-icon-refresh" size="small" @click="resetQuery">重置</el-button>
        <el-button type="primary" icon="el-icon-plus" size="small" @click="handleAdd">新增</el-button>
      </el-form-item>
    </el-form>

    <!-- 数据表格 -->
    <div class="paramTemp-table-container" id="standard-table">
      <vxe-table border show-overflow auto-resize height="auto" :data="tableData" :loading="loading" ref="xTable">
        <vxe-table-column field="vcInterfacceName" title="接口名称" min-width="150" align="center"></vxe-table-column>
        <vxe-table-column field="vcIndexType" title="接口类型" min-width="120" align="center">
          <template #default="{ row }">
            {{ transf(row.vcIndexType, 'vcIndexType') }}
          </template>
        </vxe-table-column>
        <vxe-table-column field="vcRemake" title="备注" min-width="150" align="center">
          <template #default="{ row }">
            <span>{{ row.vcRemake | noDataFilter }}</span>
          </template>
        </vxe-table-column>
        <vxe-table-column title="操作" width="400" align="center" fixed="right">
          <template #default="{ row }">
            <span class="table-operation">
              <el-button type="info" size="small" @click="handleViewCode(row)">查看代码</el-button>
              <el-button type="info" size="small" @click="handleCopyAdd(row)">复制新增</el-button>
              <el-button type="info" size="small" @click="handleEdit(row)">编辑</el-button>
              <el-button type="info" size="small" @click="handleDelete(row)">删除</el-button>
            </span>
          </template>
        </vxe-table-column>
      </vxe-table>
    </div>

    <Pagination :total="total" :limit="queryParams.pageSize" :page="queryParams.pageNum" @pagination="pagination">
    </Pagination>

    <!-- 参数配置弹窗 -->
    <ParamConfig ref="paramConfigRef" v-if="paramConfigVisible" @close="paramConfigVisible = false"
      @refresh="getList" />

    <!-- 代码展示弹窗 -->
    <code-dialog :visible.sync="codeDialogVisible" :java-code="generatedJavaCode" :python-code="generatedPythonCode" />
  </div>
</template>

<script>
import Pagination from '@/components/NewPagination'
import ParamConfig from './components/paramConfig'
import CodeDialog from './components/codeDialog.vue'
import CONSTANTS from "../constants.js"
import api from "./api"
import { Base64 } from 'js-base64'

export default {
  name: 'ParamTemp',
  components: {
    Pagination,
    ParamConfig,
    CodeDialog
  },
  data() {
    return {
      queryParams: {
        vcStrategyType: [],
        vcInterfacceName: '',
        vcIndexType: '',
        pageNum: 1,
        pageSize: 20
      },
      strategyTypeList: [
        { dimCde: 'D', dimNme: '标准参数模板' },
        { dimCde: 'C', dimNme: '自定义参数模板' }
      ],
      indexTypeList: [],
      dataFrequencyList: [],
      loading: false,
      tableData: [],
      total: 0,
      selectedProducts: [],
      isProductExpanded: false,
      strategyTypeObj: {},
      indexTypeObj: {},
      dataFrequencyObj: {},
      paramConfigVisible: false,
      codeDialogVisible: false,
      generatedJavaCode: '',
      generatedPythonCode: ''
    }
  },
  created() {
    this.setDictObj()
    this.getList()
  },
  methods: {
    setDictObj() {
      this.strategyTypeList.forEach(item => {
        this.strategyTypeObj[item.dimCde] = item.dimNme
      })
      this.indexTypeList = [...CONSTANTS.TEMPTYPE]
      this.indexTypeList.forEach(item => {
        this.indexTypeObj[item.dimCde] = item.dimNme
      })
      this.dataFrequencyList = CONSTANTS.DATAFREQUENCY
      this.dataFrequencyList.forEach(item => {
        this.dataFrequencyObj[item.dimCde] = item.dimNme
      })
    },
    async getList() {
      this.loading = true
      try {
        const params = {
          vcStrategyType: this.queryParams.vcStrategyType.length > 0 ? this.queryParams.vcStrategyType.join(',') : undefined,
          vcInterfacceName: this.queryParams.vcInterfacceName || undefined,
          vcIndexType: this.queryParams.vcIndexType || undefined,
          pageNum: this.queryParams.pageNum,
          pageSize: this.queryParams.pageSize
        }
        const res = await api.paramPage(params)
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
    handleQuery() {
      this.queryParams.pageNum = 1
      this.getList()
    },
    resetQuery() {
      this.queryParams = {
        vcStrategyType: [],
        vcInterfacceName: '',
        vcIndexType: '',
        pageNum: 1,
        pageSize: 20
      }
      this.selectedProducts = []
      this.getList()
    },
    pagination(val) {
      this.queryParams.pageNum = val.page
      this.queryParams.pageSize = val.limit
      this.getList()
    },
    transf(val, type) {
      if (type === 'vcStrategyType') {
        return this.strategyTypeObj[val] || val
      }
      if (type === 'vcIndexType') {
        return this.indexTypeObj[val] || val
      }
    },
    handleViewCode(row) {
      let configStr = row.vcConfig || row.VcConfig || row.VC_CONFIG
      if (configStr) {
        try {
          const config = JSON.parse(configStr)
          if (config.vcCode) {
            this.generatedJavaCode = config.vcCode.java ? Base64.decode(config.vcCode.java) : ''
            this.generatedPythonCode = config.vcCode.python ? Base64.decode(config.vcCode.python) : ''
            this.codeDialogVisible = true
          } else {
            this.$message.warning('该配置暂无代码片段')
          }
        } catch (e) {
          console.error('解析配置失败', e)
          this.$message.error('代码片段解析失败')
        }
      } else {
        this.$message.warning('暂无配置数据')
      }
    },
    handleCopyAdd(row) {
      this.paramConfigVisible = true
      this.$nextTick(() => {
        const copyRow = JSON.parse(JSON.stringify(row))
        delete copyRow.vcStrategyId
        delete copyRow.VCSTRATEGYID
        copyRow.vcInterfacceName = copyRow.vcInterfacceName ? `${copyRow.vcInterfacceName}-复制` : '未命名接口-复制'
        this.$refs.paramConfigRef.init(copyRow, 'copyAdd')
      })
    },
    handleAdd() {
      this.paramConfigVisible = true
      this.$nextTick(() => {
        this.$refs.paramConfigRef.init({}, 'add')
      })
    },
    handleEdit(row) {
      this.paramConfigVisible = true
      this.$nextTick(() => {
        this.$refs.paramConfigRef.init(row, 'edit')
      })
    },
    handleDelete(row) {
      this.$confirm('确定删除该数据吗？', '提示', {
        type: 'warning'
      }).then(async () => {
        try {
          const res = await api.paramDelete({ vcStrategyId: row.vcStrategyId })
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
      }).catch(() => { })
    }
  }
}
</script>

<style lang="scss" scoped>
.paramTemp-container {
  height: 100%;
  padding: 12px 10px;
  display: flex;
  flex-direction: column;

  .paramTemp-table-container {
    flex: 1;
    overflow: hidden;
  }

  .product-popover-list {
    max-height: 300px;
    overflow-y: auto;

    .product-item {
      padding: 8px 0;
      border-bottom: 1px solid #f0f0f0;

      &:last-child {
        border-bottom: none;
      }
    }
  }
}
</style>
