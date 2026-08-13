---
type: vm-module
moduleId: "campisiBondAnal"
title: "Campisi债券绩效归因"
sqlId: "95b8781e-312c-4c58-9d45-c3c7e63e2412"
templateType: "single-product-performance"
---

# Campisi债券绩效归因

## 模块概览

- 模块说明：展示Campisi债券绩效归因页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.tabData`、`body.totalData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 平均权重：对应资产、分类或指标相对组合规模的比例。
  - 收益金额：“收益金额”在该VM页面中的业务展示值。
  - 收益率：统计区间内收益相对期初或投入规模的比例。
  - 利息影响：“利息影响”在该VM页面中的业务展示值。
  - 国债影响：“国债影响”在该VM页面中的业务展示值。
  - 国债平移：“国债平移”在该VM页面中的业务展示值。
  - 国债扭曲：“国债扭曲”在该VM页面中的业务展示值。
  - 利差影响：“利差影响”在该VM页面中的业务展示值。
  - 利差平移：“利差平移”在该VM页面中的业务展示值。
  - 利差扭曲：“利差扭曲”在该VM页面中的业务展示值。
  - 证券选择：“证券选择”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：table
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：bar、line
- 维度候选：
  - 品种类别（`body.tabData[].STYLENAME`）
  - 品种类别（`body.totalData[].STYLENAME`）
- 指标候选：
  - 平均权重（`body.tabData[].WEIGHT`）
  - 收益金额（`body.tabData[].INCOME`）
  - 收益率（`body.tabData[].YIELDRATE`）
  - 利息影响（`body.tabData[].INTEREST`）
  - 国债影响（`body.tabData[].INFLUENCE`）
  - 国债平移（`body.tabData[].INFLUENCE_TR`）
  - 国债扭曲（`body.tabData[].INFLUENCE_DI`）
  - 利差影响（`body.tabData[].SPREAD`）
  - 利差平移（`body.tabData[].SPREAD_TR`）
  - 利差扭曲（`body.tabData[].SPREAD_DI`）
  - 证券选择（`body.tabData[].CHOOSEYIELD`）
  - 收益金额（`body.totalData[].INCOME`）
  - 收益率（`body.totalData[].YIELDRATE`）
  - 利息影响（`body.totalData[].INTEREST`）
  - 国债影响（`body.totalData[].INFLUENCE`）
  - 国债平移（`body.totalData[].INFLUENCE_TR`）
  - 国债扭曲（`body.totalData[].INFLUENCE_DI`）
  - 利差影响（`body.totalData[].SPREAD`）
  - 利差平移（`body.totalData[].SPREAD_TR`）
  - 利差扭曲（`body.totalData[].SPREAD_DI`）
  - 证券选择（`body.totalData[].CHOOSEYIELD`）

## 数据集绑定

- 响应数据集：`body.tabData`
- 响应数据集：`body.totalData`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.tabData[].STYLENAME | STYLENAME | 品种类别 | 原值直接使用 | 未明确 | table |
| body.tabData[].WEIGHT | WEIGHT | 平均权重 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].INCOME | INCOME | 收益金额 | 原值 ÷ 10000，保留 4 位小数 | 万元 | table |
| body.tabData[].YIELDRATE | YIELDRATE | 收益率 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].INTEREST | INTEREST | 利息影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].INFLUENCE | INFLUENCE | 国债影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].INFLUENCE_TR | INFLUENCE_TR | 国债平移 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].INFLUENCE_DI | INFLUENCE_DI | 国债扭曲 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].SPREAD | SPREAD | 利差影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].SPREAD_TR | SPREAD_TR | 利差平移 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].SPREAD_DI | SPREAD_DI | 利差扭曲 | 原值 × 100，保留 2 位小数 | % | table |
| body.tabData[].CHOOSEYIELD | CHOOSEYIELD | 证券选择 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].STYLENAME | STYLENAME | 品种类别 | 原值直接使用 | 未明确 | table |
| body.totalData[].INCOME | INCOME | 收益金额 | 原值 ÷ 10000，保留 4 位小数 | 万元 | table |
| body.totalData[].YIELDRATE | YIELDRATE | 收益率 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].INTEREST | INTEREST | 利息影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].INFLUENCE | INFLUENCE | 国债影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].INFLUENCE_TR | INFLUENCE_TR | 国债平移 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].INFLUENCE_DI | INFLUENCE_DI | 国债扭曲 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].SPREAD | SPREAD | 利差影响 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].SPREAD_TR | SPREAD_TR | 利差平移 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].SPREAD_DI | SPREAD_DI | 利差扭曲 | 原值 × 100，保留 2 位小数 | % | table |
| body.totalData[].CHOOSEYIELD | CHOOSEYIELD | 证券选择 | 原值 × 100，保留 2 位小数 | % | table |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "tabData": [
      {
        "VC_FUNDCODE": "SM0513",
        "VC_STYLE_CODE": "ZQ_GZXQ",
        "WEIGHT": 0.00407568,
        "STYLENAME": "国债",
        "RK": 1,
        "INCOME": 4132.44,
        "YIELDRATE": 0,
        "INTEREST": 0,
        "INFLUENCE": 0,
        "INFLUENCE_TR": 0,
        "INFLUENCE_DI": 0,
        "SPREAD": 0,
        "SPREAD_TR": 0,
        "SPREAD_DI": 0,
        "CHOOSEYIELD": 0,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_STYLE_CODE": "ZQ_JRZ_ZC",
        "WEIGHT": 0.08103083,
        "STYLENAME": "政策性金融债",
        "RK": 2,
        "INCOME": 194088.89,
        "YIELDRATE": 0,
        "INTEREST": 0,
        "INFLUENCE": 0,
        "INFLUENCE_TR": 0,
        "INFLUENCE_DI": 0,
        "SPREAD": 0,
        "SPREAD_TR": 0,
        "SPREAD_DI": 0,
        "CHOOSEYIELD": 0,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "VC_FUNDCODE": "SM0513",
        "VC_STYLE_CODE": "ZQ_JRZ",
        "WEIGHT": 0.1343362,
        "STYLENAME": "金融债",
        "RK": 5,
        "INCOME": 197095.9,
        "YIELDRATE": 0.0036261592316039,
        "INTEREST": 0.0029438337847194,
        "INFLUENCE": 0.0083626993204668,
        "INFLUENCE_TR": 0.0022974678849634,
        "INFLUENCE_DI": 0.0060652314355034,
        "SPREAD": -0.0060107038889821,
        "SPREAD_TR": -0.0013760522080619,
        "SPREAD_DI": -0.0046346516809202,
        "CHOOSEYIELD": -0.0016696699846002,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "totalData": [
      {
        "VC_FUNDCODE": "SM0513",
        "STYLENAME": "合计",
        "INCOME": 4464091.13,
        "YIELDRATE": -0.02897892,
        "INTEREST": 0.01081859,
        "INFLUENCE": 0.01979567,
        "INFLUENCE_TR": 0.0062982,
        "INFLUENCE_DI": 0.01349747,
        "SPREAD": -0.00979328,
        "SPREAD_TR": -0.00289517,
        "SPREAD_DI": -0.00689812,
        "CHOOSEYIELD": -0.04979989,
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ]
  }
}
```
