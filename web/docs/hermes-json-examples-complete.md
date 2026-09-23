# vmChat Hermes 返回 JSON 完整示例（逐行注释版）

> 本文档包含 **ECharts 图表（多模块合并）** 和 **表格（单模块）** 两套完整示例，每行都标注了字段含义和前端消费链路。

---

## 一、ECharts 图表 — 多模块合并

### Hermes 返回 JSON

```jsonc
{                                                                    // ════════════════════════════════════
  "intent": "report",                                                // ← 前端 parseVmHermesRenderPayload 读
  "renderType": "report",                                            //    intent/renderType 决定渲染类型
  "operations": [                                                    // ← report 类型必须包含 operations 数组
    {                                                                // ── 第一个操作 ─────────────────
      "op": "appendBlock",                                           // ← 操作类型：追加新块
                                                                     //   validateOperation 读 action||type||op
                                                                     //   最终被归一化为 action: "appendBlock"
      "block": {                                                     // ← 传给 createVmReportBlock
        "blockId": "a7c3e1f9-2b4d-6e8a-9c0f-1d2e3a4b5c6d",         // ← 块唯一标识，Vue 用做 :key
        "title": "股票净敞口与现金类仓位",                            // ← 块标题，展示在块顶部的标题栏
        "dsl": {                                                     // ← ⭐ DSL 核心契约
          "action": "create",                                        // ← 只允许 create 或 update
          "id": "a7c3e1f9-2b4d-6e8a-9c0f-1d2e3a4b5c6d",            // ← 必须是有效 UUID
          "params": {                                                // ← ⭐ 公共请求参数，合并到每个 request
            "fundCode": "SM0513",                                    //    产品代码
            "beginDate": "20220101",                                 //    开始日期（YYYYMMDD，不能有横杠）
            "endDate": "20220131",                                   //    结束日期
            "dataFreqOpen": "true",                                  //    频率开关，固定 "true"
            "benchmarks": "1",                                       //    基准模式："0"无 / "1"单 / "2"复合
            "benchmarkA": "沪深300",                                 //    单基准时必填
            "dataFreq": "日频"                                       //    数据频率
          },                                                         //
          "requests": [                                              // ← ⭐ 接口请求列表
            {                                                        // ── 请求 1：股票净敞口数据 ────
              "id": "stockExposure",                                 //   ← 请求标识，transform 用此 id 取数
              "moduleId": "stockExposureTiming",                     //   ← 模块标识，来自 catalog
              "sqlCode": "712b930b-87a5-4cba-8da0-3671d4c8dc54"     //   ← 后端 SQL UUID
            },                                                       //
            {                                                        // ── 请求 2：现金类仓位数据 ────
              "id": "cashPosition",                                  //
              "moduleId": "cashPositionTiming",                      //
              "sqlCode": "b9f4277e-2793-4a0d-b9ed-e665e4bbd717"     //
            }                                                        //
          ],                                                         //
          "transform": {                                             // ← ⭐ 数据转换函数
            "language": "javascript",                                //    固定 "javascript"
            "function": "function transform(responses) {             //    ⭐ 前端在浏览器内存中执行
  var stockRows = (responses.stockExposure                           //      ← 取 request.id="stockExposure" 的 body
    && Array.isArray(responses.stockExposure.body))
    ? responses.stockExposure.body : [];
  var cashRows = (responses.cashPosition                            //      ← 取 request.id="cashPosition" 的 body
    && Array.isArray(responses.cashPosition.body))
    ? responses.cashPosition.body : [];
  var dateMap = {};
  stockRows.forEach(function(row) {
    dateMap[row.TDATE] = {                                          //      ← 以 TDATE 为 key 建立索引
      tradeDate: row.TDATE,
      stockExposure: row.F_STOCK_EXP                                //      ← 原始字段映射为标准字段
    };
  });
  cashRows.forEach(function(row) {
    if (!dateMap[row.TDATE]) {
      dateMap[row.TDATE] = { tradeDate: row.TDATE };
    }
    dateMap[row.TDATE].cashRatio = row.F_CASH_RATIO;               //      ← 第二个模块的字段加入同一行
  });
  return Object.keys(dateMap).sort().map(function(k) {              //      ← 按日期排序输出合并数组
    return dateMap[k];
  });
}"                                                                  //    ⚠️ 禁止 ?.  ??  toFixed  window fetch eval
          },                                                        //
          "view": {                                                 // ← ⭐ 渲染描述：ECharts 图表
            "type": "echarts",                                      //   "echarts" 或 "table"
            "title": "股票净敞口与现金类仓位",                       //   图表标题
            "xField": "tradeDate",                                  //   ← 横轴字段（ECharts encode.x）
            "series": [                                             //   ← ECharts series 定义列表
              {                                                     // ── 第 1 条线 ──────────────
                "field": "stockExposure",                           //     数据字段（transform 输出的 key）
                "label": "股票净敞口",                               //     图例显示名
                "yAxisIndex": 0,                                    //     左轴 0 / 右轴 1
                "format": "percentage(2)",                          //     格式化方式（透传给 view）
                "unit": "%"                                         //     单位
              },                                                    //
              {                                                     // ── 第 2 条线 ──────────────
                "field": "cashRatio",                               //
                "label": "现金类仓位",                               //
                "yAxisIndex": 1,                                    //     用右轴（双轴场景）
                "format": "percentage(4)",                          //
                "unit": "%"                                         //
              }                                                     //
            ]                                                       //
          }                                                         //
        }                                                           //
      }                                                             //
    }                                                               //
  ]                                                                 //
}                                                                    
```

