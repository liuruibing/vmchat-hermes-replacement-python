<template>
  <div class="edit-product">
    <el-form ref="formData" class="standard-form" :model="formData" :rules="rules" label-width="120px">
      <el-row>
        <el-col :span="12" class="fund-code-col">
          <el-form-item label="产品代码" prop="fundCode">
            <div class="fund-code-input-wrap">
              <el-input
                v-model="formData.fundCode"
                placeholder="请输入产品代码"
                size="small"
                :disabled="isEdit"
              >
                <template v-if="!isEdit" slot="suffix">
                  <i
                    v-if="showFundCodeCheckLoading"
                    class="el-input__icon el-icon-loading"
                  />
                  <i
                    v-else-if="showFundCodeCheckOk"
                    class="el-input__icon el-icon-check fund-code-check-ok"
                  />
                </template>
              </el-input>
              <div v-if="showFundCodeDuplicateTip" class="fund-code-duplicate-tip">
                产品代码已存在
              </div>
            </div>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品名称" prop="fundName">
            <el-input v-model="formData.fundName" placeholder="请输入产品名称" size="small"></el-input>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="产品简称">
            <el-input v-model="formData.shortFundName" placeholder="请输入产品简称" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品管理人">
            <el-input v-model="formData.nameGlr" placeholder="请输入产品管理人" size="small"></el-input>
            <el-button
              size="small"
              icon="el-icon-edit"
              type="primary"
              @click="departmentVisible = true"
            ></el-button>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="投资经理">
            <el-input v-model="formData.fundManager" placeholder="请输入投资经理" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="成立日期" prop="createDate">
            <el-date-picker
              v-model="formData.createDate"
              type="date"
              placeholder="请选择成立日期"
              value-format="yyyy-MM-dd"
              size="small"
            />
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="策略类型" prop="investStrategy">
            <el-select
              v-model="formData.investStrategy"
              size="small"
              clearable
              filterable
              placeholder="请选择策略类型"
            >
              <el-option
                v-for="item in investOptions"
                :key="item.DIMCDE"
                :label="item.DIMNME"
                :value="item.DIMCDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="子策略类型" prop="typeDetail2">
            <el-select
              v-model="formData.typeDetail2"
              size="small"
              clearable
              filterable
              placeholder="请选择子策略类型"
            >
              <el-option
                v-for="item in investDetailOptions"
                :key="item.DIMCDE"
                :label="item.DIMNME"
                :value="item.DIMCDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="产品类型">
            <el-select
              v-model="formData.typeIn"
              size="small"
              clearable
              filterable
              placeholder="请选择产品类型"
            >
              <el-option
                v-for="item in typeInOptions"
                :key="item.DIMCDE"
                :label="item.DIMNME"
                :value="item.DIMCDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品明细类型" prop="typeDetail">
            <el-select
              v-model="formData.typeDetail"
              size="small"
              clearable
              filterable
              placeholder="请选择产品明细类型"
            >
              <el-option
                v-for="item in typeDetailOptions"
                :key="item.DIMCDE"
                :label="item.DIMNME"
                :value="item.DIMCDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="到期日">
            <el-date-picker
              v-model="formData.eDate"
              type="date"
              placeholder="请选择到期日"
              value-format="yyyy-MM-dd"
              size="small"
            />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="基准编码" prop="beCode">
            <el-select
              v-model="formData.beCode"
              size="small"
              clearable
              filterable
              placeholder="请选择基准编码"
            >
              <el-option
                v-for="item in beCodeOptions"
                :key="item.VC_BE_CODE"
                :label="item.VC_BE_NAME"
                :value="item.VC_BE_CODE"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="净值披露频率">
            <el-select
              v-model="formData.gzFrequency"
              size="small"
              clearable
              filterable
              placeholder="请选择净值披露频率"
            >
              <el-option
                v-for="item in gzFrequencyOptions"
                :key="item.value"
                :label="item.label"
                :value="item.value"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品运行状态">
            <el-select
              v-model="formData.ifClean"
              size="small"
              clearable
              filterable
              placeholder="请选择产品运行状态"
            >
              <el-option
                v-for="item in yxStatusOptions"
                :key="item.DIMCDE"
                :label="item.DIMNME"
                :value="item.DIMCDE"
              />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <div style="text-align: center" class="dialog-footer standard-form">
      <el-button size="small" type="primary" @click="handleSaveFund">
        提 交
      </el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>
    <department-component
      :department-visible="departmentVisible"
      :company-list="companyList"
      @dialogclose="handleCloseDialog"
      @submit="handleSubmit"
    ></department-component>
  </div>
