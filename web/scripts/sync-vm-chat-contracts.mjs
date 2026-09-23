#!/usr/bin/env node
import { mkdir, readFile, writeFile } from 'node:fs/promises'
import os from 'node:os'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const defaultCatalogDir = path.resolve(projectRoot, '../../AI项目/广发AI-数据浏览器/vmtomd-explain/catalog')
const defaultSchemaFile = path.join(
  os.homedir(),
  '.hermes/profiles/vm-report-template/skills/vmreport/vm-report-dsl/references/dsl.schema.json'
)
const catalogDir = path.resolve(process.env.VM_REPORT_CATALOG_DIR || defaultCatalogDir)
const schemaFile = path.resolve(process.env.VM_REPORT_DSL_SCHEMA || defaultSchemaFile)
const outputDir = path.join(projectRoot, 'src/views/vmChat/generated')

async function readJson(file, displayName) {
  try {
    return JSON.parse(await readFile(file, 'utf8'))
  } catch (error) {
    throw new Error(displayName + '无法读取：' + file + '；' + error.message)
  }
}

function asModuleSource(value, banner) {
  return [
    '// ' + banner,
    '// 请运行 npm run sync:vmchat-contracts 更新，禁止手工修改。',
    'export default ' + JSON.stringify(value, null, 2),
    ''
  ].join('\n')
}

const executionContract = await readJson(
  path.join(catalogDir, 'execution-contract.json'),
  'catalog execution contract'
)
const dslSchema = await readJson(schemaFile, 'Hermes DSL schema')
if (!executionContract.modules || !Object.keys(executionContract.modules).length) {
  throw new Error('catalog execution contract 没有模块绑定')
}
if (!dslSchema.definitions || !dslSchema.definitions.dsl) {
  throw new Error('Hermes DSL schema 必须使用 draft-07 definitions')
}

await mkdir(outputDir, { recursive: true })
await writeFile(
  path.join(outputDir, 'vm-report-catalog-contract.js'),
  asModuleSource(executionContract, '由 catalog/execution-contract.json 自动生成。'),
  'utf8'
)
await writeFile(
  path.join(outputDir, 'vm-report-dsl-schema.js'),
  asModuleSource(dslSchema, '由 Hermes vm-report-dsl/references/dsl.schema.json 自动生成。'),
  'utf8'
)
console.log('vmChat 契约已同步：' + Object.keys(executionContract.modules).length + ' 个模块')
