<template>
  <div class="vm-chat-document-shell">
    <vm-chat-core ref="core" />

    <input
      ref="pdfInput"
      accept="application/pdf,.pdf"
      class="document-file-input"
      type="file"
      @change="handlePdfSelected"
    >

    <div class="document-dock">
      <button
        class="document-attach-button"
        type="button"
        :disabled="uploading || analysing"
        title="上传投资策略 PDF"
        @click="openPdfPicker"
      >
        <i class="el-icon-paperclip" />
        <span>{{ uploading ? '上传中…' : '上传 PDF' }}</span>
      </button>

      <div v-if="document" class="document-card">
        <div class="document-card__icon"><i class="el-icon-document" /></div>
        <div class="document-card__body">
          <div class="document-card__name" :title="document.filename">{{ document.filename }}</div>
          <div class="document-card__meta">
            <span v-if="document.page_count">{{ document.page_count }} 页</span>
            <span>{{ formatFileSize(document.size_bytes) }}</span>
            <span class="document-card__ready">已解析</span>
          </div>
        </div>
        <button
          class="document-card__remove"
          type="button"
          :disabled="analysing"
          title="移除附件"
          @click="clearDocument"
        >
          ×
        </button>
      </div>

      <div v-if="uploadError" class="document-error">{{ uploadError }}</div>
      <div v-if="document" class="document-hint">发送消息后将使用 Mandate 风险指标智能体分析此 PDF</div>
    </div>
  </div>
</template>

<script>
import VmChatCore from './VmChatCore.vue'
import {
  DEFAULT_DOCUMENT_PROMPT,
  sendMandateRiskDocumentRun,
  uploadHermesPdfDocument
} from '@/api/hermesDocuments'

function createDocumentChatMessage(role, content, extra) {
  return Object.assign({
    id: 'mandate-' + Date.now().toString(36) + '-' + Math.random().toString(16).slice(2),
    role,
    content: String(content || ''),
    thinking: '',
    thinkingExpanded: false,
    streamStatus: '',
    metricsSummary: '',
    debugCopied: false,
    debugPayload: null
  }, extra || {})
}

export default {
  name: 'VmChatDocumentShell',
  components: { VmChatCore },
  data() {
    return {
      document: null,
      uploading: false,
      analysing: false,
      uploadError: '',
      originalSendMessage: null
    }
  },
  mounted() {
    this.$nextTick(() => this.installDocumentSendHook())
  },
  beforeDestroy() {
    this.restoreDocumentSendHook()
  },
  methods: {
    getCore() {
      return this.$refs.core || null
    },
    installDocumentSendHook() {
      const core = this.getCore()
      if (!core || typeof core.sendMessage !== 'function' || this.originalSendMessage) return
      this.originalSendMessage = core.sendMessage
      core.sendMessage = this.handleCoreSend
    },
    restoreDocumentSendHook() {
      const core = this.getCore()
      if (core && this.originalSendMessage) core.sendMessage = this.originalSendMessage
      this.originalSendMessage = null
    },
    openPdfPicker() {
      if (this.uploading || this.analysing) return
      const input = this.$refs.pdfInput
      if (!input) return
      input.value = ''
      input.click()
    },
    async handlePdfSelected(event) {
      const file = event && event.target && event.target.files && event.target.files[0]
      if (!file) return
      this.uploadError = ''
      this.document = null
      if (!/\.pdf$/i.test(String(file.name || ''))) {
        this.uploadError = '当前只支持 PDF 文件'
        return
      }
      if (Number(file.size || 0) > 20 * 1024 * 1024) {
        this.uploadError = 'PDF 不能超过 20 MB'
        return
      }
      this.uploading = true
      try {
        this.document = await uploadHermesPdfDocument(file)
        const core = this.getCore()
        if (core && core.$message && core.$message.success) {
          core.$message.success('PDF 已上传并解析')
        }
      } catch (error) {
        this.uploadError = error && error.message ? error.message : 'PDF 上传失败'
        const core = this.getCore()
        if (core && core.$message && core.$message.error) core.$message.error(this.uploadError)
      } finally {
        this.uploading = false
      }
    },
    clearDocument() {
      if (this.analysing) return
      this.document = null
      this.uploadError = ''
      const input = this.$refs.pdfInput
      if (input) input.value = ''
    },
    formatFileSize(value) {
      const size = Number(value || 0)
      if (!size) return '0 KB'
      if (size < 1024 * 1024) return Math.max(1, Math.round(size / 1024)) + ' KB'
      return (size / 1024 / 1024).toFixed(1) + ' MB'
    },
    async handleCoreSend() {
      const core = this.getCore()
      if (!core) return
      if (!this.document) {
        if (typeof this.originalSendMessage === 'function') {
          return this.originalSendMessage()
        }
        return
      }
      if (this.uploading || this.analysing || core.sending) return

      const question = String(core.draftMessage || '').trim() || DEFAULT_DOCUMENT_PROMPT
      const attachmentName = String(this.document.filename || 'PDF')
      core.draftMessage = ''
      core.sending = true
      this.analysing = true

      const userMessage = createDocumentChatMessage(
        'user',
        '📎 **' + attachmentName + '**\n\n' + question,
        { documentId: this.document.document_id }
      )
      const assistantMessage = createDocumentChatMessage('assistant', '', {
        streamStatus: '正在分析 PDF…'
      })
      core.chatMessages.push(userMessage, assistantMessage)
      if (typeof core.scrollMessagesToBottom === 'function') core.scrollMessagesToBottom(true)

      const startedAt = Date.now()
      try {
        const result = await sendMandateRiskDocumentRun({
          documentId: this.document.document_id,
          question,
          sessionId: core.sessionId,
          model: core.analysisModel
        }, {
          onThinking: (delta, thinking) => {
            if (typeof core.updateAssistantMessage === 'function') {
              core.updateAssistantMessage(assistantMessage, {
                thinking,
                streamStatus: '正在分析风险指标…'
              })
            } else {
              assistantMessage.thinking = thinking
            }
            if (typeof core.scheduleMessagesScroll === 'function') core.scheduleMessagesScroll()
          },
          onContent: (delta, content) => {
            if (typeof core.updateAssistantMessage === 'function') {
              core.updateAssistantMessage(assistantMessage, {
                content,
                streamStatus: '正在生成匹配报告…'
              })
            } else {
              assistantMessage.content = content
            }
            if (typeof core.scheduleMessagesScroll === 'function') core.scheduleMessagesScroll()
          }
        })
        const finalContent = String(result && result.content || '').trim()
        const patch = {
          content: finalContent || assistantMessage.content || '风险指标分析已完成。',
          thinking: result && result.thinking || assistantMessage.thinking || '',
          streamStatus: '分析完成',
          metricsSummary: '总耗时 ' + ((Date.now() - startedAt) / 1000).toFixed(1) + 's'
        }
        if (typeof core.updateAssistantMessage === 'function') core.updateAssistantMessage(assistantMessage, patch)
        else Object.assign(assistantMessage, patch)
        this.clearDocument()
      } catch (error) {
        const message = error && error.message ? error.message : 'PDF 风险指标分析失败'
        const patch = {
          content: '**分析失败**\n\n' + message,
          streamStatus: '分析失败'
        }
        if (typeof core.updateAssistantMessage === 'function') core.updateAssistantMessage(assistantMessage, patch)
        else Object.assign(assistantMessage, patch)
        if (core.$message && core.$message.error) core.$message.error(message)
      } finally {
        this.analysing = false
        core.sending = false
        if (typeof core.scrollMessagesToBottom === 'function') core.scrollMessagesToBottom(true)
      }
    }
  }
}
</script>

