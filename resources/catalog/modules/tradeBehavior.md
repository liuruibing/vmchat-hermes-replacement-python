---
type: vm-module
moduleId: "tradeBehavior"
title: "组合换手率"
sqlId: "b377deb1-e137-44f5-9aa2-b840ec2f6f18"
templateType: "single-product-performance"
---

# 组合换手率

## 模块概览

- 模块说明：展示组合换手率页面中由VM实际渲染的数据与指标。
- 数据形态：多数据集对象
- 响应区域：`body.turnOverData`、`body.dayDataColumn`、`body.dayData`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 报告期间(期间)：“报告期间(期间)”在该VM页面中的业务展示值。
  - 报告期间(年化)：“报告期间(年化)”在该VM页面中的业务展示值。
  - 过去一个月(期间)：“过去一个月(期间)”在该VM页面中的业务展示值。
  - 过去一个月(年化)：“过去一个月(年化)”在该VM页面中的业务展示值。
  - 过去三个月(期间)：“过去三个月(期间)”在该VM页面中的业务展示值。
  - 过去三个月(年化)：“过去三个月(年化)”在该VM页面中的业务展示值。
  - 过去六个月(期间)：“过去六个月(期间)”在该VM页面中的业务展示值。
  - 过去六个月(年化)：“过去六个月(年化)”在该VM页面中的业务展示值。
  - 今年以来(期间)：“今年以来(期间)”在该VM页面中的业务展示值。
  - 今年以来(年化)：“今年以来(年化)”在该VM页面中的业务展示值。
  - 股票：“股票”在该VM页面中的业务展示值。
  - 债券：“债券”在该VM页面中的业务展示值。
  - 公募基金：“公募基金”在该VM页面中的业务展示值。
  - ETF基金：“ETF基金”在该VM页面中的业务展示值。
  - 股指期货(多头)：“股指期货(多头)”在该VM页面中的业务展示值。
  - 股指期货(空头)：“股指期货(空头)”在该VM页面中的业务展示值。
  - 商品期货(多头)：“商品期货(多头)”在该VM页面中的业务展示值。
  - 商品期货(空头)：“商品期货(空头)”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 资产名称（`body.turnOverData[].assetname`）
  - 维度名称（`body.dayDataColumn[].DIM_NME`）
  - 日期（`body.dayData[].tdate`）
  - 列名（`body.dayDataColumn[].columnName`）
- 指标候选：
  - 报告期间(期间)（`body.turnOverData[].f_bt_turnover`）
  - 报告期间(年化)（`body.turnOverData[].f_bt_turnover_year`）
  - 过去一个月(期间)（`body.turnOverData[].f_onemonth_turnover`）
  - 过去一个月(年化)（`body.turnOverData[].f_onemonth_turnover_year`）
  - 过去三个月(期间)（`body.turnOverData[].f_threemonth_turnover`）
  - 过去三个月(年化)（`body.turnOverData[].f_threemonth_turnover_year`）
  - 过去六个月(期间)（`body.turnOverData[].f_sixmonth_turnover`）
  - 过去六个月(年化)（`body.turnOverData[].f_sixmonth_turnover_year`）
  - 今年以来(期间)（`body.turnOverData[].f_thisyear_turnover`）
  - 今年以来(年化)（`body.turnOverData[].f_thisyear_turnover_year`）
  - 股票（`body.dayData[].gpturnover`）
  - 债券（`body.dayData[].zqturnover`）
  - 公募基金（`body.dayData[].jjturnover`）
  - ETF基金（`body.dayData[].jjetfturnover`）
  - 股指期货(多头)（`body.dayData[].gzqhdtturnover`）
  - 股指期货(空头)（`body.dayData[].gzqhktturnover`）
  - 商品期货(多头)（`body.dayData[].spqhdtturnover`）
  - 商品期货(空头)（`body.dayData[].spqhktturnover`）

## 数据集绑定

