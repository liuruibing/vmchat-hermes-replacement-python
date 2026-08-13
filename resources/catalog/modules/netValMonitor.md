---
type: vm-module
moduleId: "netValMonitor"
title: "净值走势图"
sqlId: "8c757339-83c8-4e0b-adae-76e3cec96a8d"
templateType: "single-product-performance"
---

# 净值走势图

## 模块概览

- 模块说明：展示净值走势图页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`head.constrasCodeNames`、`head.constrasCodeColumn`、`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 单位净值：产品或组合在对应期间的净值指标。
  - 累计单位净值：产品或组合在对应期间的净值指标。
  - 基准：“基准”在该VM页面中的业务展示值。
  - 中证500：“中证500”在该VM页面中的业务展示值。
  - 上证指数：“上证指数”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 日期（`body[].VC_DATE`）
  - 数据频率（`head.dataFreq`）
  - 基准类型（`head.benchmarks`）
  - 基准名称（`head.benchName`）
  - 对比指数名称（`head.constrasCodeNames`）
  - 对比指数字段（`head.constrasCodeColumn`）
- 指标候选：
  - 单位净值（`body[].FNAV`）
  - 累计单位净值（`body[].FCNAV`）
  - 基准（`body[].BYEILD_PROD`）
  - 中证500（`body[].CONTRAS_BYEILD_PROD_1`）
  - 上证指数（`body[].CONTRAS_BYEILD_PROD_2`）

## 数据集绑定

- 响应数据集：`head.constrasCodeNames`
- 响应数据集：`head.constrasCodeColumn`
- 响应数据集：`body`
- 动态列名：`head.constrasCodeNames`
- 动态字段名：`head.constrasCodeColumn`
- 动态取值：`body[][head.constrasCodeColumn]`
- 已解析字段：`body[].CONTRAS_BYEILD_PROD_1`、`body[].CONTRAS_BYEILD_PROD_2`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].VC_DATE | VC_DATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].FNAV | FNAV | 单位净值 | 原值直接使用 | 未明确 | echarts |
| body[].FCNAV | FCNAV | 累计单位净值 | 原值直接使用 | 未明确 | echarts |
| body[].BYEILD_PROD | BYEILD_PROD | 基准 | 原值直接使用 | 未明确 | echarts |
| body[].CONTRAS_BYEILD_PROD_1 | CONTRAS_BYEILD_PROD_1 | 中证500 | 原值直接使用 | 未明确 | echarts |
| body[].CONTRAS_BYEILD_PROD_2 | CONTRAS_BYEILD_PROD_2 | 上证指数 | 原值直接使用 | 未明确 | echarts |
| head.dataFreq | dataFreq | 数据频率 | 原值直接使用 | 未明确 | table、echarts |
| head.benchmarks | benchmarks | 基准类型 | 原值直接使用 | 未明确 | table、echarts |
| head.benchName | benchName | 基准名称 | 原值直接使用 | 未明确 | table、echarts |
| head.constrasCodeNames | constrasCodeNames | 对比指数名称 | 原值直接使用 | 未明确 | table、echarts |
| head.constrasCodeColumn | constrasCodeColumn | 对比指数字段 | 原值直接使用 | 未明确 | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "benchName": "沪深300指数",
    "constrasCodeNames": [
      "中证500",
      "上证指数"
    ],
    "constrasCodeColumn": [
      "CONTRAS_BYEILD_PROD_1",
      "CONTRAS_BYEILD_PROD_2"
    ],
    "dataFreq": "1"
  },
  "body": [
    {
      "VC_DATE": "2022-01-04",
      "TDATE": "20220104",
      "FCODE": "SM0513",
      "FNAV": 0.964,
      "FCNAV": 0.964,
      "BYEILD_PROD": 0.964,
      "CONTRAS_BYEILD_PROD_1": 0.964,
      "CONTRAS_BYEILD_PROD_2": 0.964
    },
    {
      "VC_DATE": "2022-01-05",
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "FNAV": 0.972,
      "FCNAV": 0.972,
      "BYEILD_PROD": 0.9543,
      "CONTRAS_BYEILD_PROD_1": 0.9467,
      "CONTRAS_BYEILD_PROD_2": 0.9541
    },
    {
      "VC_DATE": "2022-01-06",
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "FNAV": 0.97,
      "FCNAV": 0.97,
      "BYEILD_PROD": 0.9445,
      "CONTRAS_BYEILD_PROD_1": 0.9477,
      "CONTRAS_BYEILD_PROD_2": 0.9517
    }
  ]
}
```
