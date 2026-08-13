---
type: vm-module
moduleId: "bondConcentrate"
title: "债券持仓集中度"
sqlId: "ec66b44b-5e8b-4057-8046-79dd6798eee7"
templateType: "security-detail"
---

# 债券持仓集中度

## 模块概览

- 模块说明：展示债券持仓集中度页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.topNData`、`body.tabData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 持仓比例：对应资产、分类或指标相对组合规模的比例。
  - 持仓市值：“持仓市值”在该VM页面中的业务展示值。
  - 持仓占流通股本比例：对应资产、分类或指标相对组合规模的比例。
  - 最大重仓债：“最大重仓债”在该VM页面中的业务展示值。
  - 前两大重仓债：“前两大重仓债”在该VM页面中的业务展示值。
  - 前三大重仓债：“前三大重仓债”在该VM页面中的业务展示值。
  - 前五大重仓债：“前五大重仓债”在该VM页面中的业务展示值。
  - 前十大重仓债：“前十大重仓债”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 债券代码（`body.tabData[].VC_SYMBOL`）
  - 债券名称（`body.tabData[].VC_NAME`）
- 指标候选：
  - 持仓比例（`body.tabData[].F_CCZB`）
  - 持仓市值（`body.tabData[].F_PRICE`）
  - 持仓占流通股本比例（`body.tabData[].F_LTZB`）
  - 最大重仓债（`body.topNData[].F_TOP_1_RATIO`）
  - 前两大重仓债（`body.topNData[].F_TOP_2_RATIO`）
  - 前三大重仓债（`body.topNData[].F_TOP_3_RATIO`）
  - 前五大重仓债（`body.topNData[].F_TOP_5_RATIO`）
  - 前十大重仓债（`body.topNData[].F_TOP_10_RATIO`）

## 数据集绑定

- 响应数据集：`body.topNData`
- 响应数据集：`body.tabData`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.tabData[].VC_SYMBOL | VC_SYMBOL | 债券代码 | 原值直接使用 | 未明确 | table |
| body.tabData[].VC_NAME | VC_NAME | 债券名称 | 原值直接使用 | 未明确 | table |
| body.tabData[].F_CCZB | F_CCZB | 持仓比例 | 原值 × 100，保留 4 位小数 | % | table |
| body.tabData[].F_PRICE | F_PRICE | 持仓市值 | 原值 ÷ 10000，保留 2 位小数 | 万元 | table |
| body.tabData[].F_LTZB | F_LTZB | 持仓占流通股本比例 | 原值 × 100，保留 4 位小数 | % | table |
| body.topNData[].F_TOP_1_RATIO | F_TOP_1_RATIO | 最大重仓债 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.topNData[].F_TOP_2_RATIO | F_TOP_2_RATIO | 前两大重仓债 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.topNData[].F_TOP_3_RATIO | F_TOP_3_RATIO | 前三大重仓债 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.topNData[].F_TOP_5_RATIO | F_TOP_5_RATIO | 前五大重仓债 | 原值 × 100，保留 2 位小数 | % | echarts |
| body.topNData[].F_TOP_10_RATIO | F_TOP_10_RATIO | 前十大重仓债 | 原值 × 100，保留 2 位小数 | % | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "topNData": [
      {
        "D_DATE": "2022-01-28 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "F_701A": 39035151.39,
        "F_103A": 0,
        "F_TOP_1_PRICE": 377588.4,
        "F_TOP_2_PRICE": 634418.8,
        "F_TOP_3_PRICE": 870493.3,
        "F_TOP_5_PRICE": 1308149.5,
        "F_TOP_10_PRICE": 2199126.55,
        "TDATE": "20220131",
        "F_TOP_1_RATIO": 0.0096730353682381,
        "F_TOP_2_RATIO": 0.0162525000521075,
        "F_TOP_3_RATIO": 0.0223002414235033,
        "F_TOP_5_RATIO": 0.0335120898323228,
        "F_TOP_10_RATIO": 0.0563370826470874,
        "FCODE": "SM0513"
      }
    ],
    "tabData": [
      {
        "D_DATE": "2022-01-28 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "VC_SYMBOL": "2****2",
        "VC_NAME": "2****2",
        "F_AMOUNT": 2000000,
        "F_PRICE": 199768727.59,
        "F_CUR_NUMBER": 550000000,
        "F_CCZB": 5.117662426721794,
        "F_LTZB": 0.0036363636363636,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "D_DATE": "2022-01-28 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "VC_SYMBOL": "1****4",
        "VC_NAME": "2****1",
        "F_AMOUNT": 1500000,
        "F_PRICE": 150000457.95,
        "F_CUR_NUMBER": 20000000,
        "F_CCZB": 3.842702093078779,
        "F_LTZB": 0.075,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "D_DATE": "2022-01-28 00:00:00",
        "VC_FUNDCODE": "SM0513",
        "VC_SYMBOL": "2****1",
        "VC_NAME": "2****1",
        "F_AMOUNT": 1500000,
        "F_PRICE": 149845115.16,
        "F_CUR_NUMBER": 678200000,
        "F_CCZB": 3.838722531466529,
        "F_LTZB": 0.002211736950752,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ]
  }
}
```
