import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const {
  assertVmBusinessSuccess,
  unwrapVmBusinessResponse,
  unwrapVmResponse
} = loadVmSource('../src/views/vmChat/vm-api-response.js')

assert.deepStrictEqual(unwrapVmResponse({ data: { status: 0, body: [] } }), { status: 0, body: [] })
assert.deepStrictEqual(assertVmBusinessSuccess({ status: 0, body: [] }), { status: 0, body: [] })
assert.deepStrictEqual(assertVmBusinessSuccess({ body: [] }), { body: [] })
assert.deepStrictEqual(assertVmBusinessSuccess([{ value: 1 }]), [{ value: 1 }])

assert.throws(
  () => unwrapVmBusinessResponse({ data: { status: -1, code: 'SQL_PARAM_ERROR', message: '参数不正确' } }, 'VM SQL 接口'),
  error => error.code === 'SQL_PARAM_ERROR' && /参数不正确/.test(error.message)
)
assert.throws(
  () => assertVmBusinessSuccess({ status: 500, msg: 'SQL 执行失败' }, 'VM SQL 接口'),
  /SQL 执行失败.*500/
)

console.log('vm api business response checks passed')
