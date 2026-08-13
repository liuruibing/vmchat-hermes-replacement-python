---
type: vm-module
moduleId: "topFiveIndustryTime"
title: "A股行业集中度"
sqlId: "052a0166-713f-413f-9fee-d5f9230f813c"
templateType: "single-product-performance"
---

# A股行业集中度

## 模块概览

- 模块说明：展示A股行业集中度页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.dayDataColumn`、`body.dayData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 农林牧渔：“农林牧渔”在该VM页面中的业务展示值。
  - 医药生物：“医药生物”在该VM页面中的业务展示值。
  - 传媒：“传媒”在该VM页面中的业务展示值。
  - 房地产：“房地产”在该VM页面中的业务展示值。
  - 银行：“银行”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body.dayData[].TDATE`）
  - 行业名称（`body.dayDataColumn[].industryName`）
  - 列名（`body.dayDataColumn[].columnName`）
- 指标候选：
  - 农林牧渔（`body.dayData[].F_HY1`）
  - 医药生物（`body.dayData[].F_HY11`）
  - 传媒（`body.dayData[].F_HY26`）
  - 房地产（`body.dayData[].F_HY14`）
  - 银行（`body.dayData[].F_HY17`）

## 数据集绑定

- 响应数据集：`body.dayDataColumn`
- 响应数据集：`body.dayData`
- 动态列名：`body.dayDataColumn[].industryName`
- 动态字段名：`body.dayDataColumn[].columnName`
- 动态取值：`body.dayData[][columnName]`
- 已解析字段：`body.dayData[].F_HY1`、`body.dayData[].F_HY11`、`body.dayData[].F_HY26`、`body.dayData[].F_HY14`、`body.dayData[].F_HY17`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.dayData[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body.dayDataColumn[].industryName | industryName | 行业名称 | 原值直接使用 | 未明确 | echarts |
| body.dayDataColumn[].columnName | columnName | 列名 | 原值直接使用 | 未明确 | echarts |
| body.dayData[].F_HY1 | F_HY1 | 农林牧渔 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayData[].F_HY11 | F_HY11 | 医药生物 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayData[].F_HY26 | F_HY26 | 传媒 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayData[].F_HY14 | F_HY14 | 房地产 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayData[].F_HY17 | F_HY17 | 银行 | 原值 × 100，保留 2 位小数 | % | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1",
    "industryType": "SWSR"
  },
  "body": {
    "dayDataColumn": [
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "110000",
        "industryFundRatio": 0.1648012933041419,
        "industryName": "农林牧渔",
        "columnName": "F_HY1",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "370000",
        "industryFundRatio": 0.002547144866142,
        "industryName": "医药生物",
        "columnName": "F_HY11",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "720000",
        "industryFundRatio": 0.001515936345231,
        "industryName": "传媒",
        "columnName": "F_HY26",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "dayData": [
      {
        "TDATE": "20220104",
        "FCODE": "SM0513",
        "VC_FUNDCODE": "SM0513",
        "F_HY1": 0.116674197556278,
        "F_HY2": 0,
        "F_HY3": 0,
        "F_HY4": 0,
        "F_HY5": 0,
        "F_HY6": 0,
        "F_HY7": 0,
        "F_HY8": 0,
        "F_HY9": 0,
        "F_HY10": 0,
        "F_HY11": 0,
        "F_HY12": 0,
        "F_HY13": 0,
        "F_HY14": 0,
        "F_HY15": 0,
        "F_HY16": 0.0249475881380778,
        "F_HY17": 0,
        "F_HY18": 0,
        "F_HY19": 0,
        "F_HY20": 0,
        "F_HY21": 0,
        "F_HY22": 0,
        "F_HY23": 0,
        "F_HY24": 0,
        "F_HY25": 0,
        "F_HY26": 0.0288027905593881,
        "F_HY27": 0,
        "F_HY28": 0,
        "F_HY29": 0,
        "F_HY30": 0,
        "F_HY31": 0
      },
      {
        "TDATE": "20220105",
        "FCODE": "SM0513",
        "VC_FUNDCODE": "SM0513",
        "F_HY1": 0.1253068933181225,
        "F_HY2": 0,
        "F_HY3": 0,
        "F_HY4": 0,
        "F_HY5": 0,
        "F_HY6": 0,
        "F_HY7": 0,
        "F_HY8": 0,
        "F_HY9": 0,
        "F_HY10": 0,
        "F_HY11": 0,
        "F_HY12": 0,
        "F_HY13": 0,
        "F_HY14": 0,
        "F_HY15": 0,
        "F_HY16": 0.0242732481557143,
        "F_HY17": 0,
        "F_HY18": 0,
        "F_HY19": 0,
        "F_HY20": 0,
        "F_HY21": 0,
        "F_HY22": 0,
        "F_HY23": 0,
        "F_HY24": 0,
        "F_HY25": 0,
        "F_HY26": 0,
        "F_HY27": 0,
        "F_HY28": 0,
        "F_HY29": 0,
        "F_HY30": 0,
        "F_HY31": 0
      },
      {
        "TDATE": "20220106",
        "FCODE": "SM0513",
        "VC_FUNDCODE": "SM0513",
        "F_HY1": 0.1265077703266617,
        "F_HY2": 0,
        "F_HY3": 0,
        "F_HY4": 0,
        "F_HY5": 0,
        "F_HY6": 0,
        "F_HY7": 0,
        "F_HY8": 0,
        "F_HY9": 0,
        "F_HY10": 0,
        "F_HY11": 0,
        "F_HY12": 0,
        "F_HY13": 0,
        "F_HY14": 0,
        "F_HY15": 0,
        "F_HY16": 0.0241836960840548,
        "F_HY17": 0,
        "F_HY18": 0,
        "F_HY19": 0,
        "F_HY20": 0,
        "F_HY21": 0,
        "F_HY22": 0,
        "F_HY23": 0,
        "F_HY24": 0,
        "F_HY25": 0,
        "F_HY26": 0,
        "F_HY27": 0,
        "F_HY28": 0,
        "F_HY29": 0,
        "F_HY30": 0,
        "F_HY31": 0
      }
    ]
  }
}
```
