function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

function createId(prefix) {
  return prefix + '-' + Date.now().toString(36) + '-' + Math.random().toString(16).slice(2, 8)
}

function createBlockMap(blocks) {
  return (Array.isArray(blocks) ? blocks : []).reduce((accumulator, block) => {
    if (block && block.blockId) accumulator[block.blockId] = clone(block)
    return accumulator
  }, {})
}

function getBlockWidgetHeight(block) {
  return block && (block.type === 'echarts' || block.viewType === 'echarts') ? 10 : 8
}

function createEntityKey(type, id) {
  return String(type) + ':' + String(id)
}

function parseEntityKey(entityKey) {
  const source = String(entityKey || '')
  const index = source.indexOf(':')
  if (index < 0) return { type: 'block', id: source }
  return {
    type: source.slice(0, index),
    id: source.slice(index + 1)
  }
}

function createWidget(id, position, defaults) {
  const pos = position || {}
  const base = defaults || {}
  return {
    i: String(id),
    x: Number(pos.x != null ? pos.x : base.x || 0),
    y: Number(pos.y != null ? pos.y : base.y || 0),
    w: Number(pos.w != null ? pos.w : base.w || 24),
    h: Number(pos.h != null ? pos.h : base.h || 8),
    minW: Number(pos.minW != null ? pos.minW : base.minW || 6),
    minH: Number(pos.minH != null ? pos.minH : base.minH || 6)
  }
}

function sortWidgets(widgets) {
  return clone(Array.isArray(widgets) ? widgets : []).sort((left, right) => {
    if (left.y !== right.y) return left.y - right.y
    if (left.x !== right.x) return left.x - right.x
    return String(left.i).localeCompare(String(right.i))
  })
}

function getMaxBottom(widgets) {
  return (Array.isArray(widgets) ? widgets : []).reduce((maxValue, widget) => {
    const bottom = Number(widget.y || 0) + Number(widget.h || 0)
    return Math.max(maxValue, bottom)
  }, 0)
}

function getNextLayoutPosition(widgets) {
  return {
    x: 0,
    y: getMaxBottom(widgets),
    w: 24
  }
}

function createTopLevelBlockWidget(block, position) {
  return createWidget(createEntityKey('block', block.blockId), position, {
    x: 0,
    y: 0,
    w: 24,
    h: getBlockWidgetHeight(block),
    minW: 6,
    minH: 6
  })
}

function createGroupChildWidget(block, position) {
  return createWidget(block.blockId, position, {
    x: 0,
    y: 0,
    w: 24,
    h: getBlockWidgetHeight(block),
    minW: 6,
    minH: 6
  })
}

function getGroupWidgetHeight(group) {
  const innerHeight = getMaxBottom(group && group.widgets ? group.widgets : [])
  return Math.max(12, innerHeight + 4)
}

function createTopLevelGroupWidget(group, position) {
  return createWidget(createEntityKey('group', group.groupId), position, {
    x: 0,
    y: 0,
    w: 24,
    h: getGroupWidgetHeight(group),
    minW: 6,
    minH: 10
  })
}

function normalizeState(state) {
  const source = state || {}
  return {
    blocksById: clone(source.blocksById || {}),
    groupsById: clone(source.groupsById || {}),
    widgets: clone(source.widgets || [])
  }
}

function createCanvasStateFromBlocks(blocks) {
  const list = Array.isArray(blocks) ? blocks.map(item => clone(item)) : []
  const widgets = []
  list.forEach(block => {
    widgets.push(createTopLevelBlockWidget(block, getNextLayoutPosition(widgets)))
  })
  return {
    blocksById: createBlockMap(list),
    groupsById: {},
    widgets
  }
}

function getTopLevelWidgetIndex(state, entityKey) {
  return (state.widgets || []).findIndex(widget => widget.i === entityKey)
}

