function cloneParams(params) {
  return Object.assign({}, params && typeof params === 'object' ? params : {})
}

function normalizeText(value) {
  return String(value === undefined || value === null ? '' : value)
    .trim()
    .replace(/\s+/g, '')
    .toLowerCase()
}

function normalizeBenchmarkLabel(value) {
  return normalizeText(value).replace(/指数$/, '')
}

function normalizeFrequencyLabel(value) {
  return normalizeText(value).replace(/频$/, '')
}

function normalizeOptions(options) {
  return (Array.isArray(options) ? options : [])
    .map(option => ({
      code: String(option && option.code !== undefined ? option.code : '').trim(),
      label: String(option && option.label !== undefined ? option.label : '').trim()
    }))
    .filter(option => option.code && option.label)
}

export function normalizeVmBenchmarkOptions(rows) {
  return normalizeOptions((Array.isArray(rows) ? rows : []).map(item => ({
    label: item && (item.DIM_NME !== undefined ? item.DIM_NME : item.label),
    code: item && (item.DIM_CDE !== undefined ? item.DIM_CDE : (item.code !== undefined ? item.code : item.id))
  })))
}

export function normalizeVmDataFrequencyOptions(rows) {
  return normalizeOptions((Array.isArray(rows) ? rows : [])
    .filter(item => item && (item.dimStatus === undefined || item.dimStatus === null || String(item.dimStatus) === '1'))
    .sort((left, right) => Number(left.dimOrd || 0) - Number(right.dimOrd || 0))
    .map(item => ({
      label: item.dimNme !== undefined ? item.dimNme : item.label,
      code: item.dimCde !== undefined ? item.dimCde : item.code
    })))
}

function resolveOption(input, options, config) {
  const value = String(input === undefined || input === null ? '' : input).trim()
  if (!value) throw new Error(config.displayName + '不能为空')

  const normalizedOptions = normalizeOptions(options)
  const codeMatches = normalizedOptions.filter(option => option.code === value)
  if (codeMatches.length === 1) return codeMatches[0].code
  if (codeMatches.length > 1) {
    throw new Error(config.displayName + '代码“' + value + '”在当前字典中不唯一')
  }

  const normalizedInput = config.normalizeLabel(value)
  const labelMatches = normalizedOptions.filter(option => config.normalizeLabel(option.label) === normalizedInput)
  if (labelMatches.length === 1) return labelMatches[0].code
  if (!labelMatches.length) {
    throw new Error(config.displayName + '“' + value + '”未在当前字典中找到')
  }
  throw new Error(config.displayName + '“' + value + '”匹配到多个代码，请使用更准确的名称')
}

function createCachedLoader(loader, displayName, cacheTtlMs) {
  let cachedOptions = null
  let cachedAt = 0
  let pending = null

  const load = async function loadOptions() {
    const now = Date.now()
    if (cachedOptions && now - cachedAt < cacheTtlMs) return cachedOptions
    if (pending) return pending
    pending = Promise.resolve()
      .then(() => loader())
      .then(options => {
        const normalized = normalizeOptions(options)
        if (!normalized.length) throw new Error(displayName + '字典为空')
        cachedOptions = normalized
        cachedAt = Date.now()
        pending = null
        return cachedOptions
      })
      .catch(error => {
        pending = null
        throw error
      })
    return pending
  }

  load.clear = function clearCache() {
    cachedOptions = null
    cachedAt = 0
    pending = null
  }
  return load
}

export function createVmParamResolver(options = {}) {
  if (typeof options.getBenchmarkOptions !== 'function') {
    throw new Error('缺少基准字典加载器')
  }
  if (typeof options.getDataFrequencyOptions !== 'function') {
    throw new Error('缺少频率字典加载器')
  }
  const cacheTtlMs = Number.isFinite(options.cacheTtlMs) && options.cacheTtlMs >= 0
    ? options.cacheTtlMs
    : 5 * 60 * 1000
  const loadBenchmarks = createCachedLoader(options.getBenchmarkOptions, '基准', cacheTtlMs)
  const loadDataFrequencies = createCachedLoader(options.getDataFrequencyOptions, '频率', cacheTtlMs)

  const resolver = async function resolveVmParams(params) {
    const resolved = cloneParams(params)
    const benchmarkMode = String(resolved.benchmarks || '')

    if (benchmarkMode === '1' || benchmarkMode === '2') {
      const benchmarkOptions = await loadBenchmarks()
      resolved.benchmarkA = resolveOption(resolved.benchmarkA, benchmarkOptions, {
        displayName: '基准',
        normalizeLabel: normalizeBenchmarkLabel
      })
      if (benchmarkMode === '2') {
        resolved.benchmarkB = resolveOption(resolved.benchmarkB, benchmarkOptions, {
          displayName: '基准',
          normalizeLabel: normalizeBenchmarkLabel
        })
      }
    }

    const dataFrequencyOptions = await loadDataFrequencies()
    resolved.dataFreq = resolveOption(resolved.dataFreq, dataFrequencyOptions, {
      displayName: '频率',
      normalizeLabel: normalizeFrequencyLabel
    })
    return resolved
  }

  resolver.clearCache = function clearCache() {
    loadBenchmarks.clear()
    loadDataFrequencies.clear()
  }
  return resolver
}
