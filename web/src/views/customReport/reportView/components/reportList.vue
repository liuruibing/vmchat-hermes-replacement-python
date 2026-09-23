<template>
  <div class="custom-report-list">
    <el-empty
      v-if="!reportList.length"
      description="暂无报告内容"
    />
    <div
      v-else
      id="downSign"
      class="report-content"
    >
      <el-card
        v-for="item in reportList"
        :key="item.indexCode"
        class="report-card"
        shadow="never"
      >
        <div
          slot="header"
          class="report-card-title"
        >
          {{ item.indexName }}
        </div>
        <div
          v-loading="item.loading"
          class="report-card-body"
        >
          <div
            v-if="item.empty"
            class="report-empty"
          >
            <el-empty :description="item.emptyTxt || '暂无数据'" />
          </div>
          <div
            v-show="!item.empty"
            :key="item.indexCode + renderKey"
            v-html="item.html"
          />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
  name: 'ReportList',
  props: {
    reportList: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      renderKey: 0,
      scriptTimer: null
    }
  },
  watch: {
    reportList: {
      handler() {
        this.renderKey += 1
        this.renderScripts()
      },
      deep: true,
      immediate: true
    }
  },
  mounted() {
    window.echarts = echarts
  },
  beforeDestroy() {
    clearTimeout(this.scriptTimer)
    this.removeScripts()
  },
  methods: {
    renderScripts() {
      clearTimeout(this.scriptTimer)
      this.removeScripts()
      this.scriptTimer = setTimeout(() => {
        this.$nextTick(() => {
          this.appendScripts()
        })
      }, 120)
    },
    appendScripts() {
      this.reportList.forEach(item => {
        if (!item.jsContent || item.empty || item.loading) return
        this.createScript(item.jsContent, item.data)
      })
    },
    createScript(jsStr, data) {
      const script = document.createElement('script')
      let codes = jsStr
        .replace(new RegExp('<script>', 'g'), '')
        .replace(new RegExp('</s' + 'cript>', 'g'), '')

      script.type = 'text/javascript'
      script.className = 'customScript'
      codes = codes.replace(/\$\{rootData\}/g, JSON.stringify(data || {}))

      try {
        script.appendChild(document.createTextNode(codes.toString()))
      } catch (error) {
        script.text = codes.toString()
      }

      document.body.appendChild(script)
    },
    removeScripts() {
      const tagElements = document.getElementsByTagName('script')
      for (let index = tagElements.length - 1; index >= 0; index--) {
        if (tagElements[index].className === 'customScript') {
          tagElements[index].parentNode.removeChild(tagElements[index])
        }
      }
    }
  }
}
</script>

<style lang="scss" scoped>
.custom-report-list {
  min-height: 260px;

  .report-content {
    width: 100%;
    margin: 0 auto;
  }

  .report-card {
    margin-bottom: 10px;
    border-radius: 4px;
  }

  .report-card-title {
    font-size: 15px;
    font-weight: 600;
    color: #303133;
    border-left: 3px solid #409eff;
    padding-left: 8px;
    line-height: 18px;
  }

  .report-card-body {
    min-height: 220px;
  }

  .report-empty {
    padding: 20px 0;
  }

  ::v-deep .demo-chart {
    width: 100%;
    height: 320px;
  }

  ::v-deep .demo-table {
    width: 100%;
    border-collapse: collapse;
    color: #606266;
    font-size: 13px;

    th,
    td {
      border: 1px solid #ebeef5;
      padding: 11px 12px;
      text-align: left;
    }

    th {
      background: #f5f7fa;
      color: #303133;
      font-weight: 600;
    }
  }
}
</style>