function findBlockLocation(state, blockId) {
  const standaloneWidgetIndex = getTopLevelWidgetIndex(state, createEntityKey('block', blockId))
  if (standaloneWidgetIndex >= 0 && state.blocksById && state.blocksById[blockId]) {
    return {
      container: 'top-level',
      blockId,
      widgetIndex: standaloneWidgetIndex
    }
  }
  const groupsById = state.groupsById || {}
  const groupIds = Object.keys(groupsById)
  for (let index = 0; index < groupIds.length; index += 1) {
    const groupId = groupIds[index]
    const group = groupsById[groupId]
    if (!group || !group.blocksById || !group.blocksById[blockId]) continue
    const childWidgetIndex = (group.widgets || []).findIndex(widget => widget.i === blockId)
    if (childWidgetIndex < 0) continue
    return {
      container: 'group',
      blockId,
      groupId,
      childWidgetIndex
    }
  }
  return null
}

function getOrderedTopLevelItems(state) {
  return sortWidgets(state && state.widgets).map(widget => {
    const descriptor = parseEntityKey(widget.i)
    if (descriptor.type === 'group') {
      const group = state.groupsById && state.groupsById[descriptor.id]
      return group ? { kind: 'group', widget, group } : null
    }
    const block = state.blocksById && state.blocksById[descriptor.id]
    return block ? { kind: 'block', widget, block } : null
  }).filter(Boolean)
}

function getOrderedGroupBlocks(group) {
  return sortWidgets(group && group.widgets).map(widget => {
    return group && group.blocksById && group.blocksById[widget.i]
  }).filter(Boolean)
}

function getOrderedBlocks(state) {
  return getOrderedTopLevelItems(state).reduce((accumulator, item) => {
    if (item.kind === 'block') {
      accumulator.push(item.block)
      return accumulator
    }
    return accumulator.concat(getOrderedGroupBlocks(item.group))
  }, [])
}

function appendBlockWidget(state, block, position) {
  const next = normalizeState(state)
  const nextBlock = clone(block)
  if (!nextBlock.blockId) throw new Error('create 缺少 blockId')
  if (findBlockLocation(next, nextBlock.blockId) || next.blocksById[nextBlock.blockId]) {
    throw new Error('create blockId 已存在，不允许覆盖已有报表块：' + nextBlock.blockId)
  }
  next.blocksById[nextBlock.blockId] = nextBlock
  next.widgets.push(createTopLevelBlockWidget(nextBlock, position || getNextLayoutPosition(next.widgets)))
  return next
}

function replaceBlockWidget(state, targetBlockId, block) {
  const next = normalizeState(state)
  const location = findBlockLocation(next, targetBlockId)
  const nextBlock = clone(block)
  nextBlock.blockId = targetBlockId
  if (!location) {
    throw new Error('update 目标已不存在，不允许隐式新增报表块：' + targetBlockId)
  }
  const currentBlock = location.container === 'top-level'
    ? next.blocksById[targetBlockId]
    : next.groupsById[location.groupId] && next.groupsById[location.groupId].blocksById[targetBlockId]
  if (currentBlock && currentBlock.sourceTemplateId && !nextBlock.sourceTemplateId) {
    nextBlock.sourceTemplateId = currentBlock.sourceTemplateId
    nextBlock.sourceTemplateType = currentBlock.sourceTemplateType
  }
  if (location.container === 'top-level') {
    next.blocksById[targetBlockId] = nextBlock
    const currentWidget = next.widgets[location.widgetIndex]
    next.widgets[location.widgetIndex] = Object.assign({}, currentWidget, {
      i: createEntityKey('block', targetBlockId),
      h: currentWidget.h || getBlockWidgetHeight(nextBlock)
    })
    return next
  }
  const group = next.groupsById[location.groupId]
  group.blocksById[targetBlockId] = nextBlock
  const currentWidget = group.widgets[location.childWidgetIndex]
  group.widgets[location.childWidgetIndex] = Object.assign({}, currentWidget, {
    i: targetBlockId,
    h: currentWidget.h || getBlockWidgetHeight(nextBlock)
  })
  const topLevelWidgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', location.groupId))
  if (topLevelWidgetIndex >= 0) {
    next.widgets[topLevelWidgetIndex].h = getGroupWidgetHeight(group)
  }
  return next
}

