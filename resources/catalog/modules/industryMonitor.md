---
type: vm-module
moduleId: "industryMonitor"
title: "A股行业监控"
sqlId: "8c627513-5936-4936-af12-66ad0ea1a947"
templateType: "single-product-performance"
---

# A股行业监控

## 模块概览

- 模块说明：展示A股行业监控页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.timeLineData`、`body.tabData`、`body.tabData[].data`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 基金权重：对应资产、分类或指标相对组合规模的比例。
  - 基准权重：对应资产、分类或指标相对组合规模的比例。
  - 基金收益：“基金收益”在该VM页面中的业务展示值。
  - 基准收益：“基准收益”在该VM页面中的业务展示值。
  - brinson选择：“brinson选择”在该VM页面中的业务展示值。
  - brinson配置：“brinson配置”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 时间区间（`body.tabData[].name`）
  - 行业名称（`body.tabData[].data[].industryName`）
- 指标候选：
  - 基金权重（`body.tabData[].data[].industryFundRatio`）
  - 基准权重（`body.tabData[].data[].industryIndexRatio`）
  - 基金收益（`body.tabData[].data[].industryFundYield`）
  - 基准收益（`body.tabData[].data[].industryIndexYield`）
  - brinson选择（`body.tabData[].data[].industryChooseYield`）
  - brinson配置（`body.tabData[].data[].industryStrutYield`）

## 数据集绑定

- 响应数据集：`body.timeLineData`
- 响应数据集：`body.tabData`
- 响应数据集：`body.tabData[].data`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.tabData[].name | name | 时间区间 | 原值直接使用 | 未明确 | echarts |
| body.tabData[].data[].industryName | industryName | 行业名称 | 原值直接使用 | 未明确 | table、echarts |
| body.tabData[].data[].industryFundRatio | industryFundRatio | 基金权重 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.tabData[].data[].industryIndexRatio | industryIndexRatio | 基准权重 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.tabData[].data[].industryFundYield | industryFundYield | 基金收益 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.tabData[].data[].industryIndexYield | industryIndexYield | 基准收益 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.tabData[].data[].industryChooseYield | industryChooseYield | brinson选择 | 原值 × 100，保留 2 位小数 | % | table、echarts |
| body.tabData[].data[].industryStrutYield | industryStrutYield | brinson配置 | 原值 × 100，保留 2 位小数 | % | table、echarts |

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
  "body": {
    "timeLineData": [
      {
        "VC_NAME": "2022-Q4",
        "D_BEGIN_DATE": "2022-10-01 00:00:00",
        "D_END_DATE": "2022-12-31 00:00:00",
        "RK": 1,
        "FCODE": "SM0513",
        "TDATE": "20221231"
      },
      {
        "VC_NAME": "2022-Q3",
        "D_BEGIN_DATE": "2022-07-01 00:00:00",
        "D_END_DATE": "2022-09-30 00:00:00",
        "RK": 2,
        "FCODE": "SM0513",
        "TDATE": "20221231"
      },
      {
        "VC_NAME": "2022-Q2",
        "D_BEGIN_DATE": "2022-04-01 00:00:00",
        "D_END_DATE": "2022-06-30 00:00:00",
        "RK": 3,
        "FCODE": "SM0513",
        "TDATE": "20221231"
      }
    ],
    "tabData": [
      {
        "rk": 1,
        "name": "2022-Q4",
        "data": null,
        "FCODE": "SM0513",
        "TDATE": "20221231"
      },
      {
        "rk": 4,
        "name": "2022-Q1",
        "data": [
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "110000",
            "industryFundRatio": 0.7885265913,
            "industryName": "农林牧渔",
            "industryIndexRatio": 0.0642,
            "industryCon": 0.96667806,
            "industryIncome": 3756857,
            "industryFundYield": -0.0112553085,
            "industryIndexYield": 0.0144732317,
            "industryExcessYield": -0.0257285402,
            "industryChooseYield": -0.0201482515,
            "industryStrutYield": 0.0097395571,
            "industryInteractionYield": -0.0153198458,
            "TDATE": "20220331",
            "FCODE": "SM0513"
          },
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "460000",
            "industryFundRatio": 0.1402899314,
            "industryName": "社会服务",
            "industryIndexRatio": 0,
            "industryCon": -0.379984,
            "industryIncome": -325291,
            "industryFundYield": -0.0112172196,
            "industryIndexYield": 0,
            "industryExcessYield": -0.0112172196,
            "industryChooseYield": 0,
            "industryStrutYield": 0,
            "industryInteractionYield": -0.0112172196,
            "TDATE": "20220331",
            "FCODE": "SM0513"
          },
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "370000",
            "industryFundRatio": 0.0119169208,
            "industryName": "医药生物",
            "industryIndexRatio": 0,
            "industryCon": -0.13984919,
            "industryIncome": -119720,
            "industryFundYield": 0.0003014011,
            "industryIndexYield": 0,
            "industryExcessYield": 0.0003014011,
            "industryChooseYield": 0,
            "industryStrutYield": 0,
            "industryInteractionYield": 0.0003014011,
            "TDATE": "20220331",
            "FCODE": "SM0513"
          }
        ],
        "FCODE": "SM0513",
        "TDATE": "20221231"
      },
      {
        "rk": 10,
        "name": "2022-全年",
        "data": [
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "110000",
            "industryFundRatio": 0.7885265913,
            "industryName": "农林牧渔",
            "industryIndexRatio": 0.0642,
            "industryCon": 0.70351117,
            "industryIncome": 3745841,
            "industryFundYield": -0.0112553085,
            "industryIndexYield": 0.0144732317,
            "industryExcessYield": -0.0257285402,
            "industryChooseYield": -0.0201482515,
            "industryStrutYield": 0.0097395571,
            "industryInteractionYield": -0.0153198458,
            "TDATE": "20221231",
            "FCODE": "SM0513"
          },
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "460000",
            "industryFundRatio": 0.1402899314,
            "industryName": "社会服务",
            "industryIndexRatio": 0,
            "industryCon": -0.2626344,
            "industryIncome": -325291,
            "industryFundYield": -0.0112172196,
            "industryIndexYield": 0,
            "industryExcessYield": -0.0112172196,
            "industryChooseYield": 0,
            "industryStrutYield": 0,
            "industryInteractionYield": -0.0112172196,
            "TDATE": "20221231",
            "FCODE": "SM0513"
          },
          {
            "VC_FUNDCODE": "SM0513",
            "industryCode": "370000",
            "industryFundRatio": 0.0119169208,
            "industryName": "医药生物",
            "industryIndexRatio": 0,
            "industryCon": -0.17333786,
            "industryIncome": -214691.02,
            "industryFundYield": 0.0003014011,
            "industryIndexYield": 0,
            "industryExcessYield": 0.0003014011,
            "industryChooseYield": 0,
            "industryStrutYield": 0,
            "industryInteractionYield": 0.0003014011,
            "TDATE": "20221231",
            "FCODE": "SM0513"
          }
        ],
        "FCODE": "SM0513",
        "TDATE": "20221231"
      }
    ],
    "bthyData": [
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "110000",
        "industryFundRatio": 0.7885265913,
        "industryName": "农林牧渔",
        "industryIndexRatio": 0.0642,
        "industryCon": 0.70351117,
        "industryIncome": 3745841,
        "industryFundYield": -0.0112553085,
        "industryIndexYield": 0.0144732317,
        "industryExcessYield": -0.0257285402,
        "industryChooseYield": -0.0201482515,
        "industryStrutYield": 0.0097395571,
        "industryInteractionYield": -0.0153198458,
        "TDATE": "20221231",
        "FCODE": "SM0513"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "460000",
        "industryFundRatio": 0.1402899314,
        "industryName": "社会服务",
        "industryIndexRatio": 0,
        "industryCon": -0.2626344,
        "industryIncome": -325291,
        "industryFundYield": -0.0112172196,
        "industryIndexYield": 0,
        "industryExcessYield": -0.0112172196,
        "industryChooseYield": 0,
        "industryStrutYield": 0,
        "industryInteractionYield": -0.0112172196,
        "TDATE": "20221231",
        "FCODE": "SM0513"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "industryCode": "370000",
        "industryFundRatio": 0.0119169208,
        "industryName": "医药生物",
        "industryIndexRatio": 0,
        "industryCon": -0.17333786,
        "industryIncome": -214691.02,
        "industryFundYield": 0.0003014011,
        "industryIndexYield": 0,
        "industryExcessYield": 0.0003014011,
        "industryChooseYield": 0,
        "industryStrutYield": 0,
        "industryInteractionYield": 0.0003014011,
        "TDATE": "20221231",
        "FCODE": "SM0513"
      }
    ],
    "btpieData": [
      {
        "FCODE": "SM0513",
        "TDATE": "20221231",
        "F_PIE_1": 0.9288165227,
        "F_PIE_2": 0.0221912409,
        "F_PIE_3": 0.0000474258
      }
    ]
  }
}
```
