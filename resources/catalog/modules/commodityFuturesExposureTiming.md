---
type: vm-module
moduleId: "commodityFuturesExposureTiming"
title: "商品期货净敞口时序"
sqlId: "a26dc9c7-6ca1-49f0-a93f-bceeedea3aee"
templateType: "single-product-performance"
---

# 商品期货净敞口时序

## 模块概览

- 模块说明：展示商品期货净敞口时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 商品期货净敞口占比(左)：对应资产、分类或指标相对组合规模的比例。
  - 累计单位净值(右)：产品或组合在对应期间的净值指标。
  - 南华商品指数(右)：“南华商品指数(右)”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：商品期货净敞口占比(左)
  - 右Y轴候选：累计单位净值(右)、南华商品指数(右)
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 商品期货净敞口占比(左)（`body[].F_QH_SP_EXP`）
  - 累计单位净值(右)（`body[].F_905_GYH`）
  - 南华商品指数(右)（`body[].F_NHSPZS_GYH`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_QH_SP_EXP | F_QH_SP_EXP | 商品期货净敞口占比(左) | 原值 × 100，保留 4 位小数 | % | echarts |
| body[].F_905_GYH | F_905_GYH | 累计单位净值(右) | 保留 4 位小数 | 未明确 | echarts |
| body[].F_NHSPZS_GYH | F_NHSPZS_GYH | 南华商品指数(右) | 保留 4 位小数 | 未明确 | echarts |

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
      "F_QH_SP_EXP": 0.7080306156819285,
      "F_905_GYH": 1,
      "F_NHSPZS_GYH": 1
    },
    {
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "F_QH_SP_EXP": 1.0762261440673833,
      "F_905_GYH": 1.0083,
      "F_NHSPZS_GYH": 1.0098
    },
    {
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "F_QH_SP_EXP": 0.778947960847428,
      "F_905_GYH": 1.0062,
      "F_NHSPZS_GYH": 1.0099
    }
  ]
}
```
