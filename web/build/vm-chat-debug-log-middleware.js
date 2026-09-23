'use strict'

const fs = require('fs')
const path = require('path')

const DEBUG_DIR = path.resolve(__dirname, '../.codex-debug')
const DEBUG_FILE = path.join(DEBUG_DIR, 'vm-chat-protocol-debug.jsonl')
const DEBUG_ROUTE = '/__vmchat/debug-log'

function ensureDebugDir() {
  fs.mkdirSync(DEBUG_DIR, { recursive: true })
}

function readRequestBody(req) {
  return new Promise((resolve, reject) => {
    const chunks = []
    req.on('data', chunk => {
      chunks.push(Buffer.from(chunk))
    })
    req.on('end', () => {
      resolve(Buffer.concat(chunks).toString('utf8'))
    })
    req.on('error', reject)
  })
}

function writeEntry(payload, req) {
  ensureDebugDir()
  const entry = {
    loggedAt: new Date().toISOString(),
    ip: req.ip || (req.connection && req.connection.remoteAddress) || '',
    ua: req.headers['user-agent'] || '',
    payload
  }
  fs.appendFileSync(DEBUG_FILE, JSON.stringify(entry) + '\n')
}

function registerVmChatDebugLogMiddleware(app) {
  app.post(DEBUG_ROUTE, async (req, res) => {
    try {
      const rawBody = await readRequestBody(req)
      const payload = rawBody ? JSON.parse(rawBody) : {}
      writeEntry(payload, req)
      res.json({
        ok: true,
        file: DEBUG_FILE
      })
    } catch (error) {
      res.status(500).json({
        ok: false,
        message: error && error.message ? error.message : String(error || 'write failed')
      })
    }
  })
}

module.exports = {
  DEBUG_FILE,
  registerVmChatDebugLogMiddleware
}
