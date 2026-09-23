import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const {
  assertVmHermesOperationAllowed,
  buildVmReportNoticeFromError,
  buildVmHermesMessages,
  formatVmAssistantStreamingContent,
  isExplicitVmBatchUpdateRequest,
  isLikelyVmProtocolContent,
  parseVmHermesRenderPayload
} = loadVmSource('../src/views/vmChat/vm-chat-helpers.js')

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

const createDsl = {
  action: 'create',
  id: '550e8400-e29b-41d4-a716-446655440000',
  params: {
    fundCode: 'SM0513',
    beginDate: '2022-01-01',
    endDate: '2022-01-31',
    dataFreqOpen: 'true',
    benchmarks: '1',
    benchmarkA: '沪深300',
    dataFreq: '日频'
  },
  requests: [{
    id: 'profit',
    moduleId: 'tenProfitIndustry',
    sqlCode: 'fe842e36-d296-432d-8696-d6ec8f2aab03'
  }],
  transform: {
    language: 'javascript',
    function: [
      'function transform(responses) {',
      '  var response = responses && responses.profit;',
      '  var rows = response && Array.isArray(response.body) ? response.body : [];',
      '  return rows.map(function (row) {',
      '    return { securityCode: row.VC_SYMBOL, income: row.F_INCOME };',
      '  });',
      '}'
    ].join('\n')
  },
  view: {
    type: 'table',
    title: 'A股前十盈利行业',
    columns: [
      { field: 'securityCode', label: '证券代码', format: { type: 'text', nullValue: '-' } },
      { field: 'income', label: '本期盈利', unit: '元', format: { type: 'decimal', digits: 2 } }
    ]
  }
}

assert.throws(() => assertVmHermesOperationAllowed('removeBlock'), /不允许删除报表块/)
assert.throws(() => assertVmHermesOperationAllowed('renameBlock'), /不支持的操作/)
assert.throws(() => assertVmHermesOperationAllowed('moveBlock'), /不支持的操作/)

const parsed = parseVmHermesRenderPayload(JSON.stringify(createDsl))
assert.strictEqual(parsed.renderType, 'report')
assert.strictEqual(parsed.operations.length, 1)
assert.strictEqual(parsed.operations[0].action, 'appendBlock')
assert.strictEqual(parsed.operations[0].block.blockId, createDsl.id)
assert.strictEqual(parsed.operations[0].block.dsl.params.beginDate, '20220101')
assert.strictEqual(parsed.operations[0].block.moduleKey, 'tenProfitIndustry')

const prefixedDsl = parseVmHermesRenderPayload(
  '门禁通过：指标来自 body[].YAXISDATA1，维度来自 body[].XAXISDATA。\n' + JSON.stringify(createDsl)
)
assert.strictEqual(prefixedDsl.renderType, 'report')
assert.strictEqual(prefixedDsl.operations[0].block.blockId, createDsl.id)

assert.strictEqual(isLikelyVmProtocolContent(JSON.stringify(createDsl)), true)
assert.strictEqual(formatVmAssistantStreamingContent(JSON.stringify(createDsl)), '正在生成可执行报告协议...')
assert.strictEqual(formatVmAssistantStreamingContent('正在分析'), '正在分析')

for (const legacyPayload of [
  { renderType: 'report', operations: [{ action: 'appendBlock', block: { dsl: createDsl } }] },
  { renderType: 'report', blocks: [{ dsl: createDsl }] },
  { renderType: 'report', operations: [{ action: 'removeBlock', targetBlockId: 'existing-block' }] }
]) {
  assert.throws(
    () => parseVmHermesRenderPayload(JSON.stringify(legacyPayload)),
    /只能是完整 vm-report-dsl/
  )
}

const clarifyPayload = parseVmHermesRenderPayload(JSON.stringify({
  intent: 'clarify',
  renderType: 'clarify',
  message: '### 需要补充信息\n\n请确认要查看的模块。',
  clarify: {
    questions: ['您想看哪个模块？']
  }
}))
assert.strictEqual(clarifyPayload.renderType, 'clarify')
assert.deepStrictEqual(clarifyPayload.clarify.questions, ['您想看哪个模块？'])

const businessInfoPayload = parseVmHermesRenderPayload(JSON.stringify({
  intent: 'businessInfo',
  renderType: 'businessInfo',
  title: '现金类持仓时序字段说明',
  message: '## 字段列表\n\n- 日期\n- 现金类仓位'
}))
assert.strictEqual(businessInfoPayload.renderType, 'businessInfo')
assert.strictEqual(businessInfoPayload.title, '现金类持仓时序字段说明')
assert.ok(businessInfoPayload.message.includes('字段列表'))

assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({ intent: 'businessInfo', renderType: 'businessInfo', message: '缺少标题' })),
  /businessInfo 协议缺少 title/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({ intent: 'chat', renderType: 'businessInfo', title: '类型不匹配', message: '类型不匹配' })),
  /intent 与 renderType 必须一致/
)

const noisyClarifyPayload = parseVmHermesRenderPayload(
  '锚点已记录。正在检索知识库。\n\n```json\n' +
  JSON.stringify({
    intent: 'clarify',
    renderType: 'clarify',
    message: '**请确认模块**',
    questions: ['您要查看哪个模块？']
  }) +
  '\n```\n'
)
assert.strictEqual(noisyClarifyPayload.renderType, 'clarify')
assert.deepStrictEqual(noisyClarifyPayload.clarify.questions, ['您要查看哪个模块？'])

