<template>
  <div style="height: 100%" class="PerformanceReportStyle">
    <el-container style="height: 100%">
      <!--板块组合分析-->
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden">
        <div class="standard-form-margin">
          <div class="inner-margin">
            <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="demo-form-inline form_inline_search standard-form" style="margin-top: 10px">
              <el-row>
                <el-col :span="24">
                  <div class="grid-content bg-purple analyse-page">


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
                    <el-form-item label="时间轴显示">
                      <el-select v-model="formInline.freq" size="small" clearable filterable placeholder="请选择展示频率">
                        <el-option v-for="item in freqList" :key="item.dimCde" :label="item.dimNme" :value="item.dimCde" />
                      </el-select>
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

  </div>
</template>

<script>
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import { getToken } from '@/utils/auth'
import request from '@/utils/request'
import moment from 'moment'
import commonApi from '@/api/common.js'
import store from "../../../store";
export default {
  name: 'ReportGF_STRATEGPRIVATE',
  components: {
    iframeModule,
  },
  data() {
    const validateRangeDate = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请选择日期范围'))
      } else {
        if (this.formInline.ddate_ !== null || this.formInline.ddate_ !== undefined || this.formInline.ddate_ !== '') {
          const startTime = new Date(this.formInline.ddate_[0])
          const endTime = new Date(this.formInline.ddate_[1])
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
    return {
      isShowMoreQuery: false,
      // 选择产品弹窗
      productSelectorVisible: false,
      left: false,
      selectList: [],
      zhezhao: false,
      dialogMask: false,

      pickerOptions :{},



      // 搜索
      formInline: {
        ddate_: [],
        beginDate: '',
        endDate: '',
        freq:'DAY'
      },
      freqList:[],
      datumOption: [],
      searchRules: {
        ddate_: [
          {required: true, message: "请选择日期", trigger: "change"},
          {validator: validateRangeDate, trigger: 'blur' }
        ]

      },
      issearchFxButton: false,

      noData: '--', // 没有数据
      iframeData: {
        // iframe链接
        src: ''
      },
      //成立日

      //开关
      offOn: false,
      name: 'iframeVue_reportGF_STRATEGYPRIVATE',
      id: 'J_iframe_id_reportGF_STRATEGYPRIVATE',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      onButton:false,
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      onSub:'查询',
      exportIcon:'el-icon-search',
      showDesensitization:false,
    }
  },
  mounted() {
    var self = this
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
    // 初始化时间轴频率
    this.getEchartTimePreqEdims("ECHART_TIME_FREQ");
    this.initTimesQuery();


  },
  watch: {
    '$route.path'(val) {
      if (val == '/jxbg/strategybg/strategyprivate' && this.$store.getters.isHome === true) {
        this.$store.commit('SET_HOME_STATUS', false)
        var self = this
        let beg;
        let end;
        if (self.$route.query.rows.ddate_ && self.$route.query.rows.ddate_.length) {

           beg = self.$route.query.rows.ddate_[0]
           end = self.$route.query.rows.ddate_[1]
        }
        self.formInline.ddate_ = [beg,end]
        self.formInline.beginDate = beg
        self.formInline.endDate = end
        self.onSubmit('formInline')
      }
    },

  },
  methods: {
    // 投资策略列表查询
    getEchartTimePreqEdims (type) {
      // 字典类型
      let params = type
      commonApi.edimsSelectType(params).then(res => {
        let { status, data } = res.data
        if (status === 0) {
          this.freqList = data
        }
      })
    },
    /**
     * @description 是否展示更多查询
     */
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
    },
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
        //私募策略报告查询默认T-2近一个月的起始时间
        const params = {
          indexCode: '868b4212-9d41-4ac0-a3db-8896d2913541',
          fundCode:code,
          endDate: end
        }
        request({
          url: `/api/report/v1.0/data/sql/868b4212-9d41-4ac0-a3db-8896d2913541`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.dateTime = res.data.data[0].endDate
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

    initTimesQuery() {
      this.onButton = true
      return new Promise((resolve, reject) => {
        const params = {
          indexCode: '868b4212-9d41-4ac0-a3db-8896d2913541',
        }
        request({
          url: `/api/report/v1.0/data/sql/868b4212-9d41-4ac0-a3db-8896d2913541`,
          method: 'post',
          data: params
        })
          .then((res) => {
            if (res.data.status === 0) {
              this.formInline.ddate_ = [res.data.data[0].beginDate,res.data.data[0].endDate]
              this.onSubmit('formInline')

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
              this.formInline.ddate_ = [beg,end]
            }
            resolve()
          })
          .catch((err) => {
            resolve()
          })
      })
    },
    handlecheckeddesensitizationChange(value) {
      this.showDesensitization = value;
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
    //日期时间段快捷选项  从成立日到 估值确认日期
    dateShortTPCTA() {
      var self = this

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
            '5400326f-39c4-4188-aa52-ec17e137c283',
            self.formInline.ddate_[0],
            self.formInline.ddate_[1],
            self.formInline.freq
          )
        } else {
          self.iframeData.src = this.file_vmrisk_src_view(
            // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
            '5400326f-39c4-4188-aa52-ec17e137c283',
            self.formInline.ddate_[0],
            self.formInline.ddate_[1],
            self.formInline.freq,
          )
        }
        this.$emit('iframeSrc', this.iframeData.src)
      } catch (e) {
        console.log(e)
      }
    },

    file_vmrisk_src_view(templateCode, beginDate, endDate, freq) {
      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&beginDate=' +
        beginDate +
        '&endDate=' +
        endDate +
        '&freq=' +
        freq +
        '&token=' +
        encodeURIComponent(getToken()) +
        '&autoRun=false&ajaxRun=true&showParam=true&showCondition=false&markFlag=false&srcSuffix=' +
        process.env.BASE_API +
        '&time=' +
        new Date().getTime()
      )
    },

    // 导出
    fun_export_PDF() {
      var self = this
      self.exportButton2 = true
      self.exportIcon2 = 'el-icon-loading'
      self.exportText2 = '导出数据中...'
      const templateCode =  '5400326f-39c4-4188-aa52-ec17e137c283'
      const pdfName = '策略周报.pdf'
      const beginDate = self.formInline.ddate_[0]
      const endDate = self.formInline.ddate_[1]
      const freq = self.formInline.freq
      const pdfOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption_GFJX_STRA(pdfName, JSON.stringify(pdfOption), this.id, templateCode,beginDate,endDate,freq)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 10000)
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
        self.exportButton2 = true
        self.exportIcon2 = 'el-icon-loading'
        self.exportText2 = '导出数据中...'

        fun.file_vmrisk_download(
          // 报告模板ID  新建报告VUE界面需要更换相应的模板ID
          '5400326f-39c4-4188-aa52-ec17e137c283',
          self.formInline.ddate_[0],
          self.formInline.ddate_[1],
          self.formInline.fundCode,
          self.formInline.ZB_INDEXCODEA,
          self.formInline.ZB_INDEXCODEB,
          self.formInline.ZB_INDEXWEIGHTA,
          self.formInline.ZB_INDEXWEIGHTB,
          'DWJZ',
          '104'
        )

        setTimeout(function () {
          self.exportButton2 = false
          self.exportIcon2 = 'el-icon-download'
          self.exportText2 = '导出'
        }, 20000)
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
  height: 88%;
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
