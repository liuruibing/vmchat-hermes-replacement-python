---
type: vm-module
moduleId: "riskValue"
title: "VaR"
sqlId: "8abc19f5-f2c9-4cff-8a89-48884270d042"
templateType: "single-product-performance"
---

# VaR

## 模块概览

- 模块说明：展示VaR页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.beta`、`body.varval`、`body.varrate`、`body.esval`、`body.esrate`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - VaR-日(1天)：给定置信水平和持有期下的风险价值指标。
  - VaR-周(5天)：给定置信水平和持有期下的风险价值指标。
  - VaR-月(22天)：给定置信水平和持有期下的风险价值指标。
  - VaR-季(66天)：给定置信水平和持有期下的风险价值指标。
  - VaR-年(252天)：给定置信水平和持有期下的风险价值指标。
  - VaR/净资产-日(1天)：给定置信水平和持有期下的风险价值指标。
  - VaR/净资产-周(5天)：给定置信水平和持有期下的风险价值指标。
  - VaR/净资产-月(22天)：给定置信水平和持有期下的风险价值指标。
  - VaR/净资产-季(66天)：给定置信水平和持有期下的风险价值指标。
  - VaR/净资产-年(252天)：给定置信水平和持有期下的风险价值指标。
  - ES-日(1天)：超过VaR阈值后的条件期望损失指标。
  - ES-周(5天)：超过VaR阈值后的条件期望损失指标。
  - ES-月(22天)：超过VaR阈值后的条件期望损失指标。
  - ES-季(66天)：超过VaR阈值后的条件期望损失指标。
  - ES-年(252天)：超过VaR阈值后的条件期望损失指标。
  - ES/净资产-日(1天)：超过VaR阈值后的条件期望损失指标。
  - ES/净资产-周(5天)：超过VaR阈值后的条件期望损失指标。
  - ES/净资产-月(22天)：超过VaR阈值后的条件期望损失指标。
  - ES/净资产-季(66天)：超过VaR阈值后的条件期望损失指标。
  - ES/净资产-年(252天)：超过VaR阈值后的条件期望损失指标。
  - 组合Beta：“组合Beta”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：table
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：bar、line
- 维度候选：
  - 数据频率（`head.dataFreq`）
- 指标候选：
  - VaR-日(1天)（`body.varval[].YAXISDATA1`）
  - VaR-周(5天)（`body.varval[].YAXISDATA2`）
  - VaR-月(22天)（`body.varval[].YAXISDATA3`）
  - VaR-季(66天)（`body.varval[].YAXISDATA4`）
  - VaR-年(252天)（`body.varval[].YAXISDATA5`）
  - VaR/净资产-日(1天)（`body.varrate[].YAXISDATA1`）
  - VaR/净资产-周(5天)（`body.varrate[].YAXISDATA2`）
  - VaR/净资产-月(22天)（`body.varrate[].YAXISDATA3`）
  - VaR/净资产-季(66天)（`body.varrate[].YAXISDATA4`）
  - VaR/净资产-年(252天)（`body.varrate[].YAXISDATA5`）
  - ES-日(1天)（`body.esval[].YAXISDATA1`）
  - ES-周(5天)（`body.esval[].YAXISDATA2`）
  - ES-月(22天)（`body.esval[].YAXISDATA3`）
  - ES-季(66天)（`body.esval[].YAXISDATA4`）
  - ES-年(252天)（`body.esval[].YAXISDATA5`）
  - ES/净资产-日(1天)（`body.esrate[].YAXISDATA1`）
  - ES/净资产-周(5天)（`body.esrate[].YAXISDATA2`）
  - ES/净资产-月(22天)（`body.esrate[].YAXISDATA3`）
  - ES/净资产-季(66天)（`body.esrate[].YAXISDATA4`）
  - ES/净资产-年(252天)（`body.esrate[].YAXISDATA5`）
  - 组合Beta（`body.beta[].beta`）

## 数据集绑定

- 响应数据集：`body.beta`
- 响应数据集：`body.varval`
- 响应数据集：`body.varrate`
- 响应数据集：`body.esval`
- 响应数据集：`body.esrate`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.varval[].YAXISDATA1 | YAXISDATA1 | VaR-日(1天) | 保留 2 位小数 | 未明确 | table |
| body.varval[].YAXISDATA2 | YAXISDATA2 | VaR-周(5天) | 保留 2 位小数 | 未明确 | table |
| body.varval[].YAXISDATA3 | YAXISDATA3 | VaR-月(22天) | 保留 2 位小数 | 未明确 | table |
| body.varval[].YAXISDATA4 | YAXISDATA4 | VaR-季(66天) | 保留 2 位小数 | 未明确 | table |
| body.varval[].YAXISDATA5 | YAXISDATA5 | VaR-年(252天) | 保留 2 位小数 | 未明确 | table |
| body.varrate[].YAXISDATA1 | YAXISDATA1 | VaR/净资产-日(1天) | 原值 × 100，保留 4 位小数 | % | table |
| body.varrate[].YAXISDATA2 | YAXISDATA2 | VaR/净资产-周(5天) | 原值 × 100，保留 4 位小数 | % | table |
| body.varrate[].YAXISDATA3 | YAXISDATA3 | VaR/净资产-月(22天) | 原值 × 100，保留 4 位小数 | % | table |
| body.varrate[].YAXISDATA4 | YAXISDATA4 | VaR/净资产-季(66天) | 原值 × 100，保留 4 位小数 | % | table |
| body.varrate[].YAXISDATA5 | YAXISDATA5 | VaR/净资产-年(252天) | 原值 × 100，保留 4 位小数 | % | table |
| body.esval[].YAXISDATA1 | YAXISDATA1 | ES-日(1天) | 保留 2 位小数 | 未明确 | table |
| body.esval[].YAXISDATA2 | YAXISDATA2 | ES-周(5天) | 保留 2 位小数 | 未明确 | table |
| body.esval[].YAXISDATA3 | YAXISDATA3 | ES-月(22天) | 保留 2 位小数 | 未明确 | table |
| body.esval[].YAXISDATA4 | YAXISDATA4 | ES-季(66天) | 保留 2 位小数 | 未明确 | table |
| body.esval[].YAXISDATA5 | YAXISDATA5 | ES-年(252天) | 保留 2 位小数 | 未明确 | table |
| body.esrate[].YAXISDATA1 | YAXISDATA1 | ES/净资产-日(1天) | 原值 × 100，保留 4 位小数 | % | table |
| body.esrate[].YAXISDATA2 | YAXISDATA2 | ES/净资产-周(5天) | 原值 × 100，保留 4 位小数 | % | table |
| body.esrate[].YAXISDATA3 | YAXISDATA3 | ES/净资产-月(22天) | 原值 × 100，保留 4 位小数 | % | table |
| body.esrate[].YAXISDATA4 | YAXISDATA4 | ES/净资产-季(66天) | 原值 × 100，保留 4 位小数 | % | table |
| body.esrate[].YAXISDATA5 | YAXISDATA5 | ES/净资产-年(252天) | 原值 × 100，保留 4 位小数 | % | table |
| body.beta[].beta | beta | 组合Beta | 保留 4 位小数 | 未明确 | table |
| head.dataFreq | dataFreq | 数据频率 | 原值直接使用 | 未明确 | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "beta": [
      {
        "TDATE": "20220131",
        "FCODE": "SM0513",
        "beta": 0.9521626817289943
      }
    ],
    "varval": [
      {
        "zxd": 90,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 152.36,
        "YAXISDATA2": 340.68,
        "YAXISDATA3": 714.62,
        "YAXISDATA4": 1237.75,
        "YAXISDATA5": 2418.59
      },
      {
        "zxd": 95,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 195.55,
        "YAXISDATA2": 437.26,
        "YAXISDATA3": 917.2,
        "YAXISDATA4": 1588.64,
        "YAXISDATA5": 3104.22
      },
      {
        "zxd": 99,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 276.57,
        "YAXISDATA2": 618.42,
        "YAXISDATA3": 1297.21,
        "YAXISDATA4": 2246.84,
        "YAXISDATA5": 4390.36
      }
    ],
    "varrate": [
      {
        "zxd": 90,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 0.0390306571,
        "YAXISDATA2": 0.0872752024,
        "YAXISDATA3": 0.183070009,
        "YAXISDATA4": 0.3170865569,
        "YAXISDATA5": 0.6195924725
      },
      {
        "zxd": 95,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 0.050095306,
        "YAXISDATA2": 0.1120165096,
        "YAXISDATA3": 0.2349678127,
        "YAXISDATA4": 0.4069761898,
        "YAXISDATA5": 0.7952383291
      },
      {
        "zxd": 99,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": 0.0708507473,
        "YAXISDATA2": 0.1584270873,
        "YAXISDATA3": 0.332319462,
        "YAXISDATA4": 0.5755941925,
        "YAXISDATA5": 1.1247207461
      }
    ],
    "esval": [
      {
        "zxd": 90,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -205.66,
        "YAXISDATA2": -459.86,
        "YAXISDATA3": -964.62,
        "YAXISDATA4": -1670.76,
        "YAXISDATA5": -3264.7
      },
      {
        "zxd": 95,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -241.77,
        "YAXISDATA2": -540.61,
        "YAXISDATA3": -1134,
        "YAXISDATA4": -1964.15,
        "YAXISDATA5": -3837.98
      },
      {
        "zxd": 99,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -312.71,
        "YAXISDATA2": -699.23,
        "YAXISDATA3": -1466.72,
        "YAXISDATA4": -2540.44,
        "YAXISDATA5": -4964.06
      }
    ],
    "esrate": [
      {
        "zxd": 90,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -0.0526850103,
        "YAXISDATA2": -0.1178072645,
        "YAXISDATA3": -0.2471146028,
        "YAXISDATA4": -0.4280150474,
        "YAXISDATA5": -0.8363486112
      },
      {
        "zxd": 95,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -0.0619364261,
        "YAXISDATA2": -0.138494059,
        "YAXISDATA3": -0.290507589,
        "YAXISDATA4": -0.5031739041,
        "YAXISDATA5": -0.983210283
      },
      {
        "zxd": 99,
        "FCODE": "SM0513",
        "TDATE": "20220131",
        "YAXISDATA1": -0.0801088498,
        "YAXISDATA2": -0.1791288338,
        "YAXISDATA3": -0.3757438117,
        "YAXISDATA4": -0.6508073726,
        "YAXISDATA5": -1.2716885668
      }
    ]
  }
}
```
