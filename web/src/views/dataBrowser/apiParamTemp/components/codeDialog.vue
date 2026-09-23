<template>
  <el-dialog :visible.sync="localVisible" title="生成代码" width="70% !important" :close-on-click-modal="false" @closed="handleClose">
    <el-tabs v-model="activeTab" type="border-card">
      <el-tab-pane label="Java代码" name="java">
        <div class="code-content">
          <pre class="code-block">{{ javaCode }}</pre>
        </div>
        <div class="code-actions">
          <el-button type="primary" size="small" @click="copyToClipboard(javaCode)">复制Java代码</el-button>
        </div>
      </el-tab-pane>
      <el-tab-pane label="Python代码" name="python">
        <div class="code-content">
          <pre class="code-block">{{ pythonCode }}</pre>
        </div>
        <div class="code-actions">
          <el-button type="primary" size="small" @click="copyToClipboard(pythonCode)">复制Python代码</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </el-dialog>
</template>

<script>
export default {
  name: 'CodeDialog',
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    javaCode: {
      type: String,
      default: ''
    },
    pythonCode: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      activeTab: 'java'
    }
  },
  computed: {
    localVisible: {
      get() {
        return this.visible
      },
      set(val) {
        this.$emit('update:visible', val)
      }
    }
  },
  watch: {
    visible(val) {
      if (val) {
        this.activeTab = 'java'
      }
    }
  },
  methods: {
    handleClose() {
      this.$emit('close')
    },
    copyToClipboard(text) {
      navigator.clipboard.writeText(text)
        .then(() => {
          this.$message.success('复制成功')
        })
        .catch(() => {
          this.$message.error('复制失败')
        })
    }
  }
}
</script>

<style lang="scss" scoped>
.code-content {
  max-height: 500px;
  overflow-y: auto;
  background: #f5f5f5;
  border-radius: 4px;
  padding: 16px;

  .code-block {
    margin: 0;
    font-size: 12px;
    font-family: 'Courier New', Courier, monospace;
    white-space: pre-wrap;
    word-wrap: break-word;
  }
}

.code-actions {
  margin-top: 16px;
  text-align: right;
}
</style>
