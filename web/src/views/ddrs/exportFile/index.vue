<template>
  <div>
    <reportTemplate
      v-if="currencyReportPageData.reportCode"
      :currencyReportPageData="currencyReportPageData"
      ref="reportTemplate"
    >
      <template slot="queryBtn">
        <el-button
          type="primary"
          :loading="btnDisabled"
          @click="downloadExport"
          size="small"
          icon="el-icon-download"
          >导出</el-button
        >
      </template>
    </reportTemplate>
  </div>
</template>
<script>
import reportTemplate from "./reportTemplate.vue";
import commonApi from "@/api/common";
export default {
  components: {
    reportTemplate,
  },
  data() {
    return {
      btnDisabled: false,
      currencyReportPageData: {
        reportCode: "",
      },
    };
  },
  mounted() {
    if (this.$route && this.$route.meta && this.$route.meta.suffix) {
      const queryString = this.$route.meta.suffix.split("?")[1];
      if (queryString) {
        const templateCode = queryString
          .split("templateCode=")[1]
          .split("&")[0];
        const reportCode = queryString.split("reportCode=")[1].split("&")[0];
        this.currencyReportPageData.reportCode = reportCode;
        this.currencyReportPageData.templateCode = templateCode;
      }
    }
  },
  methods: {
    async downloadExport() {
      // 修改导出的一些样式和按钮效果
      let params = await this.$refs.reportTemplate.getSearchData();

      if (this.currencyReportPageData.templateCode && !params.templateCode) {
        params.templateCode = this.currencyReportPageData.templateCode;
      }
      // let url = "/api/report/v1.0/export/template/";
      let url = "/api/report/v1.0/export/template/gzip";
      
      // 判断templateCode是不是数组
      if (Array.isArray(params.templateCode)) {
        params.fileName = (this.$route.meta.title.replace(/\s+/g, '') || '导出文件') + '.zip'
      }

      this.btnDisabled = true;
      commonApi.downLoadFileByUrlPost(url, params, params.fileName, () => {
        this.btnDisabled = false;
      });
    },
  },
};
</script>
