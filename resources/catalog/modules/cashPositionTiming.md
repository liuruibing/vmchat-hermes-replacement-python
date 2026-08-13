---
type: vm-module
moduleId: "cashPositionTiming"
title: "现金类持仓时序"
sqlId: "b9f4277e-2793-4a0d-b9ed-e665e4bbd717"
templateType: "single-product-performance"
---

# 现金类持仓时序

## 模块概览

- 模块说明：展示现金类持仓时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 现金类仓位(左)：对应资产、分类或指标相对组合规模的比例。
  - 现金类利率(右)：“现金类利率(右)”在该VM页面中的业务展示值。
  - 累计单位净值(右)：产品或组合在对应期间的净值指标。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：现金类仓位(左)
  - 右Y轴候选：现金类利率(右)、累计单位净值(右)
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 现金类仓位(左)（`body[].F_CASH_RATIO`）
  - 现金类利率(右)（`body[].F_INDEX_LJ`）
  - 累计单位净值(右)（`body[].F_905`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_CASH_RATIO | F_CASH_RATIO | 现金类仓位(左) | 原值 × 100，保留 4 位小数 | % | echarts |
| body[].F_INDEX_LJ | F_INDEX_LJ | 现金类利率(右) | 保留 4 位小数 | 未明确 | echarts |
| body[].F_905 | F_905 | 累计单位净值(右) | 原值直接使用 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1",
    "cashIndexName": null
  },
  "body": [
    {
      "TDATE": "20220104",
      "FCODE": "SM0513",
      "F_CASH_RATIO": 0.0825588226,
      "F_INDEX_LJ": 0.8571428571,
      "F_905": 0.964
    },
    {
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "F_CASH_RATIO": 0.0949583406,
      "F_INDEX_LJ": 0.8571428571,
      "F_905": 0.972
    },
    {
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "F_CASH_RATIO": 0.0897569907,
      "F_INDEX_LJ": 0.8571428571,
      "F_905": 0.97
    }
  ]
}
```
