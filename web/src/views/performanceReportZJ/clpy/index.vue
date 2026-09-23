<template>
  <div style="height: 100%" class="PerformanceReportStyle analyse-page">
    <el-container style="height: 100%">
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden">
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="demo-form-inline form_inline_search standard-form" style="margin-top: 10px">
              <el-row>
                <el-col :span="24">
                  <div class="grid-content bg-purple">
<!--                    <el-form-item label="" prop="fundName">
                      <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" effect="dark" placement="top-start">
                        <el-input v-model="formInline.fundName" clearable placeholder="请选择产品" size="small" @click.native="openFundListDialog" />
                      </el-tooltip>
                    </el-form-item>-->
                    <el-form-item label="" prop="fundName">
                      <ProductSelectInput
                        v-model="formInline.product"
                        placeholder="请选择产品"
                        :input-width="'260px'"
                        @select="handleProductSelect"
                        @clear="handleProductClear"
                      />
                    </el-form-item>
                    <el-form-item class="mb20" label="日期" prop="ddate_">
                      <el-date-picker
                        v-model="formInline.ddate_"
                        :picker-options="dateShortTPCTA()"
                        align="left"
                        end-placeholder="结束日期"
                        popper-class="popperDateShortTP"
                        range-separator="-"
                        size="small"
                        start-placeholder="开始日期"
                        type="daterange"
                        unlink-panels
                        value-format="yyyy-MM-dd"
                      ></el-date-picker>
                    </el-form-item>
                    <el-form-item class="">
                      <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary" @click="onSubmit('formInline')">{{onSub}}</el-button>
                      <el-button type="info" plain icon="el-icon-refresh-left" size="small" @click="resetForm('formInline')">重置</el-button>
                      <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2" @click="fun_export_PDF" size="small">
                        {{ exportText2 }}
                      </el-button>
                    </el-form-item>
                  </div>
                </el-col>
              </el-row>
            </el-form>
          </div>
        </div>
        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>
    </el-container>

    <product-selector
      v-if="dialogMask"
      :leftList="left"
      :dialog-visible="dialogMask"
      :tree-data="treeData"
      :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList"
      default-checked-keys="zstgwb"
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
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

