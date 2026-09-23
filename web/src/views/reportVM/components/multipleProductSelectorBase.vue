<template>
  <div style="height: 100%">
    <div class="standard-form-margin">
      <div class="inner-margin">
        <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="standard-form">
          <el-row>
            <el-form-item label="产品" prop="fundName">
<!--              <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" class="item" effect="dark" placement="top-start">
                <el-input v-model="formInline.fundName" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" />
              </el-tooltip>-->
              <ProductSelectInputMultiple
                v-model="selectedProducts"
                placeholder="请选择产品"
                :input-width="'260px'"
                @select="handleProductSelect"
                @clear="handleProductClear"
              />
            </el-form-item>
            <el-form-item label="开始日期" prop="beginDate">
              <el-date-picker v-model="formInline.beginDate" :picker-options="dateShortTPCTA()" size="small" placeholder="选择开始日期" type="date" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item label="结束日期" prop="endDate">
              <el-date-picker v-model="formInline.endDate" placeholder="选择结束日期" type="date" size="small" value-format="yyyy-MM-dd" />
            </el-form-item>
            <el-form-item>
              <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary" @click="onSubmit('formInline')">{{onSub}}</el-button>
              <el-button type="info" plain icon="el-icon-refresh-left" size="small" @click="resetForm('formInline')">重置</el-button>
              <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2" @click="fun_export_PDF" size="small">
                {{ exportText2 }}
              </el-button>
            </el-form-item>
            <el-form-item>
              <!-- <div style="color: red;">拥有此产品：{{ fundGrant }}权限，报告仅显示有权限模块。</div> -->
            </el-form-item>
          </el-row>
          <el-row style="margin-top: 10px">
            <el-col :span="24">
              <div style="display: inline-block">
                <el-form-item label="基准类型">
                  <el-select v-model="formInline.ZB_INDEXTYPE" placeholder="请选择" size="small">
                    <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == 'djz'" style="display: inline-block">
                <el-form-item label="选择基准">
                  <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == 'fhjz'" style="display: inline-block">
                <el-form-item label="基准 A">
                  <el-select v-model="formInline.ZB_INDEXCODEA" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="比例">
                  <el-input v-model="formInline.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important" @blur="handleInputWeight('A')"></el-input>
                  %
                </el-form-item>
              </div>
              <div v-show="formInline.ZB_INDEXTYPE == 'fhjz'" style="display: inline-block">
                <el-form-item label="基准 B">
                  <el-select v-model="formInline.ZB_INDEXCODEB" placeholder="请选择" size="small">
                    <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label" :value="item.id"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="比例">
                  <el-input v-model="formInline.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important" @blur="handleInputWeight('B')"></el-input>
                  %
                </el-form-item>
              </div>
            </el-col>
          </el-row>
        </el-form>
      </div>
    </div>
    <product-selector
      v-if="dialogMask"
      :multiple="true"
      :leftList="false"
      :dialog-visible="dialogMask"
      :limit="5"
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
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import productSelector from '@/components/productSelector'
import FundListDialog from '@/components/FundListDialog/ZjzqDialog'
import { getToken } from '@/utils/auth'
import request from '@/utils/request'
import moment from 'moment'
import store from "../../../store";
// 引入多选悬浮框组件
import ProductSelectInputMultiple from '@/components/productSelector/ProductSelectInputMultiple'

