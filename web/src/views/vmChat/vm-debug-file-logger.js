const DEBUG_ROUTE = '/__vmchat/debug-log'
const MAX_TEXT_LENGTH = 12000

function isBrowser() {
  return typeof window !== 'undefined' && typeof window.fetch === 'function'
}

function truncateText(value) {
  const text = String(value === undefined || value === null ? '' : value)
  return text.length > MAX_TEXT_LENGTH
    ? text.slice(0, MAX_TEXT_LENGTH) + '\n...[truncated]'
    : text
}

export function writeVmDebugFile(entry) {
  if (!isBrowser()) return Promise.resolve(false)
  const payload = Object.assign({}, entry || {})
  ;['content', 'normalizedContent', 'extractedJson', 'repairedJson', 'parseError'].forEach(key => {
    if (payload[key] !== undefined) {
      payload[key] = truncateText(payload[key])
    }
  })
  return window.fetch(DEBUG_ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  }).then(() => true).catch(() => false)
}
