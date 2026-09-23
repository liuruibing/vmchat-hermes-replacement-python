<template>
  <div class="temp-config-wrapper" v-loading="loading">
    <!-- 顶部模板基础表单 -->
    <div class="top-form-area" v-if="modelType !== '4'">
      <el-form :inline="true" :model="configForm" size="small" :rules="rules" ref="topFormRef" label-width="auto" class="config-form">
        <el-form-item label="模板名称" prop="templateName">
          <el-input v-model.trim="configForm.templateName" placeholder="请填写模板名称" style="width: 250px;"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="btnDisabled" @click="handleSave">保存</el-button>
          <el-button type="info" @click="handleCancel" :disabled="btnDisabled">取消</el-button>
        </el-form-item>
      </el-form>
      <!-- <el-divider style="margin: 10px 0;"></el-divider> -->
    </div>

    <!-- 主体：三列布局 -->
    <div class="tempConfig-container" :class="{'is-preview': modelType === '4', 'is-resizing': isDraggingLeft || isDraggingCenter}">
      
      <!-- 左侧：指标树 (非预览时可见) -->
      <div v-show="modelType !== '4'" class="tempConfig-left" :style="{ width: leftCollapsed ? '40px' : leftWidth + 'px' }" :class="{ 'is-collapsed': leftCollapsed }">
        <div class="tempConfig-title">
          <span v-show="!leftCollapsed">指标列表</span>
          <i class="collapse-icon" :class="leftCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" @click="toggleLeft" :title="leftCollapsed ? '展开' : '收起'"></i>
        </div>
        <div class="collapsed-text" v-show="leftCollapsed" @click="toggleLeft" title="展开指标列表">指标列表</div>
        <div class="tree-search-box" v-show="!leftCollapsed">
          <el-input v-model="filterText" placeholder="搜索" prefix-icon="el-icon-search" size="small" clearable style="width: 100% !important;"></el-input>
        </div>
        <div class="tempConfig-content" v-show="!leftCollapsed">
          <el-tree
            class="report-index-tree"
            ref="indexTree"
            :data="treeData"
            show-checkbox
            node-key="vcCode"
            :props="treeProps"
            :filter-node-method="filterNode"
            :default-expanded-keys="expandedKeys"
            :default-checked-keys="checkedTreeKeys"
            :check-strictly="false"
            @check="onTreeCheck"
            style="user-select: none;"
          >
            <span :class="['custom-tree-node', node.isLeaf ? 'leaf-node' : 'parent-node']" slot-scope="{ node }">
              <i :class="node.isLeaf ? 'el-icon-document' : 'el-icon-folder'"></i>
              <span v-html="highlightKeyword(node.label)"></span>
            </span>
          </el-tree>
        </div>
      </div>

      <!-- 拖拽把手 (非预览时可见) -->
      <div class="resize-handle" v-show="modelType !== '4' && !leftCollapsed" @mousedown.prevent="startDragLeft" title="拖拽调整宽度"></div>

      <!-- 中间：已选指标列表 (可拖拽排序) (非预览时可见) -->
      <div v-show="modelType !== '4'" class="tempConfig-center" :style="{ width: centerCollapsed ? '40px' : centerWidth + 'px' }" :class="{ 'is-collapsed': centerCollapsed }">
        <div class="tempConfig-title">
          <span v-show="!centerCollapsed">已选指标</span>
          <i class="collapse-icon" :class="centerCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" @click="toggleCenter" :title="centerCollapsed ? '展开' : '收起'"></i>
        </div>
        <div class="collapsed-text" v-show="centerCollapsed" @click="toggleCenter" title="展开指标">已选指标</div>
        <div class="tempConfig-content" v-show="!centerCollapsed">
          <draggable v-model="checkList" :options="{ animation: 200, ghostClass: 'sortable-ghost' }" @end="onDragEnd">
            <div 
              v-for="(item, index) in checkList" 
              :key="item.key" 
              class="draggable-item"
              @click="scrollToPreview(item.key)"
            >
              <el-tag closable @close="deleteItem(item, index)" type="info" effect="plain" class="index-tag" :title="item.vcIndexName">
                <span class="index-tag-label">{{ item.vcIndexName }}</span>
                <span class="sort-arrows">
                  <i class="el-icon-top sort-arrow" :class="{ 'is-disabled': index === 0 }" @click.stop="index > 0 && moveUp(index)" title="上移"></i>
                  <i class="el-icon-bottom sort-arrow" :class="{ 'is-disabled': index === checkList.length - 1 }" @click.stop="index < checkList.length - 1 && moveDown(index)" title="下移"></i>
                </span>
              </el-tag>
            </div>
          </draggable>
        </div>
      </div>

      <div class="resize-handle" v-show="modelType !== '4' && !centerCollapsed" @mousedown.prevent="startDragCenter" title="拖拽调整宽度"></div>

      <!-- 右侧：预览区域 -->
      <div class="tempConfig-right">
        <div class="tempConfig-title">
           模板预览
        </div>
        <div class="preview-container" id="previewContainer">
          <el-collapse v-model="activeCollapseKeys">
            <draggable v-model="checkList" :options="{ animation: 200, ghostClass: 'sortable-ghost-preview', disabled: modelType === '4' }" @end="onDragEnd">
              <el-collapse-item 
                v-for="item in checkList" 
                :key="item.key" 
                :name="item.key" 
                :id="'Collapse_' + item.key"
              >
                <template slot="title">
                   <span>{{ item.vcIndexName }}</span>
                   <i v-if="modelType !== '4'" class="el-icon-circle-close close-icon" @click.stop="deleteItem(item)"></i>
                </template>
                <div v-html="item.html" :key="item.key + 'report'"></div>
              </el-collapse-item>
            </draggable>
          </el-collapse>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import pageApi from '../scripts/api'
