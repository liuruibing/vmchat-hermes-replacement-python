---
type: vm-module
moduleId: "topTenOrTopFiveStockPositionTime"
title: "个股持仓前十/前五占比时序"
sqlId: "8c0d7ee0-1887-4e43-90b5-2aac7578daae"
templateType: "single-product-performance"
---

# 个股持仓前十/前五占比时序

## 模块概览

- 模块说明：展示个股持仓前十/前五占比时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 股票持仓占比(左)：对应资产、分类或指标相对组合规模的比例。
  - 前十大占比(左)：对应资产、分类或指标相对组合规模的比例。
  - 前五大占比(左)：对应资产、分类或指标相对组合规模的比例。
  - 沪深300(右）：“沪深300(右）”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：股票持仓占比(左)、前十大占比(左)、前五大占比(左)
  - 右Y轴候选：沪深300(右）
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 股票持仓占比(左)（`body[].F_STOCK_RATIO`）
  - 前十大占比(左)（`body[].F_TOPTEN_RATIO`）
  - 前五大占比(左)（`body[].F_TOPFIVE_RATIO`）
  - 沪深300(右）（`body[].F_HS300_PRICE`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_STOCK_RATIO | F_STOCK_RATIO | 股票持仓占比(左) | 原值 × 100，保留 2 位小数 | % | echarts |
| body[].F_TOPTEN_RATIO | F_TOPTEN_RATIO | 前十大占比(左) | 原值 × 100，保留 2 位小数 | % | echarts |
| body[].F_TOPFIVE_RATIO | F_TOPFIVE_RATIO | 前五大占比(左) | 原值 × 100，保留 2 位小数 | % | echarts |
| body[].F_HS300_PRICE | F_HS300_PRICE | 沪深300(右） | 原值直接使用 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "TDATE": "20220104",
      "FCODE": "SM0513",
      "F_STOCK_RATIO": 1.27715361,
      "F_TOPTEN_RATIO": 0.92322241,
      "F_TOPFIVE_RATIO": 0.57935091,
      "F_HS300_PRICE": 4917.77
    },
    {
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "F_STOCK_RATIO": 1.26252391,
      "F_TOPTEN_RATIO": 0.94085949,
      "F_TOPFIVE_RATIO": 0.60121798,
      "F_HS300_PRICE": 4868.12
    },
    {
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "F_STOCK_RATIO": 1.24926215,
      "F_TOPTEN_RATIO": 0.94670651,
      "F_TOPFIVE_RATIO": 0.60373652,
      "F_HS300_PRICE": 4818.23
    }
  ]
}
```
