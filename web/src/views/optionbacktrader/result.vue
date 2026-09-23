<template>
  <div style="height: 100%" class="PerformanceReportStyle">
    <el-container style="height: 100%">
      <el-main style="height: 100%; overflow-x: hidden; overflow-y: hidden">
        <div class="buttons">
          <el-button :icon="exportIcon" style="margin-bottom: 5px" size="small" :disabled="onButton" type="primary"
            @click="onSubmit('formInline')">{{ onSub }}</el-button>
          <el-button type="info" plain :icon="exportIcon2" style="margin-bottom: 5px" :disabled="exportButton2"
            @click="fun_export_PDF" size="small">
            {{ exportText2 }}
          </el-button>
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
import store from "@/store";
export default {
  name: 'ReportGF_HCJG',
  components: {
    iframeModule,
  },
  data() {
    return {
      zhezhao: false,
      dialogMask: false,
      // 搜索
      formInline: {
        product: null,
        // date: [],
        ddate_: [],
        beginDate: '',
        endDate: '',
        fundCode: '',
        fundName: '',
        programmeName:'',
        fid:'',
        ZB_INDEXCODE: '', // 基准编码
        ZB_INDEXTYPE: 'djz', // 基准类型
        ZB_INDEXCODEA: '000300', // 基准A
        ZB_INDEXWEIGHTA: '0.0000', // 基准A权重
        ZB_INDEXCODEB: '000300', // 基准B
        ZB_INDEXWEIGHTB: '0.0000', // 基准B权重
        desensitizationFlag: '', //脱敏标志
        desensitizationFun: 'ALL', //脱敏方法 ALL 不显示名称和代码  PAR 仅屏蔽部分字符
        dataFreqOpen: 'true',//数据频率过滤是否开启
        dataFreq: '1',//数据频率  1 日频 2 周频  3 月频
      },
      issearchFxButton: false,
      fundCode: '', // code值
      fundName: '', // name
      noData: '--', // 没有数据
      iframeData: {
        // iframe链接
        src: ''
      },
      //开关
      offOn: false,
      name: 'iframeVue_reportGF_HCJG',
      id: 'J_iframe_id_reportGF_HCJG',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportButton2: false, // 导出 word
      onButton: false,
      exportIcon2: 'el-icon-download',
      /*exportText2: '导出Word',*/
      exportText2: '导出',
      benchmarkA: '',
      dateTime: '',
      onSub: '查询',
      exportIcon: 'el-icon-search',
      showDesensitization: false,
    }
  },
  mounted() {
    document.title='回测结果查询'
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
    this.onSubmit('formInline')
  },
  methods: {
    handleDialogClosed() {
      this.dialogMask = false
    },
    handleSubmitClick(arr) {

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
        } catch (e) { }
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
      self.fun_iframeSrc()
      self.$fun.searchButtonDisabled('issearchFxButton', self)
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
            'e3caf0a0-fa10-481b-9e4c-aab98e8f2237',
            self.formInline.ddate_[0],
            self.formInline.ddate_[1],
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
          this.formInline.fid=this.$route.query.fid;
          this.formInline.programmeName=this.$route.query.programmeName;
          self.iframeData.src = this.file_vmrisk_src_view(
            'e3caf0a0-fa10-481b-9e4c-aab98e8f2237',this.$route.query.fid
          )
        }
        this.$emit('iframeSrc', this.iframeData.src)
      } catch (e) {
        console.log(e)
      }
    },

    file_vmrisk_src_view(templateCode, fid) {

      return (
        process.env.BASE_API +
        '/rest/report/interview.do?templateCode=' +
        templateCode +
        '&fid=' +
        fid +
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
      const templateCode = 'e3caf0a0-fa10-481b-9e4c-aab98e8f2237'
      const pdfName = "回测结果_"+this.formInline.programmeName+".pdf"
      const fundCode = self.formInline.fundCode
      const fundName = self.formInline.fundName
      const beginDate = self.formInline.ddate_[0]
      const endDate = self.formInline.ddate_[1]
      const desensitizationFlag = self.formInline.desensitizationFlag
      const desensitizationFun = self.formInline.desensitizationFun
     // const covIndexCode = 'dc4d61469e2b4a9b875706e66e59ab25'
      const pdfOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption_GFJX_new(
        pdfName,
        JSON.stringify(pdfOption),
        this.id,
        templateCode,
        fundCode,
        fundName,
        beginDate,
        endDate,
        desensitizationFlag,
        desensitizationFun,
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        "",
        // 成功回调：恢复按钮
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.success(res.message);
        },
        // 失败回调：恢复按钮
        (res) => {
          self.exportButton2 = false;
          self.exportIcon2 = 'el-icon-download';
          self.exportText2 = '导出';
          self.$message.error(res.message);
        }
      );

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
          'e3caf0a0-fa10-481b-9e4c-aab98e8f2237',
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
  }
}
</script>

<style lang="scss" scoped>

.buttons{
  margin: 0 auto;
  padding:20px 20px 0px 20px;
  display: flex;
  justify-content: end;
  width: 1248px;
}

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
