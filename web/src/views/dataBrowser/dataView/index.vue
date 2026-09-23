<!--
 * @Description: 
 * @Author: 
 * @Date: 2025-11-03 13:49:06
 * @LastEditors: Please set LastEditors
 * @LastEditTime: 2026-01-14 16:43:49
-->
<template>
  <div class="dataBrowser-dataView">
    <!-- 搜索 -->
    <el-form :inline="true" ref="formQueryRef" :model="formQuery" :rules="formRules"
      class="standard-form">
      <el-row>
        <el-col :span="24">
          <el-form-item prop="vcTemplateId">
            <el-select v-model="formQuery.vcTemplateId" size="small" filterable clearable placeholder="请选择模板"
              @change="handleTemplateChange">
              <el-option v-for="item in templateOptions" :key="item.vcTemplateId" :label="item.vcTemplateName"
                :value="item.vcTemplateId">
                <span style="float: left">{{ item.vcTemplateName }}</span>
                <span style="float: right; color: #8492a6; font-size: 12px; padding-left: 10px;">{{
                  item.vcTemplateTypeStr }}</span>
              </el-option>
            </el-select>
          </el-form-item>
          <el-form-item prop="fundNames">
            <el-tooltip :content="formQuery.fundNames" :disabled="!formQuery.fundNames" placement="top-start"
              effect="light">
              <el-input v-model="formQuery.fundNames" placeholder="请选择产品" size="small" readonly
                @click.native="fundListDialogVisible = true"></el-input>
            </el-tooltip>
          </el-form-item>
          <el-form-item prop="dateRange">
            <el-date-picker v-model="formQuery.dateRange" size="small" type="daterange" range-separator="-"
              start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd"
              :picker-options="$fun.dateShortcut()"></el-date-picker>
          </el-form-item>
          <!-- <el-form-item prop="desensitizationFlag">
            <el-checkbox-group v-model="formQuery.desensitizationFlag" @change="handlecheckeddesensitizationChange">
              <el-checkbox label="脱敏" value="true"></el-checkbox>
            </el-checkbox-group>
          </el-form-item> -->
          <el-form-item v-show="showDesensitization" prop="desensitizationFun">
            <el-select v-model="formQuery.desensitizationFun" size="small">
              <el-option label="不显示名称、代码" value="ALL"></el-option>
              <el-option label="仅屏蔽部分字符" value="PAR"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="数据频率" prop="dataFreq">
            <el-select v-model="formQuery.dataFreq" placeholder="请选择数据频率" size="small" clearable filterable>
              <el-option v-for="item in userDataFreqOptionList" :key="item.dimCde" :label="item.dimNme"
                :value="item.dimCde"></el-option>
            </el-select>
          </el-form-item>

          <el-form-item class="">
            <el-button type="primary" size="small" :loading="tableLoading" @click="onQuery(true)" class="mb5"
              icon="el-icon-search">查询</el-button>
            <el-button type="info" size="small" plain icon="el-icon-refresh"
              @click="resetForm('formQueryRef')">重置</el-button>
            <el-button type="info" size="small" plain icon="el-icon-download" @click="exportExcelFile"
              :loading="exportLoading">导出</el-button>
            <el-button type="primary" size="small" @click="showMoreQuery">
              <span>{{ isShowMoreQuery ? '收起筛选' : '展开筛选' }}</span>
              <i :class="isShowMoreQuery ? 'el-icon-caret-top' : 'el-icon-caret-bottom'" />
            </el-button>
          </el-form-item>
          <el-form-item class="">
            <el-radio-group v-model="viewMode" size="small" style="margin-left: 10px;" class="radio-button-group">
              <el-radio-button label="data">表格</el-radio-button>
              <el-radio-button label="chart">图形</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
      <el-row v-show="isShowMoreQuery">
        <el-col :span="24">
          <div style="display: inline-block">
            <el-form-item label="基准类型">
              <el-select v-model="formQuery.ZB_INDEXTYPE" placeholder="请选择" size="small">
                <el-option v-for="item in ZB_INDEXTYPEOption" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </div>
          <div v-show="formQuery.ZB_INDEXTYPE == '1'" style="display: inline-block">
            <el-form-item label="选择基准">
              <el-select v-model="formQuery.ZB_INDEXCODEA" placeholder="请选择" size="small">
                <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </div>
          <div v-show="formQuery.ZB_INDEXTYPE == '2'" style="display: inline-block">
            <el-form-item label="基准 A">
              <el-select v-model="formQuery.ZB_INDEXCODEA" placeholder="请选择" size="small">
                <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="比例">
              <el-input v-model="formQuery.ZB_INDEXWEIGHTA" size="small" style="width: 85px !important"
                @blur="handleInputWeight('A')"></el-input>
              %
            </el-form-item>
          </div>
          <div v-show="formQuery.ZB_INDEXTYPE == '2'" style="display: inline-block">
            <el-form-item label="基准 B">
              <el-select v-model="formQuery.ZB_INDEXCODEB" placeholder="请选择" size="small">
                <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="比例">
              <el-input v-model="formQuery.ZB_INDEXWEIGHTB" size="small" style="width: 85px !important"
                @blur="handleInputWeight('B')"></el-input>
              %
            </el-form-item>
          </div>
          <div style="display: inline-block">
            <el-form-item label="对比基准">
              <el-select v-model="formQuery.contrasCode" clearable collapse-tags multiple placeholder="请选择" size="small"
                @change="changeContrasCode"
                :class="formQuery.contrasCode.length > 1 && 'custom-select-multiple-tags50'">
                <el-option v-for="item in $store.state.edims.datumOption" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </div>
          <div style="display: inline-block" v-if="currentTempType === 'A' || currentTempType === 'C'">
            <el-form-item label="行业类型">
              <el-select v-model="formQuery.industryType" disabled collapse-tags placeholder="请选择" size="small">
                <el-option v-for="item in industryTypeOptions" :key="item.id" :label="item.label"
                  :value="item.id"></el-option>
              </el-select>
            </el-form-item>
          </div>
          <el-form-item label="因子类型" prop="factorType" v-if="currentTempType === 'A' || currentTempType === 'C'">
            <template slot="label">因子类型
              <el-tooltip content="只作用于多因子报告类型" placement="top" effect="light">
                <i class="el-icon-info"></i>
              </el-tooltip>
            </template>
            <el-select v-model="formQuery.factorType" size="small" disabled filterable>
              <el-option v-for="item in factorTypeOptionList" :key="item.dimCde" :label="item.dimNme"
                :value="item.dimCde" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <!-- 表格 -->
    <div class="dataView-toolbar" v-show="viewMode === 'data' && currentTempType !== 'C'">
      <div class="dataView-toolbar-left">
        <el-tabs v-model="activeName" type="card" size="small" @tab-click="handleFundClick"
          v-if="showType === '1' && selectList.length > 0 && currentTempType !== 'C'" class="custom-card-tabs">
          <el-tab-pane :label="item.VC_FUNDNAME" :name="item.VC_FUNDCODE" v-for="item in selectList"
            :key="item.id"></el-tab-pane>
        </el-tabs>
      </div>
      <!-- <div class="dataView-toolbar-right" v-if="currentTempType !== 'C'">
        <el-divider direction="vertical"></el-divider>
        <el-radio-group v-model="showType" size="mini">
          <el-radio label="1">sheet展示</el-radio>
          <el-radio label="2">排列展示</el-radio>
        </el-radio-group>
      </div> -->
      <!-- <vxe-toolbar custom ref="xToolbar" class="dataView-xToolbar"></vxe-toolbar> -->
    </div>

    <!-- 数据视图 和 图形视图 容器 -->
    <div class="view-content" v-loading="tableLoading">
      <!-- 数据视图 -->
      <div v-show="viewMode === 'data'" class="table-view">
        <template v-if="['', 'A', 'B'].includes(currentTempType)">
          <vxe-grid ref="xGridTable" border stripe sync-resize resizable auto-resize show-overflow height="auto"
            :scroll-x="{ enabled: false }" :columns="tableColumn" :data="tableData">
            <!-- 空状态 -->
            <template slot="empty">
              <div class="empty-tip" style="height: 300px; line-height: 300px;">
                <span v-if="!formQuery.vcTemplateId">请选择模板</span>
                <span v-else>暂无数据</span>
              </div>
            </template>
          </vxe-grid>
        </template>
        <template v-else-if="currentTempType === 'C'">
          <vxe-grid ref="xGridTableC" border resizable auto-resize height="auto" :scroll-x="{ enabled: false }" :columns="tableColumnC"
            :data="tableDataC"></vxe-grid>
        </template>
        <template v-else-if="currentTempType === 'D'">
          <el-tabs v-model="activeTabD" type="card" class="custom-card-tabs custom-card-tabs-D">
            <el-tab-pane v-for="(columns, key) in tableColumnD" :key="key" :label="tabNamesD[key]" :name="key">
              <vxe-grid :ref="'xGridTableD_' + key" border stripe sync-resize resizable auto-resize show-overflow
                height="auto" :scroll-x="{ enabled: false }" :columns="columns" :data="tableDataD[key] || []">
                <!-- 空状态 -->
                <template slot="empty">
                  <div class="empty-tip" style="height: 300px; line-height: 300px;">
                    <span v-if="!formQuery.vcTemplateId">请选择模板</span>
                    <span v-else>暂无数据</span>
                  </div>
                </template>
              </vxe-grid>
            </el-tab-pane>
          </el-tabs>
        </template>
      </div>

      <!-- 图形视图 -->
      <div v-show="viewMode === 'chart'" class="chart-view-wrapper">
        <!-- 顶部工具栏 -->
        <div class="chart-toolbar">
          <div class="chart-toolbar-left">
            <!-- 图表标题 -->
            <div class="chart-title-edit">
              <i class="el-icon-edit-outline chart-title-icon"></i>
              <el-input v-model="chartStyle.title" placeholder="点击输入图表标题" size="small"
                class="chart-title-input"></el-input>
            </div>
            <el-divider direction="vertical"></el-divider>
            <!-- 图表类型快捷切换 -->
            <div class="chart-type-btns" v-if="currentTempType !== 'C' && currentTempType !== 'D'">
              <el-tooltip content="折线图" placement="bottom" :open-delay="300">
                <div class="chart-type-btn" :class="{ active: chartStyle.quickType === 'line' }"
                  @click="applyQuickType('line')">
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    <polyline points="3,17 8,11 13,14 21,5" fill="none" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </div>
              </el-tooltip>
              <el-tooltip content="柱状图" placement="bottom" :open-delay="300">
                <div class="chart-type-btn" :class="{ active: chartStyle.quickType === 'bar' }"
                  @click="applyQuickType('bar')">
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    <rect x="3" y="12" width="4" height="9" rx="1" fill="currentColor" opacity="0.7" />
                    <rect x="10" y="7" width="4" height="14" rx="1" fill="currentColor" opacity="0.85" />
                    <rect x="17" y="3" width="4" height="18" rx="1" fill="currentColor" />
                  </svg>
                </div>
              </el-tooltip>
              <el-tooltip content="面积图" placement="bottom" :open-delay="300">
                <div class="chart-type-btn" :class="{ active: chartStyle.quickType === 'area' }"
                  @click="applyQuickType('area')">
                  <svg viewBox="0 0 24 24" width="18" height="18">
                    <path d="M3,20 L3,15 L8,10 L13,13 L21,4 L21,20 Z" fill="currentColor" opacity="0.25" />
                    <polyline points="3,15 8,10 13,13 21,4" fill="none" stroke="currentColor" stroke-width="2"
                      stroke-linecap="round" stroke-linejoin="round" />
                  </svg>
                </div>
              </el-tooltip>
            </div>
            <!-- C类型固定柱状图标识 -->
            <div class="chart-type-btns" v-if="currentTempType === 'C'">
              <div class="chart-type-btn active">
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <rect x="3" y="12" width="4" height="9" rx="1" fill="currentColor" opacity="0.7" />
                  <rect x="10" y="7" width="4" height="14" rx="1" fill="currentColor" opacity="0.85" />
                  <rect x="17" y="3" width="4" height="18" rx="1" fill="currentColor" />
                </svg>
              </div>
              <span style="font-size: 12px; color: #909399; margin-left: 6px;">柱状图（组合对比）</span>
            </div>
            <!-- D类型固定柱状图（横向）标识 -->
            <div class="chart-type-btns" v-if="currentTempType === 'D'">
              <div class="chart-type-btn active">
                <svg viewBox="0 0 24 24" width="18" height="18">
                  <rect x="3" y="12" width="18" height="4" rx="1" fill="currentColor" opacity="0.7" />
                  <rect x="3" y="6" width="12" height="4" rx="1" fill="currentColor" opacity="0.85" />
                  <rect x="3" y="18" width="15" height="4" rx="1" fill="currentColor" />
                </svg>
              </div>
              <span style="font-size: 12px; color: #909399; margin-left: 6px;">柱状图（标的数值）</span>
            </div>
          </div>
          <div class="chart-toolbar-right">
            <!-- 颜色主题 -->
            <el-dropdown trigger="click" @command="applyColorTheme" size="small">
              <el-button size="small" class="toolbar-action-btn">
                <span class="color-theme-dots">
                  <span v-for="(c, i) in colorThemes[chartStyle.colorTheme].colors.slice(0, 4)" :key="i"
                    class="color-dot" :style="{ background: c }"></span>
                </span>
                <span style="margin-left: 6px;">配色</span>
              </el-button>
              <el-dropdown-menu slot="dropdown" class="color-theme-dropdown">
                <el-dropdown-item v-for="(theme, key) in colorThemes" :key="key" :command="key">
                  <div class="color-theme-item" :class="{ active: chartStyle.colorTheme === key }">
                    <span class="color-theme-dots">
                      <span v-for="(c, i) in theme.colors.slice(0, 6)" :key="i" class="color-dot-lg"
                        :style="{ background: c }"></span>
                    </span>
                    <span class="color-theme-name">{{ theme.name }}</span>
                  </div>
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
            <el-divider direction="vertical"></el-divider>
            <!-- 显示选项 -->
            <el-tooltip content="数据标签" placement="bottom" :open-delay="300">
              <div class="toolbar-toggle-btn" :class="{ active: chartStyle.showDataLabel }"
                @click="chartStyle.showDataLabel = !chartStyle.showDataLabel; drawChart()">
                <i class="el-icon-price-tag"></i>
              </div>
            </el-tooltip>
            <el-tooltip content="平滑曲线" placement="bottom" :open-delay="300"
              v-if="currentTempType !== 'C' && currentTempType !== 'D'">
              <div class="toolbar-toggle-btn" :class="{ active: chartStyle.smooth }"
                @click="chartStyle.smooth = !chartStyle.smooth; drawChart()">
                <svg viewBox="0 0 20 20" width="16" height="16">
                  <path d="M2,15 C6,15 6,5 10,5 C14,5 14,12 18,12" fill="none" stroke="currentColor" stroke-width="2"
                    stroke-linecap="round" />
                </svg>
              </div>
            </el-tooltip>
            <el-tooltip content="网格线" placement="bottom" :open-delay="300">
              <div class="toolbar-toggle-btn" :class="{ active: chartStyle.showGrid }"
                @click="chartStyle.showGrid = !chartStyle.showGrid; drawChart()">
                <i class="el-icon-s-grid"></i>
              </div>
            </el-tooltip>
            <el-divider direction="vertical"></el-divider>
            <el-tooltip content="下载图片" placement="bottom" :open-delay="300">
              <div class="toolbar-toggle-btn" @click="exportChartImage">
                <i class="el-icon-download"></i>
              </div>
            </el-tooltip>
          </div>
        </div>

        <!-- 图表主体区域 -->
        <div class="chart-main-area">
          <!-- 图表展示区 -->
          <div class="chart-canvas-area">
            <div class="chart-canvas-inner" ref="chartCanvasRef">
              <Echarts v-if="viewMode === 'chart'" id="dataViewChart" :options="chartOption" resizeDom="dataViewChart"
                style="width: 100%; height: 100%;" />
            </div>
          </div>

          <!-- 拖拽条 -->
          <div class="resize-bar" :class="{ dragging: isDragging }" @mousedown="initDrag">
            <div class="resize-bar-line"></div>
          </div>

          <!-- 右侧配置栏 -->
          <div class="chart-config-sidebar" :style="{ width: sidebarWidth + 'px' }">
            <div class="sidebar-inner">

              <!-- ===== A/B类型配置 ===== -->
              <template v-if="['A', 'B'].includes(currentTempType) || !currentTempType">
                <el-tabs v-model="chartConfigTab" size="small" @tab-click="drawChart" class="config-tabs">
                  <el-tab-pane label="产品维度" name="product">
                    <div class="config-panel">
                      <div class="config-panel-header" @click="togglePanel('productData')">
                        <span><i class="el-icon-data-analysis"></i> 数据选择</span>
                        <i :class="expandedPanels.productData ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.productData" class="config-panel-body">
                          <el-form label-position="top" size="mini">
                            <el-form-item label="选择产品" class="compact-form-item">
                              <el-select v-model="chartConfigProduct.product" placeholder="请选择单产品" style="width: 100%">
                                <el-option v-for="item in selectList" :key="item.VC_FUNDCODE" :label="item.VC_FUNDNAME"
                                  :value="item.VC_FUNDCODE"></el-option>
                              </el-select>
                            </el-form-item>
                            <el-form-item label="选择指标" class="compact-form-item">
                              <MySelectMultiple v-model="chartConfigProduct.indicators" :options="PRODUCT_EDIT_COL_LIST"
                                :optionsProps="{ value: 'vcColCode', label: 'vcColName' }" placeholder="请选择"
                                size="small" style="width: 100%"></MySelectMultiple>
                            </el-form-item>
                          </el-form>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <div class="config-panel" v-if="chartConfigProduct.indicators.length > 0">
                      <div class="config-panel-header" @click="togglePanel('productSeries')">
                        <span><i class="el-icon-set-up"></i> 序列配置</span>
                        <i :class="expandedPanels.productSeries ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.productSeries" class="config-panel-body">
                          <div v-for="(ind, idx) in chartConfigProduct.indicators" :key="ind" class="series-config-row">
                            <div class="series-color-dot" :style="{ background: getSeriesColor(idx) }"></div>
                            <div class="series-name" :title="getIndicatorName(ind)">{{ getIndicatorName(ind) }}</div>
                            <el-select v-model="chartConfigProduct.seriesConfig[ind].type" style="width: 90px;"
                              size="mini" placeholder="类型">
                              <el-option label="折线图" value="line"></el-option>
                              <el-option label="柱状图" value="bar"></el-option>
                              <el-option label="面积图" value="area"></el-option>
                              <el-option label="堆叠折线" value="stackLine"></el-option>
                              <el-option label="堆叠柱状" value="stackBar"></el-option>
                              <el-option label="堆叠面积" value="stackArea"></el-option>
                            </el-select>
                            <el-select v-model="chartConfigProduct.seriesConfig[ind].yAxis" style="width: 68px;"
                              size="mini" placeholder="轴">
                              <el-option label="左轴" :value="0"></el-option>
                              <el-option label="右轴" :value="1"></el-option>
                            </el-select>
                          </div>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <div class="config-panel">
                      <div class="config-panel-header" @click="togglePanel('productAxis')">
                        <span><i class="el-icon-rank"></i> 坐标轴</span>
                        <i :class="expandedPanels.productAxis ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.productAxis" class="config-panel-body">
                          <el-form size="mini" :inline="true">
                            <el-form-item label="左Y轴" class="compact-form-item" style="margin-bottom: 8px;">
                              <el-input v-model="chartConfigProduct.leftYUnit" placeholder="名称" style="width: 100px;"
                                @change="drawChart"></el-input>
                            </el-form-item>
                            <el-form-item label="右Y轴" class="compact-form-item" style="margin-bottom: 8px;">
                              <el-input v-model="chartConfigProduct.rightYUnit" placeholder="名称" style="width: 100px;"
                                @change="drawChart"></el-input>
                            </el-form-item>
                          </el-form>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <el-button type="primary" size="small" icon="el-icon-refresh" class="refresh-chart-btn"
                      @click="drawChart">刷新图形</el-button>
                  </el-tab-pane>
                  <el-tab-pane label="指标维度" name="index">
                    <div class="config-panel">
                      <div class="config-panel-header" @click="togglePanel('indexData')">
                        <span><i class="el-icon-data-analysis"></i> 数据选择</span>
                        <i :class="expandedPanels.indexData ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.indexData" class="config-panel-body">
                          <el-form label-position="top" size="mini">
                            <el-form-item label="选择指标" class="compact-form-item">
                              <el-select v-model="chartConfigIndex.indicator" placeholder="请选择单指标" style="width: 100%">
                                <el-option v-for="col in EDIT_COL_LIST" :key="col.vcColCode" :label="col.vcColName"
                                  :value="col.vcColCode"></el-option>
                              </el-select>
                            </el-form-item>
                            <el-form-item label="选择产品" class="compact-form-item">
                              <MySelectMultiple v-model="chartConfigIndex.products" :options="selectList"
                                :optionsProps="{ value: 'VC_FUNDCODE', label: 'VC_FUNDNAME' }" placeholder="请选择"
                                size="small" style="width: 100%"></MySelectMultiple>
                            </el-form-item>
                          </el-form>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <div class="config-panel" v-if="chartConfigIndex.products.length > 0">
                      <div class="config-panel-header" @click="togglePanel('indexSeries')">
                        <span><i class="el-icon-set-up"></i> 序列配置</span>
                        <i :class="expandedPanels.indexSeries ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.indexSeries" class="config-panel-body">
                          <div v-for="(prod, idx) in chartConfigIndex.products" :key="prod" class="series-config-row">
                            <div class="series-color-dot" :style="{ background: getSeriesColor(idx) }"></div>
                            <div class="series-name" :title="getProductName(prod)">{{ getProductName(prod) }}</div>
                            <el-select v-model="chartConfigIndex.seriesConfig[prod].type" style="width: 90px;"
                              size="mini" placeholder="类型">
                              <el-option label="折线图" value="line"></el-option>
                              <el-option label="柱状图" value="bar"></el-option>
                              <el-option label="面积图" value="area"></el-option>
                              <el-option label="堆叠折线" value="stackLine"></el-option>
                              <el-option label="堆叠柱状" value="stackBar"></el-option>
                              <el-option label="堆叠面积" value="stackArea"></el-option>
                            </el-select>
                            <el-select v-model="chartConfigIndex.seriesConfig[prod].yAxis" style="width: 68px;"
                              size="mini" placeholder="轴">
                              <el-option label="左轴" :value="0"></el-option>
                              <el-option label="右轴" :value="1"></el-option>
                            </el-select>
                          </div>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <div class="config-panel">
                      <div class="config-panel-header" @click="togglePanel('indexAxis')">
                        <span><i class="el-icon-rank"></i> 坐标轴</span>
                        <i :class="expandedPanels.indexAxis ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                      </div>
                      <el-collapse-transition>
                        <div v-show="expandedPanels.indexAxis" class="config-panel-body">
                          <el-form size="mini" :inline="true">
                            <el-form-item label="左Y轴" class="compact-form-item" style="margin-bottom: 8px;">
                              <el-input v-model="chartConfigIndex.leftYUnit" placeholder="名称" style="width: 100px;"
                                @change="drawChart"></el-input>
                            </el-form-item>
                            <el-form-item label="右Y轴" class="compact-form-item" style="margin-bottom: 8px;">
                              <el-input v-model="chartConfigIndex.rightYUnit" placeholder="名称" style="width: 100px;"
                                @change="drawChart"></el-input>
                            </el-form-item>
                          </el-form>
                        </div>
                      </el-collapse-transition>
                    </div>
                    <el-button type="primary" size="small" icon="el-icon-refresh" class="refresh-chart-btn"
                      @click="drawChart">刷新图形</el-button>
                  </el-tab-pane>
                </el-tabs>
              </template>

              <!-- ===== C类型配置（组合对比） ===== -->
              <template v-else-if="currentTempType === 'C'">
                <div class="config-section-title">组合对比图配置</div>
                <div class="config-panel">
                  <div class="config-panel-header" @click="togglePanel('cData')">
                    <span><i class="el-icon-data-analysis"></i> 数据选择</span>
                    <i :class="expandedPanels.cData ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  </div>
                  <el-collapse-transition>
                    <div v-show="expandedPanels.cData" class="config-panel-body">
                      <el-form label-position="top" size="mini">
                        <el-form-item label="选择组合（多选）" class="compact-form-item">
                          <MySelectMultiple v-model="chartConfigC.products" :options="selectList"
                            :optionsProps="{ value: 'VC_FUNDCODE', label: 'VC_FUNDNAME' }" placeholder="请选择"
                            size="small" style="width: 100%"></MySelectMultiple>
                        </el-form-item>
                        <el-form-item label="选择指标（多选）" class="compact-form-item">
                          <MySelectMultiple v-model="chartConfigC.indicators" :options="C_EDIT_COL_LIST"
                            :optionsProps="{ value: 'vcColCode', label: 'vcColName' }" placeholder="请选择" size="small"
                            style="width: 100%"></MySelectMultiple>
                        </el-form-item>
                      </el-form>
                    </div>
                  </el-collapse-transition>
                </div>
                <div class="config-panel">
                  <div class="config-panel-header" @click="togglePanel('cAxis')">
                    <span><i class="el-icon-rank"></i> Y轴配置</span>
                    <i :class="expandedPanels.cAxis ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  </div>
                  <el-collapse-transition>
                    <div v-show="expandedPanels.cAxis" class="config-panel-body">
                      <el-form size="mini">
                        <el-form-item label="Y轴名称" class="compact-form-item">
                          <el-input v-model="chartConfigC.yAxisName" placeholder="名称" style="width: 100%;"
                            @change="drawChart"></el-input>
                        </el-form-item>
                      </el-form>
                    </div>
                  </el-collapse-transition>
                </div>
                <el-button type="primary" size="small" icon="el-icon-refresh" class="refresh-chart-btn"
                  @click="drawChart">刷新图形</el-button>
              </template>

              <!-- ===== D类型配置（个券模板） ===== -->
              <!-- ===== D类型配置（个券模板） ===== -->
              <template v-else-if="currentTempType === 'D'">
                <div class="config-section-title">个券指标图配置</div>
                <div class="config-panel">
                  <div class="config-panel-header" @click="togglePanel('dData')">
                    <span><i class="el-icon-data-analysis"></i> 数据选择</span>
                    <i :class="expandedPanels.dData ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  </div>
                  <el-collapse-transition>
                    <div v-show="expandedPanels.dData" class="config-panel-body">
                      <el-form label-position="top" size="mini">
                        <el-form-item label="选择组合" class="compact-form-item">
                          <el-select v-model="chartConfigD.product" placeholder="请选择单产品" style="width: 100%"
                            @change="drawChart">
                            <el-option v-for="item in selectList" :key="item.VC_FUNDCODE" :label="item.VC_FUNDNAME"
                              :value="item.VC_FUNDCODE"></el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item label="选择类型" class="compact-form-item">
                          <el-select v-model="chartConfigD.typeCode" placeholder="请选择类型" style="width: 100%"
                            @change="handleDTypeChange">
                            <el-option v-for="(name, code) in tabNamesD" :key="code" :label="name"
                              :value="code"></el-option>
                          </el-select>
                        </el-form-item>
                        <el-form-item label="选择指标" class="compact-form-item">
                          <el-select v-model="chartConfigD.indicator" placeholder="请选择单指标" style="width: 100%"
                            @change="drawChart">
                            <el-option v-for="col in availableDIndicators" :key="col.field" :label="col.title"
                              :value="col.field"></el-option>
                          </el-select>
                        </el-form-item>
                      </el-form>
                    </div>
                  </el-collapse-transition>
                </div>
                <div class="config-panel">
                  <div class="config-panel-header" @click="togglePanel('dAxis')">
                    <span><i class="el-icon-rank"></i> X轴配置</span>
                    <i :class="expandedPanels.dAxis ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
                  </div>
                  <el-collapse-transition>
                    <div v-show="expandedPanels.dAxis" class="config-panel-body">
                      <el-form size="mini">
                        <el-form-item label="X轴名称" class="compact-form-item">
                          <el-input v-model="chartConfigD.xAxisName" placeholder="名称" style="width: 100%;"
                            @change="drawChart"></el-input>
                        </el-form-item>
                      </el-form>
                    </div>
                  </el-collapse-transition>
                </div>
                <el-button type="primary" size="small" icon="el-icon-refresh" class="refresh-chart-btn"
                  @click="drawChart">刷新图形</el-button>
              </template>

            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 产品列表弹窗 -->
    <product-selector v-if="fundListDialogVisible" :multiple="true" :leftList="false"
      :dialog-visible="fundListDialogVisible" :tree-data="treeData" :show-tree-key-array="showTreeKeyArray"
      :select-list="selectList" default-checked-keys="wdgz" @closedialog="fundListDialogVisible = false"
      @submitdialog="handleFundListSubmit"></product-selector>
  </div>