function removeGroupIfEmpty(state, groupId) {
  const next = state
  const group = next.groupsById[groupId]
  if (!group) return next
  if (Object.keys(group.blocksById || {}).length) return next
  delete next.groupsById[groupId]
  const widgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', groupId))
  if (widgetIndex >= 0) next.widgets.splice(widgetIndex, 1)
  return next
}

function removeBlockWidget(state, blockId) {
  const next = normalizeState(state)
  const location = findBlockLocation(next, blockId)
  if (!location) return next
  if (location.container === 'top-level') {
    delete next.blocksById[blockId]
    next.widgets.splice(location.widgetIndex, 1)
    return next
  }
  const group = next.groupsById[location.groupId]
  delete group.blocksById[blockId]
  group.widgets.splice(location.childWidgetIndex, 1)
  removeGroupIfEmpty(next, location.groupId)
  const groupWidgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', location.groupId))
  if (groupWidgetIndex >= 0 && next.groupsById[location.groupId]) {
    next.widgets[groupWidgetIndex].h = getGroupWidgetHeight(next.groupsById[location.groupId])
  }
  return next
}

function sanitizeBlockForTemplate(block) {
  const source = clone(block || {})
  delete source.sourceTemplateId
  delete source.sourceTemplateType
  delete source.sourceData
  delete source.renderState
  delete source.requestDiagnostics
  delete source.transformDiagnostics
  delete source.renderSnapshot
  delete source.updatedAt
  delete source.createdAt
  delete source.renderSpec
  source.blockId = source.dsl && source.dsl.id || ''
  return source
}

function serializeBlockTemplate(block, widgetHeight) {
  const sanitized = sanitizeBlockForTemplate(block)
  const payload = {
    block: sanitized
  }
  if (widgetHeight != null) {
    payload.height = widgetHeight
  }
  return {
    entityType: 'vm-block-template',
    title: sanitized.title || '未命名模块',
    payload
  }
}

function serializeGroupTemplate(group) {
  if (!group) return null
  return {
    entityType: 'vm-group-template',
    title: String(group.title || '未命名组合').trim() || '未命名组合',
    payload: {
      group: {
        title: String(group.title || '未命名组合').trim() || '未命名组合',
        widgets: sortWidgets(group.widgets).map(widget => ({
          x: widget.x,
          y: widget.y,
          w: widget.w,
          h: widget.h,
          block: sanitizeBlockForTemplate(group.blocksById[widget.i])
        }))
      }
    }
  }
}

function serializeLayoutTemplate(state, title) {
  const items = getOrderedTopLevelItems(state)
  if (!items.length) return null
  const minX = Math.min.apply(null, items.map(item => item.widget.x))
  const minY = Math.min.apply(null, items.map(item => item.widget.y))
  return {
    entityType: 'vm-grid-layout-template',
    title: String(title || '自定义布局').trim() || '自定义布局',
    payload: {
      items: items.map(item => {
        if (item.kind === 'block') {
          return {
            type: 'block',
            x: item.widget.x - minX,
            y: item.widget.y - minY,
            w: item.widget.w,
            h: item.widget.h,
            block: sanitizeBlockForTemplate(item.block)
          }
        }
        return {
          type: 'group',
          x: item.widget.x - minX,
          y: item.widget.y - minY,
          w: item.widget.w,
          h: item.widget.h,
          title: item.group.title || '未命名组合',
          items: sortWidgets(item.group.widgets).map(widget => ({
            x: widget.x,
            y: widget.y,
            w: widget.w,
            h: widget.h,
            block: sanitizeBlockForTemplate(item.group.blocksById[widget.i])
          }))
        }
      })
    }
  }
}

function instantiateBlock(source) {
  return clone(source || {})
}

function markTemplateSource(value, template) {
  const next = value
  if (next && template && template.id) {
    next.sourceTemplateId = template.id
    next.sourceTemplateType = template.entityType
  }
  return next
}

function markGroupTemplateSource(group, template) {
  markTemplateSource(group, template)
  Object.keys(group && group.blocksById || {}).forEach(blockId => {
    markTemplateSource(group.blocksById[blockId], template)
  })
  return group
}

