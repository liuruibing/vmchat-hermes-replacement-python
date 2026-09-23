# Hermes 返回数据字段详解

> ⚠️ **本文档面向初学者**。如果你对 vmChat 前端代码不熟，这篇会带你逐层看懂 Hermes 返回的 JSON 里每个字段是什么意思、被谁消费、最终变成什么。

---

## 一、整体骨架

```json
{
  "intent": "report",
  "renderType": "report",
  "operations": [ ... ]
}
```

这 3 个字段是 **Hermes 协议的最外层**，由 `parseVmHermesRenderPayload()` 解析（`vm-chat-helpers.js`）。

### intent / renderType

| 字段 | 值 | 含义 |
|------|----|------|
| `intent` | `"report"` / `"clarify"` / `"chat"` | Hermes 输出的**意图类型**。`report` = 要生成/修改报表 |
| `renderType` | 同上 | `parseVmHermesRenderPayload` 先读 `renderType`，没有就 fallback 到 `intent` |

**三种意图的区别：**

| intent | 含义 | 前端行为 |
|--------|------|----------|
| `report` | 生成或修改报表块 | 遍历 `operations` 数组，逐个执行增删改 |
| `clarify` | 参数不够，需要反问用户 | 展示 `clarify.questions` 列表 |
| `chat` | 普通对话/拒绝合并 | 显示 `message` 文本，不操作画布 |

---

## 二、operations 数组

```json
"operations": [
  {
    "action": "appendBlock",
    "block": { ... }
  }
]
```

由 `validateOperation()` 处理（`vm-chat-helpers.js` 第 310 行）。

### action

| 取值 | 含义 | 效果 |
|------|------|------|
| `appendBlock` | **添加**一个新的报表块 | 在画布末尾插入一个块 |
| `replaceBlock` | **替换**已有的块 | 找到 `targetBlockId` 对应的块，整个替换 |
| `removeBlock` | **删除**块 | 从画布移除 |
| `moveBlock` | **移动**块顺序 | 改变 `toIndex` 位置 |
| `renameBlock` | **重命名**块标题 | 只改 `title`，不改数据 |

第 4 次请求用的是 `appendBlock`——因为对话上下文里还没有任何块，所以要**新建一个**。

### block 结构

```json
"block": {
  "blockId": "profitStock100",
  "title": "盈利个股列表",
  "dsl": { ... }
}
```

这是 **block 的蓝图**。前端收到后会传给 `createVmReportBlock()` → `createVmDslReportBlock()`，生成一个完整的前端 block 对象。

| 字段 | 含义 | 谁生成 |
|------|------|--------|
| `blockId` | 这个块的唯一 ID | Hermes 生成，前端用来做 key 和定位 |
| `title` | 展示在块顶部的标题 | Hermes 生成 |
| `dsl` | **核心数据**：告诉前端怎么查数据、怎么转、怎么画 | Hermes 生成，前端校验执行 |

---

## 三、dsl —— 核心

`dsl` 是**整个协议的灵魂**，前端所有工作都围绕它展开。由 `validateVmReportDsl()` 校验（`vm-report-dsl-validator.js`）。

```json
"dsl": {
  "action": "query",
  "id": "profitStock100",
  "params": { ... },
  "requests": [ ... ],
  "transform": { ... },
  "view": { ... }
}
```

### 3.1 dsl.action

| 字段 | 值 | 含义 |
|------|----|------|
| `action` | **应写** `"create"` 或 `"update"` | 表示"新建一个 DSL"还是"修改已有的 DSL" |

> ⚠️ **注意**：第 4 次请求 Hermes 返回了 `"query"`，但按 `vm-report-dsl-validator.js` 第 208 行的规则，**只允许** `"create"` 或 `"update"`。之所以第 4 次能过，是因为当时 validator 还比较宽松；后续代码收紧后就报错了。

- `"create"`：全新的 DSL，前端会生成一个新的 UUID 作为 `id`
- `"update"`：修改已有的 DSL，`id` 必须等于前端传回去的 `currentId`

### 3.2 dsl.id

DSL 的唯一标识。前端 `createVmDslReportBlock()` 会这样处理：

```js
blockId = source.blockId || dsl.id || 'vm-block-' + Date.now()
```

如果 Hermes 给了 `blockId` 就用它，没有就用 `dsl.id`，再没有就自动生成一个。

### 3.3 dsl.params

```json
"params": {
  "fundCode": "SM0513",
  "beginDate": "20220101",
  "endDate": "20220131",
  "dataFreqOpen": "true",
  "benchmarks": "1",
  "benchmarkA": "沪深300",
  "dataFreq": "daily"
}
```

