<template>
  <div class="product-edit">
    <el-form ref="formEditQuery" class="standard-form" :inline="true" :rules="rules" :model="formEditQuery" label-width="100px">
      <el-row v-if="dialogStatus !== 'EDIT'" :gutter="20">
        <el-col :span="14">
          <el-form-item label="选择产品" prop="">
            <ProductSelectInput
              v-model="formEditQuery.product"
              placeholder="请选择产品"
              :input-width="'260px'"
              @select="handleProductSelect"
              @clear="handleProductClear"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="14">
          <el-form-item label="产品代码" prop="fundCode">
            <el-input v-model="formEditQuery.fundCode" :disabled="dialogStatus || isDisabledFundCode === true" placeholder="" size="small">
              <template slot="prepend">
                <span>ZR</span>
              </template>
            </el-input>
            <span>
<!--              <el-button v-if="dialogStatus !== 'EDIT'" plain type="info" size="small" @click="productSelectorVisible = true">选择产品</el-button>-->
              <el-button type="info" size="small" plain style="margin-left: 0" @click="deleteFundCode">清除</el-button>
            </span>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="产品名称" prop="fundName">
            <el-input v-model="formEditQuery.fundName" placeholder="请输入" size="small" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="14">
          <el-form-item label="规模（万元）">
            <el-input v-model="formEditQuery.amount" placeholder="请输入" size="small" />
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="管理人名称">
            <el-input v-model="formEditQuery.managerName" placeholder="请输入" size="small" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="14">
          <el-form-item label="策略类型">
            <el-select v-model="formEditQuery.strategy" placeholder="请选择" size="small" clearable>
              <el-option v-for="item in strategyTypeOptions" :key="item.DIM_CDE" :label="item.DIM_NME" :value="item.DIM_CDE" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="10">
          <el-form-item label="成立日期">
            <el-input v-model="formEditQuery.createDate" placeholder="请输入" size="small" :readonly="true" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col>
          <el-form-item label="备注">
            <el-input v-model="formEditQuery.remark" :rows="2" type="textarea" placeholder="请输入" size="small" style="width: 617px !important" />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row :gutter="20">
        <el-col :span="16" :offset="11">
          <el-button type="primary" size="small" @click="handleSaveFund('formEditQuery')">提 交</el-button>
        </el-col>
      </el-row>
    </el-form>
    <product-selector
      :dialog-visible="productSelectorVisible"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="wdgz"
      @closedialog="handleDialogClosed"
      @submitdialog="handleSubmitClick"
    ></product-selector>
  </div>
