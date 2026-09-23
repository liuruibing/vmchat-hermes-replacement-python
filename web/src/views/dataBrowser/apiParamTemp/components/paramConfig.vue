<template>
  <div class="paramConfig-wrapper">
    <el-dialog :visible.sync="visible" :title="dialogTitle" custom-class="apiManager-paramConfigDialog"
      :fullscreen="true" :close-on-click-modal="false" :close-on-press-escape="false" @closed="handleClose"
      v-loading="loading">
      <div class="paramConfig-header">
        <div class="header-left">
          <span class="template-name">{{ dialogTitle }}</span>
          <el-form ref="headerFormRef" :model="paramForm" :rules="paramFormRules" size="small"
            class="header-inline-form" @submit.native.prevent>
            <el-form-item label="接口名称" prop="vcInterfacceName" class="header-form-item">
              <el-input v-model.trim="paramForm.vcInterfacceName" placeholder="请输入接口名称"
                style="width: 180px;"></el-input>
            </el-form-item>
            <el-form-item label="备注" prop="vcRemake" class="header-form-item">
              <el-input v-model.trim="paramForm.vcRemake" placeholder="请输入" style="width: 220px;"></el-input>
            </el-form-item>
            <el-form-item class="header-form-item">
              <el-button type="primary" size="small" @click="saveParams">保存模板</el-button>
              <el-button type="info" plain size="small" @click="handleClose">取消</el-button>
            </el-form-item>
          </el-form>
        </div>
        <div class="header-right">
          <el-button type="success" size="small" @click="generateCode">查看代码</el-button>
          <i class="el-icon-close close-btn" @click="handleClose" title="关闭"></i>
        </div>
      </div>

      <!-- 预设参数设置 -->
      <div class="paramConfig-top">
        <el-collapse v-model="activeNames">
          <el-collapse-item title="预设参数设置" name="1">
            <template #title>
              <span>预设参数设置 <i class="el-icon-setting"></i></span>
            </template>
            <el-form ref="paramFormRef" :model="paramForm" :rules="paramFormRules" :inline="true" size="small">
              <el-row>
                <el-col :span="24">
                  <el-form-item label="产品" prop="fundNameStr">
                    <el-tooltip :content="paramForm.fundNameStr" :disabled="!paramForm.fundNameStr"
                      placement="top-start" effect="light">
                      <el-input v-model="paramForm.fundNameStr" placeholder="请选择产品" size="small" readonly
                        @click.native="openFundListDialog"></el-input>
                    </el-tooltip>
                  </el-form-item>
                  <el-form-item label="时间" prop="timeSection">
                    <el-date-picker v-model="paramForm.timeSection" size="small" type="daterange" range-separator="-"
                      start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd"></el-date-picker>
                  </el-form-item>
                  <el-form-item label="数据频率" prop="vcDataStep">
                    <el-select v-model="paramForm.vcDataStep" placeholder="请选择数据频率" size="small" clearable filterable>
                      <el-option v-for="item in dataFrequencyOptions" :key="item.dimCde" :label="item.dimNme"
                        :value="item.dimCde"></el-option>
                    </el-select>
                  </el-form-item>
                  <br>
                  <div style="display: inline-block">
                    <el-form-item label="基准类型">
                      <el-select v-model="paramForm.ZB_INDEXTYPE" placeholder="请选择" size="small">
                        <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="paramForm.ZB_INDEXTYPE == '1'" style="display: inline-block">
                    <el-form-item label="选择基准">
                      <el-select v-model="paramForm.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <div v-show="paramForm.ZB_INDEXTYPE == '2'" style="display: inline-block">
                    <el-form-item label="基准 A">
                      <el-select v-model="paramForm.ZB_INDEXCODEA" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="比例">
                      <el-input v-model="paramForm.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important"
                        @blur="handleInputWeight('A')"></el-input>
                      %
                    </el-form-item>
                  </div>
                  <div v-show="paramForm.ZB_INDEXTYPE == '2'" style="display: inline-block">
                    <el-form-item label="基准 B">
                      <el-select v-model="paramForm.ZB_INDEXCODEB" placeholder="请选择" size="small">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="比例">
                      <el-input v-model="paramForm.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important"
                        @blur="handleInputWeight('B')"></el-input>
                      %
                    </el-form-item>
                  </div>
                  <div style="display: inline-block">
                    <el-form-item label="对比基准">
                      <el-select v-model="paramForm.contrasCode" clearable collapse-tags multiple placeholder="请选择"
                        size="small" :class="paramForm.contrasCode.length > 1 && 'custom-select-multiple-tags50'">
                        <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <!-- <div style="display: inline-block">
                    <el-form-item label="行业类型">
                      <el-select v-model="paramForm.industryType" clearable placeholder="请选择"
                        size="small">
                        <el-option v-for="item in industryTypeOptions" :key="item.id" :label="item.label"
                          :value="item.id"></el-option>
                      </el-select>
                    </el-form-item>
                  </div>
                  <el-form-item label="因子类型" prop="factorType">
                    <template slot="label">因子类型
                      <el-tooltip content="只作用于多因子报告类型" placement="top" effect="light">
                        <i class="el-icon-info"></i>
                      </el-tooltip>
                    </template>
                    <el-select v-model="paramForm.factorType" size="small" clearable filterable>
                      <el-option v-for="item in factorTypeOptionList" :key="item.dimCde" :label="item.dimNme"
                        :value="item.dimCde" />
                    </el-select>
                  </el-form-item> -->
                </el-col>
              </el-row>
            </el-form>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="paramConfig-main">
        <!-- 左侧指标树 -->
        <div class="main-left" :style="{ width: leftWidth + 'px' }">
          <div class="section-title">
            <span class="title-text">指标列表</span>
            <el-select :value="treeType" size="mini" class="tree-type-select" @change="handleTreeTypeChange">
              <el-option v-for="item in indexTypeList" :key="item.dimCde" :label="item.dimNme"
                :value="item.dimCde"></el-option>
            </el-select>
          </div>
          <div style="display: flex; padding: 12px 12px 0;" v-if="['A', 'C'].includes(treeType)">
            <el-select :value="paramForm.industryType" placeholder="行业类型" size="mini" @change="handleIndustryTypeChange">
              <el-option v-for="item in industryTypeOptions" :key="item.id" :label="item.label"
                :value="item.id"></el-option>
            </el-select>
            <el-select :value="paramForm.factorType" placeholder="因子类型" size="mini" @change="handleFactorTypeChange">
              <el-option v-for="item in factorTypeOptionList" :key="item.dimCde" :label="item.dimNme"
                :value="item.dimCde" />
            </el-select>
          </div>
          <div class="search-box">
            <el-input placeholder="搜索指标" prefix-icon="el-icon-search" style="width: 100% !important"
              v-model="filterText" size="small" clearable></el-input>
          </div>
          <div class="tree-container">
            <el-tree ref="indexTree" :data="indexTreeData" :props="{ label: 'vcIndexName', children: 'children' }"
              node-key="vcId" show-checkbox :check-strictly="true" default-expand-all :filter-node-method="filterNode"
              @check="handleCheck">
              <span slot-scope="{ node }" :class="['custom-tree-node', node.isLeaf ? 'leaf-node' : 'parent-node']"
                :title="node.label">
                <i :class="node.isLeaf ? 'el-icon-document' : 'el-icon-folder'"></i>
                <span class="label-text" v-html="highlightKeyword(node.label)"></span>
              </span>
            </el-tree>
          </div>
        </div>

        <!-- 拖拽条 -->
        <div class="resize-bar" @mousedown="initDrag"></div>

        <!-- 右侧参数设置区 -->
        <div class="main-right">
          <div v-if="selectedIndexList.length === 0" class="empty-tip">
            <i class="el-icon-info"></i>
            <span>请在左侧勾选指标进行参数配置</span>
          </div>
          <div v-else class="config-list">
            <div v-for="item in selectedIndexList" :key="item.vcId" class="config-card">
              <div class="card-left">
                <span :class="['index-name', validationClass(item)]">{{ item.vcIndexName }}</span>
              </div>
              <div class="card-right">
                <!-- 明细维度 -->
                <div v-if="item.params && item.params.details && item.params.details.length" class="dimension-row">
                  <span class="dim-label">明细维度：</span>
                  <div class="dim-controls">
                    <el-checkbox-group v-model="item.paramsValue.details" size="small" class="dim-checkbox-group">
                      <el-checkbox v-for="opt in item.params.details" :key="opt.vcId" :label="opt" border>{{
                        opt.vcIndexName }}</el-checkbox>
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
                    <el-checkbox-group v-model="item.paramsValue.times" size="small" class="dim-checkbox-group">
                      <el-checkbox v-for="opt in item.params.times" :key="opt.vcId" :label="opt" border>{{
                        opt.vcIndexName }}</el-checkbox>
                      <a class="toggle-all-link" @click="toggleAll(item, 'times')">
                        {{ item.paramsValue.times.length === item.params.times.length ? '取消全选' : '全选' }}
                      </a>
                    </el-checkbox-group>
                  </div>
                </div>
                <!-- 单位维度 -->
                <div v-if="item.params && item.params.units && item.params.units.length" class="dimension-row">
                  <span class="dim-label">单位维度：</span>
                  <el-radio-group v-model="item.paramsValue.unit" size="small" class="dim-radio-group">
                    <el-radio v-for="unit in item.params.units" :key="unit.vcId" :label="unit" border>{{
                      unit.vcIndexName }}</el-radio>
                  </el-radio-group>
                </div>
              </div>
              <div class="card-action">
                <i class="el-icon-delete delete-btn" @click="removeIndex(item)"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 代码展示弹窗 -->
    <code-dialog :visible.sync="codeDialogVisible" :java-code="generatedJavaCode" :python-code="generatedPythonCode" />

    <!-- 产品列表弹窗 -->
    <product-selector v-if="fundListDialogVisible" :multiple="true" :leftList="false"
      :dialog-visible="fundListDialogVisible" :tree-data="treeData" :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList" default-checked-keys="wdgz" @closedialog="fundListDialogVisible = false"
      @submitdialog="handleFundListSubmit"></product-selector>
  </div>
