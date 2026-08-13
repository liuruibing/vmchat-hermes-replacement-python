---
type: vm-module
moduleId: "assetContribute"
title: "大类资产收益贡献"
sqlId: "4c15f9fd-98c1-4280-b7bb-56893691279a"
templateType: "single-product-performance"
---

# 大类资产收益贡献

## 模块概览

- 模块说明：展示大类资产收益贡献页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 期末持仓市值：“期末持仓市值”在该VM页面中的业务展示值。
  - 期末持仓市值占资产净值比：产品或组合在对应期间的净值指标。
  - 期间收益额：统计区间内产生的绝对收益金额。
  - 期间费后收益额：统计区间内产生的绝对收益金额。
  - 净值贡献度：产品或组合在对应期间的净值指标。
  - 收益贡献比例：对应资产、分类或指标相对组合规模的比例。

## 渲染能力

- 源码组件：table
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：bar、line
- 维度候选：
  - 资产类别（`body[].assetName`）
- 指标候选：
  - 期末持仓市值（`body[].assetEndPrice`）
  - 期末持仓市值占资产净值比（`body[].assetEndRatio`）
  - 期间收益额（`body[].assetIncome`）
  - 期间费后收益额（`body[].assetIncomeAfterFee`）
  - 净值贡献度（`body[].assetIncomeAfterFeeAvgNetRatio`）
  - 收益贡献比例（`body[].assetIncomeAfterFeeRatio`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].assetName | assetName | 资产类别 | 原值直接使用 | 未明确 | table |
| body[].assetEndPrice | assetEndPrice | 期末持仓市值 | 原值直接使用 | 未明确 | table |
| body[].assetEndRatio | assetEndRatio | 期末持仓市值占资产净值比 | 原值 × 100，保留 2 位小数 | % | table |
| body[].assetIncome | assetIncome | 期间收益额 | 原值直接使用 | 元 | table |
| body[].assetIncomeAfterFee | assetIncomeAfterFee | 期间费后收益额 | 原值直接使用 | 元 | table |
| body[].assetIncomeAfterFeeAvgNetRatio | assetIncomeAfterFeeAvgNetRatio | 净值贡献度 | 原值 × 100，保留 2 位小数 | % | table |
| body[].assetIncomeAfterFeeRatio | assetIncomeAfterFeeRatio | 收益贡献比例 | 原值 × 100，保留 2 位小数 | % | table |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "assetCode": "GP",
      "assetName": "股票",
      "assetEndPrice": 10298830.74,
      "assetEndRatio": 0.5628135964713556,
      "assetIncome": 1032109.54,
      "assetIncomeAfterFee": 1001605.73,
      "assetIncomeAfterFeeAvgNetRatio": 0.05676903,
      "assetIncomeAfterFeeRatio": 1.69182078,
      "FCODE": "SM0513",
      "TDATE": "20250131"
    },
    {
      "assetCode": "QH_GZ",
      "assetName": "股指期货",
      "assetEndPrice": 5298830.74,
      "assetEndRatio": 0.2895720942659531,
      "assetIncome": -7760,
      "assetIncomeAfterFee": -8450.54,
      "assetIncomeAfterFeeAvgNetRatio": -0.00047896,
      "assetIncomeAfterFeeRatio": -0.01427388,
      "FCODE": "SM0513",
      "TDATE": "20250131"
    },
    {
      "assetCode": "QH_BT",
      "assetName": "国债期货",
      "assetEndPrice": 0,
      "assetEndRatio": 0,
      "assetIncome": -86000,
      "assetIncomeAfterFee": -86090.3,
      "assetIncomeAfterFeeAvgNetRatio": -0.00487943,
      "assetIncomeAfterFeeRatio": -0.14541586,
      "FCODE": "SM0513",
      "TDATE": "20250131"
    }
  ]
}
```
