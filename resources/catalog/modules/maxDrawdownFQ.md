---
type: vm-module
moduleId: "maxDrawdownFQ"
title: "最大回撤及盈亏占比(复权)"
sqlId: "f6dd749d-df80-41d4-b98f-9ace45fb5544"
templateType: "single-product-performance"
---

# 最大回撤及盈亏占比(复权)

## 模块概览

- 模块说明：展示最大回撤及盈亏占比(复权)页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 最大回撤：“最大回撤”在该VM页面中的业务展示值。
  - 基准最大回撤：“基准最大回撤”在该VM页面中的业务展示值。
  - 最大回撤修复天数：“最大回撤修复天数”在该VM页面中的业务展示值。
  - 平均日收益：“平均日收益”在该VM页面中的业务展示值。
  - 最大日盈利：统计区间内产生的绝对收益金额。
  - 最大日亏损：统计区间内产生的绝对收益金额。
  - 盈利日日均收益：统计区间内产生的绝对收益金额。
  - 亏损日日均收益：统计区间内产生的绝对收益金额。
  - 盈利日占比交易日：统计区间内产生的绝对收益金额。
  - 基准最大回撤修复天数：“基准最大回撤修复天数”在该VM页面中的业务展示值。
  - 基准平均日收益：“基准平均日收益”在该VM页面中的业务展示值。
  - 基准最大日盈利：统计区间内产生的绝对收益金额。
  - 基准最大日亏损：统计区间内产生的绝对收益金额。
  - 基准盈利日日均收益：统计区间内产生的绝对收益金额。
  - 基准亏损日日均收益：统计区间内产生的绝对收益金额。
  - 基准盈利日占比交易日：统计区间内产生的绝对收益金额。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- 维度候选：
  - 期间（`body[].dataAround`）
  - 最大回撤期间(起)（`body[].fq_maxdraw_topdate`）
  - 最大回撤期间(止)（`body[].fq_maxdraw_lowdate`）
  - 基准最大回撤期间(起)（`body[].b_maxdraw_topdate`）
  - 基准最大回撤期间(止)（`body[].b_maxdraw_lowdate`）
  - 数据频率（`head.dataFreq`）
  - 基准类型（`head.benchmarks`）
- 指标候选：
  - 最大回撤（`body[].fq_maxdraw`）
  - 基准最大回撤（`body[].b_maxdraw`）
  - 最大回撤修复天数（`body[].fq_maxdraw_coverworkdays`）
  - 平均日收益（`body[].avg_pyeild`）
  - 最大日盈利（`body[].max_pyeild`）
  - 最大日亏损（`body[].min_pyeild`）
  - 盈利日日均收益（`body[].avg_pyeild_income`）
  - 亏损日日均收益（`body[].avg_pyeild_loss`）
  - 盈利日占比交易日（`body[].pyeild_pup_ratio`）
  - 基准最大回撤修复天数（`body[].b_maxdraw_coverworkdays`）
  - 基准平均日收益（`body[].avg_byeild`）
  - 基准最大日盈利（`body[].max_byeild`）
  - 基准最大日亏损（`body[].min_byeild`）
  - 基准盈利日日均收益（`body[].avg_byeild_income`）
  - 基准亏损日日均收益（`body[].avg_byeild_loss`）
  - 基准盈利日占比交易日（`body[].byeild_pup_ratio`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].dataAround | dataAround | 期间 | 原值直接使用 | 未明确 | table、echarts |