**这是所有接口请求的公共参数**。前端 `buildRequestPlan()`（`vm-report-dsl-runtime.js` 第 106 行）会把 `dsl.params` **合并到每个请求里**：

```js
params: Object.assign({}, dsl.params, request自身的参数)
```

| 参数名 | 含义 | 示例 |
|--------|------|------|
| `fundCode` | 产品代码 | `"SM0513"` |
| `beginDate` | 查询开始日期 | `"20220101"`（格式 YYYYMMDD） |
| `endDate` | 查询结束日期 | `"20220131"` |
| `dataFreqOpen` | 是否开启频率控制 | `"true"`（固定值） |
| `benchmarks` | 基准模式：`"0"`=无, `"1"`=单, `"2"`=复合 | `"1"` |
| `benchmarkA` | 第一个基准代码或名称 | `"沪深300"` |
| `dataFreq` | 数据频率 | `"daily"` / `"weekly"` / `"monthly"` |

### 3.4 dsl.requests

```json
"requests": [
  {
    "id": "profitStock100_query",
    "type": "sql",
    "sqlCode": "80b30c87-13d2-4137-95c3-c5ecfd0dd2e7",
    "params": {
      "fundCode": "SM0513",
      "beginDate": "20220101",
      "endDate": "20220131"
    }
  }
]
```

**告诉前端要调哪个后端接口、传什么参数。**

前端 `buildRequestPlan()` 会把 `requests` 转换为标准查询计划：

```js
// 第 106-115 行
function buildRequestPlan(dsl) {
  return {
    requests: dsl.requests.map(request => ({
      requestId: request.id,       // 请求的唯一标识
      moduleKey: request.moduleId, // 模块标识
      mode: 'sql',                 // 固定用 SQL 接口
      sqlCode: request.sqlCode,    // 后端 SQL 的 UUID
      params: Object.assign({}, dsl.params || {})  // 合并公共参数
    }))
  }
}
```

| 字段 | 含义 | 值来源 |
|------|------|--------|
| `id` | 该请求在当前 DSL 中的唯一 ID，前端会用它来匹配响应数据 | Hermes 生成 |
| `type` | 请求类型，始终 `"sql"` | 固定 |
| `sqlCode` | **后端 SQL 语句的 UUID**，前端调用 `/rest/report/getSqlDataBySqlCode.do` 时用 | 从 catalog 模块的 markdown 中读取 |
| `params` | 该请求的私有参数（会与 `dsl.params` 合并） | Hermes 生成 |

> **为什么 `params` 里重复写了 `fundCode` 等参数？** 因为最终发请求时，`dsl.params` 和 `request.params` 会合并。`request.params` 里如果有重复字段，会覆盖 `dsl.params` 的同名字段。

### 3.5 dsl.transform

```json
"transform": {
  "type": "passthrough"
}
```

**告诉前端怎么把后端的原始数据"转换"成前端能用的数组。**

有两种形式：

#### 形式 A：passthrough（透传）

```json
{ "type": "passthrough" }
```

含义：**不需要转换**，直接把后端返回的 `body` 数组作为最终数据。

前端 `executeVmReportTransformFunction()` 收到 `passthrough` 时，会自动生成一个简单的透传函数：

```js
// 实际上会走 buildTransformFunctionFromSteps 的兜底
// 取出 body 数组直接返回
```

#### 形式 B：自定义转换函数

```json
"transform": {
  "language": "javascript",
  "function": "function transform(responses) {\n  var response = responses && responses[\"cashPositionTiming_query\"];\n  var rows = response && Array.isArray(response.body) ? response.body : [];\n  return rows.map(function (row) {\n    return {\n      \"tradeDate\": row[\"TDATE\"],\n      \"cashRatio\": row[\"F_CASH_RATIO\"]\n    };\n  });\n}"
}
```

含义：**用一段 JS 函数来处理原始数据**。

前端 `executeVmReportTransformFunction()`（`vm-report-dsl-runtime.js` 第 141 行）：

1. **安全检查**：禁止使用 `window`、`document`、`fetch`、`eval` 等危险对象
2. **编译函数**：用 `new Function()` 把字符串编译成可执行函数
3. **冻结数据**：把后端返回的数据用 `deepFreeze` 冻结，防止函数修改
4. **执行**：传入 `responses`（一个对象，key 是 `request.id`，value 是后端返回的数据）
5. **校验结果**：必须返回一个数组

