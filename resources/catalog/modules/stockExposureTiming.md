---
type: vm-module
moduleId: "stockExposureTiming"
title: "股票净敞口时序"
sqlId: "712b930b-87a5-4cba-8da0-3671d4c8dc54"
templateType: "single-product-performance"
---

# 股票净敞口时序

## 模块概览

- 模块说明：展示股票净敞口时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 股票净敞口占比(左)：对应资产、分类或指标相对组合规模的比例。
  - 累计单位净值(右)：产品或组合在对应期间的净值指标。
  - 沪深300(右)：“沪深300(右)”在该VM页面中的业务展示值。
  - 中证500(右)：“中证500(右)”在该VM页面中的业务展示值。
  - 中证1000(右)：“中证1000(右)”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：股票净敞口占比(左)
  - 右Y轴候选：累计单位净值(右)、沪深300(右)、中证500(右)、中证1000(右)
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 股票净敞口占比(左)（`body[].F_STOCK_EXP`）
  - 累计单位净值(右)（`body[].F_905_GYH`）
  - 沪深300(右)（`body[].F_HS300_GYH`）
  - 中证500(右)（`body[].F_ZZ500_GYH`）
  - 中证1000(右)（`body[].F_ZZ1000_GYH`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_STOCK_EXP | F_STOCK_EXP | 股票净敞口占比(左) | 原值 × 100，保留 2 位小数 | % | echarts |
| body[].F_905_GYH | F_905_GYH | 累计单位净值(右) | 原值直接使用 | 未明确 | echarts |
| body[].F_HS300_GYH | F_HS300_GYH | 沪深300(右) | 原值直接使用 | 未明确 | echarts |
| body[].F_ZZ500_GYH | F_ZZ500_GYH | 中证500(右) | 原值直接使用 | 未明确 | echarts |
| body[].F_ZZ1000_GYH | F_ZZ1000_GYH | 中证1000(右) | 原值直接使用 | 未明确 | echarts |

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
      "F_STOCK_EXP": 1.26,
      "F_905_GYH": 1,
      "F_HS300_GYH": 1,
      "F_ZZ500_GYH": 1,
      "F_ZZ1000_GYH": 1
    },
    {
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "F_STOCK_EXP": 1.25,
      "F_905_GYH": 1.0083,
      "F_HS300_GYH": 0.9899,
      "F_ZZ500_GYH": 0.9821,
      "F_ZZ1000_GYH": 0.9748
    },
    {
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "F_STOCK_EXP": 1.24,
      "F_905_GYH": 1.0062,
      "F_HS300_GYH": 0.9798,
      "F_ZZ500_GYH": 0.9831,
      "F_ZZ1000_GYH": 0.9826
    }
  ]
}
```