| body[].fq_maxdraw | fq_maxdraw | 最大回撤 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].b_maxdraw | b_maxdraw | 基准最大回撤 | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].fq_maxdraw_topdate | fq_maxdraw_topdate | 最大回撤期间(起) | 原值直接使用 | 未明确 | table |
| body[].fq_maxdraw_lowdate | fq_maxdraw_lowdate | 最大回撤期间(止) | 原值直接使用 | 未明确 | table |
| body[].fq_maxdraw_coverworkdays | fq_maxdraw_coverworkdays | 最大回撤修复天数 | 原值直接使用 | 未明确 | table |
| body[].avg_pyeild | avg_pyeild | 平均日收益 | 原值 × 100 | % | table |
| body[].max_pyeild | max_pyeild | 最大日盈利 | 原值 × 100 | % | table |
| body[].min_pyeild | min_pyeild | 最大日亏损 | 原值 × 100 | % | table |
| body[].avg_pyeild_income | avg_pyeild_income | 盈利日日均收益 | 原值 × 100 | % | table |
| body[].avg_pyeild_loss | avg_pyeild_loss | 亏损日日均收益 | 原值 × 100 | % | table |
| body[].pyeild_pup_ratio | pyeild_pup_ratio | 盈利日占比交易日 | 原值 × 100 | % | table、echarts |
| body[].b_maxdraw_topdate | b_maxdraw_topdate | 基准最大回撤期间(起) | 原值直接使用 | 未明确 | table |
| body[].b_maxdraw_lowdate | b_maxdraw_lowdate | 基准最大回撤期间(止) | 原值直接使用 | 未明确 | table |
| body[].b_maxdraw_coverworkdays | b_maxdraw_coverworkdays | 基准最大回撤修复天数 | 原值直接使用 | 未明确 | table |
| body[].avg_byeild | avg_byeild | 基准平均日收益 | 原值 × 100 | % | table |
| body[].max_byeild | max_byeild | 基准最大日盈利 | 原值 × 100 | % | table |
| body[].min_byeild | min_byeild | 基准最大日亏损 | 原值 × 100 | % | table |
| body[].avg_byeild_income | avg_byeild_income | 基准盈利日日均收益 | 原值 × 100 | % | table |
| body[].avg_byeild_loss | avg_byeild_loss | 基准亏损日日均收益 | 原值 × 100 | % | table |
| body[].byeild_pup_ratio | byeild_pup_ratio | 基准盈利日占比交易日 | 原值 × 100 | % | table |
| head.dataFreq | dataFreq | 数据频率 | 原值直接使用 | 未明确 | table、echarts |
| head.benchmarks | benchmarks | 基准类型 | 原值直接使用 | 未明确 | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "fcode": "SM0513",
      "FCODE": "SM0513",
      "TDATE": "20220131",
      "dataAround": "报告期间",
      "bvar": 0.0001017775665695795,
      "pbcov": 0.00010797554654442324,
      "pyeild": -0.03172866520787776,
      "byeild": -0.0762293091344004,
      "pyeild_year": -0.3479558629238517,
      "byeild_year": -0.6506407325475507,
      "p_byeild": 0.04450064392652264,
      "p_nyeild": -0.032851849624167984,
      "p_nyeild_year": -0.3629558629238401,
      "pstd": 0.030037064052553387,
      "pstd_year": 0.4768236095854453,
      "pstd_pdwon": 0.013921109131409428,
      "pstd_pdwon_year": 0.22099075641539842,
      "pstd_pup": 0.020823463998847918,
      "bstd": 0.010411650120875488,
      "te": 0.028618796882948692,
      "te_year": 0.45430931624491633,
      "maxdraw": -0.15799803729146217,
      "maxdraw_topdate": "2022-01-10",
      "maxdraw_lowdate": "2022-01-27",
      "maxdraw_coverdays": 132,
      "maxdraw_coverworkdays": 84,
      "fq_maxdraw": -0.15799803729146217,
      "fq_maxdraw_topdate": "2022-01-10",
      "fq_maxdraw_lowdate": "2022-01-27",
      "fq_maxdraw_coverdays": 132,
      "fq_maxdraw_coverworkdays": 84,
      "b_maxdraw": -0.07198254349044508,
      "b_maxdraw_topdate": "2022-01-04",
      "b_maxdraw_lowdate": "2022-01-28",
      "b_maxdraw_coverdays": 0,
      "b_maxdraw_coverworkdays": 0,
      "beta": 0.9521626822396199,
      "beta_up": -0.2760225858401368,
      "beta_down": 2.855048891464723,
      "beta_up_down": -3.1310714773048596,
      "alpha": 0.040854038242806076,
      "alpha_year": 0.2708424023865702,
      "sharpe": -0.25091437623022794,
      "sharpe_year": -0.7611952420715853,
      "calmar": -0.20081683134675432,
      "calmar_year": -2.202279654157795,
      "calmar_comp": 0.2816531438579291,
      "omega_year": 0.08285184619616037,
      "kappa_year": -4.80721626259198,
      "sortino": -0.5413887011006275,
      "sortino_year": -1.6424029168061152,
      "sortino_comp": 0.7148476183214162,
      "treynor": -0.03450234947970848,
      "treynor_year": -0.3811910188184619,
      "jensen": 0.04080030811298049,
      "inforate": 0.3567287585802896,
      "inforate_year": 0.666252834358613,
      "capture_up": 0.9837729739811083,
      "capture_down": 0.6481976580765676,
      "capture_up_down": 0.3355753159045407,
      "capture_up_year": 0.9783193867176074,
      "capture_down_year": 0.8090118992182243,
      "win_rate": 0.3157894736842105,
      "win_loss_rate": 1.0705717189767843,
      "recordhigh_count": 2,
      "win_day_rate": 0.42105263157894735,
      "win_week_rate": 0.75,
      "win_month_rate": 1,
      "win_day_rate_b": 0.5789473684210527,
      "win_week_rate_b": 0.75,
      "win_month_rate_b": 1,
      "incomep_total": 2,
      "lossp_total": 5,
      "incomeb_total": 2,
      "lossb_total": 3,
      "skewness": 1.1018660419978625,
      "kurtosis": 0.5093924487978683,
      "fynl": 0.45454545454545453,
      "jgnl": 0.375,
      "q1_pyeild": -0.02628377845662505,
      "q2_pyeild": -0.0022650056625142,
      "q3_pyeild": 0.0100254459694294,
      "avg_pyeild": -0.0012645323433267894,
      "avg_byeild": -0.004113413157894737,
      "max_pyeild": 0.0760295670538543,
      "min_pyeild": -0.0324873096446701,
      "max_byeild": 0.00996404,
      "min_byeild": -0.02262221,
      "pyeild_pup_ratio": 0.3157894736842105,
      "pyeild_pdown_ratio": 0.6842105263157895,
      "byeild_pup_ratio": 0.42105263157894735,
      "avg_byeild_income": 0.00642155125,
      "avg_byeild_loss": -0.011775205454545455,
      "avg_pyeild_income": 0.03438726792151305,
      "avg_pyeild_loss": -0.017719209388637483
    },
    {
      "fcode": "SM0513",
      "FCODE": "SM0513",
      "TDATE": "20220131",
      "dataAround": "近1月",
      "bvar": 0.0001017775665695795,
      "pbcov": 0.00010797554654442324,
      "pyeild": -0.03172866520787776,
      "byeild": -0.0762293091344004,
      "pyeild_year": -0.3479558629238517,
      "byeild_year": -0.6506407325475507,
      "p_byeild": 0.04450064392652264,
      "p_nyeild": -0.032851849624167984,
      "p_nyeild_year": -0.3629558629238401,
      "pstd": 0.030037064052553387,
      "pstd_year": 0.4768236095854453,
      "pstd_pdwon": 0.013921109131409428,
      "pstd_pdwon_year": 0.22099075641539842,
      "pstd_pup": 0.020823463998847918,
      "bstd": 0.010411650120875488,
      "te": 0.028618796882948692,
      "te_year": 0.45430931624491633,
      "maxdraw": -0.15799803729146217,
      "maxdraw_topdate": "2022-01-10",
      "maxdraw_lowdate": "2022-01-27",
      "maxdraw_coverdays": 132,
      "maxdraw_coverworkdays": 84,
      "fq_maxdraw": -0.15799803729146217,
      "fq_maxdraw_topdate": "2022-01-10",
      "fq_maxdraw_lowdate": "2022-01-27",
      "fq_maxdraw_coverdays": 132,
      "fq_maxdraw_coverworkdays": 84,
      "b_maxdraw": -0.07198254349044508,
      "b_maxdraw_topdate": "2022-01-04",
      "b_maxdraw_lowdate": "2022-01-28",
      "b_maxdraw_coverdays": 0,
      "b_maxdraw_coverworkdays": 0,
      "beta": 0.9521626822396199,
      "beta_up": -0.2760225858401368,
      "beta_down": 2.855048891464723,
      "beta_up_down": -3.1310714773048596,
      "alpha": 0.040854038242806076,
      "alpha_year": 0.2708424023865702,
      "sharpe": -0.25091437623022794,
      "sharpe_year": -0.7611952420715853,
      "calmar": -0.20081683134675432,
      "calmar_year": -2.202279654157795,
      "calmar_comp": 0.2816531438579291,
      "omega_year": 0.08285184619616037,
      "kappa_year": -4.80721626259198,
      "sortino": -0.5413887011006275,
      "sortino_year": -1.6424029168061152,
      "sortino_comp": 0.7148476183214162,
      "treynor": -0.03450234947970848,
      "treynor_year": -0.3811910188184619,
      "jensen": 0.04080030811298049,
      "inforate": 0.3567287585802896,
      "inforate_year": 0.666252834358613,
      "capture_up": 0.9837729739811083,
      "capture_down": 0.6481976580765676,
      "capture_up_down": 0.3355753159045407,
      "capture_up_year": 0.9783193867176074,
      "capture_down_year": 0.8090118992182243,
      "win_rate": 0.3157894736842105,
      "win_loss_rate": 1.0705717189767843,
      "recordhigh_count": 2,
      "win_day_rate": 0.42105263157894735,
      "win_week_rate": 0.75,
      "win_month_rate": 1,
      "win_day_rate_b": 0.5789473684210527,
      "win_week_rate_b": 0.75,
      "win_month_rate_b": 1,
      "incomep_total": 2,
      "lossp_total": 5,
      "incomeb_total": 2,
      "lossb_total": 3,
      "skewness": 1.1018660419978625,
      "kurtosis": 0.5093924487978683,
      "fynl": 0.45454545454545453,
      "jgnl": 0.375,
      "q1_pyeild": -0.02628377845662505,
      "q2_pyeild": -0.0022650056625142,
      "q3_pyeild": 0.0100254459694294,
      "avg_pyeild": -0.0012645323433267894,
      "avg_byeild": -0.004113413157894737,
      "max_pyeild": 0.0760295670538543,
      "min_pyeild": -0.0324873096446701,
      "max_byeild": 0.00996404,
      "min_byeild": -0.02262221,
      "pyeild_pup_ratio": 0.3157894736842105,
      "pyeild_pdown_ratio": 0.6842105263157895,
      "byeild_pup_ratio": 0.42105263157894735,
      "avg_byeild_income": 0.00642155125,
      "avg_byeild_loss": -0.011775205454545455,
      "avg_pyeild_income": 0.03438726792151305,
      "avg_pyeild_loss": -0.017719209388637483
    },
    {
      "fcode": "SM0513",
      "FCODE": "SM0513",
      "TDATE": "20220131",
      "dataAround": "近3月",
      "bvar": 0.0001017775665695795,
      "pbcov": 0.00010797554654442324,
      "pyeild": -0.03172866520787776,
      "byeild": -0.0762293091344004,
      "pyeild_year": -0.3479558629238517,
      "byeild_year": -0.6506407325475507,
      "p_byeild": 0.04450064392652264,
      "p_nyeild": -0.032851849624167984,
      "p_nyeild_year": -0.3629558629238401,
      "pstd": 0.030037064052553387,
      "pstd_year": 0.4768236095854453,
      "pstd_pdwon": 0.013921109131409428,
      "pstd_pdwon_year": 0.22099075641539842,
      "pstd_pup": 0.020823463998847918,
      "bstd": 0.010411650120875488,
      "te": 0.028618796882948692,
      "te_year": 0.45430931624491633,
      "maxdraw": -0.15799803729146217,
      "maxdraw_topdate": "2022-01-10",
      "maxdraw_lowdate": "2022-01-27",
      "maxdraw_coverdays": 132,
      "maxdraw_coverworkdays": 84,
      "fq_maxdraw": -0.15799803729146217,
      "fq_maxdraw_topdate": "2022-01-10",
      "fq_maxdraw_lowdate": "2022-01-27",
      "fq_maxdraw_coverdays": 132,
      "fq_maxdraw_coverworkdays": 84,
      "b_maxdraw": -0.07198254349044508,
      "b_maxdraw_topdate": "2022-01-04",
      "b_maxdraw_lowdate": "2022-01-28",
      "b_maxdraw_coverdays": 0,
      "b_maxdraw_coverworkdays": 0,
      "beta": 0.9521626822396199,
      "beta_up": -0.2760225858401368,
      "beta_down": 2.855048891464723,
      "beta_up_down": -3.1310714773048596,
      "alpha": 0.040854038242806076,
      "alpha_year": 0.2708424023865702,
      "sharpe": -0.25091437623022794,
      "sharpe_year": -0.7611952420715853,
      "calmar": -0.20081683134675432,
      "calmar_year": -2.202279654157795,
      "calmar_comp": 0.2816531438579291,
      "omega_year": 0.08285184619616037,
      "kappa_year": -4.80721626259198,
      "sortino": -0.5413887011006275,
      "sortino_year": -1.6424029168061152,
      "sortino_comp": 0.7148476183214162,
      "treynor": -0.03450234947970848,
      "treynor_year": -0.3811910188184619,
      "jensen": 0.04080030811298049,
      "inforate": 0.3567287585802896,
      "inforate_year": 0.666252834358613,
      "capture_up": 0.9837729739811083,
      "capture_down": 0.6481976580765676,
      "capture_up_down": 0.3355753159045407,
      "capture_up_year": 0.9783193867176074,
      "capture_down_year": 0.8090118992182243,
      "win_rate": 0.3157894736842105,
      "win_loss_rate": 1.0705717189767843,
      "recordhigh_count": 2,
      "win_day_rate": 0.42105263157894735,
      "win_week_rate": 0.75,
      "win_month_rate": 1,
      "win_day_rate_b": 0.5789473684210527,
      "win_week_rate_b": 0.75,
      "win_month_rate_b": 1,
      "incomep_total": 2,
      "lossp_total": 5,
      "incomeb_total": 2,
      "lossb_total": 3,
      "skewness": 1.1018660419978625,
      "kurtosis": 0.5093924487978683,
      "fynl": 0.45454545454545453,
      "jgnl": 0.375,
      "q1_pyeild": -0.02628377845662505,
      "q2_pyeild": -0.0022650056625142,
      "q3_pyeild": 0.0100254459694294,
      "avg_pyeild": -0.0012645323433267894,
      "avg_byeild": -0.004113413157894737,
      "max_pyeild": 0.0760295670538543,
      "min_pyeild": -0.0324873096446701,
      "max_byeild": 0.00996404,
      "min_byeild": -0.02262221,
      "pyeild_pup_ratio": 0.3157894736842105,
      "pyeild_pdown_ratio": 0.6842105263157895,
      "byeild_pup_ratio": 0.42105263157894735,
      "avg_byeild_income": 0.00642155125,
      "avg_byeild_loss": -0.011775205454545455,
      "avg_pyeild_income": 0.03438726792151305,
      "avg_pyeild_loss": -0.017719209388637483
    }
  ]
}
```
