---
type: vm-module
moduleId: "swInduStockAnal"
title: "A股行业brinson分解"
sqlId: "2ca96e54-2ca9-4726-8a5d-1d4d976d318d"
templateType: "single-product-performance"
---

# A股行业brinson分解

## 模块概览

- 模块说明：展示A股行业brinson分解页面中由VM实际渲染的数据与指标。
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
    "indexName": "沪深300",
    "industryType": "SWSR"
  },
  "body": [
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "110000",
      "industryFundRatio": 0.7885265913,
      "industryName": "农林牧渔",
      "industryIndexRatio": 0.0642,
      "industryCon": 0.91013176,
      "industryIncome": 972980,
      "industryFundYield": -0.0112553085,
      "industryIndexYield": 0.0144732317,
      "industryExcessYield": -0.0257285402,
      "industryChooseYield": -0.0201482515,
      "industryStrutYield": 0.0097395571,
      "industryInteractionYield": -0.0153198458,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "460000",
      "industryFundRatio": 0.1402899314,
      "industryName": "社会服务",
      "industryIndexRatio": 0,
      "industryCon": -0.10509097,
      "industryIncome": -31480,
      "industryFundYield": -0.0112172196,
      "industryIndexYield": 0,
      "industryExcessYield": -0.0112172196,
      "industryChooseYield": 0,
      "industryStrutYield": 0,
      "industryInteractionYield": -0.0112172196,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "370000",
      "industryFundRatio": 0.0119169208,
      "industryName": "医药生物",
      "industryIndexRatio": 0,
      "industryCon": -0.62185278,
      "industryIncome": -186276,
      "industryFundYield": 0.0003014011,
      "industryIndexYield": 0,
      "industryExcessYield": 0.0003014011,
      "industryChooseYield": 0,
      "industryStrutYield": 0,
      "industryInteractionYield": 0.0003014011,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
