---
type: vm-module
moduleId: "fixedPositionTiming"
title: "固定收益类持仓时序"
sqlId: "7c426689-80d2-4ce0-83d8-26c45fe5493f"
templateType: "single-product-performance"
---

# 固定收益类持仓时序

## 模块概览

- 模块说明：展示固定收益类持仓时序页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 固定收益类仓位(左)：对应资产、分类或指标相对组合规模的比例。
  - 固定收益类指数(右)：“固定收益类指数(右)”在该VM页面中的业务展示值。
  - 累计单位净值(右)：产品或组合在对应期间的净值指标。

## 渲染能力

- 源码组件：echarts
- 默认视图：echarts
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：固定收益类仓位(左)
  - 右Y轴候选：固定收益类指数(右)、累计单位净值(右)
- 维度候选：
  - 日期（`body[].TDATE`）
- 指标候选：
  - 固定收益类仓位(左)（`body[].F_FIX_RATIO`）
  - 固定收益类指数(右)（`body[].F_INDEX_LJ`）
  - 累计单位净值(右)（`body[].F_905`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].TDATE | TDATE | 日期 | 原值直接使用 | 未明确 | echarts |
| body[].F_FIX_RATIO | F_FIX_RATIO | 固定收益类仓位(左) | 原值 × 100，保留 4 位小数 | % | echarts |
| body[].F_INDEX_LJ | F_INDEX_LJ | 固定收益类指数(右) | 保留 4 位小数 | 未明确 | echarts |
| body[].F_905 | F_905 | 累计单位净值(右) | 原值直接使用 | 未明确 | echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1",
    "fixIndexName": null
  },
  "body": [
    {
      "TDATE": "20220104",
      "FCODE": "SM0513",
      "F_FIX_RATIO": null,
      "F_INDEX_LJ": null,
      "F_905": 0.964
    },
    {
      "TDATE": "20220105",
      "FCODE": "SM0513",
      "F_FIX_RATIO": null,
      "F_INDEX_LJ": null,
      "F_905": 0.972
    },
    {
      "TDATE": "20220106",
      "FCODE": "SM0513",
      "F_FIX_RATIO": null,
      "F_INDEX_LJ": null,
      "F_905": 0.97
    }
  ]
}
```