function instantiateGroup(payload, position) {
  const widgets = Array.isArray(payload && payload.items) ? payload.items : Array.isArray(payload && payload.widgets) ? payload.widgets : []
  const groupId = createId('group')
  const group = {
    groupId,
    title: String(payload && payload.title || '自定义组合').trim() || '自定义组合',
    blocksById: {},
    widgets: []
  }
  widgets.forEach(item => {
    const block = instantiateBlock(item && item.block)
    group.blocksById[block.blockId] = block
    group.widgets.push(createGroupChildWidget(block, {
      x: Number(item && item.x || 0),
      y: Number(item && item.y || 0),
      w: Number(item && item.w || 24),
      h: Number(item && item.h || getBlockWidgetHeight(block))
    }))
  })
  return {
    group,
    widget: createTopLevelGroupWidget(group, position || getNextLayoutPosition([]))
  }
}

function restoreTemplateToGrid(state, template) {
  const next = normalizeState(state)
  if (!template || !template.entityType) return next
  if (template.entityType === 'vm-block-template') {
    const block = markTemplateSource(instantiateBlock(template.payload && template.payload.block), template)
    if (next.blocksById[block.blockId]) {
      return replaceBlockWidget(next, block.blockId, block)
    }
    const position = getNextLayoutPosition(next.widgets)
    const savedHeight = template.payload && template.payload.height
    if (savedHeight != null) {
      position.h = savedHeight
    }
    return appendBlockWidget(next, block, position)
  }
  if (template.entityType === 'vm-group-template') {
    const restored = instantiateGroup(template.payload && template.payload.group, getNextLayoutPosition(next.widgets))
    markGroupTemplateSource(restored.group, template)
    next.groupsById[restored.group.groupId] = restored.group
    next.widgets.push(restored.widget)
    return next
  }
  if (template.entityType === 'vm-grid-layout-template') {
    const items = Array.isArray(template.payload && template.payload.items) ? template.payload.items : []
    const base = getNextLayoutPosition(next.widgets)
    items.forEach(item => {
      if (item && item.type === 'group') {
        const restored = instantiateGroup(item, {
          x: Number(item.x || 0),
          y: base.y + Number(item.y || 0),
          w: Number(item.w || 24),
          h: Number(item.h || 12)
        })
        markGroupTemplateSource(restored.group, template)
        next.groupsById[restored.group.groupId] = restored.group
        next.widgets.push(restored.widget)
        return
      }
      const block = markTemplateSource(instantiateBlock(item && item.block), template)
      if (next.blocksById[block.blockId]) {
        const replaced = replaceBlockWidget(next, block.blockId, block)
        next.blocksById = replaced.blocksById
        next.widgets = replaced.widgets
        return
      }
      next.blocksById[block.blockId] = block
      next.widgets.push(createTopLevelBlockWidget(block, {
        x: Number(item && item.x || 0),
        y: base.y + Number(item && item.y || 0),
        w: Number(item && item.w || 24),
        h: Number(item && item.h || getBlockWidgetHeight(block))
      }))
    })
  }
  return next
}

function mergeBlocksToGroup(state, blockIds, title) {
  const next = normalizeState(state)
  const targetIds = Array.from(new Set(Array.isArray(blockIds) ? blockIds.filter(Boolean) : []))
  const candidates = targetIds.map(blockId => {
    const location = findBlockLocation(next, blockId)
    if (!location || location.container !== 'top-level') return null
    const widget = next.widgets[location.widgetIndex]
    const block = next.blocksById[blockId]
    return widget && block ? { blockId, widget, block, widgetIndex: location.widgetIndex } : null
  }).filter(Boolean)
  if (candidates.length < 2) return next

  const selectedWidgets = sortWidgets(candidates.map(item => item.widget))
  const minX = Math.min.apply(null, selectedWidgets.map(item => item.x))
  const minY = Math.min.apply(null, selectedWidgets.map(item => item.y))
  const groupId = createId('group')
  const group = {
    groupId,
    title: String(title || '自定义组合').trim() || '自定义组合',
    blocksById: {},
    widgets: []
  }

  candidates.forEach(item => {
    group.blocksById[item.blockId] = item.block
    group.widgets.push(createGroupChildWidget(item.block, {
      x: item.widget.x - minX,
      y: item.widget.y - minY,
      w: item.widget.w,
      h: item.widget.h
    }))
  })

  next.widgets = next.widgets.filter(widget => !targetIds.includes(parseEntityKey(widget.i).id) || parseEntityKey(widget.i).type !== 'block')
  targetIds.forEach(blockId => {
    delete next.blocksById[blockId]
  })
  next.groupsById[groupId] = group
  next.widgets.push(createTopLevelGroupWidget(group, {
    x: 0,
    y: minY,
    w: 24,
    h: getGroupWidgetHeight(group)
  }))
  return next
}

