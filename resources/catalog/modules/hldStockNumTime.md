---
type: vm-module
moduleId: "hldStockNumTime"
title: "持股数量时序变化图"
sqlId: "2f3f7b80-5c28-407f-90c5-5d2464eaf5a0"
templateType: "single-product-performance"
---

# 持股数量时序变化图

## 模块概览

- 模块说明：展示持股数量时序变化图页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 日(1天)：“日(1天)”在该VM页面中的业务展示值。

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

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].XAXISDATA | XAXISDATA | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].YAXISDATA1 | YAXISDATA1 | 日(1天) | 原值直接使用 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "XAXISDATA": "20210104",
      "YAXISDATA1": 18,
      "TDATE": "20210104",
      "FCODE": "SM0513"
    },
    {
      "XAXISDATA": "20210105",
      "YAXISDATA1": 15,
      "TDATE": "20210105",
      "FCODE": "SM0513"
    },
    {
      "XAXISDATA": "20210106",
      "YAXISDATA1": 18,
      "TDATE": "20210106",
      "FCODE": "SM0513"
    }
  ]
}
```
