<template>
  <div class="report-template-style">
<!--    <div style="margin-left: 36px; margin-top: 10px">
      <span>报告名称: {{ reportConfig.templateName }}</span>
      <span>报告类型: {{ vcReportTypeStr(reportConfig.vcReportType) }}</span>
    </div>-->
    <el-container style="height: 100%">
      <!--板块组合分析-->
      <el-main v-if="reportConfig.vcReportType === '1'" style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding-left: 0.5% !important; padding-right: 0.5% !important">
        <div>
        <single-product-selector
          :template-code="reportConfig.templateCode"
          :report-type="reportConfig.type"
          :template-name="reportConfig.templateName"
          @iframeSrc="handleIframeSrc"
          @export_PDF="fun_export_PDF"
        ></single-product-selector>
        </div>
        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>

      <el-main v-if="reportConfig.vcReportType === '2'" style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding-left: 0.5% !important; padding-right: 0.5% !important">
        <div class="search-content" style="margin-top: 12px; margin-bottom: 30px">
          <multiple-product-selector-base
            :template-code="reportConfig.templateCode"
            :report-type="reportConfig.type"
            :template-name="reportConfig.templateName"
            @iframeSrc="handleIframeSrc"
            @export_PDF="fun_export_PDF"
          ></multiple-product-selector-base>
        </div>
        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>
      <el-main v-if="reportConfig.vcReportType === '3'" style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding-left: 0.5% !important; padding-right: 0.5% !important">
        <div class="search-content" style="margin-top: 12px; margin-bottom: 30px">
          <multiple-product-selector-no-base
            :template-code="reportConfig.templateCode"
            :report-type="reportConfig.type"
            :template-name="reportConfig.templateName"
            @iframeSrc="handleIframeSrc"
            @export_PDF="fun_export_PDF"
          ></multiple-product-selector-no-base>
        </div>
        <div class="iframeModule_out">
          <iframeModule :id="id" :iframe-data="iframeData" :name="name" />
          <div v-if="zhezhao" class="zhezhao" @click="zhezhao = false"></div>
        </div>
      </el-main>

      <el-main v-if="reportConfig.vcReportType === '4'" style="height: 100%; overflow-x: hidden; overflow-y: hidden; padding-left: 0.5% !important; padding-right: 0.5% !important">
        <div>
          <single-product-selectorGF
            :template-code="reportConfig.templateCode"
            :report-type="reportConfig.type"
            :template-name="reportConfig.templateName"
            @iframeSrc="handleIframeSrc"
            @export_PDF="fun_export_PDF_GFJX"
            ref ="child"
          ></single-product-selectorGF>
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
import productSelector from '@/components/productSelector'
import { getToken } from '@/utils/auth'
import singleProductSelector from './singleProductSelector'
import singleProductSelectorGF from './singleProductSelectorGF'
import multipleProductSelectorBase from './multipleProductSelectorBase'
import multipleProductSelectorNoBase from './multipleProductSelectorNoBase'
export default {
  components: {
    iframeModule,
    productSelector,
    singleProductSelector,
    singleProductSelectorGF,
    multipleProductSelectorBase,
    multipleProductSelectorNoBase
  },
  props: {
    reportConfigExtern: {
      type: Object,
      default: () => {
        return {}
      }
    }
  },
  data() {
    return {
      reportConfig: {},
      zhezhao: false,
      iframeData: {
        // iframe链接
        src: ''
      },
      name: 'iframeVue_reportCSBG',
      id: 'J_iframe_id_reportCSBG',
      baseApi: '', // 页面根地址
      exportButton: false,
      exportText: '导出',
      exportIcon: 'el-icon-download',
      exportButton2: false, // 导出 word
      exportIcon2: 'el-icon-download',
      exportText2: '导出'
    }
  },
  mounted() {
    if (
      this.$route &&
      this.$route.meta &&
      this.$route.meta.vcactionstr &&
      this.$route.meta.vcactionstr.includes('templateCode') &&
      this.$route.meta.vcactionstr.includes('vcReportType')
    ) {
      let result = this.extractParametersFromString(this.$route.meta.vcactionstr)
      if (result.vcReportType && result.templateCode) {
        this.name = `iframeVue_${result.templateCode}`
        this.id = `J_iframe_id_${result.templateCode}`
        this.reportConfig = {
          vcReportType: result.vcReportType,
          templateCode: result.templateCode,
          type: 'view',
          templateName: result.templateCode
        }
      }
    }
  },
  watch: {
    reportConfigExtern: {
      handler(n) {
        if (n && n.templateCode) {
          this.reportConfig = n
          this.name = `iframeVue_${n.templateCode}`
          this.id = `J_iframe_id_${n.templateCode}`
        }
      },
      deep: true,
      immediate: true
    }
  },
  methods: {
    vcReportTypeStr(val) {
      if (val == '1') {
        return '单产品'
      } else if (val == '2') {
        return '多产品(含对比基准)'
      } else if (val == '3') {
        return '多产品(不包含对比基准)'
      } else if (val == '4') {
        return '单产品(不包含对比基准)'
      }else if (val == '5') {
        return '策略报告'
      }
      else {
        return '-'
      }
    },
    // iframe链接地址
    handleIframeSrc(src) {
      this.iframeData.src = src
    },
    extractParametersFromString(str) {
      let result = {
        templateCode: '',
        vcReportType: ''
      }

      // 使用正则表达式匹配 templateCode 和 vcReportType 的值
      let templateCodeMatch = str.match(/templateCode=([^&]+)/)
      if (templateCodeMatch) {
        result.templateCode = templateCodeMatch[1]
      }

      let vcReportTypeMatch = str.match(/vcReportType=([^&]+)/)
      if (vcReportTypeMatch) {
        result.vcReportType = vcReportTypeMatch[1]
      }

      return result
    },
    // 导出
    fun_export_PDF() {
      var self = this
      self.exportButton2 = true
      self.exportIcon2 = 'el-icon-loading'
      self.exportText2 = '导出数据中...'
      const templateCode = this.reportConfig.templateCode
      const wordName = `${this.reportConfig.templateCode}.docx`
      // fun.fun_exportwordrisk(wordName);
      const wordOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
      fun.fun_exportPDFOption(wordName, JSON.stringify(wordOption), this.id, templateCode)
      setTimeout(() => {
        this.exportButton2 = false
        this.exportIcon2 = 'el-icon-download'
        this.exportText2 = '导出'
      }, 5000)
    },
  // 导出
  fun_export_PDF_GFJX() {
    var self = this
    self.exportButton2 = true
    self.exportIcon2 = 'el-icon-loading'
    self.exportText2 = '导出数据中...'
    const childComponent = this.$refs.child;
    const templateCode = this.reportConfig.templateCode

    const fundCode = childComponent.formInline.fundCode
    const fundName = childComponent.formInline.fundName
    const beginDate = childComponent.formInline.ddate_[0]
    const endDate = childComponent.formInline.ddate_[1]
    const desensitizationFlag = childComponent.formInline.desensitizationFlag
    const desensitizationFun = childComponent.formInline.desensitizationFun
    const pdfName = `${this.reportConfig.templateCode}.pdf`
    const covIndexCode='dc4d61469e2b4a9b875706e66e59ab25'
    // fun.fun_exportwordrisk(wordName);
    const pdfOption = { pagedir: 'h' } // vm导出word说明文档中相反，h为纵向，v为横向，默认为横向
    fun.fun_exportPDFOption_GFJX(pdfName, JSON.stringify(pdfOption), this.id, templateCode,fundCode,fundName,beginDate,endDate,desensitizationFlag,desensitizationFun,covIndexCode)
    setTimeout(() => {
      this.exportButton2 = false
      this.exportIcon2 = 'el-icon-download'
      this.exportText2 = '导出'
    }, 5000)
  }
  }
}
</script>
<style lang="scss">
.report-template-style {
  height: 100%;
}

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
