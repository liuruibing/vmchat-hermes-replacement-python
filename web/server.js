'use strict'

const fs = require('fs')
const http = require('http')
const https = require('https')
const path = require('path')
const { URL } = require('url')

const port = Number(process.env.PORT || 3000)
const host = '0.0.0.0'
const distDir = path.resolve(__dirname, 'dist')

const MIME_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.map': 'application/json; charset=utf-8',
  '.pdf': 'application/pdf'
}

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload)
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store'
  })
  res.end(body)
}

function safeStaticPath(urlPath) {
  let decoded
  try {
    decoded = decodeURIComponent(urlPath.split('?')[0])
  } catch (error) {
    return null
  }

  const normalized = path.posix.normalize('/' + decoded).replace(/^\/+/, '')
  const absolute = path.resolve(distDir, normalized)
  if (absolute !== distDir && !absolute.startsWith(distDir + path.sep)) return null
  return absolute
}

function serveFile(req, res, filePath) {
  fs.stat(filePath, (statError, stat) => {
    if (statError || !stat.isFile()) {
      const indexPath = path.join(distDir, 'index.html')
      fs.stat(indexPath, (indexError, indexStat) => {
        if (indexError || !indexStat.isFile()) {
          sendJson(res, 503, {
            ok: false,
            error: 'Frontend bundle is unavailable. Run the production build before starting the server.'
          })
          return
        }
        streamFile(req, res, indexPath, false)
      })
      return
    }
    streamFile(req, res, filePath, true)
  })
}

function streamFile(req, res, filePath, cacheable) {
  const ext = path.extname(filePath).toLowerCase()
  const headers = {
    'Content-Type': MIME_TYPES[ext] || 'application/octet-stream',
    'X-Content-Type-Options': 'nosniff',
    'Referrer-Policy': 'same-origin'
  }

  if (cacheable && /\.[0-9a-f]{8}\./i.test(path.basename(filePath))) {
    headers['Cache-Control'] = 'public, max-age=31536000, immutable'
  } else {
    headers['Cache-Control'] = 'no-cache'
  }

  res.writeHead(200, headers)
  if (req.method === 'HEAD') {
    res.end()
    return
  }
  fs.createReadStream(filePath).pipe(res)
}

function buildProxyTarget(baseUrl, incomingUrl, stripPrefix, replacementPrefix) {
  const source = String(incomingUrl || '/')
  const queryIndex = source.indexOf('?')
  const rawPath = queryIndex >= 0 ? source.slice(0, queryIndex) : source
  const query = queryIndex >= 0 ? source.slice(queryIndex) : ''

  let nextPath = rawPath
  if (stripPrefix && nextPath.indexOf(stripPrefix) === 0) {
    nextPath = nextPath.slice(stripPrefix.length)
  }
  if (!nextPath.startsWith('/')) nextPath = '/' + nextPath

  if (replacementPrefix) {
    nextPath = replacementPrefix.replace(/\/$/, '') + nextPath
  }

  const target = new URL(baseUrl)
  const basePath = target.pathname && target.pathname !== '/'
    ? target.pathname.replace(/\/$/, '')
    : ''
  target.pathname = basePath + nextPath
  target.search = query
  return target
}

function proxyRequest(req, res, options) {
  const baseUrl = String(options.baseUrl || '').trim()
  if (!baseUrl) {
    sendJson(res, 502, {
      ok: false,
      error: options.missingMessage || 'Proxy backend is not configured.'
    })
    return
  }

  let target
  try {
    target = buildProxyTarget(
      baseUrl,
      req.url,
      options.stripPrefix || '',
      options.replacementPrefix || ''
    )
  } catch (error) {
    sendJson(res, 500, { ok: false, error: 'Invalid proxy backend URL.' })
    return
  }

  const headers = Object.assign({}, req.headers)
  delete headers.host
  delete headers.origin
  delete headers.referer
  delete headers['content-length']

  headers.host = target.host
  headers['x-forwarded-host'] = req.headers.host || ''
  headers['x-forwarded-proto'] = 'https'

  if (options.apiKey) {
    headers.authorization = 'Bearer ' + options.apiKey
  }

  const transport = target.protocol === 'https:' ? https : http
  const upstream = transport.request({
    protocol: target.protocol,
    hostname: target.hostname,
    port: target.port || undefined,
    method: req.method,
    path: target.pathname + target.search,
    headers
  }, upstreamRes => {
    const responseHeaders = Object.assign({}, upstreamRes.headers)
    responseHeaders['x-accel-buffering'] = 'no'
    responseHeaders['cache-control'] = responseHeaders['cache-control'] || 'no-cache, no-transform'
    delete responseHeaders['content-length']

    res.writeHead(upstreamRes.statusCode || 502, responseHeaders)
    upstreamRes.pipe(res)
  })

  upstream.on('error', error => {
    if (res.headersSent) {
      res.destroy(error)
      return
    }
    sendJson(res, 502, {
      ok: false,
      error: 'Upstream request failed: ' + error.message
    })
  })

  req.pipe(upstream)
}

const server = http.createServer((req, res) => {
  const requestUrl = String(req.url || '/')

  if (requestUrl === '/health' || requestUrl.indexOf('/health?') === 0) {
    sendJson(res, 200, {
      ok: true,
      service: 'vmchat-web',
      hermesProxyConfigured: Boolean(String(process.env.HERMES_BACKEND_URL || '').trim()),
      pflProxyConfigured: Boolean(String(process.env.PFL_BACKEND_URL || '').trim())
    })
    return
  }

  if (requestUrl === '/hermes-api' || requestUrl.indexOf('/hermes-api/') === 0) {
    proxyRequest(req, res, {
      baseUrl: process.env.HERMES_BACKEND_URL,
      apiKey: String(process.env.HERMES_BACKEND_API_KEY || '').trim(),
      stripPrefix: '/hermes-api',
      missingMessage: 'Hermes backend is not configured.'
    })
    return
  }

  if (requestUrl === '/pfl' || requestUrl.indexOf('/pfl/') === 0) {
    proxyRequest(req, res, {
      baseUrl: process.env.PFL_BACKEND_URL,
      stripPrefix: '/pfl',
      replacementPrefix: String(process.env.PFL_BACKEND_PREFIX || '/pflfofrest'),
      missingMessage: 'PFL backend is not configured for this preview deployment.'
    })
    return
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') {
    sendJson(res, 405, { ok: false, error: 'Method not allowed.' })
    return
  }

  const filePath = safeStaticPath(requestUrl)
  if (!filePath) {
    sendJson(res, 400, { ok: false, error: 'Invalid path.' })
    return
  }

  serveFile(req, res, filePath)
})

server.keepAliveTimeout = 65000
server.headersTimeout = 66000

server.listen(port, host, () => {
  console.log('[vmchat-web] listening on http://' + host + ':' + port)
  console.log('[vmchat-web] Hermes proxy configured:', Boolean(String(process.env.HERMES_BACKEND_URL || '').trim()))
  console.log('[vmchat-web] PFL proxy configured:', Boolean(String(process.env.PFL_BACKEND_URL || '').trim()))
})
