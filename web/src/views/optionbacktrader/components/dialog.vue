<template>
  <el-dialog :title="title" :visible.sync="dialogVisible" :close-on-click-modal="false" custom-class="backtrader-dialog"  @close="handleClose" >
    <div style="padding: 0px 10px; height: 100%;max-height: 65vh; overflow-y: auto;">
      <el-form ref="editForm" :model="form" :rules="formRules" size="small" :disabled="mode === 'view'"
        label-position="right" label-width="166px">
        <el-row>
          <el-col :span="24">
            <el-form-item label="方案名称" prop="programmeName">
              <el-input v-model="form.programmeName" placeholder="请输入方案名称" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">产品信息参数</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <div  v-if="mode !== 'view'" >
            <el-form-item label="产品代码" prop="fundName" class="fund-select-form-item">
              <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
                <el-input v-model="formInline.fundName" clearable @keydown.native.prevent @paste.native.prevent :style="{cursor: 'pointer'}"
                          @clear="handleClearProduct" placeholder="请选择产品" size="small" @click.native="showFloatSelector" @mouseenter.native="showFloatSelector" @blur.native="handleInputBlur"  />
              </el-tooltip>

              <ProductFloatSelector
                ref="productFloatSelector"
                :visible="floatSelectorVisible"
                :route-path="$route.path"
                @select-product="handleSubmitClick"
                @hide-selector="hideFloatSelector"
                @mouseenter.native="handleSelectorMouseEnter"
                @mouseleave.native="handleSelectorMouseLeave"
              />
            </el-form-item>
            </div>
            <div  v-if="mode === 'view'" >
              <el-form-item label="产品代码" prop="fundName" class="fund-select-form-item">
                <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
                  <el-input v-model="formInline.fundName" clearable @keydown.native.prevent @paste.native.prevent :style="{cursor: 'pointer'}"/>
                </el-tooltip>
              </el-form-item>
            </div>
