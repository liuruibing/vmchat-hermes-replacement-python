<template>
  <div class="edit-product">
    <el-form ref="formData" :model="formData" :rules="rules" class="standard-form" label-width="auto">
      <el-row>
        <el-col :span="12" class="fund-code-col">
          <el-form-item label="产品代码" prop="fundCode">
            <div class="fund-code-input-wrap">
              <el-input v-model="formData.fundCode" placeholder="请输入产品代码" size="small" :disabled="isEdit">
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
            <!--              <template v-if="!isEdit" slot="append">
                <span>{{ userId }}</span>
                &lt;!&ndash;                <el-button type="primary" size="small" @click="generate()" :disabled="isEdit">生成</el-button>&ndash;&gt;
              </template>-->
          </el-form-item>
        </el-col>
        <!--        <el-col :span="12">-->
        <!--          <el-form-item label="产品募集方式" prop="fundType">-->
        <!--            <el-select v-model="formData.fundType" size="small" clearable filterable placeholder="请选择产品募集方式">-->
        <!--              <el-option v-for="item in fundTypeinOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />-->
        <!--            </el-select>-->
        <!--          </el-form-item>-->
        <!--        </el-col>-->
        <el-col :span="12">
          <el-form-item label="产品名称" prop="fundName">
            <el-input v-model="formData.fundName" placeholder="请输入产品名称" size="small" :disabled="isEdit && formData.source != 'SY'"></el-input>
          </el-form-item>
        </el-col>
        </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="产品简称">
            <el-input v-model="formData.shortFundName" placeholder="请输入产品简称" size="small" :disabled="isEdit && formData.source != 'SY'"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品管理人">
            <el-input v-model="formData.nameGlr" disabled placeholder="请输入产品管理人" size="small" :disabled="isEdit && formData.source != 'SY'"></el-input>
            <el-button size="small" icon="el-icon-edit" type="primary" @click="departmentVisible = true" :disabled="isEdit && formData.source != 'SY'"></el-button>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品托管人">
            <el-input v-model="formData.nameTgr" placeholder="请输入产品托管人" size="small"></el-input>
            <el-button size="small" icon="el-icon-edit" type="primary" @click="departmentVisible2 = true"></el-button>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="外包服务机构">
            <el-input v-model="formData.nameOc" placeholder="请输入外包服务机构" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="投资经理">
            <el-input v-model="formData.fundManage" placeholder="请输入投资经理" size="small"></el-input>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="策略类型" prop="strategy">
            <el-select v-model="formData.strategy" size="small" clearable filterable placeholder="请选择策略类型" @change="handleChanges">
              <el-option v-for="item in investOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="子策略类型" prop="subStrategy">
            <el-select v-model="formData.subStrategy" size="small" clearable filterable placeholder="请选择子策略类型">
              <el-option v-for="item in investDetailOptionss" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="策略标签" :error="errorMessage">
            <el-input v-model="formData.strategyLabel" placeholder="请输入策略标签" size="small" @input="checkInputLength"></el-input>
            <!-- 显示提示信息的区域 -->
            <el-form-item v-if="errorMessage" class="error-message">
              <span slot="error">{{ errorMessage }}</span>
            </el-form-item>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="产品类型" prop="typeIn">
            <el-select v-model="formData.typeIn" size="small" clearable filterable placeholder="请选择产品类型">
              <el-option v-for="item in ftyPeinOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品明细类型" prop="typeDetail">
            <el-select v-model="formData.typeDetail" size="small" clearable filterable placeholder="请选择产品明细类型">
              <el-option v-for="item in typeDetailOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="成立日期" prop="createDate">
            <el-date-picker v-model="formData.createDate" type="date" placeholder="请选择成立日期" value-format="yyyy-MM-dd" size="small" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="到期日">
            <el-date-picker v-model="formData.eDate" type="date" placeholder="请选择到期日" value-format="yyyy-MM-dd" size="small" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="业务范围">
            <el-select v-model="formData.bizline" size="small" clearable filterable placeholder="请选择产品在广发证券的业务范围">
              <el-option v-for="item in bizlineArray" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="基准编码" prop="beCode">
            <el-select v-model="formData.beCode" size="small" clearable filterable placeholder="请选择基准编码">
              <el-option v-for="item in fundBase" :key="item.beCode" :label="item.beName" :value="item.beCode" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="是否广发代销">
            <el-select v-model="formData.isAgency" size="small" clearable filterable placeholder="请选择是否广发代销">
              <el-option v-for="item in isAgencyArray" :key="item.value" :label="item.label" :value="item.value" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="是否分级">
            <el-select v-model="formData.isTier" size="small" clearable filterable placeholder="请选择是否分级">
              <el-option v-for="item in isTierOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="产品运行状态">
            <el-select v-model="formData.runningState" size="small" clearable filterable placeholder="请选择产品运行状态">
              <el-option v-for="item in yxStatusOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="FOF投资" prop="fofInvestment">
            <el-select v-model="formData.fofInvestment" size="small" clearable filterable placeholder="请选择FOF投资">
              <el-option v-for="item in isTierOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="净值披露频率">
            <el-select v-model="formData.gzFrequency" size="small" clearable filterable placeholder="请选择净值披露频率">
              <el-option v-for="item in gzFrequencyOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="数据来源" prop="source">
            <el-select v-model="formData.source" size="small" clearable filterable disabled placeholder="请选择数据来源">
              <el-option v-for="item in sourceTypeOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="所属机构" prop="companyId">
            <el-select
              :disabled="isEdit || (isEdit === false && isManager === false)"
              v-model="formData.companyId"
              size="small"
              clearable
              filterable
              @change="handleChange"
              placeholder="请选择所属机构"
            >
              <el-option v-for="item in companyTypeOptionsSelf" :key="item.deptId" :label="item.deptName" :value="item.deptId" />
            </el-select>
          </el-form-item>
        </el-col>

        <el-col :span="12">
          <el-form-item label="产品属性">
            <el-select v-model="formData.starWishFlag" size="small" clearable filterable placeholder="请选择产品属性">
              <el-option v-for="item in starWishOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
        <!--        <el-col :span="12">-->
        <!--          <el-form-item label="外部基金" prop="isOuterFund">-->
        <!--            <el-select v-model="formData.isOuterFund" size="small" clearable filterable placeholder="请选择外部基金">-->
        <!--              <el-option v-for="item in isTierOptions" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde"/>-->
        <!--            </el-select>-->
        <!--          </el-form-item>-->
        <!--        </el-col>-->
      </el-row>
    </el-form>
    <div style="text-align: center" class="standard-form">
      <el-button size="small" type="primary" @click="handleSaveFund">提 交</el-button>
      <el-button size="small" type="info" plain @click="cancel">取 消</el-button>
    </div>
    <department-component :department-visible="departmentVisible" :company-list="companyList" @dialogclose="handleCloseDialog" @submit="handleSubmit"></department-component>

    <department-tgr-component
      :department-visible="departmentVisible2"
      :company-list="companyList2"
      @dialogclose="handleCloseDialog2"
      @submit="handleSubmit2"
    ></department-tgr-component>
  </div>
