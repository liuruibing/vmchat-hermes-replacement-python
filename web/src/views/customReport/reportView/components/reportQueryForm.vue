<template>
  <div class="report-query-wrapper">
    <el-form
      ref="queryForm"
      :inline="true"
      :model="form"
      :rules="rules"
      label-width="auto"
      class="standard-form report-query-form"
    >
      <el-row>
        <el-col :span="24">
          <el-form-item prop="templateCode">
            <el-select
              v-model="form.templateCode"
              size="small"
              filterable
              clearable
              placeholder="请选择模板"
              @change="handleTemplateChange"
            >
              <el-option
                v-for="item in templateList"
                :key="item.templateCode"
                :label="item.templateName"
                :value="item.templateCode"
              >
                <span style="float: left">{{ item.templateName }}</span>
                <span class="template-type-label">{{ getReportTypeName(item.paCrReportType) }}</span>
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item prop="dateRange">
            <el-date-picker
              v-model="form.dateRange"
              size="small"
              type="daterange"
              value-format="yyyy-MM-dd"
              range-separator="至"
              start-placeholder="请选择开始日期"
              end-placeholder="请选择结束日期"
            />
          </el-form-item>

          <el-form-item prop="fundNames">
            <el-tooltip
              :content="form.fundNames"
              :disabled="!form.fundNames"
              placement="top-start"
              effect="light"
            >
              <el-input
                v-model="form.fundNames"
                size="small"
                readonly
                placeholder="请选择产品"
                @click.native="openProductSelector"
              />
            </el-tooltip>
          </el-form-item>

          <el-form-item prop="timeFrequency">
            <el-select
              v-model="form.timeFrequency"
              size="small"
              placeholder="请选择数据频率"
              clearable
            >
              <el-option
                v-for="item in timeFrequencyList"
                :key="item.dim_cde"
                :label="item.dim_nme"
                :value="item.dim_cde"
              />
            </el-select>
          </el-form-item>

          <el-form-item prop="benchmark">
            <el-select
              v-model="form.benchmark"
              size="small"
              filterable
              placeholder="请选择基准"
              clearable
            >
              <el-option
                v-for="item in benchmarkList"
                :key="item.dim_cde"
                :label="item.dim_nme"
                :value="item.dim_cde"
              />
            </el-select>
          </el-form-item>

          <el-form-item>
            <el-button
              :loading="queryLoading"
              type="primary"
              size="small"
              class="mb5"
              icon="el-icon-search"
              @click="handleQuery"
            >
              查询
            </el-button>
            <el-button
              type="info"
              size="small"
              plain
              icon="el-icon-refresh"
              @click="handleReset"
            >
              重置
            </el-button>
            <el-button
              :loading="exportLoading"
              :disabled="exportDisabled"
              size="small"
              icon="el-icon-download"
              @click="showExportDialog"
            >
              导出
            </el-button>
          </el-form-item>

          <el-form-item>
            <el-input
              :value="getReportTypeName(form.reportType)"
              size="small"
              class="report-type-input"
              placeholder="报告类型"
              readonly
            />
          </el-form-item>

          <el-form-item v-if="form.reportType === 'C'">
            <el-button
              size="small"
              type="text"
              @click="weightDialogVisible = true"
            >
              编辑权重
            </el-button>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>

    <product-selector
      v-if="productDialogVisible"
      :multiple="form.reportType !== 'A'"
      :left-list="false"
      :limit="form.reportType === 'A' ? 1 : -1"
      :dialog-visible="productDialogVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectedProductList"
      default-checked-keys="wdgz"
      @closedialog="productDialogVisible = false"
      @submitdialog="handleProductSubmit"
    />

    <el-dialog
      :visible.sync="weightDialogVisible"
      title="穿透产品权重"
      width="620px"
      append-to-body
    >
      <div class="weight-toolbar">
        <span>权重合计：{{ weightTotal }}%</span>
        <el-button
          type="primary"
          size="mini"
          icon="el-icon-plus"
          @click="openProductSelector"
        >
          选择产品
        </el-button>
      </div>
      <el-table
        :data="form.weightProducts"
        border
        size="small"
      >
        <el-table-column
          label="产品"
          min-width="280"
          show-overflow-tooltip
        >
          <template slot-scope="{ row }">
            <span>{{ row.fundName || getProductName(row.fundCode) }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="权重"
          width="160"
        >
          <template slot-scope="{ row }">
            <el-input-number
              v-model="row.weight"
              :min="0"
              :max="100"
              :precision="0"
              size="small"
              controls-position="right"
              style="width: 120px;"
            />
            <span class="weight-unit">%</span>
          </template>
        </el-table-column>
        <el-table-column
          label="操作"
          width="90"
          align="center"
        >
          <template slot-scope="{ $index }">
            <el-button
              :disabled="form.weightProducts.length === 1"
              type="text"
              size="small"
              icon="el-icon-delete"
              @click="removeWeightProduct($index)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="weightDialogVisible = false"
        >
          取消
        </el-button>
        <el-button
          type="primary"
          size="small"
          @click="confirmWeightProducts"
        >
          确定
        </el-button>
      </div>
    </el-dialog>

    <el-dialog
      :visible.sync="exportDialogVisible"
      title="添加水印"
      width="360px"
      append-to-body
    >
      <el-radio-group v-model="watermarkType">
        <el-radio label="user">用户名称</el-radio>
        <el-radio label="company">机构名称</el-radio>
      </el-radio-group>
      <div
        slot="footer"
        class="dialog-footer"
      >
        <el-button
          size="small"
          @click="exportDialogVisible = false"
        >
          取消
        </el-button>
        <el-button
          type="primary"
          size="small"
          @click="handleExport"
        >
          确认导出
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import productSelector from '@/components/productSelector'
import {
  benchmarkList,
  productList,
  reportTypeList,
  timeFrequencyList
} from '../mockData'

let rowKey = 0

function createWeightProduct(fundCode, weight, fundName) {
  rowKey += 1
  return {
    key: rowKey,
    fundCode,
    fundName,
    weight
  }
}

function toSelectorProduct(product) {
  return {
    id: product.fundCode,
    VC_FUNDCODE: product.fundCode,
    VC_FUNDNAME: product.fundName,
    D_CREATE_DATE: product.createDate || '2024-01-01',
    VC_INVESTSTRATEGY: product.strategy || '演示策略',
    VC_STRATEGY: product.subStrategy || '演示子策略',
    VC_NAME_GLR: product.manager || '演示管理人'
  }
}

export default {
  name: 'ReportQueryForm',
  components: {
    productSelector
  },
  props: {
    templateList: {
      type: Array,
      default: () => []
    },
    queryLoading: {
      type: Boolean,
      default: false
    },
    exportLoading: {
      type: Boolean,
      default: false
    },
    exportDisabled: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      reportTypeList,
      timeFrequencyList,
      productList,
      benchmarkList,
      exportDialogVisible: false,
      productDialogVisible: false,
      weightDialogVisible: false,
      watermarkType: 'user',
      selectedProductList: [],
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
        }
      ],
      showTreeKeyArray: ['产品列表', '我的关注'],
      form: this.getDefaultForm(),
      rules: {
        templateCode: [{ required: true, message: '请选择模板', trigger: 'change' }],
        fundNames: [{ required: true, message: '请选择产品', trigger: 'change' }],
        timeFrequency: [{ required: true, message: '请选择频率', trigger: 'change' }],
        dateRange: [{ required: true, type: 'array', message: '请选择时间区间', trigger: 'change' }],
        benchmark: [{ required: true, message: '请选择基准', trigger: 'change' }]
      }
    }
  },
  computed: {
    weightTotal() {
      return this.form.weightProducts.reduce((total, item) => {
        return total + Number(item.weight || 0)
      }, 0)
    }
  },
  methods: {
    getDefaultForm() {
      return {
        templateCode: '',
        reportType: '',
        fundCode: '',
        fundCodes: [],
        fundNames: '',
        weightProducts: [],
        timeFrequency: 'day',
        dateRange: ['2026-01-01', '2026-06-30'],
        benchmark: '000300'
      }
    },
    getReportTypeName(reportType) {
      const type = this.reportTypeList.find(item => item.repTypeCode === reportType)
      return type ? type.repTypeName : ''
    },
    getProductName(fundCode) {
      const selectedProduct = this.selectedProductList.find(item => item.VC_FUNDCODE === fundCode)
      const demoProduct = this.productList.find(item => item.fundCode === fundCode)
      return selectedProduct ? selectedProduct.VC_FUNDNAME : (demoProduct ? demoProduct.fundName : fundCode)
    },
    handleTemplateChange(templateCode) {
      const template = this.templateList.find(item => item.templateCode === templateCode)
      this.form.reportType = template ? template.paCrReportType : ''
      this.setDefaultProducts()
      this.$emit('template-change', templateCode)
      this.$nextTick(() => {
        this.$refs.queryForm && this.$refs.queryForm.clearValidate()
      })
    },
    setDefaultProducts() {
      if (this.form.reportType === 'A') {
        this.applySelectedProducts([toSelectorProduct(this.productList[0])])
      }
      if (this.form.reportType === 'B') {
        this.applySelectedProducts(this.productList.slice(0, 3).map(toSelectorProduct))
      }
      if (this.form.reportType === 'C') {
        this.applySelectedProducts(this.productList.slice(0, 3).map(toSelectorProduct), true)
      }
    },
    openProductSelector() {
      if (!this.form.reportType) {
        this.$message.warning('请先选择模板')
        return
      }
      this.productDialogVisible = true
    },
    handleProductSubmit(list) {
      const submitList = Array.isArray(list) ? list : []
      const nextList = this.form.reportType === 'A' ? submitList.slice(0, 1) : submitList

      this.applySelectedProducts(nextList, this.form.reportType === 'C')
      this.productDialogVisible = false
      this.$nextTick(() => {
        this.$refs.queryForm && this.$refs.queryForm.clearValidate('fundNames')
      })
    },
    applySelectedProducts(list, keepWeight) {
      const normalizedList = list.map(item => ({
        ...item,
        id: item.id || item.VC_FUNDCODE
      }))

      this.selectedProductList = normalizedList
      this.form.fundNames = normalizedList.map(item => item.VC_FUNDNAME).join(',')
      this.form.fundCode = normalizedList[0] ? normalizedList[0].VC_FUNDCODE : ''
      this.form.fundCodes = normalizedList.map(item => item.VC_FUNDCODE)

      if (this.form.reportType === 'C') {
        this.form.weightProducts = this.buildWeightProducts(normalizedList, keepWeight)
      }
    },
    buildWeightProducts(list, keepWeight) {
      const oldWeightMap = this.form.weightProducts.reduce((map, item) => {
        map[item.fundCode] = Number(item.weight || 0)
        return map
      }, {})
      const oldSelectedCodes = Object.keys(oldWeightMap)
      const newItems = list.filter(item => oldSelectedCodes.indexOf(item.VC_FUNDCODE) === -1)
      const preservedTotal = list.reduce((total, item) => {
        if (oldSelectedCodes.indexOf(item.VC_FUNDCODE) === -1) return total
        return total + oldWeightMap[item.VC_FUNDCODE]
      }, 0)
      const remaining = Math.max(0, 100 - preservedTotal)
      const equalWeight = newItems.length ? Math.floor(remaining / newItems.length) : 0
      let remainder = newItems.length ? remaining - equalWeight * newItems.length : 0

      if (!keepWeight || !this.form.weightProducts.length) {
        return this.createEqualWeightProducts(list)
      }

      return list.map(item => {
        let weight = oldWeightMap[item.VC_FUNDCODE]
        if (weight === undefined) {
          weight = equalWeight + (remainder > 0 ? 1 : 0)
          remainder -= 1
        }
        return createWeightProduct(item.VC_FUNDCODE, weight, item.VC_FUNDNAME)
      })
    },
    createEqualWeightProducts(list) {
      const baseWeight = list.length ? Math.floor(100 / list.length) : 0
      let remainder = list.length ? 100 - baseWeight * list.length : 0
      return list.map(item => {
        const weight = baseWeight + (remainder > 0 ? 1 : 0)
        remainder -= 1
        return createWeightProduct(item.VC_FUNDCODE, weight, item.VC_FUNDNAME)
      })
    },
    removeWeightProduct(index) {
      this.form.weightProducts.splice(index, 1)
      const codeList = this.form.weightProducts.map(item => item.fundCode)
      this.selectedProductList = this.selectedProductList.filter(item => codeList.indexOf(item.VC_FUNDCODE) !== -1)
      this.form.fundCodes = codeList
      this.form.fundCode = codeList[0] || ''
      this.form.fundNames = this.selectedProductList.map(item => item.VC_FUNDNAME).join(',')
    },
    confirmWeightProducts() {
      if (!this.validateWeightProducts()) return
      this.weightDialogVisible = false
    },
    handleReset() {
      const templateCode = this.form.templateCode
      const reportType = this.form.reportType
      this.form = this.getDefaultForm()
      this.form.templateCode = templateCode
      this.form.reportType = reportType
      this.setDefaultProducts()
      this.$nextTick(() => {
        this.$refs.queryForm && this.$refs.queryForm.clearValidate()
      })
      this.$emit('reset')
    },
    handleQuery() {
      this.$refs.queryForm.validate(valid => {
        if (!valid || !this.validateWeightProducts()) return
        this.$emit('query', this.getPayload())
      })
    },
    validateWeightProducts() {
      if (this.form.reportType !== 'C') return true
      const hasEmpty = this.form.weightProducts.some(item => !item.fundCode)
      const hasRepeat = new Set(this.form.weightProducts.map(item => item.fundCode)).size !== this.form.weightProducts.length

      if (hasEmpty) {
        this.$message.warning('请选择穿透产品')
        return false
      }
      if (hasRepeat) {
        this.$message.warning('穿透产品不能重复')
        return false
      }
      if (this.weightTotal !== 100) {
        this.$message.warning('穿透产品权重合计需等于100%')
        return false
      }
      return true
    },
    getPayload() {
      return {
        reportCode: this.form.templateCode,
        reportType: this.form.reportType,
        fundCode: this.form.fundCode,
        fundCodes: this.form.fundCodes,
        weightProducts: this.form.weightProducts.map(item => ({
          fundCode: item.fundCode,
          fundName: item.fundName || this.getProductName(item.fundCode),
          weight: item.weight
        })),
        timeFrequency: this.form.timeFrequency,
        beginDate: this.form.dateRange[0],
        endDate: this.form.dateRange[1],
        benchmark: this.form.benchmark,
        watermarkType: this.watermarkType
      }
    },
    showExportDialog() {
      this.exportDialogVisible = true
    },
    handleExport() {
      this.$refs.queryForm.validate(valid => {
        if (!valid || !this.validateWeightProducts()) return
        this.exportDialogVisible = false
        this.$emit('export', this.getPayload())
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.report-query-wrapper {
  position: sticky;
  top: 0;
  z-index: 20;
  padding: 12px 10px 0;
  margin-bottom: 12px;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);

  .report-query-form {
    margin-bottom: 0;
  }

  .template-type-label {
    float: right;
    color: #8492a6;
    font-size: 12px;
    padding-left: 10px;
  }

  .report-type-input {
    width: 150px;
  }

  .weight-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
    color: #606266;
  }

  .weight-unit {
    margin-left: 6px;
    color: #606266;
  }
}
</style>