<!--            <el-form-item label="产品代码" prop="fundCode">-->
<!--              <el-select-->
<!--                ref="selectRef"-->
<!--                v-model="form.fundCode"-->
<!--                placeholder="请选择产品"-->
<!--                style="width: 100%;"-->
<!--                remote-->
<!--                :loading="fundLoading"-->
<!--                :remote-method="searchFundRemote"-->
<!--                filterable-->
<!--                clearable-->
<!--                popper-class="product-fund-select-dropdown"-->
<!--                @visible-change="handleFundVisibleChange"-->
<!--                @change="handleFundChange"-->
<!--              >-->
<!--                <el-option-->
<!--                  v-for="item in fundList"-->
<!--                  :key="item.VC_FUNDCODE"-->
<!--                  :label="item.VC_FUNDNAME"-->
<!--                  :value="item.VC_FUNDCODE"-->
<!--                />-->
<!--              </el-select>-->
<!--            </el-form-item>-->
          </el-col>
          <el-col :span="12">
            <el-form-item label="基准指数代码" prop="indexCode">
              <el-select v-model="form.indexCode" placeholder="请选择基准指数" filterable style="width: 100%">
                <el-option v-for="item in selectOptions.benchIndexList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">回测基本参数</el-divider>
        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item label="运行区间" prop="runPeriodStart">
              <el-date-picker v-model="form.runPeriodStart" type="date" placeholder="开始日期" value-format="yyyy-MM-dd"
                style="width: 45%" />
              <span style="margin: 0 5px;">-</span>
              <el-date-picker v-model="form.runPeriodEnd" type="date" placeholder="结束日期" value-format="yyyy-MM-dd"
                style="width: 45%" />
            </el-form-item>
          </el-col>
          <el-col :span="24">
            <el-form-item label="优化区间" prop="optimizePeriodStart">
              <el-date-picker v-model="form.optimizePeriodStart" type="date" placeholder="开始日期"
                value-format="yyyy-MM-dd" style="width: 45%" />
              <span style="margin: 0 5px;">-</span>
              <el-date-picker v-model="form.optimizePeriodEnd" type="date" placeholder="结束日期" value-format="yyyy-MM-dd"
                style="width: 45%" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">对冲类型分类</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="策略类型" prop="hedgeStrategy">
              <el-select v-model="form.hedgeStrategy" placeholder="请选择策略类型" style="width: 100%"
                @change="handleHedgeStrategyChange">
                <el-option v-for="item in selectOptions.hedgeStrategyList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="对冲类型" prop="hedgeType">
              <el-select v-model="form.hedgeType" placeholder="请选择对冲类型" style="width: 100%">
                <el-option v-for="item in selectOptions.hedgeTypeList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">再平衡方法分类</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="再平衡策略" prop="reBalanceType">
              <el-select v-model="form.reBalanceType" placeholder="请选择再平衡策略" style="width: 100%"
                @change="handleReBalanceTypeChange">
                <el-option v-for="item in selectOptions.reBalanceTypeList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12" v-show="showCalendarFreq">
            <el-form-item label="日历对冲频率">
              <el-select v-model="form.calendarFreq" placeholder="请选择日历对冲频率" style="width: 100%">
                <el-option v-for="item in selectOptions.calendarFreqList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="个股BETA因子周期">
              <el-select v-model="form.betaWindow" placeholder="请选择BETA周期" style="width: 100%">
                <el-option v-for="item in selectOptions.betaWindowList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">

            <el-form-item label="不完全对冲敞口(%)">

              <el-input-number v-model="form.unHedgeTarget" :min="0" :max="100" :precision="2" controls-position="right" style="width: 160px;">
              </el-input-number>

            </el-form-item>


          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="动态对冲敞口阈值(%)">
              <el-input-number v-model="form.unHedgeExposureThreshold" :min="0" :max="100" :precision="2"
                controls-position="right" style="width: 160px;" />
            </el-form-item>
          </el-col>
          <el-col :span="12" v-show="showCoverageRatio">
            <el-form-item label="覆盖比例(%)">
              <el-input-number v-model="form.coverageRatio" :min="0" :max="100" :precision="2" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20" v-show="showCoverageRatio">
          <el-col :span="12">
            <el-form-item label="近一年成交量阈值(%)">
              <el-input-number v-model="form.tradeAmountOneYearRatio" :min="0" :max="100" :precision="2"
                controls-position="right" style="width: 160px;" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">交易参数</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="交易标的" prop="tradeTool">
              <el-select v-model="form.tradeTool" placeholder="请选择交易标的" style="width: 100%">
                <el-option v-for="item in selectOptions.tradeToolList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="交易合约价格档位" prop="tradeContract">
              <el-select v-model="form.tradeContract" placeholder="请选择交易合约价格档位" style="width: 100%">
                <el-option v-for="item in selectOptions.tradeContractList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="交易合约剩余交易日期(天)" prop="tradeContractDuration">
              <el-input-number v-model="form.tradeContractDuration" :min="0" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="交易时点" prop="tradeTime">
              <el-select v-model="form.tradeTime" placeholder="请选择交易时点" style="width: 100%">
                <el-option v-for="item in selectOptions.tradeTimeList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="交易费用(元)" prop="tradeCost">
              <el-input-number v-model="form.tradeCost" :min="0" :precision="2" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到期提前移仓(天)" prop="futureTransfer">
              <el-input-number v-model="form.futureTransfer" :min="0" controls-position="right" style="width: 160px;" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-divider content-position="left">持仓假设</el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="现金比例(%)">
              <el-input-number v-model="form.cashAssume" :min="0" :max="100" :precision="2" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="保证金占用现金比例(%)">
              <el-input-number v-model="form.marginAssume" :min="0" :max="100" :precision="2" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="保证金可追加比例(%)">
              <el-input-number v-model="form.marginCallMax" :min="0" :max="100" :precision="2" controls-position="right"
                style="width: 160px;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="产品规模假设">
              <el-select v-model="form.assetValueAssume" placeholder="请选择" style="width: 100%">
                <el-option v-for="item in selectOptions.assetValueAssumeList" :key="item.dimCde" :label="item.dimNme"
                  :value="item.dimCde" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <div slot="footer" v-if="mode !== 'view'" style="text-align: center;">
        <el-button size="small" @click="handleClose">取 消</el-button>
        <el-button type="primary" size="small" :loading="loading" @click="handleSubmit">保 存</el-button>
      </div>
    </div>

  </el-dialog>
