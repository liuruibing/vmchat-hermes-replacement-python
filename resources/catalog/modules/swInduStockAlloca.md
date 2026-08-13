---
type: vm-module
moduleId: "swInduStockAlloca"
title: "A股行业配置风险"
sqlId: "76022f4b-f82e-4835-9882-b2e012e08b9d"
templateType: "single-product-performance"
---

# A股行业配置风险

## 模块概览

- 模块说明：展示A股行业配置风险页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 多头市值：“多头市值”在该VM页面中的业务展示值。
  - 空头市值：“空头市值”在该VM页面中的业务展示值。
  - 净暴露：对应资产、分类或指标相对组合规模的比例。
  - 暴露占比：对应资产、分类或指标相对组合规模的比例。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 行业（`body[].industryName`）
- 指标候选：
  - 多头市值（`body[].industryAvgDtPrice`）
  - 空头市值（`body[].industryAvgKtPrice`）
  - 净暴露（`body[].industryAvgNsPrice`）
  - 暴露占比（`body[].industryNsRatio`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].industryName | industryName | 行业 | 原值直接使用 | 未明确 | table、echarts |
| body[].industryAvgDtPrice | industryAvgDtPrice | 多头市值 | 保留 2 位小数 | 元 | table |
| body[].industryAvgKtPrice | industryAvgKtPrice | 空头市值 | 保留 2 位小数 | 元 | table |
| body[].industryAvgNsPrice | industryAvgNsPrice | 净暴露 | 保留 2 位小数 | 元 | table、echarts |
| body[].industryNsRatio | industryNsRatio | 暴露占比 | 原值 × 100，保留 2 位小数 | % | table |

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
      "VC_FUNDCODE": "SM0513",
      "industryCode": "110000",
      "industryAvgDtPrice": 7741383.368421053,
      "industryName": "农林牧渔",
      "industryAvgKtPrice": 0,
      "industryAvgNsPrice": 7741383.368421053,
      "industryNsRatio": 0.87363683,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "460000",
      "industryAvgDtPrice": 1376208.2105263157,
      "industryName": "社会服务",
      "industryAvgKtPrice": 0,
      "industryAvgNsPrice": 1376208.2105263157,
      "industryNsRatio": 0.15530896,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "370000",
      "industryAvgDtPrice": 121762.36842105263,
      "industryName": "医药生物",
      "industryAvgKtPrice": 0,
      "industryAvgNsPrice": 121762.36842105263,
      "industryNsRatio": 0.01374122,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