### 水合后前端 renderSpec

```jsonc
{                                                                    // ════════════════════════════════════
  "renderSpec": {                                                   // ← buildRenderSpecFromDsl 生成空壳
    "renderer": "echarts",                                          //    hydrate 后填充数据
    "option": {                                                     // ← ⭐ Vue 模板直接绑定
      "title": { "text": "股票净敞口与现金类仓位" },                 //    <my-chart :options="block.renderSpec.option" />
      "tooltip": { "trigger": "axis" },                             //    ECharts 配置模板
      "legend": { "show": true },                                   //    由 buildChartOption 生成
      "grid": { "left": 48, "right": 48, "top": 48, "bottom": 36 },//
      "dataset": {                                                  // ← ⭐ 图表数据源
        "source": [                                                 //    transform 函数输出直接填入
          { "tradeDate": "20220104", "stockExposure": 1.26, "cashRatio": 0.0825 },  // ← 合并后的行
          { "tradeDate": "20220105", "stockExposure": 1.25, "cashRatio": 0.0949 },  //    ECharts encode
          { "tradeDate": "20220106", "stockExposure": 1.24, "cashRatio": 0.0897 }   //    绑 x(日期) y(数值)
        ]                                                           //
      },                                                            //
      "xAxis": { "type": "category", "name": "tradeDate" },         //    横轴类型
      "yAxis": [                                                    //    双轴
        { "type": "value", "position": "left" },                    //    左轴：股票净敞口
        { "type": "value", "position": "right" }                    //    右轴：现金类仓位
      ],                                                            //
      "series": [                                                   //    ECharts 系列
        {                                                           // ── 第 1 条线 ──
          "name": "股票净敞口",                                      //     图例名
          "type": "line",                                           //     折线图
          "yAxisIndex": 0,                                          //     左轴
          "encode": { "x": "tradeDate", "y": "stockExposure" }      //     ⭐ 数据绑定
        },                                                          //
        {                                                           // ── 第 2 条线 ──
          "name": "现金类仓位",                                      //
          "type": "line",                                           //
          "yAxisIndex": 1,                                          //     右轴
          "encode": { "x": "tradeDate", "y": "cashRatio" }          //
        }                                                           //
      ]                                                             //
    }                                                               //
  }                                                                 //
}                                                                    
```

---

## 二、表格 — 单模块

### Hermes 返回 JSON

