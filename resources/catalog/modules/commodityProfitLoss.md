---
type: vm-module
moduleId: "commodityProfitLoss"
title: "期货十大盈利亏损品种"
sqlId: "b0a11b9d-5709-4c27-a0c0-57e859b2d9e8"
templateType: "single-product-performance"
---

# 期货十大盈利亏损品种

## 模块概览

- 模块说明：展示期货十大盈利亏损品种页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.YLData`、`body.KSData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 收益额：统计区间内产生的绝对收益金额。
  - 贡献度：对应资产、分类或指标相对组合规模的比例。
  - 期间平均风险暴露占净值比：产品或组合在对应期间的净值指标。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：占净值比
  - 右Y轴候选：收益额
- 维度候选：
  - 十大盈利品种（`body.YLData[].VC_FUT_DETAIL_NAME`）
  - 多空方向（`body.YLData[].VC_DIRECTION`）
  - 十大亏损品种（`body.KSData[].VC_FUT_DETAIL_NAME`）
  - 多空方向（`body.KSData[].VC_DIRECTION`）
- 指标候选：
  - 收益额（`body.YLData[].F_INCOME`）
  - 贡献度（`body.YLData[].F_GXD`）
  - 期间平均风险暴露占净值比（`body.YLData[].F_JZZB`）
  - 收益额（`body.KSData[].F_INCOME`）
  - 贡献度（`body.KSData[].F_GXD`）
  - 期间平均风险暴露占净值比（`body.KSData[].F_JZZB`）

## 数据集绑定

- 响应数据集：`body.YLData`
- 响应数据集：`body.KSData`

## 父模块查询策略

- 子模块选择：clarify-submodule
- 全部子模块：combined-table
- 合并区分字段：盈亏类型
- 合并统一字段：期货品种
- 默认顺序：topProfitCommodities、topLossCommodities

## 子模块渲染能力

### 期货十大盈利品种 (`topProfitCommodities`)

- 响应区域：`body.YLData`
- 默认视图：table
- 可选视图：table、echarts
- 表格字段：
  - 十大盈利品种（`body.YLData[].VC_FUT_DETAIL_NAME`；原值直接使用）
  - 多空方向（`body.YLData[].VC_DIRECTION`；原值直接使用）
  - 收益额（`body.YLData[].F_INCOME`；原值 ÷ 10000，保留 4 位小数）
  - 贡献度（`body.YLData[].F_GXD`；原值 × 100，保留 2 位小数）
  - 期间平均风险暴露占净值比（`body.YLData[].F_JZZB`；原值 × 100，保留 2 位小数）
- 图表维度：
  - 十大盈利品种（`body.YLData[].VC_FUT_DETAIL_NAME`）
  - 多空方向（`body.YLData[].VC_DIRECTION`）
- 图表指标：
  - 收益额（`body.YLData[].F_INCOME`；原值 ÷ 10000，保留 4 位小数）
  - 贡献度（`body.YLData[].F_GXD`；原值 × 100，保留 2 位小数）
  - 期间平均风险暴露占净值比（`body.YLData[].F_JZZB`；原值 × 100，保留 2 位小数）
- VM 证据：`initTopTenFutProfitTableData`、`initTopTenFutProfitEchartData`

### 期货十大亏损品种 (`topLossCommodities`)

- 响应区域：`body.KSData`
- 默认视图：table
- 可选视图：table、echarts
- 表格字段：
  - 十大亏损品种（`body.KSData[].VC_FUT_DETAIL_NAME`；原值直接使用）
  - 多空方向（`body.KSData[].VC_DIRECTION`；原值直接使用）
  - 收益额（`body.KSData[].F_INCOME`；原值 ÷ 10000，保留 4 位小数）
  - 贡献度（`body.KSData[].F_GXD`；原值 × 100，保留 2 位小数）
  - 期间平均风险暴露占净值比（`body.KSData[].F_JZZB`；原值 × 100，保留 2 位小数）
