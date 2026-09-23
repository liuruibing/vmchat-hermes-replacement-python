<template>
  <div :class="{ 'is-sidebar-collapsed': moduleSidebarCollapsed }" :style="chatLayoutStyle" class="vm-chat-page" @click="collapseReportTocOnOutsideClick">
    <aside :class="{ 'is-entering': sidebarContentEntering }" class="module-sidebar">
      <div class="toc-head">
        <div class="toc-head__actions" aria-label="工作区操作">
          <div class="toc-head__mode-row">
            <el-switch v-model="layoutEditable" class="toc-layout-switch" active-text="编辑布局" inactive-text="浏览布局" />
          </div>
          <div class="toc-head__button-row">
            <el-button
              :disabled="!canMergeSelectedBlocks"
              class="toc-action-button"
              title="合并模块"
              native-type="button"
              @click="mergeSelectedBlocks"
            >
              <i class="el-icon-connection" />
              <span>合并</span>
            </el-button>
            <el-button
              :disabled="!reportBlocks.length"
              class="toc-action-button"
              title="保存当前布局"
              native-type="button"
              @click="saveCurrentLayoutTemplate"
            >
              <i class="el-icon-folder-add" />
              <span>保存</span>
            </el-button>
            <el-button
              :disabled="sending || (!reportBlocks.length && !reportNotices.length)"
              class="toc-action-button toc-action-button--danger"
              title="清空报告"
              native-type="button"
              @click="resetReport"
            >
              <i class="el-icon-refresh" />
              <span>清空</span>
            </el-button>
          </div>
        </div>
      </div>
      <div class="toc-body">
        <section class="custom-module-panel">
          <div class="toc-title toc-title--templates">
            <span class="toc-title-main">
              <i class="el-icon-collection-tag" />
              自定义模块
            </span>
            <small>{{ savedTemplates.length }} 个</small>
          </div>
          <div class="toc-search">
            <i class="el-icon-search toc-search__icon" />
            <input v-model="templateSearchQuery" class="toc-search__input" type="text" placeholder="筛选模块..." />
            <button v-if="templateSearchQuery" class="toc-search__clear" type="button" @click="templateSearchQuery = ''">&times;</button>
          </div>
          <div v-if="!savedTemplates.length" class="toc-empty">还没有保存的自定义模块</div>
          <div v-else class="custom-module-list">
            <div v-if="!filteredSavedTemplates.length" class="toc-empty">暂无匹配模块</div>
            <div
              v-for="template in filteredSavedTemplates"
              :key="template.id"
              :class="'template-card--' + template.entityType"
              class="template-card"
            >
              <div class="template-card__header">
                <div :title="template.title" class="template-card__title">{{ template.title }}</div>
                <el-tag :type="getTemplateTagType(template)" effect="plain" size="mini">
                  {{ getTemplateTypeLabel(template) }}
                </el-tag>
              </div>
              <div class="template-card__body">
                <div class="template-card__audit">
                  <span :title="'最后更新时间：' + formatTemplateDate(template.updatedAt)">
                    <i class="el-icon-time" />
                    更新时间：{{ formatTemplateDate(template.updatedAt) }}
                  </span>
                  <span :title="'更新人：' + getTemplateUpdatedBy(template)">
                    <i class="el-icon-user" />
                    更新人：{{ getTemplateUpdatedBy(template) }}
                  </span>
                </div>
                <div class="template-card__actions">
                  <el-button size="mini" type="text" @click.stop="insertTemplate(template.id)">插入</el-button>
                  <el-button size="mini" type="text" @click.stop="removeSavedTemplate(template.id)">删除</el-button>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
      <button
        aria-label="折叠左侧导航"
        class="sidebar-collapse-toggle"
        title="折叠左侧导航"
        type="button"
        @click="moduleSidebarCollapsed = true"
      >
        <svg aria-hidden="true" class="sidebar-toggle-icon" viewBox="0 0 24 24">
          <path d="m14 7-5 5 5 5" />
        </svg>
      </button>
    </aside>

    <section
      ref="renderPanel"
      :class="{ 'has-product-selector': globalProductSelectorVisible }"
      class="render-panel"
    >
      <transition name="sidebar-expand">
        <button
          v-if="moduleSidebarCollapsed"
          aria-label="展开左侧导航"
          class="sidebar-expand-toggle"
          title="展开左侧导航"
          type="button"
          @click="moduleSidebarCollapsed = false"
        >
          <svg aria-hidden="true" class="sidebar-toggle-icon" viewBox="0 0 24 24">
            <path d="m10 7 5 5-5 5" />
          </svg>
        </button>
      </transition>
      <div v-if="!tocCollapsed" class="report-toc">
        <div class="report-toc__panel" @click.self="tocCollapsed = true">
          <div class="report-toc__header">
            <div class="toc-title toc-title--blocks">
              <span class="toc-title-main">
                <i class="el-icon-notebook-2" />
                报告块目录
              </span>
              <small>{{ reportBlocks.length }} 个报告块</small>
            </div>
            <button title="收起报告块目录" class="report-toc__close" type="button" @click="tocCollapsed = true">
              <i class="el-icon-close" />
            </button>
          </div>
          <div class="toc-search">
            <i class="el-icon-search toc-search__icon" />
            <input v-model="blockSearchQuery" class="toc-search__input" type="text" placeholder="筛选报告块..." />
            <button v-if="blockSearchQuery" class="toc-search__clear" type="button" @click="blockSearchQuery = ''">&times;</button>
          </div>
          <div class="toc-block-list-wrapper" @click.self="tocCollapsed = true">
            <div v-if="!filteredReportTocItems.length" class="toc-empty">暂无报告块</div>
            <button
              v-for="(item, index) in filteredReportTocItems"
              :key="item.entityKey"
              :class="{ 'is-active': item.blockIds.includes(activeBlockId), 'is-drag-over': tocDragTargetId === item.entityKey, 'is-selected': item.blockIds.includes(selectedBlockId) }"
              class="toc-item"
              draggable="true"
              type="button"
              @click="focusReportTocItem(item)"
              @dragend="resetReportBlockDrag"
              @dragover.prevent="tocDragTargetId = item.entityKey"
              @dragstart="startReportBlockDrag(item.entityKey, $event)"
              @drop.prevent="dropReportBlock(item.entityKey)"
            >
              <span class="toc-item__drag" title="上下拖拽调整报告块顺序"><i class="el-icon-rank" /></span>
              <span class="toc-index">{{ index + 1 }}</span>
              <span class="toc-name">{{ item.title }}</span>
              <small v-if="item.kind === 'group'" class="toc-item__meta">组合 · {{ item.blockIds.length }} 块</small>
            </button>
          </div>
        </div>
      </div>
      <div class="render-toolbar">
        <div class="render-toolbar__main">
          <div class="render-title">
            <span>智能分析工作台</span>
            <button
              :aria-expanded="String(!tocCollapsed)"
              :class="{ 'is-active': !tocCollapsed }"
              class="render-report-toc-trigger"
              title="报告块目录"
              type="button"
              @click.stop="tocCollapsed = !tocCollapsed"
            >
              <svg aria-hidden="true" class="report-toc-trigger-icon" viewBox="0 0 20 20">
                <path d="M4 5h12M4 10h12M4 15h12" />
                <circle cx="2.5" cy="5" r=".7" />
                <circle cx="2.5" cy="10" r=".7" />
                <circle cx="2.5" cy="15" r=".7" />
              </svg>
              <span>报告目录</span>
              <small>{{ reportBlocks.length }}</small>
            </button>
          </div>
        </div>
        <div v-if="selectedBlockTitle || selectedBlockIds.length > 1" class="toolbar-actions">
          <span v-if="selectedBlockTitle" :title="'当前块：' + selectedBlockTitle" class="selected-chip">当前块：{{ selectedBlockTitle }}</span>
          <span v-if="selectedBlockIds.length > 1" class="selected-chip">已多选：{{ selectedBlockIds.length }} 个</span>
        </div>
        <el-button
          v-if="false"
          :loading="exportingPdf"
          class="render-export-pdf"
          icon="el-icon-download"
          size="mini"
          type="primary"
          @click="exportReportPdf"
        >导出 PDF</el-button>
      </div>

      <section class="global-query-panel" aria-label="通用查询条件">
        <div class="global-query-panel__head">
          <div>
            <div class="global-query-panel__title">
              <i class="el-icon-search" />
              通用查询条件
            </div>
            <div class="global-query-panel__hint">统一应用到当前报告及后续模块的查询请求</div>
          </div>
          <div :class="{ 'is-active': globalQueryTouched }" class="global-query-panel__status">
            {{ globalQueryTouched ? '条件已修改' : '默认条件' }}
          </div>
        </div>
        <div class="global-query-panel__main">
          <label class="global-query-field global-query-field--date">
            <span>开始时间</span>
            <el-date-picker
              v-model="globalQueryParams.beginDate"
              type="date"
              placeholder="选择开始时间"
              value-format="yyyy-MM-dd"
              clearable
              size="mini"
              @change="globalQueryTouched = true"
            />
          </label>
          <label class="global-query-field global-query-field--date">
            <span>结束时间</span>
            <el-date-picker
              v-model="globalQueryParams.endDate"
              type="date"
              placeholder="选择结束时间"
              value-format="yyyy-MM-dd"
              clearable
              size="mini"
              @change="globalQueryTouched = true"
            />
          </label>
          <label class="global-query-field global-query-field--product">
            <span>产品</span>
            <ProductSelectInput
              v-model="globalQueryProduct"
              :input-width="'220px'"
              size="mini"
              placeholder="请选择产品"
              @select="handleGlobalProductSelect"
              @clear="handleGlobalProductClear"
              @visibility-change="globalProductSelectorVisible = $event"
            />
          </label>
          <div class="global-query-panel__actions">
            <button
              :aria-expanded="String(showGlobalQueryMore)"
              :class="{ 'is-open': showGlobalQueryMore }"
              type="button"
              class="global-query-more-toggle"
              @click="showGlobalQueryMore = !showGlobalQueryMore"
            >
              <i class="el-icon-s-operation" />
              <span>更多条件</span>
              <em v-if="globalQueryMoreCount">{{ globalQueryMoreCount }}</em>
              <i class="el-icon-arrow-down global-query-more-toggle__arrow" />
            </button>
            <el-button :loading="globalQueryApplying" class="global-query-apply" size="mini" type="primary" @click="applyGlobalQueryParams">
              应用查询
            </el-button>
          </div>
        </div>
        <transition name="query-more">
          <div v-if="showGlobalQueryMore" class="global-query-more">
            <div class="global-query-more__grid">
              <label class="global-query-field">
                <span>数据频率</span>
                <el-select
                  v-model="globalQueryParams.dataFreq"
                  :loading="globalQueryOptionsLoading"
                  size="mini"
                  filterable
                  placeholder="请选择频率"
                  @change="globalQueryTouched = true"
                >
                  <el-option
                    v-for="item in globalQueryDataFreqOptions"
                    :key="item.code"
                    :label="item.label"
                    :value="item.label"
                  />
                </el-select>
              </label>
              <label class="global-query-field">
                <span>基准模式</span>
                <el-select v-model="globalQueryParams.benchmarks" size="mini" placeholder="请选择基准模式" @change="handleGlobalBenchmarkModeChange">
                  <el-option label="无基准" value="0" />
                  <el-option label="单基准" value="1" />
                  <el-option label="复合基准" value="2" />
                </el-select>
              </label>
              <label v-if="globalQueryParams.benchmarks === '1' || globalQueryParams.benchmarks === '2'" class="global-query-field">
                <span>基准一</span>
                <el-select
                  v-model="globalQueryParams.benchmarkA"
                  :loading="globalQueryOptionsLoading"
                  size="mini"
                  filterable
                  allow-create
                  default-first-option
                  placeholder="请选择基准"
                  @change="globalQueryTouched = true"
                >
                  <el-option
                    v-for="item in globalQueryBenchmarkOptions"
                    :key="item.code"
                    :label="item.label + '（' + item.code + '）'"
                    :value="item.label"
                  />
                </el-select>
              </label>
              <label v-if="globalQueryParams.benchmarks === '2'" class="global-query-field">
                <span>基准二</span>
                <el-select
                  v-model="globalQueryParams.benchmarkB"
                  :loading="globalQueryOptionsLoading"
                  size="mini"
                  filterable
                  allow-create
                  default-first-option
                  placeholder="请选择基准"
                  @change="globalQueryTouched = true"
                >
                  <el-option
                    v-for="item in globalQueryBenchmarkOptions"
                    :key="item.code"
                    :label="item.label + '（' + item.code + '）'"
                    :value="item.label"
                  />
                </el-select>
              </label>
            </div>
            <div class="global-query-more__footer">
              <span><i class="el-icon-info" /> 所有条件会完整传递给每个 SQL 查询，由对应 sqlCode 自行使用。</span>
            </div>
          </div>
        </transition>
      </section>

      <div id="vm-chat-report-scroll" ref="reportScroller" class="report-scroll">
        <div v-if="!reportBlocks.length && !reportNotices.length" class="empty-render">
          <div class="empty-render__title">{{ renderType === 'clarify' ? '需要补充信息' : 'vmChat 渲染区' }}</div>
          <div class="empty-render__message">在右侧输入问题，业务说明会显示在对话区，报表将展示在这里。</div>
          <ul v-if="renderType === 'clarify' && clarifyQuestions.length" class="clarify-list">
            <li v-for="question in clarifyQuestions" :key="question">
              <span class="markdown-body" v-html="renderMarkdown(question)" />
            </li>
          </ul>
        </div>

        <div v-if="reportNotices.length" class="report-notices">
          <section v-for="(notice, noticeIndex) in reportNotices" :key="notice.createdAt + '-' + notice.status" :class="'is-' + notice.status" class="report-notice">
            <header class="notice-header">
              <div>
                <div class="notice-title">{{ getNoticeTitle(notice) }}</div>
                <div class="notice-meta">
                  <span>状态：{{ getNoticeStatusText(notice) }}</span>
                  <span v-if="notice.traceId">trace：{{ notice.traceId }}</span>
                  <span v-if="notice.createdAt">时间：{{ notice.createdAt }}</span>
                </div>
              </div>
              <div class="notice-actions">
                <el-button
                  v-if="notice.status === 'error' && failedUpdateOperation"
                  :loading="sending"
                  size="mini"
                  icon="el-icon-refresh"
                  @click.stop="retryFailedUpdate"
                >重试更新</el-button>
                <el-button size="mini" icon="el-icon-document-copy" circle @click.stop="copyNoticeDebug(notice)" />
                <el-button size="mini" icon="el-icon-close" circle @click.stop="dismissReportNotice(noticeIndex)" />
              </div>
            </header>
            <div class="notice-message markdown-body" v-html="renderMarkdown(notice.message)" />
            <ul v-if="notice.questions && notice.questions.length" class="notice-questions">
              <li v-for="question in notice.questions" :key="question">
                <span class="markdown-body" v-html="renderMarkdown(question)" />
              </li>
            </ul>
            <details v-if="notice.reason || notice.debugPayload" class="notice-debug">
              <summary>诊断信息</summary>
              <div v-if="notice.reason" class="notice-debug-line markdown-body" v-html="renderMarkdown(notice.reason)" />
              <div v-if="notice.traceId" class="notice-debug-line">traceId：{{ notice.traceId }}</div>
            </details>
          </section>
        </div>

        <grid-layout
          v-if="topLevelViewItems.length"
          ref="gridLayout"
          :layout.sync="gridWidgets"
          :col-num="24"
          :row-height="32"
          :margin="[12, 12]"
          :is-draggable="layoutEditable"
          :is-resizable="layoutEditable"
          :vertical-compact="true"
          :use-css-transforms="true"
          draggable-handle=".drag-handle"
          class="report-grid"
          @layout-updated="handleGridLayoutUpdated"
        >
          <grid-item
            v-for="item in topLevelViewItems"
            :key="item.widget.i"
            :i="item.widget.i"
            :x="item.widget.x"
            :y="item.widget.y"
            :w="item.widget.w"
            :h="item.widget.h"
            :min-w="item.widget.minW || 6"
            :min-h="item.widget.minH || 6"
            class="report-grid-item"
          >
            <article
              v-if="item.kind === 'block'"
              :id="'vm-chat-block-' + item.block.blockId"
              :class="{ 'is-selected': selectedBlockId === item.block.blockId, 'is-multi-selected': selectedBlockIds.includes(item.block.blockId) }"
              class="report-block"
              @click="handleBlockClick(item.block.blockId, $event)"
            >
              <header class="block-header">
                <div class="block-header__main">
                  <div class="block-title-row">
                    <el-checkbox
                      :value="selectedBlockIds.includes(item.block.blockId)"
                      class="block-selector"
                      @click.native.stop
                      @change="toggleBlockSelection(item.block.blockId, $event)"
                    />
                    <button v-if="layoutEditable" type="button" class="drag-handle" title="拖拽布局" @click.stop>
                      <i class="el-icon-rank" />
                    </button>
                    <el-input
                      v-if="editingBlockTitleId === item.block.blockId"
                      :ref="'block-title-input-' + item.block.blockId"
                      v-model="editingBlockTitleValue"
                      class="block-title-editor"
                      size="mini"
                      @blur="commitBlockTitleEdit(item.block.blockId)"
                      @click.native.stop
                      @keyup.enter.native="commitBlockTitleEdit(item.block.blockId)"
                      @keyup.esc.native="cancelBlockTitleEdit"
                    />
                    <div v-else class="block-title">
                      {{ getBlockOrder(item.block.blockId) }}. {{ getBlockDisplayTitle(item.block) }}
                    </div>
                    <el-button
                      v-if="editingBlockTitleId !== item.block.blockId"
                      class="block-title-edit-button"
                      icon="el-icon-edit-outline"
                      title="编辑标题"
                      type="text"
                      @click.stop="startBlockTitleEdit(item.block)"
                    />
                  </div>
                </div>
                <div class="block-actions">
                  <el-button
                    v-if="item.block.renderState && item.block.renderState.status === 'error'"
                    :loading="sending"
                    size="mini"
                    icon="el-icon-refresh"
                    @click.stop="retryBlock(item.block.blockId)"
                  >重新加载</el-button>
                  <el-button-group v-if="layoutEditable">
                    <el-button size="mini" @click.stop="setTopLevelWidgetWidth(item.widget.i, 24)">全宽</el-button>
                    <el-button size="mini" @click.stop="setTopLevelWidgetWidth(item.widget.i, 12)">半宽</el-button>
                  </el-button-group>
                  <el-button
                    :icon="getBlockTemplateSource(item.block) ? 'el-icon-refresh' : 'el-icon-folder-add'"
                    :title="getBlockSaveButtonTitle(item.block)"
                    size="mini"
                    circle
                    @click.stop="saveBlockTemplate(item.block.blockId)"
                  />
                  <el-button
                    v-if="getBlockTemplateSource(item.block)"
                    icon="el-icon-document-copy"
                    title="另存为新模块"
                    size="mini"
                    circle
                    @click.stop="saveBlockTemplateAsNew(item.block.blockId)"
                  />
                  <el-button icon="el-icon-delete" size="mini" circle @click.stop="removeBlock(item.block.blockId)" />
                </div>
              </header>

              <div class="block-content">
                <div v-if="isExampleDataBlock(item.block)" class="block-watermark">示例数据</div>
                <div v-if="item.block.type === 'echarts'" class="block-chart">
                  <my-chart
                    :id="'vm-chat-chart-' + item.block.blockId"
                    :ref="'chart-' + item.block.blockId"
                    :options="item.block.renderSpec && item.block.renderSpec.option"
                    :style="{ width: '100%', height: '100%' }"
                    renderer="svg"
                    resize-dom="report-grid-item"
                  />
                </div>

                <div v-else class="block-table">
                  <vxe-table
                    :key="item.block.blockId + '-' + item.block.updatedAt"
                    :data="(item.block.renderSpec && item.block.renderSpec.rows) || []"
                    border
                    resizable
                    auto-resize
                    show-overflow
                    size="small"
                    height="100%"
                  >
                    <vxe-table-column
                      v-for="column in (item.block.renderSpec && item.block.renderSpec.columns) || []"
                      :key="column.field"
                      :field="column.field"
                      :title="column.title"
                      :min-width="column.minWidth || column.width || 120"
                      :align="column.align || 'left'"
                      :formatter="column.formatter"
                    />
                  </vxe-table>
                  <details v-if="getBlockDiagnostics(item.block).length" class="block-diagnostics" open>
                    <summary>诊断信息</summary>
                    <div v-for="(diagnostic, diagnosticIndex) in getBlockDiagnostics(item.block)" :key="diagnosticIndex" class="diagnostic-item">
                      <strong>{{ diagnostic.status }}</strong>
                      <span>{{ diagnostic.detail }}</span>
                    </div>
                  </details>
                </div>
              </div>
            </article>

            <article v-else class="report-group">
              <header class="group-header">
                <div class="group-header__main">
                  <div class="block-title-row">
                    <button v-if="layoutEditable" type="button" class="drag-handle" title="拖拽组合模块" @click.stop>
                      <i class="el-icon-rank" />
                    </button>
                    <el-input v-if="layoutEditable" :value="item.group.title" size="mini" class="group-title-input" @input="updateGroupTitle(item.group.groupId, $event)" />
                    <div v-else class="block-title">{{ item.group.title || '未命名组合' }}</div>
                  </div>
                </div>
                <div class="block-actions">
                  <el-button-group v-if="layoutEditable">
                    <el-button size="mini" @click.stop="setTopLevelWidgetWidth(item.widget.i, 24)">全宽</el-button>
                    <el-button size="mini" @click.stop="setTopLevelWidgetWidth(item.widget.i, 12)">半宽</el-button>
                  </el-button-group>
                  <el-button
                    :icon="getGroupTemplateSource(item.group) ? 'el-icon-refresh' : 'el-icon-folder-add'"
                    :title="getGroupSaveButtonTitle(item.group)"
                    size="mini"
                    circle
                    @click.stop="saveGroupTemplate(item.group.groupId)"
                  />
                  <el-button
                    v-if="getGroupTemplateSource(item.group)"
                    icon="el-icon-document-copy"
                    title="另存为新组合模块"
                    size="mini"
                    circle
                    @click.stop="saveGroupTemplateAsNew(item.group.groupId)"
                  />
                  <el-button icon="el-icon-refresh-left" size="mini" circle @click.stop="ungroup(item.group.groupId)" />
                </div>
              </header>

              <grid-layout
                :layout="item.group.widgets"
                :col-num="24"
                :row-height="28"
                :margin="[10, 10]"
                :is-draggable="layoutEditable"
                :is-resizable="layoutEditable"
                :vertical-compact="true"
                :use-css-transforms="true"
                draggable-handle=".drag-handle"
                class="report-group-grid"
                @layout-updated="handleGroupLayoutUpdated(item.group.groupId, $event)"
              >
                <grid-item
                  v-for="childWidget in item.group.widgets"
                  :key="childWidget.i"
                  :i="childWidget.i"
                  :x="childWidget.x"
                  :y="childWidget.y"
                  :w="childWidget.w"
                  :h="childWidget.h"
                  :min-w="childWidget.minW || 6"
                  :min-h="childWidget.minH || 6"
                  class="report-grid-item report-grid-item--nested"
                >
                  <article
                    :id="'vm-chat-block-' + item.group.blocksById[childWidget.i].blockId"
                    :class="{
                      'is-selected': selectedBlockId === item.group.blocksById[childWidget.i].blockId,
                      'is-multi-selected': selectedBlockIds.includes(item.group.blocksById[childWidget.i].blockId)
                    }"
                    class="report-block report-block--nested"
                    @click="handleBlockClick(item.group.blocksById[childWidget.i].blockId, $event)"
                  >
                    <header class="block-header">
                      <div class="block-header__main">
                        <div class="block-title-row">
                          <el-checkbox
                            :value="selectedBlockIds.includes(item.group.blocksById[childWidget.i].blockId)"
                            class="block-selector"
                            @click.native.stop
                            @change="toggleBlockSelection(item.group.blocksById[childWidget.i].blockId, $event)"
                          />
                          <button v-if="layoutEditable" type="button" class="drag-handle" title="拖拽组内布局" @click.stop>
                            <i class="el-icon-rank" />
                          </button>
                          <el-input
                            v-if="editingBlockTitleId === item.group.blocksById[childWidget.i].blockId"
                            :ref="'block-title-input-' + item.group.blocksById[childWidget.i].blockId"
                            v-model="editingBlockTitleValue"
                            class="block-title-editor"
                            size="mini"
                            @blur="commitBlockTitleEdit(item.group.blocksById[childWidget.i].blockId)"
                            @click.native.stop
                            @keyup.enter.native="commitBlockTitleEdit(item.group.blocksById[childWidget.i].blockId)"
                            @keyup.esc.native="cancelBlockTitleEdit"
                          />
                          <div v-else class="block-title">
                            {{ getBlockOrder(item.group.blocksById[childWidget.i].blockId) }}. {{ getBlockDisplayTitle(item.group.blocksById[childWidget.i]) }}
                          </div>
                          <el-button
                            v-if="editingBlockTitleId !== item.group.blocksById[childWidget.i].blockId"
                            class="block-title-edit-button"
                            icon="el-icon-edit-outline"
                            title="编辑标题"
                            type="text"
                            @click.stop="startBlockTitleEdit(item.group.blocksById[childWidget.i])"
                          />
                        </div>
                      </div>
                      <div class="block-actions">
                        <el-button
                          v-if="item.group.blocksById[childWidget.i].renderState && item.group.blocksById[childWidget.i].renderState.status === 'error'"
                          :loading="sending"
                          size="mini"
                          icon="el-icon-refresh"
                          @click.stop="retryBlock(item.group.blocksById[childWidget.i].blockId)"
                        >重新加载</el-button>
                        <el-button-group v-if="layoutEditable">
                          <el-button size="mini" @click.stop="setGroupBlockWidth(item.group.groupId, childWidget.i, 24)">全宽</el-button>
                          <el-button size="mini" @click.stop="setGroupBlockWidth(item.group.groupId, childWidget.i, 12)">半宽</el-button>
                        </el-button-group>
                        <el-button
                          :icon="getBlockTemplateSource(item.group.blocksById[childWidget.i]) ? 'el-icon-refresh' : 'el-icon-folder-add'"
                          :title="getBlockSaveButtonTitle(item.group.blocksById[childWidget.i])"
                          size="mini"
                          circle
                          @click.stop="saveBlockTemplate(item.group.blocksById[childWidget.i].blockId)"
                        />
                        <el-button
                          v-if="getBlockTemplateSource(item.group.blocksById[childWidget.i])"
                          icon="el-icon-document-copy"
                          title="另存为新模块"
                          size="mini"
                          circle
                          @click.stop="saveBlockTemplateAsNew(item.group.blocksById[childWidget.i].blockId)"
                        />
                        <el-button icon="el-icon-delete" size="mini" circle @click.stop="removeBlock(item.group.blocksById[childWidget.i].blockId)" />
                      </div>
                    </header>

                    <div class="block-content">
                      <div v-if="isExampleDataBlock(item.group.blocksById[childWidget.i])" class="block-watermark">示例数据</div>
                      <div v-if="item.group.blocksById[childWidget.i].type === 'echarts'" class="block-chart">
                        <my-chart
                          :id="'vm-chat-chart-' + item.group.blocksById[childWidget.i].blockId"
                          :ref="'chart-' + item.group.blocksById[childWidget.i].blockId"
                          :options="item.group.blocksById[childWidget.i].renderSpec && item.group.blocksById[childWidget.i].renderSpec.option"
                          :style="{ width: '100%', height: '100%' }"
                          renderer="svg"
                          resize-dom="report-grid-item"
                        />
                      </div>

                      <div v-else class="block-table">
                        <vxe-table
                          :key="item.group.blocksById[childWidget.i].blockId + '-' + item.group.blocksById[childWidget.i].updatedAt"
                          :data="(item.group.blocksById[childWidget.i].renderSpec && item.group.blocksById[childWidget.i].renderSpec.rows) || []"
                          border
                          resizable
                          auto-resize
                          show-overflow
                          size="small"
                          height="100%"
                        >
                          <vxe-table-column
                            v-for="column in (item.group.blocksById[childWidget.i].renderSpec && item.group.blocksById[childWidget.i].renderSpec.columns) || []"
                            :key="column.field"
                            :field="column.field"
                            :title="column.title"
                            :min-width="column.minWidth || column.width || 120"
                            :align="column.align || 'left'"
                            :formatter="column.formatter"
                          />
                        </vxe-table>
                        <details v-if="getBlockDiagnostics(item.group.blocksById[childWidget.i]).length" class="block-diagnostics" open>
                          <summary>诊断信息</summary>
                          <div v-for="(diagnostic, diagnosticIndex) in getBlockDiagnostics(item.group.blocksById[childWidget.i])" :key="diagnosticIndex" class="diagnostic-item">
                            <strong>{{ diagnostic.status }}</strong>
                            <span>{{ diagnostic.detail }}</span>
                          </div>
                        </details>
                      </div>
                    </div>
                  </article>
                </grid-item>
              </grid-layout>
            </article>
          </grid-item>
        </grid-layout>
      </div>
    </section>

    <div
      ref="chatResizer"
      :aria-valuemax="getChatPanelWidthBounds().max"
      :aria-valuemin="getChatPanelWidthBounds().min"
      :aria-valuenow="Math.round(chatPanelWidth)"
      :class="{ 'is-active': chatResizeState }"
      aria-label="调整智能助手宽度"
      aria-orientation="vertical"
      class="chat-resizer"
      role="separator"
      tabindex="0"
      @keydown="handleChatResizeKeydown"
      @pointerdown.prevent="startChatResize"
    >
      <span aria-hidden="true" class="chat-resizer__grip">
        <i /><i /><i />
      </span>
      <span v-if="showChatResizeHint" class="chat-resizer__hint">拖拽调整助手宽度</span>
    </div>

    <aside class="chat-panel">
      <div class="chat-header">
        <div>
          <div class="chat-title">卓沃 AI 智能助手</div>
          <div class="chat-status">模型：{{ analysisModel }}</div>
        </div>
        <!-- <el-button size="small" icon="el-icon-document-copy" @click="copyPageDebug">复制页面 Debug</el-button> -->
      </div>

      <div
        ref="messageList"
        class="message-list"
        @scroll="handleMessageListScroll"
        @wheel.capture="handleMessageListWheel"
      >
        <div v-for="message in chatMessages" :key="message.id" :class="'is-' + message.role" class="message-row">
          <div class="message-bubble">
            <div class="message-name">{{ message.role === 'user' ? '用户' : 'AI 助手' }}</div>
            <div class="message-content markdown-body" v-html="renderMarkdown(message.content)" />
            <div v-if="shouldShowThinking(message)" :class="{ 'is-collapsed': !message.thinkingExpanded }" class="thinking-box">
              <button
                :aria-expanded="String(!!message.thinkingExpanded)"
                class="thinking-label"
                type="button"
                @click="toggleThinking(message)"
              >
                <i class="el-icon-cpu" />
                <span>thinking</span>
                <i :class="message.thinkingExpanded ? 'el-icon-arrow-up' : 'el-icon-arrow-down'" class="thinking-toggle-icon" />
              </button>
              <pre v-show="message.thinkingExpanded" class="thinking-text">{{ message.thinking }}</pre>
            </div>
            <div v-if="message.streamStatus" class="stream-status">{{ message.streamStatus }}</div>
            <div v-if="message.metricsSummary" class="metrics-line">
              {{ message.metricsSummary }}
              <button type="button" class="metrics-toggle" @click="copyMessageDebug(message)">
                {{ message.debugCopied ? '已复制' : '复制 Debug' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="composer">
        <div v-if="selectedBlockTitle" class="composer-context">
          当前将优先更新块：{{ selectedBlockTitle }}
          <button
            type="button"
            class="link-button"
            @click="
              selectedBlockId = ''
              selectedBlockIds = []
            "
          >
            清除
          </button>
        </div>
        <el-input
          v-model="draftMessage"
          :rows="4"
          type="textarea"
          resize="none"
          placeholder="例如：帮我看产品 SM0513 在 2022-01-01 到 2022-01-31 的现金类持仓时序"
          @keydown.native="handleComposerKeydown"
        />
        <div class="composer-actions">
          <div v-if="showExampleEntry" class="example-trigger">
            <el-button size="small" @click.stop="toggleExamplePanel">示例</el-button>
            <div v-if="showExamplePanel" class="example-panel">
              <div class="example-panel__head">
                <span>选择示例问题</span>
                <button type="button" class="example-panel__close" @click.stop="showExamplePanel = false">&times;</button>
              </div>
              <div class="example-panel__list">
                <button v-for="(example, idx) in exampleQuestions" :key="idx" type="button" class="example-item" @click.stop="selectExample(example)">
                  <span class="example-item__index">{{ idx + 1 }}</span>
                  <span class="example-item__text">{{ example }}</span>
                </button>
              </div>
            </div>
            <div v-if="showExamplePanel" class="example-backdrop" @click.stop="showExamplePanel = false" />
          </div>
          <el-button class="render-wiki-trigger" icon="el-icon-document" size="mini" @click="openWikiDialog">Wiki 说明</el-button>
          <el-button :loading="sending" type="primary" size="small" @click="sendMessage">发送</el-button>
        </div>
      </div>
    </aside>

    <el-dialog
      ref="wikiDialog"
      :visible.sync="wikiDialogVisible"
      :lock-scroll="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      title="业务 Wiki 说明"
      append-to-body
      custom-class="wiki-dialog"
      @open="setWikiDialogWidth"
    >
      <div class="wiki-container">
        <aside class="wiki-sidebar">
          <el-input
            v-model="wikiTreeFilter"
            class="wiki-tree-filter"
            clearable
            placeholder="筛选文档"
            prefix-icon="el-icon-search"
            size="small"
            style="width: 100% !important"
          />
          <div v-if="wikiTreeLoading" class="wiki-tree-loading">
            <i class="el-icon-loading" />
            <span>加载目录中...</span>
          </div>
          <div v-else-if="wikiTreeError" class="wiki-tree-error">
            <span>{{ wikiTreeError }}</span>
            <el-button size="mini" type="text" @click="retryWikiLoad">重试</el-button>
          </div>
          <el-tree
            v-else
            ref="wikiTreeView"
            :data="wikiTree"
            :current-node-key="wikiSelectedPath"
            :filter-node-method="filterWikiTreeNode"
            :props="{ label: 'displayName', children: 'children' }"
            node-key="path"
            default-expand-all
            highlight-current
            @node-click="handleWikiNodeClick"
          />
        </aside>

        <main ref="wikiContent" class="wiki-content">
          <div class="wiki-search-bar">
            <el-input
              v-model="wikiSearchQuery"
              clearable
              placeholder="查找当前文档"
              prefix-icon="el-icon-search"
              size="small"
              @input="resetWikiSearch"
              @keyup.enter.native="findNextWikiMatch"
            />
            <span class="wiki-search-count">{{ wikiSearchMatchCount ? wikiSearchMatchIndex + 1 + ' / ' + wikiSearchMatchCount : '0 / 0' }}</span>
            <el-button :disabled="!wikiSearchMatchCount" icon="el-icon-arrow-up" size="mini" title="上一项" @click="findPreviousWikiMatch" />
            <el-button :disabled="!wikiSearchMatchCount" icon="el-icon-arrow-down" size="mini" title="下一项" @click="findNextWikiMatch" />
          </div>
          <div v-if="wikiDocumentLoading" class="wiki-state-box">
            <i class="el-icon-loading" />
            <span>文档加载中...</span>
          </div>
          <div v-else-if="wikiError" class="wiki-state-box wiki-state-box--error">
            <span>{{ wikiError }}</span>
            <el-button size="mini" type="primary" @click="retryWikiLoad">重试</el-button>
          </div>
          <div v-else-if="!wikiDocument" class="wiki-state-box wiki-state-box--empty">
            <span>请选择左侧文档查看说明</span>
          </div>
          <article
            v-else
            class="markdown-body wiki-document-content"
            @click="handleWikiDocumentLink"
            v-html="renderHighlightedWikiMarkdown(wikiDocument.markdown)"
          />
        </main>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import myChart from '@/components/Echarts'
import { GridLayout, GridItem } from 'vue-grid-layout'
import { toPng } from 'html-to-image'
import showdown from 'showdown'
import CodeMirror from 'codemirror'
import 'codemirror/addon/runmode/runmode'
import 'codemirror/mode/javascript/javascript'
import {
  DEFAULT_HERMES_ANALYSIS_MODEL,
  shouldUseHermesRunEvents,
  sendHermesRunEvents,
  fetchHermesWikiTree,
  fetchHermesWikiDocument,
  buildHermesRequestUrl,
  buildHermesAuthHeaders
} from '@/api/hermesResearch'
import {
  assertVmHermesOperationAllowed,
  buildVmReportNoticeFromError,
  buildVmReportNoticeFromPayload,
  buildVmHermesMessages,
  buildVmReportBlocksSummary,
  createVmReportBlock,
  getVmProtocolVersion,
  formatVmAssistantStreamingContent,
  isExplicitVmBatchUpdateRequest,
  parseVmHermesRenderPayload
} from './vm-chat-helpers.js'
import { assertVmUpdateHydrationSucceeded, hydrateVmBlock } from './vm-block-hydrator.js'
import {
  createVmDictionaryLoader,
  createVmRequestFetcher,
  fetchVmBenchmarkOptions,
  fetchVmDataFrequencyOptions
} from './vm-api.js'
import { createVmParamResolver } from './vm-param-resolver.js'
import { createVmTraceId, getVmChatLogs, logVmChatEvent } from './vm-logger.js'
import ProductSelectInput from '@/components/productSelector/ProductSelectInput'

const MARKDOWN_CONVERTER = new showdown.Converter({
  ghCodeBlocks: true,
  simplifiedAutoLink: true,
  strikethrough: true,
  tables: true,
  tasklists: true,
  noHeaderId: true,
  openLinksInNewWindow: true
})

const MARKDOWN_ALLOWED_TAGS = new Set([
  'A', 'BLOCKQUOTE', 'BR', 'CODE', 'DEL', 'EM', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6',
  'HR', 'LI', 'MARK', 'OL', 'P', 'PRE', 'SECTION', 'SPAN', 'STRONG', 'TABLE', 'TBODY', 'TD', 'TH', 'THEAD', 'TR', 'UL'
])

function sanitizeMarkdownHtml(html) {
  if (typeof document === 'undefined') return String(html || '').replace(/<[^>]*>/g, '')
  const container = document.createElement('div')
  container.innerHTML = String(html || '')
  container.querySelectorAll('script,style,iframe,object,embed,form,link,meta').forEach(node => node.remove())
  container.querySelectorAll('*').forEach(node => {
    if (!MARKDOWN_ALLOWED_TAGS.has(node.tagName)) {
      node.replaceWith(document.createTextNode(node.textContent || ''))
      return
    }
    Array.from(node.attributes).forEach(attribute => {
      const name = attribute.name.toLowerCase()
      const value = String(attribute.value || '').trim()
      if (name.indexOf('on') === 0 || name === 'style' || (name === 'href' || name === 'src') && /^(?:javascript|data|vbscript):/i.test(value)) {
        node.removeAttribute(attribute.name)
      }
    })
    if (node.tagName === 'A') {
      node.setAttribute('rel', 'noopener noreferrer')
      node.setAttribute('target', '_blank')
    }
  })
  return container.innerHTML
}

function markdownToSafeHtml(value) {
  const markdown = String(value || '').trim()
  if (!markdown) return ''
  return sanitizeMarkdownHtml(MARKDOWN_CONVERTER.makeHtml(markdown))
}

function splitMarkdownFrontmatter(value) {
  const markdown = String(value || '')
  if (!/^---\s*\r?\n/.test(markdown)) return { frontmatter: '', body: markdown }
  const endIndex = markdown.indexOf('\n---', 4)
  if (endIndex < 0) return { frontmatter: '', body: markdown }
  return {
    frontmatter: markdown.slice(4, endIndex).trim(),
    body: markdown.slice(endIndex + 5).replace(/^\s*\r?\n/, '')
  }
}

function escapeHtml(value) {
  return String(value || '').replace(/[&<>"]/g, char => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[char]))
}

function normalizeWikiListIndentation(value) {
  const markdown = String(value || '')
  if (!/^\s{2}[-*+]\s+/m.test(markdown)) return markdown
  return markdown.replace(/^( *)([-*+]\s+)/gm, (line, spaces, marker) => {
    if (!spaces || spaces.length % 2 !== 0) return line
    return ' '.repeat(spaces.length * 2) + marker
  })
}

function renderWikiMarkdown(value) {
  const sections = splitMarkdownFrontmatter(value)
  const metadataHtml = sections.frontmatter
    ? '<section class="wiki-frontmatter">' + sections.frontmatter.split(/\r?\n/).filter(Boolean).map(line => {
      const separatorIndex = line.indexOf(':')
      if (separatorIndex < 0) return '<p>' + escapeHtml(line) + '</p>'
      return '<p><strong>' + escapeHtml(line.slice(0, separatorIndex + 1)) + '</strong>' + escapeHtml(line.slice(separatorIndex + 1)) + '</p>'
    }).join('') + '</section>'
    : ''
  return highlightWikiJsonCodeBlocks(sanitizeMarkdownHtml(metadataHtml + MARKDOWN_CONVERTER.makeHtml(normalizeWikiListIndentation(sections.body).trim())))
}

function highlightWikiJsonCodeBlocks(html) {
  if (typeof document === 'undefined') return html
  const container = document.createElement('div')
  container.innerHTML = html
  container.querySelectorAll('pre > code').forEach(code => {
    const source = String(code.textContent || '').trim()
    if (!source) return
    let json
    try {
      json = JSON.parse(source)
    } catch (error) {
      return
    }
    const formatted = JSON.stringify(json, null, 2)
    CodeMirror.runMode(formatted, { name: 'javascript', json: true }, code)
    code.parentNode.classList.add('wiki-json-code-block')
  })
  return container.innerHTML
}

function highlightWikiHtml(html, query) {
  const keyword = String(query || '').trim()
  if (!keyword || typeof document === 'undefined') return html
  const container = document.createElement('div')
  container.innerHTML = html
  const matcher = new RegExp(keyword.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi')
  const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT)
  const textNodes = []
  let textNode
  while ((textNode = walker.nextNode())) {
    if (!textNode.parentNode || /^MARK$/i.test(textNode.parentNode.nodeName)) continue
    textNodes.push(textNode)
  }
  textNodes.forEach(node => {
    const text = node.nodeValue || ''
    matcher.lastIndex = 0
    if (!matcher.test(text)) return
    matcher.lastIndex = 0
    const fragment = document.createDocumentFragment()
    let cursor = 0
    let match
    while ((match = matcher.exec(text))) {
      fragment.appendChild(document.createTextNode(text.slice(cursor, match.index)))
      const mark = document.createElement('mark')
      mark.className = 'wiki-search-match'
      mark.textContent = match[0]
      fragment.appendChild(mark)
      cursor = match.index + match[0].length
    }
    fragment.appendChild(document.createTextNode(text.slice(cursor)))
    node.parentNode.replaceChild(fragment, node)
  })
  return container.innerHTML
}

const {
  appendBlockWidget,
  createCanvasStateFromBlocks,
  createEntityKey,
  findBlockLocation,
  getOrderedBlocks,
  getOrderedGroupBlocks,
  getOrderedTopLevelItems,
  mergeBlocksToGroup,
  removeBlockWidget,
  renameGroup,
  replaceBlockWidget,
  restoreTemplateToGrid,
  serializeBlockTemplate,
  serializeGroupTemplate,
  serializeLayoutTemplate,
  setGroupChildWidth,
  setTopLevelEntityWidth,
  ungroupToCanvas,
  updateGroupWidgets,
  updateTopLevelWidgets
} = require('./vm-grid-layout-runtime.cjs')

const MODULES_API_ROUTE = buildHermesRequestUrl('/v1/templates')
const SHOW_EXAMPLE_ENTRY = true
const DEFAULT_TEMPLATE_UPDATED_BY = '系统管理员'
const REPORT_TOC_POSITION_KEY = 'vm-chat-report-toc-position'
const DEFAULT_REPORT_TOC_POSITION = { left: 16, top: 82 }
const CHAT_PANEL_WIDTH_RATIO_KEY = 'vm-chat-panel-width-ratio'
const CHAT_PANEL_MIN_WIDTH = 400
const CHAT_PANEL_MAX_WIDTH = 560
const CHAT_PANEL_DEFAULT_RATIO = 0.3
const CHAT_RESIZER_WIDTH = 0
const CHAT_LAYOUT_GAP = 0
const CHAT_RESIZER_HINT_SEEN_KEY = 'vm-chat-resizer-hint-seen'
const DEFAULT_GLOBAL_QUERY_PARAMS = {
  beginDate: '',
  endDate: '',
  productCode: '',
  dataFreqOpen: 'true',
  benchmarks: '0',
  benchmarkA: '',
  benchmarkB: '',
  dataFreq: '日频'
}
function buildCatalogExampleQuestions() {
  return [
    '帮我看看净值走势图',
    '帮我移除净值走势图中的上证指数',
    '请展示产品基本信息',
    '请展示最新净值信息',
    '帮我把最新净值信息的估值日期、资产净值、产品单位净值、累计单位净值合并进产品基本信息中一起展示',
    '帮我把净值走势图的上证指数加回去',
    '帮我看看组合换手率',
    '请展示期货十大亏损品种',
    '我想查一下期货十大盈利品种',
    '帮我把期货十大盈利品种和亏损品种这两个模块合并',
    '我想查一下股票净敞口时序'
  ]
}

function createMessage(role, content, extra) {
  return Object.assign(
    {
      id:
        Date.now() +
        '-' +
        Math.random()
          .toString(16)
          .slice(2),
      role,
      content,
      thinking: '',
      thinkingExpanded: false,
      streamStatus: '',
      metricsSummary: '',
      debugCopied: false,
      debugPayload: null
    },
    extra || {}
  )
}

function createSessionId(protocolVersion) {
  const sessionVersion = String(protocolVersion || 'vm-chat')
    .replace(/[^a-zA-Z0-9]+/g, '-')
    .replace(/^-+|-+$/g, '')
  const key = 'vm-chat-hermes-session-id:' + sessionVersion
  try {
    const cached = window.localStorage.getItem(key)
    if (cached) return cached
    const next =
      'vm-chat-' +
      sessionVersion +
      '-' +
      Date.now().toString(36) +
      '-' +
      Math.random()
        .toString(16)
        .slice(2)
    window.localStorage.setItem(key, next)
    return next
  } catch (error) {
    return 'vm-chat-' + sessionVersion + '-' + Date.now().toString(36)
  }
}

function loadChatPanelWidthRatio() {
  try {
    const value = Number(window.localStorage.getItem(CHAT_PANEL_WIDTH_RATIO_KEY))
    return value > 0 && value < 1 ? value : null
  } catch (error) {
    return null
  }
}

function shouldShowChatResizeHint() {
  try {
    return window.localStorage.getItem(CHAT_RESIZER_HINT_SEEN_KEY) !== '1'
  } catch (error) {
    return false
  }
}

function clone(value) {
  if (value === null || typeof value !== 'object') return value
  if (Array.isArray(value)) return value.map(item => clone(item))
  const next = {}
  Object.keys(value).forEach(key => {
    next[key] = clone(value[key])
  })
  return next
}

function normalizeReportTocPosition(value) {
  const left = Number(value && value.left)
  const top = Number(value && value.top)
  return {
    left: Number.isFinite(left) ? Math.max(0, left) : DEFAULT_REPORT_TOC_POSITION.left,
    top: Number.isFinite(top) ? Math.max(0, top) : DEFAULT_REPORT_TOC_POSITION.top
  }
}

function normalizeGlobalQueryParams(value) {
  const source = value && typeof value === 'object' ? value : {}
  return Object.assign({}, DEFAULT_GLOBAL_QUERY_PARAMS, {
    beginDate: String(source.beginDate || '').trim(),
    endDate: String(source.endDate || '').trim(),
    productCode: String(source.productCode || source.fundCode || '').trim(),
    dataFreqOpen: 'true',
    benchmarks: ['0', '1', '2'].includes(String(source.benchmarks || '')) ? String(source.benchmarks) : '0',
    benchmarkA: String(source.benchmarkA || '').trim(),
    benchmarkB: String(source.benchmarkB || '').trim(),
    dataFreq: String(source.dataFreq || '日频').trim()
  })
}

function toCompactDate(value) {
  return String(value || '').trim().replace(/-/g, '')
}

function toDisplayDate(value) {
  const text = String(value || '').trim()
  if (/^\d{8}$/.test(text)) return text.slice(0, 4) + '-' + text.slice(4, 6) + '-' + text.slice(6, 8)
  return text
}

function loadReportTocPosition() {
  try {
    const cached = window.localStorage.getItem(REPORT_TOC_POSITION_KEY)
    if (!cached) return Object.assign({}, DEFAULT_REPORT_TOC_POSITION)
    const parsed = JSON.parse(cached)
    if (!parsed || !Number.isFinite(Number(parsed.left)) || !Number.isFinite(Number(parsed.top))) {
      return Object.assign({}, DEFAULT_REPORT_TOC_POSITION)
    }
    return normalizeReportTocPosition(parsed)
  } catch (error) {
    return Object.assign({}, DEFAULT_REPORT_TOC_POSITION)
  }
}

function hasStoredReportTocPosition() {
  try {
    const cached = window.localStorage.getItem(REPORT_TOC_POSITION_KEY)
    if (!cached) return false
    const parsed = JSON.parse(cached)
    return Boolean(parsed && Number.isFinite(Number(parsed.left)) && Number.isFinite(Number(parsed.top)))
  } catch (error) {
    return false
  }
}

function reviveBlockRenderSpec(block) {
  if (!block || !block.dsl || !block.renderSpec) return block
  try {
    const revived = createVmReportBlock({
      blockId: block.blockId,
      title: block.title,
      dsl: block.dsl,
      createdAt: block.createdAt,
      updatedAt: block.updatedAt,
      renderState: block.renderState
    })
    const next = Object.assign({}, block, {
      renderSpec: revived.renderSpec
    })
    if (block.type === 'table' && block.renderSpec && Array.isArray(block.renderSpec.rows)) {
      next.renderSpec.rows = clone(block.renderSpec.rows)
    }
    if (block.type === 'echarts' && block.renderSpec && block.renderSpec.option && block.renderSpec.option.dataset) {
      next.renderSpec.option.dataset.source = clone(block.renderSpec.option.dataset.source || [])
    }
    return next
  } catch (error) {
    return block
  }
}

function reviveBlocksById(blocksById) {
  const source = blocksById && typeof blocksById === 'object' ? blocksById : {}
  return Object.keys(source).reduce((accumulator, blockId) => {
    accumulator[blockId] = reviveBlockRenderSpec(source[blockId])
    return accumulator
  }, {})
}

function reviveGroupsById(groupsById) {
  const source = groupsById && typeof groupsById === 'object' ? groupsById : {}
  return Object.keys(source).reduce((accumulator, groupId) => {
    const group = source[groupId]
    accumulator[groupId] =
      group && typeof group === 'object'
        ? Object.assign({}, group, {
            blocksById: reviveBlocksById(group.blocksById)
          })
        : group
    return accumulator
  }, {})
}

function normalizeLayoutItems(layout) {
  return (Array.isArray(layout) ? layout : [])
    .map(item => ({
      i: String((item && item.i) || ''),
      x: Number((item && item.x) || 0),
      y: Number((item && item.y) || 0),
      w: Number((item && item.w) || 0),
      h: Number((item && item.h) || 0),
      minW: Number((item && item.minW) || 0),
      minH: Number((item && item.minH) || 0)
    }))
    .sort((left, right) => {
      if (left.i !== right.i) return left.i.localeCompare(right.i)
      if (left.y !== right.y) return left.y - right.y
      return left.x - right.x
    })
}

function isSameLayout(left, right) {
  const a = normalizeLayoutItems(left)
  const b = normalizeLayoutItems(right)
  if (a.length !== b.length) return false
  for (let index = 0; index < a.length; index += 1) {
    const current = a[index]
    const next = b[index]
    if (
      current.i !== next.i ||
      current.x !== next.x ||
      current.y !== next.y ||
      current.w !== next.w ||
      current.h !== next.h ||
      current.minW !== next.minW ||
      current.minH !== next.minH
    ) {
      return false
    }
  }
  return true
}

function normalizeTemplateRecord(template) {
  const normalized = Object.assign(
    {
      id:
        'vm-template-' +
        Date.now().toString(36) +
        '-' +
        Math.random()
          .toString(16)
          .slice(2, 8),
      title: '未命名模块',
      entityType: 'vm-block-template',
      payload: {},
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      updatedBy: DEFAULT_TEMPLATE_UPDATED_BY
    },
    clone(template || {})
  )
  normalized.updatedBy = String(normalized.updatedBy || DEFAULT_TEMPLATE_UPDATED_BY).trim() || DEFAULT_TEMPLATE_UPDATED_BY
  return normalized
}

export default {
  name: 'VmChatIndex',
  components: {
    myChart,
    GridLayout,
    GridItem,
    ProductSelectInput
  },
  data() {
    const protocolVersion = getVmProtocolVersion()
    return {
      analysisModel: DEFAULT_HERMES_ANALYSIS_MODEL,
      wikiDialogVisible: false,
      wikiTree: [],
      wikiSelectedPath: '',
      wikiDocument: null,
      wikiTreeFilter: '',
      wikiSearchQuery: '',
      wikiSearchMatchCount: 0,
      wikiSearchMatchIndex: 0,
      wikiTreeLoading: false,
      wikiDocumentLoading: false,
      wikiTreeError: '',
      wikiError: '',
      wikiRequestSequence: 0,
      protocolVersion,
      vmRequestFetcher: createVmRequestFetcher(),
      vmParamResolver: createVmParamResolver(createVmDictionaryLoader()),
      chatMessages: [],
      blocksById: {},
      groupsById: {},
      gridWidgets: [],
      reportNotices: [],
      savedTemplates: [],
      draftMessage: '',
      selectedBlockId: '',
      selectedBlockIds: [],
      activeBlockId: '',
      editingBlockTitleId: '',
      editingBlockTitleValue: '',
      exportingPdf: false,
      sending: false,
      moduleSidebarCollapsed: false,
      sidebarContentEntering: false,
      sidebarContentEnterTimer: null,
      viewportWidth: typeof window === 'undefined' ? 0 : window.innerWidth,
      chatPanelWidth: CHAT_PANEL_MIN_WIDTH,
      chatPanelWidthRatio: loadChatPanelWidthRatio(),
      chatResizeState: null,
      showChatResizeHint: shouldShowChatResizeHint(),
      chatResizeHintTimer: null,
      renderType: 'chat',
      renderMessage: '在右侧输入问题，vmChat 会生成可执行的报告块协议。',
      clarifyQuestions: [],
      tocCollapsed: true,
      reportTocPosition: loadReportTocPosition(),
      reportTocPositionCustomized: hasStoredReportTocPosition(),
      tocDragState: null,
      tocDragMoved: false,
      tocSnapping: false,
      tocSnapTimer: null,
      tocDragBlockId: '',
      tocDragTargetId: '',
      sessionId: createSessionId(protocolVersion),
      lastPayload: null,
      layoutEditable: false,
      blockSearchQuery: '',
      templateSearchQuery: '',
      globalQueryProduct: null,
      globalProductSelectorVisible: false,
      globalQueryDataFreqOptions: [],
      globalQueryBenchmarkOptions: [],
      globalQueryOptionsLoading: false,
      globalQueryParams: normalizeGlobalQueryParams(),
      globalQueryTouched: false,
      showGlobalQueryMore: false,
      globalQueryApplying: false,
      showExampleEntry: SHOW_EXAMPLE_ENTRY,
      showExamplePanel: false,
      exampleQuestions: buildCatalogExampleQuestions(),
      chartResizeTimer: null,
      messageScrollTimer: null,
      messageScrollSettleTimer: null,
      messageListPinnedToBottom: true,
      messageListAutoFollow: true,
      messageListLastScrollTop: 0,
      failedUpdateOperation: null
    }
  },
  computed: {
    reportBlocks() {
      return getOrderedBlocks(this.getCanvasState())
    },
    topLevelViewItems() {
      return getOrderedTopLevelItems(this.getCanvasState())
    },
    chartBlockCount() {
      return this.reportBlocks.filter(item => item.type === 'echarts').length
    },
    tableBlockCount() {
      return this.reportBlocks.filter(item => item.type === 'table').length
    },
    filteredBlocks() {
      const q = (this.blockSearchQuery || '').trim().toLowerCase()
      if (!q) return this.reportBlocks
      return this.reportBlocks.filter(block => {
        const title = this.getBlockDisplayTitle(block).toLowerCase()
        return title.indexOf(q) !== -1
      })
    },
    reportTocItems() {
      return this.topLevelViewItems.map(item => {
        if (item.kind === 'group') {
          return {
            entityKey: item.widget.i,
            kind: 'group',
            title: item.group.title || '未命名组合',
            blockIds: getOrderedGroupBlocks(item.group).map(block => block.blockId)
          }
        }
        return {
          entityKey: item.widget.i,
          kind: 'block',
          title: this.getBlockDisplayTitle(item.block),
          blockIds: [item.block.blockId]
        }
      })
    },
    filteredReportTocItems() {
      const query = String(this.blockSearchQuery || '').trim().toLowerCase()
      if (!query) return this.reportTocItems
      return this.reportTocItems.filter(item => item.title.toLowerCase().indexOf(query) !== -1)
    },
    selectedBlockTitle() {
      const matched = this.getBlockById(this.selectedBlockId)
      return matched ? this.getBlockDisplayTitle(matched) : ''
    },
    canMergeSelectedBlocks() {
      return this.getMergeableSelectedBlockIds().length >= 2
    },
    filteredSavedTemplates() {
      const q = (this.templateSearchQuery || '').trim().toLowerCase()
      if (!q) return this.savedTemplates
      return this.savedTemplates.filter(t => {
        const title = (t.title || '').toLowerCase()
        const typeLabel = this.getTemplateTypeLabel(t).toLowerCase()
        return title.indexOf(q) !== -1 || typeLabel.indexOf(q) !== -1
      })
    },
    globalQueryMoreCount() {
      const params = this.globalQueryParams || DEFAULT_GLOBAL_QUERY_PARAMS
      let count = 1
      if (params.benchmarks && params.benchmarks !== '0') count += 1
      if (params.benchmarkA) count += 1
      if (params.benchmarkB) count += 1
      return count
    },
    reportTocStyle() {
      if (!this.tocCollapsed || !this.reportTocPositionCustomized) return null
      return {
        left: this.reportTocPosition.left + 'px',
        top: this.reportTocPosition.top + 'px',
        right: 'auto',
        bottom: 'auto'
      }
    },
    chatLayoutStyle() {
      if (this.viewportWidth <= 1280) return null
      const sidebarColumn = this.moduleSidebarCollapsed ? '0px ' : '338px '
      return {
        gridTemplateColumns: sidebarColumn + 'minmax(0, 1fr) ' + CHAT_RESIZER_WIDTH + 'px ' + Math.round(this.chatPanelWidth) + 'px'
      }
    }
  },
  watch: {
    wikiTreeFilter(value) {
      const tree = this.$refs.wikiTreeView
      if (tree && tree.filter) tree.filter(value)
    },
    moduleSidebarCollapsed(collapsed) {
      this.$nextTick(() => this.syncChatPanelWidth())
      if (collapsed) return
      if (this.sidebarContentEnterTimer) window.clearTimeout(this.sidebarContentEnterTimer)
      this.sidebarContentEntering = true
      this.sidebarContentEnterTimer = window.setTimeout(() => {
        this.sidebarContentEntering = false
        this.sidebarContentEnterTimer = null
      }, 180)
    }
  },
  created() {
    this.syncCanvasState(createCanvasStateFromBlocks([]))
    this.loadSavedTemplates()
  },
  mounted() {
    window.addEventListener('resize', this.handleReportTocViewportResize)
    window.addEventListener('resize', this.handleChatPanelViewportResize)
    this.handleReportTocViewportResize()
    this.handleChatPanelViewportResize()
    this.scheduleChatResizeHint()
    this.loadGlobalQueryOptions()
    this.loadWikiTree()
  },
  beforeDestroy() {
    if (this.chartResizeTimer) {
      window.cancelAnimationFrame(this.chartResizeTimer)
      this.chartResizeTimer = null
    }
    if (this.messageScrollTimer) {
      window.cancelAnimationFrame(this.messageScrollTimer)
      this.messageScrollTimer = null
    }
    if (this.messageScrollSettleTimer) {
      window.clearTimeout(this.messageScrollSettleTimer)
      this.messageScrollSettleTimer = null
    }
    if (this.tocSnapTimer) {
      window.clearTimeout(this.tocSnapTimer)
      this.tocSnapTimer = null
    }
    if (this.chatResizeHintTimer) {
      window.clearTimeout(this.chatResizeHintTimer)
      this.chatResizeHintTimer = null
    }
    if (this.sidebarContentEnterTimer) {
      window.clearTimeout(this.sidebarContentEnterTimer)
      this.sidebarContentEnterTimer = null
    }
    this.stopReportTocDrag()
    this.stopChatResize()
    window.removeEventListener('resize', this.handleReportTocViewportResize)
    window.removeEventListener('resize', this.handleChatPanelViewportResize)
  },
  methods: {
    setWikiDialogWidth() {
      this.$nextTick(() => {
        const dialog = this.$refs.wikiDialog && this.$refs.wikiDialog.$el.querySelector('.wiki-dialog')
        if (dialog) dialog.style.setProperty('width', '80vw', 'important')
      })
    },
    collapseReportTocOnOutsideClick(event) {
      if (this.tocCollapsed || !event || !event.target || event.target.closest('.report-toc')) return
      this.tocCollapsed = true
    },
    renderMarkdown(value) {
      return markdownToSafeHtml(value)
    },
    renderWikiMarkdown(value) {
      return renderWikiMarkdown(value)
    },
    renderHighlightedWikiMarkdown(value) {
      return highlightWikiHtml(renderWikiMarkdown(value), this.wikiSearchQuery)
    },
    filterWikiTreeNode(value, node) {
      const query = String(value || '').trim().toLowerCase()
      if (!query) return true
      const matchesNode = current => {
        if (!current) return false
        const label = String(current.displayName || current.name || '').toLowerCase()
        return label.indexOf(query) !== -1 || (current.children || []).some(matchesNode)
      }
      return matchesNode(node)
    },
    resetWikiSearch() {
      this.wikiSearchMatchIndex = 0
      this.$nextTick(() => {
        this.syncWikiSearchMatches(true)
      })
    },
    syncWikiSearchMatches(scrollToCurrent) {
      const content = this.$refs.wikiContent
      const matches = content ? Array.from(content.querySelectorAll('.wiki-search-match')) : []
      this.wikiSearchMatchCount = matches.length
      if (!matches.length) {
        this.wikiSearchMatchIndex = 0
        return
      }
      this.wikiSearchMatchIndex = Math.min(this.wikiSearchMatchIndex, matches.length - 1)
      matches.forEach((match, index) => match.classList.toggle('is-current', index === this.wikiSearchMatchIndex))
      if (scrollToCurrent) matches[this.wikiSearchMatchIndex].scrollIntoView({ block: 'center', behavior: 'smooth' })
    },
    findNextWikiMatch() {
      if (!this.wikiSearchMatchCount) return
      this.wikiSearchMatchIndex = (this.wikiSearchMatchIndex + 1) % this.wikiSearchMatchCount
      this.syncWikiSearchMatches(true)
    },
    findPreviousWikiMatch() {
      if (!this.wikiSearchMatchCount) return
      this.wikiSearchMatchIndex = (this.wikiSearchMatchIndex - 1 + this.wikiSearchMatchCount) % this.wikiSearchMatchCount
      this.syncWikiSearchMatches(true)
    },
    openWikiDialog() {
      this.wikiDialogVisible = true
      if (!this.wikiTree.length && !this.wikiTreeLoading) {
        this.loadWikiTree()
      } else if (this.wikiTree.length && !this.wikiDocument && !this.wikiDocumentLoading) {
        const first = this.findFirstFileNode(this.wikiTree)
        if (first) {
          this.selectWikiDocument(first)
        }
      }
    },
    loadWikiTree() {
      this.wikiTreeLoading = true
      this.wikiTreeError = ''
      fetchHermesWikiTree()
        .then((res) => {
          this.wikiTreeLoading = false
          this.wikiTree = this.prepareWikiTree((res && res.tree) || [])
          this.$nextTick(() => {
            const tree = this.$refs.wikiTreeView
            if (tree && tree.filter) tree.filter(this.wikiTreeFilter)
          })
          if (!this.wikiSelectedPath) {
            const first = this.findFirstFileNode(this.wikiTree)
            if (first) {
              this.selectWikiDocument(first)
            }
          }
        })
        .catch((err) => {
          this.wikiTreeLoading = false
          this.wikiTreeError = (err && err.message) || '加载 Wiki 目录失败'
        })
    },
    prepareWikiTree(nodes) {
      return (nodes || []).map(node => ({
        ...node,
        displayName: node.title || node.name,
        children: node.children ? this.prepareWikiTree(node.children) : undefined
      }))
    },
    getWikiDocumentTitle(markdown) {
      const frontmatter = splitMarkdownFrontmatter(markdown).frontmatter
      const match = frontmatter.match(/^title:\s*(?:["']([^"']+)["']|(.+?))\s*$/m)
      return ((match && (match[1] || match[2])) || '').trim()
    },
    syncWikiTreeTitles(markdown) {
      const titlesByDocumentId = {}
      String(markdown || '').split(/\r?\n/).forEach(line => {
        const match = line.match(/^\|\s*\[([^\]]+)\]\([^)]*\)\s*\|\s*([^|]+)\|/)
        if (match) titlesByDocumentId[match[1].trim()] = match[2].trim()
      })
      const updateNodes = nodes => {
        const list = nodes || []
        list.forEach(node => {
          const title = titlesByDocumentId[node.documentId]
          if (title) this.$set(node, 'displayName', title)
          if (node.children) updateNodes(node.children)
        })
      }
      updateNodes(this.wikiTree)
    },
    syncWikiTreeNodeTitle(node, markdown) {
      const title = this.getWikiDocumentTitle(markdown)
      if (title) this.$set(node, 'displayName', title)
      if (node && node.documentId === 'index') this.syncWikiTreeTitles(markdown)
    },
    findFirstFileNode(nodes) {
      for (const node of nodes || []) {
        if (node.documentId) return node
        if (node.children && node.children.length) {
          const found = this.findFirstFileNode(node.children)
          if (found) return found
        }
      }
      return null
    },
    handleWikiNodeClick(node) {
      if (node && node.documentId) {
        this.selectWikiDocument(node)
      }
    },
    handleWikiDocumentLink(event) {
      const link = event && event.target && event.target.closest && event.target.closest('a[href]')
      if (!link || !event.currentTarget || !event.currentTarget.contains(link)) return
      const node = this.findWikiNodeByLink(link.getAttribute('href'))
      if (!node) return
      event.preventDefault()
      this.selectWikiDocument(node)
    },
    findWikiNodeByLink(href) {
      const target = String(href || '').trim()
      if (!target || /^(?:[a-z][a-z\d+.-]*:|\/\/|#)/i.test(target)) return null
      const relativePath = target.split(/[?#]/, 1)[0]
      if (!/\.md$/i.test(relativePath)) return null
      const currentPath = String((this.wikiDocument && this.wikiDocument.path) || '')
      const baseParts = currentPath.split('/').slice(0, -1)
      const pathParts = (relativePath.charAt(0) === '/' ? [] : baseParts).concat(relativePath.split('/'))
      const normalizedParts = []
      for (const part of pathParts) {
        if (!part || part === '.') continue
        if (part === '..') {
          normalizedParts.pop()
        } else {
          normalizedParts.push(part)
        }
      }
      return this.findNodeByPath(this.wikiTree, normalizedParts.join('/'))
    },
    selectWikiDocument(node) {
      if (!node || !node.documentId) return
      this.wikiSelectedPath = node.path
      this.$nextTick(() => {
        const tree = this.$refs.wikiTreeView
        if (tree && tree.setCurrentKey) tree.setCurrentKey(node.path)
      })
      this.wikiDocument = null
      this.wikiError = ''
      this.wikiDocumentLoading = true
      const seq = ++this.wikiRequestSequence
      fetchHermesWikiDocument(node.documentId)
        .then((res) => {
          this.syncWikiTreeNodeTitle(node, res && res.markdown)
          if (seq === this.wikiRequestSequence) {
            this.wikiDocument = res
            this.wikiDocumentLoading = false
            this.$nextTick(() => this.syncWikiSearchMatches(false))
          }
        })
        .catch((err) => {
          if (seq === this.wikiRequestSequence) {
            this.wikiDocumentLoading = false
            this.wikiError = (err && err.message) || '加载文档失败'
          }
        })
    },
    retryWikiLoad() {
      if (!this.wikiTree.length || this.wikiTreeError) {
        this.loadWikiTree()
      } else if (this.wikiSelectedPath) {
        const node = this.findNodeByPath(this.wikiTree, this.wikiSelectedPath)
        if (node) {
          this.selectWikiDocument(node)
        }
      }
    },
    findNodeByPath(nodes, path) {
      for (const node of nodes || []) {
        if (node.path === path) return node
        if (node.children && node.children.length) {
          const found = this.findNodeByPath(node.children, path)
          if (found) return found
        }
      }
      return null
    },
    scheduleChatResizeHint() {
      if (!this.showChatResizeHint || this.viewportWidth <= 1280) return
      this.chatResizeHintTimer = window.setTimeout(() => this.dismissChatResizeHint(), 2800)
    },
    dismissChatResizeHint() {
      if (!this.showChatResizeHint) return
      this.showChatResizeHint = false
      if (this.chatResizeHintTimer) {
        window.clearTimeout(this.chatResizeHintTimer)
        this.chatResizeHintTimer = null
      }
      try {
        window.localStorage.setItem(CHAT_RESIZER_HINT_SEEN_KEY, '1')
      } catch (error) {
        // Ignore storage restrictions; the hint will appear again next time.
      }
    },
    getChatPanelAvailableWidth() {
      const page = this.$el
      if (!page || this.viewportWidth <= 1280) return 0
      const pageStyle = window.getComputedStyle(page)
      const horizontalPadding = parseFloat(pageStyle.paddingLeft || 0) + parseFloat(pageStyle.paddingRight || 0)
      const sidebarWidth = this.moduleSidebarCollapsed ? 0 : 338
      return Math.max(0, page.clientWidth - horizontalPadding - sidebarWidth - CHAT_RESIZER_WIDTH - CHAT_LAYOUT_GAP * 3)
    },
    getChatPanelWidthBounds() {
      const availableWidth = this.getChatPanelAvailableWidth()
      const max = Math.min(CHAT_PANEL_MAX_WIDTH, Math.max(CHAT_PANEL_MIN_WIDTH, Math.floor(availableWidth / 3)))
      return { min: CHAT_PANEL_MIN_WIDTH, max }
    },
    clampChatPanelWidth(width) {
      const bounds = this.getChatPanelWidthBounds()
      return Math.max(bounds.min, Math.min(bounds.max, Math.round(width)))
    },
    syncChatPanelWidth() {
      const availableWidth = this.getChatPanelAvailableWidth()
      if (!availableWidth) return
      const preferredRatio = this.chatPanelWidthRatio || CHAT_PANEL_DEFAULT_RATIO
      this.chatPanelWidth = this.clampChatPanelWidth(availableWidth * preferredRatio)
    },
    persistChatPanelWidthRatio() {
      const availableWidth = this.getChatPanelAvailableWidth()
      if (!availableWidth) return
      this.chatPanelWidthRatio = this.chatPanelWidth / availableWidth
      try {
        window.localStorage.setItem(CHAT_PANEL_WIDTH_RATIO_KEY, String(this.chatPanelWidthRatio))
      } catch (error) {
        // Ignore storage restrictions; the width remains available in the current page.
      }
    },
    handleChatPanelViewportResize() {
      this.viewportWidth = window.innerWidth
      this.$nextTick(() => this.syncChatPanelWidth())
    },
    startChatResize(event) {
      if (this.viewportWidth <= 1280 || event.button !== 0) return
      this.dismissChatResizeHint()
      this.chatResizeState = {
        pointerId: event.pointerId,
        startX: event.clientX,
        startWidth: this.chatPanelWidth
      }
      if (event.currentTarget && event.currentTarget.setPointerCapture) event.currentTarget.setPointerCapture(event.pointerId)
      document.body.classList.add('is-vm-chat-resizing')
      window.addEventListener('pointermove', this.handleChatResizeMove)
      window.addEventListener('pointerup', this.stopChatResize)
      window.addEventListener('pointercancel', this.stopChatResize)
    },
    handleChatResizeMove(event) {
      const state = this.chatResizeState
      if (!state || event.pointerId !== state.pointerId) return
      this.chatPanelWidth = this.clampChatPanelWidth(state.startWidth - (event.clientX - state.startX))
      this.scheduleChartResize()
    },
    stopChatResize(event) {
      const state = this.chatResizeState
      if (!state) return
      if (event && event.pointerId != null && event.pointerId !== state.pointerId) return
      const resizer = this.$refs.chatResizer
      if (resizer && resizer.releasePointerCapture && resizer.hasPointerCapture && resizer.hasPointerCapture(state.pointerId)) {
        resizer.releasePointerCapture(state.pointerId)
      }
      this.chatResizeState = null
      document.body.classList.remove('is-vm-chat-resizing')
      window.removeEventListener('pointermove', this.handleChatResizeMove)
      window.removeEventListener('pointerup', this.stopChatResize)
      window.removeEventListener('pointercancel', this.stopChatResize)
      this.persistChatPanelWidthRatio()
      this.scheduleChartResize()
    },
    handleChatResizeKeydown(event) {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return
      event.preventDefault()
      const step = event.shiftKey ? 48 : 16
      const direction = event.key === 'ArrowLeft' ? 1 : -1
      this.chatPanelWidth = this.clampChatPanelWidth(this.chatPanelWidth + direction * step)
      this.persistChatPanelWidthRatio()
      this.scheduleChartResize()
    },
    toGlobalQueryOptionLabel(value, options) {
      const text = String(value || '').trim()
      if (!text) return ''
      const matched = (Array.isArray(options) ? options : []).find(option => {
        return String(option.code || '').trim() === text || String(option.label || '').trim() === text
      })
      return matched ? matched.label : text
    },
    async loadGlobalQueryOptions() {
      this.globalQueryOptionsLoading = true
      try {
        const results = await Promise.all([
          fetchVmDataFrequencyOptions().catch(() => []),
          fetchVmBenchmarkOptions().catch(() => [])
        ])
        this.globalQueryDataFreqOptions = Array.isArray(results[0]) ? results[0] : []
        this.globalQueryBenchmarkOptions = Array.isArray(results[1]) ? results[1] : []
        if (this.globalQueryDataFreqOptions.length) {
          this.globalQueryParams.dataFreq = this.toGlobalQueryOptionLabel(
            this.globalQueryParams.dataFreq,
            this.globalQueryDataFreqOptions
          ) || this.globalQueryDataFreqOptions[0].label
        }
        if (this.globalQueryBenchmarkOptions.length) {
          this.globalQueryParams.benchmarkA = this.toGlobalQueryOptionLabel(
            this.globalQueryParams.benchmarkA,
            this.globalQueryBenchmarkOptions
          )
          this.globalQueryParams.benchmarkB = this.toGlobalQueryOptionLabel(
            this.globalQueryParams.benchmarkB,
            this.globalQueryBenchmarkOptions
          )
        }
      } finally {
        this.globalQueryOptionsLoading = false
      }
    },
    handleGlobalProductSelect(product) {
      const nextProduct = product || null
      this.globalQueryProduct = nextProduct
      this.globalQueryParams.productCode = String(nextProduct && (nextProduct.VC_FUNDCODE || nextProduct.fundCode) || '').trim()
      this.globalQueryTouched = true
    },
    handleGlobalProductClear() {
      this.globalQueryProduct = null
      this.globalQueryParams.productCode = ''
      this.globalQueryTouched = true
    },
    getReportTocPositionBounds() {
      const panel = this.$refs.renderPanel
      if (!panel) return { maxLeft: 0, maxTop: 0 }
      return {
        maxLeft: Math.max(0, panel.clientWidth - 30),
        maxTop: Math.max(0, panel.clientHeight - 30)
      }
    },
    clampReportTocPosition(position) {
      const bounds = this.getReportTocPositionBounds()
      const normalized = normalizeReportTocPosition(position)
      return {
        left: Math.min(bounds.maxLeft, normalized.left),
        top: Math.min(bounds.maxTop, normalized.top)
      }
    },
    persistReportTocPosition() {
      try {
        window.localStorage.setItem(REPORT_TOC_POSITION_KEY, JSON.stringify(this.reportTocPosition))
      } catch (error) {
        // Ignore storage restrictions; the position remains available in the current page.
      }
    },
    handleReportTocViewportResize() {
      if (!this.reportTocPositionCustomized) return
      const next = this.clampReportTocPosition(this.reportTocPosition)
      if (next.left !== this.reportTocPosition.left || next.top !== this.reportTocPosition.top) {
        this.reportTocPosition = next
        this.persistReportTocPosition()
      }
    },
    toggleReportTocFromCollapsed() {
      if (this.tocDragMoved) {
        this.tocDragMoved = false
        return
      }
      this.tocCollapsed = false
    },
    startReportTocDrag(event) {
      if (!this.tocCollapsed || !event) return
      const panel = this.$refs.renderPanel
      const target = event.currentTarget
      if (!panel || !target) return
      this.tocSnapping = false
      if (this.tocSnapTimer) {
        window.clearTimeout(this.tocSnapTimer)
        this.tocSnapTimer = null
      }
      const panelRect = panel.getBoundingClientRect()
      const targetRect = target.getBoundingClientRect()
      this.tocDragState = {
        startX: event.clientX,
        startY: event.clientY,
        offsetX: event.clientX - targetRect.left,
        offsetY: event.clientY - targetRect.top,
        panelLeft: panelRect.left,
        panelTop: panelRect.top
      }
      this.tocDragMoved = false
      window.addEventListener('pointermove', this.handleReportTocDrag)
      window.addEventListener('pointerup', this.stopReportTocDrag)
      window.addEventListener('pointercancel', this.stopReportTocDrag)
    },
    handleReportTocDrag(event) {
      if (!this.tocDragState || !event) return
      const drag = this.tocDragState
      if (Math.abs(event.clientX - drag.startX) > 3 || Math.abs(event.clientY - drag.startY) > 3) {
        this.tocDragMoved = true
      }
      if (!this.tocDragMoved) return
      this.reportTocPositionCustomized = true
      this.reportTocPosition = this.clampReportTocPosition({
        left: event.clientX - drag.panelLeft - drag.offsetX,
        top: event.clientY - drag.panelTop - drag.offsetY
      })
    },
    snapReportTocToEdge() {
      const bounds = this.getReportTocPositionBounds()
      const current = this.clampReportTocPosition(this.reportTocPosition)
      const left = current.left <= bounds.maxLeft / 2 ? 0 : bounds.maxLeft
      const next = { left, top: current.top }
      const changed = next.left !== current.left || next.top !== current.top
      this.tocSnapping = changed
      this.reportTocPosition = next
      this.persistReportTocPosition()
      if (this.tocSnapTimer) window.clearTimeout(this.tocSnapTimer)
      if (changed) {
        this.tocSnapTimer = window.setTimeout(() => {
          this.tocSnapping = false
          this.tocSnapTimer = null
        }, 220)
      }
    },
    stopReportTocDrag() {
      if (!this.tocDragState) return
      window.removeEventListener('pointermove', this.handleReportTocDrag)
      window.removeEventListener('pointerup', this.stopReportTocDrag)
      window.removeEventListener('pointercancel', this.stopReportTocDrag)
      this.tocDragState = null
      if (this.tocDragMoved) this.snapReportTocToEdge()
    },
    getCanvasState() {
      return {
        blocksById: this.blocksById,
        groupsById: this.groupsById,
        widgets: this.gridWidgets
      }
    },
    syncCanvasState(nextState) {
      this.blocksById = reviveBlocksById(clone(nextState && nextState.blocksById ? nextState.blocksById : {}))
      this.groupsById = reviveGroupsById(clone(nextState && nextState.groupsById ? nextState.groupsById : {}))
      this.gridWidgets = clone(nextState && nextState.widgets ? nextState.widgets : [])
      if (this.selectedBlockId && !this.getBlockById(this.selectedBlockId)) {
        this.selectedBlockId = ''
      }
      this.selectedBlockIds = this.selectedBlockIds.filter(blockId => !!this.getBlockById(blockId))
    },
    getGlobalQueryParamsForDsl() {
      const params = normalizeGlobalQueryParams(this.globalQueryParams)
      const next = {
        fundCode: params.productCode,
        beginDate: toCompactDate(params.beginDate),
        endDate: toCompactDate(params.endDate),
        dataFreqOpen: 'true',
        benchmarks: params.benchmarks,
        dataFreq: this.toGlobalQueryOptionLabel(params.dataFreq, this.globalQueryDataFreqOptions)
      }
      if (params.benchmarks === '1' || params.benchmarks === '2') {
        next.benchmarkA = this.toGlobalQueryOptionLabel(params.benchmarkA, this.globalQueryBenchmarkOptions)
      }
      if (params.benchmarks === '2') {
        next.benchmarkB = this.toGlobalQueryOptionLabel(params.benchmarkB, this.globalQueryBenchmarkOptions)
      }
      return next
    },
    validateGlobalQueryParams() {
      const params = normalizeGlobalQueryParams(this.globalQueryParams)
      if (!params.beginDate || !params.endDate || !params.productCode) {
        throw new Error('请先填写开始时间、结束时间和产品代码')
      }
      if (params.beginDate > params.endDate) {
        throw new Error('开始时间不能晚于结束时间')
      }
      if ((params.benchmarks === '1' || params.benchmarks === '2') && !params.benchmarkA) {
        throw new Error('请选择或填写基准一')
      }
      if (params.benchmarks === '2' && !params.benchmarkB) {
        throw new Error('请选择或填写基准二')
      }
      return params
    },
    syncGlobalQueryParamsFromBlock(block) {
      if (this.globalQueryTouched || !block || !block.dsl || !block.dsl.params) return
      const params = block.dsl.params
      this.globalQueryParams = normalizeGlobalQueryParams({
        beginDate: toDisplayDate(params.beginDate),
        endDate: toDisplayDate(params.endDate),
        productCode: params.fundCode,
        dataFreq: this.toGlobalQueryOptionLabel(params.dataFreq, this.globalQueryDataFreqOptions),
        benchmarks: params.benchmarks,
        benchmarkA: this.toGlobalQueryOptionLabel(params.benchmarkA, this.globalQueryBenchmarkOptions),
        benchmarkB: this.toGlobalQueryOptionLabel(params.benchmarkB, this.globalQueryBenchmarkOptions)
      })
      this.globalQueryProduct = params.fundCode
        ? { VC_FUNDCODE: params.fundCode, VC_FUNDNAME: params.fundCode }
        : null
    },
    handleGlobalBenchmarkModeChange(mode) {
      this.globalQueryTouched = true
      if (mode === '0') {
        this.globalQueryParams.benchmarkA = ''
        this.globalQueryParams.benchmarkB = ''
      } else if (mode === '1') {
        this.globalQueryParams.benchmarkB = ''
      }
    },
    mergeGlobalQueryParamsIntoBlock(block) {
      if (!block || !block.dsl || !this.globalQueryTouched) return block
      const next = clone(block)
      const globalParams = this.getGlobalQueryParamsForDsl()
      if (Object.prototype.hasOwnProperty.call(next.dsl, 'params')) {
        next.dsl.params = Object.assign({}, next.dsl.params || {}, globalParams)
        if (globalParams.benchmarks === '0') {
          delete next.dsl.params.benchmarkA
          delete next.dsl.params.benchmarkB
        } else if (globalParams.benchmarks === '1') {
          delete next.dsl.params.benchmarkB
        }
      }
      const queryContextParams = Object.assign({}, globalParams, next.dsl.params || {})
      next.queryContext = Object.assign({}, next.queryContext || {}, {
        fundCode: queryContextParams.fundCode || '',
        productCode: queryContextParams.fundCode || '',
        beginDate: queryContextParams.beginDate || '',
        endDate: queryContextParams.endDate || '',
        dateRange: queryContextParams.beginDate && queryContextParams.endDate ? [queryContextParams.beginDate, queryContextParams.endDate] : [],
        benchmarkA: queryContextParams.benchmarkA || '',
        benchmarkB: queryContextParams.benchmarkB || '',
        benchmarks: queryContextParams.benchmarks || '',
        dataFreq: queryContextParams.dataFreq || ''
      })
      return next
    },
    async applyGlobalQueryParams() {
      if (this.globalQueryApplying) return
      try {
        this.validateGlobalQueryParams()
      } catch (error) {
        if (this.$message && this.$message.warning) this.$message.warning(error.message)
        return
      }
      this.globalQueryTouched = true
      this.globalQueryApplying = true
      const traceId = createVmTraceId('vm-global-query')
      try {
        const blockIds = this.getAllBlockIds()
        const hydratedBlocks = await Promise.all(blockIds.map(blockId => {
          const block = this.mergeGlobalQueryParamsIntoBlock(this.getBlockById(blockId))
          return hydrateVmBlock(block, this.vmRequestFetcher, {
            traceId,
            dataMode: 'live',
            paramResolver: this.vmParamResolver,
            queryParams: this.getGlobalQueryParamsForDsl()
          })
        }))
        hydratedBlocks.forEach((block, index) => {
          if (block) this.updateBlockById(blockIds[index], block)
        })
        this.clearReportNotices()
        this.$nextTick(() => this.resizeCharts())
        if (this.$message && this.$message.success) this.$message.success(blockIds.length ? '通用查询条件已应用' : '通用查询条件已保存')
      } catch (error) {
        this.setReportNotice(buildVmReportNoticeFromError(error, { traceId }))
      } finally {
        this.globalQueryApplying = false
      }
    },
    getTemplateTypeLabel(template) {
      if (!template) return ''
      if (template.entityType === 'vm-grid-layout-template') return '布局模板'
      if (template.entityType === 'vm-group-template') return '组合模块'
      return '单模块'
    },
    getTemplateTagType(template) {
      if (!template) return 'success'
      if (template.entityType === 'vm-grid-layout-template') return 'info'
      if (template.entityType === 'vm-group-template') return 'warning'
      return 'success'
    },
    getTemplateUpdatedBy(template) {
      return String(template && template.updatedBy || DEFAULT_TEMPLATE_UPDATED_BY).trim() || DEFAULT_TEMPLATE_UPDATED_BY
    },
    getCurrentTemplateUser() {
      const userState = this.$store && this.$store.state && this.$store.state.user || {}
      const profile = userState.user && typeof userState.user === 'object' ? userState.user : {}
      const candidates = [
        userState.name,
        userState.userName,
        userState.nickName,
        profile.userName,
        profile.nickName,
        profile.name
      ]
      for (let index = 0; index < candidates.length; index += 1) {
        const name = String(candidates[index] || '').trim()
        if (name) return name
      }
      return DEFAULT_TEMPLATE_UPDATED_BY
    },
    getTemplateAuditFields() {
      return {
        updatedAt: new Date().toISOString(),
        updatedBy: this.getCurrentTemplateUser()
      }
    },
    formatTemplateDate(value) {
      const date = new Date(value)
      if (Number.isNaN(date.getTime())) return '-'
      const pad = number => String(number).padStart(2, '0')
      return date.getFullYear() + '/' +
        (date.getMonth() + 1) + '/' +
        date.getDate() + ' ' +
        pad(date.getHours()) + ':' +
        pad(date.getMinutes()) + ':' +
        pad(date.getSeconds())
    },
    async loadSavedTemplates() {
      try {
        const response = await window.fetch(MODULES_API_ROUTE, {
          method: 'GET',
          headers: buildHermesAuthHeaders()
        })
        if (!response.ok) throw new Error('模板接口读取失败：HTTP ' + response.status)
        const data = await response.json()
        const templates = data && data.templates ? data.templates : []
        this.savedTemplates = Array.isArray(templates) ? templates.map(normalizeTemplateRecord) : []
      } catch (error) {
        // Python 服务不可用时仍允许页面启动；读写均不回退到前端文件。
        logVmChatEvent('ui', 'template.load.failed', error, { level: 'warn' })
        this.savedTemplates = []
      }
    },
    async persistTemplateRecord(template, method, templateId) {
      const suffix = templateId ? '/' + encodeURIComponent(templateId) : ''
      const response = await window.fetch(MODULES_API_ROUTE + suffix, {
        method: method || 'POST',
        headers: buildHermesAuthHeaders({ 'Content-Type': 'application/json' }),
        body: JSON.stringify(template)
      })
      if (!response.ok) throw new Error('模板接口保存失败：HTTP ' + response.status)
      const data = await response.json()
      return normalizeTemplateRecord(data && data.template ? data.template : template)
    },
    async fetchTemplateRecord(templateId) {
      const response = await window.fetch(MODULES_API_ROUTE + '/' + encodeURIComponent(templateId), {
        method: 'GET',
        headers: buildHermesAuthHeaders()
      })
      if (!response.ok) throw new Error('模板接口读取失败：HTTP ' + response.status)
      const data = await response.json()
      return data && data.template ? normalizeTemplateRecord(data.template) : null
    },
    getBlockOrder(blockId) {
      const index = this.reportBlocks.findIndex(item => item.blockId === blockId)
      return index >= 0 ? index + 1 : '-'
    },
    getGroupBlockCount(group) {
      return Object.keys(group && group.blocksById ? group.blocksById : {}).length
    },
    getBlockById(blockId) {
      if (!blockId) return null
      if (this.blocksById[blockId]) return this.blocksById[blockId]
      const groupIds = Object.keys(this.groupsById || {})
      for (let index = 0; index < groupIds.length; index += 1) {
        const group = this.groupsById[groupIds[index]]
        if (group && group.blocksById && group.blocksById[blockId]) return group.blocksById[blockId]
      }
      return null
    },
    updateBlockById(blockId, nextBlock) {
      const location = findBlockLocation(this.getCanvasState(), blockId)
      if (!location) return
      if (location.container === 'top-level') {
        this.$set(this.blocksById, blockId, nextBlock)
        return
      }
      const group = this.groupsById[location.groupId]
      if (!group || !group.blocksById) return
      this.$set(group.blocksById, blockId, nextBlock)
    },
    getMergeableSelectedBlockIds() {
      return this.selectedBlockIds.filter(blockId => {
        const location = findBlockLocation(this.getCanvasState(), blockId)
        return location && location.container === 'top-level'
      })
    },
    async hydratePendingBlocks(blockIds, traceId) {
      const targets = Array.isArray(blockIds) ? blockIds.filter(Boolean) : []
      for (let index = 0; index < targets.length; index += 1) {
        const blockId = targets[index]
        const block = this.getBlockById(blockId)
        if (!block || !block.dsl) continue
        if (block.renderSpec && block.renderState && block.renderState.status && block.renderState.status !== 'idle') continue
        const hydrated = await hydrateVmBlock(block, this.vmRequestFetcher, {
          traceId,
          dataMode: 'example',
          paramResolver: this.vmParamResolver,
          queryParams: this.getGlobalQueryParamsForDsl()
        })
        this.updateBlockById(blockId, hydrated)
      }
      this.$nextTick(() => this.resizeCharts())
    },
    getWidgetIds() {
      return this.gridWidgets.map(item => item.i)
    },
    getAllBlockIds() {
      return this.reportBlocks.map(item => item.blockId)
    },
    async sendMessage() {
      const question = String(this.draftMessage || '').trim()
      if (!question || this.sending) return
      const requestReportBlocks = clone(this.reportBlocks)
      const requestSelectedBlockId = this.selectedBlockId
      const allowBatchUpdate = isExplicitVmBatchUpdateRequest(question)
      this.failedUpdateOperation = null
      const userMessage = createMessage('user', question)
      const traceId = createVmTraceId('vm-chat')
      const assistantMessage = createMessage('assistant', '正在处理...', {
        traceId,
        streamStatus: '正在创建 Hermes 任务...'
      })
      this.chatMessages.push(userMessage)
      this.chatMessages.push(assistantMessage)
      this.draftMessage = ''
      this.sending = true
      this.messageListAutoFollow = true
      this.messageListPinnedToBottom = true
      this.scrollMessagesToBottom(true)

      const messages = buildVmHermesMessages({
        historyMessages: this.chatMessages.filter(item => item.id !== assistantMessage.id && item.id !== userMessage.id).map(item => ({ role: item.role, content: item.content })),
        userInput: question,
        reportBlocks: requestReportBlocks,
        selectedBlockId: requestSelectedBlockId,
        sessionId: this.sessionId,
        globalQueryParams: this.getGlobalQueryParamsForDsl()
      })

      const metrics = {
        startedAt: Date.now(),
        transport: 'run-events'
      }
      let lastRawResponse = null
      let lastChunkLogAt = 0
      let streamContentBuffer = ''
      let streamPhase = 'run'
      logVmChatEvent(
        'ui',
        'send.start',
        {
          question,
          selectedBlockId: requestSelectedBlockId,
          reportBlockCount: requestReportBlocks.length,
          messageCount: messages.length,
          model: this.analysisModel,
          protocolVersion: this.protocolVersion
        },
        { traceId }
      )

      try {
        if (shouldUseHermesRunEvents()) {
          logVmChatEvent(
            'hermes',
            'run.create.start',
            {
              sessionId: this.sessionId,
              model: this.analysisModel
            },
            { traceId }
          )
          const streamResult = await sendHermesRunEvents(
            messages,
            {
              sessionId: this.sessionId,
              model: this.analysisModel,
              skills: ['vm-report-dsl']
            },
            {
              onRunCreated: run => {
                metrics.runId = (run && run.run_id) || ''
                this.updateAssistantMessage(assistantMessage, {
                  streamStatus: 'Hermes 任务已创建，正在接收事件流...'
                })
                this.scheduleMessagesScroll()
                logVmChatEvent('hermes', 'run.created', run, { traceId })
              },
              onHeaders: headers => {
                logVmChatEvent('hermes', 'run.headers', headers, { traceId })
              },
              onThinking: (_, allThinking) => {
                this.updateAssistantMessage(assistantMessage, {
                  thinking: allThinking,
                  thinkingExpanded: true
                })
                this.scheduleMessagesScroll()
              },
              onContent: (_, allContent) => {
                streamContentBuffer = allContent || streamContentBuffer
                this.updateAssistantMessage(assistantMessage, {
                  content: formatVmAssistantStreamingContent(streamContentBuffer, '正在生成可执行报告协议...')
                })
                this.scheduleMessagesScroll()
              },
              onEvent: payload => {
                const eventName = (payload && payload.event) || 'event'
                metrics.eventNames = metrics.eventNames || {}
                metrics.eventNames[eventName] = (metrics.eventNames[eventName] || 0) + 1
                if (eventName !== 'message.delta') {
                  logVmChatEvent('hermes', 'run.event', payload, { traceId })
                }
              },
              onTool: payload => {
                logVmChatEvent('hermes', 'tool.event', payload, { traceId })
              },
              onCompleted: payload => {
                logVmChatEvent('hermes', 'run.completed', payload, { traceId })
              },
              onChunk: state => {
                this.updateAssistantMessage(assistantMessage, {
                  streamStatus: '正在接收事件流...'
                })
                metrics.chunkCount = state.chunkCount
                this.scheduleMessagesScroll()
                if (state.chunkCount === 1 || state.chunkCount % 20 === 0 || Date.now() - lastChunkLogAt > 10000) {
                  lastChunkLogAt = Date.now()
                  logVmChatEvent('hermes', 'run.chunk', state, { traceId })
                }
              },
              onDone: state => {
                metrics.chunkCount = state.chunkCount
                metrics.eventCount = state.eventCount
                metrics.byteLength = state.byteLength
                logVmChatEvent('hermes', 'run.done', state, { traceId })
              }
            }
          )
          lastRawResponse = streamResult
          const streamContent = String(streamResult.content || streamContentBuffer || '')
          logVmChatEvent('hermes', 'run.result', streamResult, { traceId })
          streamPhase = 'parse'
          logVmChatEvent(
            'protocol',
            'parse.start',
            {
              contentLength: streamContent.length,
              contentPreview: streamContent.slice(0, 500)
            },
            { traceId }
          )
          const parsedPayload = parseVmHermesRenderPayload(streamContent, {
            traceId,
            stage: 'protocol.parse.run-result',
            logSuccess: true,
            reportBlocks: requestReportBlocks,
            allowBatchUpdate
          })
          logVmChatEvent('protocol', 'parse.success', parsedPayload.raw, { traceId })
          streamPhase = 'apply'
          await this.applyVmRenderPayload(parsedPayload, traceId)
          streamPhase = 'done'
          this.updateAssistantMessage(assistantMessage, {
            content: this.getAssistantDisplayContent(parsedPayload, ''),
            thinking: streamResult.thinking || parsedPayload.thinking || assistantMessage.thinking,
            streamStatus: '',
            thinkingExpanded: false,
            metricsSummary: this.formatMetricsSummary(metrics.startedAt, streamResult),
            debugPayload: this.buildMessageDebug(question, parsedPayload, streamResult, null, traceId)
          })
        } else {
          throw Object.assign(new Error('vmChat 新协议要求使用 Hermes run-events；当前环境未启用事件流'), {
            code: 'HERMES_RUN_EVENTS_DISABLED'
          })
        }
      } catch (streamError) {
        logVmChatEvent('hermes', 'run.error', streamError, { traceId, level: 'warn' })
        if (streamContentBuffer && streamPhase !== 'apply') {
          try {
            metrics.transport = 'run-events-buffer'
            this.updateAssistantMessage(assistantMessage, {
              streamStatus: '事件流已收到协议，正在直接解析...'
            })
            logVmChatEvent(
              'protocol',
              'parse.buffer.start',
              {
                contentLength: streamContentBuffer.length,
                originalError: streamError && streamError.message ? streamError.message : String(streamError || '')
              },
              { traceId }
            )
            const parsedPayload = parseVmHermesRenderPayload(streamContentBuffer, {
              traceId,
              stage: 'protocol.parse.buffer',
              logSuccess: true,
              reportBlocks: requestReportBlocks,
              allowBatchUpdate
            })
            logVmChatEvent('protocol', 'parse.buffer.success', parsedPayload.raw, { traceId })
            await this.applyVmRenderPayload(parsedPayload, traceId)
            this.updateAssistantMessage(assistantMessage, {
              content: this.getAssistantDisplayContent(parsedPayload, ''),
              thinking: parsedPayload.thinking || assistantMessage.thinking,
              streamStatus: '',
              thinkingExpanded: false,
              metricsSummary: this.formatMetricsSummary(metrics.startedAt, {
                chunkCount: metrics.chunkCount || 0
              }),
              debugPayload: this.buildMessageDebug(
                question,
                parsedPayload,
                {
                  recoveredFromStreamBuffer: true,
                  originalError: streamError && streamError.message ? streamError.message : String(streamError || ''),
                  content: streamContentBuffer
                },
                streamError,
                traceId
              )
            })
            return
          } catch (bufferError) {
            logVmChatEvent('protocol', 'parse.buffer.failed', bufferError, { traceId, level: 'warn' })
          }
        }
        metrics.transport = 'run-events-error'
        const finalError = streamError instanceof Error ? streamError : new Error(String(streamError || 'vmChat 请求失败'))
        this.failedUpdateOperation = finalError.retryOperation ? clone(finalError.retryOperation) : null
        logVmChatEvent('ui', 'send.error', finalError, { traceId, level: 'error' })
        this.updateAssistantMessage(assistantMessage, {
          content: finalError.message || 'vmChat 请求失败',
          streamStatus: '',
          thinkingExpanded: false,
          metricsSummary: '请求失败'
        })
        this.renderType = 'chat'
        this.renderMessage = assistantMessage.content
        this.clarifyQuestions = []
        this.updateAssistantMessage(assistantMessage, {
          debugPayload: this.buildMessageDebug(question, null, lastRawResponse, finalError, traceId)
        })
        this.setReportNotice(
          buildVmReportNoticeFromError(finalError, {
            traceId,
            debugPayload: assistantMessage.debugPayload
          })
        )
      } finally {
        logVmChatEvent(
          'ui',
          'send.done',
          {
            durationMs: Date.now() - metrics.startedAt,
            transport: metrics.transport,
            reportBlockCount: this.reportBlocks.length,
            error: assistantMessage.metricsSummary === '请求失败' ? assistantMessage.content : ''
          },
          { traceId }
        )
        this.sending = false
        this.scrollMessagesToBottom()
      }
    },
    async applyVmRenderPayload(payload, traceId) {
      logVmChatEvent(
        'render',
        'payload.apply.start',
        {
          renderType: payload.renderType,
          intent: payload.intent,
          message: payload.message,
          operationCount: Array.isArray(payload.operations) ? payload.operations.length : 0
        },
        { traceId }
      )
      this.renderType = payload.renderType
      this.renderMessage = payload.message || this.renderMessage
      if (payload.renderType !== 'report' && payload.message) {
        this.scrollReportToTop()
      }
      this.clarifyQuestions = []
      this.lastPayload = payload.raw
      if (payload.renderType === 'businessInfo') {
        this.clearReportNotices()
        return
      }
      if (payload.renderType === 'clarify') {
        this.clarifyQuestions = payload.clarify ? payload.clarify.questions : []
        this.setReportNotice(
          buildVmReportNoticeFromPayload(payload, {
            traceId,
            debugPayload: this.buildNoticeDebug(payload, null, null, traceId)
          })
        )
        return
      }
      if (payload.renderType !== 'report') {
        const notice = buildVmReportNoticeFromPayload(payload, {
          traceId,
          debugPayload: this.buildNoticeDebug(payload, null, null, traceId)
        })
        if (notice) this.setReportNotice(notice)
        else this.clearReportNotices()
        return
      }
      this.clearReportNotices()
      if (payload.operations.length > 1) {
        await this.applyBatchUpdateOperationsAtomically(payload.operations, traceId)
        this.$nextTick(() => this.resizeCharts())
        return
      }
      for (let index = 0; index < payload.operations.length; index += 1) {
        await this.applyReportOperation(payload.operations[index], traceId)
      }
      this.$nextTick(() => this.resizeCharts())
    },
    async applyBatchUpdateOperationsAtomically(operations, traceId) {
      const prepared = []
      for (let index = 0; index < operations.length; index += 1) {
        const operation = operations[index]
        assertVmHermesOperationAllowed(operation && operation.action)
        if (!operation || operation.action !== 'replaceBlock') {
          throw new Error('批量操作只允许完整 update DSL')
        }
        const targetBlockId = this.resolveReplaceBlockId(operation, operation.block)
        const block = await this.hydrateBlockIfNeeded(operation.block, traceId)
        assertVmUpdateHydrationSucceeded(block, operation)
        prepared.push({ targetBlockId, block })
      }

      let nextState = clone(this.getCanvasState())
      prepared.forEach(item => {
        const current = this.getBlockById(item.targetBlockId)
        if (!current || !current.dsl || current.dsl.id !== item.block.dsl.id) {
          throw new Error('批量 update 提交前目标状态已变化，请重新发起修改')
        }
        nextState = replaceBlockWidget(nextState, item.targetBlockId, item.block)
      })
      this.syncCanvasState(nextState)
      if (prepared.length) this.syncGlobalQueryParamsFromBlock(prepared[0].block)
      const lastTarget = prepared.length ? prepared[prepared.length - 1].targetBlockId : ''
      this.selectedBlockId = lastTarget
      this.selectedBlockIds = prepared.map(item => item.targetBlockId)
      this.activeBlockId = lastTarget
    },
    assertCreateBlockIsNew(block) {
      if (!block || !block.dsl || block.dsl.action !== 'create') {
        throw new Error('appendBlock 必须携带 create DSL')
      }
      const blockId = block.blockId
      const dslId = block.dsl.id
      const collision = this.reportBlocks.find(item => item && (
        item.blockId === blockId ||
        item.blockId === dslId ||
        item.dsl && (item.dsl.id === dslId || item.dsl.id === blockId)
      ))
      if (collision) {
        throw new Error('create ID 已存在，不允许覆盖已有报表块：' + collision.blockId)
      }
      return block
    },
    resolveReplaceBlockId(operation, block) {
      const targetBlockId = operation && operation.targetBlockId
      if (!targetBlockId) throw new Error('update 缺少明确 targetBlockId')
      const existing = this.getBlockById(targetBlockId)
      if (!existing) throw new Error('update 目标已不存在，请重新选择要更新的报表块')
      if (!block || !block.dsl || block.dsl.action !== 'update') {
        throw new Error('replaceBlock 必须携带 update DSL')
      }
      if (!existing.dsl || !block || !block.dsl || existing.dsl.id !== block.dsl.id) {
        throw new Error('update 的 DSL id 与目标报表块不一致')
      }
      return targetBlockId
    },
    async applyReportOperation(operation, traceId) {
      assertVmHermesOperationAllowed(operation && operation.action)
      if (operation.action === 'appendBlock') {
        this.assertCreateBlockIsNew(operation.block)
        const block = await this.hydrateBlockIfNeeded(operation.block, traceId)
        this.assertCreateBlockIsNew(block)
        this.syncGlobalQueryParamsFromBlock(block)
        const next = appendBlockWidget(this.getCanvasState(), block)
        this.syncCanvasState(next)
        this.selectedBlockId = block.blockId
        this.selectedBlockIds = this.selectedBlockId ? [this.selectedBlockId] : []
        this.activeBlockId = this.selectedBlockId
        return
      }
      if (operation.action === 'replaceBlock') {
        const targetBlockId = this.resolveReplaceBlockId(operation, operation.block)
        const block = await this.hydrateBlockIfNeeded(operation.block, traceId)
        assertVmUpdateHydrationSucceeded(block, operation)
        this.syncGlobalQueryParamsFromBlock(block)
        const next = replaceBlockWidget(this.getCanvasState(), targetBlockId, block)
        this.syncCanvasState(next)
        this.selectedBlockId = targetBlockId
        this.selectedBlockIds = this.selectedBlockId ? [this.selectedBlockId] : []
        this.activeBlockId = this.selectedBlockId
        return
      }
    },
    async hydrateBlockIfNeeded(block, traceId, dataMode) {
      if (block && block.dsl) {
        const previousDataMode = block.sourceData && block.sourceData.runtime && block.sourceData.runtime.dataMode
        const resolvedDataMode = dataMode === 'live' || dataMode === 'example'
          ? dataMode
          : previousDataMode === 'live' || previousDataMode === 'example'
            ? previousDataMode
            : 'example'
        return hydrateVmBlock(this.mergeGlobalQueryParamsIntoBlock(block), this.vmRequestFetcher, {
          traceId,
          dataMode: resolvedDataMode,
          paramResolver: this.vmParamResolver,
          queryParams: this.getGlobalQueryParamsForDsl()
        })
      }
      return block
    },
    async retryFailedUpdate() {
      if (this.sending || !this.failedUpdateOperation) return
      const operation = clone(this.failedUpdateOperation)
      const traceId = createVmTraceId('vm-update-retry')
      const assistantMessage = createMessage('assistant', '正在重试更新...', {
        traceId,
        streamStatus: '正在重新取数并渲染...'
      })
      this.chatMessages.push(assistantMessage)
      this.sending = true
      try {
        await this.applyReportOperation(operation, traceId)
        this.failedUpdateOperation = null
        this.clearReportNotices()
        const title = operation.block && operation.block.title
        this.updateAssistantMessage(assistantMessage, {
          content: title ? '已重试并更新报表块：' + title : '已重试并更新报表块。',
          streamStatus: '',
          metricsSummary: '重试成功'
        })
        this.$nextTick(() => this.resizeCharts())
      } catch (error) {
        this.failedUpdateOperation = error && error.retryOperation ? clone(error.retryOperation) : null
        const message = error && error.message ? error.message : '更新重试失败'
        this.updateAssistantMessage(assistantMessage, {
          content: message,
          streamStatus: '',
          metricsSummary: '重试失败'
        })
        this.setReportNotice(buildVmReportNoticeFromError(error, { traceId }))
      } finally {
        this.sending = false
        this.scrollMessagesToBottom()
      }
    },
    async retryBlock(blockId) {
      if (this.sending) return
      const original = this.getBlockById(blockId)
      if (!original || !original.dsl) return
      const traceId = createVmTraceId('vm-block-retry')
      const assistantMessage = createMessage('assistant', '正在重新加载报表块...', {
        traceId,
        streamStatus: '正在重新取数并渲染...'
      })
      this.chatMessages.push(assistantMessage)
      this.sending = true
      try {
        const hydrated = await this.hydrateBlockIfNeeded(original, traceId)
        if (hydrated && hydrated.renderState && hydrated.renderState.status === 'error') {
          throw new Error(hydrated.renderState.errorMessage || '报表块重新加载失败')
        }
        this.updateBlockById(blockId, hydrated)
        this.clearReportNotices()
        this.updateAssistantMessage(assistantMessage, {
          content: '已重新加载报表块：' + this.getBlockDisplayTitle(hydrated),
          streamStatus: '',
          metricsSummary: '重试成功'
        })
        this.$nextTick(() => this.resizeCharts())
      } catch (error) {
        const message = error && error.message ? error.message : '报表块重新加载失败'
        this.updateAssistantMessage(assistantMessage, {
          content: message,
          streamStatus: '',
          metricsSummary: '重试失败'
        })
        this.setReportNotice(buildVmReportNoticeFromError(error, { traceId }))
      } finally {
        this.sending = false
        this.scrollMessagesToBottom()
      }
    },
    handleGridLayoutUpdated(nextLayout) {
      if (!isSameLayout(this.gridWidgets, nextLayout)) {
        this.syncCanvasState(updateTopLevelWidgets(this.getCanvasState(), nextLayout || []))
      }
      this.activeBlockId = this.selectedBlockId || this.activeBlockId
      this.scheduleChartResize()
    },
    setTopLevelWidgetWidth(entityKey, width) {
      this.syncCanvasState(setTopLevelEntityWidth(this.getCanvasState(), entityKey, width))
      this.scheduleChartResize()
    },
    setGroupBlockWidth(groupId, blockId, width) {
      this.syncCanvasState(setGroupChildWidth(this.getCanvasState(), groupId, blockId, width))
      this.scheduleChartResize()
    },
    removeBlock(blockId) {
      this.syncCanvasState(removeBlockWidget(this.getCanvasState(), blockId))
      if (this.selectedBlockId === blockId) this.selectedBlockId = ''
      this.selectedBlockIds = this.selectedBlockIds.filter(id => id !== blockId)
    },
    handleBlockClick(blockId, event) {
      const multi = !!(event && (event.metaKey || event.ctrlKey))
      if (multi) {
        if (this.selectedBlockIds.includes(blockId)) {
          this.selectedBlockIds = this.selectedBlockIds.filter(id => id !== blockId)
        } else {
          this.selectedBlockIds = this.selectedBlockIds.concat(blockId)
        }
      } else {
        this.selectedBlockIds = [blockId]
      }
      this.selectedBlockId = blockId
      this.activeBlockId = blockId
    },
    toggleBlockSelection(blockId, checked) {
      if (checked && !this.selectedBlockIds.includes(blockId)) {
        this.selectedBlockIds = this.selectedBlockIds.concat(blockId)
      }
      if (!checked) {
        this.selectedBlockIds = this.selectedBlockIds.filter(id => id !== blockId)
      }
      if (checked) this.selectedBlockId = blockId
      if (!checked && this.selectedBlockId === blockId) {
        this.selectedBlockId = this.selectedBlockIds[0] || ''
      }
    },
    startBlockTitleEdit(block) {
      if (!block || !block.blockId) return
      this.editingBlockTitleId = block.blockId
      this.editingBlockTitleValue = this.getBlockDisplayTitle(block)
      this.$nextTick(() => {
        const ref = this.$refs['block-title-input-' + block.blockId]
        const input = Array.isArray(ref) ? ref[0] : ref
        if (input && typeof input.focus === 'function') input.focus()
      })
    },
    cancelBlockTitleEdit() {
      this.editingBlockTitleId = ''
      this.editingBlockTitleValue = ''
    },
    commitBlockTitleEdit(blockId) {
      if (this.editingBlockTitleId !== blockId) return
      const block = this.getBlockById(blockId)
      const title = String(this.editingBlockTitleValue || '').trim()
      if (!block) {
        this.cancelBlockTitleEdit()
        return
      }
      if (!title) {
        if (this.$message && this.$message.warning) this.$message.warning('标题不能为空')
        return
      }
      const next = clone(block)
      next.title = title
      if (next.dsl && typeof next.dsl === 'object') {
        if (!next.dsl.view || typeof next.dsl.view !== 'object') next.dsl.view = {}
        next.dsl.view.title = title
      }
      this.updateBlockById(blockId, next)
      this.cancelBlockTitleEdit()
    },
    async exportReportPdf() {
      if (this.exportingPdf) return
      const target = this.$refs.reportScroller
      if (!target) return
      if (!this.reportBlocks.length && !this.reportNotices.length) {
        if (this.$message && this.$message.warning) this.$message.warning('暂无可导出的报告内容')
        return
      }

      let exportHost = null
      this.exportingPdf = true

      try {
        const JsPDF = (await import('jspdf')).default
        const pdf = new JsPDF({
          compress: true,
          format: 'a4',
          orientation: 'landscape',
          unit: 'mm'
        })
        const pageWidth = pdf.internal.pageSize.getWidth()
        const pageHeight = pdf.internal.pageSize.getHeight()
        const margin = 8
        const imageWidth = pageWidth - margin * 2
        const pageContentHeight = pageHeight - margin * 2
        const fontFamily = '-apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif'
        const orderedBlocks = []
        this.topLevelViewItems.forEach(item => {
          if (item.kind === 'block') {
            if (item.block) orderedBlocks.push(item.block)
            return
          }
          getOrderedGroupBlocks(item.group).forEach(block => {
            if (block) orderedBlocks.push(block)
          })
        })
        const formatExportValue = (value, format) => {
          if (value === null || value === undefined || value === '') {
            return format && format.nullValue !== undefined ? format.nullValue : '-'
          }
          if (!format || !format.type || format.type === 'raw' || format.type === 'text' || format.type === 'date') {
            return String(value)
          }
          const numericValue = Number(value)
          if (isNaN(numericValue)) return String(value)
          if (format.type === 'decimal' || format.type === 'percentage') {
            const digits = format.digits !== undefined ? format.digits : 2
            return String(format.prefix || '') + numericValue.toFixed(digits) + String(format.suffix || '')
          }
          return String(format.prefix || '') + String(value) + String(format.suffix || '')
        }
        let hasPdfContent = false
        const beginBlockPage = () => {
          if (hasPdfContent) pdf.addPage()
          hasPdfContent = true
        }
        const loadImage = dataUrl => new Promise((resolve, reject) => {
          const image = new Image()
          image.onload = () => resolve(image)
          image.onerror = reject
          image.src = dataUrl
        })
        const addImagePages = async(dataUrl, sourceWidth, sourceHeight) => {
          const image = await loadImage(dataUrl)
          const scale = imageWidth / sourceWidth
          const maxSourceHeight = Math.max(1, Math.floor(pageContentHeight / scale))
          let sourceOffset = 0
          let firstSlice = true
          while (sourceOffset < sourceHeight) {
            if (!firstSlice) pdf.addPage()
            const sliceHeight = Math.min(maxSourceHeight, sourceHeight - sourceOffset)
            const sliceCanvas = document.createElement('canvas')
            sliceCanvas.width = image.naturalWidth
            sliceCanvas.height = Math.max(1, Math.ceil(sliceHeight * image.naturalHeight / sourceHeight))
            const sliceContext = sliceCanvas.getContext('2d')
            sliceContext.fillStyle = '#fff'
            sliceContext.fillRect(0, 0, sliceCanvas.width, sliceCanvas.height)
            sliceContext.drawImage(
              image,
              0,
              Math.floor(sourceOffset * image.naturalHeight / sourceHeight),
              image.naturalWidth,
              sliceCanvas.height,
              0,
              0,
              sliceCanvas.width,
              sliceCanvas.height
            )
            pdf.addImage(sliceCanvas.toDataURL('image/png'), 'PNG', margin, margin, imageWidth, sliceHeight * scale, undefined, 'FAST')
            sourceOffset += sliceHeight
            firstSlice = false
          }
        }
        const renderTableCanvas = block => {
          const columns = Array.isArray(block.renderSpec && block.renderSpec.columns) ? block.renderSpec.columns : []
          const rows = Array.isArray(block.renderSpec && block.renderSpec.rows) ? block.renderSpec.rows : []
          const canvas = document.createElement('canvas')
          const canvasWidth = 1800
          const titleHeight = 76
          const headerHeight = 54
          const rowHeight = 46
          canvas.width = canvasWidth
          canvas.height = Math.max(titleHeight + headerHeight + rowHeight, titleHeight + headerHeight + rows.length * rowHeight)
          const context = canvas.getContext('2d')
          context.fillStyle = '#fff'
          context.fillRect(0, 0, canvas.width, canvas.height)
          context.font = '600 28px ' + fontFamily
          context.fillStyle = '#153b67'
          context.fillText(String(block.title || block.moduleKey || '报告'), 24, 46)
          const widths = columns.map(column => Number(column.minWidth || column.width || 120))
          const totalWidth = widths.reduce((sum, value) => sum + value, 0) || 1
          let x = 0
          context.font = '600 21px ' + fontFamily
          columns.forEach((column, index) => {
            const cellWidth = canvasWidth * widths[index] / totalWidth
            context.fillStyle = '#f2f3f5'
            context.fillRect(x, titleHeight, cellWidth, headerHeight)
            context.strokeStyle = '#dcdfe6'
            context.strokeRect(x, titleHeight, cellWidth, headerHeight)
            context.fillStyle = '#303133'
            context.fillText(String(column.title || column.label || column.field || ''), x + 12, titleHeight + 34)
            x += cellWidth
          })
          context.font = '18px ' + fontFamily
          rows.forEach((row, rowIndex) => {
            let cellX = 0
            columns.forEach((column, columnIndex) => {
              const cellWidth = canvasWidth * widths[columnIndex] / totalWidth
              const y = titleHeight + headerHeight + rowIndex * rowHeight
              context.fillStyle = '#fff'
              context.fillRect(cellX, y, cellWidth, rowHeight)
              context.strokeStyle = '#dcdfe6'
              context.strokeRect(cellX, y, cellWidth, rowHeight)
              context.fillStyle = '#606266'
              context.fillText(formatExportValue(row && row[column.field], column.format), cellX + 12, y + 30)
              cellX += cellWidth
            })
          })
          return canvas
        }
        const renderChartBlock = async block => {
          const sourceNode = target.querySelector('#vm-chat-block-' + block.blockId)
          if (!sourceNode) return null
          const rect = sourceNode.getBoundingClientRect()
          const width = Math.max(320, Math.round(rect.width))
          const height = Math.max(220, Math.round(rect.height))
          const cloneNode = sourceNode.cloneNode(true)
          cloneNode.style.backgroundColor = '#fff'
          cloneNode.style.height = height + 'px'
          cloneNode.style.left = '0'
          cloneNode.style.margin = '0'
          cloneNode.style.position = 'relative'
          cloneNode.style.transform = 'none'
          cloneNode.style.top = '0'
          cloneNode.style.width = width + 'px'
          cloneNode.querySelectorAll('.block-actions, .block-selector, .block-title-edit-button').forEach(node => {
            node.style.display = 'none'
          })
          cloneNode.querySelectorAll('.block-content').forEach(node => {
            node.style.overflow = 'visible'
          })
          exportHost = document.createElement('div')
          exportHost.style.left = '-100000px'
          exportHost.style.position = 'fixed'
          exportHost.style.top = '0'
          exportHost.appendChild(cloneNode)
          document.body.appendChild(exportHost)
          await new Promise(resolve => {
            window.requestAnimationFrame(() => window.requestAnimationFrame(resolve))
          })
          const imageData = await toPng(cloneNode, {
            backgroundColor: '#fff',
            cacheBust: true,
            height,
            pixelRatio: 2,
            style: { backgroundColor: '#fff', height: height + 'px', width: width + 'px' },
            width
          })
          exportHost.remove()
          exportHost = null
          return { dataUrl: imageData, height, width }
        }

        for (const block of orderedBlocks) {
          beginBlockPage()
          if (block.type === 'table') {
            const tableCanvas = renderTableCanvas(block)
            await addImagePages(tableCanvas.toDataURL('image/png'), tableCanvas.width, tableCanvas.height)
            continue
          }
          if (block.type === 'echarts') {
            const chartImage = await renderChartBlock(block)
            if (chartImage) await addImagePages(chartImage.dataUrl, chartImage.width, chartImage.height)
          }
        }
        if (!hasPdfContent && this.reportNotices.length) {
          const noticeCanvas = document.createElement('canvas')
          noticeCanvas.width = 1800
          noticeCanvas.height = Math.max(240, this.reportNotices.length * 90)
          const noticeContext = noticeCanvas.getContext('2d')
          noticeContext.fillStyle = '#fff'
          noticeContext.fillRect(0, 0, noticeCanvas.width, noticeCanvas.height)
          noticeContext.font = '18px ' + fontFamily
          noticeContext.fillStyle = '#606266'
          this.reportNotices.forEach((notice, index) => noticeContext.fillText(String(notice.message || ''), 24, 42 + index * 80))
          hasPdfContent = true
          await addImagePages(noticeCanvas.toDataURL('image/png'), noticeCanvas.width, noticeCanvas.height)
        }

        const now = new Date()
        const pad = value => String(value).padStart(2, '0')
        const fileName = 'vmChat报告_' + now.getFullYear() + pad(now.getMonth() + 1) + pad(now.getDate()) + '_' + pad(now.getHours()) + pad(now.getMinutes()) + '.pdf'
        pdf.save(fileName)
        if (this.$message && this.$message.success) this.$message.success('报告 PDF 已导出')
      } catch (error) {
        logVmChatEvent('ui', 'export.pdf.failed', error, { level: 'warn' })
        if (this.$message && this.$message.error) this.$message.error('报告 PDF 导出失败，请稍后重试')
      } finally {
        if (exportHost && exportHost.parentNode) exportHost.parentNode.removeChild(exportHost)
        this.exportingPdf = false
      }
    },
    focusBlock(blockId) {
      this.selectedBlockId = blockId
      this.selectedBlockIds = [blockId]
      this.activeBlockId = blockId
      const target = document.getElementById('vm-chat-block-' + blockId)
      const scroller = this.$refs.reportScroller
      if (target && scroller) {
        const scrollerRect = scroller.getBoundingClientRect()
        const targetRect = target.getBoundingClientRect()
        const nextTop = scroller.scrollTop + targetRect.top - scrollerRect.top - 8
        scroller.scrollTo({
          top: Math.max(0, nextTop),
          behavior: 'smooth'
        })
      }
    },
    focusReportTocItem(item) {
      const firstBlockId = item && item.blockIds && item.blockIds[0]
      if (firstBlockId) this.focusBlock(firstBlockId)
    },
    startReportBlockDrag(entityKey, event) {
      this.tocDragBlockId = entityKey
      this.tocDragTargetId = entityKey
      if (event && event.dataTransfer) {
        event.dataTransfer.effectAllowed = 'move'
        event.dataTransfer.setData('text/plain', entityKey)
      }
    },
    resetReportBlockDrag() {
      this.tocDragBlockId = ''
      this.tocDragTargetId = ''
    },
    dropReportBlock(targetEntityKey) {
      const sourceEntityKey = this.tocDragBlockId
      this.resetReportBlockDrag()
      if (!sourceEntityKey || sourceEntityKey === targetEntityKey) return
      const sourceWidget = this.gridWidgets.find(widget => widget.i === sourceEntityKey)
      const targetWidget = this.gridWidgets.find(widget => widget.i === targetEntityKey)
      if (!sourceWidget || !targetWidget) return
      const nextWidgets = this.gridWidgets.map(widget => {
        if (widget.i === sourceWidget.i) return Object.assign({}, widget, { y: targetWidget.y })
        if (widget.i === targetWidget.i) return Object.assign({}, widget, { y: sourceWidget.y })
        return widget
      })
      this.syncCanvasState(updateTopLevelWidgets(this.getCanvasState(), nextWidgets))
      this.scheduleChartResize()
    },
    resetReport() {
      this.cancelBlockTitleEdit()
      this.syncCanvasState(createCanvasStateFromBlocks([]))
      this.selectedBlockId = ''
      this.selectedBlockIds = []
      this.activeBlockId = ''
      this.renderType = 'chat'
      this.renderMessage = '已清空报告。'
      this.clarifyQuestions = []
      this.reportNotices = []
      this.failedUpdateOperation = null
      this.lastPayload = null
    },
    getBlockTemplateSource(block) {
      if (!block || block.sourceTemplateType !== 'vm-block-template' || !block.sourceTemplateId) return null
      return this.savedTemplates.find(item => item.id === block.sourceTemplateId && item.entityType === 'vm-block-template') || null
    },
    getBlockSaveButtonTitle(block) {
      return this.getBlockTemplateSource(block) ? '覆盖来源模板' : '保存为自定义模块'
    },
    getGroupTemplateSource(group) {
      if (!group || group.sourceTemplateType !== 'vm-group-template' || !group.sourceTemplateId) return null
      return this.savedTemplates.find(item => item.id === group.sourceTemplateId && item.entityType === 'vm-group-template') || null
    },
    getGroupSaveButtonTitle(group) {
      return this.getGroupTemplateSource(group) ? '覆盖来源组合模板' : '保存为自定义组合模块'
    },
    async persistSavedTemplateUpdate(templateId, serializedTemplate, successMessage) {
      const index = this.savedTemplates.findIndex(item => item.id === templateId)
      const current = index >= 0 ? this.savedTemplates[index] : null
      if (!current) return false
      const next = normalizeTemplateRecord(Object.assign(
        {},
        serializedTemplate,
        {
          id: current.id,
          createdAt: current.createdAt
        },
        this.getTemplateAuditFields()
      ))
      const saved = await this.persistTemplateRecord(next, 'PUT', templateId)
      this.$set(this.savedTemplates, index, saved)
      if (this.$message && this.$message.success) this.$message.success(successMessage)
      return true
    },
    async saveBlockTemplateAsNew(blockId) {
      const block = this.getBlockById(blockId)
      if (!block) return
      const widget = this.gridWidgets.find(w => w.i === createEntityKey('block', blockId))
      const widgetHeight = widget ? widget.h : null
      const next = normalizeTemplateRecord(Object.assign(
        {},
        serializeBlockTemplate(block, widgetHeight),
        this.getTemplateAuditFields()
      ))
      const saved = await this.persistTemplateRecord(next)
      this.savedTemplates.unshift(saved)
      if (this.$message && this.$message.success) this.$message.success('单模块已保存到自定义模块')
    },
    saveBlockTemplate(blockId) {
      const block = this.getBlockById(blockId)
      if (!block) return
      const source = this.getBlockTemplateSource(block)
      if (!source) {
        this.saveBlockTemplateAsNew(blockId)
        return
      }
      this.$confirm(`确认覆盖自定义模块「${source.title || '未命名模块'}」？`, '覆盖确认', {
        confirmButtonText: '确认覆盖',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          const widget = this.gridWidgets.find(w => w.i === createEntityKey('block', blockId))
          const widgetHeight = widget ? widget.h : null
          return this.persistSavedTemplateUpdate(
            source.id,
            serializeBlockTemplate(block, widgetHeight),
            '已覆盖原自定义模块'
          )
        })
        .catch(() => {})
    },
    async saveGroupTemplateAsNew(groupId) {
      const group = this.groupsById[groupId]
      if (!group) return
      const template = serializeGroupTemplate(group)
      if (!template) return
      const next = normalizeTemplateRecord(Object.assign({}, template, this.getTemplateAuditFields()))
      const saved = await this.persistTemplateRecord(next)
      this.savedTemplates.unshift(saved)
      if (this.$message && this.$message.success) this.$message.success('组合模块已保存到自定义模块')
    },
    saveGroupTemplate(groupId) {
      const group = this.groupsById[groupId]
      if (!group) return
      const source = this.getGroupTemplateSource(group)
      if (!source) {
        this.saveGroupTemplateAsNew(groupId)
        return
      }
      this.$confirm(`确认覆盖组合模块「${source.title || '未命名组合'}」？`, '覆盖确认', {
        confirmButtonText: '确认覆盖',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => this.persistSavedTemplateUpdate(source.id, serializeGroupTemplate(group), '已覆盖原组合模块'))
        .catch(() => {})
    },
    saveCurrentLayoutTemplate() {
      const defaultTitle = '当前布局 ' + new Date().toLocaleString()
      this.$prompt('请输入布局模板名称', '保存布局模板', {
        confirmButtonText: '保存',
        cancelButtonText: '取消',
        inputValue: defaultTitle,
        inputPattern: /.+/,
        inputErrorMessage: '名称不能为空'
      })
        .then(({ value }) => {
          const title = String(value || '').trim() || defaultTitle
          const template = serializeLayoutTemplate(this.getCanvasState(), title)
          if (!template) return
          const next = normalizeTemplateRecord(Object.assign({}, template, this.getTemplateAuditFields()))
          this.persistTemplateRecord(next)
            .then(saved => this.savedTemplates.unshift(saved))
            .catch(error => logVmChatEvent('ui', 'template.persist.failed', error, { level: 'warn' }))
          if (this.$message && this.$message.success) this.$message.success('当前布局已保存')
        })
        .catch(() => {})
    },
    mergeSelectedBlocks() {
      const targetIds = this.getMergeableSelectedBlockIds()
      if (targetIds.length < 2) return
      const next = mergeBlocksToGroup(this.getCanvasState(), targetIds, '自定义组合')
      this.syncCanvasState(next)
      this.selectedBlockIds = []
      this.selectedBlockId = ''
      this.scheduleChartResize()
      if (this.$message && this.$message.success) this.$message.success('已合并为组合模块')
    },
    ungroup(groupId) {
      this.syncCanvasState(ungroupToCanvas(this.getCanvasState(), groupId))
      this.scheduleChartResize()
    },
    updateGroupTitle(groupId, title) {
      this.syncCanvasState(renameGroup(this.getCanvasState(), groupId, title))
    },
    handleGroupLayoutUpdated(groupId, nextLayout) {
      const group = this.groupsById[groupId]
      if (!group || isSameLayout(group.widgets, nextLayout)) return
      this.syncCanvasState(updateGroupWidgets(this.getCanvasState(), groupId, nextLayout || []))
      this.scheduleChartResize()
    },
    removeSavedTemplate(templateId) {
      const template = this.savedTemplates.find(item => item.id === templateId)
      const title = template ? template.title || '未命名' : '未命名'
      const typeLabel = template ? this.getTemplateTypeLabel(template) : ''
      this.$confirm(`确认删除「${title}」${typeLabel ? '(' + typeLabel + ')' : ''}？删除后不可恢复。`, '删除确认', {
        confirmButtonText: '确认删除',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          return window.fetch(MODULES_API_ROUTE + '/' + encodeURIComponent(templateId), {
            method: 'DELETE',
            headers: buildHermesAuthHeaders()
          }).then(response => {
            if (!response.ok) throw new Error('模板接口删除失败：HTTP ' + response.status)
            this.savedTemplates = this.savedTemplates.filter(item => item.id !== templateId)
            if (this.$message && this.$message.success) this.$message.success('已删除')
          })
        })
        .catch(error => {
          if (error) logVmChatEvent('ui', 'template.delete.failed', error, { level: 'warn' })
        })
    },
    async insertTemplate(templateId) {
      let template = this.savedTemplates.find(item => item.id === templateId)
      try {
        template = await this.fetchTemplateRecord(templateId) || template
      } catch (error) {
        logVmChatEvent('ui', 'template.fetch.failed', error, { level: 'warn' })
      }
      if (!template) return
      const beforeIds = new Set(this.getAllBlockIds())
      const next = restoreTemplateToGrid(this.getCanvasState(), template)
      this.syncCanvasState(next)
      const insertedIds = this.getAllBlockIds().filter(id => !beforeIds.has(id))
      await this.hydratePendingBlocks(insertedIds, createVmTraceId('vm-template'))
    },
    setReportNotice(notice) {
      if (!notice) return
      this.reportNotices = [notice]
      this.scrollReportToTop()
      logVmChatEvent(
        'render',
        'notice.set',
        {
          status: notice.status,
          message: notice.message,
          reason: notice.reason,
          questionCount: Array.isArray(notice.questions) ? notice.questions.length : 0
        },
        {
          traceId: notice.traceId,
          level: notice.status === 'error' ? 'error' : notice.status === 'rejected' ? 'warn' : 'info'
        }
      )
    },
    clearReportNotices() {
      if (!this.reportNotices.length) return
      this.reportNotices = []
    },
    dismissReportNotice(index) {
      if (index < 0 || index >= this.reportNotices.length) return
      if (this.reportNotices[index] && this.reportNotices[index].status === 'error') {
        this.failedUpdateOperation = null
      }
      this.reportNotices.splice(index, 1)
    },
    getNoticeTitle(notice) {
      if (!notice) return 'vmChat 状态'
      if (notice.status === 'clarify') return '需要补充信息'
      if (notice.status === 'rejected') return '无法合并展示'
      if (notice.status === 'error') return '处理失败'
      return 'vmChat 状态'
    },
    getNoticeStatusText(notice) {
      if (!notice) return ''
      if (notice.status === 'clarify') return 'clarify'
      if (notice.status === 'rejected') return 'rejected'
      if (notice.status === 'error') return 'error'
      return notice.status
    },
    getBlockRangeText(block) {
      const range = (block.queryContext && block.queryContext.dateRange) || []
      return range.length === 2 ? range[0] + ' 至 ' + range[1] : ''
    },
    getBlockProductCode(block) {
      return (block.queryContext && (block.queryContext.productCode || block.queryContext.fundCode)) || ''
    },
    getBlockDisplayTitle(block) {
      const dslTitle = block && block.dsl && block.dsl.view && block.dsl.view.title
      const title = dslTitle || (block && block.title)
      return String(title || '').trim()
    },
    getBlockRuntimeText(block) {
      const runtime = block && block.sourceData && block.sourceData.runtime
      const rowCounts = runtime && runtime.rowCounts
      if (!rowCounts || typeof rowCounts !== 'object') return ''
      const summary = Object.keys(rowCounts)
        .map(key => key + ' ' + rowCounts[key])
        .join(' / ')
      if (runtime.dataMode === 'mock') return summary + '（mock样例）'
      if (runtime.dataMode === 'mixed') return summary + '（真实+mock）'
      if (runtime.dataMode === 'example') return summary + '（示例数据）'
      return summary
    },
    isExampleDataBlock(block) {
      const runtime = block && block.sourceData && block.sourceData.runtime
      return !!runtime && runtime.dataMode === 'example'
    },
    getBlockDiagnostics(block) {
      const diagnostics = block && block.sourceData && block.sourceData.runtime && block.sourceData.runtime.displayDiagnostics
      return Array.isArray(diagnostics) ? diagnostics : []
    },
    handleComposerKeydown(event) {
      if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
        event.preventDefault()
        this.sendMessage()
      }
    },
    toggleExamplePanel() {
      this.showExamplePanel = !this.showExamplePanel
    },
    selectExample(text) {
      this.draftMessage = text
      this.showExamplePanel = false
    },
    resizeCharts() {
      this.reportBlocks.forEach(block => {
        if (block.type !== 'echarts') return
        const ref = this.$refs['chart-' + block.blockId]
        const chart = Array.isArray(ref) ? ref[0] : ref
        if (chart && chart.resize) chart.resize()
      })
    },
    scheduleChartResize() {
      if (this.chartResizeTimer) {
        window.cancelAnimationFrame(this.chartResizeTimer)
      }
      this.chartResizeTimer = window.requestAnimationFrame(() => {
        this.chartResizeTimer = null
        this.$nextTick(() => this.resizeCharts())
      })
    },
    scrollMessagesToBottom(force) {
      if (force) {
        this.messageListAutoFollow = true
        this.messageListPinnedToBottom = true
      }
      if (!this.messageListAutoFollow || !this.messageListPinnedToBottom) return
      this.$nextTick(() => {
        if (!this.messageListAutoFollow || !this.messageListPinnedToBottom) return
        this.setMessagesScrollBottom()
        window.requestAnimationFrame(() => {
          if (this.messageListAutoFollow && this.messageListPinnedToBottom) this.setMessagesScrollBottom()
        })
        if (this.messageScrollSettleTimer) {
          window.clearTimeout(this.messageScrollSettleTimer)
        }
        this.messageScrollSettleTimer = window.setTimeout(() => {
          this.messageScrollSettleTimer = null
          if (this.messageListAutoFollow && this.messageListPinnedToBottom) this.setMessagesScrollBottom()
        }, 80)
      })
    },
    scrollReportToTop() {
      this.$nextTick(() => {
        const target = this.$refs.reportScroller
        if (!target) return
        target.scrollTop = 0
        window.requestAnimationFrame(() => {
          if (this.$refs.reportScroller === target) target.scrollTop = 0
        })
      })
    },
    setMessagesScrollBottom() {
      const target = this.$refs.messageList
      if (!target) return
      target.scrollTop = target.scrollHeight
    },
    handleMessageListScroll() {
      const target = this.$refs.messageList
      if (!target) return
      const movedUp = target.scrollTop < this.messageListLastScrollTop - 1
      this.messageListLastScrollTop = target.scrollTop
      if (movedUp) {
        this.messageListAutoFollow = false
        this.messageListPinnedToBottom = false
        if (this.messageScrollSettleTimer) {
          window.clearTimeout(this.messageScrollSettleTimer)
          this.messageScrollSettleTimer = null
        }
        return
      }
      if (!this.messageListAutoFollow) {
        this.messageListPinnedToBottom = false
        return
      }
      const distanceToBottom = target.scrollHeight - target.scrollTop - target.clientHeight
      this.messageListPinnedToBottom = distanceToBottom <= 24
      if (!this.messageListPinnedToBottom && this.messageScrollSettleTimer) {
        window.clearTimeout(this.messageScrollSettleTimer)
        this.messageScrollSettleTimer = null
      }
    },
    handleMessageListWheel(event) {
      if (!event || !event.deltaY) return
      if (event.deltaY < 0) {
        this.messageListAutoFollow = false
        this.messageListPinnedToBottom = false
        if (this.messageScrollSettleTimer) {
          window.clearTimeout(this.messageScrollSettleTimer)
          this.messageScrollSettleTimer = null
        }
        return
      }
      if (event.deltaY > 0) {
        window.requestAnimationFrame(() => {
          const target = this.$refs.messageList
          if (!target) return
          const distanceToBottom = target.scrollHeight - target.scrollTop - target.clientHeight
          if (distanceToBottom <= 24) {
            this.messageListAutoFollow = true
            this.messageListPinnedToBottom = true
          }
        })
      }
    },
    scheduleMessagesScroll() {
      if (this.messageScrollTimer) return
      this.messageScrollTimer = window.requestAnimationFrame(() => {
        this.messageScrollTimer = null
        this.scrollMessagesToBottom()
      })
    },
    updateAssistantMessage(message, patch) {
      if (!message || !patch) return
      Object.assign(message, patch)
      const index = this.chatMessages.findIndex(item => item && item.id === message.id)
      if (index >= 0) {
        this.$set(this.chatMessages, index, Object.assign({}, this.chatMessages[index], patch))
      }
    },
    normalizeMessageTextForCompare(text) {
      return String(text || '')
        .replace(/\s+/g, ' ')
        .trim()
    },
    shouldShowThinking(message) {
      if (!message || !message.thinking) return false
      const thinking = this.normalizeMessageTextForCompare(message.thinking)
      if (!thinking) return false
      const content = this.normalizeMessageTextForCompare(message.content)
      if (!content) return true
      return thinking !== content
    },
    toggleThinking(message) {
      if (!message || !this.shouldShowThinking(message)) return
      this.$set(message, 'thinkingExpanded', !message.thinkingExpanded)
    },
    formatMetricsSummary(startedAt, streamResult) {
      const totalMs = Date.now() - startedAt
      const chunkCount = streamResult && streamResult.chunkCount ? streamResult.chunkCount : 0
      return '总耗时 ' + (totalMs / 1000).toFixed(1) + 's' + (chunkCount ? ' / 分片 ' + chunkCount : '')
    },
    getAssistantDisplayContent(payload, fallback) {
      const message = String(payload && payload.message ? payload.message : '').trim()
      if (message) return message
      if (!payload || payload.renderType !== 'report') {
        return String(fallback || '已处理完成。')
      }
      const operations = Array.isArray(payload.operations) ? payload.operations : []
      const firstBlock = operations.map(item => item && item.block).find(Boolean)
      const title = firstBlock && firstBlock.title ? String(firstBlock.title) : ''
      const hasUpdate = operations.some(item => item && item.action === 'replaceBlock')
      if (hasUpdate) return title ? '已更新报告块：' + title : '已更新报告块。'
      return title ? '已生成报告块：' + title : '已生成报告块。'
    },
    buildMessageDebug(question, parsedPayload, rawResponse, error, traceId) {
      return {
        copiedAt: new Date().toISOString(),
        sessionId: this.sessionId,
        traceId,
        userQuestion: question,
        selectedBlockId: this.selectedBlockId,
        selectedBlockIds: this.selectedBlockIds,
        parsedPayload: parsedPayload ? parsedPayload.raw : null,
        rawResponse,
        reportNotices: this.reportNotices,
        widgets: this.gridWidgets,
        groupsById: this.groupsById,
        savedTemplates: this.savedTemplates,
        renderedBlocksSummary: JSON.parse(buildVmReportBlocksSummary(this.reportBlocks) || '[]'),
        logs: getVmChatLogs({ traceId, limit: 200 }),
        error: error ? error.message || String(error) : ''
      }
    },
    buildNoticeDebug(parsedPayload, rawResponse, error, traceId) {
      return {
        copiedAt: new Date().toISOString(),
        sessionId: this.sessionId,
        traceId,
        selectedBlockId: this.selectedBlockId,
        selectedBlockIds: this.selectedBlockIds,
        parsedPayload: parsedPayload ? parsedPayload.raw : null,
        rawResponse,
        widgets: this.gridWidgets,
        groupsById: this.groupsById,
        renderedBlocksSummary: JSON.parse(buildVmReportBlocksSummary(this.reportBlocks) || '[]'),
        logs: getVmChatLogs({ traceId, limit: 200 }),
        error: error ? error.message || String(error) : ''
      }
    },
    async copyMessageDebug(message) {
      await this.copyText(JSON.stringify(message.debugPayload || {}, null, 2))
      this.$set(message, 'debugCopied', true)
      setTimeout(() => {
        this.$set(message, 'debugCopied', false)
      }, 1500)
    },
    async copyNoticeDebug(notice) {
      const payload =
        notice && notice.debugPayload
          ? notice.debugPayload
          : {
              copiedAt: new Date().toISOString(),
              sessionId: this.sessionId,
              notice,
              widgets: this.gridWidgets,
              groupsById: this.groupsById,
              renderedBlocksSummary: JSON.parse(buildVmReportBlocksSummary(this.reportBlocks) || '[]'),
              logs: getVmChatLogs({ limit: 200 })
            }
      await this.copyText(JSON.stringify(payload, null, 2))
      if (this.$message && this.$message.success) this.$message.success('状态卡 Debug 已复制')
    },
    async copyPageDebug() {
      const debugPayload = {
        copiedAt: new Date().toISOString(),
        sessionId: this.sessionId,
        protocolVersion: this.protocolVersion,
        selectedBlockId: this.selectedBlockId,
        selectedBlockIds: this.selectedBlockIds,
        lastPayload: this.lastPayload,
        reportNotices: this.reportNotices,
        widgets: this.gridWidgets,
        groupsById: this.groupsById,
        savedTemplates: this.savedTemplates,
        renderedBlocksSummary: JSON.parse(buildVmReportBlocksSummary(this.reportBlocks) || '[]'),
        logs: getVmChatLogs({ limit: 300 })
      }
      await this.copyText(JSON.stringify(debugPayload, null, 2))
      if (this.$message && this.$message.success) this.$message.success('页面 Debug 已复制')
    },
    async copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text)
        return
      }
      const textarea = document.createElement('textarea')
      textarea.value = text
      textarea.setAttribute('readonly', 'readonly')
      textarea.style.position = 'absolute'
      textarea.style.left = '-9999px'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
    }
  }
}
</script>

<style scoped>
.vm-chat-page {
  display: grid;
  grid-template-columns: 338px minmax(0, 1fr) 0px 400px;
  column-gap: 0;
  height: calc(100vh - 112px);
  min-height: 0;
  padding: 16px 16px 20px;
  box-sizing: border-box;
  overflow: hidden;
  background: linear-gradient(180deg, #f3f6fa 0%, #eef2f7 100%);
  transition: grid-template-columns 0.24s cubic-bezier(0.22, 1, 0.36, 1);
}

.vm-chat-page.is-sidebar-collapsed {
  grid-template-columns: 0 minmax(0, 1fr) 0px 400px;
}

.module-sidebar {
  margin-right: 0;
  position: relative;
  min-width: 0;
  min-height: 0;
  align-self: stretch;
  z-index: 9;
  display: flex;
  flex-direction: column;
  overflow: visible;
  opacity: 1;
  transform: translateX(0);
  transition: width 0.24s cubic-bezier(0.22, 1, 0.36, 1), opacity 0.16s ease, transform 0.24s cubic-bezier(0.22, 1, 0.36, 1);
}

.vm-chat-page.is-sidebar-collapsed .module-sidebar {
  width: 0;
  overflow: hidden;
  opacity: 0;
  pointer-events: none;
  transform: translateX(-12px);
}

.module-sidebar.is-entering .toc-head,
.module-sidebar.is-entering .toc-body {
  animation: sidebar-content-in 0.18s ease-out both;
}

@keyframes sidebar-content-in {
  from {
    opacity: 0;
    transform: translateX(-8px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .vm-chat-page,
  .module-sidebar,
  .sidebar-expand-enter-active,
  .sidebar-expand-leave-active {
    transition: none;
  }

  .module-sidebar.is-entering .toc-head,
  .module-sidebar.is-entering .toc-body {
    animation: none;
  }
}

.toc-head {
  position: relative;
  flex: 0 0 auto;
  min-height: 0;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  padding: 12px;
  border: 1px solid rgba(216, 227, 239, 0.9);
  border-radius: 16px;
  background: linear-gradient(135deg, #ffffff 0%, #f2f7fd 100%);
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.07);
  overflow: visible;
}

.sidebar-collapse-toggle,
.sidebar-expand-toggle {
  width: 20px;
  height: 48px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border: 1px solid #cbddec;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.98);
  color: #17345f;
  font-size: 16px;
  line-height: 1;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(32, 69, 106, 0.12);
  transition: color 0.16s ease, border-color 0.16s ease, background-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.sidebar-collapse-toggle:hover,
.sidebar-expand-toggle:hover {
  border-color: #5a95ca;
  background: rgba(255, 255, 255, 0.98);
  color: #397cb9;
  box-shadow: 0 6px 16px rgba(45, 114, 177, 0.24);
  transform: translateY(-1px);
}

.sidebar-collapse-toggle:focus-visible,
.sidebar-expand-toggle:focus-visible {
  outline: 2px solid rgba(64, 158, 255, 0.45);
  outline-offset: 2px;
}

.sidebar-toggle-icon {
  display: inline-block;
  width: 12px;
  height: 12px;
  box-sizing: border-box;
  fill: none;
  stroke: #90a7bf;
  stroke-linecap: round;
  stroke-linejoin: round;
  stroke-width: 2;
}

.sidebar-collapse-toggle {
  position: absolute;
  top: 50%;
  right: -13px;
  z-index: 9;
  transform: translateY(-50%);
}

.sidebar-expand-toggle {
  position: absolute;
  top: 50%;
  left: 8px;
  z-index: 9;
  transform: translateY(-50%);
}

.sidebar-collapse-toggle:hover,
.sidebar-expand-toggle:hover {
  transform: translateY(-50%) scale(1.06);
}

.sidebar-expand-enter-active,
.sidebar-expand-leave-active {
  transition: opacity 0.16s ease, transform 0.2s ease;
}

.sidebar-expand-enter,
.sidebar-expand-leave-to {
  opacity: 0;
  transform: translate(-8px, -50%);
}

.toc-head__actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 8px 12px 10px;
  border: 1px solid rgba(219, 231, 244, 0.95);
  border-radius: 12px;
  background: rgba(245, 249, 254, 0.88);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.82);
}

.toc-head__mode-row {
  display: flex;
  align-items: center;
  min-height: 28px;
  padding: 0 2px;
}

.toc-layout-switch {
  flex: 0 0 auto;
  min-height: 28px;
}

.toc-head__button-row {
  display: grid;
  width: min(100%, 264px);
  margin: 0 auto;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 8px;
}

.toc-action-button.el-button {
  width: 100%;
  height: 31px;
  margin: 0;
  padding: 0 6px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  border: 1px solid #d9e5f2;
  border-radius: 9px;
  background: #fff;
  color: #47627f;
  font-size: 12px;
  line-height: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  box-shadow: 0 2px 5px rgba(36, 72, 112, 0.05);
  transition: color 0.16s ease, border-color 0.16s ease, background-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.toc-action-button.el-button:hover:not(.is-disabled) {
  color: #1d5ea8;
  border-color: #9fc3e8;
  background: #f5faff;
  box-shadow: 0 5px 12px rgba(41, 102, 170, 0.12);
  transform: translateY(-1px);
}

.toc-action-button.el-button:active:not(.is-disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 5px rgba(36, 72, 112, 0.08);
}

.toc-action-button.el-button.is-disabled {
  color: #aebbc9;
  border-color: #e4ebf3;
  background: #f8fafc;
  box-shadow: none;
  opacity: 1;
}

.toc-action-button i {
  flex: 0 0 auto;
  font-size: 13px;
}

.toc-action-button--danger.el-button {
  color: #a46a63;
  border-color: #ecd9d5;
  background: #fffaf9;
}

.toc-action-button--danger.el-button:hover:not(.is-disabled) {
  color: #a84f45;
  border-color: #e5b6af;
  background: #fff3f0;
}

.toc-body {
  position: relative;
  width: 100%;
  flex: 1;
  min-height: 0;
  margin-top: 12px;
}

.custom-module-panel {
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 0;
  box-sizing: border-box;
  padding: 10px;
  border: 1px solid rgba(216, 227, 239, 0.9);
  border-radius: 16px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.98), rgba(246, 250, 255, 0.96));
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.08);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.custom-module-list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 5px;
  scroll-behavior: smooth;
}

.custom-module-list::-webkit-scrollbar {
  width: 3px;
}

.custom-module-list::-webkit-scrollbar-thumb {
  background: #d0d8e3;
  border-radius: 99px;
}

.report-toc {
  position: absolute;
  top: 54px;
  bottom: 16px;
  left: 16px;
  z-index: 5;
  width: 268px;
  min-height: 0;
  pointer-events: none;
}

.report-toc__panel {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  min-height: 0;
  padding: 10px;
  border: 1px solid rgba(216, 227, 239, 0.9);
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
  overflow: hidden;
  pointer-events: auto;
  opacity: 1;
  transform: translateX(0);
  visibility: visible;
  transition: opacity 0.18s ease, transform 0.24s ease, visibility 0s linear 0s;
}

.report-toc__header {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.report-toc__header .toc-title {
  flex: 1;
  min-width: 0;
  margin-bottom: 0;
}

.report-toc__panel > .toc-search {
  margin-top: 10px;
}

.report-toc__close {
  width: 30px;
  height: 30px;
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dce7f3;
  border-radius: 9px;
  background: #f8fbff;
  color: #17345f;
  cursor: pointer;
  transition: border-color 0.16s ease, background-color 0.16s ease, transform 0.16s ease;
}

.report-toc__close:hover {
  border-color: #17345f;
  background: #edf4fc;
  transform: translateY(-1px);
}

.toc-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
  color: #5f6b7a;
}

.toc-title-main {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #153b67;
}

.toc-empty {
  font-size: 13px;
  color: #8a96a3;
}

.toc-search {
  position: relative;
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.toc-search__icon {
  position: absolute;
  left: 10px;
  color: #929eb0;
  font-size: 14px;
  pointer-events: none;
}

.toc-search__input {
  width: 100%;
  height: 32px;
  padding: 0 28px 0 32px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  background: #f5f8fc;
  color: #1e293b;
  font-size: 13px;
  outline: none;
  transition: border-color 0.16s, background 0.16s;
}

.toc-search__input::placeholder {
  color: #a4b0c0;
}

.toc-search__input:focus {
  border-color: #153b67;
  background: #fff;
}

.toc-search__clear {
  position: absolute;
  right: 6px;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 6px;
  background: transparent;
  color: #929eb0;
  font-size: 16px;
  cursor: pointer;
  line-height: 1;
}

.toc-search__clear:hover {
  background: #e2e8f0;
  color: #475569;
}

.toc-item {
  width: 100%;
  display: flex;
  gap: 8px;
  align-items: center;
  margin-bottom: 8px;
  padding: 10px;
  border: 1px solid #e6ebf2;
  border-radius: 10px;
  background: #fff;
  cursor: pointer;
  text-align: left;
  transition: border-color 0.16s ease, background-color 0.16s ease, box-shadow 0.16s ease;
}

.toc-item[draggable='true'] {
  cursor: grab;
}

.toc-item[draggable='true']:active {
  cursor: grabbing;
}

.toc-item:hover {
  border-color: #b9cce3;
  background: #f7fbff;
  box-shadow: 0 6px 14px rgba(23, 52, 95, 0.06);
}

.toc-item.is-active,
.toc-item.is-selected {
  border-color: #153b67;
  background: #eef5fd;
}

.toc-item.is-drag-over {
  border-color: #5a95ca;
  background: #eaf3fc;
  box-shadow: inset 0 2px 0 #5a95ca;
}

.toc-item__drag {
  width: 12px;
  flex: 0 0 12px;
  color: #9aabba;
  font-size: 13px;
  text-align: center;
}

.toc-item:hover .toc-item__drag {
  color: #397cb9;
}

.toc-index {
  width: 22px;
  height: 22px;
  line-height: 22px;
  border-radius: 999px;
  background: #153b67;
  color: #fff;
  text-align: center;
  font-size: 12px;
}

.toc-name {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  line-height: 1.45;
  color: #2f3a4b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.toc-item__meta {
  flex: 0 0 auto;
  color: #7f91a4;
  font-size: 11px;
  white-space: nowrap;
}

.toc-block-list-wrapper {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
  padding: 5px;
  scroll-behavior: smooth;
}

.toc-block-list-wrapper::-webkit-scrollbar {
  width: 3px;
}

.toc-block-list-wrapper::-webkit-scrollbar-thumb {
  background: #d0d8e3;
  border-radius: 99px;
}

.toc-block-list-wrapper::-webkit-scrollbar-track,
.custom-module-list::-webkit-scrollbar-track {
  background: transparent;
}

.template-card {
  margin-bottom: 10px;
  padding: 11px 12px 9px 13px;
  border: 1px solid #e6ebf2;
  border-radius: 10px;
  background: #fff;
  box-shadow: 0 3px 10px rgba(23, 52, 95, 0.03);
  transition: transform 0.16s ease, border-color 0.16s ease, box-shadow 0.16s ease;
}

.template-card:hover {
  transform: translateY(-1px);
  border-color: #c7d8eb;
  box-shadow: 0 8px 18px rgba(23, 52, 95, 0.08);
}

.template-card__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
}

.template-card__title {
  flex: 1;
  min-width: 0;
  font-size: 13px;
  font-weight: 600;
  line-height: 1.45;
  color: #17345f;
  display: -webkit-box;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.template-card__header .el-tag {
  flex: 0 0 auto;
  margin-top: 1px;
  line-height: 18px;
}

.template-card__body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: 10px;
  margin-top: 9px;
}

.template-card__audit {
  display: flex;
  flex-direction: column;
  gap: 1px;
  font-size: 11px;
  line-height: 18px;
  color: #8a97a8;
}

.template-card__audit span {
  display: flex;
  align-items: center;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.template-card__audit i {
  flex: 0 0 auto;
  margin-right: 4px;
  color: #a7b4c4;
}

.template-card__actions {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
  white-space: nowrap;
}

.render-panel,
.chat-panel {
  min-height: 0;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 16px 36px rgba(15, 23, 42, 0.08);
  overflow: hidden;
}

.render-panel {
  width: auto;
  max-width: none;
  justify-self: stretch;
  min-width: 0;
  margin: 0 5px;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 16px;
}

.render-panel.has-product-selector {
  z-index: 10;
  overflow: visible;
}

.chat-resizer {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: stretch;
  justify-content: center;
  cursor: col-resize;
  touch-action: none;
  outline: none;
}

.chat-resizer::before {
  width: 0;
  margin: 18px 0;
  content: '';
  transition: width 0.16s ease;
}

.chat-resizer::after {
  position: absolute;
  z-index: 1;
  top: 0;
  right: -6px;
  bottom: 0;
  left: -6px;
  content: '';
}

.chat-resizer__grip {
  position: absolute;
  z-index: 2;
  top: 50%;
  left: 50%;
  width: 20px;
  height: 48px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  border: 1px solid #cbddec;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 4px 12px rgba(32, 69, 106, 0.12);
  transform: translate(-50%, -50%);
  transition: border-color 0.16s ease, box-shadow 0.16s ease, transform 0.16s ease;
}

.chat-resizer__grip i {
  width: 3px;
  height: 3px;
  border-radius: 50%;
  background: #90a7bf;
}

.chat-resizer__hint {
  position: absolute;
  z-index: 4;
  top: 50%;
  left: 50%;
  width: max-content;
  padding: 6px 9px;
  border-radius: 7px;
  background: #17345f;
  box-shadow: 0 6px 16px rgba(15, 41, 73, 0.18);
  color: #fff;
  font-size: 12px;
  line-height: 1.3;
  pointer-events: none;
  transform: translate(16px, -50%);
}

.chat-resizer:hover::before,
.chat-resizer.is-active::before,
.chat-resizer:focus::before {
  width: 0;
}

.chat-resizer:hover .chat-resizer__grip,
.chat-resizer.is-active .chat-resizer__grip,
.chat-resizer:focus .chat-resizer__grip {
  border-color: #5a95ca;
  box-shadow: 0 6px 16px rgba(45, 114, 177, 0.24);
  transform: translate(-50%, -50%) scale(1.06);
}

.chat-resizer:hover .chat-resizer__grip i,
.chat-resizer.is-active .chat-resizer__grip i,
.chat-resizer:focus .chat-resizer__grip i {
  background: #397cb9;
}

.chat-resizer:focus-visible {
  box-shadow: inset 0 0 0 1px #5a95ca;
}

.render-toolbar,
.chat-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 16px;
}

.render-toolbar {
  align-items: center;
  flex-wrap: nowrap;
}

.render-toolbar__main {
  flex: 1 1 auto;
  min-width: 0;
}

.render-title,
.chat-title {
  font-size: 18px;
  font-weight: 700;
  color: #17345f;
}

.render-title {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.render-report-toc-trigger {
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 0 7px;
  border: 1px solid #dce7f3;
  border-radius: 5px;
  background: #f8fbff;
  color: #6f87a0;
  font-size: 12px;
  line-height: 1;
  cursor: pointer;
  transition: background-color 0.16s ease, color 0.16s ease;
}

.render-report-toc-trigger:hover {
  border-color: #8fb7dc;
  background: #edf4fc;
  color: #245d96;
}

.render-report-toc-trigger.is-active {
  border-color: #a9c9e7;
  background: #eaf3fc;
  color: #245d96;
}

.render-report-toc-trigger small {
  min-width: 14px;
  padding: 1px 3px;
  border-radius: 8px;
  background: #d9eafb;
  color: #3972a7;
  font-size: 10px;
  line-height: 1.2;
  text-align: center;
}

.report-toc-trigger-icon {
  width: 16px;
  height: 16px;
  fill: currentColor;
  stroke: currentColor;
  stroke-linecap: round;
  stroke-width: 1.4;
}

.render-meta,
.chat-status,
.block-meta,
.notice-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  font-size: 12px;
  color: #7b8794;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  flex: 0 0 auto;
  min-width: 0;
  flex-wrap: nowrap;
  gap: 8px;
  white-space: nowrap;
}

.toolbar-actions .el-switch,
.toolbar-actions .el-button,
.selected-chip {
  flex: 0 0 auto;
}

.toolbar-actions .el-button {
  padding-left: 10px;
  padding-right: 10px;
}

.selected-chip {
  max-width: none;
  padding: 6px 10px;
  border-radius: 999px;
  background: #edf4fc;
  color: #153b67;
  font-size: 12px;
  white-space: normal;
  overflow-wrap: anywhere;
}

.render-export-pdf.el-button {
  flex: 0 0 auto;
  border: 0;
  border-radius: 8px;
  background: linear-gradient(135deg, #e8a873 0%, #d88b58 100%);
  box-shadow: 0 5px 12px rgba(184, 111, 61, 0.18);
}

.render-export-pdf.el-button:hover,
.render-export-pdf.el-button:focus {
  background: linear-gradient(135deg, #efb887 0%, #df9664 100%);
}

.global-query-panel {
  flex: 0 0 auto;
  margin: -2px 0 12px;
  padding: 12px 14px;
  border: 1px solid #dce7f3;
  border-radius: 14px;
  background: linear-gradient(135deg, #fbfdff 0%, #f3f8fd 100%);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.global-query-panel__head,
.global-query-panel__main,
.global-query-more__footer {
  display: flex;
  align-items: center;
}

.global-query-panel__head {
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.global-query-panel__title {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #24466e;
  font-size: 13px;
  font-weight: 700;
}

.global-query-panel__title i {
  color: #4a8fd1;
  font-size: 14px;
}

.global-query-panel__hint {
  margin-top: 3px;
  color: #8a99aa;
  font-size: 11px;
}

.global-query-panel__status {
  flex: 0 0 auto;
  padding: 4px 9px;
  border-radius: 999px;
  background: #edf3f9;
  color: #8291a2;
  font-size: 11px;
}

.global-query-panel__status.is-active {
  background: #e5f2ff;
  color: #2f78b8;
}

.global-query-panel__main {
  gap: 10px;
  flex-wrap: wrap;
}

.global-query-field {
  display: flex;
  align-items: center;
  gap: 7px;
  min-width: 0;
  color: #60758c;
  font-size: 12px;
  white-space: nowrap;
}

.global-query-field > span {
  flex: 0 0 auto;
}

.global-query-field .el-input,
.global-query-field .el-select,
.global-query-field .el-date-editor {
  width: 148px;
}

.global-query-field--date .el-date-editor {
  width: 154px;
}

.global-query-field--product {
  flex: 1 1 190px;
}

.global-query-field--product .el-input {
  width: 100%;
  max-width: 220px;
}

.global-query-panel__actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.global-query-more-toggle {
  height: 32px;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 0 9px;
  border: 1px solid #d7e3ef;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.76);
  color: #55718e;
  font-size: 12px;
  cursor: pointer;
  transition: color 0.16s ease, border-color 0.16s ease, background-color 0.16s ease;
}

.global-query-more-toggle:hover,
.global-query-more-toggle.is-open {
  border-color: #a8c9e9;
  background: #f4f9ff;
  color: #2365a0;
}

.global-query-more-toggle em {
  min-width: 17px;
  height: 17px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  background: #e6f1fc;
  color: #3675ad;
  font-size: 10px;
  font-style: normal;
}

.global-query-more-toggle__arrow {
  transition: transform 0.18s ease;
}

.global-query-more-toggle.is-open .global-query-more-toggle__arrow {
  transform: rotate(180deg);
}

.global-query-apply.el-button {
  height: 32px;
  margin: 0;
  padding: 0 13px;
  border: 0;
  border-radius: 8px;
  background: linear-gradient(135deg, #4c91d1 0%, #3377ba 100%);
  box-shadow: 0 5px 12px rgba(50, 116, 182, 0.18);
  font-size: 12px;
}

.global-query-apply.el-button:hover,
.global-query-apply.el-button:focus {
  background: linear-gradient(135deg, #5b9ddd 0%, #3d83c6 100%);
}

.global-query-more {
  margin-top: 10px;
  padding: 12px 12px 8px;
  border: 1px solid #dce8f3;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.78);
}

.global-query-more__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(150px, 1fr));
  gap: 10px 16px;
}

.global-query-more__footer {
  margin-top: 10px;
  color: #8a99aa;
  font-size: 11px;
}

.global-query-more__footer i {
  margin-right: 4px;
  color: #76a8d1;
}

.query-more-enter-active,
.query-more-leave-active {
  overflow: hidden;
  transition: max-height 0.2s ease, opacity 0.16s ease, margin-top 0.2s ease, padding 0.2s ease;
}

.query-more-enter,
.query-more-leave-to {
  max-height: 0;
  margin-top: 0;
  padding-top: 0;
  padding-bottom: 0;
  opacity: 0;
}

.query-more-enter-to,
.query-more-leave {
  max-height: 260px;
  opacity: 1;
}

.report-scroll {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding: 8px 8px 14px;
  border-radius: 14px;
  background: #f3f6fa;
  overscroll-behavior: contain;
  scroll-padding-top: 8px;
}

.empty-render {
  min-height: 320px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: #6b7280;
  border: 1px dashed #d7deea;
  border-radius: 18px;
  background: #f8fbff;
}

.empty-render__title {
  font-size: 20px;
  font-weight: 700;
  color: #17345f;
  margin-bottom: 8px;
}

.empty-render__message {
  width: min(100%, 720px);
  color: #526174;
  text-align: left;
}

.markdown-body {
  line-height: 1.7;
  overflow-wrap: anywhere;
  word-break: break-word;
}

.clarify-list .markdown-body,
.notice-questions .markdown-body {
  display: inline;
}

.report-notices {
  margin-bottom: 16px;
}

.report-notice {
  margin-bottom: 12px;
  padding: 14px 16px;
  border: 1px solid #d9e5f4;
  border-radius: 16px;
  background: #f8fbff;
}

.report-notice.is-clarify {
  border-color: #bcd8f5;
  background: #f3f8ff;
}

.report-notice.is-rejected {
  border-color: #f1c7c7;
  background: #fff7f7;
}

.report-notice.is-error {
  border-color: #f3b9b9;
  background: #fff4f4;
}

.notice-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 10px;
}

.notice-title {
  font-size: 15px;
  font-weight: 700;
  color: #17345f;
}

.notice-actions {
  display: flex;
  gap: 6px;
}

.notice-message {
  color: #2f3a4b;
}

.notice-questions {
  margin: 10px 0 0;
  padding-left: 20px;
  color: #2f3a4b;
}

.notice-debug {
  margin-top: 10px;
  padding: 8px 10px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.72);
  color: #6b7280;
  font-size: 12px;
}

.notice-debug summary {
  cursor: pointer;
  font-weight: 700;
}

.notice-debug-line {
  margin-top: 6px;
  word-break: break-all;
}

.report-grid {
  min-height: 100%;
  padding-bottom: 4px;
}

.report-grid-item {
  touch-action: none;
}

.report-block {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border: 1px solid #e8edf5;
  border-radius: 18px;
  background: #fff;
  overflow: hidden;
}

.report-block.is-selected {
  border-color: #153b67;
  box-shadow: 0 0 0 3px rgba(21, 59, 103, 0.08);
}

.report-block.is-multi-selected {
  border-color: #8cb6e5;
  box-shadow: 0 0 0 2px rgba(96, 151, 215, 0.12);
}

.report-group {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 16px;
  border: 1px solid #d9e5f4;
  border-radius: 18px;
  background: #f8fbff;
  overflow: hidden;
}

.group-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.group-header__main {
  flex: 1;
  min-width: 0;
}

.group-title-input {
  max-width: 320px;
}

.report-group-grid {
  flex: 1;
  min-height: 220px;
}

.report-grid-item--nested {
  touch-action: none;
}

.block-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 12px;
}

.block-header__main {
  flex: 1;
  min-width: 0;
}

.block-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.block-selector {
  flex: 0 0 auto;
}

.drag-handle {
  width: 26px;
  height: 26px;
  border: 1px solid #d8e3ef;
  border-radius: 8px;
  background: #f8fbff;
  color: #5d7391;
  cursor: move;
}

.block-title {
  font-size: 16px;
  font-weight: 700;
  color: #17345f;
  min-width: 0;
  word-break: break-word;
}

.block-title-editor {
  flex: 1 1 360px;
  max-width: 520px;
}

.block-title-editor >>> .el-input__inner {
  height: 30px;
  line-height: 30px;
  padding: 0 10px;
  border-color: #8bb7e8;
  color: #17345f;
  font-size: 16px;
  font-weight: 700;
}

.block-title-edit-button {
  flex: 0 0 auto;
  padding: 3px 4px;
  color: #8aa0b8;
}

.block-title-edit-button:hover,
.block-title-edit-button:focus {
  color: #2f76b7;
}

.block-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.block-content {
  flex: 1;
  min-height: 0;
  position: relative;
  overflow: hidden;
}

.block-watermark {
  position: absolute;
  inset: 0;
  z-index: 5;
  pointer-events: none;
  overflow: hidden;
  color: transparent;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='235' height='124' viewBox='0 0 235 124'%3E%3Cg transform='translate(26 50) rotate(-24)' opacity='0.24'%3E%3Crect x='0' y='8' width='17' height='17' rx='3' fill='none' stroke='%236b7280' stroke-width='3'/%3E%3Ccircle cx='8.5' cy='16.5' r='3' fill='%236b7280'/%3E%3Ctext x='26' y='15' font-family='Arial,sans-serif' font-size='14' font-weight='700' fill='%236b7280'%3E%E7%A4%BA%E4%BE%8B%E6%95%B0%E6%8D%AE%3C/text%3E%3Ctext x='26' y='30' font-family='Arial,sans-serif' font-size='10' font-weight='600' fill='%236b7280'%3EEXAMPLE DATA%3C/text%3E%3C/g%3E%3C/svg%3E");
  background-repeat: repeat;
  background-size: 235px 124px;
  background-position: 4px 2px;
  opacity: 0.82;
}

.report-block--nested {
  padding: 12px;
  border-radius: 14px;
}

.block-chart,
.block-table {
  height: 100%;
}

.block-table {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.block-table .vxe-table {
  flex: 1;
  min-height: 0;
}

.block-diagnostics {
  padding: 8px 10px;
  border: 1px solid #f0d8a8;
  border-radius: 10px;
  background: #fff9ed;
  color: #7a4b00;
  font-size: 12px;
}

.block-diagnostics summary {
  cursor: pointer;
  font-weight: 700;
}

.diagnostic-item {
  display: flex;
  gap: 8px;
  margin-top: 6px;
  line-height: 1.5;
  word-break: break-all;
}

.chat-panel {
  width: 100%;
  min-width: 0;
  padding: 16px;
  display: flex;
  flex-direction: column;
}

.message-list {
  flex: 1;
  min-height: 0;
  overflow: auto;
  padding-right: 4px;
}

.message-row {
  margin-bottom: 12px;
  display: flex;
}

.message-row.is-user {
  justify-content: flex-end;
}

.message-bubble {
  max-width: 100%;
  padding: 12px 14px;
  border-radius: 16px;
  background: #f5f8fd;
}

.message-row.is-user .message-bubble {
  background: #17345f;
  color: #fff;
}

.message-name {
  font-size: 12px;
  font-weight: 700;
  margin-bottom: 6px;
}

.message-content {
  color: inherit;
}

.thinking-box {
  margin-top: 8px;
  padding: 8px 10px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.65);
  color: #2f3a4b;
  overflow: hidden;
}

.message-row.is-user .thinking-box {
  background: rgba(255, 255, 255, 0.12);
  color: #fff;
}

.thinking-label {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0;
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
  font-size: 12px;
  font-weight: 700;
  text-align: left;
}

.thinking-toggle-icon {
  margin-left: auto;
  color: #8a9aae;
  font-size: 13px;
}

.thinking-box.is-collapsed {
  padding-top: 7px;
  padding-bottom: 7px;
}

.thinking-text {
  max-height: 220px;
  margin: 8px 0 0;
  padding-right: 6px;
  font-size: 12px;
  line-height: 1.5;
  white-space: pre-wrap;
  overflow-y: auto;
  overscroll-behavior: auto;
  overflow-wrap: anywhere;
}

.stream-status,
.metrics-line {
  margin-top: 8px;
  font-size: 12px;
  color: #7b8794;
}

.message-row.is-user .stream-status,
.message-row.is-user .metrics-line {
  color: rgba(255, 255, 255, 0.85);
}

.metrics-toggle,
.link-button {
  margin-left: 8px;
  border: none;
  background: transparent;
  color: inherit;
  cursor: pointer;
  text-decoration: underline;
}

.composer {
  margin-top: 14px;
}

.composer-context {
  margin-bottom: 8px;
  padding: 10px 12px;
  border-radius: 12px;
  background: #edf4fc;
  color: #17345f;
  font-size: 12px;
}

.composer-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

.example-trigger {
  position: relative;
  margin-right: auto;
}

.example-backdrop {
  position: fixed;
  inset: 0;
  z-index: 8;
}

.example-panel {
  position: absolute;
  bottom: calc(100% + 8px);
  left: 0;
  width: 320px;
  max-height: 360px;
  z-index: 9;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18), 0 0 0 1px rgba(15, 23, 42, 0.06);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.example-panel__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid #edf1f7;
  font-size: 14px;
  font-weight: 600;
  color: #17345f;
  flex-shrink: 0;
}

.example-panel__close {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 8px;
  background: transparent;
  font-size: 18px;
  color: #6f7f92;
  cursor: pointer;
}

.example-panel__close:hover {
  background: #f0f3f8;
  color: #17345f;
}

.example-panel__list {
  overflow-y: auto;
  padding: 8px;
  flex: 1;
}

.example-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  border-radius: 10px;
  background: transparent;
  text-align: left;
  cursor: pointer;
  color: #2c3e50;
  font-size: 13px;
  line-height: 1.55;
}

.example-item:hover {
  background: #f2f7fd;
}

.example-item__index {
  flex: 0 0 auto;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  background: #edf4fc;
  color: #17345f;
  font-size: 12px;
  font-weight: 600;
  margin-top: 1px;
}

.example-item:hover .example-item__index {
  background: #17345f;
  color: #fff;
}

.example-item__text {
  flex: 1;
  min-width: 0;
}

@media (max-width: 1280px) {
  .vm-chat-page {
    display: flex;
    flex-direction: column;
    height: auto;
  }

  .module-sidebar {
    margin-right: 0;
    min-height: 0;
    align-items: stretch;
  }

  .report-toc {
    top: 72px;
    right: 16px;
    bottom: 16px;
    width: 268px;
  }

  .report-toc.is-collapsed {
    right: auto;
    width: 30px;
  }

  .chat-panel {
    width: 100%;
    min-width: 0;
  }

  .chat-resizer {
    display: none;
  }

  .global-query-panel__main {
    align-items: stretch;
  }

  .global-query-panel__actions {
    margin-left: 0;
  }

  .global-query-more__grid {
    grid-template-columns: repeat(2, minmax(150px, 1fr));
  }
}
</style>

<style>
/* v-html 生成的 Markdown 节点没有 scoped 属性，使用全局规则保证结构化内容可读。 */
.markdown-body > :first-child { margin-top: 0; }
.markdown-body > :last-child { margin-bottom: 0; }
.markdown-body p { margin: 0 0 8px; }
.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 {
  margin: 12px 0 6px;
  color: #17345f;
  line-height: 1.35;
}
.markdown-body h1 { font-size: 18px; }
.markdown-body h2 { font-size: 16px; }
.markdown-body h3,
.markdown-body h4,
.markdown-body h5,
.markdown-body h6 { font-size: 14px; }
.markdown-body ul,
.markdown-body ol {
  margin: 6px 0 10px;
  padding-left: 22px;
}
.markdown-body li + li { margin-top: 4px; }
.markdown-body blockquote {
  margin: 8px 0;
  padding: 6px 10px;
  border-left: 3px solid #9fc3e8;
  background: #f3f7fc;
  color: #637286;
}
.markdown-body code {
  padding: 1px 4px;
  border-radius: 4px;
  background: #eef2f7;
  color: #1d5ea8;
  font-size: 0.92em;
}
.markdown-body pre {
  margin: 8px 0;
  padding: 9px 10px;
  overflow-x: auto;
  border-radius: 8px;
  background: #eef2f7;
  color: #334155;
  white-space: pre-wrap;
}
.markdown-body pre code { padding: 0; background: transparent; color: inherit; }
.markdown-body table {
  width: 100%;
  margin: 8px 0;
  border-collapse: collapse;
  font-size: 12px;
}
.markdown-body th,
.markdown-body td {
  padding: 6px 8px;
  border: 1px solid #dce5f0;
  text-align: left;
  vertical-align: top;
}
.markdown-body th { background: #f2f6fb; color: #17345f; font-weight: 700; }
.markdown-body a { color: #1d5ea8; text-decoration: underline; }
.wiki-dialog .el-dialog__header {
  padding: 16px 20px;
  border-bottom: 1px solid #eef2f7;
  background: #f8fafc;
}
.wiki-dialog {
  margin-top: 7vh !important;
}
.wiki-dialog .el-dialog__title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}
.wiki-dialog .el-dialog__body {
  padding: 0;
  height: min(78vh, 820px);
  overflow: hidden;
}
.wiki-container {
  display: flex;
  height: 100%;
  background: #fff;
}
.wiki-sidebar {
  width: 320px;
  flex-shrink: 0;
  border-right: 1px solid #e2e2e3;
  background: #fff;
  padding: 20px 12px;
  overflow-y: auto;
}
.wiki-tree-filter {
  display: block;
  width: 100%;
  box-sizing: border-box;
  margin-bottom: 12px;
}
.wiki-tree-loading,
.wiki-tree-error {
  padding: 20px 12px;
  text-align: center;
  color: #64748b;
  font-size: 13px;
}
.wiki-sidebar .el-tree {
  background: transparent;
  color: #213547;
  font-size: 13px;
}
.wiki-sidebar .el-tree-node__content {
  height: 30px;
  border-radius: 4px;
}
.wiki-sidebar .el-tree-node__content:hover {
  color: #3451b2;
  background: #f6f6f7;
}
.wiki-sidebar .el-tree-node.is-current > .el-tree-node__content {
  background: #e7efff;
  color: #3451b2;
  font-weight: 600;
}
.wiki-content {
  flex: 1;
  min-width: 0;
  padding: 18px 48px 96px;
  overflow-y: auto;
  background: #fff;
}
.wiki-search-bar {
  position: sticky;
  z-index: 2;
  top: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 900px;
  margin: 0 auto 28px;
  padding: 8px;
  border: 1px solid #dbe7f3;
  border-radius: 8px;
  background: rgba(248, 250, 252, 0.96);
  box-shadow: 0 4px 12px rgba(32, 69, 106, 0.06);
}
.wiki-search-bar .el-input {
  flex: 1;
}
.wiki-search-count {
  min-width: 42px;
  color: #64748b;
  font-size: 12px;
  text-align: center;
  white-space: nowrap;
}
.wiki-document-content .wiki-search-match {
  padding: 0 2px;
  border-radius: 2px;
  background: #fff3a6;
  color: inherit;
}
.wiki-document-content .wiki-search-match.is-current {
  background: #f8cf58;
  box-shadow: 0 0 0 1px rgba(186, 133, 17, 0.28);
}
.wiki-state-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #64748b;
  font-size: 14px;
  gap: 12px;
}
.wiki-state-box--error {
  color: #ef4444;
}
.wiki-document-content {
  max-width: 900px;
  margin: 0 auto;
  color: #334155;
  font-size: 16px;
  line-height: 1.75;
}
.wiki-document-content .wiki-frontmatter {
  margin: 0 0 32px;
  padding: 16px 18px;
  border: 1px solid #e2e2e3;
  border-radius: 8px;
  background: #f8fafc;
  color: #476582;
  font-family: var(--vp-font-family-mono, Menlo, Monaco, Consolas, 'Courier New', monospace);
  font-size: 13px;
  line-height: 1.65;
}
.wiki-document-content .wiki-frontmatter p {
  margin: 0;
}
.wiki-document-content .wiki-frontmatter strong {
  margin-right: 6px;
  color: #213547;
  font-weight: 600;
}
.wiki-document-content h1,
.wiki-document-content h2,
.wiki-document-content h3,
.wiki-document-content h4,
.wiki-document-content h5,
.wiki-document-content h6 {
  color: #213547;
  font-weight: 600;
}
.wiki-document-content h1 {
  margin: 0 0 28px;
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e2e3;
  font-size: 30px;
  letter-spacing: -0.01em;
}
.wiki-document-content h2 {
  margin: 40px 0 16px;
  padding-top: 20px;
  border-top: 1px solid #e2e2e3;
  font-size: 23px;
}
.wiki-document-content h3 {
  margin: 28px 0 10px;
  font-size: 19px;
}
.wiki-document-content p {
  margin: 16px 0;
}
.wiki-document-content ul,
.wiki-document-content ol {
  margin: 16px 0;
  padding-left: 24px;
}
.wiki-document-content ul {
  list-style: disc;
}
.wiki-document-content ul ul {
  margin: 6px 0;
  list-style: circle;
}
.wiki-document-content ol {
  list-style: decimal;
}
.wiki-document-content li::marker {
  color: #3451b2;
}
.wiki-document-content li + li {
  margin-top: 6px;
}
.wiki-document-content blockquote {
  margin: 20px 0;
  padding: 12px 16px;
  border-left-color: #3451b2;
  border-radius: 0 4px 4px 0;
  background: #f6f6f7;
  color: #476582;
}
.wiki-document-content code {
  display: inline-block;
  padding: 2px 5px;
  border-radius: 4px;
  background: #f6f6f7;
  color: #3451b2;
  white-space: nowrap;
}
.wiki-document-content pre {
  margin: 18px 0;
  padding: 14px 16px;
  overflow-x: hidden;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #f6f8fa;
  color: #334155;
  font-size: 13px;
  line-height: 1.6;
}
.wiki-document-content pre code {
  display: block;
  color: inherit;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  word-break: break-word;
}
.wiki-document-content pre.wiki-json-code-block {
  border-left: 3px solid #93b4d4;
  background: #f7f9fc;
}
.wiki-document-content .cm-property { color: #1f5d99; }
.wiki-document-content .cm-string { color: #15805d; }
.wiki-document-content .cm-number { color: #b35528; }
.wiki-document-content .cm-atom { color: #7b4fab; }
.wiki-document-content .cm-bracket { color: #53657a; }
.wiki-document-content a {
  color: #3451b2;
  font-weight: 500;
  text-decoration: none;
}
.wiki-document-content a:hover {
  color: #5672cd;
  text-decoration: underline;
}
.wiki-document-content table {
  width: 100%;
  margin: 18px 0;
  font-size: 14px;
  border-collapse: collapse;
}
.wiki-document-content th {
  background: #f4f6f8;
  color: #213547;
  font-weight: 600;
}
.wiki-document-content th,
.wiki-document-content td {
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  vertical-align: top;
}

@media (max-width: 768px) {
  .wiki-dialog .el-dialog__body {
    height: 75vh;
  }
  .wiki-container {
    flex-direction: column;
  }
  .wiki-sidebar {
    width: 100%;
    max-height: 180px;
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  .wiki-content {
    padding: 16px;
  }
}
</style>
