---
type: vm-module
moduleId: "creditRiskRateDistribution"
title: "信用风险评级分布"
sqlId: "944d0936-066f-4d4c-ad16-67767a431d7a"
templateType: "single-product-performance"
---

# 信用风险评级分布

## 模块概览

- 模块说明：展示信用风险评级分布页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 持仓市值：“持仓市值”在该VM页面中的业务展示值。
  - 评级市值占比(持仓)：对应资产、分类或指标相对组合规模的比例。
  - 评级市值占比(债券)：对应资产、分类或指标相对组合规模的比例。
  - 评级面值占比(债券)：对应资产、分类或指标相对组合规模的比例。

## 渲染能力

- 源码组件：table
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：bar、line
- 维度候选：
  - 持仓评级（`body[].VC_LONG_LEVEL_NAME`）
- 指标候选：
  - 持仓市值（`body[].F_PRICE`）
  - 评级市值占比(持仓)（`body[].F_ZJZB`）
  - 评级市值占比(债券)（`body[].F_ZZQB`）
  - 评级面值占比(债券)（`body[].F_ZMZB`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].VC_LONG_LEVEL_NAME | VC_LONG_LEVEL_NAME | 持仓评级 | 原值直接使用 | 未明确 | table |
| body[].F_PRICE | F_PRICE | 持仓市值 | 原值 ÷ 10000，保留 4 位小数 | 万元 | table |
| body[].F_ZJZB | F_ZJZB | 评级市值占比(持仓) | 原值 × 100，保留 2 位小数 | % | table |
| body[].F_ZZQB | F_ZZQB | 评级市值占比(债券) | 原值 × 100，保留 2 位小数 | % | table |
| body[].F_ZMZB | F_ZMZB | 评级面值占比(债券) | 原值 × 100，保留 2 位小数 | % | table |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "VC_FUNDCODE": "SM0513",
      "VC_LONG_LEVEL_CODE": "1",
      "VC_LONG_LEVEL_NAME": "A",
      "F_RK": 8,
      "F_PRICE": 12121,
      "F_ZJZB": 0.0000352834307865,
      "F_ZZQB": 0.0054544505454451,
      "F_ZMZB": 0.1516896120150188,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "VC_LONG_LEVEL_CODE": "7",
      "VC_LONG_LEVEL_NAME": "A-3",
      "F_RK": 9,
      "F_PRICE": 121212,
      "F_ZJZB": 0.000352840129733,
      "F_ZZQB": 0.0545454054545405,
      "F_ZMZB": 0.2908635794743429,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "VC_LONG_LEVEL_CODE": "OTHER",
      "VC_LONG_LEVEL_NAME": "其它",
      "F_RK": 27,
      "F_PRICE": 2322,
      "F_ZJZB": 0.0000067591887044,
      "F_ZZQB": 0.00104490010449,
      "F_ZMZB": 0.2780976220275344,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