export default {
  name: 'ReportCLPY',
  components: {
    FundListDialog,
    iframeModule,
    productSelector,
    ProductSelectInput
  },
  data() {
    const validateRangeDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择日期范围'))
      } else {
        if (this.formInline.ddate_ !== null || this.formInline.ddate_ !== undefined || this.formInline.ddate_ !== '') {
          const startTime = new Date(this.formInline.ddate_[0])
          const endTime = new Date(this.formInline.ddate_[1])
          const fundCreateTime=new Date(this.timDate)
          const fundEndTime=new Date(this.dateTime)
          if(endTime >fundEndTime){
            callback(new Error('结束日期不能大于产品最新的估值确认日期'))
          }else if(startTime < fundCreateTime) {
            callback(new Error('开始日期不能早于产品的成立日期'))
          }else if (startTime > endTime) {
            callback(new Error('开始日期不能大于结束日期'))
          } else {
            callback()
          }
        } else {
          callback()
        }
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
      // 选择产品弹窗
      productSelectorVisible: false,
      left: false,
      selectList: [],
      loading: false,
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
      // 搜索
      formInline: {
        product: null,
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
      },
      datumOption: [],
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        // ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        // beginDate: [
        //   { required: true, message: '请选择开始日期', trigger: 'blur' },
        //   { validator: validatebeginDate, trigger: 'blur' }
        // ],
        // endDate: [
        //   { required: true, message: '请选择结束日期', trigger: 'blur' },
        //   { validator: validateEndDate, trigger: 'blur' }
        // ],
        fundName: [{ required: true, message: '请选择产品', trigger: 'change' }],
        ddate_: [
          {required: true, message: "请选择日期", trigger: "change"},
          {validator: validateRangeDate, trigger: 'blur' }
        ],
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
      name: 'iframeVue_reportCLPY',
      id: 'J_iframe_id_reportCLPY',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      onButton:false,
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      dateTime:'',
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
    self.baseApi = process.env.BASE_API
    if(store.state.edims.userType == '2' || store.state.edims.userType == 2){
      self.left = true;
      self.showTreeKeyArray = ['产品列表'];
    }
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
  methods: {


    getTimeBig(){
      if(this.formInline.fundCode =='' || this.formInline.fundCode == null){
        if(this.formInline.beginDate!=''){
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.beginDate =''
      }else {
        if (this.formInline.beginDate !='' && this.formInline.beginDate < this.timDate) {
          setTimeout(() => {
            this.formInline.beginDate = this.timDate;
          }, 500);
        }
      }
    },
    getTimeEnd(){
      if(this.formInline.fundCode =='' || this.formInline.fundCode == null){
        if(this.formInline.endDate!=''){
          this.$message({
            message: '请选择产品代码',
            type: 'warning'
          })
        }
        this.formInline.endDate =''
      }else{
        if((this.formInline.endDate != this.dateTime) && (this.formInline.endDate != '' || this.formInline.endDate != null)){
          this.getTimes(this.formInline.fundCode,this.formInline.endDate)
        }
      }
    },
    getTimes(code,end) {
      this.onButton = true
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode:code,
          endDate: end
        }
        request({
          url: `/api/report/v1.0/data/sql/dacc5f54-8ff8-418b-984a-52a18409d716`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.dateTime = res.data.data[0].endTime
              if(this.dateTime != null && this.formInline.endDate > this.dateTime){
                this.formInline.endDate = this.dateTime
              }
            }
            resolve()
            this.onButton = false
          })
          .catch((err) => {
            this.onButton = false
            resolve()
          })
      })
    },
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
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },

    //日期时间段快捷选项  从成立日到 估值确认日期
    dateShortTPCTA() {
      var self = this
      if(self.dateTime!==null && self.dateTime!==""
        && self.timDate!==null && self.timDate!==""){
        const pickerOptions = {
          shortcuts: [{
            text: '本周',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '本月',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '本季度',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          }, {
            text: '今年以来',
            onClick(picker) {
              const end = moment(self.dateTime).format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              const create = self.timDate
              const createTime=moment(self.timDate).format('YYYY-MM-DD')
              //判断开始日期是否再成立日期之前
              picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
            }
          },
            {
              text: '成立以来',
              onClick(picker) {
                self.getStandard();
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])

              }
            },
            {
              text: '近一个月',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近三个月',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近半年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近一年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            }, {
              text: '近三年',
              onClick(picker) {
                const end = moment(self.dateTime).format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                const create = self.timDate
                const createTime=moment(self.timDate).format('YYYY-MM-DD')
                //判断开始日期是否再成立日期之前
                picker.$emit('pick', [moment(start).isAfter(create)===true?start:createTime, end])
              }
            },],

          disabledDate(time) {
            // 设置产品的日期范围，成立日到最新的估值确认日期
            return time < new Date(self.timDate) || time > new Date(self.dateTime);
          },
        }
        return pickerOptions
      }else {
        const pickerOptions = {
          shortcuts: [{
            text: '本周',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).isoWeekday(1).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '本月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1]).month(moment(end).month()).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '本季度',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01').quarter(moment(end).quarter()).format('YYYY-MM-DD')
              picker.$emit('pick', [start, end])
            }
          }, {
            text: '今年以来',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              picker.$emit('pick', [start, end])
            }
          },
            {
              text: '成立以来',
              onClick(picker) {
                self.getStandard();
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = self.timDate
                picker.$emit('pick', [start, end])

              }
            },
            {
              text: '近一个月',
              onClick(picker) {
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                picker.$emit('pick', [start, end])
              }
            }, {
              text: '近三个月',
              onClick(picker) {
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                picker.$emit('pick', [start, end])
              }
            }, {
              text: '近半年',
              onClick(picker) {
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                picker.$emit('pick', [start, end])
              }
            }, {
              text: '近一年',
              onClick(picker) {
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                picker.$emit('pick', [start, end])
              }
            }, {
              text: '近三年',
              onClick(picker) {
                const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
                const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
                picker.$emit('pick', [start, end])
              }
            },],


        }
        return pickerOptions
      }

    },
    async getStandard() {
      if (this.fundCode == '' || this.formInline.fundName == '') {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '请先选择产品！',
          type: 'warning'
        })
        return
      } else if (this.timDate == '' || this.timDate == undefined || this.timDate == null) {
        this.offOn = false
        this.timDate = ''
        this.$message({
          message: '未获取到成立日！',
          type: 'warning'
        })
        return
      } else {
        this.offOn = true
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
      this.dialogMask = false
      this.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.timDate = arr[0].D_CREATE_DATE || ''
      this.selectList = arr
      //估值最新确认日期
      this.initTimGzLastDate(arr[0].VC_FUNDCODE || '')
    },
    handleProductSelect: function(product) {
      this.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundCode = product.VC_FUNDCODE || ''
      this.formInline.fundName = product.VC_FUNDNAME || ''
      this.timDate = product.D_CREATE_DATE || ''
      //估值最新确认日期
      this.initTimGzLastDate(product.VC_FUNDCODE || '')
    },
    handleProductClear: function() {
      this.fundCode = ''
      this.formInline.fundCode = ''
      this.formInline.fundName =  ''
      this.timDate = ''
    },
    initTimGzLastDate(fundCode){
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: 'dacc5f54-8ff8-418b-984a-52a18409d716',
          fundCode:fundCode,
        }
        request({
          url: `/api/report/v1.0/data/sql/dacc5f54-8ff8-418b-984a-52a18409d716`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.dateTime = res.data.data[0].endTime
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    file_vmrisk_src(templateCode, beginDate, endDate, fundCode, benchmarkA, benchmarkB, benchmarkAValue, benchmarkBValue, kpiCode, contrasCode) {
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

    onSubmit(formName) {
      var self = this
      self.$refs[formName].validate((valid) => {
        if (valid) {
          try {
            self.fun_iframeSrc()
          } catch (e) {}
          // 禁用搜索按钮
          self.$fun.searchButtonDisabled('issearchFxButton', self)
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
      var self = this
      self.onButton = true
      self.onSub = '查询中...'
      self.exportButton2 = true
      self.exportIcon = 'el-icon-loading'
      try {
        self.iframeData.src = this.file_vmrisk_src(
          // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
          'f03ffd44-e468-4d8c-88db-3f76c39c7afb',
          self.formInline.ddate_[0],
          self.formInline.ddate_[1],
          self.formInline.fundCode,
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          '',
          'DWJZ',
          '104'
        )
      } catch (e) {
        console.log(e)
      }
    },
    // 导出
    fun_export_PDF() {
      var self = this
      self.exportButton2 = true
      self.exportIcon2 = 'el-icon-loading'
      self.exportText2 = '导出数据中...'
      const templateCode = 'f03ffd44-e468-4d8c-88db-3f76c39c7afb'
      const wordName = '策略漂移报告.pdf'
      const fundName = self.formInline.fundName
      const beginDate = self.formInline.ddate_[0]
      const endDate = self.formInline.ddate_[1]
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode, fundName, beginDate, endDate)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 10000)
    },

  }
}
</script>

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
::v-deep .standard-form .el-form-item {
  margin-bottom: 5px !important;
}
</style>