</template>

<script>
import productSelector from '@/components/productSelector'
import Echarts from '@/components/Echarts'
import MySelectMultiple from '../components/MySelectMultiple.vue'
import SelectTable from '@/components/SelectTable'
import * as echartsLib from 'echarts'
import pageApi from './api.js'
import tempPageApi from '../tempManage/api.js'
import CONSTANTS from '../constants.js'
import commonApi from '@/api/common.js'
import { downLoadFileByUrlPost } from '@/utils'

export default {
  name: 'DataView',
  components: {
    productSelector,
    Echarts,
    MySelectMultiple,
    SelectTable
  },
  data() {
    return {
      currentTemplateIndexList: [],
      sidebarWidth: 320,
      isDragging: false,
      startX: 0,
      startWidth: 0,
      viewMode: 'data',
      chartOption: {},
      chartConfigTab: 'product',
      // 图表样式配置（PPT风格）
      chartStyle: {
        title: '',
        quickType: 'line',
        colorTheme: 'default',
        showDataLabel: false,
        smooth: true,
        showGrid: true
      },
      // 颜色主题预设
      colorThemes: {
        'default': {
          name: '经典蓝',
          colors: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4']
        },
        'business': {
          name: '商务灰',
          colors: ['#2c3e50', '#3498db', '#1abc9c', '#f39c12', '#e74c3c', '#9b59b6', '#34495e', '#16a085']
        },
        'fresh': {
          name: '清新绿',
          colors: ['#26a69a', '#66bb6a', '#42a5f5', '#ffa726', '#ef5350', '#ab47bc', '#8d6e63', '#78909c']
        },
        'warm': {
          name: '暖色调',
          colors: ['#e57373', '#ff8a65', '#ffb74d', '#fff176', '#aed581', '#4db6ac', '#4dd0e1', '#7986cb']
        },
        'dark': {
          name: '深色调',
          colors: ['#00bcd4', '#4caf50', '#ff9800', '#e91e63', '#9c27b0', '#3f51b5', '#009688', '#ff5722']
        },
        'elegant': {
          name: '优雅紫',
          colors: ['#7b68ee', '#6a5acd', '#9370db', '#ba55d3', '#da70d6', '#dda0dd', '#e6e6fa', '#8a2be2']
        }
      },
      // 可折叠面板展开状态
      expandedPanels: {
        productData: true,
        productSeries: true,
        productAxis: false,
        indexData: true,
        indexSeries: true,
        indexAxis: false,
        cData: true,
        cAxis: false,
        dData: true,
        dAxis: false
      },
      chartConfigProduct: {
        product: '',
        indicators: [],
        seriesConfig: {},
        leftYUnit: '',
        rightYUnit: ''
      },
      chartConfigIndex: {
        indicator: '',
        products: [],
        seriesConfig: {},
        leftYUnit: '',
        rightYUnit: ''
      },
      chartConfigC: {
        products: [],
        indicators: [],
        yAxisName: ''
      },
      chartConfigD: {
        product: '',
        typeCode: '',
        indicator: '',
        xAxisName: ''
      },
      templateColumns: [
        { prop: 'vcTemplateName', label: '模板名称', width: '220' },
        { prop: 'vcTemplateTypeStr', label: '模板类型', width: '150' }
      ],
      isShowMoreQuery: false,
      showDesensitization: false,
      formQuery: {
        vcTemplateId: '',
        dateRange: [],
        fundNames: '',
        dataFreq: '1',
        desensitizationFlag: '',
        desensitizationFun: 'ALL',
        ZB_INDEXTYPE: '1',
        ZB_INDEXCODEA: '000300',
        ZB_INDEXWEIGHTA: '0.0000',
        ZB_INDEXCODEB: '000300',
        ZB_INDEXWEIGHTB: '0.0000',
        contrasCode: [],
        industryType: 'SWSR',
        factorType: ''
      },
      formRules: {
        vcTemplateId: [{ required: true, message: '请选择模板', trigger: 'change' }],
        dateRange: [{ required: true, message: '请选择时间区间', trigger: 'change' }],
        fundNames: [{ required: true, message: '请选择产品', trigger: 'change' }],
        dataFreq: [{ required: true, message: '请选择数据频率', trigger: 'change' }],
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
        { dimCde: "CNE5", dimNme: "CNE5" },
        { dimCde: "CNE6", dimNme: "CNE6" }
      ],
      dataFreqOptionList: [],
      userDataFreqOptionList: [],
      exportLoading: false,
      showType: '1',
      dataObj: {},
      tableLoading: false,
      currentTempType: '',
      tableData: [],
      tableColumn: [],
      tableColumnC: [],
      tableDataC: [],
      tableColumnD: {},
      tableDataD: {},
      tabNamesD: {},
      activeTabD: '',
      dataFrequencyOptions: CONSTANTS.DATAFREQUENCY,
      tempTypeOptions: CONSTANTS.TEMPTYPE,
      templateOptions: [],
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
      selectList: [],
      selectListTemp: [],
      activeName: ''
    }
  },
  created() {
    const jumpToTemplateInfo = sessionStorage.getItem('dataView_jumpToTemplateInfo');
    if (jumpToTemplateInfo) {
      sessionStorage.removeItem('dataView_jumpToTemplateInfo');
      const { vcTemplateId, vcTemplateType, moreParams = {} } = JSON.parse(jumpToTemplateInfo);
      this.formQuery.vcTemplateId = vcTemplateId;
      this.handleTemplateChange(vcTemplateId, vcTemplateType, moreParams);
    }
    this.getTemplateList()
    this.getDataFreqOptions('DATAFREQ')
  },
  activated() {
    const jumpToTemplateInfo = sessionStorage.getItem('dataView_jumpToTemplateInfo');
    if (jumpToTemplateInfo) {
      sessionStorage.removeItem('dataView_jumpToTemplateInfo');
      const { vcTemplateId, vcTemplateType, moreParams = {} } = JSON.parse(jumpToTemplateInfo);
      this.formQuery.vcTemplateId = vcTemplateId;
      this.handleTemplateChange(vcTemplateId, vcTemplateType, moreParams);
    }
    this.getTemplateList()
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.xGridTable && this.$refs.xToolbar) {
        this.$refs.xGridTable.connect(this.$refs.xToolbar)
      }
    })
  },
  computed: {
    // 过滤后的指标列表，排除固定列，供图表配置选择器使用 (取所有选中的产品的列信息的并集)
    EDIT_COL_LIST() {
      if (!this.dataObj || Object.keys(this.dataObj).length === 0) {
        return this.currentTemplateIndexList;
      }
      let allAllowedCols = new Set();
      let hasColumnInfo = false;
      this.selectList.forEach(fund => {
        const columnKey = fund.VC_FUNDCODE + '_column';
        const allowedCols = this.dataObj[columnKey];
        if (Array.isArray(allowedCols)) {
          hasColumnInfo = true;
          allowedCols.forEach(col => allAllowedCols.add(col));
        }
      });
      if (hasColumnInfo) {
        return this.currentTemplateIndexList.filter(item => allAllowedCols.has(item.vcColCode));
      }
      return this.currentTemplateIndexList;
    },
    // 根据当前图表配置的单产品，过滤出对应产品的指标列表
    PRODUCT_EDIT_COL_LIST() {
      if (!this.chartConfigProduct.product || !this.dataObj || Object.keys(this.dataObj).length === 0) {
        return this.currentTemplateIndexList;
      }
      const columnKey = this.chartConfigProduct.product + '_column';
      const allowedCols = this.dataObj[columnKey];
      if (Array.isArray(allowedCols) && allowedCols.length > 0) {
        return this.currentTemplateIndexList.filter(item => allowedCols.includes(item.vcColCode));
      }
      return this.currentTemplateIndexList;
    },
    // C类型（组合对比）专用的图表指标选择下拉列表
    C_EDIT_COL_LIST() {
      if (this.currentTempType !== 'C' || !this.tableDataC || this.tableDataC.length === 0) {
        return this.currentTemplateIndexList;
      }
      // tableDataC 在查询后已经过滤掉了无数据的指标
      return this.tableDataC.map(row => ({
        vcColCode: row.indexCode,
        vcColName: row.indexName
      }));
    },
    availableDIndicators() {
      if (!this.chartConfigD.typeCode) return [];
      
      let allowedCols = null;
      if (this.chartConfigD.product && this.dataObj && Object.keys(this.dataObj).length > 0) {
        const columnKey = this.chartConfigD.product + '_column';
        allowedCols = this.dataObj[columnKey];
      }

      let cols = this.currentTemplateIndexList.filter(item => {
        const typeMatch = (item.vcTypeCode || 'default') === this.chartConfigD.typeCode;
        if (!typeMatch) return false;
        if (Array.isArray(allowedCols) && allowedCols.length > 0) {
          return allowedCols.includes(item.vcColCode);
        }
        return true;
      });

      return cols.map(item => ({
        field: item.vcColCode,
        title: item.vcColName
      }));
    }
  },
  watch: {
    showType() {
      if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
        this.updateTableABDisplay()
      } else if (this.currentTempType === 'D') {
        this.updateTableDDisplay()
        this.updateTableDDisplayData()
      }
    },
    viewMode(val) {
      if (val === 'chart') {
        this.$nextTick(() => {
          this.drawChart()
        })
      }
    },
    'chartConfigProduct.indicators': {
      handler(newVal) {
        newVal.forEach(ind => {
          if (!this.chartConfigProduct.seriesConfig[ind]) {
            this.$set(this.chartConfigProduct.seriesConfig, ind, { type: 'line', yAxis: 0 });
          }
        });
        this.drawChart();
      },
      deep: true
    },
    'chartConfigIndex.products': {
      handler(newVal) {
        newVal.forEach(prod => {
          if (!this.chartConfigIndex.seriesConfig[prod]) {
            this.$set(this.chartConfigIndex.seriesConfig, prod, { type: 'line', yAxis: 0 });
          }
        });
        this.drawChart();
      },
      deep: true
    },
    'chartConfigProduct.seriesConfig': {
      deep: true,
      handler() { this.drawChart(); }
    },
    'chartConfigIndex.seriesConfig': {
      deep: true,
      handler() { this.drawChart(); }
    },

  },
  methods: {
    // 获取模板数据
    getTemplateList() {
      const params = {
        pageNum: 1,
        pageSize: 10000
      }
      return tempPageApi.getTempList(params).then(res => {
        const { status, data } = res.data
        if (status === 200) {
          const list = data.list || []
          this.templateOptions = list.map(item => {
            const typeItem = this.tempTypeOptions.find(t => t.dimCde === item.vcTemplateType)
            return {
              ...item,
              vcTemplateTypeStr: typeItem ? typeItem.dimNme : item.vcTemplateType
            }
          })

          // 优化：切换菜单（keep-alive激活时），检查当前选中的模板是否有效或已被修改
          if (this.formQuery.vcTemplateId) {
            const exists = this.templateOptions.find(item => item.vcTemplateId === this.formQuery.vcTemplateId)
            console.log("existsexistsexistsexistsexistsexistsexistsexists", exists);
            
            if (!exists) {
              // 模板已被删除，重置当前选项以及表格和图表区域内容
              this.formQuery.vcTemplateId = ''
              this.currentTempType = ''
              this.currentTemplateIndexList = []
              this.tableData = []
              this.tableColumn = []
              this.tableColumnC = []
              this.tableDataC = []
              this.tableColumnD = {}
              this.tableDataD = {}
              this.tabNamesD = {}
              this.activeTabD = ''
              this.dataObj = {}
              this.resetChartView()
            }
          }
        }
      })
    },
    handleDTypeChange() {
      this.chartConfigD.indicator = ''
      if (this.availableDIndicators.length > 0) {
        this.chartConfigD.indicator = this.availableDIndicators[0].field
      }
      this.drawChart()
    },
    togglePanel(name) {
      this.expandedPanels[name] = !this.expandedPanels[name]
    },
    getSeriesColor(index) {
      const colors = this.colorThemes[this.chartStyle.colorTheme].colors
      return colors[index % colors.length]
    },
    applyQuickType(type) {
      this.chartStyle.quickType = type
      // 图表类型映射
      const typeMap = {
        'line': 'line',
        'bar': 'bar',
        'area': 'area'
      }
      const applyToConfig = (configObj, key, index) => {
        if (!configObj[key]) return
        if (type === 'area') {
          this.$set(configObj[key], 'type', 'area')
        } else {
          this.$set(configObj[key], 'type', type)
        }
      }
      if (this.chartConfigTab === 'product') {
        this.chartConfigProduct.indicators.forEach((ind, idx) => applyToConfig(this.chartConfigProduct.seriesConfig, ind, idx))
      } else {
        this.chartConfigIndex.products.forEach((prod, idx) => applyToConfig(this.chartConfigIndex.seriesConfig, prod, idx))
      }
      this.drawChart()
    },
    applyColorTheme(theme) {
      this.chartStyle.colorTheme = theme
      this.drawChart()
    },
    exportChartImage() {
      const chartEl = document.getElementById('dataViewChart')
      if (!chartEl) return
      const instance = echartsLib.getInstanceByDom(chartEl)
      if (!instance) return
      const url = instance.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#fff' })
      const a = document.createElement('a')
      a.href = url
      a.download = (this.chartStyle.title || '图表') + '.png'
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      this.$message.success('图片已下载')
    },
    resetChartView() {
      this.viewMode = 'data'
      this.chartOption = {}
      this.chartStyle.quickType = 'line'
      this.chartConfigProduct = {
        product: '',
        indicators: [],
        seriesConfig: {},
        leftYUnit: '',
        rightYUnit: ''
      }
      this.chartConfigIndex = {
        indicator: '',
        products: [],
        seriesConfig: {},
        leftYUnit: '',
        rightYUnit: ''
      }
      this.chartConfigC = {
        products: [],
        indicators: [],
        yAxisName: ''
      }
      this.chartConfigD = {
        product: this.selectList.length > 0 ? this.selectList[0].VC_FUNDCODE : '',
        typeCode: '',
        indicator: '',
        xAxisName: ''
      }
    },
    getProductName(code) {
      const fund = this.selectList.find(item => item.VC_FUNDCODE === code)
      return fund ? fund.VC_FUNDNAME : code
    },
    getIndicatorName(code) {
      const col = this.currentTemplateIndexList.find(item => item.vcColCode === code)
      return col ? col.vcColName : code
    },
    drawChart() {
      let xAxisData = []
      let seriesData = []
      const themeColors = this.colorThemes[this.chartStyle.colorTheme].colors
      const isArea = this.chartStyle.quickType === 'area'

      if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
        const times = new Set()
        Object.values(this.dataObj).forEach(fundData => {
          if (Array.isArray(fundData)) {
            fundData.forEach(row => {
              if (row && row.TDATE) times.add(row.TDATE)
            })
          }
        })
        xAxisData = Array.from(times).sort()

        if (this.chartConfigTab === 'product') {
          const currentProd = this.chartConfigProduct.product;
          const selectedInds = this.chartConfigProduct.indicators || [];
          if (currentProd && selectedInds.length > 0) {
            const fundData = this.dataObj[currentProd] || [];
            selectedInds.forEach((ind, idx) => {
              const config = this.chartConfigProduct.seriesConfig[ind] || { type: 'line', yAxis: 0 };
              const data = xAxisData.map(time => {
                const row = fundData.find(r => r.TDATE === time);
                return row ? (parseFloat(String(row[ind] || '0').replace(/%/g, '').replace(/,/g, '')) || 0) : 0;
              });
              const realType = (config.type === 'area' || config.type === 'stackLine' || config.type === 'stackArea') ? 'line'
                : config.type === 'stackBar' ? 'bar' : config.type;
              const seriesItem = {
                name: this.getIndicatorName(ind),
                type: realType,
                yAxisIndex: config.yAxis,
                smooth: this.chartStyle.smooth,
                data: data,
                itemStyle: { color: themeColors[idx % themeColors.length] },
                lineStyle: { width: 2.5 }
              };
              if (config.type === 'area' || (isArea && config.type === 'line')) {
                seriesItem.areaStyle = { opacity: 0.15 }
              }
              if (config.type === 'stackLine' || config.type === 'stackBar' || config.type === 'stackArea') {
                seriesItem.stack = 'total'
                if (config.type === 'stackLine') seriesItem.areaStyle = { opacity: 0.08 }
                if (config.type === 'stackArea') seriesItem.areaStyle = { opacity: 0.25 }
              }
              if (this.chartStyle.showDataLabel) {
                seriesItem.label = { show: true, position: 'top', fontSize: 10, color: '#666' }
              }
              seriesData.push(seriesItem);
            });
          }
        } else if (this.chartConfigTab === 'index') {
          const currentInd = this.chartConfigIndex.indicator;
          const selectedProds = this.chartConfigIndex.products || [];
          if (currentInd && selectedProds.length > 0) {
            selectedProds.forEach((prod, idx) => {
              const config = this.chartConfigIndex.seriesConfig[prod] || { type: 'line', yAxis: 0 };
              const fundData = this.dataObj[prod] || [];
              const data = xAxisData.map(time => {
                const row = fundData.find(r => r.TDATE === time);
                return row ? (parseFloat(String(row[currentInd] || '0').replace(/%/g, '').replace(/,/g, '')) || 0) : 0;
              });
              const realType = (config.type === 'area' || config.type === 'stackLine') ? 'line'
                : config.type === 'stackBar' ? 'bar' : config.type;
              const seriesItem = {
                name: this.getProductName(prod),
                type: realType,
                yAxisIndex: config.yAxis,
                smooth: this.chartStyle.smooth,
                data: data,
                itemStyle: { color: themeColors[idx % themeColors.length] },
                lineStyle: { width: 2.5 }
              };
              if (config.type === 'area' || (isArea && config.type === 'line')) {
                seriesItem.areaStyle = { opacity: 0.15 }
              }
              if (config.type === 'stackLine' || config.type === 'stackBar' || config.type === 'stackArea') {
                seriesItem.stack = 'total'
                if (config.type === 'stackLine') seriesItem.areaStyle = { opacity: 0.08 }
                if (config.type === 'stackArea') seriesItem.areaStyle = { opacity: 0.25 }
              }
              if (this.chartStyle.showDataLabel) {
                seriesItem.label = { show: true, position: 'top', fontSize: 10, color: '#666' }
              }
              seriesData.push(seriesItem);
            });
          }
        }
      } else if (this.currentTempType === 'C') {
        const selectedInds = this.chartConfigC.indicators || [];
        const selectedProds = this.chartConfigC.products || [];

        xAxisData = selectedInds.map(code => this.getIndicatorName(code));

        selectedProds.forEach((prod, idx) => {
          const data = selectedInds.map(indCode => {
            const indName = this.getIndicatorName(indCode);
            const row = this.tableDataC.find(r => r.indexName === indName);
            if (row && row[prod]) {
              const val = parseFloat(String(row[prod]).replace(/%/g, '').replace(/,/g, ''));
              return isNaN(val) ? 0 : val;
            }
            return 0;
          });

          const seriesItem = {
            name: this.getProductName(prod),
            type: 'bar', // C类型固定为柱状图
            data: data,
            itemStyle: { color: themeColors[idx % themeColors.length] },
            barMaxWidth: 60
          };

          if (this.chartStyle.showDataLabel) {
            seriesItem.label = { show: true, position: 'top', fontSize: 10, color: '#666' }
          }
          seriesData.push(seriesItem);
        });
      } else if (this.currentTempType === 'D') {
        const indCode = this.chartConfigD.indicator;
        const typeCode = this.chartConfigD.typeCode || 'default';
        let currentData = [...(this.dataObj[this.chartConfigD.product] || [])];

        const symbolFieldMap = {
          'ggzb': 'VC_SYMBOL_ggzb',
          'gzzb': 'VC_SYMBOL_gzzb',
          'pzzb': 'VC_SYMBOL_pzzb',
          'gjzb': 'VC_SYMBOL_gjzb',
          'more': 'VC_SYMBOL_more'
        };
        const symbolField = symbolFieldMap[typeCode];

        // 剔除标的代码为空的行，并使用正确的标的字段作为标签
        if (symbolField) {
          currentData = currentData.filter(row => {
            const val = row[symbolField];
            return val !== undefined && val !== null && val !== '' && val !== '-';
          });
        }

        if (indCode && currentData.length > 0) {
          const colInfo = this.availableDIndicators.find(c => c.field === indCode);
          const indName = colInfo ? colInfo.title : indCode;

          // 对条形图做排序处理，Echarts中Y轴第一项在最底部，这里升序排，即可让最大的数值在最顶部
          currentData.sort((a, b) => {
            const valA = parseFloat(String(a[indCode] || '0').replace(/%/g, '').replace(/,/g, '')) || 0;
            const valB = parseFloat(String(b[indCode] || '0').replace(/%/g, '').replace(/,/g, '')) || 0;
            return valA - valB;
          });

          xAxisData = currentData.map(r => {
            return (symbolField ? r[symbolField] : (r.secName || r.secCode)) || '未知';
          });
          const dataVals = currentData.map(r => parseFloat(String(r[indCode] || '0').replace(/%/g, '').replace(/,/g, '')) || 0);

          const seriesItem = {
            name: indName,
            type: 'bar',
            data: dataVals,
            itemStyle: { color: themeColors[0] },
            barMaxWidth: 30
          };
          if (this.chartStyle.showDataLabel) {
            seriesItem.label = { show: true, position: 'right', fontSize: 10, color: '#666' };
          }
          seriesData.push(seriesItem);
        }
      }

      const hasBar = seriesData.some(s => s.type === 'bar');
      let leftName = ''
      let rightName = ''

      let xAxisConfig = {
        type: 'category',
        boundaryGap: hasBar,
        data: xAxisData,
        axisLine: { lineStyle: { color: '#dcdfe6' } },
        axisTick: { show: false },
        axisLabel: { color: '#909399', fontSize: 11 }
      };

      let yAxisConfig = [
        {
          type: 'value',
          name: '', // dynamically set below
          nameTextStyle: { color: '#909399', fontSize: 11 },
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { color: '#909399', fontSize: 11 },
          splitLine: { show: this.chartStyle.showGrid, lineStyle: { color: '#f0f0f0', type: 'dashed' } }
        },
        {
          type: 'value',
          name: '', // dynamically set below
          nameTextStyle: { color: '#909399', fontSize: 11 },
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { color: '#909399', fontSize: 11 },
          splitLine: { show: false }
        }
      ];

      let dataZoomConfig = [
        {
          type: 'inside',
          xAxisIndex: this.currentTempType !== 'D' ? 0 : undefined,
          yAxisIndex: this.currentTempType === 'D' ? 0 : undefined,
          start: 0,
          end: 100
        },
        {
          type: 'slider',
          xAxisIndex: this.currentTempType !== 'D' ? 0 : undefined,
          yAxisIndex: this.currentTempType === 'D' ? 0 : undefined,
          show: xAxisData.length > 20,
          start: 0,
          end: 100,
          height: this.currentTempType !== 'D' ? 20 : undefined,
          bottom: this.currentTempType !== 'D' ? 0 : undefined,
          width: this.currentTempType === 'D' ? 20 : undefined,
          right: this.currentTempType === 'D' ? 0 : undefined,
          borderColor: '#dcdfe6',
          fillerColor: 'rgba(64,158,255,0.15)',
          handleStyle: { color: '#409eff' }
        }
      ];

      if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
        leftName = this.chartConfigTab === 'product' ? this.chartConfigProduct.leftYUnit : this.chartConfigIndex.leftYUnit
        rightName = this.chartConfigTab === 'product' ? this.chartConfigProduct.rightYUnit : this.chartConfigIndex.rightYUnit
        yAxisConfig[0].name = leftName;
        yAxisConfig[1].name = rightName;
      } else if (this.currentTempType === 'C') {
        leftName = this.chartConfigC.yAxisName
        yAxisConfig[0].name = leftName;
        yAxisConfig[1].name = leftName;
      } else if (this.currentTempType === 'D') {
        // 横向柱状图，X轴为数值，Y轴为标的
        xAxisConfig = {
          type: 'value',
          name: this.chartConfigD.xAxisName,
          nameLocation: 'middle',
          nameGap: 24,
          nameTextStyle: { color: '#909399', fontSize: 12 },
          splitLine: { show: this.chartStyle.showGrid, lineStyle: { color: '#f0f0f0', type: 'dashed' } },
          axisLine: { show: false },
          axisTick: { show: false },
          axisLabel: { color: '#909399', fontSize: 11 }
        };
        yAxisConfig = [
          {
            type: 'category',
            data: xAxisData, // 使用标的名称作为Y轴
            axisLine: { lineStyle: { color: '#dcdfe6' } },
            axisTick: { show: false },
            axisLabel: { color: '#909399', fontSize: 11, width: 100, overflow: 'truncate' }
          }
        ];
        // 如果数量太多则设置一下起始缩放
        if (xAxisData.length > 15) {
          dataZoomConfig[0].start = Math.max(0, 100 - Math.floor((15 / xAxisData.length) * 100));
          dataZoomConfig[1].start = Math.max(0, 100 - Math.floor((15 / xAxisData.length) * 100));
        }
      }

      const option = {
        color: themeColors,
        title: this.chartStyle.title ? {
          text: this.chartStyle.title,
          left: 'center',
          top: 8,
          textStyle: {
            fontSize: 16,
            fontWeight: 600,
            color: '#303133'
          }
        } : undefined,
        tooltip: {
          trigger: 'axis',
          backgroundColor: 'rgba(255,255,255,0.96)',
          borderColor: '#ebeef5',
          borderWidth: 1,
          textStyle: { color: '#303133', fontSize: 13 },
          extraCssText: 'box-shadow: 0 4px 20px rgba(0,0,0,0.1); border-radius: 8px;'
        },
        legend: {
          top: this.chartStyle.title ? 36 : 8,
          type: 'scroll',
          textStyle: { fontSize: 12, color: '#606266' },
          itemWidth: 18,
          itemHeight: 10,
          itemGap: 16
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '8%',
          top: this.chartStyle.title ? 75 : 50,
          containLabel: true
        },
        xAxis: xAxisConfig,
        yAxis: yAxisConfig,
        dataZoom: dataZoomConfig,
        animationDuration: 800,
        animationEasing: 'cubicInOut',
        series: seriesData
      }

      this.chartOption = option
    },
    handleTemplateChange(val, vcTemplateType = '', moreParams = {}) {
      // 兼容 val 可能为字符串（从 URL 取）或数字（从接口取）导致 === 匹配失败的问题
      const currentData = this.templateOptions.find(item => String(item.vcTemplateId) === String(val)) || {};
      this.resetChartView()
      this.currentTempType = currentData.vcTemplateType || vcTemplateType
      if (currentData.vcBenchMark || moreParams) {
        try {
          const benchmarkObj = JSON.parse(currentData.vcBenchMark)
          this.formQuery.industryType = benchmarkObj.industryType || moreParams.industryType || 'SWSR'
          this.formQuery.factorType = benchmarkObj.factorType || moreParams.factorType || 'CNE5'
        } catch (e) {
          this.formQuery.industryType = moreParams.industryType || 'SWSR'
          this.formQuery.factorType = moreParams.factorType || 'CNE5'
        }
      } else {
        this.formQuery.industryType = moreParams.industryType || 'SWSR'
        this.formQuery.factorType = moreParams.factorType || 'CNE5'
      }
      // // 预设参数回填
      // // 日期
      // if (currentData.dStartTime && currentData.dEndTime) {
      //   this.formQuery.dateRange = [currentData.dStartTime, currentData.dEndTime];
      // }
      // // 基准
      // if (currentData.vcBenchMark) {
      //   this.formQuery.vcBenchMark = currentData.vcBenchMark
      // }
      // // 数据频率
      // if (currentData.vcTimeRate) {
      //   this.formQuery.dataFreq = currentData.vcTimeRate
      // }
      // // 产品
      // if (currentData.templateByFundDtos && currentData.templateByFundDtos.length) {
      //   this.selectList = currentData.templateByFundDtos.map(item => {
      //     return {
      //       VC_FUNDCODE: item.fundCode,
      //       VC_FUNDNAME: item.fundName
      //     }
      //   })
      // }

      this.tableData = []
      this.tableDataD = {}
      this.dataObj = {}

      // 调用接口获取指标列
      const params = { vcTemplateId: currentData.vcTemplateId || val }
      this.tableLoading = true;
      tempPageApi.getTemplateIndexInfoList(params).then(res => {
        const { status, data } = res.data
        if (status === 200) {
          const colList = data || []
          // 过滤掉固定列（日期、产品、标的代码/名称等保存时拼接的列）
          const beforeCodes = ['before_code', 'ggzb', 'gzzb', 'pzzb', 'gjzb']
          this.currentTemplateIndexList = colList.filter(item => !beforeCodes.includes(item.vcIndexCode))

          // 组装列
          if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
            this.updateTableABDisplay()
          } else if (this.currentTempType === 'C') {
            this.updateTableCDisplay()
          } else if (this.currentTempType === 'D') {
            this.updateTableDDisplay()
          }
        }
      }).finally(() => {
        this.tableLoading = false;
      })
    },
    updateTableDDisplay() {
      let currentCols = this.currentTemplateIndexList
      if (this.dataObj && Object.keys(this.dataObj).length > 0) {
        if (this.showType === '1' && this.activeName) {
          const columnKey = this.activeName + '_column'
          const allowedCols = this.dataObj[columnKey]
          if (Array.isArray(allowedCols) && allowedCols.length > 0) {
            currentCols = this.currentTemplateIndexList.filter(item => allowedCols.includes(item.vcColCode))
          }
        } else if (this.showType === '2') {
          let allAllowedCols = new Set()
          let hasColumnInfo = false
          this.selectList.forEach(fund => {
            const columnKey = fund.VC_FUNDCODE + '_column'
            const allowedCols = this.dataObj[columnKey]
            if (Array.isArray(allowedCols)) {
              hasColumnInfo = true
              allowedCols.forEach(col => allAllowedCols.add(col))
            }
          })
          if (hasColumnInfo) {
            currentCols = this.currentTemplateIndexList.filter(item => allAllowedCols.has(item.vcColCode))
          }
        }
      }

      const columnsMapD = {}
      const tabNames = {}
      currentCols.forEach(item => {
        const typeCode = item.vcTypeCode || 'default'
        const typeName = item.vcTypeName || '默认'
        if (!columnsMapD[typeCode]) {
          if (typeCode === 'ggzb') {
            columnsMapD[typeCode] = [
              { title: '产品', field: 'FCODE', align: 'center', minWidth: 100, fixed: 'left' },
              { title: '标的代码', field: 'VC_SYMBOL_ggzb', align: 'center', minWidth: 100, fixed: 'left' },
            ]
          } else if (typeCode === 'gzzb') {
            columnsMapD[typeCode] = [
              { title: '产品', field: 'FCODE', align: 'center', minWidth: 100, fixed: 'left' },
              { title: '标的代码', field: 'VC_SYMBOL_gzzb', align: 'center', minWidth: 100, fixed: 'left' },
            ]
          } else if (typeCode === 'pzzb') {
            columnsMapD[typeCode] = [
              { title: '产品', field: 'FCODE', align: 'center', minWidth: 100, fixed: 'left' },
              { title: '标的代码', field: 'VC_SYMBOL_pzzb', align: 'center', minWidth: 100, fixed: 'left' },
            ]
          } else if (typeCode === 'gjzb') {
            columnsMapD[typeCode] = [
              { title: '产品', field: 'FCODE', align: 'center', minWidth: 100, fixed: 'left' },
              { title: '标的代码', field: 'VC_SYMBOL_gjzb', align: 'center', minWidth: 100, fixed: 'left' },
            ]
          } else if (typeCode === 'more') {
            columnsMapD[typeCode] = [
              { title: '产品', field: 'FCODE', align: 'center', minWidth: 100, fixed: 'left' },
              { title: '标的代码', field: 'VC_SYMBOL_more', align: 'center', minWidth: 100, fixed: 'left' },
            ]
          }
          tabNames[typeCode] = typeName
        }
        columnsMapD[typeCode].push({
          title: item.vcColName,
          field: item.vcColCode,
          minWidth: 150,
          align: 'center'
        })
      })
      this.tableColumnD = columnsMapD
      this.tabNamesD = tabNames
      const keys = Object.keys(columnsMapD)

      // 当切换到D类型时，设置默认的组合、 activeTabD 和 chartConfigD.typeCode
      if (this.selectList.length > 0 && !this.chartConfigD.product) {
        this.chartConfigD.product = this.selectList[0].VC_FUNDCODE
      }
      if (keys.length > 0 && (!this.activeTabD || !keys.includes(this.activeTabD))) {
        this.activeTabD = keys[0]
        this.chartConfigD.typeCode = keys[0]
      }
      // setTimeout 保证计算属性 availableDIndicators 更新后再执行赋值和绘图
      setTimeout(() => {
        if (this.availableDIndicators.length > 0 && (!this.chartConfigD.indicator || !this.availableDIndicators.find(i=>i.field===this.chartConfigD.indicator))) {
          this.chartConfigD.indicator = this.availableDIndicators[0].field
        }
        this.drawChart()
      }, 50)
    },
    getQueryParams() {
      return {
        templateId: this.formQuery.vcTemplateId,
        templateType: this.currentTempType,
        fundInfos: this.selectList.map((item, index) => ({
          isPack: false,
          fundCodeTitle: item.VC_FUNDNAME || item.fundName || '',
          fundCodeKey: item.VC_FUNDCODE || item.fundCode || '',
          funds: [
            {
              fundCode: item.VC_FUNDCODE || item.fundCode || '',
              dataSource: ""
            }
          ]
        })),
        beginDate: (this.formQuery.dateRange && this.formQuery.dateRange[0]) || '',
        endDate: (this.formQuery.dateRange && this.formQuery.dateRange[1]) || '',
        singleBenchmark: this.formQuery.ZB_INDEXTYPE == '0' ? '' : (this.formQuery.ZB_INDEXCODEA || ''),
        dateType: 'workDate',
        dateStep: this.formQuery.dataFreq || '',
        paramMap: {
          templateCode: this.formQuery.vcTemplateId,
          beginDate: (this.formQuery.dateRange && this.formQuery.dateRange[0]) || '',
          endDate: (this.formQuery.dateRange && this.formQuery.dateRange[1]) || '',
          // fundCode: '',
          benchmarks: this.formQuery.ZB_INDEXTYPE,
          benchmarkA: this.formQuery.ZB_INDEXCODEA,
          benchmarkB: this.formQuery.ZB_INDEXCODEB,
          benchmarkAValue: this.formQuery.ZB_INDEXWEIGHTA,
          benchmarkBValue: this.formQuery.ZB_INDEXWEIGHTB,
          kpiCode: '',
          contrasCode: (this.formQuery.contrasCode || []).join(","),
          industryType: this.formQuery.industryType,
          factorType: this.formQuery.factorType,
          desensitizationFlag: this.formQuery.desensitizationFlag,
          desensitizationFun: this.formQuery.desensitizationFun,
          dataFreqOpen: 'true',
          dataFreq: this.formQuery.dataFreq
        }
      }
    },
    onQuery(isRefresh) {
      this.$refs.formQueryRef.validate((valid) => {
        if (valid) {
          this.resetChartView()
          this.tableLoading = true
          const params = this.getQueryParams()
          pageApi.indexBrowserQuery(params).then(res => {
            const { status, data, message } = res.data;
            if (status === 200 && data) {
              if (this.selectList.length === 0) {
                this.selectList = [...this.selectListTemp]
                this.formQuery.fundNames = this.selectList.map((item) => item.VC_FUNDNAME).join(',')
              }
              if (this.selectList.length > 0) {
                this.activeName = this.selectList[0].VC_FUNDCODE
              }

              if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
                this.dataObj = data || {}
                this.updateTableABDisplay()
              } else if (this.currentTempType === 'C') {
                this.updateTableCDisplay()
                if (Array.isArray(data)) {
                  this.tableDataC = data
                } else if (typeof data === 'object') {
                  // 后端返回结构: { indexCode: { fundCode: value } }
                  this.dataObj = data || {}
                  let filteredDataC = []
                  this.tableDataC.forEach(row => {
                    const indexData = this.dataObj[row.indexCode]
                    let hasValidData = false
                    this.selectList.forEach(fund => {
                      const val = indexData && indexData[fund.VC_FUNDCODE]
                      const finalVal = val !== undefined && val !== null ? val : '-'
                      this.$set(row, fund.VC_FUNDCODE, finalVal)
                      if (finalVal !== '-') {
                        hasValidData = true
                      }
                    })
                    if (hasValidData) {
                      filteredDataC.push(row)
                    }
                  })
                  this.tableDataC = filteredDataC
                }
              } else if (this.currentTempType === 'D') {
                this.dataObj = data || {}
                this.updateTableDDisplay()
                this.updateTableDDisplayData()
                if (this.selectList.length > 0 && !this.chartConfigD.product) {
                  this.chartConfigD.product = this.selectList[0].VC_FUNDCODE
                }
              }

              this.tableLoading = false
            } else {
              this.$message.error(message || "查询失败")
            }
          }).finally(() => {
            this.tableLoading = false;
          })
        }
      })
    },
    handleFundClick() {
      if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
        this.updateTableABDisplay()
      } else if (this.currentTempType === 'D') {
        this.updateTableDDisplayData()
      }
    },
    resetForm(formName) {
      if (this.$refs[formName]) {
        this.$refs[formName].resetFields()
      }
    },
    showMoreQuery() {
      this.isShowMoreQuery = !this.isShowMoreQuery
    },
    handlecheckeddesensitizationChange(value) {
      this.showDesensitization = value
    },
    handleInputWeight(type) {
      if (type === 'A') {
        const val = this.formQuery.ZB_INDEXWEIGHTA
        const isValid = /^\d+(\.\d{1,4})?$/.test(val)
        if (!isValid) {
          this.$message.warning('请输入有效的正数，最多4位小数')
          this.formQuery.ZB_INDEXWEIGHTA = ''
        }
      } else {
        const val = this.formQuery.ZB_INDEXWEIGHTB
        const isValid = /^\d+(\.\d{1,4})?$/.test(val)
        if (!isValid) {
          this.$message.warning('请输入有效的正数，最多4位小数')
          this.formQuery.ZB_INDEXWEIGHTB = ''
        }
      }
    },
    changeContrasCode(val) {
      if (val.length > 3) {
        this.$message({ type: 'warning', message: '对比基准最多只能选三个' })
        this.formQuery.contrasCode.splice(-1)
      }
    },
    getDataFreqOptions(type) {
      commonApi.edimsSelectType(type).then(res => {
        const { status, data } = res.data
        if (status === 0) {
          this.dataFreqOptionList = data
          this.userDataFreqOptionList = data
        }
      })
    },
    initDrag(e) {
      this.isDragging = true;
      this.startX = e.clientX;
      this.startWidth = this.sidebarWidth;
      document.addEventListener('mousemove', this.doDrag);
      document.addEventListener('mouseup', this.stopDrag);
      document.body.style.userSelect = 'none';
    },
    doDrag(e) {
      if (!this.isDragging) return;
      const dx = this.startX - e.clientX;
      let newWidth = this.startWidth + dx;
      if (newWidth < 300) newWidth = 300; // 最小宽度
      if (newWidth > 800) newWidth = 800; // 最大宽度
      this.sidebarWidth = newWidth;
    },
    stopDrag() {
      this.isDragging = false;
      document.removeEventListener('mousemove', this.doDrag);
      document.removeEventListener('mouseup', this.stopDrag);
      document.body.style.userSelect = '';
      // 触发布局更新，确保echarts根据新的容器大小重绘
      window.dispatchEvent(new Event('resize'));
    },
    // 产品列表弹窗提交
    handleFundListSubmit(data) {
      console.log(data)
      this.selectList = data
      this.formQuery.fundNames = data.map((item) => item.VC_FUNDNAME).join(',')
      this.fundListDialogVisible = false
      if (this.currentTempType === 'C') {
        this.updateTableCDisplay()
      }
    },
    updateTableCDisplay() {
      this.tableColumnC = [
        { title: '指标', field: 'indexName', align: 'center', minWidth: 150, className: 'first-col-bg', fixed: 'left' }
      ]
      this.selectList.forEach(item => {
        this.tableColumnC.push({
          title: item.VC_FUNDNAME,
          field: item.VC_FUNDCODE,
          align: 'center',
          minWidth: 120
        })
      })

      this.tableDataC = this.currentTemplateIndexList.map(item => {
        const rowData = {
          indexName: item.vcColName,
          indexCode: item.vcColCode
        }
        this.selectList.forEach(fund => {
          rowData[fund.VC_FUNDCODE] = '-'
        })
        return rowData
      })
    },
    handleFundClick(val) {
      if (['A', 'B'].includes(this.currentTempType) || !this.currentTempType) {
        this.updateTableABDisplay()
      } else if (this.currentTempType === 'D') {
        this.updateTableDDisplay()
        this.updateTableDDisplayData()
      }
    },
    updateTableABDisplay() {
      // 默认全量表头
      let currentCols = this.currentTemplateIndexList

      // 如果是查询后，且存在对应产品的列信息，则过滤表头
      if (this.dataObj && Object.keys(this.dataObj).length > 0) {
        if (this.showType === '1' && this.activeName) {
          const columnKey = this.activeName + '_column'
          const allowedCols = this.dataObj[columnKey]
          if (Array.isArray(allowedCols) && allowedCols.length > 0) {
            currentCols = this.currentTemplateIndexList.filter(item => allowedCols.includes(item.vcColCode))
          }
        } else if (this.showType === '2') {
          // 如果是排列展示，取所有选中的产品的列信息的并集
          let allAllowedCols = new Set()
          let hasColumnInfo = false
          this.selectList.forEach(fund => {
            const columnKey = fund.VC_FUNDCODE + '_column'
            const allowedCols = this.dataObj[columnKey]
            if (Array.isArray(allowedCols)) {
              hasColumnInfo = true
              allowedCols.forEach(col => allAllowedCols.add(col))
            }
          })
          if (hasColumnInfo) {
            currentCols = this.currentTemplateIndexList.filter(item => allAllowedCols.has(item.vcColCode))
          }
        }
      }

      // 统一表头
      this.tableColumn = [
        { title: '日期', field: 'TDATE', minWidth: 100, align: 'center', fixed: 'left' },
        { title: '产品', field: 'FCODE', minWidth: 150, align: 'center', fixed: 'left' }
      ].concat(
        currentCols.map(item => ({
          title: item.vcColName,
          field: item.vcColCode,
          minWidth: 150,
          align: 'center'
        }))
      )

      if (this.showType === '1') {
        // sheet展示：查看单个产品数据
        this.tableData = this.dataObj[this.activeName] || []
      } else {
        // 排列展示：查看所有产品数据，将数据垂直合并到一个表格中
        let allData = []
        this.selectList.forEach(fund => {
          if (this.dataObj[fund.VC_FUNDCODE]) {
            allData = allData.concat(this.dataObj[fund.VC_FUNDCODE])
          }
        })
        this.tableData = allData
      }
    },
    updateTableDDisplayData() {
      // 每个标签页类型对应的标的代码字段
      const symbolFieldMap = {
        'ggzb': 'VC_SYMBOL_ggzb',
        'gzzb': 'VC_SYMBOL_gzzb',
        'pzzb': 'VC_SYMBOL_pzzb',
        'gjzb': 'VC_SYMBOL_gjzb',
        'more': 'VC_SYMBOL_more'
      }

      let sourceData = []
      if (this.showType === '1') {
        // sheet展示：查看单个产品数据
        sourceData = this.dataObj[this.activeName] || []
      } else {
        // 排列展示：查看所有产品数据，将数据垂直合并到一个表格中
        this.selectList.forEach(fund => {
          if (this.dataObj[fund.VC_FUNDCODE]) {
            sourceData = sourceData.concat(this.dataObj[fund.VC_FUNDCODE])
          }
        })
      }

      // 按标签页类型过滤：剔除标的代码列无数据的行
      const tableDataD = {}
      Object.keys(this.tableColumnD).forEach(typeCode => {
        const symbolField = symbolFieldMap[typeCode]
        if (symbolField) {
          tableDataD[typeCode] = sourceData.filter(row => {
            const val = row[symbolField]
            return val !== undefined && val !== null && val !== '' && val !== '-'
          })
        } else {
          // 未知类型，保留全部数据
          tableDataD[typeCode] = sourceData
        }
      })
      this.tableDataD = tableDataD
    },
    // 导出
    exportExcelFile() {
      this.$refs.formQueryRef.validate((valid) => {
        if (valid) {
          const url = "/api/browser/indexBrowser_download"
          const params = this.getQueryParams()
          const fileName = "数据浏览器.xlsx";
          this.exportLoading = true;
          downLoadFileByUrlPost(url, params, fileName, this)
        }
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dataBrowser-dataView {
  height: calc(100% - 20px);
  overflow-y: auto;
  padding: 12px 10px;
  box-sizing: border-box;
  ::v-deep .vxe-body--column.first-col-bg,
  ::v-deep .vxe-header--column.first-col-bg {
    background-color: #f5f7fa !important;
  }

  // .radio-button-group {}

  .dataView-toolbar {
    height: 50px;
    display: flex;
    align-items: center;
    justify-content: space-between;

    .dataView-toolbar-left {
      // width: calc(100% - 220px);
      width: 100%;
    }

    .dataView-toolbar-right {
      width: 220px;
      display: flex;
      align-items: center;
    }
  }

  .custom-card-tabs {
    ::v-deep .el-tabs__header .el-tabs__item.is-active {
      font-weight: 600;
    }
  }

  .custom-card-tabs-D {
    height: 100%;
    ::v-deep .el-tabs__content {
      height: calc(100% - 45px);
      .el-tab-pane {
        height: 100%;
      }
    }
  }

  .view-content {
    height: calc(100% - 160px);
    .table-view {
      height: 100%;
    }
  }

  // ===== PPT风格图表编辑器 =====
  .chart-view-wrapper {
    border: 1px solid #e4e7ed;
    border-radius: 8px;
    overflow: hidden;
    background: #fff;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
  }

  // 顶部工具栏
  .chart-toolbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 46px;
    padding: 0 16px;
    background: linear-gradient(180deg, #fafbfc 0%, #f5f7fa 100%);
    border-bottom: 1px solid #ebeef5;

    .chart-toolbar-left,
    .chart-toolbar-right {
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .chart-toolbar-left {
      flex: 1;
    }

    .chart-title-edit {
      display: flex;
      align-items: center;
      gap: 6px;

      .chart-title-icon {
        color: #909399;
        font-size: 15px;
      }

      .chart-title-input {
        width: 200px;

        ::v-deep .el-input__inner {
          border: 1px solid transparent;
          background: transparent;
          font-size: 14px;
          font-weight: 500;
          color: #303133;
          padding: 0 8px;
          height: 30px;
          line-height: 30px;
          transition: all 0.2s;

          &:hover {
            border-color: #dcdfe6;
            background: #fff;
          }

          &:focus {
            border-color: #409eff;
            background: #fff;
            box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.15);
          }
        }
      }
    }

    // 图表类型按钮
    .chart-type-btns {
      display: flex;
      gap: 2px;
      background: #ebeef5;
      border-radius: 6px;
      padding: 2px;
    }

    .chart-type-btn {
      width: 32px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      cursor: pointer;
      color: #909399;
      transition: all 0.2s;


      &:hover {
        color: #409eff;
        background: rgba(64, 158, 255, 0.08);
      }

      &.active {
        color: #409eff;
        background: #fff;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
      }
    }

    // 工具栏切换按钮
    .toolbar-toggle-btn {
      width: 30px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      cursor: pointer;
      color: #909399;
      transition: all 0.2s;
      font-size: 15px;

      &:hover {
        color: #409eff;
        background: rgba(64, 158, 255, 0.08);
      }

      &.active {
        color: #409eff;
        background: rgba(64, 158, 255, 0.12);
      }
    }

    .toolbar-action-btn {
      display: flex;
      align-items: center;
      border-color: #dcdfe6;
      background: #fff;
      padding: 5px 10px;
      font-size: 12px;
    }
  }

  // 颜色主题
  .color-theme-dots {
    display: inline-flex;
    gap: 2px;
    align-items: center;
  }

  .color-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
  }


  // 图表主体区域
  .chart-main-area {
    display: flex;
    height: 520px;
  }

  .chart-canvas-area {
    flex: 1;
    min-width: 0;
    padding: 12px;
    box-sizing: border-box;
    background: #fafbfc;
    background-image:
      radial-gradient(circle, #e4e7ed 0.5px, transparent 0.5px);
    background-size: 20px 20px;
  }

  .chart-canvas-inner {
    width: 100%;
    height: 100%;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
    overflow: hidden;
  }

  // 拖拽条
  .resize-bar {
    width: 8px;
    cursor: col-resize;
    background-color: transparent;
    transition: background-color 0.3s;
    z-index: 10;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;

    .resize-bar-line {
      width: 2px;
      height: 30px;
      border-radius: 1px;
      background: #dcdfe6;
      transition: all 0.2s;
    }

    &:hover,
    &.dragging {
      background-color: rgba(64, 158, 255, 0.06);

      .resize-bar-line {
        background: #409eff;
        height: 40px;
      }
    }
  }

  // 右侧配置栏
  .chart-config-sidebar {
    border-left: 1px solid #ebeef5;
    box-sizing: border-box;
    overflow-y: auto;
    background: #fff;
    flex-shrink: 0;

    &::-webkit-scrollbar {
      width: 4px;
    }

    &::-webkit-scrollbar-thumb {
      background: #dcdfe6;
      border-radius: 2px;
    }

    &::-webkit-scrollbar-track {
      background: transparent;
    }
  }

  .sidebar-inner {
    padding: 8px 14px;
  }

  // 配置标签页
  .config-tabs {
    ::v-deep .el-tabs__header {
      margin-bottom: 10px;
    }

    ::v-deep .el-tabs__item {
      font-size: 13px;
      padding: 0 14px;
    }
  }

  // 可折叠面板
  .config-panel {
    margin-bottom: 8px;
    border: 1px solid #ebeef5;
    border-radius: 6px;
    overflow: hidden;
    background: #fff;
  }

  .config-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 12px;
    background: #f8f9fb;
    cursor: pointer;
    transition: background 0.2s;
    user-select: none;

    span {
      font-size: 13px;
      font-weight: 500;
      color: #303133;
      display: flex;
      align-items: center;
      gap: 6px;

      i {
        color: #909399;
        font-size: 14px;
      }
    }

    >i {
      color: #c0c4cc;
      font-size: 12px;
      transition: transform 0.2s;
    }

    &:hover {
      background: #f0f2f5;
    }
  }

  .config-panel-body {
    padding: 10px 12px;
    border-top: 1px solid #ebeef5;
  }

  .compact-form-item {
    margin-bottom: 10px !important;

    ::v-deep .el-form-item__label {
      font-size: 12px;
      color: #606266;
      padding-bottom: 4px;
    }
  }

  // 序列配置行
  .series-config-row {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 6px 0;
    border-bottom: 1px solid #f5f7fa;

    &:last-child {
      border-bottom: none;
    }
  }

  .series-color-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .series-name {
    flex: 1;
    font-size: 12px;
    color: #606266;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
  }

  // 刷新按钮
  .refresh-chart-btn {
    width: 100%;
    margin-top: 12px;
    border-radius: 6px;
  }
}
</style>

<!-- 非scoped样式，用于dropdown等弹出层 -->
<style lang="scss">
.color-theme-dropdown {
  .el-dropdown-menu__item {
    padding: 6px 12px !important;
  }
}

.color-theme-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 6px;
  border-radius: 4px;
  transition: background 0.2s;

  &.active {
    background: rgba(64, 158, 255, 0.08);
  }

  .color-theme-dots {
    display: flex;
    gap: 3px;
  }

  .color-dot-lg {
    width: 14px;
    height: 14px;
    border-radius: 3px;
    display: inline-block;
  }

  .color-theme-name {
    font-size: 13px;
    color: #606266;
    margin-left: 4px;
  }
}
</style>