<style scoped>
.vm-chat-document-shell {
  position: relative;
  min-height: 0;
}

.document-file-input {
  display: none;
}

.document-dock {
  position: fixed;
  right: 24px;
  bottom: 104px;
  z-index: 2200;
  width: min(360px, calc(100vw - 48px));
  pointer-events: none;
}

.document-attach-button,
.document-card,
.document-error,
.document-hint {
  pointer-events: auto;
}

.document-attach-button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-left: auto;
  padding: 7px 12px;
  border: 1px solid #c7d8ea;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.98);
  color: #315d88;
  font-size: 12px;
  cursor: pointer;
  box-shadow: 0 4px 14px rgba(34, 77, 121, 0.12);
}

.document-attach-button:hover:not(:disabled) {
  border-color: #409eff;
  color: #409eff;
}

.document-attach-button:disabled,
.document-card__remove:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.document-card {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 8px;
  padding: 10px 12px;
  border: 1px solid #d7e4f1;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 8px 22px rgba(34, 77, 121, 0.14);
}

.document-card__icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  border-radius: 8px;
  background: #eef6ff;
  color: #409eff;
  font-size: 18px;
}

.document-card__body {
  min-width: 0;
  flex: 1;
}

.document-card__name {
  overflow: hidden;
  color: #26384a;
  font-size: 13px;
  font-weight: 600;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.document-card__meta {
  display: flex;
  gap: 8px;
  margin-top: 4px;
  color: #7b8da0;
  font-size: 11px;
}

.document-card__ready {
  color: #38a169;
}

.document-card__remove {
  border: 0;
  background: transparent;
  color: #9aa9b7;
  font-size: 20px;
  line-height: 1;
  cursor: pointer;
}

.document-error,
.document-hint {
  margin-top: 6px;
  padding: 5px 8px;
  border-radius: 6px;
  background: rgba(255, 255, 255, 0.96);
  font-size: 11px;
}

.document-error {
  color: #d94b4b;
}

.document-hint {
  color: #6c7e90;
}

@media (max-width: 900px) {
  .document-dock {
    right: 16px;
    bottom: 96px;
    width: min(320px, calc(100vw - 32px));
  }
}
</style>
