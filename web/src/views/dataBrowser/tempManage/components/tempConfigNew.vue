<!--
 * @Description: 
 * @Author: 
 * @Date: 2025-11-03 14:52:19
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2025-12-31 10:14:30
-->
<template>
  <div class="tempConfig-wrapper">
    <el-dialog :visible.sync="visible" :title="dialogTitle" custom-class="dataBrowser-tempConfigDialog"
      :fullscreen="true" :close-on-click-modal="false" :close-on-press-escape="false" @closed="handleClose"
      v-loading="loading" element-loading-text="加载指标中。。。">
      <el-form :model="formData" inline ref="form">
        <el-form-item label="模板名称" prop="templateName">
          <el-input v-model="formData.templateName" placeholder="请输入模板名称" size="small" disabled></el-input>
        </el-form-item>
        <el-form-item label="模板类型" prop="templateType">
          <el-select v-model="formData.templateType" placeholder="请选择模板类型" size="small" disabled>
            <el-option v-for="item in templateTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <!-- 行业类型 -->
        <el-form-item label="行业类型" prop="industryType" v-if="['A', 'C'].includes(formData.templateType)">
          <el-select v-model="formData.industryType" placeholder="请选择行业类型" size="small" disabled>
            <el-option v-for="item in industryTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <!-- 因子类型 -->
        <el-form-item label="因子类型" prop="factorType" v-if="['A', 'C'].includes(formData.templateType)">
          <el-select v-model="formData.factorType" placeholder="请选择因子类型" size="small" disabled>
            <el-option v-for="item in factorTypeOptions" :key="item.dimCde" :label="item.dimNme"
              :value="item.dimCde"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="small" @click="saveTemplateConfig" :loading="btnLoading">保存模板</el-button>
          <el-button type="info" size="small" @click="handleClose" :disabled="btnLoading">取消</el-button>
        </el-form-item>
      </el-form>
      <div class="tempConfig-container" :class="{ 'is-resizing': isDraggingLeft || isDraggingCenter }">
        <div class="tempConfig-left" :style="{ width: leftCollapsed ? '40px' : leftWidth + 'px' }"
          :class="{ 'is-collapsed': leftCollapsed }">
          <div class="tempConfig-title">
            <span v-show="!leftCollapsed">指标列表</span>
            <i class="collapse-icon" :class="leftCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'" @click="toggleLeft"
              :title="leftCollapsed ? '展开' : '收起'"></i>
          </div>
          <div class="collapsed-text" v-show="leftCollapsed" @click="toggleLeft" title="展开指标列表">
            指标列表
          </div>
          <div class="tempConfig-content" v-show="!leftCollapsed">
            <el-input v-model="filterText" placeholder="搜索" prefix-icon="el-icon-search" size="small" clearable
              style="width: 100% !important;"></el-input>
            <el-tree ref="indexTreeRef" class="index-tree" :data="indexTreeData"
              :props="{ label: 'vcIndexName', children: 'children' }" default-expand-all
              :filter-node-method="filterNode" style="user-select: none" show-checkbox :check-strictly="true"
              @check="onCheck" node-key="vcId">
              <span slot-scope="{ node }" :class="['custom-node', node.isLeaf ? 'leaf-node' : 'parent-node']"
                :title="node.label">
                <i :class="node.isLeaf ? 'el-icon-document' : 'el-icon-folder'"></i>
                <span v-html="highlightKeyword(node.label)"></span>
              </span>
            </el-tree>
          </div>
        </div>
        <div class="resize-handle" v-show="!leftCollapsed" @mousedown.prevent="startDragLeft" title="拖拽调整宽度"></div>
        <div class="tempConfig-center" :style="{ width: centerCollapsed ? '40px' : centerWidth + 'px' }"
          :class="{ 'is-collapsed': centerCollapsed }">
          <div class="tempConfig-title">
            <span v-show="!centerCollapsed">已选指标</span>
            <i class="collapse-icon" :class="centerCollapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'"
              @click="toggleCenter" :title="centerCollapsed ? '展开' : '收起'"></i>
          </div>
          <div class="collapsed-text" v-show="centerCollapsed" @click="toggleCenter" title="展开已选指标">
            已选指标
          </div>
          <div class="tempConfig-content" v-show="!centerCollapsed">
            <template v-if="['A', 'B', 'C'].includes(currentTempType)">
              <draggable v-model="selectedIndexList" :options="{ animation: 200, ghostClass: 'sortable-ghost' }"
                @end="handleDragEnd">
                <div v-for="(item, index) in selectedIndexList" :key="item.vcId" class="draggable-item"
                  @click="handleClickItem(item)">
                  <el-tag closable @close="handleRemoveItem({ item, index })" type="info" effect="plain"
                    class="index-tag" :title="item.vcIndexName">
                    <span :class="['index-tag-label', validationClass(item)]">{{ item.vcIndexName }}</span>
                  </el-tag>
                </div>
              </draggable>
            </template>
            <template v-if="currentTempType === 'D'">
              <div v-for="group in groupedSelectedIndexList" :key="group.vcTypeCode" class="d-type-group">
                <div class="group-title">{{ group.vcTypeName }}</div>
                <draggable :value="group.list" :options="{ animation: 200, ghostClass: 'sortable-ghost' }"
                  @input="newList => updateGroupList(group.vcTypeCode, newList)" @end="handleDragEnd">
                  <div v-for="(item) in group.list" :key="item.vcId" class="draggable-item"
                    @click="handleClickItem(item)">
                    <el-tag closable @close="handleRemoveItemD(item)" type="info" effect="plain" class="index-tag"
                      :title="item.vcIndexName">
                      <span :class="['index-tag-label', validationClass(item)]">{{ item.vcIndexName }}</span>
                    </el-tag>
                  </div>
                </draggable>
              </div>
            </template>
          </div>
        </div>
        <div class="resize-handle" v-show="!centerCollapsed" @mousedown.prevent="startDragCenter" title="拖拽调整宽度"></div>
        <div class="tempConfig-right">
          <div class="tempConfig-title">
            <el-radio-group v-model="rightActiveTab" size="small" style="margin-right: 15px;">
              <el-radio-button label="dimension">维度配置</el-radio-button>
              <el-radio-button label="preview">模板预览</el-radio-button>
            </el-radio-group>
            <span style="color: red; font-size: 12px; font-weight: normal;">
              注意：新增、移除、拖拽指标 或 配置指标维度 将重置模板表头顺序，请在完成这些操作后再拖拽表头调整顺序
            </span>
          </div>
          <div class="tempConfig-content">
            <!-- 维度配置面板 -->
            <div v-show="rightActiveTab === 'dimension'" class="right-dimension-config">
              <div v-if="selectedIndexList.length === 0" class="empty-tip">
                <i class="el-icon-info"></i>
                <span>请在左侧勾选指标或从已选指标中选择</span>
              </div>
              <draggable v-else v-model="selectedIndexList" :options="{ animation: 200, handle: '.card-left' }" @end="handleDragEnd" class="config-list">
                <div v-for="item in selectedIndexList" :key="item.vcId" :id="'config-card-' + item.vcId" class="config-card">
                  <div class="card-left" title="拖拽排序" style="cursor: move;">
                    <span :class="['index-name', validationClass(item)]">{{ item.vcIndexName }}</span>
                  </div>
                  <div class="card-right">
                    <!-- 明细维度 -->
                    <div v-if="item.params && item.params.details && item.params.details.length" class="dimension-row">
                      <span class="dim-label">明细维度：</span>
                      <div class="dim-controls">
                        <el-checkbox-group v-model="item.paramsValue.details" size="small" class="dim-checkbox-group" @change="updateTableDisplay">
                          <el-checkbox v-for="opt in item.params.details" :key="opt.vcId" :label="opt" border>{{ opt.vcIndexName }}</el-checkbox>
                          <a class="toggle-all-link" @click="toggleAll(item, 'details')">
                            {{ item.paramsValue.details.length === item.params.details.length ? '取消全选' : '全选' }}
                          </a>
                        </el-checkbox-group>
                      </div>
                    </div>
                    <!-- 时间维度 -->
                    <div v-if="item.params && item.params.times && item.params.times.length" class="dimension-row">
                      <span class="dim-label">时间维度：</span>
                      <div class="dim-controls">
                        <el-checkbox-group v-model="item.paramsValue.times" size="small" class="dim-checkbox-group" @change="updateTableDisplay">
                          <el-checkbox v-for="opt in item.params.times" :key="opt.vcId" :label="opt" border>{{ opt.vcIndexName }}</el-checkbox>
                          <a class="toggle-all-link" @click="toggleAll(item, 'times')">
                            {{ item.paramsValue.times.length === item.params.times.length ? '取消全选' : '全选' }}
                          </a>
                        </el-checkbox-group>
                      </div>
                    </div>
                    <!-- 单位维度 -->
                    <div v-if="item.params && item.params.units && item.params.units.length" class="dimension-row">
                      <span class="dim-label">单位维度：</span>
                      <el-radio-group v-model="item.paramsValue.unit" size="small" class="dim-radio-group" @change="updateTableDisplay">
                        <el-radio v-for="unit in item.params.units" :key="unit.vcId" :label="unit" border>{{ unit.vcIndexName }}</el-radio>
                      </el-radio-group>
                    </div>
                  </div>
                  <div class="card-action">
                    <i class="el-icon-delete delete-btn" @click="removeIndex(item)"></i>
                  </div>
                </div>
              </draggable>
            </div>

            <!-- 表头预览面板 -->
            <div v-show="rightActiveTab === 'preview'" style="height: 100%;">
              <template v-if="['A', 'B'].includes(currentTempType)">
                <vxe-grid ref="vxeTableA" :columns="tableColumn" :data="tableData" :scroll-x="{ enabled: false }"
                  column-key border auto-resize align="center"></vxe-grid>
              </template>
              <template v-if="currentTempType === 'C'">
                <vxe-grid ref="vxeTableC" :columns="tableColumnC" :data="tableDataC" :scroll-x="{ enabled: false }"
                  column-key row-id="vcId" border auto-resize align="center"></vxe-grid>
              </template>
              <template v-if="currentTempType === 'D'">
                <el-tabs v-model="activeTabD" @tab-click="handleTabClickD" type="card">
                  <el-tab-pane v-for="group in groupedSelectedIndexList" :key="group.vcTypeCode" :label="group.vcTypeName"
                    :name="group.vcTypeCode">
                    <vxe-grid v-if="tableColumnD[group.vcTypeCode]" :ref="'vxeTableD_' + group.vcTypeCode"
                      :columns="tableColumnD[group.vcTypeCode]" :data="tableData" :scroll-x="{ enabled: false }"
                      column-key border auto-resize align="center"></vxe-grid>
                  </el-tab-pane>
                </el-tabs>
              </template>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import CONSTANTS from '../../constants.js'