```jsonc
{                                                                    // ════════════════════════════════════
  "intent": "report",                                                // ← 意图：生成报表
  "renderType": "report",                                            // ← 渲染类型
  "message": "已生成 SM0513 在 2022-01-01 至 2022-01-31 的盈利个股列表。", // ← 展示给用户的消息
  "operations": [                                                    // ← 画布操作列表
    {                                                                // ── 第一个操作 ─────────────────
      "action": "appendBlock",                                       // ← 追加新块
      "block": {                                                     //
        "blockId": "0629f0a7-5570-4719-b54a-6637c67de32e",           // ← 块 ID
        "title": "盈利个股列表",                                      // ← 块标题
        "dsl": {                                                     //
          "action": "create",                                        //
          "id": "0629f0a7-5570-4719-b54a-6637c67de32e",              //
          "params": {                                                //
            "fundCode": "SM0513",                                    //
            "beginDate": "20220101",                                 //
            "endDate": "20220131",                                   //
            "dataFreqOpen": "true",                                  //
            "benchmarks": "1",                                       //
            "benchmarkA": "沪深300",                                 //
            "dataFreq": "日频"                                       //
          },                                                         //
          "requests": [                                              //
            {                                                        // ── 仅 1 个请求 ──────────
              "id": "profit",                                        //
              "moduleId": "profitStock100",                          //
              "sqlCode": "80b30c87-13d2-4137-95c3-c5ecfd0dd2e7"     //
            }                                                        //
          ],                                                         //
          "transform": {                                             // ← ⭐ 单模块 transform
            "language": "javascript",                                //    不需要 join，直接映射字段
            "function": "function transform(responses) {             //
  var response = responses && responses.profit;                      //    取 request.id="profit" 的数据
  var rows = response && Array.isArray(response.body)
    ? response.body : [];
  return rows.map(function (row) {
    return {
      securityCode: row.VC_SYMBOL,                                  //    原始字段 → 标准字段
      securityName: row.VC_NAME,                                    //
      industryName: row.VC_INDUSTRY_NAME,                           //
      income: row.F_INCOME,                                         //
      profitRatio: row.F_YLZB,                                      //
      positionRatio: row.F_CWZB                                     //
    };
  });
}"                                                                  //
          },                                                        //
          "view": {                                                 // ← ⭐ 表格 view
            "type": "table",                                        //    "table" 类型
            "title": "盈利个股列表",                                 //
            "columns": [                                            // ← ⭐ 列定义列表
              {                                                     // ── 第 1 列 ──────────────
                "field": "securityCode",                            //     数据行字段名（对应 transform 输出 key）
                "label": "证券代码",                                 //     表头显示名
                "format": { "type": "text", "nullValue": "-" }      //     格式化对象（预解析格式）
              },                                                    //
              {                                                     // ── 第 2 列 ──────────────
                "field": "securityName",                            //
                "label": "证券名称",                                 //
                "format": { "type": "text", "nullValue": "-" }      //
              },                                                    //
              {                                                     // ── 第 3 列 ──────────────
                "field": "industryName",                            //
                "label": "行业",                                     //
                "format": { "type": "text", "nullValue": "-" }      //
              },                                                    //
              {                                                     // ── 第 4 列 ──────────────
                "field": "income",                                  //
                "label": "本期盈利",                                 //
                "unit": "元",                                       //     单位
                "format": { "type": "decimal", "digits": 2 }        //     保留 2 位小数
              },                                                    //
              {                                                     // ── 第 5 列 ──────────────
                "field": "profitRatio",                             //
                "label": "盈利占比",                                 //
                "unit": "%",                                        //
                "format": {                                         //     百分比格式
                  "type": "percentage",                             //
                  "multiplier": 100,                                //     原始值 × 100
                  "digits": 4,                                      //     保留 4 位小数
                  "suffix": "%"                                     //     后缀
                }                                                   //
              },                                                    //
              {                                                     // ── 第 6 列 ──────────────
                "field": "positionRatio",                           //
                "label": "期间仓位",                                 //
                "unit": "%",                                        //
                "format": {                                         //
                  "type": "percentage",                             //
                  "multiplier": 100,                                //
                  "digits": 4,                                      //
                  "suffix": "%"                                     //
                }                                                   //
              }                                                     //
            ]                                                       //
          },                                                        //
          "pendingMappings": [                                      // ← 标记字段：中文名映射标记
            { "param": "benchmarkA", "value": "沪深300" },          //    Hermes 的 benchmarkA 值是中文
            { "param": "dataFreq", "value": "日频" }                //    dataFreq 也是中文
          ]                                                         //    前端后续需要映射为内部代码
        }                                                           //
      }                                                             //
    }                                                               //
  ]                                                                 //
}                                                                    
```

### 水合后前端 renderSpec

