import { hydrateVmDslReportBlock } from './vm-report-dsl-runtime.js'
import { logVmChatEvent } from './vm-logger.js'

export function assertVmUpdateHydrationSucceeded(hydrated, operation) {
  const status = hydrated && hydrated.renderState && hydrated.renderState.status
  if (status !== 'error') return hydrated
  const detail = hydrated.renderState.errorMessage ||
    hydrated.sourceData && hydrated.sourceData.runtime && hydrated.sourceData.runtime.lastError ||
    '未知错误'
  const error = new Error('更新失败，已保留原报表块：' + detail)
  error.code = 'VM_UPDATE_HYDRATION_FAILED'
  error.retryOperation = operation
  throw error
}

export async function hydrateVmBlock(block, fetcher, options = {}) {
  const traceId = options.traceId || ''
  const source = block && typeof block === 'object' ? block : {}
  if (!source.dsl) {
    logVmChatEvent('block-hydrator', 'hydrate.skip', {
      blockId: source.blockId,
      reason: 'missing dsl'
    }, { traceId })
    return Object.assign({}, source, {
      renderState: {
        status: 'ready',
        hydratedAt: new Date().toISOString()
      }
    })
  }
  logVmChatEvent('block-hydrator', 'hydrate.start', {
    blockId: source.blockId,
    title: source.title,
    viewType: source.viewType || source.type,
    requestCount: Array.isArray(source.dsl && source.dsl.requests) ? source.dsl.requests.length : 0
  }, { traceId })
  const hydrated = await hydrateVmDslReportBlock(source, fetcher, options)
  logVmChatEvent('block-hydrator', 'hydrate.done', {
    blockId: hydrated.blockId,
    status: hydrated.renderState && hydrated.renderState.status,
    rowCount: Array.isArray(hydrated.renderSpec && hydrated.renderSpec.rows)
      ? hydrated.renderSpec.rows.length
      : hydrated.renderSpec && hydrated.renderSpec.option && hydrated.renderSpec.option.dataset && Array.isArray(hydrated.renderSpec.option.dataset.source)
        ? hydrated.renderSpec.option.dataset.source.length
        : 0
  }, {
    traceId,
    level: hydrated.renderState && hydrated.renderState.status === 'error' ? 'error' : 'info'
  })
  return hydrated
}