import draggable from 'vuedraggable'
import Sortable from 'sortablejs'
import pageApi from '../api.js'

export default {
  components: {
    draggable
  },
  data() {
    return {
      rightActiveTab: 'dimension', // 默认激活维度配置
      visible: false,
      loading: false,
      btnLoading: false,
      sortable: null,
      sortableC: null,
      dialogTitle: '新增模板配置',
      currentTempType: "", // 当前模板类型
      formData: {
        templateName: '',
        templateType: '',
        industryType: '',
        factorType: ''
      },
      templateTypeOptions: CONSTANTS.TEMPTYPE,
      industryTypeOptions: [
        { dimCde: 'SWSR', dimNme: '申万行业' },
        { dimCde: 'ZXSR', dimNme: '中信行业' }
      ],
      factorTypeOptions: [
        { dimCde: "CNE5", dimNme: "CNE5" },
        { dimCde: "CNE6", dimNme: "CNE6" }
      ],
      filterText: '',
      indexListData: [],
      indexTreeData: [],
      selectedIndexList: [],
      fixedColumn: [
        {
          title: '日期',
          field: 'time',
          align: 'center',
          width: 120,
          headerClassName: 'noDrag'
        },
        {
          title: '产品',
          field: 'fundName',
          align: 'center',
          width: 140,
          headerClassName: 'noDrag'
        }
      ],
      // 单组合
      tableColumn: [],
      tableData: [],
      // 组合对比
      tableColumnC: [
        {
          title: '指标',
          field: 'indexName',
          align: 'center',
          className: 'index-header-cell',
        },
        {
          title: '产品一',
          field: 'fundName1',
          align: 'center',
        },
        {
          title: '产品二',
          field: 'fundName2',
          align: 'center',
        },
        {
          title: '产品...',
          field: 'fundName',
          align: 'center',
        }
      ],
      tableDataC: [],
      // D类型：个券模板
      sortableD: null,
      activeTabD: '', // 当前选中的tab
      tableColumnD: {}, // { vcTypeCode: columnsArray }
      fixedColumnD: {},
      leftWidth: 240,
      centerWidth: 240,
      isDraggingLeft: false,
      isDraggingCenter: false,
      startX: 0,
      startLeftWidth: 0,
      startCenterWidth: 0,
      leftCollapsed: false,
      centerCollapsed: false
    }
  },
  props: {
    dialogType: {
      type: String,
      default: 'add'
    }
  },
  mounted() {
    this.visible = true
    this.initFixedColumns()
    if (this.dialogType === 'edit') {
      this.dialogTitle = '编辑模板配置'
    }
  },
  watch: {
    filterText(val) {
      this.$refs.indexTreeRef.filter(val)
    }
  },
  beforeDestroy() {
    document.removeEventListener('mousemove', this.onDragLeft)
    document.removeEventListener('mousemove', this.onDragCenter)
    document.removeEventListener('mousemove', this.onDragCenter)
    document.removeEventListener('mouseup', this.stopDrag)
  },
  computed: {
    // 根据 vcTypeCode 对 selectedIndexList 分组，供 D 类型使用
    groupedSelectedIndexList() {
      const groupsMap = {}
      const groupsList = []
      this.selectedIndexList.forEach(item => {
        const typeCode = item.vcTypeCode
        if (!groupsMap[typeCode]) {
          const newGroup = {
            vcTypeCode: typeCode,
            vcTypeName: item.vcTypeName,
            list: []
          }
          groupsMap[typeCode] = newGroup
          groupsList.push(newGroup)
        }
        groupsMap[typeCode].list.push(item)
      })
      return groupsList
    }
  },
  methods: {
    // 初始化固定表头
    initFixedColumns() {
      // 单产品类型
      this.fixedColumn = CONSTANTS.TEMPCOLBEFORE1.map(item => {
        return {
          title: item.title,
          field: item.dataIndex,
          align: 'center',
          width: 120,
          fixed: 'left',
          headerClassName: 'noDrag'
        }
      });
      // 个券模板类型
      const FUND_FIXED = CONSTANTS.TEMPCOLBEFORE.map(item => {
        return {
          title: item.title,
          field: item.dataIndex,
          align: 'center',
          width: 120,
          fixed: 'left',
          headerClassName: 'noDrag'
        }
      })
      for (let key in CONSTANTS.TEMPCOLBEFORE2) {
        const SYMBOL_FIXED = CONSTANTS.TEMPCOLBEFORE2[key].map(item => {
          return {
            title: item.title,
            field: item.dataIndex,
            align: 'center',
            width: 120,
            fixed: 'left',
            headerClassName: 'noDrag'
          }
        })
        const columns = [...FUND_FIXED, ...SYMBOL_FIXED]
        this.fixedColumnD[key] = columns;
      }

    },
    // 校验指标是否已选择参数
    validationClass(item) {
      if (!item.params || !item.paramsValue) {
        return 'valid'
      }
      if (item.params.details.length && !item.paramsValue.details.length) {
        return 'invalid'
      }
      if (item.params.times.length && !item.paramsValue.times.length) {
        return 'invalid'
      }
      if (item.params.units.length && !item.paramsValue.unit) {
        return 'invalid'
      }
      return 'valid'
    },
    // 根据当前模板类型更新对应的表格显示视图
    updateTableDisplay() {
      if (['A', 'B'].includes(this.currentTempType)) {
        this.setTableColumn()
      } else if (this.currentTempType === 'C') {
        this.setTableDataC()
      } else if (this.currentTempType === 'D') {
        this.setTableColumnD()
      }
    },
    // 提取的维度交叉组合辅助方法
    generateIndexCombinations() {
      let combinations = []
      this.selectedIndexList.forEach((item) => {
        const { details = [], times = [], unit = {} } = item.paramsValue || {}
        
        // 按照参数原有的顺序进行过滤，确保笛卡尔积顺序不受勾选先后顺序的影响
        const sortedDetails = (item.params && item.params.details ? item.params.details : []).filter(d => details.some(v => v.vcId === d.vcId))
        const sortedTimes = (item.params && item.params.times ? item.params.times : []).filter(t => times.some(v => v.vcId === t.vcId))

        if (sortedDetails.length && sortedTimes.length) {
          sortedDetails.forEach((detailItem) => {
            sortedTimes.forEach((timeItem) => {
              combinations.push({ item, detailItem, timeItem, unitItem: unit })
            })
          })
        } else if (sortedDetails.length && !sortedTimes.length) {
          sortedDetails.forEach((detailItem) => {
            combinations.push({ item, detailItem, timeItem: {}, unitItem: unit })
          })
        } else if (!sortedDetails.length && sortedTimes.length) {
          sortedTimes.forEach((timeItem) => {
            combinations.push({ item, detailItem: {}, timeItem, unitItem: unit })
          })
        } else {
          combinations.push({ item, detailItem: {}, timeItem: {}, unitItem: unit || {} })
        }
      })
      return combinations
    },
    // 获取指标树数据
    getIndexData() {
      return new Promise((resolve, reject) => {
        this.loading = true
        let apiMethod = "";
        switch (this.formData.templateType) {
          case "A":
            apiMethod = "getIndexDetailInfoTreeList"
            break;
          case "C":
            apiMethod = "getIndexDetailInfoTreeZHList"
            break;
          case "D":
            apiMethod = "getIndexDetailInfoTreeGQList"
            break;

          default:
            apiMethod = "getIndexDetailInfoTreeList"
            break;
        }
        let params = {}
        let industryType = 'SWSR'
        let factorType = 'CNE5'
        if (['A', 'C'].includes(this.formData.templateType)) {
          const vcBenchMark = this.formData.vcBenchMark || (this.rowData && this.rowData.vcBenchMark) || ""
          if (vcBenchMark) {
            try {
              const benchmarkObj = JSON.parse(vcBenchMark)
              if (benchmarkObj && typeof benchmarkObj === 'object') {
                industryType = benchmarkObj.industryType || 'SWSR'
                factorType = benchmarkObj.factorType || 'CNE5'
              }
            } catch (e) {
              console.error('getIndexData parse vcBenchMark error:', e)
            }
          }
          params = {
            vcIndustType: industryType,
            vcFactorType: factorType
          }
        }
        pageApi[apiMethod](params).then((res) => {
          const { status, data } = res.data
          if (status === 200 && data) {
            // 根据isIndexOrType字段区分指标和指标参数维度
            const indexList = data.filter((item) => item.isIndexOrType === '1').sort((a, b) => a.fOrder - b.fOrder).filter((item, index, arr) => arr.findIndex(i => i.vcId === item.vcId) === index)
            const indexParamList = data.filter((item) => item.isIndexOrType !== '1').sort((a, b) => a.fOrder - b.fOrder)
            // 组装this.indexListData
            this.indexListData = indexList.map((indexItem) => {
              // 查找当前指标对应的所有参数维度数据
              const relatedParams = indexParamList.filter((paramItem) => paramItem.vcPid === indexItem.vcId)

              // 分别归类明细、时间和单位维度数据
              const details = relatedParams.filter((item) => item.isIndexOrType === '3')
              const times = relatedParams.filter((item) => item.isIndexOrType === '2')
              const units = relatedParams.filter((item) => item.isIndexOrType === '4')

              // 配置模板类型D时，勾选指标若找不到对应的类型，则设置为“其他”，typeCode: "more"
              const validTypes = ['ggzb', 'gzzb', 'pzzb', 'gjzb']
              if (this.formData.templateType === 'D') {
                if (!indexItem.vcTypeCode || !validTypes.includes(indexItem.vcTypeCode)) {
                  indexItem.vcTypeCode = 'more'
                  indexItem.vcTypeName = '其他'
                }
              }

              // 组装成要求的数据结构
              return {
                ...indexItem,
                params: {
                  details: details, // 明细维度数据
                  times: times, // 时间维度数据
                  units: units // 单位维度数据
                },
                paramsValue: {
                  details: [], // 明细维度数据
                  times: [], // 时间维度数据
                  units: '' // 单位维度数据
                }
              }
            })
            this.indexTreeData = this.delDepartTree(this.indexListData, 'vcId', 'vcPid')
          }
          this.loading = false
          resolve()
        }).catch(() => {
          this.loading = false
          resolve()
        })
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
        this.leftWidth = 240 // 展开时恢复默认宽度
      }
      this.$nextTick(() => {
        this.$refs.vxeTableA && this.$refs.vxeTableA.recalculate(true)
        this.$refs.vxeTableC && this.$refs.vxeTableC.recalculate(true)
      })
    },
    toggleCenter() {
      this.centerCollapsed = !this.centerCollapsed
      if (!this.centerCollapsed) {
        this.centerWidth = 240 // 展开时恢复默认宽度
      }
      this.$nextTick(() => {
        this.$refs.vxeTableA && this.$refs.vxeTableA.recalculate(true)
        this.$refs.vxeTableC && this.$refs.vxeTableC.recalculate(true)
      })
    },
    stopDrag() {
      if (this.isDraggingLeft || this.isDraggingCenter) {
        this.isDraggingLeft = false
        this.isDraggingCenter = false
        document.removeEventListener('mousemove', this.onDragLeft)
        document.removeEventListener('mousemove', this.onDragCenter)
        document.removeEventListener('mouseup', this.stopDrag)
        // 拖拽结束时重新计算 vxe-grid 宽度，防止部分情况的布局显示错误
        this.$nextTick(() => {
          this.$refs.vxeTableA && this.$refs.vxeTableA.recalculate(true)
          this.$refs.vxeTableC && this.$refs.vxeTableC.recalculate(true)
        })
      }
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
    tableDrop() {
      this.$nextTick(() => {
        if (['A', 'B'].includes(this.currentTempType)) {
          this.$refs.vxeTableA && this.rowDrop()
        }
        if (this.currentTempType === 'C') {
          this.$refs.vxeTableC && this.rowDropC()
        }
        if (this.currentTempType === 'D') {
          this.rowDropD()
        }
      })
    },
    // 从新增进来
    init(data) {
      this.formData = _.cloneDeep(data)
      this.currentTempType = data.vcTemplateType;
      this.tableDrop();
      this.formData.templateName = data.vcTemplateName;
      this.formData.templateType = data.vcTemplateType;
      // 其他字段
      // ...
      let industryType = 'SWSR'
      let factorType = 'CNE5'
      if (data.vcBenchMark) {
        try {
          const benchmarkObj = JSON.parse(data.vcBenchMark)
          if (benchmarkObj && typeof benchmarkObj === 'object') {
            industryType = benchmarkObj.industryType || 'SWSR'
            factorType = benchmarkObj.factorType || 'CNE5'
          }
        } catch (e) {
          console.error(e)
        }
      }
      this.$set(this.formData, 'industryType', industryType)
      this.$set(this.formData, 'factorType', factorType)

      this.getIndexData()
    },
    // 编辑回显
    async editInit(row) {
      row = _.cloneDeep(row)
      this.rowData = row;
      this.currentTempType = row.vcTemplateType;
      this.tableDrop();
      this.formData.templateName = row.vcTemplateName
      this.formData.templateType = row.vcTemplateType

      let industryType = 'SWSR'
      let factorType = 'CNE5'
      if (row.vcBenchMark) {
        try {
          const benchmarkObj = JSON.parse(row.vcBenchMark)
          if (benchmarkObj && typeof benchmarkObj === 'object') {
            industryType = benchmarkObj.industryType || 'SWSR'
            factorType = benchmarkObj.factorType || 'CNE5'
          }
        } catch (e) {
          console.error(e)
        }
      }
      this.$set(this.formData, 'industryType', industryType)
      this.$set(this.formData, 'factorType', factorType)

      await this.getIndexData()
      try {
        // 调用接口获取指标配置信息
        this.loading = true;
        const res = await pageApi.getTemplateIndexInfoList({
          vcTemplateId: row.vcTemplateId
        })
        const { status, data: colList } = res.data
        if (status === 200 && colList) {
          colList.sort((a, b) => a.fColOrder - b.fColOrder)
          // 过滤掉固定列数据（日期、产品、标的代码/名称等），这些是保存时拼接的，回显时不需要
          const beforeCodes = ['before_code', 'ggzb', 'gzzb', 'pzzb', 'gjzb', 'more']
          const filteredColList = colList.filter(item => !beforeCodes.includes(item.vcIndexCode))
          // 编辑回显
          // 组装表格列数据this.tableColumn、this.selectedIndexList数据

          // 重置已选指标列表和表格列
          this.selectedIndexList = []
          this.tableColumn = [...this.fixedColumn]
          this.tableDataC = []

          // 先按指标分组，收集每个指标的所有维度值
          const indexParamsMap = new Map()

          // 建立索引映射，将 O(N^2) 的查找性能优化为 O(N)
          const indexListMap = new Map(this.indexListData.map(item => [item.vcId, item]))

          const columnsMapD = {}

          filteredColList.forEach((colItem) => {
            // 通过 Map 获取，提升性能
            const indexItem = indexListMap.get(colItem.vcIndexCode)

            if (indexItem) {
              // 从指标的params中找到对应的维度信息
              const timeItem = indexItem.params.times.find((item) => item.vcTimeId === colItem.vcTimeDefineId)
              const detailItem = indexItem.params.details.find((item) => item.vcItemId === colItem.vcItemDefineId)
              const unitItem = indexItem.params.units.find((item) => item.vcId === colItem.vcUnitType)

              // A类型：组装表格列数据
              if (['A', 'B'].includes(this.currentTempType)) {
                this.tableColumn.push({
                  field: colItem.vcColCode,
                  title: colItem.vcColName,
                  minWidth: 150,
                  align: 'center',
                  headerClassName: 'index-drag',
                  indexItemInfo: {
                    indexItem: indexItem,
                    timeItem: timeItem || {},
                    detailItem: detailItem || {},
                    unitItem: unitItem || {}
                  }
                })
              }

              // C类型：组装表格行数据
              if (this.currentTempType === 'C') {
                this.tableDataC.push({
                  vcId: colItem.vcColCode,
                  parentVcId: indexItem.vcId,
                  indexName: colItem.vcColName,
                  indexItemInfo: {
                    indexItem: indexItem,
                    detailItem: detailItem || {},
                    timeItem: timeItem || {},
                    unitItem: unitItem || {}
                  }
                })
              }

              // D类型：组装表格列数据
              if (this.currentTempType === 'D') {
                if (!columnsMapD[indexItem.vcTypeCode]) {
                  columnsMapD[indexItem.vcTypeCode] = [...this.fixedColumnD[indexItem.vcTypeCode]]
                }
                columnsMapD[indexItem.vcTypeCode].push({
                  field: colItem.vcColCode,
                  title: colItem.vcColName,
                  minWidth: 150,
                  align: 'center',
                  headerClassName: 'index-drag',
                  indexItemInfo: {
                    indexItem: indexItem,
                    timeItem: timeItem || {},
                    detailItem: detailItem || {},
                    unitItem: unitItem || {}
                  }
                })
              }

              // 收集指标的维度值
              if (!indexParamsMap.has(indexItem.vcId)) {
                indexParamsMap.set(indexItem.vcId, {
                  indexItem: indexItem,
                  details: new Set(),
                  times: new Set(),
                  unit: unitItem || {}
                })
              }

              const indexParams = indexParamsMap.get(indexItem.vcId)
              if (detailItem) indexParams.details.add(detailItem)
              if (timeItem) indexParams.times.add(timeItem)
              // 单位维度取最后一个值（通常一个指标只有一个单位）
              if (unitItem) indexParams.unit = unitItem
            }
          })

          // 组装selectedIndexList
          indexParamsMap.forEach((params, vcId) => {
            // 深拷贝指标对象，避免修改原数据
            const selectedItem = _.cloneDeep(params.indexItem)
            // 重新映射维度值引用：必须使用克隆后 selectedItem.params 中的引用，
            // 而非原始 indexListData 中的引用，否则 el-checkbox-group 的 === 引用比较会失败
            const detailsVal = Array.from(params.details).map(origDetail => {
              return selectedItem.params.details.find(d => d.vcItemId === origDetail.vcItemId)
            }).filter(Boolean)

            const timesVal = Array.from(params.times).map(origTime => {
              return selectedItem.params.times.find(t => t.vcTimeId === origTime.vcTimeId)
            }).filter(Boolean)

            let unitVal = params.unit
            if (unitVal && unitVal.vcId && Array.isArray(selectedItem.params.units)) {
              unitVal = selectedItem.params.units.find(u => u.vcId === unitVal.vcId) || unitVal
            }

            selectedItem.paramsValue = {
              details: detailsVal,
              times: timesVal,
              unit: unitVal
            }
            this.selectedIndexList.push(selectedItem)
          })

          if (this.currentTempType === 'D') {
            this.tableColumnD = columnsMapD
            const keys = Object.keys(columnsMapD)
            if (keys.length > 0) this.activeTabD = keys[0]
            this.tableDrop()
          }

          // 设置el-tree勾选项
          this.$nextTick(() => {
            this.$refs.indexTreeRef.setCheckedKeys(this.selectedIndexList.map((item) => item.vcId))
          })
        }
      } catch (error) {
        this.loading = false
      } finally {
        this.loading = false
      }
    },
    // 关闭弹窗
    handleClose() {
      this.visible = false
      this.$emit('close')
    },
    // 保存模板配置
    saveTemplateConfig() {
      this.$message.closeAll()
      // 校验指标是否已选择
      if (this.selectedIndexList.length === 0) {
        this.$message({
          message: '请选择指标',
          type: 'warning'
        })
        return
      }
      // 指标是否已选参数
      for (let i = 0; i < this.selectedIndexList.length; i++) {
        const item = this.selectedIndexList[i]
        const itemClass = this.validationClass(item)
        if (itemClass === 'invalid') {
          this.$message({
            message: `【${item.vcIndexName}】 参数未选择！`,
            type: 'warning'
          })
          return
        }
      }
      const params = {
        vcTemplateName: this.formData.templateName,
        vcTemplateType: this.formData.templateType,
        vcDateType: this.formData.vcDateType,
        vcTimeRate: this.formData.vcTimeRate,
        dStartTime: this.formData.beginDate,
        dEndTime: this.formData.endDate,
        vcRemark: this.formData.vcRemark,
        vcFundInfos: this.formData.vcFundInfos,
        vcBenchMark: this.formData.vcBenchMark
      }
      let colList = []
      // 根据模板类型获取遍历的源，并按参考项目逻辑拼接固定列
      let list = []
      if (['A', 'B'].includes(this.currentTempType)) {
        // A/B类型：取指标列（有indexItemInfo的），前面拼接固定列TEMPCOLBEFORE1（日期、产品）
        const indexCols = this.tableColumn.filter((item) => item.indexItemInfo)
        list = [...CONSTANTS.TEMPCOLBEFORE1, ...indexCols]
      } else if (this.currentTempType === 'C') {
        // C类型：直接使用表格行数据，不需要拼接固定列
        list = this.tableDataC
      } else if (this.currentTempType === 'D') {
        // D类型：每个分组前拼接TEMPCOLBEFORE2对应的固定列（标的代码、标的名称），最外层拼接TEMPCOLBEFORE（产品代码、产品名称）
        Object.keys(this.tableColumnD).forEach(vcTypeCode => {
          const groupCols = this.tableColumnD[vcTypeCode].filter((item) => item.indexItemInfo)
          const beforeCols = CONSTANTS.TEMPCOLBEFORE2[vcTypeCode] || []
          const mergedCols = [...beforeCols, ...groupCols]
          mergedCols.forEach(col => {
            list.push({
              ...col,
              vcTypeCode: col.vcTypeCode || vcTypeCode,
              vcTypeName: col.vcTypeName || ''
            })
          })
        })
        list = [...CONSTANTS.TEMPCOLBEFORE, ...list]
      }

      list.forEach((item, index) => {
        // 判断是否为固定列（来自TEMPCOLBEFORE/TEMPCOLBEFORE1/TEMPCOLBEFORE2，有dataIndex字段）
        if (item.dataIndex !== undefined) {
          // 固定列：按参考项目的字段映射方式组装
          colList.push({
            fColOrder: index + 1,
            vcColName: item.title || '',
            vcColCode: item.dataIndex || '',
            vcInfoDefineId: item.vcInfoDefineId || '',
            vcIndexCode: item.pId || '',
            vcUnitType: item.unit || '',
            vcUnitDefineId: item.vcUnitDefineId || '',
            vcFormat: item.vcFormat || '',
            vcScale: item.vcScale || '',
            vcItemDefineId: item.vcItemId || '',
            vcTimeDefineId: item.vcTimeId || '',
            vcTypeCode: item.vcTypeCode || '',
            vcTypeName: item.vcTypeName || '',
            vcModelValue: item.vcModelValue || ''
          })
        } else if (item.indexItemInfo) {
          // 指标列：使用原有逻辑
          const { indexItem = {}, detailItem = {}, timeItem = {}, unitItem = {} } = item.indexItemInfo
          colList.push({
            fColOrder: index + 1,
            vcColName: ['A', 'B', 'D'].includes(this.currentTempType) ? item.title : item.indexName,
            vcColCode: ['A', 'B', 'D'].includes(this.currentTempType) ? item.field : item.vcId,
            vcInfoDefineId: indexItem.vcInfoDefineId || '',
            vcIndexCode: indexItem.vcId || '',
            vcUnitType: unitItem.vcId || '',
            vcUnitDefineId: unitItem.vcUnitId || '',
            vcFormat: unitItem.vcFormat || '',
            vcScale: unitItem.vcScale || '',
            vcItemDefineId: detailItem.vcItemId || '',
            vcTimeDefineId: timeItem.vcTimeId || '',
            vcTypeCode: indexItem.vcTypeCode || '',
            vcTypeName: indexItem.vcTypeName || '',
            vcModelValue: indexItem.vcModelValue || ''
          })
        }
      })
      params.colList = colList
      if (this.dialogType == "edit") {
        const editParams = {
          vcTemplateId: this.rowData.vcTemplateId,
          colList
        }
        this.btnLoading = true;
        pageApi.updateTemplateDetail(editParams).then(res => {
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success(message || "编辑成功");
            this.$emit("close");
            this.$emit("refresh");
          } else {
            this.$message.error(message || "编辑失败");
          }
        }).finally(() => {
          this.btnLoading = false;
        })
      } else {
        this.btnLoading = true;
        pageApi.insertTemplateInfo(params).then(res => {
          const { status, message } = res.data;
          if (status === 200) {
            this.$message.success(message || "新增成功");
            this.$emit("close");
            this.$emit("refresh");
          } else {
            this.$message.error(message || "新增失败");
          }
        }).finally(() => {
          this.btnLoading = false;
        })
      }
    },
    // 勾选/取消勾选 节点
    onCheck(data, { checkedKeys }) {
      // console.log(data, checkedKeys)
      if (checkedKeys.includes(data.vcId)) {
        const clonedData = _.cloneDeep(data)
        const { details = [], times = [], units = [] } = clonedData.params || {}
        const hasDimension = details.length > 0 || times.length > 0 || units.length > 0

        if (!hasDimension) {
          // 无任何维度数据 → 提示，直接加入
          // this.$message.warning(`【${clonedData.vcIndexName}】无维度数据`)
          this.selectedIndexList.push(clonedData)
        } else if (details.length === 0 && times.length === 0 && units.length === 1) {
          // 仅有单位维度且只有一个 → 自动填充，不弹窗
          clonedData.paramsValue = {
            details: [],
            times: [],
            unit: units[0]
          }
          this.selectedIndexList.push(clonedData)
        } else {
          // 其他场景：正常加入，如果有单位列表，默认选中第一个单位，减少用户操作
          if (clonedData.params && Array.isArray(clonedData.params.units) && clonedData.params.units.length > 0) {
            clonedData.paramsValue.unit = clonedData.params.units[0]
          }
          this.selectedIndexList.push(clonedData)
        }
      } else {
        // 取消勾选不改变其他已选指标的顺序，直接删除
        const index = this.selectedIndexList.findIndex((item) => item.vcId === data.vcId)
        if (index !== -1) {
          this.selectedIndexList.splice(index, 1)
        }
      }
      this.updateTableDisplay()
    },
    // 设置表格列 (A类型)
    setTableColumn() {
      const combinations = this.generateIndexCombinations()
      const indexColumn = combinations.map(({ item, detailItem, timeItem, unitItem }) => {
        let field = item.vcId
        let title = item.vcIndexName

        if (detailItem && detailItem.vcId) {
          field += `_${detailItem.vcId}`
          title += `_${detailItem.vcIndexName}`
        }
        if (timeItem && timeItem.vcId) {
          field += `_${timeItem.vcId}`
          title += `_${timeItem.vcIndexName}`
        }
        if (unitItem && unitItem.vcId && unitItem.vcId !== 'original' && unitItem.vcIndexName !== '原值') {
          title += `(${unitItem.vcIndexName})`
        }

        return {
          field,
          title,
          minWidth: 150,
          align: 'center',
          headerClassName: 'index-drag',
          indexItemInfo: { indexItem: item, detailItem, timeItem, unitItem }
        }
      })
      this.tableColumn = [...this.fixedColumn, ...indexColumn]
    },
    // 设置C类型表格行数据
    setTableDataC() {
      const combinations = this.generateIndexCombinations()
      this.tableDataC = combinations.map(({ item, detailItem, timeItem, unitItem }) => {
        let vcId = item.vcId
        let indexName = item.vcIndexName

        if (detailItem && detailItem.vcId) {
          vcId += `_${detailItem.vcId}`
          indexName += `_${detailItem.vcIndexName}`
        }
        if (timeItem && timeItem.vcId) {
          vcId += `_${timeItem.vcId}`
          indexName += `_${timeItem.vcIndexName}`
        }
        if (unitItem && unitItem.vcId && unitItem.vcId !== 'original' && unitItem.vcIndexName !== '原值') {
          indexName += `(${unitItem.vcIndexName})`
        }

        return {
          vcId,
          parentVcId: item.vcId,
          indexName,
          indexItemInfo: { indexItem: item, detailItem, timeItem, unitItem }
        }
      })
    },
    // 设置D类型表格列数据
    setTableColumnD() {
      const combinations = this.generateIndexCombinations()
      let columnsMap = {}

      combinations.forEach(({ item, detailItem, timeItem, unitItem }) => {
        let field = item.vcId
        let title = item.vcIndexName

        if (detailItem && detailItem.vcId) {
          field += `_${detailItem.vcId}`
          title += `_${detailItem.vcIndexName}`
        }
        if (timeItem && timeItem.vcId) {
          field += `_${timeItem.vcId}`
          title += `_${timeItem.vcIndexName}`
        }
        if (unitItem && unitItem.vcId && unitItem.vcId !== 'original' && unitItem.vcIndexName !== '原值') {
          title += `(${unitItem.vcIndexName})`
        }

        const colItem = {
          field,
          title,
          minWidth: 150,
          align: 'center',
          headerClassName: 'index-drag',
          indexItemInfo: { indexItem: item, detailItem, timeItem, unitItem }
        }

        if (!columnsMap[item.vcTypeCode]) {
          columnsMap[item.vcTypeCode] = []
        }
        columnsMap[item.vcTypeCode].push(colItem)
      })

      this.tableColumnD = {}
      for (const typeCode in columnsMap) {
        this.$set(this.tableColumnD, typeCode, [...this.fixedColumnD[typeCode], ...columnsMap[typeCode]])
      }

      // 更新激活的Tab
      const typeCodes = Object.keys(columnsMap)
      if (typeCodes.length > 0) {
        if (!this.activeTabD || !typeCodes.includes(this.activeTabD)) {
          this.activeTabD = typeCodes[0]
        }
      } else {
        this.activeTabD = ''
      }

      this.tableDrop() // 每当D类型表头数据变化时需要重置拖拽挂载
    },
    // D类型拖动分组的更新
    updateGroupList(typeCode, newList) {
      const otherItemsLeft = []
      const otherItemsRight = []
      let seenType = false
      this.selectedIndexList.forEach(item => {
        if (item.vcTypeCode === typeCode) {
          seenType = true
        } else {
          if (seenType) otherItemsRight.push(item)
          else otherItemsLeft.push(item)
        }
      })
      this.selectedIndexList = [...otherItemsLeft, ...newList, ...otherItemsRight]
    },
    // D类型的移除
    handleRemoveItemD(item) {
      const index = this.selectedIndexList.findIndex(i => i.vcId === item.vcId)
      if (index !== -1) {
        this.selectedIndexList.splice(index, 1)
        this.$refs.indexTreeRef.setCheckedKeys(this.selectedIndexList.map((i) => i.vcId))
        this.updateTableDisplay()
      }
    },
    // D类型的 Tab 切换
    handleTabClickD(tab) {
      this.activeTabD = tab.name
      this.tableDrop()
    },
    // 移除指标
    handleRemoveItem({ item, index }) {
      this.selectedIndexList.splice(index, 1)
      // 设置el-tree勾选项
      this.$refs.indexTreeRef.setCheckedKeys(this.selectedIndexList.map((i) => i.vcId))
      this.updateTableDisplay()
    },
    // 点击已选指标，自动切换到“维度配置”面板并定位滚动到对应的指标卡片
    handleClickItem(data) {
      const { details = [], times = [], units = [] } = data.params || {}
      const hasDimension = details.length > 0 || times.length > 0 || units.length > 0
      if (!hasDimension) {
        this.$message.warning(`【${data.vcIndexName}】无维度数据`)
        return
      }
      this.rightActiveTab = 'dimension'
      this.$nextTick(() => {
        const cardEl = document.getElementById(`config-card-${data.vcId}`)
        if (cardEl) {
          cardEl.scrollIntoView({ behavior: 'smooth', block: 'center' })
          cardEl.classList.add('highlight-card')
          setTimeout(() => {
            cardEl.classList.remove('highlight-card')
          }, 1500)
        }
      })
    },
    // 一键全选/反选明细维度或时间维度
    toggleAll(item, type) {
      if (item.paramsValue[type].length === item.params[type].length) {
        // 已全选 -> 取消全选
        this.$set(item.paramsValue, type, [])
      } else {
        // 未全选 -> 全选
        this.$set(item.paramsValue, type, [...item.params[type]])
      }
      this.updateTableDisplay()
    },
    // 统一处理已选卡片的删除操作
    removeIndex(item) {
      if (this.currentTempType === 'D') {
        this.handleRemoveItemD(item)
      } else {
        const index = this.selectedIndexList.findIndex((i) => i.vcId === item.vcId)
        if (index !== -1) {
          this.handleRemoveItem({ item, index })
        }
      }
    },
    // 拖拽结束
    handleDragEnd() {
      this.updateTableDisplay()
    },
    /*拖拽功能*/
    rowDrop() {
      const self = this
      this.$nextTick(() => {
        let xTable = this.$refs.vxeTableA;
        if (!xTable) return
        const headerEl = xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row')
        if (!headerEl) return
        const scrollEl = xTable.$el.querySelector('.vxe-table--body-wrapper')
        this.sortable = Sortable.create(headerEl, {
          handle: '.vxe-header--column',
          animation: 180,
          delay: 0,
          draggable: '.index-drag',
          scroll: scrollEl || true,
          scrollSensitivity: 100,
          scrollSpeed: 10,
          bubbleScroll: true,
          onEnd: ({ item, newIndex, oldIndex }) => {
            self.$nextTick(() => {
              const tableColumnClone = _.cloneDeep(self.tableColumn)
              const oldItem = tableColumnClone[oldIndex]
              tableColumnClone.splice(oldIndex, 1)
              tableColumnClone.splice(newIndex, 0, oldItem)
              self.tableColumn = tableColumnClone
            })
          }
        })
      })
    },
    /* D类型-表头拖拽排序 */
    rowDropD() {
      const self = this
      this.$nextTick(() => {
        if (!this.activeTabD) return
        let refs = this.$refs['vxeTableD_' + this.activeTabD]
        let xTable = refs && refs[0]
        if (!xTable) return
        const header = xTable.$el.querySelector('.body--wrapper>.vxe-table--header .vxe-header--row')
        if (!header) return
        if (self.sortableD) self.sortableD.destroy()
        const scrollEl = xTable.$el.querySelector('.vxe-table--body-wrapper')
        self.sortableD = Sortable.create(header, {
          handle: '.vxe-header--column',
          animation: 180,
          delay: 0,
          draggable: '.index-drag',
          scroll: scrollEl || true,
          scrollSensitivity: 100,
          scrollSpeed: 10,
          bubbleScroll: true,
          onEnd: ({ item, newIndex, oldIndex }) => {
            self.$nextTick(() => {
              const columns = _.cloneDeep(self.tableColumnD[self.activeTabD])
              const oldItem = columns[oldIndex]
              columns.splice(oldIndex, 1)
              columns.splice(newIndex, 0, oldItem)
              self.$set(self.tableColumnD, self.activeTabD, columns)
            })
          }
        })
      })
    },
    /* 组合对比-行拖拽排序 */
    rowDropC() {
      const self = this
      this.$nextTick(() => {
        let xTable = this.$refs.vxeTableC
        if (!xTable) return
        const tbody = xTable.$el.querySelector('.body--wrapper>.vxe-table--body tbody')
        self.sortableC = Sortable.create(tbody, {
          handle: '.vxe-body--row',
          animation: 180,
          delay: 0,
          onEnd: ({ newIndex, oldIndex, item }) => {
            if (newIndex === oldIndex) return
            // 先将 DOM 恢复到拖拽前的位置，避免与 vxe-table 重渲染冲突
            const parent = item.parentNode
            const children = parent.children
            if (oldIndex < newIndex) {
              parent.insertBefore(item, children[oldIndex])
            } else {
              parent.insertBefore(item, children[oldIndex + 1])
            }
            // 再更新数据，让 vxe-table 自行渲染
            const tableDataClone = [...self.tableDataC]
            const movedItem = tableDataClone.splice(oldIndex, 1)[0]
            tableDataClone.splice(newIndex, 0, movedItem)
            self.tableDataC = tableDataClone
          }
        })
      })
    },
    /**
     * list数据转tree
     * @param _data {Array} list数据
     * @param _id {String} id
     * @param _pId {String} pId
     */
    delDepartTree(_data, _id, _pId) {
      const data = _.cloneDeep(_data) // 防止改变原数据
      const obj = {} // 重新存储数据
      const res = [] // 存储最后结果
      const len = data.length
      const id = _id || 'id'
      const parentId = _pId || 'pId'
      const children = 'children'
      // 遍历原始数据data，构造obj数据，键名为id，值为数据
      for (let i = 0; i < len; i++) {
        obj[data[i][id]] = data[i]
      }
      // 遍历原始数据
      for (let j = 0; j < len; j++) {
        const list = data[j]
        // 通过每条数据的 pid 去obj中查询
        const parentList = obj[list[parentId]]
        if (parentList) {
          // 根据 pid 找到的是父节点，list是子节点，
          if (!parentList[children]) {
            parentList[children] = []
          }
          // 将子节点插入 父节点的 children 字段中
          parentList[children].push(list)
        } else {
          // pid 找不到对应值，说明是根结点，直接插到根数组中
          res.push(list)
        }
      }
      return res
    }
  }
}
</script>

<style lang="scss">
.tempConfig-wrapper {
  .dataBrowser-tempConfigDialog.el-dialog.is-fullscreen {
    width: 100% !important;

    .el-dialog__body {
      height: calc(100% - 50px);
      max-height: none !important;
      overflow: hidden !important;

      .tempConfig-container {
        display: flex;
        height: calc(100% - 56px);
        border: 1px solid #e4e7ed;
        border-radius: 4px;

        &.is-resizing {
          user-select: none;
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

          .index-tree {
            height: calc(100% - 40px);
            overflow-y: auto;
            overflow-x: hidden;

            .el-tree-node__content:has(.parent-node) {
              .el-checkbox {
                display: none;
              }
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

          .right-dimension-config {
            height: 98%;
            overflow-y: auto;
            padding: 10px;
            background-color: #f5f7fa;

            .empty-tip {
              height: 100%;
              display: flex;
              flex-direction: column;
              justify-content: center;
              align-items: center;
              color: #909399;
              gap: 12px;

              i {
                font-size: 40px;
              }
            }

            .config-list {
              display: flex;
              flex-direction: column;
              gap: 10px;

              .config-card {
                border: 1px solid #ebeef5;
                border-radius: 12px;
                display: flex;
                padding: 16px;
                background: #fff;
                transition: transform 0.2s, box-shadow 0.2s;

                &:hover {
                  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);

                  .delete-btn {
                    opacity: 1;
                  }
                }

                &.highlight-card {
                  border-color: #409eff;
                  box-shadow: 0 0 12px rgba(64, 158, 255, 0.25);
                  background-color: #f4f9ff;
                }

                .card-left {
                  width: 140px;
                  padding-right: 20px;
                  display: flex;
                  align-items: center;
                  border-right: 1px solid #f0f0f0;

                  .index-name {
                    font-size: 16px;
                    font-weight: 600;
                    color: #409eff;
                    line-height: 1.4;
                    word-break: break-all;

                    &.invalid {
                      color: #f56c6c;
                    }
                  }
                }

                .card-right {
                  flex: 1;
                  padding: 0 24px;
                  display: flex;
                  flex-direction: column;
                  gap: 12px;
                  min-width: 0;

                  .dimension-row {
                    display: flex;
                    align-items: flex-start;

                    .dim-label {
                      width: 70px;
                      font-size: 13px;
                      color: #606266;
                      white-space: nowrap;
                      line-height: 32px;
                    }

                    .dim-controls {
                      flex: 1;
                      display: flex;
                      align-items: flex-start;
                      gap: 10px;
                      flex-wrap: wrap;
                    }

                    .dim-checkbox-group {
                      display: flex !important;
                      flex-wrap: wrap !important;
                      gap: 8px !important;
                      align-items: center !important;

                      .el-checkbox {
                        margin-right: 0 !important;
                        margin-left: 0 !important;
                        border-radius: 6px !important;

                        &.is-bordered {
                          height: 32px !important;
                          line-height: 10px !important;
                          padding: 8px 12px !important;
                        }
                      }

                      .toggle-all-link {
                        font-size: 13px;
                        color: #409eff;
                        cursor: pointer;
                        white-space: nowrap;
                        user-select: none;
                        margin-left: 4px;

                        &:hover {
                          color: #66b1ff;
                          text-decoration: underline;
                        }
                      }
                    }

                    .dim-radio-group {
                      display: flex !important;
                      flex-wrap: wrap !important;
                      gap: 8px !important;

                      .el-radio {
                        margin-right: 0 !important;
                        margin-left: 0 !important;
                        border-radius: 6px !important;

                        &.is-bordered {
                          height: 32px !important;
                          line-height: 10px !important;
                          padding: 8px 12px !important;
                        }
                      }
                    }
                  }
                }

                .card-action {
                  width: 32px;
                  display: flex;
                  justify-content: center;
                  align-items: flex-start;

                  .delete-btn {
                    font-size: 18px;
                    color: #f56c6c;
                    cursor: pointer;
                    opacity: 0.3;
                    transition: opacity 0.2s;

                    &:hover {
                      transform: scale(1.1);
                    }
                  }
                }
              }
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

        &.is-resizing {

          .tempConfig-left,
          .tempConfig-center {
            transition: none;
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
          padding: 4px;
          height: calc(100% - 40px);
          overflow-y: auto;
          overflow-x: hidden;

          .draggable-item {
            margin-bottom: 4px;

            &:hover {
              opacity: 0.8;
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
            justify-content: space-between;

            .index-tag-label {
              flex: 1;
              overflow: hidden;
              white-space: nowrap;
              text-overflow: ellipsis;
              cursor: pointer;
            }

            .invalid {
              color: #f56c6c;
            }
          }

          .d-type-group {
            margin-bottom: 15px;
            border: 1px solid #e4e7ed;
            border-radius: 4px;

            .group-title {
              background-color: #f5f7fa;
              padding: 8px 12px;
              font-size: 13px;
              font-weight: 600;
              border-bottom: 1px solid #e4e7ed;
              margin-bottom: 8px;
            }

            .draggable-item {
              margin: 0 8px 8px 8px;
            }
          }
        }
      }
    }
  }
}

// C类型表格第一列背景色与表头一致
.index-header-cell {
  background-color: #f8f8f9 !important;
  font-weight: 600;
}
</style>