| 字段 | 含义 |
|------|------|
| `language` | 固定 `"javascript"` |
| `function` | 一个完整的 JS 函数源代码。接收 `responses` 参数，返回数组 |

### 3.6 dsl.view

```json
"view": {
  "type": "table",
  "fields": [
    { "field": "securityCode", "label": "证券代码", "format": "text" },
    { "field": "securityName", "label": "证券名称", "format": "text" },
    { "field": "industryName", "label": "行业", "format": "text" },
    { "field": "income", "label": "本期盈利", "format": "decimal(2)", "unit": "元" },
    { "field": "profitRatio", "label": "盈利占比", "format": "percentage(4)", "unit": "%" },
    { "field": "positionRatio", "label": "期间仓位", "format": "percentage(4)", "unit": "%" }
  ]
}
```

**告诉前端最终要渲染成什么样子。**

`buildRenderSpecFromDsl()`（`vm-report-dsl-runtime.js` 第 84 行）根据 `view.type` 决定渲染方式。

| view.type | 含义 | 前端渲染组件 |
|-----------|------|-------------|
| `"table"` | 表格 | `<vxe-table>`：用 `columns` 和 `rows` |
| `"echarts"` | 图表 | `<my-chart>`（ECharts）：用 `option` |

#### view 的通用字段

| 字段 | 出现在 | 含义 |
|------|--------|------|
| `type` | 所有 | `"table"` 或 `"echarts"` |
| `title` | 可选 | 块标题，如果 `block.title` 没给会用这个 |
| `xField` | echarts | 横轴字段名，如 `"tradeDate"` |

#### table 特有的 fields

```json
"fields": [
  { "field": "securityCode", "label": "证券代码", "format": "text" }
]
```

`buildTableColumns()`（`vm-report-dsl-runtime.js` 第 45 行）把 `fields` 转成 `columns`：

```js
{
  field: "securityCode",    // 数据行里的字段名
  title: "证券代码",         // 表头显示的文字
  label: "证券代码",         // 同上
  unit: "元",               // 单位
  format: {                 // 格式化规则（字符串→对象）
    type: "decimal",
    digits: 2
  },
  align: "left"             // 对齐方式
}
```

| fields 子字段 | 含义 | 示例 |
|---------------|------|------|
| `field` | **关键**：对应 transform 返回的数组对象的 key 名 | `"securityCode"` |
| `label` | 表格表头显示的中文名 | `"证券代码"` |
| `format` | 格式化方式：`text` / `decimal(N)` / `percentage(N)` | `"decimal(2)"` |
| `unit` | 单位 | `"元"` / `"%"` |

前端 `<vxe-table>` 模板（`index.vue` 第 144-151 行）：
```vue
<vxe-table :data="block.renderSpec.rows">
  <vxe-table-column
    v-for="col in block.renderSpec.columns"
    :field="col.field"
    :title="col.title"
  />
</vxe-table>
```

#### echarts 特有的 fields + series

```json
"view": {
  "type": "echarts",
  "xField": "tradeDate",
  "fields": [
    { "field": "tradeDate", "label": "日期", "format": "date" },
    { "field": "cashRatio", "label": "现金类仓位", "format": "percentage(4)", "unit": "%" }
  ],
  "series": [
    { "field": "cashRatio", "name": "现金类仓位", "chartType": "line", "yAxisIndex": 0 }
  ]
}
```

`buildChartOption()`（`vm-report-dsl-runtime.js` 第 56 行）把 `view` 转成 ECharts `option`：

```js
{
  title: { text: "标题" },
  tooltip: { trigger: "axis" },
  legend: { show: true },
  grid: { left: 48, right: ..., top: 48, bottom: 36 },
  dataset: { source: [...转换后的行数据...] },
  xAxis: { type: "category", name: "tradeDate" },
  yAxis: [
    { type: "value", position: "left" },
    { type: "value", position: "right" }  // 如果有双轴
  ],
  series: [
    {
      name: "现金类仓位",
      type: "line",
      yAxisIndex: 0,
      encode: { x: "tradeDate", y: "cashRatio" }
    }
  ]
}
```

---

## 四、前端接到这个 JSON 后，完整的 7 步处理流程

