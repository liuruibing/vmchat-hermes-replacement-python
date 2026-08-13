---
type: vm-module
moduleId: "netValue"
title: "产品规模走势"
sqlId: "38ac7662-b120-4cb9-9fdf-8becaf856723"
templateType: "single-product-performance"
---

# 产品规模走势

## 模块概览

- 模块说明：展示产品规模走势页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.lastData`、`body.hisData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 资产净值：产品或组合在对应期间的净值指标。
  - 产品单位净值：产品或组合在对应期间的净值指标。
  - 累计单位净值：产品或组合在对应期间的净值指标。
  - 资产净值(左)：产品或组合在对应期间的净值指标。
  - 单位净值(右)：产品或组合在对应期间的净值指标。
  - 累计单位净值(右)：产品或组合在对应期间的净值指标。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：资产净值(左)
  - 右Y轴候选：单位净值(右)、累计单位净值(右)
- 维度候选：
  - 产品名称（`body.lastData[].VC_FUNDNAME`）
  - 成立日期（`body.lastData[].FUNDCREATEDATE`）
  - 估值日期（`body.lastData[].GZDATE`）
  - 日期（`body.hisData[].TDATE`）
- 指标候选：
  - 资产净值（`body.lastData[].F_701A`）
  - 产品单位净值（`body.lastData[].F_702A`）
  - 累计单位净值（`body.lastData[].F_905`）
  - 资产净值(左)（`body.hisData[].F_701A`）
  - 单位净值(右)（`body.hisData[].F_702A`）
  - 累计单位净值(右)（`body.hisData[].F_905`）

## 数据集绑定

- 响应数据集：`body.lastData`
- 响应数据集：`body.hisData`

## 父模块查询策略

- 子模块选择：clarify-submodule
- 全部子模块：unsupported
- 合并区分字段：不适用
- 合并统一字段：不适用
- 默认顺序：latestNetValue、netValueTrend

## 子模块渲染能力

### 最新净值信息 (`latestNetValue`)

- 响应区域：`body.lastData`
- 默认视图：table
- 可选视图：table、echarts
- 表格字段：
  - 产品名称（`body.lastData[].VC_FUNDNAME`；原值直接使用）
  - 成立日期（`body.lastData[].FUNDCREATEDATE`；原值直接使用）
  - 估值日期（`body.lastData[].GZDATE`；原值直接使用）
  - 资产净值（`body.lastData[].F_701A`；原值直接使用）
  - 产品单位净值（`body.lastData[].F_702A`；原值直接使用）
  - 累计单位净值（`body.lastData[].F_905`；原值直接使用）
- 图表维度：
  - 不适用（源码未渲染页面图表或未识别维度）
- 图表指标：
  - 不适用（源码未渲染页面图表或未识别指标）
- VM 证据：`initTableData`

### 净值走势(成立以来) (`netValueTrend`)

- 响应区域：`body.hisData`
- 默认视图：echarts
- 可选视图：echarts、table
- 表格字段：
  - 不适用（源码未渲染页面表格）
- 图表维度：
  - 日期（`body.hisData[].TDATE`）
- 图表指标：
  - 资产净值(左)（`body.hisData[].F_701A`；原值直接使用）
  - 单位净值(右)（`body.hisData[].F_702A`；原值直接使用）
  - 累计单位净值(右)（`body.hisData[].F_905`；原值直接使用）
- VM 证据：`initEchartData`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.lastData[].VC_FUNDNAME | VC_FUNDNAME | 产品名称 | 原值直接使用 | 未明确 | table |
| body.lastData[].FUNDCREATEDATE | FUNDCREATEDATE | 成立日期 | 原值直接使用 | 未明确 | table |
| body.lastData[].GZDATE | GZDATE | 估值日期 | 原值直接使用 | 未明确 | table |
| body.lastData[].F_701A | F_701A | 资产净值 | 原值直接使用 | 元 | table |
| body.lastData[].F_702A | F_702A | 产品单位净值 | 原值直接使用 | 元 | table |
| body.lastData[].F_905 | F_905 | 累计单位净值 | 原值直接使用 | 元 | table |
| body.hisData[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body.hisData[].F_701A | F_701A | 资产净值(左) | 原值直接使用 | 未明确 | echarts |
| body.hisData[].F_702A | F_702A | 单位净值(右) | 原值直接使用 | 未明确 | echarts |
| body.hisData[].F_905 | F_905 | 累计单位净值(右) | 原值直接使用 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "lastData": [
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUNDNAME": "度量3期大消费基金",
        "FUNDCREATEDATE": "2015-10-09",
        "F_702A": 0.885,
        "F_905": 0.885,
        "F_701A": 39035151.39,
        "GZDATE": "2022-01-28",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "hisData": [
      {
        "D_DATE": "2015-11-18 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_702A": 1,
        "F_905": 1,
        "F_701A": 83491148.41,
        "TDATE": "20151118",
        "FCODE": "SM0513"
      },
      {
        "D_DATE": "2015-11-19 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_702A": 1,
        "F_905": 1,
        "F_701A": 83488929.84,
        "TDATE": "20151119",
        "FCODE": "SM0513"
      },
      {
        "D_DATE": "2015-11-20 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_702A": 1,
        "F_905": 1,
        "F_701A": 83486711.37,
        "TDATE": "20151120",
        "FCODE": "SM0513"
      }
    ]
  }
}
```
