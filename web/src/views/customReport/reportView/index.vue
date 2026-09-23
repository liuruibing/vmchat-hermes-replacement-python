<template>
  <div class="custom-report-view">
    <ReportQueryForm
      :template-list="templateList"
      :query-loading="queryLoading"
      :export-loading="exportLoading"
      :export-disabled="exportDisabled"
      @template-change="handleTemplateChange"
      @query="handleQuery"
      @reset="handleReset"
      @export="handleExport"
    />

    <div
      v-loading="templateLoading"
      class="custom-report-view-content"
    >
      <ReportList :report-list="reportList" />
    </div>
  </div>
</template>

<script>
import ReportList from './components/reportList.vue'
import ReportQueryForm from './components/reportQueryForm.vue'
import {
  exportReport,
  findTemplate,
  findTemplateLevel,
  getIndexData,
  getTemplateList
} from './mockData'

export default {
  name: 'CustomReportView',
  components: {
    ReportList,
    ReportQueryForm
  },
  data() {
    return {
      templateList: [],
      reportList: [],
      templateLoading: false,
      queryLoading: false,
      exportLoading: false,
      hasQueried: false
    }
  },
  computed: {
    exportDisabled() {
      return !this.hasQueried || !this.reportList.length || this.queryLoading
    }
  },
  created() {
    this.loadTemplateList()
  },
  methods: {
    loadTemplateList() {
      this.templateLoading = true
      getTemplateList().then(data => {
        this.templateList = data
      }).finally(() => {
        this.templateLoading = false
      })
    },
    handleTemplateChange(templateCode) {
      this.hasQueried = false
      this.reportList = []
      if (!templateCode) return

      this.templateLoading = true
      findTemplate(templateCode).then(res => {
        this.reportList = this.createInitialReportList(res.indexList || [])
      }).finally(() => {
        this.templateLoading = false
      })
    },
    handleReset() {
      this.hasQueried = false
      this.reportList = this.reportList.map(item => ({
        ...item,
        loading: false,
        empty: false,
        emptyTxt: '',
        data: null
      }))
    },
    handleQuery(payload) {
      this.queryLoading = true
      this.hasQueried = false
      this.reportList = this.reportList.map(item => ({
        ...item,
        loading: true,
        empty: false,
        emptyTxt: '',
        data: null
      }))

      findTemplateLevel(payload).then(res => {
        const indexList = res.indexList || []
        this.reportList = this.createInitialReportList(indexList, true)
        return Promise.all(this.reportList.map(item => {
          return getIndexData({
            ...payload,
            indexCode: item.indexCode,
            indexName: item.indexName
          }).then(indexRes => {
            return {
              indexCode: item.indexCode,
              data: indexRes.Data
            }
          })
        }))
      }).then(resultList => {
        const dataMap = resultList.reduce((map, item) => {
          map[item.indexCode] = item.data
          return map
        }, {})

        this.reportList = this.reportList.map(item => {
          const data = dataMap[item.indexCode]
          return {
            ...item,
            loading: false,
            empty: !data,
            emptyTxt: data ? '' : '暂无数据',
            data
          }
        })
        this.hasQueried = true
      }).catch(() => {
        this.reportList = this.reportList.map(item => ({
          ...item,
          loading: false,
          empty: true,
          emptyTxt: '数据加载失败'
        }))
        this.$message.error('报告查询失败')
      }).finally(() => {
        this.queryLoading = false
      })
    },
    handleExport(payload) {
      this.exportLoading = true
      exportReport(payload).then(res => {
        if (res.State === 0) {
          this.$message.success(res.ErrMsg || '导出演示成功')
        } else {
          this.$message.error(res.ErrMsg || '导出失败')
        }
      }).finally(() => {
        this.exportLoading = false
      })
    },
    createInitialReportList(indexList, loading) {
      return indexList.map(item => ({
        ...item,
        loading: !!loading,
        empty: false,
        emptyTxt: '',
        data: null
      }))
    }
  }
}
</script>

<style lang="scss" scoped>
.custom-report-view {
  height: 100%;
  padding: 0 10px 12px;
  background: #f5f7fa;
  overflow-y: auto;

  .custom-report-view-content {
    min-height: 320px;
  }
}
</style>
