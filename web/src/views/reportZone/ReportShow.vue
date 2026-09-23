<template>
  <div class="report-show-page">
    <!-- 顶部搜索区域 -->
    <div class="top-section">
      <div class="bg-container">
        <img class="bg-img" src="./img/背景0.png" alt="背景图" v-if="true" />
        <div class="search-box">
          <el-autocomplete
            v-model="searchKeyword"
            :fetch-suggestions="querySearch"
            placeholder="输入名称进行搜索"
            class="search-input"
            @select="handleSelect"
            clearable
          >
            <i slot="prefix" class="el-icon-search"></i>
          </el-autocomplete>
        </div>
      </div>
    </div>

    <!-- 底部报告展示区域 -->
    <div class="bottom-section">
      <div class="report-modules">
        <div class="report-module" v-for="(module, index) in reportModules" :key="index">
          <div class="module-header">
            <img class="module-bg" src="./img/背景2.png" alt="" />
            <div class="title-wrapper">
              <h3 class="module-title">{{ module.name }}</h3>
              <i class="module-desc" v-if="index == 0">动态跟踪私募产品运作表现</i>
              <i class="module-desc" v-if="index == 1">月度市场复盘与策略展望</i>
              <i class="module-desc" v-if="index == 2">穿透底层逻辑，挖掘收益与风险</i>
            </div>
            <img class="module-icon" src="./img/私募跟踪报告.png" alt="模块图标" v-if="index == 0" />
            <img class="module-icon" src="./img/市场策略月报.png" alt="模块图标" v-if="index == 1" />
            <img class="module-icon" src="./img/产品研究报告.png" alt="模块图标" v-if="index == 2" />
          </div>

          <div class="report-list" :class="{ 'show-more': module.showMore }">
            <div
              class="report-item"
              v-for="report in module.list"
              :key="report.fid"
              @click="previewReport(report)"
            >
              <span class="report-name" :title="report.vcReportName">{{ report.vcReportName }}</span>
              <img src="./img/导出.png" class="download-icon" @click.stop="downloadReport(report)" title="下载报告" alt="下载" />
            </div>
            <div class="report-item placeholder" v-for="n in getPlaceholderCount(module.list.length)" :key="'placeholder-' + n">
              <span class="report-name"></span>
            </div>
            <div
              class="more-btn"
              @click="module.showMore = true"
              v-if="module.list.length > 9 && !module.showMore"
            >
            查看更多
          </div>
        </div>
      </div>
    </div>
  </div>

  <el-dialog
    title="报告预览"
    :visible.sync="previewVisible"
    style="width:100%"
    append-to-body

    @close="handlePreviewClose"
  >
    <div class="preview-container">
      <div v-if="previewLoading" class="loading">加载中...</div>
      <div v-if="fileExt === 'pdf'">
        <iframe
          :src="previewUrl"
          style="z-index: 1000;height:650px;width:100%"
        ></iframe>
      </div>
      <div v-else-if="(fileExt === 'doc' || fileExt === 'docx') && useMammothFallback" class="mammoth-preview" v-html="mammothHtml"></div>
      <div v-else-if="fileExt === 'doc' || fileExt === 'docx'">
        <vue-office-docx
          :src="previewUrl"
          style="width: 100%; height: 650px"
          @rendered="handleDocxRendered"
          @error="handleDocxError"
        />
      </div>
      <div v-else-if="fileExt === 'ppt' || fileExt === 'pptx'">
        <vue-office-pptx
          :src="previewUrl"
          style="width: 100%; height: 650px"
          @rendered="handlePptxRendered"
          @error="handlePreviewError"
        />
      </div>
      <div v-else class="unsupported">
        暂不支持该类型（{{ fileExt }}）预览，可点击下载
        <el-button type="primary" size="small" @click="downloadCurrentReport">下载</el-button>
      </div>
    </div>
    <div slot="footer" class="dialog-footer">
      <el-button @click="previewVisible = false" type="info" size="small">关闭</el-button>
      <el-button type="primary" size="small" @click="downloadCurrentReport">下载</el-button>
    </div>
  </el-dialog>
  </div>
</template>

<script>
import reportZoneApi from '@/api/reportZone/index'
import commonApi from '@/api/common'
import VueOfficePptx from '@vue-office/pptx'
import VueOfficeDocx from '@vue-office/docx'
import '@vue-office/docx/lib/index.css'
import VueOfficePdf from '@vue-office/pdf'

