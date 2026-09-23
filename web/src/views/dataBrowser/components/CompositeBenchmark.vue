<!--
 * @Description: 复合基准设置弹窗组件
 * @Author:
 * @Date: 2025-05-22
-->
<template>
  <div class="composite-benchmark-wrapper">
    <el-dialog :visible.sync="dialogVisible" title="复合基准设置" custom-class="composite-benchmark-dialog"
      :close-on-click-modal="false" :close-on-press-escape="false" @closed="handleClose" width="960px !important">

      <div class="benchmark-body">
        <!-- 左侧：指数列表 -->
        <div class="benchmark-left">
          <el-input v-model="searchText" placeholder="输入指数名称或代码..." prefix-icon="el-icon-search" size="small"
            clearable style="width: 94% !important; margin: 0 auto 10px auto;"></el-input>
          <div class="index-list">
            <div v-for="item in filteredIndexList" :key="item.code"
              :class="['index-item', { 'is-selected': isIndexSelected(item) }]" @click="handleAddIndex(item)">
              <div class="index-info">
                <div class="index-name">{{ item.name }}</div>
                <div class="index-code">{{ item.code }}</div>
              </div>
              <i v-if="!isIndexSelected(item)" class="el-icon-circle-plus add-icon"></i>
              <i v-else class="el-icon-success added-icon"></i>
            </div>
            <div v-if="filteredIndexList.length === 0" class="empty-list">
              <span>暂无匹配的指数</span>
            </div>
          </div>
        </div>

        <!-- 中间：配置工作台 -->
        <div class="benchmark-center">
          <div class="center-header">
            <span class="center-title">配置工作台</span>
            <el-tooltip content="通过分配权重来定义您的自定义指数。" placement="top" effect="light">
              <i class="el-icon-info info-icon"></i>
            </el-tooltip>
          </div>
          <div class="config-table-wrapper">
            <vxe-table ref="configTable" :data="selectedList" auto-resize show-overflow="tooltip" stripe
              style="width: 100%" empty-text="" height="300px">
              <vxe-table-column field="name" title="指数名称" min-width="140" header-align="center" align="left"
                show-overflow="tooltip"></vxe-table-column>
              <vxe-table-column field="code" title="代码" min-width="120" header-align="center"
                align="center"></vxe-table-column>
              <vxe-table-column title="权重 (%)" width="110" header-align="center" align="center">
                <template slot-scope="{ row }">
                  <el-input-number v-model="row.weight" :min="0" :max="100" :precision="2" :controls="false"
                    size="small" class="weight-input" @change="onWeightChange"></el-input-number>
                </template>
              </vxe-table-column>
              <vxe-table-column title="操作" width="60" header-align="center" align="center">
                <template slot-scope="{ $rowIndex }">
                  <i class="el-icon-delete delete-icon" @click="handleRemoveIndex($rowIndex)"></i>
                </template>
              </vxe-table-column>
            </vxe-table>
          </div>
          <!-- 总权重 -->
          <div class="weight-summary" v-if="selectedList.length > 0">
            <div class="weight-total" :class="{ 'is-valid': totalWeight === 100, 'is-invalid': totalWeight !== 100 }">
              <i :class="totalWeight === 100 ? 'el-icon-success' : 'el-icon-warning'"></i>
              <span>总权重: {{ totalWeight }}%</span>
            </div>
            <span class="asset-count">已包含 {{ selectedList.length }} 个资产</span>
          </div>
          <!-- 保存为预设基准 -->
          <div class="save-preset" v-if="selectedList.length > 0">
            <div>保存为常用复合基准</div>
            <div class="save-preset-form">
              <el-input v-model="presetName" placeholder="名称" size="small"
                class="preset-name-input"></el-input>
              <el-button size="small" @click="handleSavePreset" :disabled="!presetName.trim()">保存</el-button>
            </div>
          </div>
        </div>

        <!-- 右侧：预设模板 -->
        <div class="benchmark-right">
          <el-input v-model="presetSearchText" placeholder="搜索常用预设..." prefix-icon="el-icon-search" size="small"
            clearable style="width: 94% !important; margin: 0 auto 10px auto;"></el-input>
          <div class="preset-list">
            <div v-for="(preset, index) in filteredPresetList" :key="preset.id" class="preset-card">
              <div class="preset-card-header">
                <span class="preset-name">{{ preset.name }}</span>
                <div class="preset-actions">
                  <i class="el-icon-delete" @click="handleDeletePreset(index)" title="删除"></i>
                  <i :class="['star-icon', preset.starred ? 'el-icon-star-on' : 'el-icon-star-off']"
                    @click="handleToggleStar(preset)" :title="preset.starred ? '取消收藏' : '收藏'"></i>
                </div>
              </div>
              <div class="preset-desc">{{ preset.description }}</div>
              <el-button size="mini" class="use-template-btn" @click="handleUseTemplate(preset)">使用模板</el-button>
            </div>
            <div v-if="filteredPresetList.length === 0" class="empty-list">
              <span>暂无匹配的预设</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 底部按钮 -->
      <div slot="footer" class="dialog-footer">
        <el-button @click="handleCancel" size="small">取消</el-button>
        <el-button type="primary" @click="handleConfirm" size="small"
          :disabled="totalWeight !== 100 || selectedList.length === 0">确认应用</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'CompositeBenchmark',
  props: {
    // 指数列表数据源
    indexList: {
      type: Array,
      default: () => []
    },
    // 预设模板列表
    presetList: {
      type: Array,
      default: () => []
    },
    // 回显数据：已选的基准配置
    value: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      dialogVisible: false,
      searchText: '',
      presetSearchText: '',
      selectedList: [], // [{ name, code, weight }]
      presetName: '',
      localPresetList: []
    }
  },
  computed: {
    filteredIndexList() {
      if (!this.searchText) return this.indexList
      const keyword = this.searchText.toLowerCase()
      return this.indexList.filter(item =>
        item.name.toLowerCase().includes(keyword) || item.code.toLowerCase().includes(keyword)
      )
    },
    filteredPresetList() {
      if (!this.presetSearchText) return this.localPresetList
      const keyword = this.presetSearchText.toLowerCase()
      return this.localPresetList.filter(item =>
        item.name.toLowerCase().includes(keyword) || (item.description && item.description.toLowerCase().includes(keyword))
      )
    },
    totalWeight() {
      return this.selectedList.reduce((sum, item) => sum + (Number(item.weight) || 0), 0)
    }
  },
  watch: {
    presetList: {
      handler(val) {
        this.localPresetList = _.cloneDeep(val || [])
      },
      immediate: true
    }
  },
  methods: {
    /** 打开弹窗 */
    open(data) {
      this.dialogVisible = true
      this.searchText = ''
      this.presetSearchText = ''
      this.presetName = ''
      // 回显已选配置
      if (data && data.length > 0) {
        this.selectedList = _.cloneDeep(data)
      } else if (this.value && this.value.length > 0) {
        this.selectedList = _.cloneDeep(this.value)
      } else {
        this.selectedList = []
      }
    },
    /** 关闭弹窗 */
    handleClose() {
      this.dialogVisible = false
      this.$emit('close')
    },
    /** 取消 */
    handleCancel() {
      this.dialogVisible = false
    },
    /** 确认应用 */
    handleConfirm() {
      if (this.totalWeight !== 100) {
        this.$message.warning('总权重必须为 100%')
        return
      }
      if (this.selectedList.length === 0) {
        this.$message.warning('请至少选择一个指数')
        return
      }
      const result = _.cloneDeep(this.selectedList)
      this.$emit('input', result)
      this.$emit('confirm', result)
      this.dialogVisible = false
    },
    /** 判断指数是否已选 */
    isIndexSelected(item) {
      return this.selectedList.some(s => s.code === item.code)
    },
    /** 添加指数到配置工作台 */
    handleAddIndex(item) {
      if (this.isIndexSelected(item)) return
      this.selectedList.push({
        name: item.name,
        code: item.code,
        weight: 0
      })
    },
    /** 从配置工作台移除指数 */
    handleRemoveIndex(index) {
      this.selectedList.splice(index, 1)
    },
    /** 权重变化 */
    onWeightChange() {
      // 可按需添加权重自动平衡逻辑
    },
    /** 保存为预设 */
    handleSavePreset() {
      if (!this.presetName.trim()) {
        this.$message.warning('请输入预设名称')
        return
      }
      if (this.selectedList.length === 0) {
        this.$message.warning('请至少选择一个指数')
        return
      }
      const preset = {
        id: 'preset_' + Date.now(),
        name: this.presetName.trim(),
        description: this.selectedList.map(s => `${s.name}(${s.weight}%)`).join('、'),
        starred: false,
        items: _.cloneDeep(this.selectedList)
      }
      this.localPresetList.unshift(preset)
      this.$emit('save-preset', preset)
      this.$message.success('预设保存成功')
      this.presetName = ''
    },
    /** 使用模板 */
    handleUseTemplate(preset) {
      if (preset.items && preset.items.length > 0) {
        this.selectedList = _.cloneDeep(preset.items)
      }
    },
    /** 删除预设 */
    handleDeletePreset(index) {
      this.$confirm('确定删除该预设模板吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        const removed = this.localPresetList.splice(index, 1)[0]
        this.$emit('delete-preset', removed)
        this.$message.success('删除成功')
      }).catch(() => { })
    },
    /** 切换收藏 */
    handleToggleStar(preset) {
      preset.starred = !preset.starred
      this.$emit('toggle-star', preset)
    }
  }
}
</script>