```
Hermes 返回 JSON
     ↓
① parseVmHermesRenderPayload()        ← 解析外层 intent/renderType/operations
     ↓
② validateOperation()                 ← 校验 action 是否合法
     ↓
③ createVmReportBlock()               ← 把 block 转换成前端对象
   └─ createVmDslReportBlock()
      ├─ validateVmReportDsl()         ← 校验 dsl 结构
      ├─ deriveModuleKey()             ← 从 requests 提取 moduleKey
      ├─ buildRenderSpecFromDsl()      ← 从 view 生成空的 renderSpec
      └─ deriveQueryContext()          ← 从 params 提取 queryContext
     ↓
④ index.vue 把 block 加入 reportBlocks 数组    ← Vue 响应式，立刻显示"加载中..."骨架
     ↓
⑤ hydrateVmBlock()                    ← 开始异步加载数据
   └─ hydrateVmDslReportBlock()
      ├─ buildRequestPlan()            ← dsl.requests → queryPlan
      ├─ executeVmQueryPlan()          ← 调用后端 API
      │   ├─ 请求去重（相同 sqlCode+params 只调一次）
      │   └─ Promise.all 并发请求
      ├─ executeVmReportTransformFunction()  ← 执行 transform 函数
      │   ├─ 安全检查（禁用危险 API）
      │   ├─ Function() 编译
      │   └─ 执行得到最终 rows 数组
      └─ 填充 renderSpec
          ├─ table：columns + rows
          └─ echarts：option.dataset.source
     ↓
⑥ Vue 响应式更新                     ← 数据进入模板，图表/表格刷新
     ↓
⑦ 用户看到最终渲染结果
```

---

---

## 附录：完整 JSON 逐行注释版

> 以下是对第 4 次成功请求的**完整 Hermes 返回 JSON**，每一行都加了注释，说明它是什么、去哪里、做什么。

```jsonc
{                                                                    // ════════════════════════════════════
  "intent": "report",                                                // ← 告诉前端：这是"生成报表"的意图
                                                                     //   3 种可能：report / clarify / chat
  "renderType": "report",                                            // ← 同上，前端优先读这个字段
                                                                     //   缺省时 fallback 到 intent
  "operations": [                                                    // ← operations 数组，前端逐个执行
    {                                                                // ── 第一个操作 ─────────────────
      "action": "appendBlock",                                       // ← 操作类型：追加一个新块
                                                                     //   可选：appendBlock / replaceBlock
                                                                     //         removeBlock / moveBlock / renameBlock
      "block": {                                                     // ← 新块的蓝图，传给 createVmReportBlock()
        "blockId": "profitStock100",                                 // ← 块的唯一 ID，Vue 用做 :key
                                                                     //   前端会 fallback：blockId → dsl.id → 自动生成
        "title": "盈利个股列表",                                      // ← 块标题，展示在块顶部的蓝色标题栏
        "dsl": {                                                     // ← ⭐ 核心数据契约：告诉前端怎么查、怎么转、怎么画
          "action": "query",                                         // ← DSL 的动作类型
                                                                     //   ⚠️ 按最新 validator，只允许 "create" 或 "update"
                                                                     //   "query" 会被拒绝，这条请求成功是因为当时较宽松
          "id": "profitStock100",                                    // ← DSL 的唯一 ID
                                                                     //   create 时前端会替换为自动生成的 UUID
                                                                     //   update 时必须等于前端传回的 currentId
          "params": {                                                // ← ⭐ 公共请求参数：合并到每个接口请求里
            "fundCode": "SM0513",                                    //    产品代码
            "beginDate": "20220101",                                 //    查询开始日期（YYYYMMDD）
            "endDate": "20220131",                                   //    查询结束日期（YYYYMMDD）
            "dataFreqOpen": "true",                                  //    频率开关，固定 "true"
            "benchmarks": "1",                                       //    基准模式："0"=无 / "1"=单 / "2"=复合
            "benchmarkA": "沪深300",                                 //    基准代码或名称（单基准时必填）
            "dataFreq": "daily"                                      //    数据频率：daily / weekly / monthly
          },                                                         //
          "requests": [                                              // ← ⭐ 接口请求列表：要调哪些后端接口
            {                                                        // ── 第一个请求 ──────────────
              "id": "profitStock100_query",                          //   ← 这个请求在当前 DSL 内的唯一 ID
                                                                     //     前端用它来匹配后端返回的数据
              "type": "sql",                                         //   ← 请求类型，固定 "sql"
              "sqlCode": "80b30c87-13d2-4137-95c3-c5ecfd0dd2e7",     //   ← ⭐ 后端 SQL 的 UUID
                                                                     //     前端调 /rest/report/getSqlDataBySqlCode.do
                                                                     //     时把这个当 sqlCode 参数传
              "params": {                                            //   ← 该请求的私有参数（与 dsl.params 合并）
                "fundCode": "SM0513",                                //
                "beginDate": "20220101",                             //
                "endDate": "20220131"                                //     最终实际请求参数 =
              }                                                      //     Object.assign({}, dsl.params, request.params)
            }                                                        //
          ],                                                         //
          "transform": {                                             // ← ⭐ 数据转换指令：原始数据 → 前端数组
            "type": "passthrough"                                    //   "passthrough" = 透传，不需转换
                                                                     //   直接把 body 数组作为最终数据
                                                                     //
                                                                     //   另一种形式（自定义函数）：
                                                                     //   {
                                                                     //     "language": "javascript",
                                                                     //     "function": "function transform(responses){
                                                                     //       var r = responses['xxx'];
                                                                     //       return r.body.map(...);
                                                                     //     }"
                                                                     //   }
          },                                                         //
          "view": {                                                  // ← ⭐ 渲染描述：最终长什么样
            "type": "table",                                         //   "table" = 表格
                                                                     //   另一种："echarts" = 图表
            "fields": [                                              // ← 列定义列表
              {                                                      // ── 第 1 列 ──────────────
                "field": "securityCode",                             //     数据行里的字段名（对应 transform 输出的 key）
                "label": "证券代码",                                  //     表头显示的中文名
                "format": "text"                                     //     格式化方式：text / decimal(N) / percentage(N)
              },                                                     //
              {                                                      // ── 第 2 列 ──────────────
                "field": "securityName",                             //
                "label": "证券名称",                                  //
                "format": "text"                                     //
              },                                                     //
              {                                                      // ── 第 3 列 ──────────────
                "field": "industryName",                             //
                "label": "行业",                                      //
                "format": "text"                                     //
              },                                                     //
              {                                                      // ── 第 4 列 ──────────────
                "field": "income",                                   //
                "label": "本期盈利",                                  //
                "format": "decimal(2)",                              //     保留 2 位小数
                "unit": "元"                                         //     单位，表头上显示
              },                                                     //
              {                                                      // ── 第 5 列 ──────────────
                "field": "profitRatio",                              //
                "label": "盈利占比",                                  //
                "format": "percentage(4)",                           //     百分比，保留 4 位小数
                "unit": "%"                                          //
              },                                                     //
              {                                                      // ── 第 6 列 ──────────────
                "field": "positionRatio",                            //
                "label": "期间仓位",                                  //
                "format": "percentage(4)",                           //
                "unit": "%"                                          //
              }                                                      //
            ]                                                        //
          }                                                          //
        }                                                            //
      }                                                              //
    }                                                                //
  ]                                                                  //
}                                                                    
```

