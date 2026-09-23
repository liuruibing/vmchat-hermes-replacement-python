import assert from 'assert'
import { existsSync } from 'fs'
import { mkdtemp, readFile, rm, writeFile } from 'fs/promises'
import os from 'os'
import path from 'path'
import { spawnSync } from 'child_process'
import { fileURLToPath } from 'url'
import { loadVmSource } from './load-vm-source.mjs'

const { validateVmReportDsl } = loadVmSource('../src/views/vmChat/vm-report-dsl-validator.js')
const frontendCatalogContract = loadVmSource('../src/views/vmChat/generated/vm-report-catalog-contract.js').default
const frontendDslSchema = loadVmSource('../src/views/vmChat/generated/vm-report-dsl-schema.js').default

const skillDir = process.env.VM_REPORT_DSL_SKILL_DIR || path.join(
  os.homedir(),
  '.hermes',
  'profiles',
  'vm-report-template',
  'skills',
  'vmreport',
  'vm-report-dsl'
)
const schemaFile = path.join(skillDir, 'references', 'dsl.schema.json')
const schemaValidator = path.join(skillDir, 'scripts', 'validate-schema.py')
const fullValidator = path.join(skillDir, 'scripts', 'validate-dsl.mjs')
const ingestCatalogDir = process.env.VM_REPORT_CATALOG_DIR || path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  '../../../AI项目/广发AI-数据浏览器/vmtomd-explain/catalog'
)

if (!existsSync(schemaFile) || !existsSync(schemaValidator) || !existsSync(fullValidator)) {
  console.log('跳过 Hermes/前端 DSL 契约一致性测试：未找到 vm-report-dsl skill')
  process.exit(0)
}

assert.deepStrictEqual(frontendDslSchema, JSON.parse(await readFile(schemaFile, 'utf8')))
if (existsSync(path.join(ingestCatalogDir, 'execution-contract.json'))) {
  assert.deepStrictEqual(
    frontendCatalogContract,
    JSON.parse(await readFile(path.join(ingestCatalogDir, 'execution-contract.json'), 'utf8'))
  )
}

const baseDsl = {
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
  requests: [{
    id: 'stock',
    moduleId: 'stockExposureTiming',
    sqlCode: '712b930b-87a5-4cba-8da0-3671d4c8dc54'
  }],
  transform: {
    language: 'javascript',
    function: 'function transform(responses) { var rows = responses.stock && responses.stock.body || []; return rows.map(function (row) { return { exposure: row.F_STOCK_EXP }; }); }'
  },
  view: {
    type: 'table',
    title: '契约一致性测试',
    columns: [{ field: 'exposure', label: '股票净敞口占比', format: { type: 'raw' } }]
  }
}

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

const cases = [
  { name: 'valid', expected: true, schemaExpected: true, mutate() {} },
  {
    name: 'reject-multiplier',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { dsl.view.columns[0].format.multiplier = 100 }
  },
  {
    name: 'reject-no-benchmark-extras',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { dsl.params.benchmarks = '0' }
  },
  {
    name: 'reject-single-benchmark-b',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { dsl.params.benchmarkB = '中证500' }
  },
  {
    name: 'reject-dynamic-code',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { dsl.params.benchmarkA = '000300' }
  },
  {
    name: 'reject-extra-field',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { dsl.unexpected = true }
  },
  {
    name: 'reject-missing-action',
    expected: false,
    schemaExpected: false,
    mutate(dsl) { delete dsl.action }
  },
  {
    name: 'reject-invalid-date',
    expected: false,
    schemaExpected: true,
    mutate(dsl) { dsl.params.beginDate = '20220231' }
  },
  {
    name: 'reject-catalog-sql-mismatch',
    expected: false,
    schemaExpected: true,
    mutate(dsl) { dsl.requests[0].sqlCode = 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa' }
  },
  {
    name: 'reject-transform-missing-request',
    expected: false,
    schemaExpected: true,
    mutate(dsl) { dsl.transform.function = 'function transform(responses) { return [{ value: 1 }]; }' }
  },
  {
    name: 'reject-transform-missing-view-field',
    expected: false,
    schemaExpected: true,
    mutate(dsl) {
      dsl.transform.function = 'function transform(responses) { var rows = responses.stock.body || []; return rows.map(function () { return { other: 1 }; }); }'
    }
  }
]

const tempDir = await mkdtemp(path.join(os.tmpdir(), 'vm-dsl-contract-'))
try {
  for (const testCase of cases) {
    const dsl = clone(baseDsl)
    testCase.mutate(dsl)
    let frontendPassed = true
    try {
      validateVmReportDsl(dsl)
    } catch (error) {
      frontendPassed = false
    }

    const payloadFile = path.join(tempDir, testCase.name + '.json')
    await writeFile(payloadFile, JSON.stringify(dsl), 'utf8')
    const schemaResult = spawnSync(
      process.env.VM_REPORT_PYTHON || 'python3',
      [schemaValidator, schemaFile, payloadFile],
      { encoding: 'utf8' }
    )
    const schemaPassed = schemaResult.status === 0
    const fullResult = spawnSync(process.execPath, [fullValidator, payloadFile], {
      encoding: 'utf8'
    })
    const hermesPassed = fullResult.status === 0
    assert.strictEqual(frontendPassed, testCase.expected, testCase.name + ' 前端 validator 结果错误')
    assert.strictEqual(
      schemaPassed,
      testCase.schemaExpected,
      testCase.name + ' Hermes schema 结果错误：' + (schemaResult.stderr || schemaResult.stdout || '')
    )
    assert.strictEqual(
      hermesPassed,
      testCase.expected,
      testCase.name + ' Hermes 完整 validator 结果错误：' + (fullResult.stderr || fullResult.stdout || '')
    )
    assert.strictEqual(frontendPassed, hermesPassed, testCase.name + ' 两端完整契约发生漂移')
  }
} finally {
  await rm(tempDir, { recursive: true, force: true })
}

console.log(cases.length + ' 项 Hermes/前端完整 DSL 契约一致性检查通过')