<style lang="scss">
.composite-benchmark-dialog {
  border-radius: 8px;

  .el-dialog__header {
    padding: 16px 20px;
    border-bottom: 1px solid #e4e7ed;
    margin-right: 0;
  }

  .el-dialog__body {
    padding: 0;
  }

  .el-dialog__footer {
    padding: 12px 20px;
    border-top: 1px solid #e4e7ed;
  }

  .benchmark-body {
    display: flex;
    height: 480px;
    min-height: 420px;
  }

  /* ===== 左侧：指数列表 ===== */
  .benchmark-left {
    width: 220px;
    flex-shrink: 0;
    border-right: 1px solid #e4e7ed;
    display: flex;
    flex-direction: column;
    background: #fafbfc;

    .index-list {
      flex: 1;
      overflow-y: auto;
      padding: 0 4px;

      .index-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px;
        cursor: pointer;
        border-radius: 4px;
        transition: background-color 0.2s;
        margin-bottom: 2px;

        &:hover {
          background-color: #ecf5ff;
        }

        &.is-selected {
          background-color: #f0f7ff;
        }

        .index-info {
          flex: 1;
          min-width: 0;

          .index-name {
            font-size: 13px;
            font-weight: 500;
            color: #303133;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }

          .index-code {
            font-size: 11px;
            color: #909399;
            margin-top: 2px;
          }
        }

        .add-icon {
          font-size: 18px;
          color: #409eff;
          flex-shrink: 0;
          margin-left: 8px;
          opacity: 0;
          transition: opacity 0.2s;
        }

        &:hover .add-icon {
          opacity: 1;
        }

        .added-icon {
          font-size: 16px;
          color: #67c23a;
          flex-shrink: 0;
          margin-left: 8px;
        }
      }

      .empty-list {
        text-align: center;
        padding: 40px 12px;
        color: #c0c4cc;
        font-size: 13px;
      }
    }
  }

  /* ===== 中间：配置工作台 ===== */
  .benchmark-center {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-width: 0;
    padding: 0;

    .center-header {
      display: flex;
      align-items: center;
      padding: 12px 16px 8px;

      .center-title {
        font-size: 14px;
        font-weight: 600;
        color: #303133;
      }

      .info-icon {
        font-size: 14px;
        color: #c0c4cc;
        margin-left: 6px;
        cursor: pointer;

        &:hover {
          color: #409eff;
        }
      }
    }

    .config-table-wrapper {
      flex: 1;
      overflow-y: auto;
      padding: 0 16px;

      .vxe-table {
        .weight-input {
          width: 100%;

          .el-input {
            width: 100% !important;
          }
        }

        .delete-icon {
          font-size: 16px;
          color: #f56c6c;
          cursor: pointer;
          transition: color 0.2s;

          &:hover {
            color: #e6303e;
          }
        }
      }

      .table-empty {
        .empty-placeholder {
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
          padding: 60px 20px;
          color: #c0c4cc;

          i {
            font-size: 36px;
            margin-bottom: 12px;
          }

          p {
            font-size: 13px;
            margin: 0;
          }
        }
      }
    }

    .weight-summary {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 10px 16px;
      border-top: 1px solid #ebeef5;

      .weight-total {
        display: flex;
        align-items: center;
        font-size: 13px;
        font-weight: 600;

        i {
          margin-right: 6px;
          font-size: 16px;
        }

        &.is-valid {
          color: #67c23a;
        }

        &.is-invalid {
          color: #e6a23c;
        }
      }

      .asset-count {
        font-size: 12px;
        color: #909399;
      }
    }

    .save-preset {
      padding: 8px 16px 12px;
      border-top: 1px solid #ebeef5;

      .el-checkbox {
        font-size: 13px;

        .el-checkbox__label {
          font-size: 13px;
        }
      }

      .save-preset-form {
        display: flex;
        align-items: center;
        margin-top: 8px;
        gap: 8px;

        .preset-name-input {
          flex: 1;
        }
      }
    }
  }

  /* ===== 右侧：预设模板 ===== */
  .benchmark-right {
    width: 240px;
    flex-shrink: 0;
    border-left: 1px solid #e4e7ed;
    display: flex;
    flex-direction: column;
    background: #fafbfc;

    .preset-list {
      flex: 1;
      overflow-y: auto;
      padding: 4px 12px;

      .preset-card {
        background: #fff;
        border: 1px solid #e4e7ed;
        border-radius: 6px;
        padding: 12px;
        margin-bottom: 10px;
        transition: box-shadow 0.2s, border-color 0.2s;

        &:hover {
          border-color: #c0c4cc;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }

        .preset-card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;

          .preset-name {
            font-size: 13px;
            font-weight: 600;
            color: #303133;
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
          }

          .preset-actions {
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;

            i {
              font-size: 14px;
              color: #c0c4cc;
              cursor: pointer;
              transition: color 0.2s;

              &:hover {
                color: #409eff;
              }
            }

            .star-icon.el-icon-star-on {
              color: #e6a23c;
            }
          }
        }

        .preset-desc {
          font-size: 12px;
          color: #909399;
          margin-top: 6px;
          line-height: 1.5;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
        }

        .use-template-btn {
          margin-top: 10px;
          width: 100%;
        }
      }

      .empty-list {
        text-align: center;
        padding: 40px 12px;
        color: #c0c4cc;
        font-size: 13px;
      }
    }
  }

  /* ===== 底部 ===== */
  .dialog-footer {
    text-align: right;
  }
}
</style>
