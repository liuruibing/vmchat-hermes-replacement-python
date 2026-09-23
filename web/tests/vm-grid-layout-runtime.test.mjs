import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const {
  appendBlockWidget,
  createCanvasStateFromBlocks,
  mergeBlocksToGroup,
  replaceBlockWidget,
  restoreTemplateToGrid,
  serializeBlockTemplate,
  ungroupToCanvas
} = loadVmSource('../src/views/vmChat/vm-grid-layout-runtime.cjs')

const uuidPattern = /^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i

function createBlock(id, title) {
  return {
    blockId: id,
    title,
    type: 'table',
    viewType: 'table',
    dsl: {
      action: 'create',
      id: '550e8400-e29b-41d4-a716-446655440000',
      params: {
        fundCode: 'SM0513',
        beginDate: '20220101',
        endDate: '20220131',
        dataFreqOpen: 'true',
        benchmarks: '1',
        benchmarkA: '沪深300',
        dataFreq: '日频'
      },
      requests: [
        {
          id: 'profit',
          moduleId: 'tenProfitIndustry',
          sqlCode: 'fe842e36-d296-432d-8696-d6ec8f2aab03'
        }
      ],
      transform: {
        language: 'javascript',
        function: 'function transform(responses) { return []; }'
      },
      view: {
        type: 'table',
        title,
        columns: [
          { field: 'name', label: '名称', format: { type: 'text' }}
        ]
      }
    },
    renderSpec: {
      renderer: 'table',
      columns: [],
      rows: []
    },
    renderState: { status: 'ready' },
    sourceData: { runtime: { totalRows: 1 }}
  }
}

let state = createCanvasStateFromBlocks([])
state = appendBlockWidget(state, createBlock('block-a', '模块 A'))
state = appendBlockWidget(state, createBlock('block-b', '模块 B'))

assert.deepStrictEqual(Object.keys(state.blocksById).sort(), ['block-a', 'block-b'])
assert.strictEqual(state.widgets.length, 2)
assert.ok(state.widgets.every(widget => widget.i.indexOf('block:') === 0))

assert.throws(
  () => appendBlockWidget(state, createBlock('block-a', '重复模块')),
  /create blockId 已存在/
)
assert.throws(
  () => replaceBlockWidget(state, 'missing-block', createBlock('replacement', '替换模块')),
  /update 目标已不存在/
)

const grouped = mergeBlocksToGroup(state, ['block-a', 'block-b'], '组合模块')
assert.strictEqual(Object.keys(grouped.blocksById).length, 0)
assert.strictEqual(Object.keys(grouped.groupsById).length, 1)
assert.strictEqual(grouped.widgets.length, 1)

const groupId = Object.keys(grouped.groupsById)[0]
const ungrouped = ungroupToCanvas(grouped, groupId)
assert.deepStrictEqual(Object.keys(ungrouped.blocksById).sort(), ['block-a', 'block-b'])
assert.strictEqual(Object.keys(ungrouped.groupsById).length, 0)

const template = Object.assign({ id: 'template-source-1' }, serializeBlockTemplate(createBlock('block-template-source', '模板模块')))
const restored = restoreTemplateToGrid(createCanvasStateFromBlocks([]), template)
const restoredBlock = Object.values(restored.blocksById)[0]

assert.ok(restoredBlock.blockId)
assert.notStrictEqual(restoredBlock.blockId, 'block-template-source')
assert.ok(uuidPattern.test(restoredBlock.dsl.id), 'restored DSL id must be a UUID')
assert.strictEqual(restoredBlock.sourceTemplateId, 'template-source-1')
assert.strictEqual(restoredBlock.sourceTemplateType, 'vm-block-template')

const replaced = replaceBlockWidget(restored, restoredBlock.blockId, createBlock(restoredBlock.blockId, '更新后的模块'))
assert.strictEqual(replaced.blocksById[restoredBlock.blockId].sourceTemplateId, 'template-source-1')
assert.strictEqual(replaced.blocksById[restoredBlock.blockId].sourceTemplateType, 'vm-block-template')

console.log('vm grid layout runtime checks passed')
