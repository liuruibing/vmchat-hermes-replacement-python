import Ajv from 'ajv'
import catalogContract from './generated/vm-report-catalog-contract.js'
import dslSchema from './generated/vm-report-dsl-schema.js'

const schemaValidator = new Ajv({ allErrors: true, jsonPointers: true }).compile(dslSchema)

function fail(message) {
  throw new Error(message)
}

function clone(value) {
  return JSON.parse(JSON.stringify(value))
}

function hasValue(value) {
  return value !== undefined &&
    value !== null &&
    (typeof value !== 'string' || value.trim() !== '')
}

function isPlaceholder(value) {
  return typeof value === 'string' && /^\{[^{}]+\}$/.test(value.trim())
}

function requireConcrete(value, label) {
  if (!hasValue(value) || isPlaceholder(value)) fail(label + ' 必须是已解析的有效值')
}

function requireSemanticLabel(value, label) {
  requireConcrete(value, label)
  if (!/[\u3400-\u9fff]/.test(String(value).trim())) {
    fail(label + ' 必须输出中文语义名称，不能输出动态字典 code')
  }
}

function formatSchemaErrors(errors) {
  return (errors || []).slice(0, 5).map(error => {
    const path = error.dataPath || '/'
    return path + ' ' + error.message
  }).join('；')
}

function validateStructuralContract(dsl) {
  // 新版 DSL 将查询条件移到页面级查询区，不再携带顶层 params。
  // 旧版 DSL 仍保留手工校验，以兼容已保存的历史模板。
  if (dsl && Object.prototype.hasOwnProperty.call(dsl, 'params')) return
  if (!schemaValidator(dsl)) {
    fail('DSL Schema 校验失败：' + formatSchemaErrors(schemaValidator.errors))
  }
}

function validateDateRange(beginDate, endDate) {
  const values = [
    ['开始日期', String(beginDate || '').replace(/-/g, '')],
    ['结束日期', String(endDate || '').replace(/-/g, '')]
  ]
  values.forEach(([label, digits]) => {
    if (!/^\d{8}$/.test(digits)) fail(label + ' 必须为 YYYYMMDD 或 YYYY-MM-DD')
    const year = Number(digits.slice(0, 4))
    const month = Number(digits.slice(4, 6))
    const day = Number(digits.slice(6, 8))
    const parsed = new Date(Date.UTC(year, month - 1, day))
    if (parsed.getUTCFullYear() !== year || parsed.getUTCMonth() !== month - 1 || parsed.getUTCDate() !== day) {
      fail(label + ' 不是有效日期')
    }
  })
  if (values[0][1] > values[1][1]) fail('开始日期不得晚于结束日期')
}

function escapeRegExp(value) {
  return String(value).replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
}

function sourceWritesField(source, field) {
  const escapedField = escapeRegExp(field)
  const objectPropertyPattern = new RegExp('(?:^|[,{}]\\s*)' + escapedField + '\\s*:', 'm')
  const assignedPropertyPattern = new RegExp('(?:\\.\\s*' + escapedField + '\\b|\\[\\s*[\'\"]' + escapedField + '[\'\"]\\s*\\])\\s*=')
  return objectPropertyPattern.test(source) || assignedPropertyPattern.test(source)
}

function assertCatalogBinding(request) {
  const moduleBinding = catalogContract.modules && catalogContract.modules[request.moduleId]
  if (!moduleBinding) fail('catalog 中不存在 request.moduleId：' + request.moduleId)
  if (moduleBinding.sqlCode !== request.sqlCode) {
    fail('request ' + request.id + '.sqlCode 与 catalog 模块 ' + request.moduleId + ' 不一致')
  }
  if (request.submoduleId && moduleBinding.submoduleIds.indexOf(request.submoduleId) === -1) {
    fail('request ' + request.id + '.submoduleId 未绑定到 catalog 父模块 ' + request.moduleId)
  }
}

function normalizeDateValue(value) {
  const text = String(value || '').trim()
  if (!text) return text
  if (/^\d{8}$/.test(text)) return text
  if (/^\d{4}-\d{2}-\d{2}$/.test(text)) return text.replace(/-/g, '')
  return text
}