export default {
  name: '',
  components: {
    FundListDialog,
    iframeModule,
    productSelector,
    ProductSelectInputMultiple
  },
  props: {
    templateCode: {
      type: String,
      default: ''
    },
    reportType: {
      type: String,
      default: ''
    },
    templateName: {
      type: String,
      default: ''
    }
  },
  data() {
    const validateDate = (rule, value, callback) => {
      if (value === null || value.length === 0) {
        callback(new Error('请选择日期'))
      } else if (!this.$validate.validateThreeYears(value)) {
        callback(new Error('选择日期区间大于三年'))
      } else {
        callback()
      }
    }
    const validatebeginDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择开始日期'))
      } else {
        if (this.formInline.endDate !== null || this.formInline.endDate !== undefined || this.formInline.endDate !== '') {
          const startTime = new Date(value)
          const endTime = new Date(this.formInline.endDate)
          if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    const validateEndDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择结束日期'))
      } else {
        if (this.formInline.beginDate !== null || this.formInline.beginDate !== undefined || this.formInline.beginDate !== '') {
          const startTime = new Date(this.formInline.beginDate)
          const endTime = new Date(value)
          if (startTime > endTime) {
            callback(new Error('结束日期不能小于开始日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
      }
    }
    return {
      selectedProducts: [],
      // 选择产品弹窗
      productSelectorVisible: false,

      selectList: [],
      zhezhao: false,
      dialogMask: false,
      pickerOptions: {},
      productCheckArr: [],
      companyCheckArr: [],
      fundArray: [],
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '管理人旗下产品',
          id: 'glrqxcp'
        },
        {
          label: '私有产品',
          id: 'sycp'
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
      showTreeKeyArray: ['产品列表', '私有产品', '我的关注'],
      // 搜索
      formInline: {
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'djz', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000' // 基准B权重
      },
      ZB_INDEXTYPEOption: [
        {
          id: 'djz',
          label: '单基准'
        },
        {
          id: 'fhjz',
          label: '复合基准'
        }
      ],
      datumOption: [],
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        //ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        beginDate: [
          { required: true, message: '请选择开始日期', trigger: 'blur' },
          { validator: validatebeginDate, trigger: 'blur' }
        ],
        endDate: [
          { required: true, message: '请选择结束日期', trigger: 'blur' },
          { validator: validateEndDate, trigger: 'blur' }
        ],
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }]
      },
      issearchFxButton: false,
      fundCode: '', // code值
      fundName: '', // name
      noData: '--', // 没有数据
      iframeData: {
        // iframe链接
        src: ''
      },
      //成立日
      timDate: '',
      //开关
      offOn: false,
      name: 'iframeVue_reportZJZJFX',
      id: 'J_iframe_id_reportZJZJFX',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      fundGrant: '--',
      onButton:false,
      onSub:'查询',
      exportIcon:'el-icon-search'
    }
  },
  mounted() {
    var self = this
    var baseTime = store.state.edims.baseTime
    if(baseTime){
      self.formInline.ddate_ = [baseTime.beginDate, baseTime.endDate]
      self.formInline.beginDate = baseTime.beginDate
      self.formInline.endDate = baseTime.endDate
    }
    // self.getContrasOptions()
    // self.getDate()
    self.baseApi = process.env.BASE_API
    window.addEventListener('message', (msg) => {
      if (msg.data && msg.data.action == 'INFO_VM') {
        if (msg.data.payload.type == 'stop') {
          self.onButton = false
          self.onSub = '查询'
          self.exportButton2 = false
          self.exportIcon = 'el-icon-search'
        }
      }
    })
  },
  watch: {
    // 监听选中产品变化，自动更新查询参数
    selectedProducts: {
      handler(newVal) {
        if (newVal && newVal.length > 0) {
          this.formInline.fundCode = newVal.map(function(item) {
            return item.VC_FUNDCODE
          })
          this.formInline.fundName = newVal.map(function(item) {
            return item.VC_FUNDNAME
          }).join(',')
          if (newVal[0] && newVal[0].D_CREATE_DATE) {
            this.timDate = newVal[0].D_CREATE_DATE
          }
        } else {
          this.formInline.fundCode = []
          this.formInline.fundName = ""
          this.timDate = ""
        }
      },
      immediate: true
    }
  },
  methods: {
    /**
     * @description 获取默认时间
     */
    getDate() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/3ca0695e-a77a-4aeb-b82c-9b40360ba892`,
          method: 'post',
          data: {
            indexCode: '3ca0695e-a77a-4aeb-b82c-9b40360ba892'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              let beg = res.data.data[0].NEXTDATE
              let end = res.data.data[0].PREVDATE
              this.formInline.beginDate = beg
              this.formInline.endDate = end
              //this.formInline.ddate_ = [beg,end]
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    /**
     * @description 获取基准下拉
     */
    getContrasOptions() {
      return new Promise((resolve, reject) => {
        request({
          url: `/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d`,
          method: 'post',
          data: {
            indexCode: 'd43c924b-eebd-4d8f-97e5-ed46b609456d'
          }
        })
          .then((res) => {
            if (res.data.status === 0) {
              const resultDim = res.data.data || []
              this.datumOption = resultDim.map((item) => {
                return {
                  label: item.DIM_NME,
                  id: item.DIM_CDE
                }
              })
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    //日期时间段快捷选项
    dateShortTPCTA() {
      var self = this
      const pickerOptions = {
        shortcuts: [
          {
            text: '本周',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '本月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1])
                .month(moment(end).month())
                .format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '本季度',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01')
                .quarter(moment(end).quarter())
                .format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '今年以来',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard()
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = self.timDate
              if (self.offOn) {
                self.formInline.beginDate = start
                self.formInline.endDate = end
              } else {
                self.formInline.beginDate = ''
                self.formInline.endDate = ''
              }
              // picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          },
          {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              /*picker.$emit('pick', [start, end])*/
              self.formInline.beginDate = start
              self.formInline.endDate = end
            }
          }
        ]
      }
      return pickerOptions
    },
    async getStandard() {
      if(this.formInline.fundCode.length == 0){
        this.timDate =""
        this.$message({
          message: '请先选择产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      }
      if(this.formInline.fundCode.length > 1){
        this.timDate =""
        this.$message({
          message: '请选择单个产品！',
          type: 'warning',
          customClass: "message-warning"
        });
        return
      } else if (this.timDate == '' || this.timDate == undefined || this.timDate == null) {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '未获取到成立日！',
          type: 'warning',
          customClass: 'message-warning'
        })
        return
      } else {
        this.offOn = true
      }
    },
    // 权重校验
    handleInputWeight(type) {
      const regex = /^(0(\.\d+)?|[1-9]\d*(\.\d+)?)$/
      if (type == 'A') {
        if (!regex.test(this.formInline.ZB_INDEXWEIGHTA)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '只能输入大于等于0的数',
            customClass: 'message-warning'
          })
          this.formInline.ZB_INDEXWEIGHTA = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTB != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '基金A、B权重不能超过100%',
              customClass: 'message-warning'
            })
            this.formInline.ZB_INDEXWEIGHTA = '0'
          } else {
            this.formInline.ZB_INDEXWEIGHTA = '' + Number(this.formInline.ZB_INDEXWEIGHTA).toFixed(4)
          }
        }
      } else {
        if (!regex.test(this.formInline.ZB_INDEXWEIGHTB)) {
          this.$message.closeAll()
          this.$message({
            type: 'warning',
            message: '只能输入大于等于0的数',
            customClass: 'message-warning'
          })
          this.formInline.ZB_INDEXWEIGHTB = '0.0000'
          return
        }
        if (this.formInline.ZB_INDEXWEIGHTA != '') {
          if (Number(this.formInline.ZB_INDEXWEIGHTA) + Number(this.formInline.ZB_INDEXWEIGHTB) > 100) {
            this.$message.closeAll()
            this.$message({
              type: 'warning',
              message: '基金A、B权重不能超过100%',
              customClass: 'message-warning'
            })
            this.formInline.ZB_INDEXWEIGHTB = '0'
          } else {
            this.formInline.ZB_INDEXWEIGHTB = '' + Number(this.formInline.ZB_INDEXWEIGHTB).toFixed(4)
          }
        }
      }
    },
    // 获取选中数据
    getTemplateRow(data) {
      this.fundCode = data.data.fundCode
      this.formInline.fundCode = data.data.fundCode
      this.formInline.fundName = data.data.fundName
      this.timDate = data.data.createDate
      this.dialogMask = false
    },
    openFundListDialog() {
      /*this.productSelectorVisible = true*/
      this.dialogMask = true
    },
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {
      const self = this
      this.dialogMask = false
      if (arr) {
        self.formInline.fundCode = []
        self.formInline.fundName = ''
        arr.forEach(function (item, index) {
          index++
          if (index < arr.length) {
            self.formInline.fundName = self.formInline.fundName + item.VC_FUNDNAME + ','
          } else {
            self.formInline.fundName = self.formInline.fundName + item.VC_FUNDNAME
          }
          self.timDate = item.D_CREATE_DATE
          self.formInline.fundCode.push(item.VC_FUNDCODE)
        })
      }
      this.selectList = arr
    },
    fromLink() {
      var self = this
      if (this.$route.params && this.$route.params.date) {
        this.formInline.date = []
        this.formInline.date.push(this.$route.params.date[0])
        this.formInline.date.push(this.$route.params.date[1])
        this.fundCode = this.$route.params.fundCode
        this.fundName = this.$route.params.fundName

        try {
          // this.ProductAndPropertyData.fundCode =
          //   this.$route.params.fundCode;
          this.ProductAndPropertyData.performanceDefaultFundCode = this.fundCode
          this.$refs.bondAnalysis.myactiavted()
        } catch (e) {}
        // this.onQuery();
        // self.getFundBenchmark(this.fundCode);
        self.fun_iframeSrc()
      }
    },
    file_vmrisk_src_view(templateCode, beginDate, endDate, fundCode, benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode) {
      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&beginDate=' +
        beginDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
        '&benchmarkA=' +
        benchmarkA +
        '&benchmarkB=' +
        benchmarkB +
        '&benchmarkAValue=' +
        benchmarkAValue +
        '&benchmarkBValue=' +
        benchmarkBValue +
        '&kpiCode=' +
        kpiCode +
        '&contrasCode=' +
        contrasCode +
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },
    file_vmrisk_src_preview(templateCode, beginDate, endDate, fundCode, benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode) {
      return (
        process.env.BASE_API +
        '/rest/report/preview.do?templateCode=' +
        templateCode +
        '&beginDate=' +
        beginDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
        '&benchmarkA=' +
        benchmarkA +
        '&benchmarkB=' +
        benchmarkB +
        '&benchmarkAValue=' +
        benchmarkAValue +
        '&benchmarkBValue=' +
        benchmarkBValue +
        '&kpiCode=' +
        kpiCode +
        '&contrasCode=' +
        contrasCode +
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },
    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.fun_iframeSrc()
          } catch (e) {}
          // 禁用搜索按钮
          // self.$fun.searchButtonDisabled('issearchFxButton', self)
        } else {
          return false
        }
      })
    },
    // 清除
    resetForm(formName) {
      var self = this
      self.$refs[formName].resetFields()
      this.fundCode = ''
      this.fundName = ''
    },
    // iframe链接地址
    fun_iframeSrc() {
      /*   if (this.formInline.ddate_ && this.formInline.ddate_.length) {
             this.formInline.beginDate = this.formInline.ddate_[0];
             this.formInline.endDate = this.formInline.ddate_[1];
           }*/
      var self = this
      self.onButton = true
      self.onSub = '查询中...'
      self.exportButton2 = true
      self.exportIcon = 'el-icon-loading'
      if (self.formInline.ZB_INDEXTYPE == 'djz') {
        self.formInline.ZB_INDEXCODEB = ''
        self.formInline.ZB_INDEXWEIGHTA = ''
        self.formInline.ZB_INDEXWEIGHTB = ''
      }
      try {
        if (this.reportType == 'preview') {
          self.iframeData.src = this.file_vmrisk_src_preview(
            // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
            this.templateCode,
            self.formInline.beginDate,
            self.formInline.endDate,
            self.formInline.fundCode,
            self.formInline.ZB_INDEXCODEA,
            self.formInline.ZB_INDEXCODEB,
            self.formInline.ZB_INDEXWEIGHTA,
            self.formInline.ZB_INDEXWEIGHTB,
            '',
            '',
            '',
            '',
            'DWJZ',
            '104'
          )
        } else {
          self.iframeData.src = this.file_vmrisk_src_view(
            // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
            this.templateCode,
            self.formInline.beginDate,
            self.formInline.endDate,
            self.formInline.fundCode,
            self.formInline.ZB_INDEXCODEA,
            self.formInline.ZB_INDEXCODEB,
            self.formInline.ZB_INDEXWEIGHTA,
            self.formInline.ZB_INDEXWEIGHTB,
            '',
            '',
            '',
            '',
            'DWJZ',
            '104'
          )
        }
        this.$emit('iframeSrc', this.iframeData.src)
      } catch (e) {
        console.log(e)
      }
    },
    // 导出
    fun_export_PDF() {
      this.$emit('export_PDF')
    },
    // 导出vm
    fun_export() {
      var self = this

      if (self.formInline.fundCode == '') {
        self.$message({
          message: '请选择产品代码',
          type: 'warning'
        })
      } else {
        self.exportButton = true
        self.exportIcon = 'el-icon-loading'
        self.exportText = '导出数据中...'

        fun.file_vmrisk_download(
          // 报告模板ID  新建报告VUE界面需要更换相应的模板ID
          '28c29080-fe73-4c60-87b8-2b0564d78d5e',
          self.formInline.beginDate,
          self.formInline.endDate,
          self.formInline.fundCode,
          '',
          '',
          '',
          '',
          'DWJZ',
          '104'
        )

        setTimeout(function () {
          self.exportButton = false
          self.exportIcon = 'el-icon-download'
          self.exportText = '导出'
        }, 5000)
      }
    },

    // 导出word11
    fun_exportword() {
      this.exportButton2 = true
      this.exportIcon2 = 'el-icon-loading'
      this.exportText2 = '导出数据中...'

      const wordName = '报告.docx'
      // fun.fun_exportwordrisk(wordName);
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportwordriskOption(wordName, JSON.stringify(wordOption), this.id)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出Word'
      }, 10000)
    },
    fun_getDate() {
      var date = new Date()
      date.setDate(1)
      var month = parseInt(date.getMonth() + 1)
      var day = date.getDate()
      if (month < 10) {
        month = '0' + month
      }
      if (day < 10) {
        day = '0' + day
      }
      var statrDate = date.getFullYear() + '-' + month + '-' + day
      var date2 = new Date()
      var day2 = date2.getDate()
      if (day2 < 10) {
        day2 = '0' + day2
      }
      var endDate = date.getFullYear() + '-' + month + '-' + day2
      var dates = [statrDate, endDate]
      return dates
    }
  }
}
</script>

<style lang="scss">
.el-dialog {
  width: 60% !important;
}
</style>
<style lang="scss" scoped>
.el-dialog {
  width: 60% !important;
}

.customWidth {
  width: 80% !important;
}

input::-webkit-input-placeholder {
  color: #999 !important;
}
</style>

<style lang="scss" scoped>
.iframeModule_out {
  width: 100%;
  height: 100%;
  position: relative;

  .zhezhao {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
}

::v-deep .el-button.el-button--info {
  color: #333;
  background-color: #dddddd;
  border-color: #dddddd;
}
</style>
