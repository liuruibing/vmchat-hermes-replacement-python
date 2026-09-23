async page => {
  const liveMode = '__VM_CHAT_BROWSER_LIVE__' === 'true'
  const liveApiTokenBase64 = '__VM_CHAT_API_TOKEN_BASE64__'
  const dsl = {
    action: 'create',
    id: '550e8400-e29b-41d4-a716-446655440099',
    params: {
      fundCode: 'SM0513',
      beginDate: '2022-01-01',
      endDate: '2022-01-31',
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
      function: 'function transform(responses) { var rows = responses.stock && responses.stock.body || []; return rows.map(function (row) { return { tradeDate: row.TDATE, stockExposure: row.F_STOCK_EXP === null || row.F_STOCK_EXP === undefined ? null : Number(row.F_STOCK_EXP) * 100 }; }); }'
    },
    view: {
      type: 'echarts',
      title: '浏览器端到端：股票净敞口时序',
      legend: { show: true, data: ['股票净敞口'] },
      dataset: { source: '$transform', dimensions: ['tradeDate', 'stockExposure'] },
      xAxis: { type: 'category', name: '日期' },
      yAxis: [{ type: 'value', name: '%' }],
      series: [{
        type: 'line',
        name: '股票净敞口',
        encode: { x: 'tradeDate', y: 'stockExposure' },
        yAxisIndex: 0,
        format: { type: 'percentage', digits: 2 }
      }]
    }
  }
  const secondDsl = JSON.parse(JSON.stringify(dsl))
  secondDsl.id = '550e8400-e29b-41d4-a716-446655440098'
  secondDsl.view.title = '浏览器端到端：第二个股票净敞口时序'
  const firstUpdateDsl = JSON.parse(JSON.stringify(dsl))
  firstUpdateDsl.action = 'update'
  firstUpdateDsl.view.title = '不应提交：第一个批量更新'
  const secondUpdateDsl = JSON.parse(JSON.stringify(secondDsl))
  secondUpdateDsl.action = 'update'
  secondUpdateDsl.params.benchmarkA = '不存在的基准'
  secondUpdateDsl.view.title = '不应提交：第二个批量更新'
  const hermesOutputs = [dsl, secondDsl, [firstUpdateDsl, secondUpdateDsl]]
  const state = {
    hermesRunSeen: false,
    hermesRunCount: 0,
    businessRequestSeen: false,
    businessParamsResolved: false
  }

  await page.addInitScript(({ liveMode, liveApiTokenBase64 }) => {
    try {
      if (liveMode) window.localStorage.setItem('BDSUGSTORED', window.atob(liveApiTokenBase64))
      window.localStorage.setItem('BAIDUID', JSON.stringify({ account: 'vm-chat-e2e' }))
      window.localStorage.setItem('fof-research-hermes-base-url', '/hermes-api')
      window.localStorage.setItem('fof-research-hermes-api-key', 'vm-chat-browser-e2e-hermes-key')
    } catch (error) {
      // transform.function runs in a sandboxed iframe without localStorage access.
    }
  }, { liveMode, liveApiTokenBase64 })

  await page.route('**/*', async route => {
    const request = route.request()
    const requestUrl = request.url()
    const path = requestUrl.split('?')[0]
    const queryParam = name => {
      const match = requestUrl.match(new RegExp('[?&]' + name + '=([^&]*)'))
      return match ? decodeURIComponent(match[1].replace(/\+/g, ' ')) : null
    }
    const fulfillJson = body => route.fulfill({
      status: 200,
      contentType: 'application/json',
      headers: {
        'access-control-allow-origin': 'http://127.0.0.1:19528',
        'access-control-allow-credentials': 'true',
        'access-control-allow-headers': 'authorization,content-type',
        'access-control-allow-methods': 'GET,POST,OPTIONS'
      },
      body: JSON.stringify(body)
    })

    if (request.method() === 'OPTIONS' && requestUrl.includes('192.168.1.203:8010')) {
      if (liveMode) return route.continue()
      return route.fulfill({
        status: 204,
        headers: {
          'access-control-allow-origin': 'http://127.0.0.1:19528',
          'access-control-allow-credentials': 'true',
          'access-control-allow-headers': 'authorization,content-type',
          'access-control-allow-methods': 'GET,POST,OPTIONS'
        }
      })
    }

    if (path.endsWith('/api/system/v1.0/getMenuAll')) {
      return fulfillJson({
        status: 0,
        data: [{
          id: 'vm-chat-e2e-menu',
          pId: '0',
          name: '测试首页',
          vcactionname: '测试首页',
          vcactioncode: 'VM_CHAT_E2E',
          vcactiontype: 'PAGE.PERMISSION.TYPE.MU',
          vcstatus: '启用',
          vcmodel: '内部链接',
          vcurl: '/dashboard',
          vcremark: 'views/home/index',
          vcicon: 'dashboard'
        }]
      })
    }
    if (path.includes('/api/system/passwordPolicy/getPwdStrategy')) {
      return fulfillJson({ status: 0, data: {} })
    }
    if (path.includes('dynamicReport')) {
      return fulfillJson({ status: 0, data: [] })
    }
    if (path.endsWith('/api/report/v1.0/data/sql/868b4212-9d41-4ac0-a3db-8896d2913541')) {
      return fulfillJson({ status: 0, data: [{ beginDate: '20220101', endDate: '20220131' }] })
    }
    if (path.endsWith('/api/report/v1.0/data/sql/d43c924b-eebd-4d8f-97e5-ed46b609456d')) {
      if (liveMode) return route.continue()
      return fulfillJson({ status: 0, data: [{ DIM_NME: '沪深300', DIM_CDE: '000300' }] })
    }
    if (path.includes('/api/report/v1.0/data/sql/')) {
      return fulfillJson({ status: 0, data: [] })
    }
    if (path.includes('/api/common/edim/')) {
      if (path.endsWith('/api/common/edim/DATAFREQ')) {
        if (liveMode) return route.continue()
        return fulfillJson({ status: 0, data: [{ dimNme: '日频', dimCde: '1', dimStatus: '1', dimOrd: 1 }] })
      }
      return fulfillJson({ status: 0, data: [] })
    }
    if (path.endsWith('/hermes-api/v1/wiki/tree')) {
      return fulfillJson({
        catalogVersion: '1.0.0',
        tree: [
          {
            type: 'directory',
            name: 'catalog',
            path: 'catalog',
            children: [
              { type: 'file', name: 'index.md', path: 'catalog/index.md', documentId: 'index' },
              { type: 'file', name: 'metrics.md', path: 'catalog/metrics.md', documentId: 'metrics' },
              {
                type: 'directory',
                name: 'modules',
                path: 'catalog/modules',
                children: [
                  { type: 'file', name: 'stockExposureTiming.md', path: 'catalog/modules/stockExposureTiming.md', documentId: 'stockExposureTiming' }
                ]
              }
            ]
          }
        ]
      })
    }
    if (path.endsWith('/hermes-api/v1/wiki/documents/index')) {
      return fulfillJson({
        documentId: 'index',
        path: 'catalog/index.md',
        markdown: '# VM 模块索引\n\n欢迎查看 VM 模块索引说明文档。'
      })
    }
    if (path.endsWith('/hermes-api/v1/wiki/documents/stockExposureTiming')) {
      return fulfillJson({
        documentId: 'stockExposureTiming',
        path: 'catalog/modules/stockExposureTiming.md',
        markdown: '# 股票净敞口时序\n\n| 指标 | 说明 |\n| --- | --- |\n| 股票净敞口 | 展示产品股票持仓净敞口趋势 |\n'
      })
    }
    if (path.endsWith('/hermes-api/v1/runs') && request.method() === 'POST') {
      const payload = request.postDataJSON()
      if (!Array.isArray(payload.skills) || !payload.skills.includes('vm-report-dsl')) {
        return route.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ error: 'missing vm-report-dsl skill' }) })
      }
      if (!String(payload.instructions || '').includes('当前 currentDsls：')) {
        return route.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ error: 'missing currentDsls context' }) })
      }
      state.hermesRunSeen = true
      state.hermesRunCount += 1
      if (liveMode) return route.continue()
      if (!hermesOutputs[state.hermesRunCount - 1]) {
        return route.fulfill({ status: 400, contentType: 'application/json', body: JSON.stringify({ error: 'unexpected Hermes run' }) })
      }
      return fulfillJson({ run_id: 'vm-chat-browser-e2e-run-' + state.hermesRunCount })
    }
    const runEventMatch = path.match(/\/hermes-api\/v1\/runs\/vm-chat-browser-e2e-run-(\d+)\/events$/)
    if (runEventMatch) {
      const output = hermesOutputs[Number(runEventMatch[1]) - 1]
      const content = JSON.stringify(output)
      const body = [
        'data: ' + JSON.stringify({ event: 'message.delta', delta: content }),
        '',
        'data: ' + JSON.stringify({ event: 'run.completed', usage: { input_tokens: 1, output_tokens: 1 } }),
        '',
        ''
      ].join('\n')
      return route.fulfill({ status: 200, contentType: 'text/event-stream', headers: { 'cache-control': 'no-cache' }, body })
    }
    if (liveMode && /\/hermes-api\/v1\/runs\/[^/]+\/events$/.test(path)) {
      return route.continue()
    }
    if (path.endsWith('/rest/report/getSqlDataBySqlCode.do')) {
      state.businessRequestSeen = true
      state.businessParamsResolved = queryParam('sqlCode') === '712b930b-87a5-4cba-8da0-3671d4c8dc54' &&
        queryParam('benchmarkA') === '000300' &&
        queryParam('dataFreq') === '1' &&
        queryParam('fundCode') === 'SM0513'
      if (liveMode) return route.continue()
      if (!state.businessParamsResolved) {
        return fulfillJson({ status: -1, message: '动态参数没有在业务请求前解析' })
      }
      return fulfillJson({
        status: 0,
        head: { benchmarks: '1', dataFreq: '1' },
        body: [
          { TDATE: '20220104', F_STOCK_EXP: 0.51 },
          { TDATE: '20220105', F_STOCK_EXP: 0.49 }
        ]
      })
    }
    if (requestUrl.includes('192.168.1.203:8010')) {
      return fulfillJson({ status: 0, data: [] })
    }
    return route.continue()
  })

  const browserErrors = []
  page.on('pageerror', error => browserErrors.push(error.stack || error.message))
  await page.goto('http://127.0.0.1:19528/#/login', { waitUntil: 'domcontentloaded' })
  await page.locator('#app').waitFor({ state: 'attached', timeout: 30000 })
  await page.evaluate(({ liveMode, liveApiTokenBase64 }) => {
    const app = document.querySelector('#app') && document.querySelector('#app').__vue__
    if (!app || !app.$store || !app.$router) throw new Error('无法取得 Vue 根实例')
    const apiToken = liveMode ? window.atob(liveApiTokenBase64) : 'vm-chat-browser-e2e-token'
    window.localStorage.setItem('BDSUGSTORED', apiToken)
    app.$store.commit('SET_TOKEN', apiToken)
    app.$store.commit('SET_ROLES', ['vm-chat-e2e'])
    app.$store.commit('SET_ROUTERS', [])
    return app.$router.push('/vmChat/index')
  }, { liveMode, liveApiTokenBase64 })
  try {
    await page.locator('.composer textarea').waitFor({ state: 'visible', timeout: 30000 })
  } catch (error) {
    const bodyText = await page.locator('body').innerText().catch(() => '')
    const bodyHtml = await page.locator('body').innerHTML().catch(() => '')
    const scripts = await page.locator('script').evaluateAll(nodes => nodes.map(node => node.src)).catch(() => [])
    throw new Error('vmChat 输入框未出现；pageerror=' + browserErrors.join(' | ') + '；body=' + bodyText.slice(0, 1000) + '；html=' + bodyHtml.slice(0, 1000) + '；scripts=' + scripts.join(','))
  }
  await page.locator('.render-wiki-trigger').click()
  await page.locator('.wiki-dialog').waitFor({ state: 'visible', timeout: 10000 })
  await page.getByText('index.md', { exact: false }).waitFor({ state: 'visible', timeout: 10000 })
  await page.getByText('stockExposureTiming.md', { exact: false }).waitFor({ state: 'visible', timeout: 10000 })
  await page.locator('.wiki-document-content h1').filter({ hasText: 'VM 模块索引' }).waitFor({ state: 'visible', timeout: 10000 })
  await page.getByText('stockExposureTiming.md', { exact: true }).click()
  await page.locator('.wiki-document-content h1').filter({ hasText: '股票净敞口时序' }).waitFor({ state: 'visible', timeout: 10000 })
  await page.locator('.wiki-sidebar .el-tree-node.is-current').filter({ hasText: 'stockExposureTiming.md' }).waitFor({ state: 'visible', timeout: 10000 })
  await page.locator('.wiki-dialog .el-dialog__headerbtn').click()
  await page.locator('.wiki-dialog').waitFor({ state: 'hidden', timeout: 10000 })
  await page.locator('.composer textarea').fill('展示产品 SM0513 在 2022-01-01 到 2022-01-31 的股票净敞口时序全部指标日频数据，用沪深300单基准，使用折线图')
  await page.locator('.composer-actions button').filter({ hasText: '发送' }).click()
  const firstBlock = liveMode
    ? page.locator('.report-block').first()
    : page.locator('#vm-chat-block-550e8400-e29b-41d4-a716-446655440099')
  await firstBlock.waitFor({ state: 'visible', timeout: 180000 })
  await firstBlock.locator('.block-chart canvas').waitFor({ state: 'visible', timeout: 60000 })

  if (liveMode) {
    await firstBlock.getByText('状态：ready', { exact: true }).waitFor({ state: 'visible', timeout: 60000 })
    if (!state.hermesRunSeen || state.hermesRunCount !== 1) throw new Error('live 浏览器链路没有唯一调用 Hermes run')
    if (!state.businessRequestSeen) throw new Error('live 浏览器链路没有调用真实 VM SQL 接口')
    if (!state.businessParamsResolved) throw new Error('live 浏览器业务请求没有使用实时字典 code')
    if (browserErrors.length) throw new Error('live 浏览器运行错误：' + browserErrors.join(' | '))
    return { liveMode: true, blockCount: await page.locator('.report-block').count(), hermesRunCount: state.hermesRunCount, businessParamsResolved: true }
  }

  await page.getByText('浏览器端到端：股票净敞口时序', { exact: true }).waitFor({ state: 'visible', timeout: 30000 })

  await page.waitForFunction(() => {
    const button = Array.from(document.querySelectorAll('.composer-actions button')).find(node => node.textContent.includes('发送'))
    return button && !button.disabled
  })
  await page.locator('.composer textarea').fill('再新增一张股票净敞口时序图')
  await page.locator('.composer-actions button').filter({ hasText: '发送' }).click()
  await page.locator('#vm-chat-block-550e8400-e29b-41d4-a716-446655440098').waitFor({ state: 'visible', timeout: 90000 })
  await page.getByText('浏览器端到端：第二个股票净敞口时序', { exact: true }).waitFor({ state: 'visible', timeout: 30000 })

  await page.waitForFunction(() => {
    const button = Array.from(document.querySelectorAll('.composer-actions button')).find(node => node.textContent.includes('发送'))
    return button && !button.disabled
  })
  await page.locator('.composer textarea').fill('批量更新全部模块；如果任意一个失败就不要提交任何修改')
  await page.locator('.composer-actions button').filter({ hasText: '发送' }).click()
  await page.getByText(/不存在的基准.*未在当前字典中找到/).first().waitFor({ state: 'visible', timeout: 90000 })

  const blockCount = await page.locator('.report-block').count()
  const firstOriginalTitleCount = await page.getByText('浏览器端到端：股票净敞口时序', { exact: true }).count()
  const secondOriginalTitleCount = await page.getByText('浏览器端到端：第二个股票净敞口时序', { exact: true }).count()
  const uncommittedTitleCount = await page.getByText(/不应提交：/).count()
  if (!state.hermesRunSeen) throw new Error('浏览器没有创建 Hermes run')
  if (!state.businessRequestSeen) {
    const blockText = await page.locator('.report-block').allInnerTexts()
    const messageText = await page.locator('.message-content').allInnerTexts()
    throw new Error('浏览器没有调用 VM SQL 接口；block=' + blockText.join(' | ') + '；messages=' + messageText.join(' | ') + '；pageerror=' + browserErrors.join(' | '))
  }
  if (!state.businessParamsResolved) throw new Error('浏览器业务请求没有使用动态字典 code')
  if (state.hermesRunCount !== 3) throw new Error('预期创建 3 个 Hermes run，实际为 ' + state.hermesRunCount)
  if (blockCount !== 2) throw new Error('预期渲染 2 个报表块，实际为 ' + blockCount)
  if (firstOriginalTitleCount !== 1 || secondOriginalTitleCount !== 1 || uncommittedTitleCount !== 0) {
    throw new Error('批量 update 失败后画布发生了部分提交')
  }
  if (browserErrors.length) throw new Error('浏览器运行错误：' + browserErrors.join(' | '))

  return { blockCount, hermesRunCount: state.hermesRunCount, businessParamsResolved: state.businessParamsResolved, atomicBatchRollback: true }
}
