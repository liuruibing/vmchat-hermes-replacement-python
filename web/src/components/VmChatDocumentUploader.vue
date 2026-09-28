<template>
  <div class="vmchat-document-uploader">
    <input
      ref="fileInput"
      class="vmchat-document-uploader__input"
      type="file"
      accept="application/pdf,.pdf"
      @change="handleFileChange"
    />

    <div v-if="document" class="vmchat-document-uploader__card">
      <div class="vmchat-document-uploader__icon">
        <i class="el-icon-document" />
      </div>
      <div class="vmchat-document-uploader__meta">
        <strong :title="document.filename">{{ document.filename }}</strong>
        <span>
          {{ formatSize(document.size_bytes) }}
          <template v-if="document.page_count"> · {{ document.page_count }} 页</template>
        </span>
        <small>已上传，发送下一条消息时将使用 Mandate Risk AI 分析</small>
      </div>
      <button
        class="vmchat-document-uploader__remove"
        type="button"
        title="移除文件"
        :disabled="uploading"
        @click="removeDocument"
      >
        <i class="el-icon-close" />
      </button>
    </div>

    <button
      v-else
      class="vmchat-document-uploader__trigger"
      type="button"
      :disabled="uploading"
      title="上传 PDF 投资策略文件"
      @click="chooseFile"
    >
      <i :class="uploading ? 'el-icon-loading' : 'el-icon-paperclip'" />
      <span>{{ uploading ? '正在解析 PDF…' : '上传 PDF' }}</span>
    </button>
  </div>
</template>

<script>
import {
  clearPendingHermesDocument,
  getPendingHermesDocument,
  uploadHermesDocument
} from '@/api/hermesResearch'

export default {
  name: 'VmChatDocumentUploader',
  data() {
    return {
      uploading: false,
      document: getPendingHermesDocument()
    }
  },
  methods: {
    chooseFile() {
      if (this.uploading) return
      const input = this.$refs.fileInput
      if (!input) return
      input.value = ''
      input.click()
    },
    async handleFileChange(event) {
      const input = event && event.target
      const file = input && input.files && input.files[0]
      if (!file) return
      if (!/\.pdf$/i.test(file.name || '') || (file.type && file.type !== 'application/pdf')) {
        this.$message.error('当前只支持 PDF 文件')
        return
      }
      const maxBytes = 20 * 1024 * 1024
      if (file.size > maxBytes) {
        this.$message.error('PDF 文件不能超过 20 MB')
        return
      }

      this.uploading = true
      try {
        this.document = await uploadHermesDocument(file)
        this.$message.success('PDF 已上传并解析完成')
      } catch (error) {
        const responseError = error && error.response && error.response.data && error.response.data.error
        this.$message.error(responseError || (error && error.message) || 'PDF 上传失败')
      } finally {
        this.uploading = false
        if (input) input.value = ''
      }
    },
    removeDocument() {
      clearPendingHermesDocument()
      this.document = null
    },
    formatSize(value) {
      const bytes = Number(value || 0)
      if (!bytes) return '0 KB'
      if (bytes < 1024 * 1024) return Math.max(1, Math.round(bytes / 1024)) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    }
  }
}
</script>

<style scoped>
.vmchat-document-uploader {
  position: fixed;
  top: 78px;
  right: 28px;
  z-index: 2100;
  font-size: 13px;
}

.vmchat-document-uploader__input {
  display: none;
}

.vmchat-document-uploader__trigger {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  height: 34px;
  padding: 0 14px;
  border: 1px solid #dcdfe6;
  border-radius: 8px;
  background: #fff;
  color: #606266;
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  cursor: pointer;
}

.vmchat-document-uploader__trigger:hover:not(:disabled) {
  color: #409eff;
  border-color: #b3d8ff;
}

.vmchat-document-uploader__trigger:disabled {
  cursor: default;
  opacity: 0.75;
}

.vmchat-document-uploader__card {
  display: flex;
  align-items: center;
  width: 360px;
  min-height: 64px;
  padding: 10px 10px 10px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
}

.vmchat-document-uploader__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 36px;
  width: 36px;
  height: 36px;
  margin-right: 10px;
  border-radius: 8px;
  background: #ecf5ff;
  color: #409eff;
  font-size: 18px;
}

.vmchat-document-uploader__meta {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  gap: 2px;
}

.vmchat-document-uploader__meta strong {
  overflow: hidden;
  color: #303133;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.vmchat-document-uploader__meta span {
  color: #909399;
  font-size: 12px;
}

.vmchat-document-uploader__meta small {
  color: #67c23a;
  font-size: 11px;
  line-height: 1.35;
}

.vmchat-document-uploader__remove {
  flex: 0 0 28px;
  width: 28px;
  height: 28px;
  margin-left: 8px;
  border: 0;
  border-radius: 50%;
  background: transparent;
  color: #909399;
  cursor: pointer;
}

.vmchat-document-uploader__remove:hover:not(:disabled) {
  background: #f5f7fa;
  color: #f56c6c;
}
</style>