function validateFormat(format, label) {
  if (!format || typeof format !== 'object' || Array.isArray(format)) {
    fail(label + ' 必须是对象')
  }
  const allowedTypes = ['raw', 'text', 'date', 'decimal', 'percentage']
  if (!allowedTypes.includes(format.type)) {
    fail(label + ' 使用了不支持的格式化类型：' + format.type)
  }
  if (format.digits !== undefined && (!Number.isInteger(format.digits) || format.digits < 0)) {
    fail(label + '.digits 必须是非负整数')
  }
  if (Object.prototype.hasOwnProperty.call(format, 'multiplier')) {
    fail(label + '.multiplier 已禁用；数值换算必须只在 transform.function 中执行一次')
  }
  ['prefix', 'suffix', 'nullValue'].forEach(property => {
    if (format[property] !== undefined && typeof format[property] !== 'string') {
      fail(label + '.' + property + ' 必须是字符串')
    }
  })
}

function normalizeVmReportDslShape(sourceDsl) {
  const source = sourceDsl && typeof sourceDsl === 'object' && !Array.isArray(sourceDsl)
    ? clone(sourceDsl)
    : sourceDsl
  if (!source || typeof source !== 'object' || Array.isArray(source)) return source

  if (Object.prototype.hasOwnProperty.call(source, 'params')) {
    const params = source.params && typeof source.params === 'object' && !Array.isArray(source.params)
      ? source.params
      : {}
    params.beginDate = normalizeDateValue(params.beginDate)
    params.endDate = normalizeDateValue(params.endDate)
    source.params = params
  }

  return source
}