- 图表维度：
  - 十大亏损品种（`body.KSData[].VC_FUT_DETAIL_NAME`）
  - 多空方向（`body.KSData[].VC_DIRECTION`）
- 图表指标：
  - 收益额（`body.KSData[].F_INCOME`；原值 ÷ 10000，保留 4 位小数）
  - 贡献度（`body.KSData[].F_GXD`；原值 × 100，保留 2 位小数）
  - 期间平均风险暴露占净值比（`body.KSData[].F_JZZB`；原值 × 100，保留 2 位小数）
- VM 证据：`initTopTenFutLossTableData`、`initTopTenFutLossEchartData`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.YLData[].VC_FUT_DETAIL_NAME | VC_FUT_DETAIL_NAME | 十大盈利品种 | 原值直接使用 | 未明确 | table、echarts |
| body.YLData[].VC_DIRECTION | VC_DIRECTION | 多空方向 | 原值直接使用 | 未明确 | table |
| body.YLData[].F_INCOME | F_INCOME | 收益额 | 原值 ÷ 10000，保留 4 位小数 | 万元 | table、echarts |
| body.YLData[].F_GXD | F_GXD | 贡献度 | 原值 × 100，保留 2 位小数 | % | table |
| body.YLData[].F_JZZB | F_JZZB | 期间平均风险暴露占净值比 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.KSData[].VC_FUT_DETAIL_NAME | VC_FUT_DETAIL_NAME | 十大亏损品种 | 原值直接使用 | 未明确 | table、echarts |
| body.KSData[].VC_DIRECTION | VC_DIRECTION | 多空方向 | 原值直接使用 | 未明确 | table |
| body.KSData[].F_INCOME | F_INCOME | 收益额 | 原值 ÷ 10000，保留 4 位小数 | 万元 | table、echarts |
| body.KSData[].F_GXD | F_GXD | 贡献度 | 原值 × 100，保留 2 位小数 | % | table |
| body.KSData[].F_JZZB | F_JZZB | 期间平均风险暴露占净值比 | 原值 × 100，保留 2 位小数 | % | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "YLData": [
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "3010103",
        "VC_FUT_DETAIL_NAME": "上证50指数",
        "VC_DIRECTION": "空头",
        "F_INCOME": 119400,
        "F_GXD": 0.37837375,
        "F_JZZB": -0.00117939,
        "VC_SYMBOL": "3010103",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "1010107",
        "VC_FUT_DETAIL_NAME": "冶金焦炭",
        "VC_DIRECTION": "空头",
        "F_INCOME": 92000,
        "F_GXD": 0.29154427,
        "F_JZZB": 0.04119929,
        "VC_SYMBOL": "1010107",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "3010101",
        "VC_FUT_DETAIL_NAME": "沪深300指数",
        "VC_DIRECTION": "空头",
        "F_INCOME": 42081,
        "F_GXD": 0.13335298,
        "F_JZZB": 0.04058968,
        "VC_SYMBOL": "3010101",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "KSData": [
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "1020105",
        "VC_FUT_DETAIL_NAME": "锡",
        "VC_DIRECTION": "空头",
        "F_INCOME": -2190780,
        "F_GXD": 0.5404368,
        "F_JZZB": -0.20471436,
        "VC_SYMBOL": "1020105",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "3010102",
        "VC_FUT_DETAIL_NAME": "中证500指数",
        "VC_DIRECTION": "多头",
        "F_INCOME": -698420,
        "F_GXD": 0.17229109,
        "F_JZZB": 0.16551565,
        "VC_SYMBOL": "3010102",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_FUT_DETAIL": "1050501",
        "VC_FUT_DETAIL_NAME": "生猪",
        "VC_DIRECTION": "多头",
        "F_INCOME": -416320,
        "F_GXD": 0.1027007,
        "F_JZZB": 0.07659609,
        "VC_SYMBOL": "1050501",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ]
  }
}
```