</template>

<script>
import CONSTANTS from '../../constants.js'
import CODESTR from '../../code.js'
import productSelector from '@/components/productSelector'
import CodeDialog from './codeDialog.vue'
import { Base64 } from 'js-base64'
import dataBrowserApi from '@/views/dataBrowser/tempManage/api.js'
import pageApi from '../api.js'

export default {
  name: 'ParamConfig',
  components: {
    productSelector,
    CodeDialog
  },
  data() {
    return {
      visible: false,
      loading: false,
      dialogType: 'add',
      dialogTitle: '参数配置',
      activeNames: ['1'],
      isShowMoreQuery: false,
      paramForm: {
        vcInterfacceName: '',
        vcDataStep: '',
        fundNameStr: '',
        timeSection: [],
        vcBenchmark: '',
        vcRemake: '',
        ZB_INDEXTYPE: '1',
        ZB_INDEXCODEA: '000300',
        ZB_INDEXWEIGHTA: '0.0000',
        ZB_INDEXCODEB: '000300',
        ZB_INDEXWEIGHTB: '0.0000',
        contrasCode: [],
        industryType: 'SWSR',
        factorType: 'CNE5'
      },
      paramFormRules: {
        vcInterfacceName: [
          { required: true, message: '请输入接口名称', trigger: 'change' }
        ]
      },
      ZB_INDEXTYPEOption: [
        { id: '0', label: '无基准' },
        { id: '1', label: '单基准' },
        { id: '2', label: '复合基准' }
      ],
      industryTypeOptions: [
        { id: 'SWSR', label: '申万行业' },
        { id: 'ZXSR', label: '中信行业' }
      ],
      factorTypeOptionList: [
        { dimCde: 'CNE5', dimNme: 'CNE5' },
        { dimCde: 'CNE6', dimNme: 'CNE6' }
      ],
      filterText: '',
      leftWidth: 260,
      indexTypeList: [],
      treeType: 'A',
      rowData: {},
      rowDetails: {},
      indexListData: [],
      indexTreeData: [],
      selectedIndexList: [],
      keyMap: {},
      codeDialogVisible: false,
      generatedJavaCode: '',
      generatedPythonCode: '',
      dataFrequencyOptions: CONSTANTS.DATAFREQUENCY,
      benchMarkOptions: [],
      fundListDialogVisible: false,
      treeData: [
        {
          label: '产品列表',
          id: 'zstgwb'
        },
        {
          label: '我的关注',
          id: 'wdgz',
          children: [
            {
              label: '默认分组',
              id: 'mrfz'
            },
            {
              label: '权益组',
              id: 'qyz'
            }
          ]
        }
      ],
      showTreeKeyArray: ['产品列表', '我的关注'],
      selectList: []
    }
  },
  watch: {
    filterText(val) {
      this.$refs.indexTree && this.$refs.indexTree.filter(val)
    }
  },
  mounted() {
    this.visible = true
    this.indexTypeList = [...CONSTANTS.TEMPTYPE]

    // 初始化基准数据 (此处可以按照实际情况获取，暂时用模拟数据)
    this.benchMarkOptions = [
      {
        dimCde: '000300',
        dimNme: '沪深300'
      },
      {
        dimCde: '000905',
        dimNme: '中证500'
      }
    ]

    this.getKey();
  },
  methods: {
    // 获取密钥
    getKey() {
      // index_browser_api_strategy_key
      this.keyMap = {
        appKey: 'appKey',
        appSecret: 'appSecret',
        manageId: 'manageId'
      }
      // TODO：后续换成接口获取
    },
    // 校验指标是否已选择参数
    validationClass(item) {
      if (!item.params || !item.paramsValue) {
        return 'valid'
      }
      if (item.params.details && item.params.details.length && (!item.paramsValue.details || !item.paramsValue.details.length)) {
        return 'invalid'
      }
      if (item.params.times && item.params.times.length && (!item.paramsValue.times || !item.paramsValue.times.length)) {
        return 'invalid'
      }
      if (item.params.units && item.params.units.length && !item.paramsValue.unit) {
        return 'invalid'
      }
      return 'valid'
    },
    async init(data, type = 'add') {
      this.rowData = _.cloneDeep(data || {})
      this.rowDetails = {}
      this.dialogType = type
      this.dialogTitle = ['add', 'copyAdd'].includes(type) ? '新增参数模板' : '编辑参数模板'
      this.treeType = data.vcIndexType || "A"

      let configObj = {}
      if (data.vcConfig || data.VcConfig) {
        try {
          const configStr = data.vcConfig || data.VcConfig
          configObj = typeof configStr === 'string' ? JSON.parse(configStr) : configStr
        } catch (e) {
          console.error('Failed to parse vcConfig', e)
        }
      }

      this.paramForm = {
        vcInterfacceName: data.vcInterfacceName || '',
        vcDataStep: configObj.vcDataStep || data.vcDataStep || '',
        fundNameStr: configObj.fundNameStr || data.fundNameStr || '',
        timeSection: configObj.timeSection ? configObj.timeSection : (data.timeSection ? data.timeSection.split('至') : []),
        vcBenchmark: configObj.vcBenchmark || data.vcBenchmark || '',
        vcRemake: data.vcRemake || '',
        ZB_INDEXTYPE: configObj.ZB_INDEXTYPE || data.ZB_INDEXTYPE || '1',
        ZB_INDEXCODEA: configObj.ZB_INDEXCODEA || data.ZB_INDEXCODEA || '000300',
        ZB_INDEXWEIGHTA: configObj.ZB_INDEXWEIGHTA || data.ZB_INDEXWEIGHTA || '0.0000',
        ZB_INDEXCODEB: configObj.ZB_INDEXCODEB || data.ZB_INDEXCODEB || '000300',
        ZB_INDEXWEIGHTB: configObj.ZB_INDEXWEIGHTB || data.ZB_INDEXWEIGHTB || '0.0000',
        contrasCode: configObj.contrasCode || data.contrasCode || [],
        industryType: configObj.industryType || data.industryType || 'SWSR',
        factorType: configObj.factorType || data.factorType || 'CNE5'
      }

      if (configObj.fundList && configObj.fundList.length > 0) {
        this.selectList = configObj.fundList.map(item => ({ VC_FUNDNAME: item.VC_FUNDNAME, VC_FUNDCODE: item.VC_FUNDCODE }))
      } else {
        this.selectList = []
      }

      await this.getIndexData()
      // TODO 处理编辑回填
      if (this.dialogType !== 'add') {
        if (configObj.colList && configObj.colList.length > 0) {
          this.rowDetails = { colList: configObj.colList }
        } else {
          await this.getRowDetails();
        }
        // 回显参数
        this.editInit();
      }
    },
    // 回显参数
    editInit() {
      const rowDetails = _.cloneDeep(this.rowDetails || {})
      let colList = _.cloneDeep(rowDetails.cols || rowDetails.colList || [])

      if (!Array.isArray(colList) || !colList.length) {
        this.selectedIndexList = []
        this.$nextTick(() => {
          this.$refs.indexTree && this.$refs.indexTree.setCheckedKeys([])
        })
        return
      }

      // 保持和老逻辑一致：按列顺序回显
      colList = colList.sort((a, b) => (a.fColOrder || 0) - (b.fColOrder || 0))
      const beforeCodes = ['before_code', 'ggzb', 'gzzb', 'pzzb', 'gjzb']
      colList = colList.filter(item => !beforeCodes.includes(item.vcIndexCode))

      const codeMap = new Map()
      colList.forEach((col) => {
        const key = col.vcIndexCode
        if (!key) return
        if (!codeMap.has(key)) {
          codeMap.set(key, {
            vcIndexCode: key,
            vcInfoDefineId: '',
            vcTypeCode: '',
            vcTypeName: '',
            vcModelValue: '',
            paramsValue: {
              details: [],
              times: [],
              vcItemId: [],
              vcTimeId: [],
              vcUnitType: ''
            }
          })
        }
        const target = codeMap.get(key)
        if (col.vcInfoDefineId && !target.vcInfoDefineId) target.vcInfoDefineId = col.vcInfoDefineId
        if (col.vcTypeCode) target.vcTypeCode = col.vcTypeCode
        if (col.vcTypeName) target.vcTypeName = col.vcTypeName
        if (col.vcModelValue) target.vcModelValue = col.vcModelValue
        if (col.vcItemDefineId && !target.paramsValue.vcItemId.includes(col.vcItemDefineId)) {
          target.paramsValue.vcItemId.push(col.vcItemDefineId)
        }
        if (col.vcTimeDefineId && !target.paramsValue.vcTimeId.includes(col.vcTimeDefineId)) {
          target.paramsValue.vcTimeId.push(col.vcTimeDefineId)
        }
        if (!target.paramsValue.vcUnitType && col.vcUnitType) {
          target.paramsValue.vcUnitType = col.vcUnitType
        }
      })

      const indexMap = new Map(this.indexListData.map(item => [item.vcId, item]))
      const selectedIndexList = []
      const checkedKeys = []
      codeMap.forEach((codeItem, code) => {
        const indexItem = indexMap.get(code)
        if (!indexItem) return

        const selectedItem = _.cloneDeep(indexItem)
        const paramsValue = {
          details: [],
          times: [],
          unit: {}
        }
        // 明细维度回显 - 从克隆后的对象中找引用
        if (Array.isArray(codeItem.paramsValue.vcItemId) && Array.isArray(selectedItem.params.details)) {
          paramsValue.details = codeItem.paramsValue.vcItemId.map((itemId) => {
            return selectedItem.params.details.find(opt => opt.vcItemId === itemId)
          }).filter(Boolean)
        }
        // 时间维度回显 - 从克隆后的对象中找引用
        if (Array.isArray(codeItem.paramsValue.vcTimeId) && Array.isArray(selectedItem.params.times)) {
          paramsValue.times = codeItem.paramsValue.vcTimeId.map((timeId) => {
            return selectedItem.params.times.find(opt => opt.vcTimeId === timeId)
          }).filter(Boolean)
        }
        // 单位维度回显 - 从克隆后的对象中找引用
        if (codeItem.paramsValue.vcUnitType && Array.isArray(selectedItem.params.units)) {
          paramsValue.unit = selectedItem.params.units.find(unit => unit.vcId === codeItem.paramsValue.vcUnitType) || {}
        }
        selectedItem.paramsValue = paramsValue
        selectedItem.vcModelValue = codeItem.vcModelValue || ''
        selectedIndexList.push(selectedItem)
        checkedKeys.push(code)
      })

      this.selectedIndexList = selectedIndexList
      this.$nextTick(() => {
        this.$refs.indexTree && this.$refs.indexTree.setCheckedKeys(checkedKeys)
      })
    },
    handleIndustryTypeChange(val) {
      if (this.selectedIndexList && this.selectedIndexList.length > 0) {
        this.$confirm('切换行业类型将会清空右侧已选指标，确定继续吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.doIndustryTypeChange(val)
        }).catch(() => {})
      } else {
        this.doIndustryTypeChange(val)
      }
    },
    doIndustryTypeChange(val) {
      this.paramForm.industryType = val
      this.selectedIndexList = []
      this.$nextTick(() => {
        if (this.$refs.indexTree) {
          this.$refs.indexTree.setCheckedKeys([])
        }
      })
      this.filterText = ''
      this.getIndexData()
    },
    handleFactorTypeChange(val) {
      if (this.selectedIndexList && this.selectedIndexList.length > 0) {
        this.$confirm('切换因子类型将会清空右侧已选指标，确定继续吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.doFactorTypeChange(val)
        }).catch(() => {})
      } else {
        this.doFactorTypeChange(val)
      }
    },
    doFactorTypeChange(val) {
      this.paramForm.factorType = val
      this.selectedIndexList = []
      this.$nextTick(() => {
        if (this.$refs.indexTree) {
          this.$refs.indexTree.setCheckedKeys([])
        }
      })
      this.filterText = ''
      this.getIndexData()
    },
    handleTreeTypeChange(val) {
      if (this.selectedIndexList && this.selectedIndexList.length > 0) {
        this.$confirm('切换指标类型将会清空右侧已选指标，确定继续吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.doTreeTypeChange(val)
        }).catch(() => {})
      } else {
        this.doTreeTypeChange(val)
      }
    },
    doTreeTypeChange(val) {
      this.treeType = val
      // 切换类型后，清空已选数据
      this.selectedIndexList = []
      this.$nextTick(() => {
        if (this.$refs.indexTree) {
          this.$refs.indexTree.setCheckedKeys([])
        }
      })
      // 重新加载数据
      this.filterText = ''
      this.getIndexData()
    },
    // 获取指标树数据（与 tempConfig.vue 保持一致）
    getIndexData() {
      return new Promise((resolve) => {
        this.loading = true
        let apiMethod = ""
        switch (this.treeType) {
          case "A":
            apiMethod = "getIndexDetailInfoTreeList"
            break
          case "C":
            apiMethod = "getIndexDetailInfoTreeZHList"
            break
          case "D":
            apiMethod = "getIndexDetailInfoTreeGQList"
            break
          default:
            apiMethod = "getIndexDetailInfoTreeList"
            break
        }
        let params = {}
        if (['A', 'C'].includes(this.treeType)) {
          params = {
            vcIndustType: this.paramForm.industryType,
            vcFactorType: this.paramForm.factorType
          }
        }
        dataBrowserApi[apiMethod](params).then((res) => {
          const { status, data } = res.data
          if (status === 200 && data) {
            // 根据isIndexOrType字段区分指标和指标参数维度，去重并排序
            const indexList = data.filter((item) => item.isIndexOrType === '1')
              .sort((a, b) => a.fOrder - b.fOrder)
              .filter((item, index, arr) => arr.findIndex(i => i.vcId === item.vcId) === index)
            const indexParamList = data.filter((item) => item.isIndexOrType !== '1')
              .sort((a, b) => a.fOrder - b.fOrder)
            // 组装 indexListData
            this.indexListData = indexList.map((indexItem) => {
              // 查找当前指标对应的所有参数维度数据
              const relatedParams = indexParamList.filter((paramItem) => paramItem.vcPid === indexItem.vcId)

              // 分别归类明细、时间和单位维度数据
              const details = relatedParams.filter((item) => item.isIndexOrType === '3')
              const times = relatedParams.filter((item) => item.isIndexOrType === '2')
              const units = relatedParams.filter((item) => item.isIndexOrType === '4')

              // 配置模板类型D时，勾选指标若找不到对应的类型，则设置为“其他”，typeCode: "more"
              const validTypes = ['ggzb', 'gzzb', 'pzzb', 'gjzb']
              if (this.treeType === 'D') {
                if (!indexItem.vcTypeCode || !validTypes.includes(indexItem.vcTypeCode)) {
                  indexItem.vcTypeCode = 'more'
                  indexItem.vcTypeName = '其他'
                }
              }

              // 组装成要求的数据结构
              return {
                ...indexItem,
                params: {
                  details: details,
                  times: times,
                  units: units
                },
                paramsValue: {
                  details: [],
                  times: [],
                  unit: ''
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
    // 获取行详情
    getRowDetails() {
      return new Promise((resolve) => {
        const rowData = _.cloneDeep(this.rowData || {})
        // 优先使用上游已传入的详情结构，便于无接口场景回显
        const rowDetails = _.cloneDeep(rowData.rowDetails || rowData.detail || {})
        if (!Array.isArray(rowDetails.cols) || !rowDetails.cols.length) {
          if (Array.isArray(rowData.cols)) {
            rowDetails.cols = _.cloneDeep(rowData.cols)
          } else if (Array.isArray(rowData.colList)) {
            rowDetails.cols = _.cloneDeep(rowData.colList)
          } else {
            rowDetails.cols = []
          }
        }
        this.rowDetails = rowDetails
        resolve(rowDetails)
      })
    },
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
    // 勾选/取消勾选节点
    handleCheck(data, { checkedKeys }) {
      if (checkedKeys.includes(data.vcId)) {
        // 勾选 - 添加到已选列表
        const item = _.cloneDeep(data)
        if (item.params && Array.isArray(item.params.units) && item.params.units.length > 0) {
          item.paramsValue.unit = item.params.units[0]
        }
        this.selectedIndexList.push(item)
      } else {
        // 取消勾选 - 从列表移除
        const index = this.selectedIndexList.findIndex((item) => item.vcId === data.vcId)
        if (index !== -1) {
          this.selectedIndexList.splice(index, 1)
        }
      }
    },
    removeIndex(item) {
      const index = this.selectedIndexList.findIndex((i) => i.vcId === item.vcId)
      if (index > -1) {
        this.selectedIndexList.splice(index, 1)
        this.$refs.indexTree.setChecked(item.vcId, false)
      }
    },
    initDrag(e) {
      const startX = e.clientX
      const startWidth = this.leftWidth
      const onMouseMove = (moveEvent) => {
        const delta = moveEvent.clientX - startX
        this.leftWidth = Math.max(240, Math.min(500, startWidth + delta))
      }
      const onMouseUp = () => {
        document.removeEventListener('mousemove', onMouseMove)
        document.removeEventListener('mouseup', onMouseUp)
      }
      document.addEventListener('mousemove', onMouseMove)
      document.addEventListener('mouseup', onMouseUp)
    },
    handleClose() {
      this.visible = false
      this.$emit('close')
    },
    toggleAll(item, type) {
      if (item.paramsValue[type].length === item.params[type].length) {
        // 已全选 -> 取消全选
        this.$set(item.paramsValue, type, [])
      } else {
        // 未全选 -> 全选
        this.$set(item.paramsValue, type, [...item.params[type]])
      }
    },
    resetParams() {
      this.$confirm('确定要重置所有参数配置吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.selectedIndexList = []
        if (this.$refs.indexTree) {
          this.$refs.indexTree.setCheckedKeys([])
        }
        this.paramForm.vcDataStep = ''
        this.paramForm.fundNameStr = ''
        this.paramForm.timeSection = []
        this.paramForm.vcBenchmark = ''
        this.paramForm.vcRemake = ''
        this.paramForm.ZB_INDEXTYPE = '1'
        this.paramForm.ZB_INDEXCODEA = '000300'
        this.paramForm.ZB_INDEXWEIGHTA = '0.0000'
        this.paramForm.ZB_INDEXCODEB = '000300'
        this.paramForm.ZB_INDEXWEIGHTB = '0.0000'
        this.paramForm.contrasCode = []
        this.selectList = []
        this.$message.success('重置成功')
      }).catch(() => { })
    },
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
    },
    handleInputWeight(type) {
      if (type === 'A') {
        const val = this.paramForm.ZB_INDEXWEIGHTA
        const isValid = /^\d+(\.\d{1,4})?$/.test(val)
        if (!isValid) {
          this.$message.warning('请输入有效的正数，最多4位小数')
          this.paramForm.ZB_INDEXWEIGHTA = ''
        }
      } else {
        const val = this.paramForm.ZB_INDEXWEIGHTB
        const isValid = /^\d+(\.\d{1,4})?$/.test(val)
        if (!isValid) {
          this.$message.warning('请输入有效的正数，最多4位小数')
          this.paramForm.ZB_INDEXWEIGHTB = ''
        }
      }
    },
    // 打开产品列表弹窗
    openFundListDialog() {
      this.fundListDialogVisible = true
    },
    handleFundListSubmit(data) {
      this.selectList = data
      this.paramForm.fundNameStr = data.map((item) => item.VC_FUNDNAME).join(',')
      this.fundListDialogVisible = false
    },
    async saveParams() {
      const valid = await this.$refs.headerFormRef.validate().catch(() => { })
      if (!valid) {
        this.$message.warning('请输入接口名称！')
        return
      }
      if (!this.selectedIndexList || this.selectedIndexList.length === 0) {
        return this.$message.warning('请至少选择一个指标')
      }

      for (let i = 0; i < this.selectedIndexList.length; i++) {
        const item = this.selectedIndexList[i]

        const itemClass = this.validationClass(item)
        if (itemClass === 'invalid') {
          this.$message({
            message: `请完善【${item.vcIndexName}】的参数配置！`,
            type: 'warning'
          })
          return
        }
      }

      const params = this.getSubmitModel()

      let res = null
      if (this.dialogType === 'edit') {
        res = await pageApi.paramUpdate(params)
      } else {
        res = await pageApi.paramInsert(params)
      }

      const { status, message } = res.data;
      if (status === 200) {
        this.$message.success('参数保存成功')
        this.handleClose()
        this.$emit('refresh')
      } else {
        this.$message.error(message || '保存失败')
      }
    },
    // 构建上送后端的完整模型
    getSubmitModel() {
      const { vcInterfacceName, vcDataStep, timeSection, vcRemake, vcBenchmark, ZB_INDEXCODEA, ZB_INDEXCODEB, ZB_INDEXWEIGHTA, ZB_INDEXWEIGHTB, ZB_INDEXTYPE, contrasCode, industryType, factorType } = this.paramForm

      // 1. 构建 colList
      const colList = this.getColList()

      // 2. 构建代码片段并 Base64 编码
      const javaCode = this.getGeneratedJavaCode(colList)
      const pythonCode = this.getGeneratedPythonCode(colList)

      // 3. 构建基准 JSON
      const vcBenchmarkJson = this.getBenchmarkJson()

      const model = {
        vcStrategyType: 'C',
        vcInterfacceName: vcInterfacceName,
        vcIndexType: this.treeType,
        vcRemake: vcRemake || '',
        VcConfig: JSON.stringify({
          colList,
          ...this.paramForm,
          fundList: this.selectList.map(item => ({ VC_FUNDCODE: item.VC_FUNDCODE, VC_FUNDNAME: item.VC_FUNDNAME })),
          vcCode: {
            java: Base64.encode(javaCode || ''),
            python: Base64.encode(pythonCode || '')
          }
        }),
      }

      if (this.dialogType !== 'add' && this.rowData.vcStrategyId) {
        model.vcStrategyId = this.rowData.vcStrategyId
      }

      return model
    },
    // 构建指标列数据
    getColList() {
      const resList = []

      // 添加前置固定列
      if (['A', 'C'].includes(this.treeType)) {
        CONSTANTS.TEMPCOLBEFORE1.forEach(item => {
          resList.push({
            vcInfoDefineId: item.vcInfoDefineId,
            vcIndexCode: item.pId,
            vcColCode: item.dataIndex,
            vcColName: item.title,
            vcUnitType: '',
            vcUnitDefineId: item.vcUnitDefineId,
            vcScale: '',
            vcFormat: '',
            vcModelValue: '',
            vcItemDefineId: item.vcItemId,
            vcTimeDefineId: item.vcTimeId
          })
        })
      } else if (this.treeType === 'D') {
        CONSTANTS.TEMPCOLBEFORE.forEach(item => {
          resList.push({
            vcInfoDefineId: item.vcInfoDefineId,
            vcIndexCode: item.pId,
            vcColCode: item.dataIndex,
            vcColName: item.title,
            vcUnitType: '',
            vcUnitDefineId: item.vcUnitDefineId,
            vcScale: '',
            vcFormat: '',
            vcModelValue: '',
            vcItemDefineId: item.vcItemId,
            vcTimeDefineId: item.vcTimeId
          })
        })
      }

      // 添加所选指标列
      this.selectedIndexList.forEach(item => {
        const { paramsValue, params } = item
        const { details = [], times = [], unit } = paramsValue || {}
        const { details: detailList, times: timeList, units: unitList } = params || {}

        let vcItemIds = []
        let vcItemNames = []
        details.forEach(dItem => {
          vcItemIds.push(dItem.vcItemId)
          vcItemNames.push(dItem.vcIndexName)
        })

        let vcTimeIds = []
        let vcTimeNames = []
        times.forEach(tItem => {
          vcTimeIds.push(tItem.vcTimeId)
          vcTimeNames.push(tItem.vcIndexName)
        })

        const unitObj = unit || (unitList && unitList[0]) || {}

        if (details.length && times.length) {
          details.forEach((a, aIndex) => {
            times.forEach((b, bIndex) => {
              resList.push({
                vcInfoDefineId: item.vcInfoDefineId,
                vcIndexCode: item.vcId,
                vcColCode: `${item.vcId}_${a.vcId}_${b.vcId}`,
                vcColName: unitObj.vcId === 'original' || unitObj.vcIndexName == '原值' ?
                  `${item.vcIndexName}(${vcItemNames[aIndex]}-${vcTimeNames[bIndex]})` :
                  `${item.vcIndexName}(${vcItemNames[aIndex]}-${vcTimeNames[bIndex]})(${unitObj.vcIndexName})`,
                vcUnitType: unitObj.vcId,
                vcUnitDefineId: unitObj.vcUnitId,
                vcScale: unitObj.vcScale || '',
                vcFormat: unitObj.vcFormat || '',
                vcModelValue: '',
                vcItemDefineId: vcItemIds[aIndex],
                vcTimeDefineId: vcTimeIds[bIndex],
              })
            })
          })
        } else if (details.length && !times.length) {
          details.forEach((a, aIndex) => {
            resList.push({
              vcInfoDefineId: item.vcInfoDefineId,
              vcIndexCode: item.vcId,
              vcColCode: `${item.vcId}_${a.vcId}`,
              vcColName: unitObj.vcId === 'original' || unitObj.vcIndexName == '原值' ?
                `${item.vcIndexName}(${vcItemNames[aIndex]})` :
                `${item.vcIndexName}(${vcItemNames[aIndex]})(${unitObj.vcIndexName})`,
              vcUnitType: unitObj.vcId,
              vcUnitDefineId: unitObj.vcUnitId,
              vcScale: unitObj.vcScale || '',
              vcFormat: unitObj.vcFormat || '',
              vcModelValue: '',
              vcItemDefineId: vcItemIds[aIndex],
              vcTimeDefineId: '',
            })
          })
        } else if (!details.length && times.length) {
          times.forEach((b, bIndex) => {
            resList.push({
              vcInfoDefineId: item.vcInfoDefineId,
              vcIndexCode: item.vcId,
              vcColCode: `${item.vcId}_${b.vcId}`,
              vcColName: unitObj.vcId === 'original' || unitObj.vcIndexName == '原值' ?
                `${item.vcIndexName}(${vcTimeNames[bIndex]})` :
                `${item.vcIndexName}(${vcTimeNames[bIndex]})(${unitObj.vcIndexName})`,
              vcUnitType: unitObj.vcId,
              vcUnitDefineId: unitObj.vcUnitId,
              vcScale: unitObj.vcScale || '',
              vcFormat: unitObj.vcFormat || '',
              vcModelValue: '',
              vcItemDefineId: '',
              vcTimeDefineId: vcTimeIds[bIndex],
            })
          })
        } else {
          resList.push({
            vcInfoDefineId: item.vcInfoDefineId,
            vcIndexCode: item.vcId,
            vcColCode: item.vcId,
            vcColName: unitObj.vcId === 'original' || unitObj.vcIndexName == '原值' ?
              `${item.vcIndexName}` :
              `${item.vcIndexName}(${unitObj.vcIndexName})`,
            vcUnitType: unitObj.vcId,
            vcUnitDefineId: unitObj.vcUnitId,
            vcScale: unitObj.vcScale || '',
            vcFormat: unitObj.vcFormat || '',
            vcModelValue: '',
            vcItemDefineId: '',
            vcTimeDefineId: '',
          })
        }
      })

      // 加上排序
      resList.forEach((col, index) => {
        col.fColOrder = index + 1
      })
            
      return resList
    },
    // 获取基准配置 JSON
    getBenchmarkJson() {
      const { vcBenchmark } = this.paramForm
      const benchItem = this.benchMarkOptions.find(opt => opt.dimCde === vcBenchmark) || {}
      const benchmarkParams = {
        singleBenchmark: vcBenchmark,
        benchmarkType: '1', // 默认单基准类型
        vcBenchmarkShow: benchItem.dimNme || ''
      }
      return JSON.stringify(benchmarkParams)
    },
    // 获取 Java 代码
    getGeneratedJavaCode(colList) {
      let dateArr = this.paramForm.timeSection || []

      let fundInfos = []
      if (this.selectList && this.selectList.length > 0) {
        fundInfos = this.selectList.map(item => {
          return {
            isPack: false,
            fundCodeTitle: item.VC_FUNDNAME || "",
            fundCodeKey: item.VC_FUNDCODE || "",
            funds: [{ fundCode: item.VC_FUNDCODE || "", dataSource: "" }]
          }
        })
      } else {
        fundInfos = [{
          isPack: false,
          fundCodeTitle: "测试产品-请替换为真实产品",
          fundCodeKey: "000000",
          funds: [{ fundCode: "000000", dataSource: "" }]
        }]
      }

      let reqBody = {
        fundInfos: fundInfos,
        beginDate: dateArr[0] || "",
        endDate: dateArr[1] || "",
        singleBenchmark: this.paramForm.ZB_INDEXTYPE === '1' ? (this.paramForm.ZB_INDEXCODEA || "") : "",
        dateType: "workDate",
        dateStep: this.paramForm.vcDataStep || "1",
        paramMap: {
          templateCode: this.rowData.vcStrategyId || "",
          beginDate: dateArr[0] || "",
          endDate: dateArr[1] || "",
          benchmarks: this.paramForm.ZB_INDEXTYPE || "1",
          benchmarkA: this.paramForm.ZB_INDEXCODEA || "",
          benchmarkB: this.paramForm.ZB_INDEXCODEB || "",
          benchmarkAValue: this.paramForm.ZB_INDEXWEIGHTA || "0.0000",
          benchmarkBValue: this.paramForm.ZB_INDEXWEIGHTB || "0.0000",
          kpiCode: "",
          contrasCode: Array.isArray(this.paramForm.contrasCode) ? this.paramForm.contrasCode.join(',') : (this.paramForm.contrasCode || ""),
          industryType: this.paramForm.industryType || "SWSR",
          desensitizationFlag: "",
          desensitizationFun: "ALL",
          dataFreqOpen: "true",
          dataFreq: this.paramForm.vcDataStep || "1"
        },
        colList: colList
      }

      const jsonStr = JSON.stringify(reqBody, null, 2)
      const lines = jsonStr.split('\n')

      const commentMap = {
        '"fundInfos":': '产品信息列表',
        '"fundCodeTitle":': '产品名称',
        '"fundCodeKey":': '产品代码',
        '"beginDate":': '开始日期',
        '"endDate":': '结束日期',
        '"singleBenchmark":': '单基准代码',
        '"dateType":': '日期类型',
        '"dateStep":': '数据步长',
        '"paramMap":': '参数集合',
        '"templateCode":': '模板代码 -- 不填',
        '"benchmarks":': '基准类型：1-单基准，2-复合基准',
        '"benchmarkA":': '基准A代码',
        '"benchmarkB":': '基准B代码',
        '"benchmarkAValue":': '基准A比例',
        '"benchmarkBValue":': '基准B比例',
        '"contrasCode":': '对比基准代码集合',
        '"industryType":': '行业类型',
        '"dataFreq":': '数据频率',
        '"colList":': '指标表头配置列表',
        '"vcInfoDefineId":': '指标定义ID',
        '"vcColName":': '表头名称',
        '"fColOrder":': '列排序'
      }

      const javaJsonLines = lines.map((line, index) => {
        // 去除每行的前导空格，使得拼接出来的 JSON 更紧凑，且不会有换行符
        let trimmedLine = line.trim()
        let escapedLine = trimmedLine.replace(/"/g, '\\"')

        let comment = ''
        for (let key in commentMap) {
          if (trimmedLine.startsWith(key)) {
            comment = ' // ' + commentMap[key]
            break
          }
        }

        if (index === 0) {
          return '        return "' + escapedLine + '"' + comment
        } else if (index === lines.length - 1) {
          return '            + "' + escapedLine + '";' + comment
        } else {
          return '            + "' + escapedLine + '"' + comment
        }
      })
      const jsonBodyStr = javaJsonLines.join('\n')

      let host = window.location.origin
      if (process.env.BASE_API && !process.env.BASE_API.startsWith('http')) {
        host += process.env.BASE_API
      } else if (process.env.BASE_API) {
        host = process.env.BASE_API
      }

      let javaTemplate = `import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class ApiCaller {

    public static void main(String[] args) {
        //用户TOKEN
        String token = "替换用户TOKEN";

        //URL接口地址（js代码动态替换为当前后端访问地址）
        String host="&host";
        String intf="/api/browser/index_token";
        String url = host+intf;
        String jsonBody = buildJsonBody();
        String response = sendPostRequest(url, token, jsonBody);
        System.out.println("响应结果: " + response);
    }
    
    private static String buildJsonBody() {
&jsonBodyStr
    }
    
    private static String sendPostRequest(String urlString, String token, String jsonBody) {
        HttpURLConnection connection = null;
        try {
            URL url = new URL(urlString);
            connection = (HttpURLConnection) url.openConnection();
            
            // 设置请求方法
            connection.setRequestMethod("POST");
            
            // 设置请求头
            connection.setRequestProperty("Content-Type", "application/json; charset=UTF-8");
            connection.setRequestProperty("Accept", "application/json");
            connection.setRequestProperty("token", token);
            
            // 允许输出
            connection.setDoOutput(true);
            connection.setDoInput(true);
            
            // 写入请求Body
            try (OutputStream os = connection.getOutputStream()) {
                byte[] input = jsonBody.getBytes(StandardCharsets.UTF_8);
                os.write(input, 0, input.length);
            }
            
            // 获取响应码
            int responseCode = connection.getResponseCode();
            System.out.println("响应码: " + responseCode);
            
            // 判断状态码
            if (responseCode >= 200 && responseCode < 300) {
                // 成功响应（2xx）
                StringBuilder response = new StringBuilder();
                try (BufferedReader br = new BufferedReader(
                        new InputStreamReader(connection.getInputStream(), StandardCharsets.UTF_8))) {
                    String line;
                    while ((line = br.readLine()) != null) {
                        response.append(line);
                    }
                }
                return response.toString();
            } else {
                throw new RuntimeException(String.format("HTTP请求失败，状态码: %d", responseCode));
            }
            
        } catch (Exception e) {
            e.printStackTrace();
            // 尝试读取错误流
            if (connection != null) {
                try (BufferedReader br = new BufferedReader(
                        new InputStreamReader(connection.getErrorStream(), StandardCharsets.UTF_8))) {
                    StringBuilder errorResponse = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        errorResponse.append(line);
                    }
                    return "错误响应: " + errorResponse.toString();
                } catch (IOException ex) {
                    return "请求失败: " + e.getMessage();
                }
            }
            return "请求失败: " + e.getMessage();
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}`

      return javaTemplate.replace('&jsonBodyStr', jsonBodyStr).replace('&host', host)
    },
    // 获取 Python 代码
    getGeneratedPythonCode(colList) {
      let dateArr = this.paramForm.timeSection || []

      let fundInfos = []
      if (this.selectList && this.selectList.length > 0) {
        fundInfos = this.selectList.map(item => {
          return {
            isPack: false,
            fundCodeTitle: item.VC_FUNDNAME || "",
            fundCodeKey: item.VC_FUNDCODE || "",
            funds: [{ fundCode: item.VC_FUNDCODE || "", dataSource: "" }]
          }
        })
      } else {
        fundInfos = [{
          isPack: false,
          fundCodeTitle: "测试产品-请替换为真实产品",
          fundCodeKey: "000000",
          funds: [{ fundCode: "000000", dataSource: "" }]
        }]
      }

      let reqBody = {
        fundInfos: fundInfos,
        beginDate: dateArr[0] || "",
        endDate: dateArr[1] || "",
        singleBenchmark: this.paramForm.ZB_INDEXTYPE === '1' ? (this.paramForm.ZB_INDEXCODEA || "") : "",
        dateType: "workDate",
        dateStep: this.paramForm.vcDataStep || "1",
        paramMap: {
          templateCode: this.rowData.vcStrategyId || "",
          beginDate: dateArr[0] || "",
          endDate: dateArr[1] || "",
          benchmarks: this.paramForm.ZB_INDEXTYPE || "1",
          benchmarkA: this.paramForm.ZB_INDEXCODEA || "",
          benchmarkB: this.paramForm.ZB_INDEXCODEB || "",
          benchmarkAValue: this.paramForm.ZB_INDEXWEIGHTA || "0.0000",
          benchmarkBValue: this.paramForm.ZB_INDEXWEIGHTB || "0.0000",
          kpiCode: "",
          contrasCode: Array.isArray(this.paramForm.contrasCode) ? this.paramForm.contrasCode.join(',') : (this.paramForm.contrasCode || ""),
          industryType: this.paramForm.industryType || "SWSR",
          desensitizationFlag: "",
          desensitizationFun: "ALL",
          dataFreqOpen: "true",
          dataFreq: this.paramForm.vcDataStep || "1"
        },
        colList: colList
      }

      let pythonDictStr = JSON.stringify(reqBody, null, 4)
      pythonDictStr = pythonDictStr.replace(/:\s*true/g, ': True')
        .replace(/:\s*false/g, ': False')
        .replace(/:\s*null/g, ': None')

      const commentMap = {
        '"fundInfos":': '产品信息列表',
        '"fundCodeTitle":': '产品名称',
        '"fundCodeKey":': '产品代码',
        '"beginDate":': '开始日期',
        '"endDate":': '结束日期',
        '"singleBenchmark":': '单基准代码',
        '"dateType":': '日期类型',
        '"dateStep":': '数据步长',
        '"paramMap":': '参数集合',
        '"templateCode":': '模板代码 -- 不填',
        '"benchmarks":': '基准类型：1-单基准，2-复合基准',
        '"benchmarkA":': '基准A代码',
        '"benchmarkB":': '基准B代码',
        '"benchmarkAValue":': '基准A比例',
        '"benchmarkBValue":': '基准B比例',
        '"contrasCode":': '对比基准代码集合',
        '"industryType":': '行业类型',
        '"dataFreq":': '数据频率',
        '"colList":': '指标表头配置列表',
        '"vcInfoDefineId":': '指标定义ID',
        '"vcColName":': '表头名称',
        '"fColOrder":': '列排序'
      }

      const dictLines = pythonDictStr.split('\n')
      pythonDictStr = dictLines.map((line, index) => {
        let trimmedLine = line.trim()
        let comment = ''
        for (let key in commentMap) {
          if (trimmedLine.startsWith(key) || trimmedLine.startsWith("'" + key.replace(/"/g, "") + "'")) {
            comment = ' # ' + commentMap[key]
            break
          }
        }
        if (index === 0) return line + comment
        return '        ' + line + comment
      }).join('\n')

      let host = window.location.origin
      if (process.env.BASE_API && !process.env.BASE_API.startsWith('http')) {
        host += process.env.BASE_API
      } else if (process.env.BASE_API) {
        host = process.env.BASE_API
      }

      let pythonTemplate = `import requests
import json
from typing import Dict, Any

class ApiCaller:
    
    @staticmethod
    def build_json_body() -> str:
        """构建请求的JSON Body"""
        json_body = &pythonDictStr
        return json.dumps(json_body, ensure_ascii=False)
    
    @staticmethod
    def send_post_request(url: str, token: str, json_body: str) -> str:
        """发送POST请求"""
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "token": token
        }
        
        try:
            # 发送POST请求
            response = requests.post(url, data=json_body.encode('utf-8'), headers=headers)
            
            # 获取响应码
            print(f"响应码: {response.status_code}")
            
            # 判断状态码
            if 200 <= response.status_code < 300:
                # 成功响应
                return response.text
            else:
                raise Exception(f"HTTP请求失败，状态码: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            # 尝试获取错误响应
            if hasattr(e, 'response') and e.response is not None:
                try:
                    return f"错误响应: {e.response.text}"
                except:
                    return f"请求失败: {str(e)}"
            return f"请求失败: {str(e)}"
    
    @staticmethod
    def main():
        # 用户TOKEN
        token = "替换用户TOKEN"
        
        # URL接口地址
        host = "&host"
        intf = "/api/browser/index_token"
        url = host + intf
        
        # 构建JSON Body
        json_body = ApiCaller.build_json_body()
        
        # 发送请求并获取响应
        response = ApiCaller.send_post_request(url, token, json_body)
        print(f"响应结果: {response}")


if __name__ == "__main__":
    ApiCaller.main()`

      return pythonTemplate.replace('&pythonDictStr', pythonDictStr).replace('&host', host)
    },
    generateCode() {
      if (!this.selectedIndexList || this.selectedIndexList.length === 0) {
        this.$message.warning('请至少选择一个指标')
        return
      }

      // 验证所有指标是否已配置参数
      for (let i = 0; i < this.selectedIndexList.length; i++) {
        const item = this.selectedIndexList[i]
        const itemClass = this.validationClass(item)
        if (itemClass === 'invalid') {
          this.$message({
            message: `请完善【${item.vcIndexName}】的参数配置！`,
            type: 'warning'
          })
          return
        }
      }

      const colList = this.getColList()
      this.generatedJavaCode = this.getGeneratedJavaCode(colList)
      this.generatedPythonCode = this.getGeneratedPythonCode(colList)
      this.codeDialogVisible = true
    },
    /**
     * list 数据转 tree
     */
    delDepartTree(_data, _id, _pId) {
      const data = _.cloneDeep(_data)
      const obj = {}
      const res = []
      const len = data.length
      const id = _id || 'id'
      const parentId = _pId || 'pId'
      const children = 'children'
      for (let i = 0; i < len; i++) {
        obj[data[i][id]] = data[i]
      }
      for (let j = 0; j < len; j++) {
        const list = data[j]
        const parentList = obj[list[parentId]]
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
  }
}
</script>

<style lang="scss">
.paramConfig-wrapper {
  .apiManager-paramConfigDialog {
    background: #f0f2f5 !important;
    width: 100% !important;

    .el-dialog__header {
      display: none;
    }

    .el-dialog__body {
      padding: 0;
      height: 100%;
      display: flex;
      flex-direction: column;
      max-height: none !important;
    }
  }
}
</style>

<style lang="scss" scoped>
.paramConfig-wrapper {
  .paramConfig-header {
    height: 56px;
    padding: 0 20px;
    background: #fff;
    display: flex;
    justify-content: space-between;
    align-items: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    z-index: 10;

    .template-name {
      font-size: 18px;
      font-weight: 600;
      color: #303133;
      margin-right: 20px;
      white-space: nowrap;
    }

    .header-left {
      display: flex;
      align-items: center;
      flex: 1;
      overflow: hidden;
    }

    .header-inline-form {
      display: flex;
      align-items: center;
      gap: 16px;

      .header-form-item {
        margin-bottom: 0 !important;
        display: flex;
        align-items: center;

        ::v-deep .el-form-item__label {
          padding: 0 8px 0 0;
          line-height: 32px;
          white-space: nowrap;
        }

        ::v-deep .el-form-item__content {
          line-height: 32px;
        }

        ::v-deep .el-form-item__error {
          padding-top: 0;
          top: 100%;
        }
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 8px;

      .close-btn {
        font-size: 20px;
        color: #909399;
        cursor: pointer;
        margin-left: 8px;
        padding: 4px;
        border-radius: 4px;
        transition: all 0.2s;

        &:hover {
          color: #f56c6c;
          background: #fef0f0;
        }
      }
    }
  }

  .paramConfig-top {
    margin: 12px 12px 0;

    ::v-deep .el-collapse-item__header {
      font-size: 15px;
      font-weight: 600;
      color: #333;
      padding-left: 16px;
      background-color: #fff;
      border-radius: 8px 8px 0 0;
    }

    ::v-deep .el-collapse-item__wrap {
      border-radius: 0 0 8px 8px;

      .el-collapse-item__content {
        padding-bottom: 10px;
      }
    }

    ::v-deep .el-collapse {
      border: none;
    }

    ::v-deep .el-form {
      padding: 10px 16px;
      background-color: #fff;
      border-radius: 0 0 8px 8px;
      width: 100% !important;
    }

    ::v-deep .el-form-item {
      margin-bottom: 10px;
    }
  }

  .paramConfig-main {
    flex: 1;
    display: flex;
    overflow: hidden;
    background: #f0f2f5;
    padding: 12px;
    gap: 5px;

    .main-left {
      background: #fff;
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);

      .section-title {
        height: 48px;
        padding: 0 16px;
        font-weight: 600;
        border-bottom: 1px solid #f0f0f0;
        color: #333;
        display: flex;
        justify-content: space-between;
        align-items: center;

        .title-text {
          font-size: 15px;
        }

        .tree-type-select {
          width: 140px;
        }
      }

      .search-box {
        padding: 12px;
      }

      .tree-container {
        flex: 1;
        overflow-y: auto;
        padding: 0 8px 12px;

        ::v-deep .el-tree-node__content:has(.parent-node) {
          .el-checkbox {
            display: none;
          }
        }

        .custom-tree-node {
          display: flex;
          align-items: center;
          gap: 6px;
          overflow: hidden;

          i {
            color: #909399;
          }

          .label-text {
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
          }
        }
      }
    }

    .resize-bar {
      width: 4px;
      cursor: col-resize;
      background: transparent;
      transition: background 0.3s;

      &:hover {
        background: #409eff;
      }
    }

    .main-right {
      flex: 1;
      background: #fff;
      border-radius: 8px;
      overflow-y: auto;
      padding: 20px;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);

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
        gap: 16px;

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

              ::v-deep .dim-checkbox-group {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;
                align-items: center;

                .el-checkbox {
                  margin-right: 0;
                  margin-left: 0;
                  border-radius: 6px;

                  &.is-bordered {
                    height: 32px;
                    line-height: 10px;
                    padding: 8px 12px;
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

              ::v-deep .dim-radio-group {
                display: flex;
                flex-wrap: wrap;
                gap: 8px;

                .el-radio {
                  margin-right: 0;
                  border-radius: 6px;

                  &.is-bordered {
                    height: 32px;
                    line-height: 10px;
                    padding: 8px 12px;
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
}
</style>
