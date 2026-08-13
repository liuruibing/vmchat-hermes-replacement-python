---
type: vm-module
moduleId: "fundDurationTiming"
title: "组合加权久期时序"
sqlId: "7d29ed40-0d69-4cd1-93a8-0a2bf9eac9cd"
templateType: "single-product-performance"
---

# 组合加权久期时序

## 模块概览

- 模块说明：展示组合加权久期时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 组合久期：衡量债券组合对利率变化敏感度的久期指标。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 组合久期（`body[].F_MDF_DURATION`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_MDF_DURATION | F_MDF_DURATION | 组合久期 | 保留 4 位小数 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "D_DATE": "2022-01-04 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_MDF_DURATION": 2.3383,
      "TDATE": "20220104",
      "FCODE": "SM0513"
    },
    {
      "D_DATE": "2022-01-05 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_MDF_DURATION": 2.3305,
      "TDATE": "20220105",
      "FCODE": "SM0513"
    },
    {
      "D_DATE": "2022-01-06 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_MDF_DURATION": 2.3314,
      "TDATE": "20220106",
      "FCODE": "SM0513"
    }
  ]
}
```