</template>
<script>
import productSelector from '@/components/productSelector'
import { saveNewFund } from '../scripts/api'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'ProductEdit',
  components: {
    productSelector,
    ProductSelectInput
  },
  props: {
    strategyTypeOptions: {
      type: Array,
      default: () => []
    },
    currentRow: {
      type: Object,
      default: () => {}
    },
    dialogStatus: {
      type: String,
      default: 'ADD'
    }
  },
  data() {
    const validateFundCode = (rule, value, callback) => {
      const regFundCode = /[^0-9A-Za-z-—_]/
      if (value === '') {
        callback(new Error('请输入产品代码'))
      } else if (regFundCode.test(value)) {
        callback(new Error('可输入6-20位代码，规范为数字/大小写字母/—/-/_'))
      } else if (value.length < 6 || value.length > 20) {
        callback(new Error('可输入6-20位代码'))
      } else {
        callback()
      }
    }
    return {
      formEditQuery: {
        product: null,
        fundCode: '',
        fundName: '',
        amount: '',
        managerName: '',
        createDate: '',
        strategy: '',
        remark: ''
      },
      rules: {
        fundCode: [{ validator: validateFundCode, trigger: 'change' }],
        fundName: [{ required: true, message: '请输入产品名称', trigger: 'change' }]
      },
      // 选择产品弹窗
      productSelectorVisible: false,
      treeData: [
        {
          label: '市场私募',
          id: 'scsm'
        },
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
      showTreeKeyArray: ['产品列表','私有产品','我的关注'],
      selectList: [],
      isDisabledFundCode: false,
      isPrefix: true
    }
  },
  watch: {
    currentRow: {
      handler(val) {
        if (val) {
          this.formEditQuery = Object.assign(this.formEditQuery, val)
        }
      },
      immediate: true
    }
  },
  methods: {
    triggerProductInputTooltip() {
      if (this.$refs.productSelectInput) {
        const inputEl = this.$refs.productSelectInput.$el;
        const mouseEnterEvent = new MouseEvent('mouseenter', {
          bubbles: true,
          cancelable: true,
          view: window
        });
        inputEl.dispatchEvent(mouseEnterEvent);
      }
    },
    handleSaveFund(formName) {
      try {
        this.$refs[formName].validate(async (valid) => {
          if (valid) {
            let params = {}
            if (this.dialogStatus === 'EDIT') {
              params = {
                ...this.formEditQuery,
                fundCode: this.currentRow.isPrefix ? 'ZR' + this.formEditQuery.fundCode : this.formEditQuery.fundCode
              }
            } else {
              params = {
                ...this.formEditQuery,
                fundCode: this.isPrefix ? 'ZR' + this.formEditQuery.fundCode : this.formEditQuery.fundCode
              }
            }
            const res = await saveNewFund(params)
            if (res.data.status === 0) {
              this.$message({
                type: 'success',
                message: '提交成功',
                customClass: 'message-success'
              })
              this.$emit('closeEdit', 'refesh')
            } else if (res.data.status === -2) {
              this.$message({
                type: 'warning',
                message: res.data.message || '该产品代码已提交，不可重复提交。',
                customClass: 'message-warning'
              })
            } else {
              this.$message({
                type: 'error',
                message: res.data.message || '提交失败',
                customClass: 'message-error'
              })
            }
          } else {
            this.$message({
              type: 'warning',
              message: '产品代码不规范请重新输入，代码规范位：可输入6-10位代码，规范为数字/大小写字母/—/-/_',
              customClass: 'message-warning'
            })
          }
        })
      } catch (e) {
        this.$message({
          type: 'error',
          message: '提交失败',
          customClass: 'message-error'
        })
      }
    },
    deleteFundCode() {
      if (this.dialogStatus === 'ADD') {
        this.formEditQuery.fundCode = ''
        this.formEditQuery.product = null
        this.isDisabledFundCode = false
        this.isPrefix = true
      } else {
        this.formEditQuery.amount = ''
        this.formEditQuery.managerName = ''
        this.formEditQuery.createDate = ''
        this.formEditQuery.strategy = ''
        this.formEditQuery.remark = ''
      }
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formEditQuery.fundCode = arr[0].VC_FUNDCODE || ''
      this.formEditQuery.fundName = arr[0].VC_FUNDNAME || ''
      this.formEditQuery.createDate = arr[0].D_CREATE_DATE || ''
      this.formEditQuery.managerName = arr[0].VC_NAME_GLR || ''
      this.isDisabledFundCode = true
      this.isPrefix = false
      this.selectList = arr
    },
    handleProductSelect: function(product) {
      this.formEditQuery.fundCode = product.VC_FUNDCODE || ''
      this.formEditQuery.fundName = product.VC_FUNDNAME || ''
      this.formEditQuery.createDate = product.D_CREATE_DATE || ''
      this.formEditQuery.managerName = product.VC_NAME_GLR || ''
      this.isDisabledFundCode = true
      this.isPrefix = false
    },
    handleProductClear: function() {
    },
  }
}
</script>
<style lang="scss" scoped>
.product-edit {
  .el-dialog__body {
    overflow: visible !important;
  }
  width: 100%;
  ::v-deep .el-form {
    width: 100% !important;
    .el-input-group__prepend {
      padding: 0 8px;
    }
  }
}
</style>
