---
type: vm-module
moduleId: "productInfo"
title: "产品基本信息"
sqlId: "4475dbc6-a3f9-4e37-bb8b-fda45fda68fc"
templateType: "security-detail"
---

# 产品基本信息

## 模块概览

- 模块说明：展示产品基本信息页面中由VM实际渲染的数据与指标。
- 数据形态：单数据集
- 响应区域：`body`
- 业务规则：
  - 只使用 VM 实际读取并渲染的响应字段；同名字段按完整 JSON 路径区分。
- 指标业务说明：
  - 源码未明确。

## 渲染能力

- 源码组件：table
- 默认视图：table
- 默认视图依据：截图视觉事实
- 可选视图：table、echarts
- 推荐图表：bar、line
- 维度候选：
  - 产品代码（`body[].fundCode`）
  - 产品名称（`body[].fundName`）
  - 成立日期（`body[].fundCreateDate`）
  - 管理人（`body[].glrName`）
  - 投资经理（`body[].fundManage`）
  - 业绩基准（`body[].benchName`）
- 指标候选：
  - 源码未明确

## 字段映射

| JSON 路径 | 原始字段 | 展示名称 | 展示转换 | 展示单位 | 适用视图 |
|---|---|---|---|---|---|
| body[].fundCode | fundCode | 产品代码 | 原值直接使用 | 未明确 | table |
| body[].fundName | fundName | 产品名称 | 原值直接使用 | 未明确 | table |
| body[].fundCreateDate | fundCreateDate | 成立日期 | 原值直接使用 | 未明确 | table |
| body[].glrName | glrName | 管理人 | 原值直接使用 | 未明确 | table |
| body[].fundManage | fundManage | 投资经理 | 原值直接使用 | 未明确 | table |
| body[].benchName | benchName | 业绩基准 | 原值直接使用 | 未明确 | table |

## 示例 JSON 数据

```json
{
  "head": {
    "benchmarks": "1",
    "dataFreq": "1"
  },
  "body": [
    {
      "TDATE": "20220131",
      "FCODE": "SM0513",
      "fundCode": "SM0513",
      "fundName": "度量3期大消费基金",
      "fundCreateDate": "2015-10-09",
      "glrName": "上海度库资产管理合伙企业（有限合伙）",
      "fundManage": "-",
      "benchName": "沪深300指数"
    }
  ]
}
```
