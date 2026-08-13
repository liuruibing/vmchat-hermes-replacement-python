---
type: vm-module
moduleId: "averagePePb"
title: "持仓平均PE/PB时序"
sqlId: "cf8b548d-50d3-4a92-bde5-784bf707733f"
templateType: "single-product-performance"
---

# 持仓平均PE/PB时序

## 模块概览

- 模块说明：展示持仓平均PE/PB时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - PB：市净率估值指标。
  - PE：市盈率估值指标。
  - PS：市销率估值指标。
  - EPS：市销率估值指标。
  - PCF：“PCF”在该VM页面中的业务展示值。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：PE、PB、PS、PCF
  - 右Y轴候选：EPS
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - PB（`body[].F_PB`）
  - PE（`body[].F_PETTM`）
  - PS（`body[].F_PSTTM`）
  - EPS（`body[].F_EPS`）
  - PCF（`body[].F_PCFTTM`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_PB | F_PB | PB | 保留 4 位小数 | 未明确 | echarts |
| body[].F_PETTM | F_PETTM | PE | 保留 4 位小数 | 未明确 | echarts |
| body[].F_PSTTM | F_PSTTM | PS | 保留 4 位小数 | 未明确 | echarts |
| body[].F_EPS | F_EPS | EPS | 保留 4 位小数 | 未明确 | echarts |
| body[].F_PCFTTM | F_PCFTTM | PCF | 保留 4 位小数 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "D_DATE": "2022-01-04 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_PB": 3.09539298,
      "F_PE": 39.91694813,
      "F_PETTM": -14.6501986,
      "F_PS": 3.09565943,
      "F_PSTTM": 2.80081692,
      "F_EPS": -0.4073474,
      "F_PCF": 40.15629423,
      "F_PCFTTM": -95.75996195,
      "TDATE": "20220104",
      "FCODE": "SM0513"
    },
    {
      "D_DATE": "2022-01-05 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_PB": 3.06500682,
      "F_PE": 39.54301091,
      "F_PETTM": -11.56939356,
      "F_PS": 2.84533231,
      "F_PSTTM": 2.65622697,
      "F_EPS": -0.42255535,
      "F_PCF": 36.81006784,
      "F_PCFTTM": -97.3405851,
      "TDATE": "20220105",
      "FCODE": "SM0513"
    },
    {
      "D_DATE": "2022-01-06 00:00:00",
      "VC_FUNDCODE": "SM0513",
      "F_PB": 3.08692405,
      "F_PE": 40.20274327,
      "F_PETTM": -8.34305472,
      "F_PS": 2.81340963,
      "F_PSTTM": 2.61832919,
      "F_EPS": -0.42609475,
      "F_PCF": 36.46099121,
      "F_PCFTTM": -100.27614242,
      "TDATE": "20220106",
      "FCODE": "SM0513"
    }
  ]
}
```
