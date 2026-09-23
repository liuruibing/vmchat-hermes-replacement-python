<template>
  <div style="height: 100%;padding-left: 16px; padding-right:20px">
    <el-container style="height: 100%">
      <!--板块组合分析-->
      <el-main
        style="
          height: 100%;
          overflow-x: hidden;
          overflow-y: hidden;
          padding-left: 0.5% !important;
          padding-right: 0.5% !important;
        "
      >
        <div class="search-content" style="margin-top: 12px;margin-bottom: 30px">
          <el-form ref="formInline" :inline="true" :model="formInline" :rules="searchRules" class="demo-form-inline form_inline_search" style="margin-top: 10px">
            <el-row>
              <el-form-item label="" prop="beginDate">
                <el-date-picker v-model="formInline.beginDate" :picker-options="pickerOptions" placeholder="开始日期" type="date" value-format="yyyy-MM-dd" />
              </el-form-item>
              <el-form-item label="" prop="endDate">
                <el-date-picker v-model="formInline.endDate" :picker-options="pickerOptions" placeholder="结束日期" type="date" value-format="yyyy-MM-dd" />
              </el-form-item>
              <el-form-item label="" prop="fundName">
                <el-tooltip :content="formInline.fundName" :disabled="!formInline.fundName" class="item" effect="dark" placement="top-start">
                  <el-input v-model="formInline.fundName" clearable placeholder="产品" size="small" @click.native="openFundListDialog" />
                </el-tooltip>
              </el-form-item>
              <el-form-item>
                <el-button icon="el-icon-search" size="small" type="primary" @click="onSubmit('formInline')">
                  查询
                </el-button>
                <el-button icon="el-icon-refresh-left" type="info" plain size="small" @click="resetForm('formInline')">
                  重置
                </el-button>
              </el-form-item>
              <el-form-item>
                <div style="color: red;">拥有此产品：{{ fundGrant }}权限，报告仅显示有权限模块。</div>
              </el-form-item>
              <el-form-item class="search_button_com">
                <el-button type="info" :disabled="exportButton2" @click="fun_export_PDF" size="small">
                  {{ exportText2 }}
                </el-button>
              </el-form-item>
            </el-row>
          </el-form>
        </div>

        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>
    </el-container>
    <product-selector
      v-if="productSelectorVisible"
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
import iframeModule from '@/components/iframe'
import fun from '@/filters/common'
import productSelector from '@/components/productSelector'
import { getToken } from '@/utils/auth'

export default {
  name: 'ReportCTA',
  components: {
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
      treeData: [
        {
          label: '市场私募',
          id: 'scsm'
        },
        {
          label: '广发托管/外包',
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
      showTreeKeyArray: ['广发托管/外包', '我的关注'],
      selectList: [],
      zhezhao: false,
      dialogMask: false,
      pickerOptions: {},
      productCheckArr: [],
      companyCheckArr: [],
      fundArray: [],

      // 搜索
      formInline: {
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: ''
      },
      searchRules: {
        // date: [{ required: true, trigger: "change", validator: validateDate }],
        // ddate_: [{required: true, message: "请选择日期", trigger: "change"}],
        beginDate: [{ required: true, message: '请选择开始日期', trigger: 'blur' }, { validator: validatebeginDate, trigger: 'blur' }],
        endDate: [{ required: true, message: '请选择结束日期', trigger: 'blur' }, { validator: validateEndDate, trigger: 'blur' }],
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
      name: 'iframeVue_reportCTABG',
      id: 'J_iframe_id_reportCTABG',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportIcon: 'el-icon-download',
      exportButton2: false, // 导出 word
      exportIcon2: 'el-icon-download',
      exportText2: '导出',
      benchmarkA: '',
      fundGrant: '--'
    }
  },
  mounted() {
    self.baseApi = process.env.BASE_API
  },
  methods: {
    openFundListDialog() {
      this.productSelectorVisible = true
    },
    handleDialogClosed() {
      this.productSelectorVisible = false
    },
    handleSubmitClick(arr) {
      this.productSelectorVisible = false
      this.formInline.fundCode = arr[0].VC_FUNDCODE || ''
      this.formInline.fundName = arr[0].VC_FUNDNAME || ''
      this.fundGrant = arr[0].VC_FUND_GRANT || '--'
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
    file_vmrisk_src(templateCode, startDate, endDate, fundCode, kpiCode, contrasCode) {
      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&startDate=' +
        startDate +
        '&endDate=' +
        endDate +
        '&fundCode=' +
        fundCode +
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
      self.$refs[formName].validate(valid => {
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
      try {
        self.iframeData.src = this.file_vmrisk_src(
          // "2ae0c3f9-f8ee-4cab-b7c0-65b0f654548e",
          '71fc8e1a-874b-42d3-9ec7-bdd65310f38b',
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
      const templateCode = '71fc8e1a-874b-42d3-9ec7-bdd65310f38b'
      const wordName = 'CTA绩效报告.docx'
      // fun.fun_exportwordrisk(wordName);
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 5000)
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
          '71fc8e1a-874b-42d3-9ec7-bdd65310f38b',
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

        setTimeout(function() {
          self.exportButton = false
          self.exportIcon = 'el-icon-download'
          self.exportText = '导出'
        }, 10000)
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
      }, 5000)
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
.customWidth {
  width: 55% !important;
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
</style>