import draggable from 'vuedraggable'
import * as echarts from 'echarts'
import $ from 'jquery'

window.$ = $;
window.jQuery = $;
window.echarts = echarts;

// 树形结构转换工具
const delDepartTree = (data, _id = 'id', _pId = 'pId') => {
  const obj = {}
  const res = []
  const len = data.length
  const children = 'children'
  for (let i = 0; i < len; i++) {
    obj[data[i][_id]] = data[i]
  }
  for (let j = 0; j < len; j++) {
    const list = data[j]
    const parentList = obj[list[_pId]]
    if (parentList) {
      if (!parentList[children]) {
        parentList[children] = []
      }
      parentList[children].push(list)
    } else {
      res.push(list)
    }
  }
  return res
}

// 自定义模板固定封面、声明 指标id
const coverId = '8cf9997c-e5c4-40e9-8d79-660e61d323ce';
const declarationId = '8c5e1a7e-bc6a-471a-b7f9-ba927ed19526';

export default {
  name: 'TempConfig',
  components: {
    draggable
  },
  props: {
    modelType: String, // 1(新增)、2(编辑)、3(复制新增)、4(预览)
    vcTemplateId: String,
    rowData: {
      type: Object,
      default: () => ({})
    }
  },
  data() {
    return {
      loading: false,
      btnDisabled: false,
      configForm: {
        templateName: ''
      },
      rules: {
         templateName: [{ required: true, message: '请填写模板名称', trigger: 'change' }]
      },
      
      leftWidth: 240,
      centerWidth: 260,
      isDraggingLeft: false,
      isDraggingCenter: false,
      startX: 0,
      startLeftWidth: 0,
      startCenterWidth: 0,
      leftCollapsed: false,
      centerCollapsed: false,
      filterText: '',
      
      treeDataAll: [], // 所有打平转树的数据
      treeData: [],    // 当前显示的树
      expandedKeys: [],
      checkedTreeKeys: [],
      
      checkList: [], // { key, vcIndexName, html, indexOrder }
      oldCheckKeys: [], // 用于跟踪已执行过脚本的指标key
      activeCollapseKeys: []
    }
  },
  watch: {
    filterText(val) {
      this.$refs.indexTree && this.$refs.indexTree.filter(val)
    },
    checkList: {
      handler(newVal, oldVal) {
        // 当已选列表变更时，执行新增指标的脚本
        this.executeNewScripts()
      },
      deep: true
    }
  },
  computed: {
    treeProps() {
      return {
        label: 'vcIndexName',
        children: 'children',
        disabled: (data, node) => {
          // 只针对子节点（叶子节点），vcIndexType !== '1' 时禁用勾选
          if (node.isLeaf) {
            return data.vcIndexType !== '1'
          }
          return false
        }
      }
    }
  },
  created() {
    // 回显示 form 数据
    window.echarts = echarts
    if (['2', '3', '4'].includes(this.modelType)) {
      this.configForm.templateName = this.modelType === '3' ? '' : (this.rowData.templateName || '')
    }
    this.getTreeList()
  },
  beforeDestroy() {
    document.removeEventListener('mousemove', this.onDragLeft)
    document.removeEventListener('mousemove', this.onDragCenter)
    document.removeEventListener('mouseup', this.stopDrag)
  },
  destroyed() {
    this.removeScripts()
  },
  methods: {
    // 获取指标字典树
    getTreeList() {
      this.loading = true;
      pageApi.getIndexTree({}).then(res => {
        const { status, data } = res.data;
        if (status === 200 && data) {
          // this.treeDataAll = delDepartTree(data, 'vcCode', 'vcParentCode')
          this.treeData = delDepartTree(data, 'vcCode', 'vcParentCode')
          // 编辑、复制新增、预览 回显数据
          if (['2', '3', '4'].includes(this.modelType)) {
            this.initContentAndTree()
          }
        }
      }).finally(() => {
        this.loading = false
      })
    },
    // 初始化回显数据
    async initContentAndTree() {
      // 先剔除固定的封面和声明指标，避免重复回显
      const fixedIds = [coverId, declarationId];
      const checkIndexData = (this.rowData.indexData || []).filter(item => !fixedIds.includes(item.indexCode));
      if (!checkIndexData.length) return;

      // 按 f_order 升序排列，保证回显顺序与保存时一致
      const sorted = [...checkIndexData].sort((a, b) => (a.fOrder != null ? a.fOrder : 0) - (b.fOrder != null ? b.fOrder : 0));

      // 在树中递归查找节点
      const findNodeByCode = (nodes, code) => {
        for (const node of nodes) {
          if (node.vcCode === code) return node;
          if (node.children && node.children.length) {
            const found = findNodeByCode(node.children, code);
            if (found) return found;
          }
        }
        return null;
      };

      // 1. 收集需要勾选的 key 并设置树的勾选状态
      const keys = sorted.map(item => item.indexCode).filter(Boolean);
      this.checkedTreeKeys = keys;
      this.syncTreeCheckedKeys();

      // 2. 先同步创建所有占位项，保持顺序
      this.loading = true;
      sorted.forEach(function (item) {
        var code = item.indexCode;
        var treeNode = findNodeByCode(this.treeData, code);
        var vcIndexName = treeNode ? treeNode.vcIndexName : code;

        this.checkList.push({
          key: code,
          vcIndexName: vcIndexName,
          html: '<div style="padding: 30px; text-align: center; color: #909399;"><i class="el-icon-loading"></i> 正在加载指标预览...</div>',
          indexOrder: treeNode ? treeNode.indexOrder : item.fOrder
        });

        if (!this.activeCollapseKeys.includes(code)) {
          this.activeCollapseKeys.push(code);
        }
      }.bind(this));

      // 3. 并行请求所有预览接口
      var self = this;
      var promises = sorted.map(function (item) {
        var code = item.indexCode;
        return pageApi.previewIndex(code).then(function (res) {
          let { status: resStatus, data: rawHtml, message } = res.data

          if (resStatus === 200) {
            var itemInList = self.checkList.find(function (i) { return i.key === code; });
            if (itemInList) {
              itemInList.html = rawHtml || '';
              var idx = self.checkList.indexOf(itemInList);
              self.checkList.splice(idx, 1, Object.assign({}, itemInList));
            }
          } else {
            throw new Error(message || '预览加载失败');
          }
        }).catch(function (e) {
          console.error('Preview Error:', e);
          var itemInList = self.checkList.find(function (i) { return i.key === code; });
          if (itemInList) {
            itemInList.html = '<div style="padding: 30px; text-align: center; color: #f56c6c;"><i class="el-icon-error"></i> 加载失败: ' + (e.message || '接口异常') + '</div>';
            var idx = self.checkList.indexOf(itemInList);
            self.checkList.splice(idx, 1, Object.assign({}, itemInList));
          }
        });
      });

      Promise.all(promises).then(function () {
        self.loading = false;
      });
    },
    // Tree Check 处理
    onTreeCheck(data, status) {
      const { checkedNodes } = status
      // 只处理叶子节点
      let leafNodes = checkedNodes.filter(n => !n.children || n.children.length === 0)
      
      const oldKeys = this.checkList.map(i => i.key)
      
      if (this.filterText) {
        const clickedNode = this.$refs.indexTree.getNode(data.vcCode || data.vcId)
        if (clickedNode && !clickedNode.isLeaf) {
          // 点击了父节点，找出该父节点下所有的可见叶子节点
          let visibleLeaves = []
          const traverse = (node) => {
            if (node.isLeaf && node.visible) {
              let isDisabled = false
              if (typeof this.treeProps.disabled === 'function') {
                isDisabled = this.treeProps.disabled(node.data, node)
              } else if (this.treeProps.disabled) {
                isDisabled = node.data[this.treeProps.disabled]
              }
              if (!isDisabled) {
                visibleLeaves.push(node)
              }
            }
            if (node.childNodes && node.childNodes.length) {
              node.childNodes.forEach(child => traverse(child))
            }
          }
          traverse(clickedNode)
          
          const allVisibleChecked = visibleLeaves.length > 0 && visibleLeaves.every(leaf => oldKeys.includes(leaf.data.vcCode || leaf.data.vcId))
          
          const leafKeysToToggle = visibleLeaves.map(leaf => leaf.data.vcCode || leaf.data.vcId)
          let newCheckedKeys = [...oldKeys]
          
          if (allVisibleChecked) {
            newCheckedKeys = newCheckedKeys.filter(k => !leafKeysToToggle.includes(k))
          } else {
            leafKeysToToggle.forEach(k => {
              if (!newCheckedKeys.includes(k)) {
                newCheckedKeys.push(k)
              }
            })
          }
          
          let finalLeafNodes = []
          newCheckedKeys.forEach(k => {
             const node = this.$refs.indexTree.getNode(k)
             if (node && node.data) {
                finalLeafNodes.push(node.data)
             } else {
                const existingItem = this.checkList.find(i => i.key === k)
                if (existingItem) {
                  finalLeafNodes.push({
                     vcCode: k,
                     vcIndexName: existingItem.vcIndexName,
                     indexOrder: existingItem.indexOrder
                  })
                }
             }
          })
          leafNodes = finalLeafNodes
        }
      }
      
      const currentKeys = leafNodes.map(n => n.vcCode || n.vcId)
      
      // 1. 移除取消勾选的项，同时清理对应的 script
      const removedItems = this.checkList.filter(item => !currentKeys.includes(item.key))
      removedItems.forEach(item => this.removeScriptByKey(item.key))
      this.checkList = this.checkList.filter(item => currentKeys.includes(item.key))
      
      // 2. 处理新增勾选的项
      const newNodes = leafNodes.filter(node => {
        const key = node.vcCode || node.vcId;
        return !oldKeys.includes(key);
      });

      newNodes.forEach(node => {
        const key = node.vcCode || node.vcId
        // 添加占位项并显示加载状态
        const newItem = {
          key: key,
          vcIndexName: node.vcIndexName,
          html: '<div style="padding: 30px; text-align: center; color: #909399;"><i class="el-icon-loading"></i> 正在加载指标预览...</div>',
          indexOrder: node.indexOrder
        }
        this.checkList.push(newItem)
        
        // 默认展开新加的面板
        if (!this.activeCollapseKeys.includes(key)) {
           this.activeCollapseKeys.push(key)
        }
        
        // 并行调用预览接口
        pageApi.previewIndex(key).then(res => {
          let { status: resStatus, data: rawHtml, message } = res.data
          
          if (resStatus === 200) {
            const itemInList = this.checkList.find(i => i.key === key)
            if (itemInList) {
              itemInList.html = rawHtml || ''
              // 触发响应式更新
              const idx = this.checkList.indexOf(itemInList)
              this.checkList.splice(idx, 1, { ...itemInList })
            }
          } else {
            throw new Error(message || '预览加载失败')
          }
        }).catch(e => {
          console.error('Preview Error:', e)
          const itemInList = this.checkList.find(i => i.key === key)
          if (itemInList) {
            itemInList.html = `<div style="padding: 30px; text-align: center; color: #f56c6c;"><i class="el-icon-error"></i> 加载失败: ${e.message || '接口异常'}</div>`
            const idx = this.checkList.indexOf(itemInList)
            this.checkList.splice(idx, 1, { ...itemInList })
          }
        })
      })
      
      this.checkedTreeKeys = this.checkList.map(i => i.key)
      this.syncTreeCheckedKeys()
    },
    syncTreeCheckedKeys() {
      this.$nextTick(() => {
        if (this.$refs.indexTree) {
          this.$refs.indexTree.setCheckedKeys(this.checkedTreeKeys || [])
        }
      })
    },
    // 过滤节点（命中父节点时展示其所有子节点）
    filterNode(value, data, node) {
      if (!value) return true
      const lowerValue = value.toLowerCase()
      // 当前节点自身匹配
      if (data.vcIndexName && data.vcIndexName.toLowerCase().indexOf(lowerValue) !== -1) {
        return true
      }
      // 检查祖先节点是否匹配，如果父节点命中搜索则子节点也要展示
      let parent = node.parent
      while (parent) {
        if (parent.data && parent.data.vcIndexName && parent.data.vcIndexName.toLowerCase().indexOf(lowerValue) !== -1) {
          return true
        }
        parent = parent.parent
      }
      return false
    },
    highlightKeyword(text) {
      if (!this.filterText) return text
      const regex = new RegExp(`(${this.filterText})`, 'gi')
      return text.replace(regex, `<span style="color: #1890ff;">$1</span>`)
    },
    // 中间拖拽功能
    onDragEnd() {
       // vuedraggable automatically updates checkList model
    },
    moveUp(index) {
      const el = this.checkList.splice(index, 1)[0]
      this.checkList.splice(index - 1, 0, el)
    },
    moveDown(index) {
      const el = this.checkList.splice(index, 1)[0]
      this.checkList.splice(index + 1, 0, el)
    },
    deleteItem(item, idx) {
      // 找到idx并删除
      const index = idx !== undefined ? idx : this.checkList.findIndex(i => i.key === item.key)
      if (index > -1) {
        // 清理对应的 script 标签
        this.removeScriptByKey(this.checkList[index].key)
        this.checkList.splice(index, 1)
        this.checkedTreeKeys = this.checkList.map(i => i.key)
        this.syncTreeCheckedKeys()
      }
    },
    scrollToPreview(key) {
      if (!this.activeCollapseKeys.includes(key)) {
         this.activeCollapseKeys.push(key)
      }
      this.$nextTick(() => {
        const element = document.getElementById('Collapse_' + key)
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' })
        }
      })
    },
    // 拖拽改变宽度
    startDragLeft(e) {
      this.isDraggingLeft = true
      this.startX = e.clientX
      this.startLeftWidth = this.leftWidth
      document.addEventListener('mousemove', this.onDragLeft)
      document.addEventListener('mouseup', this.stopDrag)
    },
    onDragLeft(e) {
      if (this.isDraggingLeft) {
        let newWidth = this.startLeftWidth + (e.clientX - this.startX)
        if (newWidth < 150) newWidth = 150
        if (newWidth > 800) newWidth = 800
        this.leftWidth = newWidth
      }
    },
    startDragCenter(e) {
      this.isDraggingCenter = true
      this.startX = e.clientX
      this.startCenterWidth = this.centerWidth
      document.addEventListener('mousemove', this.onDragCenter)
      document.addEventListener('mouseup', this.stopDrag)
    },
    onDragCenter(e) {
      if (this.isDraggingCenter) {
        let newWidth = this.startCenterWidth + (e.clientX - this.startX)
        if (newWidth < 150) newWidth = 150
        if (newWidth > 800) newWidth = 800
        this.centerWidth = newWidth
      }
    },
    toggleLeft() {
      this.leftCollapsed = !this.leftCollapsed
      if (!this.leftCollapsed) {
        this.leftWidth = 240
      }
    },
    toggleCenter() {
      this.centerCollapsed = !this.centerCollapsed
      if (!this.centerCollapsed) {
        this.centerWidth = 260
      }
    },
    stopDrag() {
      if (this.isDraggingLeft || this.isDraggingCenter) {
        this.isDraggingLeft = false
        this.isDraggingCenter = false
        document.removeEventListener('mousemove', this.onDragLeft)
        document.removeEventListener('mousemove', this.onDragCenter)
        document.removeEventListener('mouseup', this.stopDrag)
      }
    },
    // 脚本注入：参考 mainCanvas.vue，通过 DOM 查找 script 标签并执行
    executeNewScripts() {
      this.$nextTick(() => {
        this.checkList.forEach(item => {
          const isNew = !this.oldCheckKeys.some(oldKey => oldKey === item.key)
          if (isNew) {
            // 先移除同 key 的旧 script（处理反复勾选的场景）
            this.removeScriptByKey(item.key)
            let timer = null
            timer = setInterval(() => {
              const div = document.getElementById('Collapse_' + item.key)
              if (div) {
                const scripts = div.getElementsByTagName('script')
                for (let i = 0; i < scripts.length; i++) {
                  this.executeScript(scripts[i].textContent, item.key)
                }
                if (scripts && scripts.length > 0) {
                  clearInterval(timer)
                }
              }
            }, 3000)
          }
        })
        // 更新已执行脚本的 key 列表
        this.oldCheckKeys = this.checkList.map(i => i.key)
      })
    },
    executeScript(scriptContent, key) {
      const script = document.createElement('script')
      script.textContent = scriptContent
      script.className = 'customScript'
      if (key) script.setAttribute('data-key', key)
      document.body.appendChild(script)
    },
    // 移除指定 key 的 script 标签
    removeScriptByKey(key) {
      const scripts = document.querySelectorAll(`.customScript[data-key="${key}"]`)
      scripts.forEach(el => el.parentNode && el.parentNode.removeChild(el))
    },
    removeScripts() {
      // 组件销毁时清理所有注入的 script
      const scripts = document.querySelectorAll('.customScript')
      scripts.forEach(el => el.parentNode && el.parentNode.removeChild(el))
    },
    handleCancel() {
      this.$emit('closeModal')
    },
    handleSave() {
      this.$refs.topFormRef.validate(valid => {
        if (!valid) return
        
        if (!this.checkList.length) {
          this.$message.warning('未配置指标！')
          return
        }
        
        // 构建 indexInfo：封面在最前，声明在最后
        const userIndexInfo = this.checkList.map((item, index) => ({
           indexCode: item.key,
           f_order: index + 1 // 从1开始，0留给封面
        }))
        const indexInfo = [
          { indexCode: coverId, f_order: 0 },
          ...userIndexInfo,
          { indexCode: declarationId, f_order: userIndexInfo.length + 1 }
        ]
        const params = {
          templateName: this.configForm.templateName,
          type: "1", // 固定参数
          vcTempType: "1", // 固定参数-自定义模板
          indexInfo
        }
        
        if (this.modelType === '2') {
          // 编辑
          params.templateId = this.rowData.templateId;
          this.btnDisabled = true;
          pageApi.editSaveTemp(params).then(res => {
            const { status, message } = res;
            if (status === 200) {
              this.$message.success('保存成功');
              this.$emit('refresh');
              this.$emit('closeModal');
            } else {
              this.$message.error(message || '保存失败');
            }
          }).finally(() => {
            this.btnDisabled = false;
          })
        } else {
          // 新增
          this.btnDisabled = true
          pageApi.addSaveTemp(params).then(res => {
            const { status, message } = res
            if (status === 200) {
              this.$message.success('保存成功')
              this.$emit('refresh')
              this.$emit('closeModal')
            } else {
              this.$message.error(message || '保存失败')
            }
          }).finally(() => {
            this.btnDisabled = false
          })
        }
        
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.temp-config-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 15px;

  .top-form-area {
    flex-shrink: 0;
    .config-form {
      ::v-deep .el-form-item {
        .el-form-item__label {
          margin-right: 0 !important;
        }
      }
    }
  }

  .tempConfig-container {
    display: flex;
    flex: 1;
    border: 1px solid #e4e7ed;
    border-radius: 4px;
    height: 100%;
    overflow: hidden;

    &.is-preview {
      .tempConfig-right {
        border-left: none;
        margin-left: 0;
      }
    }

    &.is-resizing {
      user-select: none;
      .tempConfig-left,
      .tempConfig-center {
        transition: none;
      }
    }

    .resize-handle {
      width: 4px;
      height: 100%;
      cursor: col-resize;
      background-color: #f4f4f5;
      border-left: 1px solid #e4e7ed;
      border-right: 1px solid #e4e7ed;
      position: relative;
      z-index: 10;
      transition: background-color 0.2s;
      flex-shrink: 0;

      &:hover,
      &:active {
        background-color: #409eff;
        border-color: #409eff;
      }
    }

    .tempConfig-left {
      height: 100%;
      flex-shrink: 0;
      display: flex;
      flex-direction: column;

      .tree-search-box {
        padding: 8px 8px 0;
        flex-shrink: 0;
      }

      .tempConfig-content {
        flex: 1;
        height: 0;
      }

      .report-index-tree {
        ::v-deep .el-checkbox {
          margin-right: 6px !important;
        }
      }
    }

    .tempConfig-center {
      height: 100%;
      flex-shrink: 0;
    }

    .tempConfig-right {
      flex: 1;
      height: 100%;
      min-width: 0;
      display: flex;
      flex-direction: column;
      
      .preview-container {
        flex: 1;
        overflow-y: auto;
        padding: 15px;

        .close-icon {
          margin-left: 5px;
          color: #f5222d;
          font-size: 16px;
          cursor: pointer;
          position: relative;
          z-index: 10;
          &:hover {
             color: #cf1322;
          }
        }

        .sortable-ghost-preview {
          opacity: 0.5;
          background: #e6f7ff;
        }
      }
    }

    .tempConfig-left,
    .tempConfig-center {
      transition: width 0.3s ease-in-out;

      .tempConfig-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        white-space: nowrap;
        overflow: hidden;

        .collapse-icon {
          cursor: pointer;
          font-size: 16px;
          color: #909399;
          flex-shrink: 0;
          margin-left: 8px;

          &:hover {
            color: #409eff;
          }
        }
      }
    }

    .is-collapsed {
      border-right: 1px solid #e4e7ed;

      .tempConfig-title {
        justify-content: center !important;
        padding: 8px 0 !important;

        .collapse-icon {
          margin-left: 0;
        }
      }

      .collapsed-text {
        width: 1em;
        margin: 24px auto 0;
        font-size: 14px;
        color: #606266;
        cursor: pointer;
        user-select: none;
        line-height: 1.6;
        word-break: break-all;
        text-align: center;

        &:hover {
          color: #409eff;
        }
      }
    }

    .tempConfig-title {
      font-size: 14px;
      font-weight: 600;
      color: #333;
      padding: 8px;
      border-bottom: 1px solid #e4e7ed;
      background: #fafafa;
    }

    .tempConfig-content {
      padding: 8px;
      height: calc(100% - 40px);
      overflow-y: auto;
      overflow-x: hidden;

      .draggable-item {
        margin-bottom: 4px;

        &:hover {
          opacity: 0.8;

          .sort-arrows {
            display: inline-flex;
          }
        }
      }

      .sortable-ghost {
        opacity: 0.5;
        background: #f0f0f0;
      }

      .index-tag {
        width: 100%;
        display: flex;
        align-items: center;

        .index-tag-label {
          flex: 1;
          overflow: hidden;
          white-space: nowrap;
          text-overflow: ellipsis;
          cursor: pointer;
        }

        .sort-arrows {
          display: inline-flex;
          align-items: center;
          margin-left: 4px;
          flex-shrink: 0;
          display: none;

          .sort-arrow {
            cursor: pointer;
            font-size: 14px;
            color: #909399;
            margin-right: 2px;

            &:hover:not(.is-disabled) {
              color: #409eff;
            }

            &.is-disabled {
              color: #dcdfe6;
              cursor: not-allowed;
            }
          }
        }
      }
    }
  }
}
</style>