const clarifyWithPreamble = parseVmHermesRenderPayload(
  '## 知识库中与「持仓」相关的模块\n\n- **持仓平均PE/PB时序**\n\n' +
  JSON.stringify({
    intent: 'clarify',
    renderType: 'chat',
    message: '## 知识库中与「持仓」相关的模块\n\n- **持仓平均PE/PB时序**',
    questions: ['您想看哪一个持仓相关模块？']
  })
)
assert.strictEqual(clarifyWithPreamble.renderType, 'clarify')
assert.deepStrictEqual(clarifyWithPreamble.clarify.questions, ['您想看哪一个持仓相关模块？'])
assert.ok(clarifyWithPreamble.thinking.includes('Hermes 检索说明'))

assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({ intent: 'clarify', renderType: 'clarify' })),
  /缺少 message/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({ intent: 'chat', renderType: 'clarify', message: '类型不匹配' })),
  /intent 与 renderType 必须一致/
)

const naturalGatePayload = parseVmHermesRenderPayload('缺少产品代码、开始日期和结束日期，请补充后我再生成报表配置。')
assert.strictEqual(naturalGatePayload.renderType, 'chat')
assert.ok(naturalGatePayload.message.includes('缺少产品代码'))

const existingBlock = {
  blockId: 'existing-block',
  title: createDsl.view.title,
  viewType: 'table',
  dsl: clone(createDsl),
  renderState: { status: 'ready' },
  renderSpec: { columns: [], rows: [] }
}
const secondExistingBlock = {
  ...existingBlock,
  blockId: 'second-existing-block',
  title: '第二个模块',
  dsl: {
    ...clone(createDsl),
    id: '66666666-6666-4666-8666-666666666666',
    view: { ...clone(createDsl.view), title: '第二个模块' }
  }
}
const reportBlocks = [existingBlock, secondExistingBlock]

const updatePayload = parseVmHermesRenderPayload(JSON.stringify({
  ...clone(createDsl),
  action: 'update'
}), { reportBlocks })
assert.strictEqual(updatePayload.operations[0].action, 'replaceBlock')
assert.strictEqual(updatePayload.operations[0].targetBlockId, 'existing-block')

const batchDsls = [
  { ...clone(secondExistingBlock.dsl), action: 'update' },
  { ...clone(createDsl), action: 'update' }
]
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify(batchDsls), { reportBlocks }),
  /未明确要求批量修改/
)
const batchPayload = parseVmHermesRenderPayload(JSON.stringify(batchDsls), {
  reportBlocks,
  allowBatchUpdate: true
})
assert.deepStrictEqual(
  batchPayload.operations.map(item => item.targetBlockId),
  ['second-existing-block', 'existing-block']
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify([createDsl]), {
    reportBlocks,
    allowBatchUpdate: true
  }),
  /每一项都必须是 update/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify([
    { ...clone(createDsl), action: 'update' },
    { ...clone(createDsl), action: 'update' }
  ]), { reportBlocks, allowBatchUpdate: true }),
  /不得重复更新同一个报表块/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({
    ...clone(createDsl),
    action: 'update',
    id: '77777777-7777-4777-8777-777777777777'
  }), { reportBlocks }),
  /update 目标不存在/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify({ ...clone(createDsl), action: 'update' }), {
    reportBlocks: [existingBlock, { ...existingBlock, blockId: 'duplicate-dsl-id-block' }]
  }),
  /update 目标不唯一/
)
assert.throws(
  () => parseVmHermesRenderPayload(JSON.stringify(createDsl), { reportBlocks }),
  /create ID 已存在/
)

assert.strictEqual(isExplicitVmBatchUpdateRequest('把所有模块都修改成表格'), true)
assert.strictEqual(isExplicitVmBatchUpdateRequest('修改这个模块'), false)
assert.strictEqual(isExplicitVmBatchUpdateRequest('展示所有模块'), false)

const hermesMessages = buildVmHermesMessages({
  historyMessages: [],
  userInput: '把当前模块改成表格',
  reportBlocks,
  selectedBlockId: 'existing-block',
  sessionId: 'vm-report-dsl-test'
})
const systemMessage = hermesMessages[0].content
assert.ok(systemMessage.includes('$vm-report-dsl'))
assert.ok(systemMessage.includes('不得向用户显示 catalog、moduleId、submoduleId、sqlCode、英文模块标识或文件路径'))
assert.ok(systemMessage.includes('父模块中文标题 > 子模块中文标题'))
assert.ok(systemMessage.includes('示例 JSON 只供 transform 判断接口响应结构和原始取值'))
assert.ok(systemMessage.includes('currentDsls'))
assert.ok(systemMessage.includes('以语言目标为准'))
assert.ok(systemMessage.includes('不要代码块或 operations/blocks 包装对象'))
assert.ok(systemMessage.includes('intent/renderType: businessInfo'))

const errorNotice = buildVmReportNoticeFromError(new Error('vmChat 请求失败'), {
  traceId: 'trace-error',
  createdAt: '2026-06-24T00:00:02.000Z'
})
assert.strictEqual(errorNotice.status, 'error')
assert.strictEqual(errorNotice.message, 'vmChat 请求失败')

console.log('vm chat strict protocol checks passed')
