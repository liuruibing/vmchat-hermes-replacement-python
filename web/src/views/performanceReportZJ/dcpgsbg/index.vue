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
                  <div class="grid-content bg-purple">
                    <el-form-item label="产品" prop="fundName">
                      <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" class="item" effect="dark" placement="top-start">
                        <el-input v-model="formInline.fundName" clearable placeholder="请输入" size="small" @click.native="openFundListDialog" />
                      </el-tooltip>
                    </el-form-item>
                    <el-form-item label="开始日期" prop="beginDate">
                      <el-date-picker v-model="formInline.beginDate" :picker-options="dateShortTPCTA()" placeholder="选择开始日期" type="date" value-format="yyyy-MM-dd" />
                    </el-form-item>
                    <el-form-item label="结束日期" prop="endDate">
                      <el-date-picker v-model="formInline.endDate" placeholder="选择结束日期" type="date" value-format="yyyy-MM-dd" />
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
export default {
  name: 'ReportDCPGSBG',
  components: {
    FundListDialog,
    iframeModule,
    productSelector
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
      // 选择产品弹窗
      productSelectorVisible: false,
      left: false,
      selectList: [],
      zhezhao: false,
      dialogMask: false,
      onButton:false,
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
      },
      datumOption: [],
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        // ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
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
      name: 'iframeVue_reportDCPGSBG',
      id: 'J_iframe_id_reportDCPGSBG',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
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
              self.formInline.beginDate = start
              self.formInline.endDate = end
              /*picker.$emit('pick', [start, end])*/
            }
          },
          {
            text: '本月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment([moment(end).year(), 0, 1])
                .month(moment(end).month())
                .format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              /*picker.$emit('pick', [start, end])*/
            }
          },
          {
            text: '本季度',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).year() + '-01-01')
                .quarter(moment(end).quarter())
                .format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              /*  picker.$emit('pick', [start, end])*/
            }
          },
          {
            text: '今年以来',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(end).year() + '-01-01'
              self.formInline.beginDate = start
              self.formInline.endDate = end
              //picker.$emit('pick', [start, end])
            }
          },
          {
            text: '成立以来',
            onClick(picker) {
              self.getStandard()
              const start = self.timDate
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
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
              self.formInline.beginDate = start
              self.formInline.endDate = end
              //picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近三个月',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              //picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近半年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(6, 'month').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              //picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近一年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(1, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              // picker.$emit('pick', [start, end])
            }
          },
          {
            text: '近三年',
            onClick(picker) {
              const end = moment().subtract(1, 'days').format('YYYY-MM-DD')
              const start = moment(moment(end).subtract(3, 'years').format('YYYY-MM-DD')).subtract(-1, 'days').format('YYYY-MM-DD')
              self.formInline.beginDate = start
              self.formInline.endDate = end
              //picker.$emit('pick', [start, end])
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
    openFundListDialog() {
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
          'b496473b-063e-4a90-af42-677b96fb2546',
          self.formInline.beginDate,
          self.formInline.endDate,
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
      const templateCode = 'b496473b-063e-4a90-af42-677b96fb2546'
      const wordName = '多产品固收报告.pdf'
      const fundName = self.formInline.fundName
      const beginDate = self.formInline.beginDate
      const endDate = self.formInline.endDate
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode, fundName, beginDate, endDate)
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
          'b496473b-063e-4a90-af42-677b96fb2546',
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
::v-deep .standard-form .el-form-item {
  margin-bottom: 5px !important;
}
</style>
