---
type: vm-module
moduleId: "hsInduStockVala"
title: "港股行业估值风险"
sqlId: "125bb87f-2c9c-485e-8042-87ce0d60cd30"
templateType: "single-product-performance"
---

# 港股行业估值风险

## 模块概览

- 模块说明：展示港股行业估值风险页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 期间平均投资比例：对应资产、分类或指标相对组合规模的比例。
  - 期间平均基准比例：对应资产、分类或指标相对组合规模的比例。
  - PE(组合)：市盈率估值指标。
  - PE(基准)：市盈率估值指标。
  - PB(组合)：市净率估值指标。
  - PB(基准)：市净率估值指标。
  - ROE(组合)：净资产收益率指标。
  - ROE(基准)：净资产收益率指标。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：PE(左)、PB(左)、ROE(左)
  - 右Y轴候选：期间平均投资比例(右)、期间平均基准比例(右)
- 维度候选：
  - 分组名称（`body[].industryName`）
- 指标候选：
  - 期间平均投资比例（`body[].avgFundIndustryRatio`）
  - 期间平均基准比例（`body[].avgIndexIndustryWeight`）
  - PE(组合)（`body[].fundPE`）
  - PE(基准)（`body[].indexPE`）
  - PB(组合)（`body[].fundPB`）
  - PB(基准)（`body[].indexPB`）
  - ROE(组合)（`body[].fundROE`）
  - ROE(基准)（`body[].indexROE`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].industryName | industryName | 分组名称 | 原值直接使用 | 未明确 | table、echarts |
| body[].avgFundIndustryRatio | avgFundIndustryRatio | 期间平均投资比例 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].avgIndexIndustryWeight | avgIndexIndustryWeight | 期间平均基准比例 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].fundPE | fundPE | PE(组合) | 保留 4 位小数 | 未明确 | table、echarts |
| body[].indexPE | indexPE | PE(基准) | 保留 4 位小数 | 未明确 | table |
| body[].fundPB | fundPB | PB(组合) | 保留 4 位小数 | 未明确 | table、echarts |
| body[].indexPB | indexPB | PB(基准) | 保留 4 位小数 | 未明确 | table |
| body[].fundROE | fundROE | ROE(组合) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].indexROE | indexROE | ROE(基准) | 原值 × 100，保留 4 位小数 | % | table |

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
      "avgFundIndustryRatio": 0.7525229951663938,
      "industryName": "能源业",
      "avgIndexIndustryWeight": 0,
      "fundPE": 8,
      "indexPE": 0,
      "fundPB": 0,
      "indexPB": 0,
      "fundROE": 0,
      "indexROE": 0,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "28",
      "avgFundIndustryRatio": 0.0476190476190476,
      "industryName": "医疗保健业",
      "avgIndexIndustryWeight": 1,
      "fundPE": 56,
      "indexPE": 2,
      "fundPB": 3,
      "indexPB": 4,
      "fundROE": 5,
      "indexROE": 6,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "industryCode": "70",
      "avgFundIndustryRatio": 0.0107819759551905,
      "industryName": "资讯科技业",
      "avgIndexIndustryWeight": 0,
      "fundPE": 0,
      "indexPE": 0,
      "fundPB": 0,
      "indexPB": 0,
      "fundROE": 0,
      "indexROE": 0,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
