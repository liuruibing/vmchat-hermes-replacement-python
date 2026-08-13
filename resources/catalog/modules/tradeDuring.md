---
type: vm-module
moduleId: "tradeDuring"
title: "期间交易额"
sqlId: "d49ae5ec-675c-4ae2-808e-793eecee064f"
templateType: "single-product-performance"
---

# 期间交易额

## 模块概览

- 模块说明：展示期间交易额页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 日(1天)：“日(1天)”在该VM页面中的业务展示值。
  - 周(5天)：“周(5天)”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body[].XAXISDATA`）
- 指标候选：
  - 日(1天)（`body[].YAXISDATA1`）
  - 周(5天)（`body[].YAXISDATA2`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].XAXISDATA | XAXISDATA | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].YAXISDATA1 | YAXISDATA1 | 日(1天) | 原值直接使用 | 万元 | echarts |
| body[].YAXISDATA2 | YAXISDATA2 | 周(5天) | 原值直接使用 | 万元 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "XAXISDATA": "股票",
      "YAXISDATA1": 1785.6385,
      "YAXISDATA2": 2907.7561
    },
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "XAXISDATA": "基金",
      "YAXISDATA1": 84.7656,
      "YAXISDATA2": 0
    },
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "XAXISDATA": "ETF基金",
      "YAXISDATA1": 84.7656,
      "YAXISDATA2": 0
    }
  ]
}
```
