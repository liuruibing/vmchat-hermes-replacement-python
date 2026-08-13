---
type: vm-module
moduleId: "holdPlate"
title: "A股持仓指数及板块时序"
sqlId: "caa5b2df-8278-458e-b176-db71cce9a024"
templateType: "single-product-performance"
---

# A股持仓指数及板块时序

## 模块概览

- 模块说明：展示A股持仓指数及板块时序页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.dayIndexData`、`body.dayBoardColumn`、`body.dayBoardData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 沪深300：“沪深300”在该VM页面中的业务展示值。
  - 中证500：“中证500”在该VM页面中的业务展示值。
  - 中证1000：“中证1000”在该VM页面中的业务展示值。
  - 中证2000：“中证2000”在该VM页面中的业务展示值。
  - 其他：“其他”在该VM页面中的业务展示值。
  - 沪市主板：“沪市主板”在该VM页面中的业务展示值。
  - 科创板：“科创板”在该VM页面中的业务展示值。
  - 深市主板：“深市主板”在该VM页面中的业务展示值。
  - 创业板：“创业板”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body.dayIndexData[].TDATE`）
  - 日期（`body.dayBoardData[].TDATE`）
  - 维度名称（`body.dayBoardColumn[].DIM_NME`）
  - 列名（`body.dayBoardColumn[].columnName`）
- 指标候选：
  - 沪深300（`body.dayIndexData[].F_HS300_RATIO`）
  - 中证500（`body.dayIndexData[].F_ZZ500_RATIO`）
  - 中证1000（`body.dayIndexData[].F_ZZ1000_RATIO`）
  - 中证2000（`body.dayIndexData[].F_ZZ2000_RATIO`）
  - 其他（`body.dayIndexData[].F_QT_RATIO`）
  - 沪市主板（`body.dayBoardData[].F_HZB_RATIO`）
  - 科创板（`body.dayBoardData[].F_KCB_RATIO`）
  - 深市主板（`body.dayBoardData[].F_SZB_RATIO`）
  - 创业板（`body.dayBoardData[].F_CYB_RATIO`）

## 数据集绑定

- 响应数据集：`body.dayIndexData`
- 响应数据集：`body.dayBoardColumn`
- 响应数据集：`body.dayBoardData`
- 动态列名：`body.dayBoardColumn[].DIM_NME`
- 动态字段名：`body.dayBoardColumn[].columnName`
- 动态取值：`body.dayBoardData[][columnName]`
- 已解析字段：`body.dayBoardData[].F_HZB_RATIO`、`body.dayBoardData[].F_KCB_RATIO`、`body.dayBoardData[].F_SZB_RATIO`、`body.dayBoardData[].F_CYB_RATIO`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.dayIndexData[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body.dayIndexData[].F_HS300_RATIO | F_HS300_RATIO | 沪深300 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayIndexData[].F_ZZ500_RATIO | F_ZZ500_RATIO | 中证500 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayIndexData[].F_ZZ1000_RATIO | F_ZZ1000_RATIO | 中证1000 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayIndexData[].F_ZZ2000_RATIO | F_ZZ2000_RATIO | 中证2000 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayIndexData[].F_QT_RATIO | F_QT_RATIO | 其他 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayBoardData[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body.dayBoardColumn[].DIM_NME | DIM_NME | 维度名称 | 原值直接使用 | 未明确 | echarts |
| body.dayBoardColumn[].columnName | columnName | 列名 | 原值直接使用 | 未明确 | echarts |
| body.dayBoardData[].F_HZB_RATIO | F_HZB_RATIO | 沪市主板 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayBoardData[].F_KCB_RATIO | F_KCB_RATIO | 科创板 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayBoardData[].F_SZB_RATIO | F_SZB_RATIO | 深市主板 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.dayBoardData[].F_CYB_RATIO | F_CYB_RATIO | 创业板 | 原值 × 100，保留 2 位小数 | % | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "dayIndexData": [
      {
        "TDATE": "20220127",
        "FCODE": "SM0513",
        "F_HS300_RATIO": 3.6e-7,
        "F_ZZ500_RATIO": 3.6e-7,
        "F_ZZ1000_RATIO": 0.00000129,
        "F_ZZ2000_RATIO": 0.00129401,
        "F_QT_RATIO": null
      },
      {
        "TDATE": "20220128",
        "FCODE": "SM0513",
        "F_HS300_RATIO": 2.8e-7,
        "F_ZZ500_RATIO": 2.8e-7,
        "F_ZZ1000_RATIO": 0.00000102,
        "F_ZZ2000_RATIO": 0.00102539,
        "F_QT_RATIO": null
      }
    ],
    "dayBoardColumn": [
      {
        "DIM_CDE": "HZB",
        "DIM_NME": "沪市主板",
        "F_RK": 1,
        "columnName": "F_HZB_RATIO",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "KCB",
        "DIM_NME": "科创板",
        "F_RK": 2,
        "columnName": "F_KCB_RATIO",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "SZB",
        "DIM_NME": "深市主板",
        "F_RK": 3,
        "columnName": "F_SZB_RATIO",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "dayBoardData": [
      {
        "TDATE": "20220127",
        "FCODE": "SM0513",
        "F_HZB_RATIO": 2.8e-7,
        "F_KCB_RATIO": 2.8e-7,
        "F_SZB_RATIO": 0.00000102,
        "F_CYB_RATIO": 0.00102539,
        "F_HK_RATIO": null,
        "F_BJS_RATIO": null,
        "F_XSB_RATIO": null,
        "F_QT_RATIO": null
      },
      {
        "TDATE": "20220128",
        "FCODE": "SM0513",
        "F_HZB_RATIO": 3.6e-7,
        "F_KCB_RATIO": 3.6e-7,
        "F_SZB_RATIO": 0.00000129,
        "F_CYB_RATIO": 0.00129401,
        "F_HK_RATIO": null,
        "F_BJS_RATIO": null,
        "F_XSB_RATIO": null,
        "F_QT_RATIO": null
      }
    ]
  }
}
```