</template>

<script>
import { gzFrequencyOptions } from '@/dataDictionary/frequency'
import { saveFund, checkFundCodeExists } from '../scripts/api'
import departmentComponent from '@/components/departmentComponent'
export default {
  name: 'editProduct',
  components: {
    departmentComponent
  },
  props: {
    curFundRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    yxStatusOptions: {
      default: Array,
      default: () => []
    },
    beCodeOptions: {
      default: Array,
      default: () => []
    },
    typeDetailOptions: {
      default: Array,
      default: () => []
    },
    typeInOptions: {
      default: Array,
      default: () => []
    },
    investOptions: {
      default: Array,
      default: () => []
    },
    investDetailOptions: {
      default: Array,
      default: () => []
    }
  },
  computed: {
    showFundCodeCheckLoading() {
      return (
        !this.isEdit &&
        this.fundCodeCheckStatus === 'checking' &&
        this.isFundCodeFormatValid(this.formData.fundCode)
      )
    },
    showFundCodeCheckOk() {
      return !this.isEdit && this.fundCodeCheckStatus === 'available'
    },
    showFundCodeDuplicateTip() {
      return !this.isEdit && this.fundCodeCheckStatus === 'duplicate'
    }
  },
  watch: {
    curFundRow: {
      handler(val) {
        if (val) {
          for (const key in this.formData) {
            this.formData[key] = val[key]
          }
        }
        this.resetFundCodeCheck()
      },
      deep: true,
      immediate: true
    },
    'formData.fundCode'(val) {
      if (this.isEdit) return
      this.scheduleFundCodeCheck(val)
    },
    isEdit(val) {
      if (val) this.resetFundCodeCheck()
    }
  },
  beforeDestroy() {
    if (this.fundCodeCheckTimer) {
      clearTimeout(this.fundCodeCheckTimer)
      this.fundCodeCheckTimer = null
    }
  },
  mounted() {
    // if (!this.isEdit) {
    //   // this.formData.nameGlr = this.$store.state.user.name
    // }
  },
  data() {
    const validateFundCode = (rule, value, callback) => {
      const regFundCode = /[^0-9A-Za-z-—_]/
      if (regFundCode.test(value)) {
        callback(new Error('规范为数字/大小写字母/—/-/_'))
      } else if (value.length < 6 || value.length > 10) {
        callback(new Error('可输入6-10位代码'))
      } else {
        callback()
      }
    }
    return {
      // 已选管理人
      companyList: [],
      // 管理人弹窗状态
      departmentVisible: false,
      // 净值披露频率下拉
      gzFrequencyOptions,
      userId: JSON.parse(localStorage.getItem('BAIDUID')).userId,
      /** idle | checking | available | duplicate | invalid */
      fundCodeCheckStatus: 'idle',
      fundCodeCheckTimer: null,
      lastCheckedFundCode: '',
      // form表单绑定
      formData: {
        fundCode: '',
        fundName: '',
        shortFundName: '',
        nameGlr: '',
        fundManager: '',
        createDate: '',
        investStrategy: '',
        typeDetail2: '',
        typeIn: '',
        typeDetail: '',
        eDate: '',
        beCode: '',
        gzFrequency: '',
        ifClean: ''
      },
      // 校验规则
      rules: {
        fundCode: [
          { required: true, message: '产品代码不能为空', trigger: 'blur' },
          { validator: validateFundCode, trigger: 'change' }
        ],
        fundName: [
          { required: true, message: '产品名称不能为空', trigger: 'blur' },
        ],
        investStrategy: [{ required: true, message: '策略类型不能为空', trigger: 'change' }],
        typeDetail2: [{ required: true, message: '子策略类型不能为空', trigger: 'change' }],
        typeDetail: [{ required: true, message: '产品类型明细不能为空', trigger: 'change' }],
        beCode: [{ required: true, message: '基准编码不能为空', trigger: 'change' }],
        createDate: [{ required: true, message: '成立日期不能为空', trigger: 'change' }],

      }
    }
  },
  methods: {
    isFundCodeFormatValid(value) {
      if (!value) return false
      const regFundCode = /[^0-9A-Za-z-—_]/
      if (regFundCode.test(value)) return false
      if (value.length < 6 || value.length > 10) return false
      return true
    },
    resetFundCodeCheck() {
      if (this.fundCodeCheckTimer) {
        clearTimeout(this.fundCodeCheckTimer)
        this.fundCodeCheckTimer = null
      }
      this.fundCodeCheckStatus = 'idle'
      this.lastCheckedFundCode = ''
    },
    scheduleFundCodeCheck(val) {
      if (this.fundCodeCheckTimer) {
        clearTimeout(this.fundCodeCheckTimer)
        this.fundCodeCheckTimer = null
      }
      if (!val) {
        this.fundCodeCheckStatus = 'idle'
        this.lastCheckedFundCode = ''
        return
      }
      if (!this.isFundCodeFormatValid(val)) {
        this.fundCodeCheckStatus = 'invalid'
        this.lastCheckedFundCode = ''
        return
      }
      this.fundCodeCheckStatus = 'checking'
      this.fundCodeCheckTimer = setTimeout(() => {
        this.fundCodeCheckTimer = null
        this.runFundCodeCheck(val)
      }, 400)
    },
    runFundCodeCheck(fundCode) {
      if (!fundCode || !this.isFundCodeFormatValid(fundCode)) {
        this.fundCodeCheckStatus = fundCode ? 'invalid' : 'idle'
        return Promise.resolve()
      }
      this.fundCodeCheckStatus = 'checking'
      return checkFundCodeExists({ fundCode })
        .then(res => {
          if (this.formData.fundCode !== fundCode) {
            this.scheduleFundCodeCheck(this.formData.fundCode)
            return
          }
          if (res.data.status !== 0) {
            this.fundCodeCheckStatus = 'idle'
            return
          }
          const exists = res.data.data === true
          this.lastCheckedFundCode = fundCode
          this.fundCodeCheckStatus = exists ? 'duplicate' : 'available'
        })
        .catch(() => {
          if (this.formData.fundCode === fundCode) {
            this.fundCodeCheckStatus = 'idle'
          } else {
            this.scheduleFundCodeCheck(this.formData.fundCode)
          }
        })
    },
    /**
     * @description 关闭管理人弹窗
     */
    handleCloseDialog() {
      this.departmentVisible = false
    },
    /**
     * @description 选择管理人
     */
    handleSubmit(arr) {
      this.companyList = arr
      this.formData.nameGlr = this.companyList.map(item => item.COMPANY_SHORT_NAME).toString()
    },
    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },
    /**
     * @description 保存产品
     */
    handleSaveFund() {
      this.$refs['formData'].validate(valid => {
        if (!valid) return false
        this.doSaveFund()
      })
    },
    async doSaveFund() {
      const code = this.formData.fundCode
      if (!this.isEdit) {
        if (this.fundCodeCheckStatus === 'duplicate') {
          this.$message.error('产品代码已存在')
          return
        }
        if (this.isFundCodeFormatValid(code)) {
          if (
            this.lastCheckedFundCode !== code ||
            this.fundCodeCheckStatus !== 'available'
          ) {
            await this.runFundCodeCheck(code)
            if (this.formData.fundCode !== code) return
            if (this.fundCodeCheckStatus === 'duplicate') {
              this.$message.error('产品代码已存在')
              return
            }
            if (this.fundCodeCheckStatus !== 'available') {
              this.$message.error('产品代码校验未完成，请稍后重试')
              return
            }
          }
        }
      }
      const params = Object.assign({}, this.formData)
      params.operation = this.isEdit ? 'update' : 'insert'
      try {
        const res = await saveFund(params)
        if (res.data.status === 0) {
          this.$message.success(res.data.message || '保存成功')
          this.$emit('closeDialog', 'REFESH')
        } else {
          this.$message.error(res.data.message || '保存失败')
        }
      } catch (e) {
        this.$message.error('保存失败')
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.fund-code-col {
  min-width: 0;
}
.fund-code-col ::v-deep .el-form-item__content {
  min-width: 0;
  max-width: 100%;
}
.fund-code-input-wrap {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
}
.fund-code-check-ok {
  color: #67c23a;
}
.fund-code-duplicate-tip {
  color: #f56c6c;
  font-size: 12px;
  line-height: 1.2;
  margin-top: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