</template>

<script>
import { generateList, insertFund, updateFund, checkFundCodeExists } from '../scripts/api'
import departmentComponent from '@/components/departmentComponent'
import departmentTgrComponent from '@/components/departmentComponent/indexTgr'

export default {
  name: 'editProduct',
  components: {
    departmentComponent,
    departmentTgrComponent
  },
  props: {
    isManager: {
      type: Boolean,
      default: false
    },
    curFundRow: {
      type: Object,
      default: () => {}
    },
    isEdit: {
      type: Boolean,
      default: false
    },
    yxStatusOptions: {
      type: Array,
      default: () => []
    },
    fundBase: {
      type: Array,
      default: () => []
    },
    typeDetailOptions: {
      type: Array,
      default: () => []
    },
    sourceTypeOptions: {
      type: Array,
      default: () => []
    },
    gzFrequencyOptions: {
      type: Array,
      default: () => []
    },
    isTierOptions: {
      type: Array,
      default: () => []
    },
    ftyPeinOptions: {
      type: Array,
      default: () => []
    },
    companiesOptions: {
      type: Array,
      default: () => []
    },
    investOptions: {
      type: Array,
      default: () => []
    },
    fundTypeinOptions: {
      type: Array,
      default: () => []
    },
    investDetailOptions: {
      type: Array,
      default: () => []
    },
    starWishOptions: {
    type: Array,
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

          for (var i = 0; i < this.fundTypeinOptions.length; i++) {
            if (this.fundTypeinOptions[i].dimNme == val.fundType) {
              this.formData.fundType = this.fundTypeinOptions[i].dimCde
              break
            } else {
              this.formData.fundType = ''
            }
          }
          for (var i = 0; i < this.investOptions.length; i++) {
            if (this.investOptions[i].dimNme == val.strategy) {
              this.formData.strategy = this.investOptions[i].dimCde
              break
            } else {
              this.formData.strategy = ''
            }
          }
          this.handleChanges(this.formData.strategy)
          for (var i = 0; i < this.investDetailOptionss.length; i++) {
            if (this.investDetailOptionss[i].dimNme == val.subStrategy) {
              this.formData.subStrategy = this.investDetailOptionss[i].dimCde
              break
            } else {
              this.formData.subStrategy = ''
            }
          }
          for (var i = 0; i < this.ftyPeinOptions.length; i++) {
            if (this.ftyPeinOptions[i].dimNme == val.typeIn) {
              this.formData.typeIn = this.ftyPeinOptions[i].dimCde
              break
            } else {
              this.formData.typeIn = ''
            }
          }
          for (var i = 0; i < this.typeDetailOptions.length; i++) {
            if (this.typeDetailOptions[i].dimNme == val.typeDetail) {
              this.formData.typeDetail = this.typeDetailOptions[i].dimCde
              break
            } else {
              this.formData.typeDetail = ''
            }
          }
          if (val.isTier == '不分级') {
            this.formData.isTier = 0
          } else if (val.isTier == '分级') {
            this.formData.isTier = 1
          } else {
            this.formData.isTier = ''
          }
          for (var i = 0; i < this.yxStatusOptions.length; i++) {
            if (this.yxStatusOptions[i].dimNme == val.runningState) {
              this.formData.runningState = this.yxStatusOptions[i].dimCde
              break
            } else {
              this.formData.runningState = ''
            }
          }
          if (val.fofInvestment == '否') {
            this.formData.fofInvestment = 0
          } else if (val.fofInvestment == '是') {
            this.formData.fofInvestment = 1
          } else {
            this.formData.fofInvestment = ''
          }
          for (var i = 0; i < this.gzFrequencyOptions.length; i++) {
            if (this.gzFrequencyOptions[i].dimNme == val.gzFrequency) {
              this.formData.gzFrequency = this.gzFrequencyOptions[i].dimCde
              break
            } else {
              this.formData.gzFrequency = ''
            }
          }
          for (var i = 0; i < this.sourceTypeOptions.length; i++) {
            if (this.sourceTypeOptions[i].dimNme == val.source) {
              this.formData.source = this.sourceTypeOptions[i].dimCde
              break
            } else {
              this.formData.source = ''
            }
          }

          for (var i = 0; i < this.starWishOptions.length; i++) {
            if (this.starWishOptions[i].dimNme == val.starWishFlag) {
              this.formData.starWishFlag = this.starWishOptions[i].dimCde
              break
            } else {
              this.formData.starWishFlag = ''
            }
          }

          // for (var i = 0; i < this.companiesOptions.length; i++) {
          //   if (this.companiesOptions[i].deptName == val.companyName) {
          //     this.formData.companyId = this.companiesOptions[i].deptId
          //     this.formData.companyName = this.companiesOptions[i].deptName
          //     break
          //   } else {
          //     this.formData.companyName = ''
          //     this.formData.companyId = ''
          //   }
          // }

          // 判断是否是 管理人
          if (this.isEdit) {
            this.companyTypeOptionsSelf = this.companiesOptions
          } else {
            if (this.isManager) {
              this.companyTypeOptionsSelf = this.companiesOptions
            } else {
              // let userDeptId = this.$store.state.user.user.companyId
              let userDeptId = JSON.parse(localStorage.getItem('BAIDUID')).companyId
              let findObj = this.companiesOptions.find((item) => item.deptId == userDeptId)
              if (findObj) {
                this.formData.companyName = findObj.deptName
                this.formData.companyId = findObj.deptId
                this.companyTypeOptionsSelf = [
                  {
                    deptId: findObj.deptId,
                    deptName: findObj.deptName
                  }
                ]
              } else {
                this.companyTypeOptionsSelf = []
                this.formData.companyName = ''
                this.formData.companyId = ''
              }
            }
          }

          // if (val.isOuterFund == '否') {
          //   this.formData.isOuterFund = 0
          // } else if (val.isOuterFund == '是') {
          //   this.formData.isOuterFund = 1
          // } else {
          //   this.formData.isOuterFund = ''
          // }
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

      // 产品托管人已选信息
      companyList2: [],

      // 管理人弹窗状态
      departmentVisible: false,
      // 产品托管人已选信息
      departmentVisible2: false,

      userId: JSON.parse(localStorage.getItem('BAIDUID')).userId,
      /** idle | checking | available | duplicate | invalid */
      fundCodeCheckStatus: 'idle',
      fundCodeCheckTimer: null,
      lastCheckedFundCode: '',
      errorMessage: '',
      // form表单绑定
      formData: {
        fundCode: '',
        fundType: '',
        fundName: '',
        shortFundName: '',
        codeGlr: '',
        nameGlr: '',
        fundManage: '',
        strategy: '',
        subStrategy: '',
        strategyLabel: '',
        createDate: '',
        eDate: '',
        runningState: '',
        typeIn: '',
        typeDetail: '',
        isTier: '',
        source: '',
        gzFrequency: '',
        starWishFlag:'',
        fofInvestment: '',
        companyId: '',
        companyName: '',
        // isOuterFund: '',
        beCode: '',
        nameTgr: '',
        codeTgr: '',
        nameOc: '',
        bizline: '',
        isAgency: ''

      },
      investDetailOptionss: [],
      // 校验规则
      rules: {
        fundCode: [
          { required: true, message: '产品代码不能为空', trigger: 'blur' },
          { validator: validateFundCode, trigger: 'change' }
        ],
        // fundType: [{ required: true, message: '产品募集方式不能为空', trigger: 'blur' }],
        // strategy: [{ required: true, message: '策略类型不能为空', trigger: 'change' }],
        beCode: [{ required: true, message: '基准编码不能为空', trigger: 'change' }],
        // subStrategy: [{ required: true, message: '子策略类型不能为空', trigger: 'change' }],
        // typeDetail: [{ required: true, message: '产品类型明细不能为空', trigger: 'change' }],
        source: [{ required: true, message: '数据来源不能为空', trigger: 'change' }],
        createDate: [{ required: true, message: '成立日期不能为空', trigger: 'change' }],
        // companyId: [{ required: true, message: '所属机构不能为空', trigger: 'change' }]
        // isOuterFund: [{required: true, message: '外部基金不能为空', trigger: 'change'}]
      },
      isAgencyArray: [
        {
          label: '否',
          value: '0'
        },
        {
          label: '是',
          value: '1'
        }
      ],
      bizlineArray: [
        {
          label: '托管外包',
          value: '1'
        },
        {
          label: '外包',
          value: '2'
        }
      ],
      companyTypeOptionsSelf: []
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
    checkInputLength() {
      // 检查输入长度
      if (this.formData.strategyLabel.length > 20) {
        this.formData.strategyLabel = this.formData.strategyLabel.substring(0, 20)
        this.errorMessage = '策略标签不能超过20个字符'
      } else {
        this.errorMessage = '' // 清除错误信息
      }
    },
    /**
     * @description 关闭管理人弹窗
     */
    handleCloseDialog() {
      this.departmentVisible = false
    },

    /**
     * @description 关闭产品托管人弹窗
     */
    handleCloseDialog2() {
      this.departmentVisible2 = false
    },

    /**
     * @description 选择管理人
     */
    handleSubmit(arr) {
      this.companyList = arr
      // this.formData.nameGlr = this.companyList.map((item) => item.managerName).toString()
      // this.formData.codeGlr = this.companyList.map((item) => item.managerCode).toString()
      this.formData.nameGlr = this.companyList.map((item) => item.COMPANY_NAME).toString()
      this.formData.codeGlr = this.companyList.map((item) => item.COMPANY_ID).toString()
    },

    /**
     * @description 选择产品托管人
     */
    handleSubmit2(arr) {
      this.companyList2 = arr
      // this.formData.nameGlr = this.companyList.map((item) => item.managerName).toString()
      // this.formData.codeGlr = this.companyList.map((item) => item.managerCode).toString()
      this.formData.nameTgr = this.companyList2.map((item) => item.COMPANY_NAME).toString()
      this.formData.codeTgr = this.companyList2.map((item) => item.COMPANY_ID).toString()
    },

    /**
     * @description 取消按钮关闭弹窗
     */
    cancel() {
      this.$emit('closeDialog', 'NO_REFESH')
    },
    /**
     *生成产品代码
     */
    generate() {
      const data = {}
      generateList(data).then((res) => {
        console.log('查看数据')
        console.log(res.data.data.fundCode)
        if (res.data.status === 0) {
          this.formData.fundCode = res.data.data.fundCode
        }
      })
    },
    //监听策略类型
    handleChanges(value) {
      this.formData.subStrategy = ''
      this.investDetailOptionss = this.investDetailOptions.filter((item) => item.dimEdit === value)
    },
    //监听所属机构
    handleChange(value) {
      for (var i = 0; i < this.companiesOptions.length; i++) {
        if (this.companiesOptions[i].deptId == value) {
          this.formData.companyId = this.companiesOptions[i].deptId
          this.formData.companyName = this.companiesOptions[i].deptName
        }
      }
      console.log(value) // 这将包含你选择的整个对象，包括 deptId 和 deptName
    },
    /**
     * @description 保存产品
     */
    handleSaveFund() {
      this.$refs['formData'].validate((valid) => {
        if (!valid) return false
        this.doSaveFund()
      })
    },
    async doSaveFund() {
      const code = this.formData.fundCode
      if (!this.isEdit) {
        if (this.fundCodeCheckStatus === 'duplicate') {
          this.$message({
            type: 'error',
            message: '产品代码已存在',
            customClass: 'message-error'
          })
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
              this.$message({
                type: 'error',
                message: '产品代码已存在',
                customClass: 'message-error'
              })
              return
            }
            if (this.fundCodeCheckStatus !== 'available') {
              this.$message({
                type: 'error',
                message: '产品代码校验未完成，请稍后重试',
                customClass: 'message-error'
              })
              return
            }
          }
        }
      }
      const params = Object.assign({}, this.formData)
      params.operation = this.isEdit ? 'update' : 'insert'
      try {
        if (params.operation == 'insert') {
          const res = await insertFund(params)
          const { message } = res.data
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: '保存成功',
              customClass: 'message-success'
            })
            this.$emit('closeDialog', 'REFESH')
          } else {
            this.$message({
              type: 'error',
              message: message || '保存失败',
              customClass: 'message-error'
            })
          }
        } else if (params.operation == 'update') {
          const res = await updateFund(params)
          const { message } = res.data
          if (res.data.status === 0) {
            this.$message({
              type: 'success',
              message: '保存成功',
              customClass: 'message-success'
            })
            this.$emit('closeDialog', 'REFESH')
          } else {
            this.$message({
              type: 'error',
              message: message || '保存失败',
              customClass: 'message-error'
            })
          }
        }
      } catch (e) {
        this.$message({
          type: 'error',
          message: '保存失败',
          customClass: 'message-error'
        })
      }
    }
  }
}
</script>

<style lang="scss" scoped>
/* flex 子列默认 min-width:auto，错误提示出现后左侧列变宽会把同排/下一排字段挤偏 */
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
