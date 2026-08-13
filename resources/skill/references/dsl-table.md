# Table DSL 规范

本文档只描述如何根据模块 MD 和用户问题生成 Table DSL，不描述如何编写模块 MD。

## 适用场景

- 列表
- 截面
- 排名
- 个券明细
- 用户明确要求“表格”“明细”“列表”

## view 结构

```json
{
  "type": "table",
  "title": "表格标题",
  "columns": [
    {
      "field": "securityName",
      "label": "证券名称",
      "format": {
        "type": "text",
        "nullValue": "-"
      }
    }
  ]
}
```

## columns 规则

| 字段 | 必填 | 说明 |
|---|---|---|
| `field` | 是 | transform 输出字段 |
| `label` | 是 | 前端展示名称，来自模块 MD 的字段映射 |
| `unit` | 条件必填 | 模块 MD 的展示单位不是“未明确”时必须原样提供 |
| `format` | 条件必填 | 模块 MD 存在数值转换时必须提供并与转换一致 |

## format 规则

`format` 负责前端展示格式化。transform 中保持 number 类型，不得转成字符串。

具体格式类型、展示转换映射、百分比换算规则以 [DSL 通用规范的展示格式化规则](dsl-spec.md#展示格式化规则) 为唯一准则。不要在本文档中另行推导 format 映射。

禁止：

- `columns[].requestId`
- `dataAlignment`
- `rowKey`

## 生成规则

- `columns[].label` 必须使用对应行的"展示名称"，不得附加单位后缀。例如 MD 展示名称为"收益额"、单位为"万元"时，`label` 应为 `"收益额"`、`unit` 应为 `"万元"`，绝不可把 `label` 写成 `"收益额(万元)"`。同理，百分比单位的展示名称不加 `(%)` 后缀。
- 示例 JSON 只用于 transform 确认响应结构和原始取值。示例 JSON 中存在、但字段映射表中不存在的字段不得进入 `columns`。
- 表格列优先覆盖用户问题中点名的字段；用户要求“全部字段”时，只输出字段映射表中的稳定业务字段。
- 单模块表格按字段映射表的先后顺序排列所选列。不得因为示例 JSON 中存在日期、代码或其他字段而自行补列或调整顺序。
- 百分比、金额、小数等展示格式必须写在 `columns[].format`；数值换算和 format 结构按 [DSL 通用规范的展示格式化规则](dsl-spec.md#展示格式化规则) 生成。
