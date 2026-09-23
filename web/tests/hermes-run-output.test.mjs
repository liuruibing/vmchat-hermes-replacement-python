import assert from 'assert'
import { loadVmSource } from './load-vm-source.mjs'

const {
  getHermesBaseUrl,
  buildHermesRequestUrl,
  extractHermesRunOutputText,
  getHermesRunEventsDisabled,
  setHermesRunEventsDisabled,
  shouldUseHermesRunEvents,
  HERMES_BASE_URL_STORAGE_KEY
} = loadVmSource('../src/api/hermesResearch.js')

assert.strictEqual(extractHermesRunOutputText('{"intent":"chat"}'), '{"intent":"chat"}')

assert.strictEqual(
  extractHermesRunOutputText([
    {
      type: 'message',
      content: [
        {
          type: 'output_text',
          text: '{"intent":"report","renderType":"report"}'
        }
      ]
    }
  ]),
  '{"intent":"report","renderType":"report"}'
)

assert.strictEqual(
  extractHermesRunOutputText({
    message: {
      content: [
        { text: 'hello' },
        { output_text: ' world' }
      ]
    }
  }),
  'hello world'
)

assert.strictEqual(extractHermesRunOutputText({ type: 'unknown' }), '')

const originalWindow = global.window
global.window = {
  location: {
    hostname: '127.0.0.1',
    port: '9528'
  },
  localStorage: {
    store: {},
    getItem(key) {
      return Object.prototype.hasOwnProperty.call(this.store, key) ? this.store[key] : null
    },
    setItem(key, value) {
      this.store[key] = String(value)
    },
    removeItem(key) {
      delete this.store[key]
    }
  }
}

assert.strictEqual(getHermesBaseUrl(), '/hermes-api')
global.window.localStorage.setItem(HERMES_BASE_URL_STORAGE_KEY, 'http://192.168.30.241:8642')
assert.strictEqual(getHermesBaseUrl(), '/hermes-api')
assert.strictEqual(buildHermesRequestUrl('/v1/wiki/tree'), '/hermes-api/v1/wiki/tree')

global.window.location = {
  hostname: 'fof.example.com',
  port: ''
}
global.window.localStorage.setItem(HERMES_BASE_URL_STORAGE_KEY, 'http://127.0.0.1:8642')
assert.strictEqual(getHermesBaseUrl(), '/hermes-api')
assert.strictEqual(buildHermesRequestUrl('/v1/wiki/tree'), '/hermes-api/v1/wiki/tree')

setHermesRunEventsDisabled(false)
assert.strictEqual(getHermesRunEventsDisabled(), false)
assert.strictEqual(shouldUseHermesRunEvents(), true)

setHermesRunEventsDisabled(true)
assert.strictEqual(getHermesRunEventsDisabled(), true)
assert.strictEqual(shouldUseHermesRunEvents(), true)

global.window = originalWindow

console.log('hermes run output extraction checks passed')