### 如果 view.type 是 echarts（对比参考）

第 5 次请求返回了 echarts 类型，`view` 部分会长这样：

```jsonc
"view": {
  "type": "echarts",                                                 // ← 渲染类型：图表
  "title": "现金类持仓时序",                                          // ← 图表标题
  "xField": "tradeDate",                                             // ← 横轴字段名
  "fields": [                                                        // ← 字段定义（用于自动生成 series）
    { "field": "tradeDate", "label": "日期", "format": "date" },
    { "field": "cashRatio", "label": "现金类仓位", "format": "percentage(4)", "unit": "%" },
    { "field": "cashIndexValue", "label": "现金类利率", "format": "raw" },
    { "field": "navValue", "label": "累计单位净值", "format": "raw" }
  ],
  "series": [                                                        // ← ⭐ ECharts series 定义
    {                                                                //    如果 fields 不够用，可以显式写 series
      "field": "cashRatio",                                          //    数据字段
      "name": "现金类仓位",                                           //    图例名
      "chartType": "line",                                           //    图表类型：line / bar / scatter
      "yAxisIndex": 0                                                //    左轴=0 / 右轴=1
    },
    {
      "field": "cashIndexValue",
      "name": "现金类利率",
      "chartType": "line",
      "yAxisIndex": 1                                                //    用右轴（双轴场景）
    }
  ]
}
```

---

## 六、一句话总结

这个 JSON 的本质是 Hermes 在说：

> **"用户要看『SM0513 的盈利个股列表』。我查了 catalog，发现模块是 profitStock100，sqlCode 是 80b30c87...。参数齐全：产品 SM0513、时间 2022.1.1~1.31、单基准沪深300、日频。不需要额外转换（passthrough），直接展示成表格，列是证券代码、名称、行业、盈利金额、占比、仓位。"**

前端拿到后："好的，我去调接口，数据回来填到表格里。"
