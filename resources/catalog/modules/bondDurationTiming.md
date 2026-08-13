---
type: vm-module
moduleId: "bondDurationTiming"
title: "债券久期变动时序"
sqlId: "2010a50e-3f6a-478c-8dc2-796df2799f10"
templateType: "single-product-performance"
---

# 债券久期变动时序

## 模块概览

- 模块说明：展示债券久期变动时序页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.dayDataColumn`、`body.dayData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 修正久期:0-1.0：衡量债券组合对利率变化敏感度的久期指标。
  - 修正久期:1.0-3.0：衡量债券组合对利率变化敏感度的久期指标。
  - 修正久期:3.0-5.0：衡量债券组合对利率变化敏感度的久期指标。
  - 修正久期:5.0-7.0：衡量债券组合对利率变化敏感度的久期指标。
  - 修正久期>7.0：衡量债券组合对利率变化敏感度的久期指标。
  - 其它：“其它”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body.dayData[].TDATE`）
  - 维度名称（`body.dayDataColumn[].DIM_NME`）
  - 列名（`body.dayDataColumn[].columnName`）
- 指标候选：
  - 修正久期:0-1.0（`body.dayData[].F_XZJQ1`）
  - 修正久期:1.0-3.0（`body.dayData[].F_XZJQ2`）
  - 修正久期:3.0-5.0（`body.dayData[].F_XZJQ3`）
  - 修正久期:5.0-7.0（`body.dayData[].F_XZJQ4`）
  - 修正久期>7.0（`body.dayData[].F_XZJQ5`）
  - 其它（`body.dayData[].F_XZJQ6`）

## 数据集绑定

- 响应数据集：`body.dayDataColumn`
- 响应数据集：`body.dayData`
- 动态列名：`body.dayDataColumn[].DIM_NME`
- 动态字段名：`body.dayDataColumn[].columnName`
- 动态取值：`body.dayData[][columnName]`
- 已解析字段：`body.dayData[].F_XZJQ1`、`body.dayData[].F_XZJQ2`、`body.dayData[].F_XZJQ3`、`body.dayData[].F_XZJQ4`、`body.dayData[].F_XZJQ5`、`body.dayData[].F_XZJQ6`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.dayData[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body.dayDataColumn[].DIM_NME | DIM_NME | 维度名称 | 原值直接使用 | 未明确 | echarts |
| body.dayDataColumn[].columnName | columnName | 列名 | 原值直接使用 | 未明确 | echarts |
| body.dayData[].F_XZJQ1 | F_XZJQ1 | 修正久期:0-1.0 | 原值 × 100 | % | echarts |
| body.dayData[].F_XZJQ2 | F_XZJQ2 | 修正久期:1.0-3.0 | 原值 × 100 | % | echarts |
| body.dayData[].F_XZJQ3 | F_XZJQ3 | 修正久期:3.0-5.0 | 原值 × 100 | % | echarts |
| body.dayData[].F_XZJQ4 | F_XZJQ4 | 修正久期:5.0-7.0 | 原值 × 100 | % | echarts |
| body.dayData[].F_XZJQ5 | F_XZJQ5 | 修正久期>7.0 | 原值 × 100 | % | echarts |
| body.dayData[].F_XZJQ6 | F_XZJQ6 | 其它 | 原值 × 100 | % | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "dayDataColumn": [
      {
        "DIM_CDE": "1",
        "DIM_NME": "修正久期:0-1.0",
        "F_RK": 1,
        "columnName": "F_XZJQ1",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "2",
        "DIM_NME": "修正久期:1.0-3.0",
        "F_RK": 2,
        "columnName": "F_XZJQ2",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "3",
        "DIM_NME": "修正久期:3.0-5.0",
        "F_RK": 3,
        "columnName": "F_XZJQ3",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "dayData": [
      {
        "D_DATE": "2022-01-26 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_XZJQ1": 0.5,
        "F_XZJQ2": 0.25,
        "F_XZJQ3": 0.25,
        "F_XZJQ4": 0,
        "F_XZJQ5": 0,
        "F_XZJQ6": 0,
        "TDATE": "20220126",
        "FCODE": "SM0513"
      },
      {
        "D_DATE": "2022-01-27 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_XZJQ1": 0.3333333333333333,
        "F_XZJQ2": 0.1666666666666667,
        "F_XZJQ3": 0.1666666666666667,
        "F_XZJQ4": 0.1666666666666667,
        "F_XZJQ5": 0,
        "F_XZJQ6": 0.1666666666666667,
        "TDATE": "20220127",
        "FCODE": "SM0513"
      },
      {
        "D_DATE": "2022-01-28 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_XZJQ1": 0.25,
        "F_XZJQ2": 0.125,
        "F_XZJQ3": 0.125,
        "F_XZJQ4": 0.125,
        "F_XZJQ5": 0.25,
        "F_XZJQ6": 0.125,
        "TDATE": "20220128",
        "FCODE": "SM0513"
      }
    ]
  }
}
```