export default {
  components: {
    VueOfficeDocx,
    VueOfficePptx,
    VueOfficePdf,
  },
  data() {
    return {
      searchKeyword: '',
      allReports: [],
      reportModules: [
        { type: '1', name: '私募跟踪报告', list: [], showMore: false },
        { type: '2', name: '市场策略月报', list: [], showMore: false },
        { type: '3', name: '产品研究报告', list: [], showMore: false }
      ],
      previewVisible: false,
      previewLoading: false,
      previewUrl: '',
      fileExt: '',
      currentReport: null,
      baseSrc: 'static',
      previewDocxBlob: null, // 用于 mammoth 兜底
      useMammothFallback: false,
      mammothHtml: ''
    }
  },
  mounted() {
    this.loadAllReportModules()
  },
  created() {
    if(process.env.NODE_ENV){
      if (process.env.NODE_ENV === "development") {
        // alert("开发环境");
        this.baseSrc = '/src/assets'
      }else {
        // alert("生产环境");
        this.baseSrc = 'static'
      }
    }
  },
  methods: {
    handleDocxRendered() {
      this.previewLoading = false
    },
    handlePptxRendered() {
      this.previewLoading = false
    },
    handlePreviewError(error) {
      console.error('文件预览错误:', error)
      this.$message.error(`预览失败: ${error.message || '无法加载文件'}`)
      this.previewLoading = false
    },
    // docx 预览失败时尝试 mammoth 兜底
    async handleDocxError(error) {
      console.error('vue-office docx 预览错误:', error)
      if (this.fileExt !== 'docx') {
        if(this.fileExt == 'doc') {
          this.$message.error(`该文档暂不支持在线预览，请点击下方「下载」按钮，使用 WPS 或 Word 打开查看。`)
          return
        }
        this.handlePreviewError(error)
        return
      }
      try {
        let arrayBuffer
        if (this.previewDocxBlob) {
          arrayBuffer = await this.previewDocxBlob.arrayBuffer()
        } else if (this.previewUrl) {
          const res = await fetch(this.previewUrl)
          arrayBuffer = await res.arrayBuffer()
        } else {
          throw new Error('无可用文件数据')
        }
        const mammoth = await import('mammoth')
        const result = await mammoth.default.convertToHtml({ arrayBuffer })
        this.mammothHtml = result.value
        this.useMammothFallback = true
        this.previewLoading = false
      } catch (mammothErr) {
        console.warn('mammoth 兜底预览失败:', mammothErr)
        let msg = error.message || '无法加载文件'
        if (msg.includes('central directory') || msg.includes('zip file')) {
          msg = '该文档暂不支持在线预览，请点击下方「下载」按钮，使用 WPS 或 Word 打开查看。'
        }
        this.$message.error(`预览失败: ${msg}`)
        this.previewLoading = false
      }
    },
    getPlaceholderCount(length) {
      const visibleCount = 9
      return length < visibleCount ? visibleCount - length : 0
    },
    // 加载报告数据
    async loadAllReportModules() {
      for (let module of this.reportModules) {
        try {
          const res = await reportZoneApi.selectFrontReportList(module.type)
          if (res.status === 200) {
            module.list = res.data.data || []
          }
        } catch (e) {
          this.$message.error('加载' + module.name + '失败：' + e.message)
        }
      }
      this.allReports = []
      this.reportModules.forEach(module => {
        this.allReports.push(...module.list)
      })
    },
    // 联想搜索
    querySearch(queryString, cb) {
      if (!queryString) {
        cb([])
        return
      }
      const results = this.allReports.filter(item => {
        return item.vcReportName && item.vcReportName.toLowerCase().indexOf(queryString.toLowerCase()) > -1
      })
      const formattedResults = results.map(item => ({
        value: item.vcReportName,
        fid: item.fid,
        ...item
      }))
      cb(formattedResults)
    },
    // 选中搜索结果
    handleSelect(item) {
      this.previewReport(item)
    },
    // 预览报告
    async previewReport(report) {
      this.currentReport = report
      this.previewVisible = true
      this.previewLoading = true
      this.useMammothFallback = false
      this.mammothHtml = ''
      this.previewDocxBlob = null
      this.fileExt = (report.vcAttachmentExt || '').toLowerCase().replace(/^\./, '')

      try {
        if ((report.vcAttachmentUrl && report.vcAttachmentUrl !== '')||(report.uuid && report.uuid !== '')) {
          const res = await reportZoneApi.downloadReport(report.fid)
          const blob = new Blob([res.data], { type: 'application/pdf' })
          const blobUrl = URL.createObjectURL(blob)
          if (this.fileExt === 'pdf') {
            this.previewUrl = blobUrl
          } else if (this.fileExt === 'doc') {
            this.$message.warning('旧版.doc格式不支持在线预览，请点击下载查看')
            this.previewVisible = false
            this.previewLoading = false
            URL.revokeObjectURL(blobUrl)
            return
          } else {
            this.previewUrl = blobUrl
            if (this.fileExt === 'docx') this.previewDocxBlob = blob
          }
        } else {
          this.$message.error('报告无附件，无法预览')
          this.previewVisible = false
        }
      } catch (e) {
        this.$message.error('预览失败：' + e.message)
        this.previewLoading = false
      } finally {
        if (this.fileExt !== 'docx' && this.fileExt !== 'doc' && this.fileExt !== 'ppt' && this.fileExt !== 'pptx') {
          this.previewLoading = false
        }
      }
    },
    // 下载报告
    async downloadReport(report) {
      this.currentReport = report
      await this.downloadCurrentReport()
    },
    // 下载当前报告
    async downloadCurrentReport() {
      if (!this.currentReport) return
      const { fid, uuid, vcAttachmentUrl, vcAttachmentName, vcAttachmentExt } = this.currentReport

      try {
          const res = await reportZoneApi.downloadReport(fid)
          const blob = new Blob([res.data], { type: 'application/octet-stream' })
          const href = URL.createObjectURL(blob)
          this.downloadFile(href, vcAttachmentName, vcAttachmentExt)
        this.$message.success('下载成功')
      } catch (e) {
        this.$message.error('下载失败：' + e.message)
      }
    },
    downloadFile(href, name, ext) {
      const a = document.createElement('a')
      a.href = href
      a.download = name ? name : `报告.${ext || ''}`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      if (href.startsWith('blob:')) {
        setTimeout(() => URL.revokeObjectURL(href), 5000)
      }
    },
    handlePreviewClose() {
      if (this.previewUrl && this.previewUrl.startsWith('blob:')) {
        URL.revokeObjectURL(this.previewUrl)
      }
      this.previewUrl = ''
      this.previewDocxBlob = null
      this.useMammothFallback = false
      this.mammothHtml = ''
      this.currentReport = null
    }
  }
}
</script>

