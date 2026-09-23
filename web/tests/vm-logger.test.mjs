import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const {
  clearVmChatLogs,
  getVmChatLogs,
  logVmChatEvent
} = loadVmSource('../src/views/vmChat/vm-logger.js')

function createStorage(initial = {}) {
  return {
    values: Object.assign({}, initial),
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(this.values, key) ? this.values[key] : null
    },
    setItem(key, value) {
      this.values[key] = String(value)
    },
    removeItem(key) {
      delete this.values[key]
    }
  }
}

const originalWindow = global.window
const originalNodeEnv = process.env.NODE_ENV
const localStorage = createStorage({ 'vm-chat-logs': '{"logs":[{"legacy":true}]}' })
const sessionStorage = createStorage()
global.window = { localStorage, sessionStorage }

process.env.NODE_ENV = 'production'
logVmChatEvent('vm-api', 'request.start', {
  requestId: 'r1',
  moduleKey: 'stockExposureTiming',
  params: { fundCode: 'SM0513' },
  response: [{ secretBusinessValue: 42 }]
})
const productionLog = getVmChatLogs({ limit: 1 })[0]
assert.strictEqual(productionLog.payload.requestId, 'r1')
assert.strictEqual(productionLog.payload.moduleKey, 'stockExposureTiming')
assert.strictEqual('params' in productionLog.payload, false)
assert.strictEqual('response' in productionLog.payload, false)
assert.strictEqual(localStorage.getItem('vm-chat-logs'), null)
assert.strictEqual(sessionStorage.getItem('vm-chat-logs'), null)

delete global.window.__VM_CHAT_LOGS__
process.env.NODE_ENV = 'development'
logVmChatEvent('query-executor', 'request.normalized', {
  requestId: 'r2',
  rowsSample: [{ fundCode: 'SM0513' }]
})
assert.strictEqual(localStorage.getItem('vm-chat-logs'), null)
const debugSession = JSON.parse(sessionStorage.getItem('vm-chat-logs'))
assert.ok(debugSession.expiresAt > Date.now())
assert.strictEqual(debugSession.logs.length, 1)
assert.strictEqual(debugSession.logs[0].payload.rowsSample.sample[0].fundCode, 'SM0513')

clearVmChatLogs()
assert.strictEqual(JSON.parse(sessionStorage.getItem('vm-chat-logs')).logs.length, 0)

if (originalNodeEnv === undefined) delete process.env.NODE_ENV
else process.env.NODE_ENV = originalNodeEnv
global.window = originalWindow

console.log('vm logger persistence and redaction checks passed')
