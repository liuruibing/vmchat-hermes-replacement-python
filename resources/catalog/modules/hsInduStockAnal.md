---
type: vm-module
moduleId: "hsInduStockAnal"
title: "港股行业brinson分解"
sqlId: "73ab4b7f-b543-4b94-ac6c-50685997d361"
templateType: "single-product-performance"
---

# 港股行业brinson分解

## 模块概览

- 模块说明：展示港股行业brinson分解页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 期间平均权重(占A股)：对应资产、分类或指标相对组合规模的比例。
  - 基准平均权重：对应资产、分类或指标相对组合规模的比例。
  - 贡献度：对应资产、分类或指标相对组合规模的比例。
  - 费后收益额：统计区间内产生的绝对收益金额。
  - 产品收益：“产品收益”在该VM页面中的业务展示值。
  - 基准收益：“基准收益”在该VM页面中的业务展示值。
  - 超额收益：“超额收益”在该VM页面中的业务展示值。
  - 选择收益：“选择收益”在该VM页面中的业务展示值。
  - 配置收益：“配置收益”在该VM页面中的业务展示值。
  - 交互收益：“交互收益”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：配置收益(左)、选择收益(左)、交互收益(左)
  - 右Y轴候选：组合权重(右)、基准权重(右)
- 维度候选：
  - 行业名称（`body[].industryName`）
- 指标候选：
  - 期间平均权重(占A股)（`body[].industryFundRatio`）
  - 基准平均权重（`body[].industryIndexRatio`）
  - 贡献度（`body[].industryCon`）
  - 费后收益额（`body[].industryIncome`）
  - 产品收益（`body[].industryFundYield`）
  - 基准收益（`body[].industryIndexYield`）
  - 超额收益（`body[].industryExcessYield`）
  - 选择收益（`body[].industryChooseYield`）
  - 配置收益（`body[].industryStrutYield`）
  - 交互收益（`body[].industryInteractionYield`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].industryName | industryName | 行业名称 | 原值直接使用 | 未明确 | table、echarts |
| body[].industryFundRatio | industryFundRatio | 期间平均权重(占A股) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].industryIndexRatio | industryIndexRatio | 基准平均权重 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].industryCon | industryCon | 贡献度 | 原值 × 100，保留 4 位小数 | % | table |
| body[].industryIncome | industryIncome | 费后收益额 | 保留 2 位小数 | 元 | table |
| body[].industryFundYield | industryFundYield | 产品收益 | 原值 × 100，保留 4 位小数 | % | table |
| body[].industryIndexYield | industryIndexYield | 基准收益 | 原值 × 100，保留 4 位小数 | % | table |
| body[].industryExcessYield | industryExcessYield | 超额收益 | 原值 × 100，保留 4 位小数 | % | table |
| body[].industryChooseYield | industryChooseYield | 选择收益 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].industryStrutYield | industryStrutYield | 配置收益 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].industryInteractionYield | industryInteractionYield | 交互收益 | 原值 × 100，保留 4 位小数 | % | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "benchName": "沪深300指数",
    "dataFreq": "1",
    "indexName": "恒生指数"
  },
  "body": [
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "00",
      "industryFundRatio": 0.7525229952,
      "industryName": "能源业",
      "industryIndexRatio": 0,
      "industryCon": 0,
      "industryIncome": 0,
      "industryFundYield": 0,
      "industryIndexYield": 0,
      "industryExcessYield": 0,
      "industryChooseYield": 0,
      "industryStrutYield": 0,
      "industryInteractionYield": 0,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "28",
      "industryFundRatio": 0.0476190476,
      "industryName": "医疗保健业",
      "industryIndexRatio": 0,
      "industryCon": 0,
      "industryIncome": 0,
      "industryFundYield": 0,
      "industryIndexYield": 0,
      "industryExcessYield": 0,
      "industryChooseYield": 0,
      "industryStrutYield": 0,
      "industryInteractionYield": 0,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "70",
      "industryFundRatio": 0.010781976,
      "industryName": "资讯科技业",
      "industryIndexRatio": 0,
      "industryCon": 0,
      "industryIncome": 0,
      "industryFundYield": 0,
      "industryIndexYield": 0,
      "industryExcessYield": 0,
      "industryChooseYield": 0,
      "industryStrutYield": 0,
      "industryInteractionYield": 0,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
