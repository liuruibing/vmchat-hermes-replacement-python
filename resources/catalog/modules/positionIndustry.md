---
type: vm-module
moduleId: "positionIndustry"
title: "股票期末持仓行业占比"
sqlId: "d8ac50c1-b41c-498e-8c8a-bd6a577177a6"
templateType: "single-product-performance"
---

# 股票期末持仓行业占比

## 模块概览

- 模块说明：展示股票期末持仓行业占比页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 期末持仓市值：“期末持仓市值”在该VM页面中的业务展示值。
  - 期末占比：对应资产、分类或指标相对组合规模的比例。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 行业（`body[].industryName`）
- 指标候选：
  - 期末持仓市值（`body[].industryPrice`）
  - 期末占比（`body[].industryRatio`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].industryName | industryName | 行业 | 原值直接使用 | 未明确 | table、echarts |
| body[].industryPrice | industryPrice | 期末持仓市值 | 原值 ÷ 10000，保留 2 位小数 | 万元 | table |
| body[].industryRatio | industryRatio | 期末占比 | 原值 × 100，保留 4 位小数 | % | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1",
    "industryType": "SWSR"
  },
  "body": [
    {
      "industryCode": "110000",
      "industryName": "申万(A股)-农林牧渔",
      "industryPrice": 8481558,
      "industryRatio": 0.4615220115354955,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "industryCode": "460000",
      "industryName": "申万(A股)-社会服务",
      "industryPrice": 1414248,
      "industryRatio": 0.076955976929009,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "industryCode": "00",
      "industryName": "恒生(港股)-能源业",
      "industryPrice": 8481558,
      "industryRatio": 0.4615220115354955,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