- 响应数据集：`body.turnOverData`
- 响应数据集：`body.dayDataColumn`
- 响应数据集：`body.dayData`
- 动态列名：`body.dayDataColumn[].DIM_NME`
- 动态字段名：`body.dayDataColumn[].columnName`
- 动态取值：`body.dayData[][columnName]`
- 已解析字段：`body.dayData[].gpturnover`、`body.dayData[].zqturnover`、`body.dayData[].jjturnover`、`body.dayData[].jjetfturnover`、`body.dayData[].gzqhdtturnover`、`body.dayData[].gzqhktturnover`、`body.dayData[].spqhdtturnover`、`body.dayData[].spqhktturnover`

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body.turnOverData[].assetname | assetname | 资产名称 | 原值直接使用 | 未明确 | table、echarts |
| body.turnOverData[].f_bt_turnover | f_bt_turnover | 报告期间(期间) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body.turnOverData[].f_bt_turnover_year | f_bt_turnover_year | 报告期间(年化) | 原值 × 100，保留 4 位小数 | % | table |
| body.turnOverData[].f_onemonth_turnover | f_onemonth_turnover | 过去一个月(期间) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body.turnOverData[].f_onemonth_turnover_year | f_onemonth_turnover_year | 过去一个月(年化) | 原值 × 100，保留 4 位小数 | % | table |
| body.turnOverData[].f_threemonth_turnover | f_threemonth_turnover | 过去三个月(期间) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body.turnOverData[].f_threemonth_turnover_year | f_threemonth_turnover_year | 过去三个月(年化) | 原值 × 100，保留 4 位小数 | % | table |
| body.turnOverData[].f_sixmonth_turnover | f_sixmonth_turnover | 过去六个月(期间) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body.turnOverData[].f_sixmonth_turnover_year | f_sixmonth_turnover_year | 过去六个月(年化) | 原值 × 100，保留 4 位小数 | % | table |
| body.turnOverData[].f_thisyear_turnover | f_thisyear_turnover | 今年以来(期间) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body.turnOverData[].f_thisyear_turnover_year | f_thisyear_turnover_year | 今年以来(年化) | 原值 × 100，保留 4 位小数 | % | table |
| body.dayDataColumn[].DIM_NME | DIM_NME | 维度名称 | 原值直接使用 | 未明确 | echarts |
| body.dayData[].tdate | tdate | 日期 | 原值直接使用 | 未明确 | echarts |
| body.dayDataColumn[].columnName | columnName | 列名 | 原值直接使用 | 未明确 | echarts |
| body.dayData[].gpturnover | gpturnover | 股票 | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].zqturnover | zqturnover | 债券 | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].jjturnover | jjturnover | 公募基金 | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].jjetfturnover | jjetfturnover | ETF基金 | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].gzqhdtturnover | gzqhdtturnover | 股指期货(多头) | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].gzqhktturnover | gzqhktturnover | 股指期货(空头) | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].spqhdtturnover | spqhdtturnover | 商品期货(多头) | 原值 × 100，保留 4 位小数 | % | echarts |
| body.dayData[].spqhktturnover | spqhktturnover | 商品期货(空头) | 原值 × 100，保留 4 位小数 | % | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": {
    "turnOverData": [
      {
        "TDATE": "20220131",
        "FCODE": "SM0513",
        "rk": 1,
        "assetname": "股票",
        "f_bt_turnover": 10.095224860415467,
        "f_onemonth_turnover": 0.5689625099751224,
        "f_threemonth_turnover": 3.385352927632586,
        "f_sixmonth_turnover": 8.552055861636374,
        "f_thisyear_turnover": 0.5689625099751224,
        "f_bt_turnover_year": 9.304942106191024,
        "f_onemonth_turnover_year": 6.699074714223215,
        "f_threemonth_turnover_year": 13.431019767237977,
        "f_sixmonth_turnover_year": 16.964676029876504,
        "f_thisyear_turnover_year": 6.699074714223215
      },
      {
        "TDATE": "20220131",
        "FCODE": "SM0513",
        "rk": 2,
        "assetname": "债券",
        "f_bt_turnover": 0.03592039962169929,
        "f_onemonth_turnover": 0.03879239242565686,
        "f_threemonth_turnover": 0.0406027374478712,
        "f_sixmonth_turnover": 0.046580400874358135,
        "f_thisyear_turnover": 0.03879239242565686,
        "f_bt_turnover_year": 0.033108449146263236,
        "f_onemonth_turnover_year": 0.4567491366246694,
        "f_threemonth_turnover_year": 0.16108694748340205,
        "f_sixmonth_turnover_year": 0.09240133869098217,
        "f_thisyear_turnover_year": 0.4567491366246694
      },
      {
        "TDATE": "20220131",
        "FCODE": "SM0513",
        "rk": 3,
        "assetname": "公募基金",
        "f_bt_turnover": 3.6120956775696396,
        "f_onemonth_turnover": 0.010275813810613309,
        "f_threemonth_turnover": 0.38069914222723683,
        "f_sixmonth_turnover": 2.314166697385609,
        "f_thisyear_turnover": 0.010275813810613309,
        "f_bt_turnover_year": 3.3293306119013093,
        "f_onemonth_turnover_year": 0.12098942067335025,
        "f_threemonth_turnover_year": 1.5103824664450156,
        "f_sixmonth_turnover_year": 4.590602416009496,
        "f_thisyear_turnover_year": 0.12098942067335025
      }
    ],
    "dayDataColumn": [
      {
        "DIM_CDE": "GP",
        "DIM_NME": "股票",
        "F_RK": 1,
        "columnName": "gpturnover",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "ZQ",
        "DIM_NME": "债券",
        "F_RK": 2,
        "columnName": "zqturnover",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      },
      {
        "DIM_CDE": "JJ",
        "DIM_NME": "公募基金",
        "F_RK": 3,
        "columnName": "jjturnover",
        "FCODE": "SM0513",
        "TDATE": "20220131"
      }
    ],
    "dayData": [
      {
        "tdate": "20210104",
        "fcode": "SM0513",
        "gpturnover": 0.03108408077790263,
        "zqturnover": 0,
        "jjturnover": 0.02184172810892212,
        "jjetfturnover": 0.02184172810892212,
        "hgturnover": 0,
        "qhturnover": 0.015460156530587897,
        "qqturnover": 0,
        "gzqhdtturnover": 0,
        "gzqhktturnover": 0.014027373096568482,
        "btqhdtturnover": 0,
        "btqhktturnover": 0,
        "spqhdtturnover": 0.0014327834340194165,
        "spqhktturnover": 0,
        "spzsqhdtturnover": 0,
        "spzsqhktturnover": 0,
        "FCODE": "SM0513",
        "TDATE": "20210104"
      },
      {
        "tdate": "20210105",
        "fcode": "SM0513",
        "gpturnover": 0.13048682951202284,
        "zqturnover": 0,
        "jjturnover": 0.05581969117582127,
        "jjetfturnover": 0.05581969117582127,
        "hgturnover": 0,
        "qhturnover": 0.037748100992703544,
        "qqturnover": 0,
        "gzqhdtturnover": 0,
        "gzqhktturnover": 0.007157628298351441,
        "btqhdtturnover": 0,
        "btqhktturnover": 0,
        "spqhdtturnover": 0.003010306061314136,
        "spqhktturnover": 0.027580166633037962,
        "spzsqhdtturnover": 0,
        "spzsqhktturnover": 0,
        "FCODE": "SM0513",
        "TDATE": "20210105"
      },
      {
        "tdate": "20210106",
        "fcode": "SM0513",
        "gpturnover": 0.011347622157849175,
        "zqturnover": 0,
        "jjturnover": 0,
        "jjetfturnover": 0,
        "hgturnover": 0,
        "qhturnover": 0.03497825264923182,
        "qqturnover": 0,
        "gzqhdtturnover": 0,
        "gzqhktturnover": 0,
        "btqhdtturnover": 0,
        "btqhktturnover": 0,
        "spqhdtturnover": 0.004385493398806534,
        "spqhktturnover": 0.030592759250425285,
        "spzsqhdtturnover": 0,
        "spzsqhktturnover": 0,
        "FCODE": "SM0513",
        "TDATE": "20210106"
      }
    ]
  }
}
```