export function validateVmReportDsl(dsl, context = {}, options = {}) {
  validateStructuralContract(dsl)
  dsl = normalizeVmReportDslShape(dsl)
  if (!dsl || typeof dsl !== 'object' || Array.isArray(dsl)) fail('DSL 必须是对象')

  if ('status' in dsl) fail('DSL 不再使用 status，请使用 action')
  if (['create', 'update'].indexOf(dsl.action) === -1) {
    fail('顶层 action 只能为 create 或 update')
  }

  requireConcrete(dsl.id, '顶层 id')
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(dsl.id)) {
    fail('顶层 id 必须是有效 UUID')
  }

  const currentId = context && context.currentId
  const currentDsl = context && context.currentDsl
  if (dsl.action === 'update' && options.enforceUpdateContext === true) {
    if (!currentId || !currentDsl || currentDsl.id !== currentId) {
      fail('update 缺少前端回传的 currentId 或 currentDsl')
    }
    if (dsl.id !== currentId) {
      fail('update 的顶层 id 必须复用前端回传的 currentId')
    }
  }

  const params = dsl.params
  if (Object.prototype.hasOwnProperty.call(dsl, 'params')) {
    if (!params || typeof params !== 'object' || Array.isArray(params)) {
      fail('DSL 顶层 params 必须是对象')
    }
    ['fundCode', 'beginDate', 'endDate', 'dataFreqOpen', 'benchmarks', 'dataFreq'].forEach(param => {
      requireConcrete(params[param], '顶层 params.' + param)
    })
    validateDateRange(params.beginDate, params.endDate)
    if (params.dataFreqOpen !== 'true') {
      fail('顶层 params.dataFreqOpen 必须为字符串 "true"')
    }
    if (!['0', '1', '2'].includes(params.benchmarks)) {
      fail('顶层 params.benchmarks 必须为字符串 "0"、"1" 或 "2"')
    }
    const hasBenchmarkA = Object.prototype.hasOwnProperty.call(params, 'benchmarkA')
    const hasBenchmarkB = Object.prototype.hasOwnProperty.call(params, 'benchmarkB')
    if (params.benchmarks === '0' && (hasBenchmarkA || hasBenchmarkB)) {
      fail('无基准模式不得包含 params.benchmarkA 或 params.benchmarkB')
    }
    if (params.benchmarks === '1') {
      requireSemanticLabel(params.benchmarkA, '顶层 params.benchmarkA')
      if (hasBenchmarkB) fail('单基准模式不得包含 params.benchmarkB')
    }
    if (params.benchmarks === '2') {
      requireSemanticLabel(params.benchmarkA, '顶层 params.benchmarkA')
      requireSemanticLabel(params.benchmarkB, '顶层 params.benchmarkB')
    }
    requireSemanticLabel(params.dataFreq, '顶层 params.dataFreq')
  }
  if ('pendingMappings' in dsl) {
    fail('DSL 不允许 pendingMappings；动态参数由前端执行期解析')
  }
  if ('resolvedParams' in dsl) {
    fail('DSL 不允许 resolvedParams；解析结果只保存在前端运行时诊断中')
  }

  if (!Array.isArray(dsl.requests) || !dsl.requests.length) {
    fail('DSL 必须包含 requests')
  }
  const requestIds = new Set()
  dsl.requests.forEach(request => {
    if (!request || typeof request !== 'object' || Array.isArray(request)) {
      fail('request 必须是对象')
    }
    requireConcrete(request.id, 'request.id')
    requireConcrete(request.moduleId, 'request ' + request.id + '.moduleId')
    requireConcrete(request.sqlCode, 'request ' + request.id + '.sqlCode')
    assertCatalogBinding(request)
    if (requestIds.has(request.id)) fail('request id 重复：' + request.id)
    requestIds.add(request.id)
    if ('type' in request) fail('request ' + request.id + ' 不应包含 type')
    if ('params' in request) fail('request ' + request.id + ' 不应重复包含 params')
  })

  if ('fieldMappings' in dsl) {
    fail('前端 DSL 不应包含 fieldMappings；原始字段映射仅用于 Hermes 内部生成 transform')
  }

  if (!dsl.transform || typeof dsl.transform !== 'object' || Array.isArray(dsl.transform)) {
    fail('DSL 必须包含 transform')
  }
  if (dsl.transform.language !== 'javascript') {
    fail('transform.language 必须为 javascript')
  }
  requireConcrete(dsl.transform.function, 'transform.function')
  const transformSource = dsl.transform.function
  if (!/^\s*function\s+transform\s*\(\s*responses\s*\)/.test(transformSource)) {
    fail('transform.function 必须使用 function transform(responses) 签名')
  }
  if (!/\breturn\b/.test(transformSource)) {
    fail('transform.function 必须返回前端可渲染的数据数组')
  }
  if (transformSource.includes('?.')) fail('transform.function 不支持可选链语法 ?.')
  if (transformSource.includes('??')) fail('transform.function 不支持空值合并语法 ??')
  if (/\.toFixed\s*\(/.test(transformSource)) fail('transform.function 不得使用 toFixed；展示格式化必须由 view.format 完成')
  try {
    Function('"use strict"; return (' + transformSource + ');')
  } catch (error) {
    fail('transform.function 无法编译')
  }
  requestIds.forEach(requestId => {
    const escapedId = escapeRegExp(requestId)
    const referencePattern = new RegExp('responses\\s*(?:\\.\\s*' + escapedId + '\\b|\\[\\s*[\'\"]' + escapedId + '[\'\"]\\s*\\])')
    if (!referencePattern.test(transformSource)) fail('transform.function 未引用 request：' + requestId)
  })

  if (!dsl.view || typeof dsl.view !== 'object' || Array.isArray(dsl.view)) {
    fail('DSL 必须包含 view')
  }
  if (!['table', 'echarts'].includes(dsl.view.type)) {
    fail('DSL 必须包含 table 或 echarts view')
  }

  if (dsl.view.type === 'table') {
    if (!Array.isArray(dsl.view.columns) || !dsl.view.columns.length) fail('table view 必须包含 columns')
    const columnFields = new Set()
    dsl.view.columns.forEach(column => {
      requireConcrete(column.field, 'column.field')
      if (columnFields.has(column.field)) fail('table column.field 重复：' + column.field)
      columnFields.add(column.field)
      requireConcrete(column.label, 'column ' + column.field + '.label')
      if (column.format !== undefined) validateFormat(column.format, 'column ' + column.field + '.format')
    })
  }

  if (dsl.view.type === 'echarts') {
    if ('xField' in dsl.view) {
      fail('echarts view 不再使用 xField，请使用 dataset.dimensions 与 series.encode')
    }
    if (!dsl.view.legend || typeof dsl.view.legend !== 'object' || Array.isArray(dsl.view.legend)) {
      fail('echarts view 必须包含 legend')
    }
    if (dsl.view.legend.show !== true) {
      fail('echarts legend.show 必须为 true')
    }
    if (!Array.isArray(dsl.view.legend.data) || !dsl.view.legend.data.length) {
      fail('echarts legend.data 必须是非空数组')
    }
    if (!dsl.view.dataset || typeof dsl.view.dataset !== 'object' || Array.isArray(dsl.view.dataset)) {
      fail('echarts view 必须包含 dataset')
    }
    if (dsl.view.dataset.source !== '$transform') {
      fail('echarts dataset.source 必须为 "$transform"')
    }
    if (!Array.isArray(dsl.view.dataset.dimensions) || !dsl.view.dataset.dimensions.length) {
      fail('echarts dataset.dimensions 必须是非空数组')
    }
    const dimensionSet = new Set(dsl.view.dataset.dimensions)
    const xFields = new Set()
    const legendNames = []
    let cartesianSeriesCount = 0
    if (!Array.isArray(dsl.view.series) || !dsl.view.series.length) {
      fail('echarts view 必须包含 series')
    }
    dsl.view.series.forEach((series, index) => {
      if (!series || typeof series !== 'object' || Array.isArray(series)) fail('series 必须是对象')
      if ('chartType' in series) fail('echarts series 不再使用 chartType，请使用 type')
      requireConcrete(series.name, 'series[' + index + '].name')
      requireConcrete(series.type, 'series ' + series.name + '.type')
      if (!['line', 'bar', 'pie'].includes(series.type)) {
        fail('不支持的 series.type：' + series.type)
      }
      if (!series.encode || typeof series.encode !== 'object' || Array.isArray(series.encode)) {
        fail('series 必须包含 encode')
      }
      if (series.type === 'pie') {
        requireConcrete(series.encode.itemName, 'series ' + series.name + '.encode.itemName')
        requireConcrete(series.encode.value, 'series ' + series.name + '.encode.value')
        if (!dimensionSet.has(series.encode.itemName)) {
          fail('series ' + series.name + '.encode.itemName 必须引用 dataset.dimensions 中的字段')
        }
        if (!dimensionSet.has(series.encode.value)) {
          fail('series ' + series.name + '.encode.value 必须引用 dataset.dimensions 中的字段')
        }
      } else {
        cartesianSeriesCount += 1
        if (series.yAxisIndex !== undefined && (!Number.isInteger(series.yAxisIndex) || series.yAxisIndex < 0)) {
          fail('series ' + series.name + '.yAxisIndex 必须是非负整数')
        }
        if (series.yAxisIndex !== undefined && series.yAxisIndex > 1) {
          fail('单个 ECharts 最多支持两个 Y 轴，yAxisIndex 只能为 0 或 1')
        }
        requireConcrete(series.encode.x, 'series ' + series.name + '.encode.x')
        requireConcrete(series.encode.y, 'series ' + series.name + '.encode.y')
        if (!dimensionSet.has(series.encode.x)) {
          fail('series ' + series.name + '.encode.x 必须引用 dataset.dimensions 中的字段')
        }
        if (!dimensionSet.has(series.encode.y)) {
          fail('series ' + series.name + '.encode.y 必须引用 dataset.dimensions 中的字段')
        }
        xFields.add(series.encode.x)
      }
      legendNames.push(series.name)
      if (series.format !== undefined) validateFormat(series.format, 'series ' + series.name + '.format')
    })
    dsl.view.legend.data.forEach(name => {
      if (!legendNames.includes(name)) fail('legend.data 包含未声明的 series：' + name)
    })
    if (JSON.stringify(dsl.view.legend.data) !== JSON.stringify(legendNames)) {
      fail('echarts legend.data 必须与 series.name 顺序一致')
    }
    if (xFields.size > 1) {
      fail('同一 ECharts 图表的非饼图 series 必须使用相同 encode.x')
    }
    if (cartesianSeriesCount > 0) {
      if (!dsl.view.xAxis || typeof dsl.view.xAxis !== 'object' || Array.isArray(dsl.view.xAxis)) {
        fail('包含 line/bar 的 echarts view 必须包含 xAxis 对象')
      }
      if (!Array.isArray(dsl.view.yAxis) || !dsl.view.yAxis.length) {
        fail('包含 line/bar 的 echarts view 必须包含非空 yAxis 数组')
      }
      dsl.view.series.filter(series => series.type !== 'pie').forEach(series => {
        const axisIndex = series.yAxisIndex === undefined ? 0 : series.yAxisIndex
        if (axisIndex >= dsl.view.yAxis.length) {
          fail('series ' + series.name + '.yAxisIndex 引用了不存在的 Y 轴')
        }
      })
    }
  }

  const viewFields = dsl.view.type === 'table'
    ? dsl.view.columns.map(column => column.field)
    : dsl.view.dataset.dimensions
  viewFields.forEach(field => {
    if (!sourceWritesField(transformSource, field)) {
      fail('transform.function 未生成 view 字段：' + field)
    }
  })

  return dsl
}
