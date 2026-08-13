---
type: vm-module
moduleId: "tenProfitIndustry"
title: "A股前十盈利行业"
sqlId: "fe842e36-d296-432d-8696-d6ec8f2aab03"
templateType: "single-product-performance"
---

# A股前十盈利行业

## 模块概览

- 模块说明：展示A股前十盈利行业页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 本期盈利：统计区间内产生的绝对收益金额。
  - 盈利占比：统计区间内产生的绝对收益金额。
  - 期间仓位：对应资产、分类或指标相对组合规模的比例。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 行业代码（`body[].VC_INDUSTRY_CODE`）
  - 行业名称（`body[].VC_INDUSTRY_NAME`）
- 指标候选：
  - 本期盈利（`body[].F_INCOME`）
  - 盈利占比（`body[].F_YLZB`）
  - 期间仓位（`body[].F_CWZB`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].VC_INDUSTRY_CODE | VC_INDUSTRY_CODE | 行业代码 | 原值直接使用 | 未明确 | table |
| body[].VC_INDUSTRY_NAME | VC_INDUSTRY_NAME | 行业名称 | 原值直接使用 | 未明确 | table、echarts |
| body[].F_INCOME | F_INCOME | 本期盈利 | 保留 2 位小数 | 元 | table |
| body[].F_YLZB | F_YLZB | 盈利占比 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].F_CWZB | F_CWZB | 期间仓位 | 原值 × 100，保留 4 位小数 | % | table |

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
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "VC_FUNDCODE": "SM0513",
      "VC_INDUSTRY_CODE": "110000",
      "VC_INDUSTRY_NAME": "农林牧渔",
      "F_INCOME": 972980,
      "F_YLZB": 0.9101317613516249,
      "F_CWZB": 0.1876917384657767,
      "F_RK": 1
    },
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "VC_FUNDCODE": "SM0513",
      "VC_INDUSTRY_CODE": "420000",
      "VC_INDUSTRY_NAME": "交通运输",
      "F_INCOME": 72900,
      "F_YLZB": 0.068191129727778,
      "F_CWZB": 0,
      "F_RK": 2
    },
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "VC_FUNDCODE": "SM0513",
      "VC_INDUSTRY_CODE": "720000",
      "VC_INDUSTRY_NAME": "传媒",
      "F_INCOME": 15904,
      "F_YLZB": 0.0148767040766884,
      "F_CWZB": 0.0019952075883502,
      "F_RK": 3
    }
  ]
}
```