function ungroupToCanvas(state, groupId) {
  const next = normalizeState(state)
  const group = next.groupsById[groupId]
  if (!group) return next
  const groupWidgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', groupId))
  const groupWidget = groupWidgetIndex >= 0 ? next.widgets[groupWidgetIndex] : null
  if (groupWidgetIndex >= 0) next.widgets.splice(groupWidgetIndex, 1)
  delete next.groupsById[groupId]
  const baseY = groupWidget ? groupWidget.y : getNextLayoutPosition(next.widgets).y
  sortWidgets(group.widgets).forEach(widget => {
    const block = group.blocksById[widget.i]
    if (!block) return
    next.blocksById[block.blockId] = block
    next.widgets.push(createTopLevelBlockWidget(block, {
      x: widget.x,
      y: baseY + widget.y,
      w: widget.w,
      h: widget.h
    }))
  })
  return next
}

function renameGroup(state, groupId, title) {
  const next = normalizeState(state)
  if (!next.groupsById[groupId]) return next
  next.groupsById[groupId].title = String(title !== undefined && title !== null ? title : '')
  return next
}

function updateTopLevelWidgets(state, widgets) {
  const next = normalizeState(state)
  next.widgets = clone(widgets || [])
  return next
}

function updateGroupWidgets(state, groupId, widgets) {
  const next = normalizeState(state)
  if (!next.groupsById[groupId]) return next
  next.groupsById[groupId].widgets = clone(widgets || [])
  const topLevelWidgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', groupId))
  if (topLevelWidgetIndex >= 0) {
    next.widgets[topLevelWidgetIndex].h = getGroupWidgetHeight(next.groupsById[groupId])
  }
  return next
}

function setTopLevelEntityWidth(state, entityKey, width) {
  const next = normalizeState(state)
  const widgetIndex = getTopLevelWidgetIndex(next, entityKey)
  if (widgetIndex < 0) return next
  const widget = next.widgets[widgetIndex]
  widget.w = width
  widget.x = width === 24 ? 0 : (widget.x >= 12 ? 12 : 0)
  return next
}

function setGroupChildWidth(state, groupId, blockId, width) {
  const next = normalizeState(state)
  const group = next.groupsById[groupId]
  if (!group) return next
  const widget = (group.widgets || []).find(item => item.i === blockId)
  if (!widget) return next
  widget.w = width
  widget.x = width === 24 ? 0 : (widget.x >= 12 ? 12 : 0)
  const topLevelWidgetIndex = getTopLevelWidgetIndex(next, createEntityKey('group', groupId))
  if (topLevelWidgetIndex >= 0) {
    next.widgets[topLevelWidgetIndex].h = getGroupWidgetHeight(group)
  }
  return next
}

function removeTopLevelEntity(state, entityKey) {
  const descriptor = parseEntityKey(entityKey)
  const next = normalizeState(state)
  const widgetIndex = getTopLevelWidgetIndex(next, entityKey)
  if (widgetIndex >= 0) next.widgets.splice(widgetIndex, 1)
  if (descriptor.type === 'group') {
    delete next.groupsById[descriptor.id]
    return next
  }
  delete next.blocksById[descriptor.id]
  return next
}

module.exports = {
  appendBlockWidget,
  createCanvasStateFromBlocks,
  createEntityKey,
  findBlockLocation,
  getNextLayoutPosition,
  getOrderedBlocks,
  getOrderedGroupBlocks,
  getOrderedTopLevelItems,
  mergeBlocksToGroup,
  parseEntityKey,
  removeBlockWidget,
  removeTopLevelEntity,
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
}