<style lang="scss" scoped>
::v-deep .el-dialog {
  width: 90% !important;
  margin-top: 5vh !important;
}
::v-deep .dialog-footer {
  text-align: center !important;  // 按钮居中
}
.report-show-page {
  height: 100vh;
  background: #fff;
  //padding-top: 40px;
  //padding-bottom: 50px;
  box-sizing: border-box;

  // 顶部搜索区域
  .top-section {
    height: 178px;
    position: relative;
    .bg-container {
      width: 100%;
      height: 100%;
      position: relative;
      .bg-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
      .search-box {
        position: absolute;
        top: 50%;
        right: 20%;
        transform: translateY(-50%);
        width: 500px;

        .search-input {
          width: 100%;
          ::v-deep .el-input__inner {
            height: 42px;
            border-radius: 21px;
            padding-left: 40px;
            font-size: 16px;
            border: 1px solid #ddd;
          }
          ::v-deep .el-input__prefix {
            top: 50%;
            transform: translateY(-50%);
            height: 100%;
            display: flex;
            align-items: center;
            font-size: 20px;
            left: 15px;
            z-index: 10;
          }
          ::v-deep .el-autocomplete-suggestion {
            margin-top: 5px;
            border-radius: 8px;
            box-shadow: 0 4px 16px 0 rgba(0, 0, 0, 0.1);
            border: 1px solid #ebeef5;
            z-index: 999 !important;
            .el-autocomplete-suggestion__wrap {
              max-height: 200px;
            }
            .el-autocomplete-suggestion__item {
              padding: 12px 16px;
              font-size: 15px;
              &:hover {
                background: #f5f7fa;
              }
              &.selected {
                background: #e8f4ff;
              }
            }
          }
        }
      }
    }
  }

  .bottom-section {
    height: calc(100vh - 100px - 178px);
    padding: 40px 20px 70px 20px;
    display: flex;
    justify-content: center;
    .report-modules {
      display: flex;
      justify-content: center;
      gap: 55px;
      align-items: stretch;

      .report-module {
        width: 380px;
        flex: 0 0 380px;
        height: 100%;
        min-height: 400px;
        border: 1px solid #ebeef5;
        border-radius: 8px;
        padding: 0;
        position: relative;
        display: flex;
        flex-direction: column;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        transition: box-shadow 0.2s ease;
        &:hover {
          box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
        }

        .module-header {
          height: 132px;
          position: relative;
          border-bottom: 1px solid #ebeef5;
          .title-wrapper {
            position: absolute;
            top: 45%;
            left: 20px;
            transform: translateY(-50%);
            z-index: 2;
            display: flex;
            flex-direction: column;
            gap: 12px; // 标题和描述之间的间距
          }
          .module-bg {
            width: 100%;
            height: 100%;
            object-fit: cover;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 1;
            border-radius: 8px 8px 0 0;
          }
          .module-title {
            font-size: 28px;
            font-weight: 700;
            margin: 0;
            color: #333;
          }
          .module-desc {
            font-size: 14px;
            color: #666;
            font-style: normal;
          }
          .module-icon {
            width: 106px;
            height: 106px;
            position: absolute;
            right: 20px;
            bottom: -42.4px;
            z-index: 3;
            border-radius: 4px;
          }
        }

        .report-list {
          flex: 1;
          min-height: 200px;
          overflow: hidden;
          padding: 0 20px;
          margin-top: 42.4px;
          position: relative;

          &.show-more {
            overflow-y: auto;
            &::-webkit-scrollbar {
              width: 6px;
            }
            &::-webkit-scrollbar-track {
              background: #f5f7fa;
              border-radius: 3px;
            }
            &::-webkit-scrollbar-thumb {
              background: #dcdfe6;
              border-radius: 3px;
              &:hover {
                background: #c0c4cc;
              }
            }
          }

          .report-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px dashed #f0f0f0;
            cursor: pointer;
            height: 40px; // 行高改为40px

            &.placeholder {
              border-bottom: none;
              cursor: default;
            }

            .report-name {
              flex: 1;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
              font-size: 14px;
            }

            .report-item:not(.placeholder) .report-name {
              cursor: pointer;
            }

            .download-icon {
              margin-left: 10px;
              width: 18px;
              height: 13px;
              cursor: pointer;
              vertical-align: middle;
            }
          }

          .more-btn {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            text-align: center;
            color: #b1b1b1;
            cursor: pointer;
            padding: 10px 0;
            font-size: 14px;
            border-radius: 8px;
            //font-weight: 700;
            background: #fff;
            border-top: 1px solid #f5f7fa;
            &:hover {
              color: #b1b1b1;
              background: #f8f9fa;
            }
          }
        }
      }
    }
  }

  // 预览弹框样式
  .preview-container {
    height: 600px;
    position: relative;
    .loading {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      font-size: 18px;
    }
    .pdf-preview {
      width: 100%;
      height: 100%;
    }
    .doc-preview, .ppt-preview {
      width: 100%;
      height: 100%;
    }
    .mammoth-preview {
      width: 100%;
      height: 650px;
      overflow-y: auto;
      padding: 20px 40px;
      font-size: 14px;
      line-height: 1.6;
      &::-webkit-scrollbar {
        width: 6px;
      }
      &::-webkit-scrollbar-track {
        background: #f5f7fa;
        border-radius: 3px;
      }
      &::-webkit-scrollbar-thumb {
        background: #dcdfe6;
        border-radius: 3px;
      }
      ::v-deep p { margin: 0 0 0.5em; }
      ::v-deep table { border-collapse: collapse; margin: 1em 0; }
      ::v-deep td, ::v-deep th { border: 1px solid #ddd; padding: 6px 10px; }
      ::v-deep ul, ::v-deep ol { margin: 0.5em 0; padding-left: 1.5em; }
    }
    .unsupported {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
    }
  }
}
</style>
