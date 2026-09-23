import path from 'path'
import { spawnSync } from 'child_process'
import { fileURLToPath } from 'url'

const testsDir = path.dirname(fileURLToPath(import.meta.url))
const testFiles = [
  'hermes-run-output.test.mjs',
  'vm-api-response.test.mjs',
  'vm-chat-modern-protocol.test.mjs',
  'vm-combined-table-block.test.mjs',
  'vm-dsl-contract-consistency.test.mjs',
  'vm-grid-layout-runtime.test.mjs',
  'vm-logger.test.mjs',
  'vm-param-resolver.test.mjs',
  'vm-query-executor-response-shape.test.mjs'
]

for (const testFile of testFiles) {
  const result = spawnSync(process.execPath, [path.join(testsDir, testFile)], {
    cwd: path.resolve(testsDir, '..'),
    env: process.env,
    encoding: 'utf8'
  })
  if (result.stdout) process.stdout.write(result.stdout)
  if (result.stderr) process.stderr.write(result.stderr)
  if (result.status !== 0) process.exit(result.status || 1)
}

console.log(testFiles.length + ' 组 vmChat 确定性回归测试全部通过')
