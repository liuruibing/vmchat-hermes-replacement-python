#!/usr/bin/env node
import { readFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const transformRunner = fileURLToPath(new URL('./run-transform.mjs', import.meta.url));

function fail(message) {
  throw new Error(message);
}

function hasValue(value) {
  return value !== undefined
    && value !== null
    && (typeof value !== 'string' || value.trim() !== '');
}

function isPlaceholder(value) {
  return typeof value === 'string' && /^\{[^{}]+\}$/.test(value.trim());
}

function requireConcrete(value, label) {
  if (!hasValue(value) || isPlaceholder(value)) fail(`${label} 必须是已解析的有效值`);
}

function escapeRegExp(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function sourceWritesField(source, field) {
  const escapedField = escapeRegExp(field);
  const objectPropertyPattern = new RegExp(
    `(?:^|[,{]\\s*)${escapedField}\\s*:`,
    'm',
  );
  const assignedPropertyPattern = new RegExp(
    `(?:\\.\\s*${escapedField}\\b|\\[\\s*['"]${escapedField}['"]\\s*\\])\\s*=`,
  );
  return objectPropertyPattern.test(source) || assignedPropertyPattern.test(source);
}

function validateFormat(format, label) {
  if (!format || typeof format !== 'object' || Array.isArray(format)) {
    fail(`${label} 必须是对象`);
  }
  const allowedTypes = ['raw', 'text', 'date', 'decimal', 'percentage'];
  if (!allowedTypes.includes(format.type)) {
    fail(`${label} 使用了不支持的格式化类型：${format.type}`);
  }
  if (format.digits !== undefined
    && (!Number.isInteger(format.digits) || format.digits < 0)) {
    fail(`${label}.digits 必须是非负整数`);
  }
  if ('multiplier' in format) {
    fail(`${label}.multiplier 已禁用；数值换算必须只在 transform.function 中执行一次`);
  }
  for (const property of ['prefix', 'suffix', 'nullValue']) {
    if (format[property] !== undefined && typeof format[property] !== 'string') {
      fail(`${label}.${property} 必须是字符串`);
    }
  }
}

function requireStringArray(value, label) {
  if (!Array.isArray(value) || !value.length) fail(`${label} 必须是非空数组`);
  for (const item of value) {
    requireConcrete(item, label);
  }
}

export function validateDsl(dsl, context) {
  if (!dsl || typeof dsl !== 'object' || Array.isArray(dsl)) fail('DSL 必须是对象');
  if ('status' in dsl) fail('DSL 不再使用 status，请使用 action');
  if (!['create', 'update'].includes(dsl.action)) {
    fail('顶层 action 只能为 create 或 update');
  }
  requireConcrete(dsl.id, '顶层 id');
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(dsl.id)) {
    fail('顶层 id 必须是有效 UUID');
  }
  const currentId = context && context.currentId;
  const currentDsl = context && context.currentDsl;
  if (dsl.action === 'update') {
    if (!currentId || !currentDsl || currentDsl.id !== currentId) {
      fail('update 缺少前端回传的 currentId 或 currentDsl');
    }
    if (dsl.id !== currentId) {
      fail('update 的顶层 id 必须复用前端回传的 currentId');
    }
  }
  if (dsl.action === 'create' && (currentId || currentDsl)) {
    fail('create 不应携带 currentId 或 currentDsl 编辑上下文');
  }

  if (!Array.isArray(dsl.requests) || !dsl.requests.length) {
    fail('DSL 必须包含 requests');
  }

  if ('params' in dsl) {
    fail('DSL 不再使用顶层 params；请求参数由页面查询条件或数据接口层提供');
  }
  if ('pendingMappings' in dsl) {
    fail('DSL 不允许 pendingMappings');
  }

  const requestIds = new Set();

  for (const request of dsl.requests) {
    requireConcrete(request.id, 'request.id');
    requireConcrete(request.moduleId, `request ${request.id}.moduleId`);
    requireConcrete(request.sqlCode, `request ${request.id}.sqlCode`);
    if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i.test(request.sqlCode)) {
      fail(`request ${request.id}.sqlCode 必须是有效 UUID`);
    }
    if (requestIds.has(request.id)) fail(`request id 重复：${request.id}`);
    requestIds.add(request.id);
    if ('params' in request) fail(`request ${request.id} 不应重复包含 params`);
  }

  if ('fieldMappings' in dsl) {
    fail('前端 DSL 不应包含 fieldMappings；原始字段映射仅用于 Hermes 内部生成 transform');
  }

  if (!dsl.transform || typeof dsl.transform !== 'object' || Array.isArray(dsl.transform)) {
    fail('DSL 必须包含 transform');
  }
  if (dsl.transform.language !== 'javascript') {
    fail('transform.language 必须为 javascript');
  }
  requireConcrete(dsl.transform.function, 'transform.function');
  const transformSource = dsl.transform.function;
  if (!/^\s*function\s+transform\s*\(\s*responses\s*\)/.test(transformSource)) {
    fail('transform.function 必须使用 function transform(responses) 签名');
  }
  if (!/\breturn\b/.test(transformSource)) {
    fail('transform.function 必须返回前端可渲染的数据数组');
  }
  if (transformSource.includes('?.')) {
    fail('transform.function 不支持可选链语法 ?.');
  }
  if (transformSource.includes('??')) {
    fail('transform.function 不支持空值合并语法 ??');
  }
  if (/\.toFixed\s*\(/.test(transformSource)) {
    fail('transform.function 不得使用 toFixed；展示格式化必须由 view.format 完成');
  }
  if (/\b(?:process|require|module|globalThis|Function|eval|WebAssembly|fetch|XMLHttpRequest)\b|\b(?:constructor|prototype|__proto__)\b/.test(transformSource)) {
    fail('transform.function 包含禁止的宿主访问或动态代码执行能力');
  }
  try {
    Function(`"use strict"; return (${transformSource});`);
  } catch {
    fail('transform.function 无法编译');
  }
  for (const requestId of requestIds) {
    const escapedId = escapeRegExp(requestId);
    const referencePattern = new RegExp(
      `responses\\s*(?:\\.\\s*${escapedId}\\b|\\[\\s*['"]${escapedId}['"]\\s*\\])`,
    );
    if (!referencePattern.test(transformSource)) {
      fail(`transform.function 未引用 request：${requestId}`);
    }
  }
  if (!dsl.view || !['table', 'echarts'].includes(dsl.view.type)) {
    fail('DSL 必须包含 table 或 echarts view');
  }
  if ('dataAlignment' in dsl.view || 'rowKey' in dsl.view) {
    fail('view 不再使用 dataAlignment 或 rowKey，取值与合并必须由 transform 完成');
  }

  if (dsl.view.type === 'table') {
    if (!dsl.view.columns || !dsl.view.columns.length) fail('table view 必须包含 columns');
    const columnFields = new Set();
    for (const column of dsl.view.columns) {
      requireConcrete(column.field, 'column.field');
      if (columnFields.has(column.field)) fail(`table column.field 重复：${column.field}`);
      columnFields.add(column.field);
      requireConcrete(column.label, `column ${column.field}.label`);
      if ('requestId' in column) {
        fail('transform 已统一输出数据，column 不应包含 requestId');
      }
      if (column.format !== undefined) {
        validateFormat(column.format, `column ${column.field}.format`);
      }
    }
  }
  if (dsl.view.type === 'echarts') {
    if ('xField' in dsl.view) {
      fail('echarts view 不再使用 xField，请使用 dataset.dimensions 与 series.encode');
    }
    if (!dsl.view.dataset || typeof dsl.view.dataset !== 'object' || Array.isArray(dsl.view.dataset)) {
      fail('echarts view 必须包含 dataset');
    }
    if (dsl.view.dataset.source !== '$transform') {
      fail('echarts dataset.source 必须为 "$transform"');
    }
    requireStringArray(dsl.view.dataset.dimensions, 'echarts dataset.dimensions');
    if (!dsl.view.legend || typeof dsl.view.legend !== 'object' || Array.isArray(dsl.view.legend)) {
      fail('echarts view 必须包含 legend');
    }
    if (dsl.view.legend.show !== true) {
      fail('echarts legend.show 必须为 true');
    }
    requireStringArray(dsl.view.legend.data, 'echarts legend.data');
    const dimensions = new Set(dsl.view.dataset.dimensions);
    if (!dsl.view.series || !dsl.view.series.length) {
      fail('echarts view 必须包含 series');
    }
    const xFields = new Set();
    const seriesNames = [];
    let cartesianSeriesCount = 0;
    for (const series of dsl.view.series) {
      if ('field' in series) {
        fail('echarts series 不再使用 field，请使用 encode.y');
      }
      if ('chartType' in series) {
        fail('echarts series 不再使用 chartType，请使用 type');
      }
      requireConcrete(series.name, 'series.name');
      requireConcrete(series.type, `series ${series.name}.type`);
      if (!['line', 'bar', 'pie'].includes(series.type)) {
        fail(`不支持的 series.type：${series.type}`);
      }
      if (!series.encode || typeof series.encode !== 'object' || Array.isArray(series.encode)) {
        fail(`series ${series.name}.encode 必须是对象`);
      }
      if (series.type === 'pie') {
        requireConcrete(series.encode.itemName, `series ${series.name}.encode.itemName`);
        requireConcrete(series.encode.value, `series ${series.name}.encode.value`);
        if (!dimensions.has(series.encode.itemName)) {
          fail(`series ${series.name}.encode.itemName 未包含在 dataset.dimensions 中`);
        }
        if (!dimensions.has(series.encode.value)) {
          fail(`series ${series.name}.encode.value 未包含在 dataset.dimensions 中`);
        }
        if (series.yAxisIndex !== undefined) {
          fail(`pie series ${series.name} 不应包含 yAxisIndex`);
        }
      } else {
        cartesianSeriesCount += 1;
        requireConcrete(series.encode.x, `series ${series.name}.encode.x`);
        requireConcrete(series.encode.y, `series ${series.name}.encode.y`);
        if (!dimensions.has(series.encode.x)) {
          fail(`series ${series.name}.encode.x 未包含在 dataset.dimensions 中`);
        }
        if (!dimensions.has(series.encode.y)) {
          fail(`series ${series.name}.encode.y 未包含在 dataset.dimensions 中`);
        }
        xFields.add(series.encode.x);
      }
      seriesNames.push(series.name);
      if (series.yAxisIndex !== undefined
        && (!Number.isInteger(series.yAxisIndex) || series.yAxisIndex < 0)) {
        fail(`series ${series.name}.yAxisIndex 必须是非负整数`);
      }
      if (series.yAxisIndex !== undefined && series.yAxisIndex > 1) {
        fail('单个 ECharts 最多支持两个 Y 轴，yAxisIndex 只能为 0 或 1');
      }
      if ('requestId' in series) {
        fail('transform 已统一输出数据，series 不应包含 requestId');
      }
      if (series.format === undefined) {
        fail(`series ${series.name}.format 必须显式声明；未知展示格式请使用 {"type":"raw"}`);
      }
      validateFormat(series.format, `series ${series.name}.format`);
    }
    if (xFields.size > 1) {
      fail('单个 ECharts view 中所有 series.encode.x 必须使用同一个横轴字段');
    }
    if (cartesianSeriesCount > 0) {
      if (!dsl.view.xAxis || typeof dsl.view.xAxis !== 'object' || Array.isArray(dsl.view.xAxis)) {
        fail('包含 line/bar 的 echarts view 必须包含 xAxis 对象');
      }
      requireConcrete(dsl.view.xAxis.type, 'echarts xAxis.type');
      if (!Array.isArray(dsl.view.yAxis) || !dsl.view.yAxis.length) {
        fail('包含 line/bar 的 echarts view 必须包含非空 yAxis 数组');
      }
      if (dsl.view.yAxis.length > 2) {
        fail('单个 ECharts 最多支持两个 Y 轴');
      }
      for (let index = 0; index < dsl.view.yAxis.length; index += 1) {
        const axis = dsl.view.yAxis[index];
        if (!axis || typeof axis !== 'object' || Array.isArray(axis)) {
          fail(`echarts yAxis[${index}] 必须是对象`);
        }
        requireConcrete(axis.type, `echarts yAxis[${index}].type`);
      }
      for (const series of dsl.view.series.filter((item) => item.type !== 'pie')) {
        const axisIndex = series.yAxisIndex === undefined ? 0 : series.yAxisIndex;
        if (axisIndex >= dsl.view.yAxis.length) {
          fail(`series ${series.name}.yAxisIndex 引用了不存在的 Y 轴`);
        }
      }
    }
    if (JSON.stringify(dsl.view.legend.data) !== JSON.stringify(seriesNames)) {
      fail('echarts legend.data 必须与 series.name 顺序一致');
    }
  }

  const viewFields = dsl.view.type === 'table'
    ? dsl.view.columns.map((column) => column.field)
    : dsl.view.dataset.dimensions;
  for (const field of viewFields) {
    if (!sourceWritesField(transformSource, field)) {
      fail(`transform.function 未生成 view 字段：${field}`);
    }
  }

  return dsl;
}

function sourceReferencesDataPath(source, dataPath) {
  const segments = dataPath.split('[]').join('').split('.');
  let pattern = `\\b${escapeRegExp(segments[0])}\\b`;
  for (const segment of segments.slice(1)) {
    const escaped = escapeRegExp(segment);
    pattern += `(?:\\s*\\.\\s*${escaped}\\b|\\s*\\[\\s*['"]${escaped}['"]\\s*\\])`;
  }
  return new RegExp(pattern).test(source);
}

function splitCandidateNames(value) {
  return value.split(/[、,，]/).map((item) => item.trim()).filter(Boolean);
}

function mappingsForSeriesName(seriesName, mappings, allowQualified) {
  const exact = mappings.filter((mapping) => mapping.displayName === seriesName && mapping.requestId);
  if (exact.length || !allowQualified) return exact;
  const contained = mappings.filter((mapping) => mapping.requestId && seriesName.includes(mapping.displayName));
  if (!contained.length) return [];
  const longest = Math.max(...contained.map((mapping) => mapping.displayName.length));
  return contained.filter((mapping) => mapping.displayName.length === longest);
}

function collectLeafPaths(value, prefix = '', output = []) {
  if (Array.isArray(value)) {
    if (!value.length) output.push(prefix);
    else for (const item of value) collectLeafPaths(item, `${prefix}[]`, output);
    return output;
  }
  if (value && typeof value === 'object') {
    for (const [key, child] of Object.entries(value)) {
      collectLeafPaths(child, prefix ? `${prefix}.${key}` : key, output);
    }
    return output;
  }
  output.push(prefix);
  return output;
}

function referencedPropertyNames(source) {
  const names = new Set();
  for (const match of source.matchAll(/\.\s*([A-Za-z_$][\w$]*)|\[\s*['"]([^'"]+)['"]\s*\]/g)) {
    names.add(match[1] || match[2]);
  }
  return names;
}

function propertyNamesInJsonPath(pathValue) {
  return String(pathValue || '')
    .replace(/\[\]/g, '')
    .split('.')
    .map((segment) => segment.trim())
    .filter(Boolean);
}

function parseDisplayTransform(value) {
  const text = String(value || '').trim();
  const digitsMatch = text.match(/保留\s*(\d+)\s*位小数/);
  return {
    multiplier: /×\s*100|百分化/.test(text) ? 100 : (/÷\s*10000/.test(text) ? 0.0001 : 1),
    digits: digitsMatch ? Number(digitsMatch[1]) : undefined,
  };
}

function validateViewFormat(viewItem, mapping, label) {
  const rule = parseDisplayTransform(mapping.displayTransform);
  if (mapping.displayUnit && mapping.displayUnit !== '未明确' && 'unit' in viewItem && viewItem.unit !== mapping.displayUnit) {
    fail(`${label}.unit 与模块 MD 展示单位不一致`);
  }
  if (mapping.displayUnit && mapping.displayUnit !== '未明确' && !('unit' in viewItem) && label.startsWith('column ')) {
    fail(`${label}.unit 缺少模块 MD 展示单位：${mapping.displayUnit}`);
  }
  const needsPercentage = rule.multiplier === 100 && mapping.displayUnit === '%';
  const needsDecimal = rule.multiplier === 0.0001 || rule.digits !== undefined;
  if (!needsPercentage && !needsDecimal) return;
  if (!viewItem.format) fail(`${label}.format 缺少模块 MD 展示转换`);
  const expectedType = needsPercentage ? 'percentage' : 'decimal';
  if (viewItem.format.type !== expectedType) fail(`${label}.format.type 应为 ${expectedType}`);
  if (rule.digits !== undefined && viewItem.format.digits !== rule.digits) {
    fail(`${label}.format.digits 应为 ${rule.digits}`);
  }
  if (needsPercentage && viewItem.format.suffix !== '%') fail(`${label}.format.suffix 应为 %`);
}

function valuesAtPath(root, pathValue) {
  const segments = pathValue.replace(/\[\]/g, '.[]').split('.').filter(Boolean);
  let values = [root];
  for (const segment of segments) {
    const next = [];
    for (const value of values) {
      if (segment === '[]') {
        if (Array.isArray(value)) next.push(...value);
      } else if (value && typeof value === 'object' && Object.prototype.hasOwnProperty.call(value, segment)) {
        next.push(value[segment]);
      }
    }
    values = next;
  }
  return values;
}

function equivalentValue(actual, expected) {
  if (actual === expected) return true;
  if (typeof actual === 'number' && typeof expected === 'number' && Number.isFinite(actual) && Number.isFinite(expected)) {
    return Math.abs(actual - expected) <= Math.max(1, Math.abs(expected)) * 1e-9;
  }
  return false;
}

function outputFieldChanged(baseline, probe, field) {
  const select = (rows) => Array.isArray(rows) ? rows.map((row) => row && row[field]) : rows;
  return JSON.stringify(select(baseline)) !== JSON.stringify(select(probe));
}

function runTransformIsolated(source, responses, probes) {
  const result = spawnSync(
    process.execPath,
    ['--max-old-space-size=64', '--disable-proto=throw', '--permission', `--allow-fs-read=${transformRunner}`, transformRunner],
    {
      input: JSON.stringify({ source, responses, probes, timeout: 500 }),
      encoding: 'utf8',
      env: {},
      timeout: 15000,
      maxBuffer: 20 * 1024 * 1024,
    },
  );
  if (result.error || result.status !== 0) fail('transform.function 隔离执行失败');
  let parsed;
  try { parsed = JSON.parse(result.stdout); }
  catch { fail('transform.function 隔离执行结果无法解析'); }
  if (parsed.error) fail(`transform.function 隔离执行失败：${parsed.error}`);
  return parsed;
}

function parseCatalogModule(markdown, expectedModuleId) {
  const frontmatter = markdown.match(/^---\s*\n([\s\S]*?)\n---/);
  if (!frontmatter) fail(`catalog 模块 ${expectedModuleId} 缺少 YAML 头`);
  const readYamlScalar = (key) => {
    const match = frontmatter[1].match(new RegExp(`^${key}:\\s*["']?([^"'\\n]+)["']?\\s*$`, 'm'));
    return match && match[1].trim();
  };
  const moduleId = readYamlScalar('moduleId');
  const sqlId = readYamlScalar('sqlId');
  if (moduleId !== expectedModuleId) {
    fail(`catalog 文件名与 YAML moduleId 不一致：${expectedModuleId}`);
  }
  requireConcrete(sqlId, `catalog 模块 ${expectedModuleId}.sqlId`);
  const exampleMatch = markdown.match(/## 示例 JSON 数据[\s\S]*?```json\s*\n([\s\S]*?)\n```/);
  if (!exampleMatch) fail(`catalog 模块 ${expectedModuleId} 缺少示例 JSON 数据`);
  let example;
  try {
    example = JSON.parse(exampleMatch[1]);
  } catch {
    fail(`catalog 模块 ${expectedModuleId} 的示例 JSON 无法解析`);
  }
  const mappingSection = markdown.match(/## 字段映射\s*\n([\s\S]*?)(?=\n## |$)/);
  if (!mappingSection) fail(`catalog 模块 ${expectedModuleId} 缺少字段映射`);
  const fieldMappings = mappingSection[1]
    .split('\n')
    .map((line) => line.trim())
    .filter((line) => line.startsWith('|') && line.endsWith('|'))
    .map((line) => line.slice(1, -1).split('|').map((cell) => cell.trim()))
    .filter((cells) => cells.length >= 3
      && cells[0] !== 'JSON 路径'
      && !/^[-:]+$/.test(cells[0]))
    .map((cells) => ({
      jsonPath: cells[0],
      rawField: cells[1],
      displayName: cells[2],
      displayTransform: cells[3] || '',
      displayUnit: cells[4] || '',
      applicableViews: (cells[5] || 'table、echarts')
        .split('、')
        .map((item) => item.trim())
        .filter(Boolean),
    }));
  if (!fieldMappings.length) fail(`catalog 模块 ${expectedModuleId} 的字段映射为空`);
  const readPolicyValue = (label) => {
    const match = markdown.match(new RegExp(`^\\s*- ${label}：(.+?)\\s*$`, 'm'));
    return match ? match[1].trim() : '';
  };
  return {
    sqlId,
    example,
    fieldMappings,
    submoduleSelection: readPolicyValue('子模块选择'),
    allSubmodules: readPolicyValue('全部子模块'),
    mergeDiscriminator: readPolicyValue('合并区分字段'),
    mergedFieldNames: readPolicyValue('合并统一字段').split('、').map((item) => item.trim()).filter((item) => item && item !== '不适用'),
    defaultSubmoduleOrder: readPolicyValue('默认顺序').split('、').map((item) => item.trim()).filter(Boolean),
    yAxisRecommendation: readPolicyValue('Y轴推荐'),
    leftYAxisCandidates: splitCandidateNames(readPolicyValue('左Y轴候选')),
    rightYAxisCandidates: splitCandidateNames(readPolicyValue('右Y轴候选')),
  };
}

async function validateCatalogBindingsAndRuntime(dsl, catalogDir) {
  let submoduleContract;
  let executionContract;
  try {
    submoduleContract = JSON.parse(await readFile(path.join(catalogDir, 'submodules.json'), 'utf8'));
  } catch {
    fail('catalog 缺少或无法解析 submodules.json');
  }
  try {
    executionContract = JSON.parse(await readFile(path.join(catalogDir, 'execution-contract.json'), 'utf8'));
  } catch {
    fail('catalog 缺少或无法解析 execution-contract.json');
  }
  const submodules = submoduleContract.submodules || [];
  const executableModules = executionContract.modules || {};
  const responses = {};
  const selectedMappings = [];
  const combinedModules = new Map();
  const yAxisRecommendations = [];
  for (const request of dsl.requests) {
    const moduleFile = path.join(catalogDir, 'modules', `${request.moduleId}.md`);
    let markdown;
    try {
      markdown = await readFile(moduleFile, 'utf8');
    } catch {
      fail(`catalog 中不存在 request.moduleId：${request.moduleId}`);
    }
    const catalogModule = parseCatalogModule(markdown, request.moduleId);
    const executableModule = executableModules[request.moduleId];
    if (!executableModule) {
      fail(`request ${request.id}.moduleId 不在 execution-contract.json 执行白名单中`);
    }
    if (catalogModule.sqlId !== executableModule.sqlCode) {
      fail(`catalog 模块 ${request.moduleId} 的 sqlId 与 execution-contract.json 不一致`);
    }
    if (executableModule.sqlCode !== request.sqlCode) {
      fail(`request ${request.id}.sqlCode 与 execution-contract.json 不一致`);
    }
    let requestMappings = catalogModule.fieldMappings;
    const siblings = submodules.filter((item) => item.moduleId === request.moduleId);
    const executableSubmoduleIds = executableModule.submoduleIds || [];
    const contractSubmoduleIds = siblings.map((item) => item.id).sort();
    if (JSON.stringify([...executableSubmoduleIds].sort()) !== JSON.stringify(contractSubmoduleIds)) {
      fail(`catalog 模块 ${request.moduleId} 的子模块契约与 execution-contract.json 不一致`);
    }
    if (!request.submoduleId && catalogModule.submoduleSelection === 'clarify-submodule') {
      fail(`request ${request.id} 必须选择 catalog 父模块 ${request.moduleId} 的具体子模块`);
    }
    if (request.submoduleId) {
      const selected = submodules.find((item) => item.id === request.submoduleId);
      if (!selected || selected.moduleId !== request.moduleId) {
        fail(`request ${request.id}.submoduleId 未绑定到 catalog 父模块 ${request.moduleId}`);
      }
      if (!executableSubmoduleIds.includes(request.submoduleId)) {
        fail(`request ${request.id}.submoduleId 不在 execution-contract.json 执行白名单中`);
      }
      const siblingRequests = dsl.requests.filter((item) => (
        item.moduleId === request.moduleId && item.submoduleId
      ));
      const requestedSubmoduleIds = siblingRequests.map((item) => item.submoduleId);
      const isCombinedRequest = siblingRequests.length > 1;
      if (isCombinedRequest) {
        if (catalogModule.allSubmodules !== 'combined-table') {
          fail(`catalog 模块 ${request.moduleId} 不允许全部子模块合并展示`);
        }
        if (dsl.view.type !== 'table') {
          fail(`catalog 模块 ${request.moduleId} 的全部子模块只允许 combined-table`);
        }
        if (JSON.stringify(requestedSubmoduleIds) !== JSON.stringify(catalogModule.defaultSubmoduleOrder)) {
          fail(`模块 ${request.moduleId} 的全部子模块 request 必须按 catalog 默认顺序完整生成`);
        }
        if (!catalogModule.mergeDiscriminator || catalogModule.mergeDiscriminator === '不适用') {
          fail(`catalog 模块 ${request.moduleId} 缺少合并区分字段`);
        }
        combinedModules.set(request.moduleId, {
          discriminator: catalogModule.mergeDiscriminator,
          mergedFieldNames: catalogModule.mergedFieldNames,
        });
      }
      const allowedSubmoduleIds = isCombinedRequest ? requestedSubmoduleIds : [request.submoduleId];
      const allowed = new Set(siblings
        .filter((item) => allowedSubmoduleIds.includes(item.id))
        .flatMap((item) => item.dataPaths));
      for (const dataPath of selected.dataPaths) {
        if (!sourceReferencesDataPath(dsl.transform.function, dataPath)) {
          fail(`transform.function 未读取子模块 ${request.submoduleId} 的数据集：${dataPath}`);
        }
      }
      for (const sibling of siblings) {
        for (const dataPath of sibling.dataPaths) {
          if (!allowed.has(dataPath) && sourceReferencesDataPath(dsl.transform.function, dataPath)) {
            fail(`transform.function 越界读取子模块 ${request.submoduleId} 之外的数据集：${dataPath}`);
          }
        }
      }
      const selectedFieldPaths = new Set(selected.fieldPaths || []);
      requestMappings = requestMappings.filter((mapping) => selectedFieldPaths.has(mapping.jsonPath));
      if (requestMappings.length !== selectedFieldPaths.size) {
        fail(`catalog 子模块 ${request.submoduleId} 的 fieldPaths 与模块字段映射不一致`);
      }
    }
    requestMappings = requestMappings.filter((mapping) => mapping.applicableViews.includes(dsl.view.type));
    if (!requestMappings.length) {
      fail(`catalog 模块 ${request.moduleId} 没有适用于 ${dsl.view.type} 的字段映射`);
    }
    selectedMappings.push(...requestMappings.map((mapping) => ({ ...mapping, requestId: request.id })));
    responses[request.id] = catalogModule.example;
    if (catalogModule.yAxisRecommendation === '双Y轴') {
      yAxisRecommendations.push({
        moduleId: request.moduleId,
        left: catalogModule.leftYAxisCandidates,
        right: catalogModule.rightYAxisCandidates,
      });
    }
  }

  for (const [moduleId, policy] of combinedModules) {
    const discriminator = policy.discriminator;
    if (!dsl.view.columns.some((column) => column.label === discriminator)) {
      fail(`模块 ${moduleId} 的 combined-table 缺少区分字段列：${discriminator}`);
    }
    selectedMappings.unshift({
      jsonPath: '$derived.submodule',
      rawField: '$derived',
      displayName: discriminator,
    });
    for (const displayName of policy.mergedFieldNames) {
      const byRawField = new Map();
      for (const mapping of selectedMappings.filter((item) => item.requestId)) {
        const values = byRawField.get(mapping.rawField) || [];
        values.push(mapping);
        byRawField.set(mapping.rawField, values);
      }
      const sourceCandidates = [...byRawField.values()].find((values) => (
        new Set(values.map((item) => item.requestId)).size === dsl.requests.length
        && new Set(values.map((item) => item.displayName)).size > 1
      )) || [];
      selectedMappings.push({
        jsonPath: '$derived.merged-field',
        rawField: '$derived',
        displayName,
        sourceCandidates,
      });
    }
  }

  const knownLeafNames = new Set();
  for (const example of Object.values(responses)) {
    for (const fieldPath of collectLeafPaths(example)) knownLeafNames.add(fieldPath.split('.').pop().replace(/\[\]$/, ''));
  }
  const allowedMappings = selectedMappings.flatMap((mapping) => (
    mapping.sourceCandidates?.length ? mapping.sourceCandidates : [mapping]
  ));
  const allowedRawFields = new Set(allowedMappings.map((mapping) => mapping.rawField));
  const allowedPathProperties = new Set(allowedMappings.flatMap((mapping) => propertyNamesInJsonPath(mapping.jsonPath)));
  const propertyNames = referencedPropertyNames(dsl.transform.function);
  for (const propertyName of propertyNames) {
    if (knownLeafNames.has(propertyName)
      && !allowedRawFields.has(propertyName)
      && !allowedPathProperties.has(propertyName)) {
      fail(`transform.function 静态引用了未授权字段：${propertyName}`);
    }
  }
  for (const request of dsl.requests) {
    const requestRawFields = selectedMappings
      .filter((mapping) => mapping.requestId === request.id)
      .map((mapping) => mapping.rawField);
    if (!requestRawFields.some((rawField) => propertyNames.has(rawField))) {
      fail(`transform.function 未读取 request ${request.id} 的授权叶子字段`);
    }
  }

  if (dsl.view.type === 'table') {
    const mappingIndexes = new Map();
    selectedMappings.forEach((mapping, index) => {
      if (!mappingIndexes.has(mapping.displayName)) mappingIndexes.set(mapping.displayName, index);
    });
    let previousIndex = -1;
    for (const column of dsl.view.columns) {
      if (!mappingIndexes.has(column.label)) {
        fail(`table column.label 不在模块 MD 字段映射中：${column.label}`);
      }
      if (dsl.requests.length === 1) {
        const currentIndex = mappingIndexes.get(column.label);
        if (currentIndex < previousIndex) {
          fail('单模块 table columns 必须遵循模块 MD 字段映射顺序');
        }
        previousIndex = currentIndex;
      }
      const formatCandidates = selectedMappings.filter((mapping) => mapping.displayName === column.label && mapping.rawField !== '$derived');
      if (formatCandidates.length) validateViewFormat(column, formatCandidates[0], `column ${column.field}`);
    }
  } else {
    for (const series of dsl.view.series) {
      const candidates = mappingsForSeriesName(series.name, selectedMappings, dsl.requests.length > 1);
      if (!candidates.length) {
        fail(`echarts series.name 不在模块 MD 字段映射中：${series.name}`);
      }
      validateViewFormat(series, candidates[0], `series ${series.name}`);
    }
  }

  if (dsl.view.type === 'echarts') {
    for (const recommendation of yAxisRecommendations) {
      const leftSeries = dsl.view.series.filter((series) => recommendation.left.includes(series.name));
      const rightSeries = dsl.view.series.filter((series) => recommendation.right.includes(series.name));
      if (!leftSeries.length || !rightSeries.length) continue;
      if (dsl.view.yAxis.length !== 2) {
        fail(`catalog 模块 ${recommendation.moduleId} 同时选择左右轴指标时必须使用双Y轴`);
      }
      if (leftSeries.some((series) => (series.yAxisIndex ?? 0) !== 0)) {
        fail(`catalog 模块 ${recommendation.moduleId} 的左Y轴候选必须使用 yAxisIndex 0`);
      }
      if (rightSeries.some((series) => series.yAxisIndex !== 1)) {
        fail(`catalog 模块 ${recommendation.moduleId} 的右Y轴候选必须使用 yAxisIndex 1`);
      }
    }
  }

  const viewBindings = [];
  if (dsl.view.type === 'table') {
    for (const column of dsl.view.columns) {
      const matched = selectedMappings.filter((mapping) => mapping.displayName === column.label);
      const candidates = matched.flatMap((mapping) => mapping.sourceCandidates?.length ? mapping.sourceCandidates : (mapping.requestId ? [mapping] : []));
      if (candidates.length) viewBindings.push({ field: column.field, label: column.label, candidates });
    }
  } else {
    for (const series of dsl.view.series) {
      const candidates = mappingsForSeriesName(series.name, selectedMappings, dsl.requests.length > 1);
      if (candidates.length) viewBindings.push({ field: series.type === 'pie' ? series.encode.value : series.encode.y, label: series.name, candidates });
    }
    const xField = dsl.view.series.find((series) => series.type !== 'pie')?.encode.x;
    if (xField && dsl.view.xAxis?.name) {
      const candidates = selectedMappings.filter((mapping) => mapping.displayName === dsl.view.xAxis.name && mapping.requestId);
      if (candidates.length) viewBindings.push({ field: xField, label: dsl.view.xAxis.name, candidates });
    }
  }
  const probeMap = new Map();
  let probeIndex = 0;
  for (const binding of viewBindings) {
    for (const mapping of binding.candidates) {
      const key = `${mapping.requestId}\u0000${mapping.jsonPath}`;
      if (!probeMap.has(key)) {
        probeMap.set(key, {
          id: `probe-${probeIndex}`,
          requestId: mapping.requestId,
          path: mapping.jsonPath,
          marker: 900000000 + probeIndex * 100003,
        });
        probeIndex += 1;
      }
    }
  }
  const runtime = runTransformIsolated(dsl.transform.function, responses, [...probeMap.values()]);
  const output = runtime.baseline;
  if (!Array.isArray(output)) {
    fail('transform.function 使用 catalog 示例数据时必须返回数组');
  }
  if (!output.length) fail('transform.function 使用 catalog 示例数据时不得返回空数组，无法验证字段血缘');
  const probeOutputs = new Map(runtime.probes.map((item) => [item.id, item.output]));
  for (const binding of viewBindings) {
    const candidateProbeIds = binding.candidates.map((mapping) => probeMap.get(`${mapping.requestId}\u0000${mapping.jsonPath}`)?.id).filter(Boolean);
    if (!candidateProbeIds.some((id) => outputFieldChanged(output, probeOutputs.get(id), binding.field))) {
      fail(`view 字段 ${binding.field} 未证明来源于对应 Catalog 字段：${binding.label}`);
    }
    const expectedValues = binding.candidates.flatMap((mapping) => {
      const rule = parseDisplayTransform(mapping.displayTransform);
      return valuesAtPath(responses[mapping.requestId], mapping.jsonPath).map((value) => (
        typeof value === 'number' && Number.isFinite(value) ? value * rule.multiplier : value
      ));
    });
    for (const row of output) {
      const value = row && row[binding.field];
      if (value === null || value === undefined) continue;
      if (!expectedValues.some((expected) => equivalentValue(value, expected))) {
        fail(`view 字段 ${binding.field} 的输出值不符合 Catalog 字段或展示转换：${binding.label}`);
      }
    }
  }
  for (const request of dsl.requests) {
    const requestProbeIds = [...probeMap.values()].filter((probe) => probe.requestId === request.id).map((probe) => probe.id);
    if (!requestProbeIds.some((id) => JSON.stringify(output) !== JSON.stringify(probeOutputs.get(id)))) {
      fail(`transform.function 输出未证明依赖 request ${request.id}`);
    }
  }
  const requiredFields = dsl.view.type === 'table'
    ? dsl.view.columns.map((column) => column.field)
    : dsl.view.dataset.dimensions;
  for (let index = 0; index < output.length; index += 1) {
    const row = output[index];
    if (!row || typeof row !== 'object' || Array.isArray(row)) {
      fail(`transform.function 输出第 ${index + 1} 行必须是对象`);
    }
    for (const field of requiredFields) {
      if (!Object.prototype.hasOwnProperty.call(row, field)) {
        fail(`transform.function 输出第 ${index + 1} 行缺少 view 字段：${field}`);
      }
    }
  }
}

export function validateDslResponse(response, context) {
  if (!Array.isArray(response)) {
    return validateDsl(response, context);
  }
  if (!response.length) fail('批量 update 不能为空');
  if (!context || context.updateAll !== true) {
    fail('用户未明确要求修改全部模块，不得返回多个 DSL');
  }
  if (!Array.isArray(context.currentDsls) || !context.currentDsls.length) {
    fail('批量 update 缺少前端回传的 currentDsls');
  }

  const currentById = new Map(
    context.currentDsls
      .filter((item) => item && item.id)
      .map((item) => [item.id, item]),
  );
  const returnedIds = new Set();

  for (const dsl of response) {
    if (!dsl || dsl.action !== 'update') {
      fail('批量结果中的每一项都必须是 update DSL');
    }
    if (returnedIds.has(dsl.id)) fail(`批量 update 的 id 重复：${dsl.id}`);
    returnedIds.add(dsl.id);
    const currentDsl = currentById.get(dsl.id);
    if (!currentDsl) {
      fail(`批量 update 的 id 不存在于前端 currentDsls：${dsl.id}`);
    }
    validateDsl(dsl, {
      currentId: dsl.id,
      currentDsl,
    });
  }

  return response;
}

async function main() {
  const file = process.argv[2];
  if (!file) fail('用法：node scripts/validate-dsl.mjs <dsl.json>');
  const skillDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const schemaFile = path.join(skillDir, 'references', 'dsl.schema.json');
  const schemaValidator = path.join(skillDir, 'scripts', 'validate-schema.py');
  const schemaResult = spawnSync(
    process.env.VM_REPORT_PYTHON || 'python3',
    [schemaValidator, schemaFile, file],
    { encoding: 'utf8' },
  );
  if (schemaResult.status !== 0) {
    fail((schemaResult.stderr || schemaResult.stdout || 'DSL Schema 校验失败').trim());
  }
  const contextFile = process.argv[3];
  const context = contextFile
    ? JSON.parse(await readFile(contextFile, 'utf8'))
    : undefined;
  const response = JSON.parse(await readFile(file, 'utf8'));
  validateDslResponse(response, context);
  const profileDir = path.resolve(skillDir, '..', '..', '..');
  const catalogDir = process.env.VM_REPORT_CATALOG_DIR
    ? path.resolve(process.env.VM_REPORT_CATALOG_DIR)
    : path.join(profileDir, 'workspace', 'catalog');
  const dsls = Array.isArray(response) ? response : [response];
  for (const dsl of dsls) {
    await validateCatalogBindingsAndRuntime(dsl, catalogDir);
  }
  console.log('DSL 校验通过');
}

if (process.argv[1] && process.argv[1].endsWith('validate-dsl.mjs')) {
  main().catch((error) => {
    console.error(error.message);
    process.exitCode = 1;
  });
}
