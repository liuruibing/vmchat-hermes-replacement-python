# ECharts DSL 规范

本文档只描述如何根据模块 MD 和用户问题生成 ECharts DSL，不描述如何编写模块 MD。

## 适用场景

- 时序趋势
- 分类对比
- 分布占比
- 排名图
- 用户明确要求“图”“折线”“柱状”“饼图”

## view 结构

ECharts 必须使用 `dataset + encode + legend`。

```json
{
  "type": "echarts",
  "title": "图表标题",
  "legend": {
    "show": true,
    "data": ["指标 A", "指标 B"]
  },
  "dataset": {
    "source": "$transform",
    "dimensions": ["TDATE", "valueA", "valueB"]
  },
  "xAxis": {
    "type": "category",
    "name": "日期"
  },
  "yAxis": [
    {
      "type": "value",
      "name": "指标 A"
    }
  ],
  "series": [
    {
      "type": "line",
      "name": "指标 A",
      "encode": {
        "x": "TDATE",
        "y": "valueA"
      },
      "yAxisIndex": 0
    }
  ]
}
```

## 硬规则

- 必须有 `legend`。
- `legend.show` 必须是 `true`。
- `legend.data` 必须与 `series[].name` 顺序一致。
- `dataset.source` 固定为 `"$transform"`。
- `dataset.dimensions` 必须包含所有轴和 series 使用的字段。
- `series[].type` 只允许 `line`、`bar`、`pie`。
- `line`、`bar` 必须有 `xAxis` 和 `yAxis`。
- `line`、`bar` 必须使用 `series[].encode.x` 和 `series[].encode.y`，且必须引用 `dataset.dimensions` 中的字段。
- 同一个 ECharts view 中所有 `line`、`bar` 的 `series[].encode.x` 必须一致。
- 单图最多两个 Y 轴。
- `yAxisIndex` 只能是 `0` 或 `1`。
- 模块 MD 声明 `Y轴推荐：双Y轴` 时，只选择单侧候选可用单轴；同时选择左右候选时必须生成两个 Y 轴，左侧候选使用 `yAxisIndex: 0`，右侧候选使用 `yAxisIndex: 1`。
- 单模块 `series[].name` 必须使用字段映射展示名称原文，不能删除 `(左)`、`(右)` 等来源或轴向标记。
- 相同单位、相同量纲应共用同一 Y 轴。
- 单个 ECharts DSL 不支持三种及以上不兼容量纲同时使用独立 Y 轴。
- **量级悬殊必须分轴**：即使字段映射中多个指标的单位相同（如都是「元」），若示例数据或常识表明数值量级相差悬殊（如资产净值在千万级、单位净值在 1 附近），必须拆分为两个 Y 轴——量级大的指标用 yAxisIndex: 0，量级小的指标用 yAxisIndex: 1。不能因为单位相同就默认共用同一 Y 轴。当用户明确指出「不应该用一个 y 轴」时，立即按量级拆分，无需反问。
- 每个 `series[]` 都必须显式包含 `format`，格式结构与 Table DSL 的 `columns[].format` 一致。
- 若 MD 的字段映射表提供“展示转换”或“展示单位”，必须据此生成对应 `format`。
- 若 MD 未提供展示转换、单位或小数位规则，不得根据字段名、指标名、数值范围或常识猜测格式；必须使用 `{"type":"raw"}`，让前端按原值展示。

## format 规则

ECharts 的数值格式化必须写在 `series[].format` 中，不在 transform 中转字符串。`series[].format` 是必填字段，禁止省略。

具体格式类型、展示转换映射、百分比换算规则以 [DSL 通用规范的展示格式化规则](dsl-spec.md#展示格式化规则) 为唯一准则。不要在本文档中另行推导 format 映射。

## 堆叠图

- 堆叠柱状图使用 `series[].type = "bar"`，并为同组 series 设置相同的 `stack`。
- 堆叠折线图使用 `series[].type = "line"`，并为同组 series 设置相同的 `stack`。
- 不新增 `stackedBar` 或 `stackedLine` 作为 `series[].type`。

## pie

- 不需要 `xAxis`、`yAxis`、`yAxisIndex`。
- 必须使用 `series[].encode.itemName` 和 `series[].encode.value`。
- `series[].encode.itemName` 必须引用 `dataset.dimensions` 中的分类字段。
- `series[].encode.value` 必须引用 `dataset.dimensions` 中的数值字段。

## 禁止旧结构

```json
{
  "xField": "TDATE",
  "series": [
    {
      "field": "value",
      "chartType": "line"
    }
  ]
}
```
