---
type: vm-module
moduleId: "overallFutures"
title: "期货大类归因"
sqlId: "b435f30d-6914-4916-93d6-3c1e8d3e510e"
templateType: "single-product-performance"
---

# 期货大类归因

## 模块概览

- 模块说明：展示期货大类归因页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 期间平均权重(占净值比)：产品或组合在对应期间的净值指标。
  - 净值贡献度：产品或组合在对应期间的净值指标。
  - 收益额：统计区间内产生的绝对收益金额。

## 渲染能力

- 源码组件：table、echarts
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：line、bar
- Y轴推荐：双Y轴
  - 左Y轴候选：收益额
  - 右Y轴候选：权重(占净值比)
- 维度候选：
  - 资产分类（`body[].VC_TYPE_DETAIL_NAME`）
- 指标候选：
  - 期间平均权重(占净值比)（`body[].AVGWEIGHT`）
  - 净值贡献度（`body[].JZGXD`）
  - 收益额（`body[].F_INCOME`）

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].VC_TYPE_DETAIL_NAME | VC_TYPE_DETAIL_NAME | 资产分类 | 原值直接使用 | 未明确 | table、echarts |
| body[].AVGWEIGHT | AVGWEIGHT | 期间平均权重(占净值比) | 原值 × 100，保留 4 位小数 | % | table、echarts |
| body[].JZGXD | JZGXD | 净值贡献度 | 原值 × 100，保留 4 位小数 | % | table |
| body[].F_INCOME | F_INCOME | 收益额 | 保留 2 位小数 | 元 | table、echarts |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "VC_FUNDCODE": "SM0513",
      "VC_TYPE_DETAIL": "QH_GZ",
      "F_INCOME": -841280,
      "VC_TYPE_DETAIL_NAME": "股指期货",
      "AVGWEIGHT": 0,
      "JZGXD": -0.0203970399374104,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    },
    {
      "VC_FUNDCODE": "SM0513",
      "VC_TYPE_DETAIL": "QH_SP",
      "F_INCOME": -2896880,
      "VC_TYPE_DETAIL_NAME": "商品期货",
      "AVGWEIGHT": -0.1853158808979101,
      "JZGXD": -0.070235566106273,
      "FCODE": "SM0513",
      "TDATE": "20220131"
    }
  ]
}
```
