'use strict'

const fs = require('fs')
const path = require('path')

const MODULES_JSON_DIR = path.resolve(__dirname, '../src/views/vmChat/modules_json')
const ROUTE = '/__vmchat/modules-json'

const TYPE_FILE_MAP = {
  block: 'block-templates.json',
  group: 'group-templates.json',
  layout: 'layout-templates.json'
}

function ensureDir() {
  fs.mkdirSync(MODULES_JSON_DIR, { recursive: true })
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

function readAllTemplates() {
  ensureDir()
  const merged = []
  Object.keys(TYPE_FILE_MAP).forEach(type => {
    const filePath = path.join(MODULES_JSON_DIR, TYPE_FILE_MAP[type])
    try {
      if (fs.existsSync(filePath)) {
        const raw = fs.readFileSync(filePath, 'utf8')
        const parsed = JSON.parse(raw)
        if (Array.isArray(parsed)) {
          merged.push.apply(merged, parsed)
        }
      }
    } catch (error) {
      console.warn('[vmChat modules-json] 读取 ' + TYPE_FILE_MAP[type] + ' 失败：', error.message)
    }
  })
  return merged
}

function writeTemplatesByType(templates) {
  ensureDir()
  const list = Array.isArray(templates) ? templates : []
  const buckets = { block: [], group: [], layout: [] }
  list.forEach(template => {
    if (!template || !template.entityType) return
    if (template.entityType === 'vm-block-template') buckets.block.push(template)
    else if (template.entityType === 'vm-group-template') buckets.group.push(template)
    else if (template.entityType === 'vm-grid-layout-template') buckets.layout.push(template)
  })
  Object.keys(buckets).forEach(type => {
    const filePath = path.join(MODULES_JSON_DIR, TYPE_FILE_MAP[type])
    fs.writeFileSync(filePath, JSON.stringify(buckets[type], null, 2), 'utf8')
  })
}

function registerVmChatModulesJsonMiddleware(app) {
  app.get(ROUTE, (req, res) => {
    try {
      const templates = readAllTemplates()
      res.json({ ok: true, templates })
    } catch (error) {
      res.status(500).json({
        ok: false,
        message: error && error.message ? error.message : String(error || 'read failed')
      })
    }
  })

  app.post(ROUTE, async (req, res) => {
    try {
      const rawBody = await readRequestBody(req)
      const payload = rawBody ? JSON.parse(rawBody) : {}
      const templates = Array.isArray(payload.templates) ? payload.templates : payload
      writeTemplatesByType(templates)
      res.json({ ok: true })
    } catch (error) {
      res.status(500).json({
        ok: false,
        message: error && error.message ? error.message : String(error || 'write failed')
      })
    }
  })
}

module.exports = {
  MODULES_JSON_DIR,
  registerVmChatModulesJsonMiddleware
}