```jsonc
{                                                                    // ════════════════════════════════════
  "renderSpec": {                                                   //
    "renderer": "table",                                            //
    "columns": [                                                    // ← buildTableColumns 从 dsl.view 生成
      {                                                             // ── 第 1 列 ──
        "field": "securityCode",                                    //
        "title": "证券代码",                                         //    label 复制为 title
        "label": "证券代码",                                         //
        "format": { "type": "text", "nullValue": "-" },             //
        "align": "left"                                             //    buildTableColumns 默认 align
      },                                                            //
      {                                                             // ── 第 2 列 ──
        "field": "securityName",                                    //
        "title": "证券名称",                                         //
        "label": "证券名称",                                         //
        "format": { "type": "text", "nullValue": "-" },             //
        "align": "left"                                             //
      },                                                            //
      {                                                             // ── 第 3 列 ──
        "field": "industryName",                                    //
        "title": "行业",                                             //
        "label": "行业",                                             //
        "format": { "type": "text", "nullValue": "-" },             //
        "align": "left"                                             //
      },                                                            //
      {                                                             // ── 第 4 列 ──
        "field": "income",                                          //
        "title": "本期盈利",                                         //
        "label": "本期盈利",                                         //
        "unit": "元",                                               //
        "format": { "type": "decimal", "digits": 2 },               //
        "align": "left"                                             //
      },                                                            //
      {                                                             // ── 第 5 列 ──
        "field": "profitRatio",                                     //
        "title": "盈利占比",                                         //
        "label": "盈利占比",                                         //
        "unit": "%",                                                //
        "format": {                                                 //
          "type": "percentage",                                     //
          "multiplier": 100,                                        //
          "digits": 4,                                              //
          "suffix": "%"                                             //
        },                                                          //
        "align": "left"                                             //
      },                                                            //
      {                                                             // ── 第 6 列 ──
        "field": "positionRatio",                                   //
        "title": "期间仓位",                                         //
        "label": "期间仓位",                                         //
        "unit": "%",                                                //
        "format": {                                                 //
          "type": "percentage",                                     //
          "multiplier": 100,                                        //
          "digits": 4,                                              //
          "suffix": "%"                                             //
        },                                                          //
        "align": "left"                                             //
      }                                                             //
    ],                                                              //
    "rows": [                                                       // ← ⭐ transform 函数输出的 17 行数据
      {                                                             // ── 第 1 行 ──
        "securityCode": "603363",                                   //
        "securityName": "傲农生物",                                  //
        "industryName": "农林牧渔",                                 //
        "income": 3311782,                                          //
        "profitRatio": 0.39203,                                     //
        "positionRatio": 0.10485                                    //
      },                                                            //
      {                                                             // ── 第 2 行 ──
        "securityCode": "000876",                                   //
        "securityName": "新希望",                                   //
        "industryName": "-",                                        //
        "income": 1957000,                                          //
        "profitRatio": 0.23166,                                     //
        "positionRatio": 0.2085                                     //
      },                                                            //
      {                                                             // ── 第 3 行 ──
        "securityCode": "002567",                                   //
        "securityName": "唐人神",                                   //
        "industryName": "农林牧渔",                                 //
        "income": 1050194,                                          //
        "profitRatio": 0.12432,                                     //
        "positionRatio": 0.15958                                    //
      }                                                             //
    ]                                                               //
  }                                                                 //
}                                                                    
```

---

## 三、两套结构的关键差异

| 维度 | ECharts（多模块合并） | 表格（单模块） |
|------|---------------------|--------------|
| `view.type` | `"echarts"` | `"table"` |
| 关键字段 | `xField` + `series[]` | `columns[]` |
| `requests` 数量 | **2 个**（需要 join） | 1 个 |
| `transform` 职责 | 多数据源 **按 TDATE 做内存 join** | 单数据源 **字段映射** |
| `renderSpec` 结构 | `renderer: "echarts"` + `option` | `renderer: "table"` + `columns` + `rows` |
| 数据注入 | `option.dataset.source = rows`（ECharts source） | `rows = rows`（vxe-table data） |
| Vue 组件 | `<my-chart :options>` | `<vxe-table :data>` |
| `format` 格式 | 字符串 `"percentage(2)"` | 对象 `{"type":"text","nullValue":"-"}` |
| `yAxisIndex` | 有（决定左轴/右轴） | 无 |
| `pendingMappings` | 无 | 有（中文参数名标记） |

---

## 四、前端消费链路速查

```text
Hermes 返回 JSON
       ↓
parseVmHermesRenderPayload          ← 读 intent/renderType/operations
       ↓
validateOperation                   ← 读 action||type||op
       ↓
createVmReportBlock
  └─ createVmDslReportBlock
     ├─ validateVmReportDsl          ← 校验 dsl 结构
     ├─ buildRenderSpecFromDsl       ← 生成空 renderSpec
     └─ deriveQueryContext           ← 从 params 派生
       ↓
hydrateVmDslReportBlock
  ├─ buildRequestPlan                ← dsl.requests → 查询计划
  ├─ executeVmQueryPlan              ← 并发请求后端 API
  ├─ executeVmReportTransformFunction ← 执行 transform 函数（内存 join）
  └─ 填充 renderSpec
     ├─ echarts: option.dataset.source = rows
     └─ table: rows = rows
       ↓
Vue 模板渲染
  ├─ <my-chart :options="block.renderSpec.option" />
  └─ <vxe-table :data="block.renderSpec.rows" />
```