</template>

<script>
import commonApi from '@/api/common'
import pageApi from '../scripts/api'
import ProductFloatSelector from '@/components/productSelector/ProductFloatSelector'
const DEFAULT_FORM = {
  fid: '',
  programmeName: '',
  fundCode: '',
  fundName: '',
  indexCode: '',
  runPeriodStart: '',
  runPeriodEnd: '',
  optimizePeriodStart: '',
  optimizePeriodEnd: '',
  hedgeStrategy: '',
  hedgeType: '',
  reBalanceType: '',
  calendarFreq: '',
  betaWindow: '',
  unHedgeTarget: 5,
  unHedgeExposureThreshold: 20,
  coverageRatio: 50,
  tradeTool: '',
  tradeContract: '',
  tradeContractDuration: 10,
  tradeTime: '',
  tradeCost: 15,
  futureTransfer: 2,
  tradeAmountOneYearRatio: 10,
  cashAssume: 10,
  marginAssume: 50,
  marginCallMax: 30,
  assetValueAssume: ''
}

const EMPTY_SELECT_OPTIONS = () => ({
  benchIndexList: [],
  hedgeStrategyList: [],
  hedgeTypeList: [],
  reBalanceTypeList: [],
  calendarFreqList: [],
  betaWindowList: [],
  tradeToolList: [],
  tradeContractList: [],
  tradeTimeList: [],
  assetValueAssumeList: []
})

const TITLE_MAP = {
  add: '新增策略回测方案',
  edit: '修改策略回测方案',
  copy: '复制策略回测方案',
  view: '查看策略回测方案'
}

export default {
  name: 'BacktraderDialog',
  components: {ProductFloatSelector},
  props: {
    mode: {
      type: String,
      default: () => ("add")
    },
    row: {
      type: Object,
      default: null
    }
  },
  data() {
    return {

      floatSelectorVisible: false,
      isHoveringSelector: false,
      //========
      isShowMoreQuery: false,
      // 选择产品弹窗
      productSelectorVisible: false,
      left: false,
      selectList: [],
      dialogMask: false,

      formInline: {
        fundCode: '',
        fundName: ''
      },

      form: { ...DEFAULT_FORM },
      loading: false,
      selectOptions: EMPTY_SELECT_OPTIONS(),
      fundList: [],
      fundLoading: false,
      fundAppendLoading: false,
      fundPageNum: 1,
      fundPageSize: 10,
      fundKeyword: '',
      fundHasMore: true,
      fundScrollWrap: null,
      formRules: {
        programmeName: [{ required: true, message: '方案名称不能为空', trigger: 'blur' }],
        fundCode: [{ required: true, message: '产品代码不能为空', trigger: 'change' }],
        indexCode: [{ required: true, message: '基准指数代码不能为空', trigger: 'change' }],
        runPeriodStart: [{ required: true, message: '运行开始日期不能为空', trigger: 'change' }],
        runPeriodEnd: [{ required: true, message: '运行结束日期不能为空', trigger: 'change' }],
        optimizePeriodStart: [{ required: true, message: '优化开始日期不能为空', trigger: 'change' }],
        optimizePeriodEnd: [{ required: true, message: '优化结束日期不能为空', trigger: 'change' }],
        hedgeStrategy: [{ required: true, message: '策略类型不能为空', trigger: 'change' }],
        hedgeType: [{ required: true, message: '对冲类型不能为空', trigger: 'change' }],
        reBalanceType: [{ required: true, message: '再平衡策略不能为空', trigger: 'change' }],
        tradeTool: [{ required: true, message: '交易标的不能为空', trigger: 'change' }],
        tradeContract: [{ required: true, message: '交易合约价格档位不能为空', trigger: 'change' }],
        tradeContractDuration: [{ required: true, message: '交易合约剩余交易日期不能为空', trigger: 'blur' }],
        tradeTime: [{ required: true, message: '交易时点不能为空', trigger: 'change' }],
        tradeCost: [{ required: true, message: '交易费用不能为空', trigger: 'blur' }],
        futureTransfer: [{ required: true, message: '到期提前移仓不能为空', trigger: 'blur' }]
      },
      dialogVisible: true
    }
  },
  computed: {
    title() {
      return TITLE_MAP[this.mode] || ''
    },
    showCalendarFreq() {
      return this.form.reBalanceType === 'CALENDAR_HEDGE'
    },
    showCoverageRatio() {
      return this.form.hedgeStrategy === 'COVERED'
    }
  },
  mounted() {
    this.initForm()
    this.loadSelectOptions()
    //this.searchFund(this.form.fundCode, false)
  },
  methods: {

    handleClearProduct() {
      this.formInline.fundCode = '';
      this.formInline.fundName = '';
      this.timDate = '';
      this.selectList = [];
      this.form.fundCode='';

    },
    // 显示悬浮框
    showFloatSelector() {
      this.floatSelectorVisible = true;
      // 重置悬浮框悬浮标记
      this.isHoveringSelector = false;
    },

    // 隐藏悬浮框
    hideFloatSelector() {
      this.floatSelectorVisible = false;
      this.isHoveringSelector = false;
    },

    // 鼠标移入悬浮框，标记
    handleSelectorMouseEnter() {
      this.isHoveringSelector = true;
    },
    // 鼠标移出悬浮框，关闭并重置标记
    handleSelectorMouseLeave() {
      const isHoveringDropdown = document.querySelector('.el-select-dropdown:hover');
      const isHoveringTooltip = document.querySelector('.el-tooltip__popper:hover');
      const isHoveringSelector = this.$refs.floatContainer && document.querySelector('.product-float-selector:hover');

      if (isHoveringDropdown || isHoveringTooltip || isHoveringSelector) {
        return;
      }
      this.isHoveringSelector = false;
      this.floatSelectorVisible = false;
    },
    handleSubmitClick(arr) {
      this.dialogMask = false
      //this.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.selectList = arr
      this.form.fundCode=arr[0].VC_FUNDCODE || ''
      // 隐藏悬浮框
      this.floatSelectorVisible = false
    },


    handleFundVisibleChange(visible) {
      if (visible) {
        this.$nextTick(() => {
          setTimeout(() => this.attachFundScrollListener(), 100)
        })
      } else {
        this.removeFundScrollListener()
      }
    },
    attachFundScrollListener() {
      const wrap = document.querySelector('.product-fund-select-dropdown .el-select-dropdown__wrap')
      if (wrap && !this.fundScrollWrap) {
        this.fundScrollWrap = wrap
        wrap.addEventListener('scroll', this.onFundDropdownScroll)
      }
    },
    removeFundScrollListener() {
      if (this.fundScrollWrap) {
        this.fundScrollWrap.removeEventListener('scroll', this.onFundDropdownScroll)
        this.fundScrollWrap = null
      }
    },
    onFundDropdownScroll(e) {
      const { scrollTop, clientHeight, scrollHeight } = e.target
      if (scrollTop + clientHeight >= scrollHeight - 30 && this.fundHasMore && !this.fundLoading && !this.fundAppendLoading) {
        this.loadMoreFund()
      }
    },
    /** remote-method：用户输入时触发，重置分页并搜索 */
    searchFundRemote(query) {
      this.fundKeyword = query || ''
      this.fundPageNum = 1
      this.fundHasMore = true
      this.searchFund(this.fundKeyword, false)
    },
    /** 滚动到底部时加载下一页 */
    loadMoreFund() {
      if (!this.fundHasMore || this.fundLoading || this.fundAppendLoading) return
      this.searchFund(this.fundKeyword, true)
    },
    handleFundChange(val) {
      const item = this.fundList.find((f) => f.VC_FUNDCODE === val)
      if (item) this.form.fundName = item.VC_FUNDNAME
    },
    initForm() {
      console.log(this.row)
      if (this.mode === 'add' || !this.row) {
        this.form = { ...DEFAULT_FORM }
      } else {
        this.form = this.row
        this.formInline.fundCode = this.row.fundCode || ''
        this.formInline.fundName = this.row.fundName || ''

        if(this.form.tradeContract && typeof this.form.tradeContract === 'number'){
          this.form.tradeContract = this.form.tradeContract+""
        }
      }
    },
    async loadSelectOptions() {
      const res = await pageApi.selectAllOptions()
      const data = res.data || res
      if (data) this.selectOptions = data
    },
    /**
     * 分页查询产品列表
     * @param {string} query - 搜索关键字（用户输入或空）
     * @param {boolean} append - true 表示加载下一页并追加，false 表示从第一页重新加载
     */
    async searchFund(query, append) {
      if (append) {
        if (this.fundAppendLoading || !this.fundHasMore) return
        this.fundAppendLoading = true
      } else {
        if (this.fundLoading) return
        this.fundLoading = true
      }
      if (!append) {
        this.fundPageNum = 1
      }
      const pageNum = append ? this.fundPageNum : 1
      const params = {
        userInput: query || '',
        indexCode: '32aad2ac-edf2-4a05-86a2-75b78aa2ba64',
        flag: 'B',
        _pageFlag: true,
        _pageNum: pageNum,
        _pageSize: this.fundPageSize
      }
      try {
        const response = await commonApi.getDataBysqlCode(params)
        if (response.data && response.data.status === 0) {
          const rows = response.data.data.rows || []
          if (append) {
            this.fundList = [...this.fundList, ...rows]
            this.fundPageNum += 1
          } else {
            this.fundList = rows
            this.fundPageNum = 2
          }
          this.fundHasMore = rows.length >= this.fundPageSize
        } else {
          if (!append) this.fundList = []
          this.fundHasMore = false
          if (!append) this.$message.warning('产品数据加载失败')
        }
      } catch (e) {
        if (!append) this.fundList = []
        this.fundHasMore = false
        if (!append) this.$message.warning('产品数据加载失败')
      } finally {
        if (append) {
          this.fundAppendLoading = false
        } else {
          this.fundLoading = false
        }
      }
    },
    handleClose() {
      this.$emit('closeDialog')
    },
    async handleSubmit() {
      this.$refs.editForm.validate(async (valid) => {
        if (!valid) return
        this.loading = true

        try {
          let res = null;
          if (this.mode === 'add') {
            res = await pageApi.addBackTrader(this.form)
          } else if (this.mode === 'edit') {
            res = await pageApi.editBackTrader(this.form)
          } else if (this.mode === 'copy') {
            res = await pageApi.copyBackTrader(this.form)
          }
          // console.log('接口返回：', res)
          if (res.data.resultCode ==='1') {
            this.$message.success('保存成功')
            this.$emit('saveSuccess')
            this.$emit('closeDialog', 'REFESH')
          } else {
            this.$message.error('保存失败，请重试')
          }
        } catch (err) {
          this.$message.error('保存失败，请重试')
        } finally {
          this.loading = false
        }
      })
    },
    handleHedgeStrategyChange(val) {
      if (val === 'PP') {
        this.form.coverageRatio = 0
        this.form.tradeAmountOneYearRatio = 0
      }
    },
    handleReBalanceTypeChange() { },
  }
}
</script>

<style lang="scss" scoped>
::v-deep .backtrader-dialog {
  width: 1090px !important;

  .el-dialog__body {
    padding: 10px 20px;
  }

  .el-divider__text {
    color: red;
    font-weight: bold;
    font-size: 15px;
  }

  .el-form-item {
    margin-bottom: 12px;
  }
}

::v-deep .el-dialog .el-form {
  width: 100% !important;
}



</style>
