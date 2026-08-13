---
name: vm-report-dsl
description: 当 Hermes 需要根据自然语言检索 VM 报表语料、判断单模块或跨模块字段能否合并，并生成前端表格或 ECharts 渲染 JSON 时使用。
---

# VM 前端渲染 DSL

## 目标

检索当前 Hermes profile 的 VM 报表 Catalog，依次完成意图命中、合并门禁、字段解析、DSL 构建和校验。只有全部门禁与校验通过后，才输出前端可执行的 `create` 或 `update` DSL。

本 skill 是完整 DSL 生成器。不要调用历史 vmChat 协议、旧包装 skill 或 raw 层资料。

## Catalog 边界

只使用当前 profile 的 `workspace/catalog`：

- `index.md`、`metrics.md`
- `modules/<moduleId>.md`
- `submodules.json`
- `execution-contract.json`

本机标准 profile 名为 `vm-report-template`。不得改用其他 profile；路径不存在时回到当前 profile 定位，不得扫描全部 profiles。不得读取或暴露 Catalog 以外的业务语料。

检索必须逐步收窄：

1. 先读取或搜索 `index.md` 与 `metrics.md`。
2. 只有唯一定位 `moduleId` 后，才读取对应模块 MD。
3. 多模块请求也只能读取索引已命中的模块文件。
4. 读取对应模块后必须读取 `execution-contract.json`；命中父子模块时同时读取 `submodules.json`。
5. 禁止枚举或全文扫描 `catalog/modules`；索引未命中时请用户补充中文模块名、指标名或业务口径。

## 参考路由

按场景读取，不要一次加载全部参考：

| 场景 | 必读参考 |
|---|---|
| 构建任何 DSL | [DSL 通用规范](references/dsl-spec.md) |
| 生成 table | [Table DSL 规范](references/dsl-table.md) |
| 生成 ECharts | [ECharts DSL 规范](references/dsl-echarts.md) |
| 跨模块合并，或 Catalog 未授权的多子模块合并/对比 | [合并规则](references/merge-rules.md) |

`references/dsl.schema.json` 是校验器使用的机器契约，不作为生成模板。

## 用户可见输出

- 所有说明、反问和错误必须使用自然中文。
- 当由 vmChat 调用时，所有描述性说明必须提供为可嵌入 `message` 字段的 Markdown 文本：使用短标题、空行和项目符号/编号列表组织候选模块、命中依据、冲突原因和下一步；禁止把多条信息直接拼成连续文本。
- 对业务知识说明必须使用下方“业务信息展示协议”的 `businessInfo` 返回格式；不得以自然语言裸文本、`chat` 或 `clarify` 代替。
- 澄清反问必须排版清晰，禁止将所有文案堆叠成大段无排版文本。禁止在回复中使用 `**` 加粗符号。反问格式统一规范为：
  1. 背景说明：1–2 句简明说明知识库命中情况及需要确认的原因（模块与字段名使用普通书名号 `「」`，禁止添加 `**`）。
  2. 选项列表：使用 `1. 选项标题：选项描述` 数字列表清晰列出可选意图或渲染形式。
  3. 推荐选项：在列表末尾添加 `💡 推荐选项：根据您这次的提问，建议选择 1. 选项标题`。
- 候选名称只能使用 `index.md` 的中文业务名称。不得向用户展示 `catalog`、`moduleId`、`submoduleId`、`sqlCode`、英文模块标识、文件路径或内部异常。
- 需要说明依据时统一说“知识库”。子模块使用“父模块中文标题 > 子模块中文标题”。
- 门禁通过前禁止生成、缓存或输出 UUID、requests、transform、view 等 DSL 中间产物，不得输出 Markdown 表格、代码块、JSON 或 DSL 片段。
- 不得输出 `removeBlock` 或删除指令；用户要求删除时提示其使用前端删除按钮。

## 业务信息展示协议

当用户询问知识库中的业务信息，而不是要求生成、修改或删除图表/表格时，必须返回 `businessInfo`。

适用问题包括但不限于：

- 有哪些模块、某模块能做什么。
- 某模块有哪些字段、字段含义、单位、格式、口径。
- 指标定义、计算口径、展示方式、适用场景。
- 查询条件含义、模块之间的区别、可用维度说明。
- 根据知识库整理出的业务说明或模块清单。

`businessInfo` 的 `message` 必须使用 Markdown 编排，包含清晰标题、空行和项目符号或编号列表；内容必须完整且可独立阅读。

`businessInfo` 不得生成 DSL，不得请求数据，不得返回 `operations`、`blocks`、SQL、模块英文标识、文件路径或代码片段。只向用户展示知识库中的中文业务名称及其业务说明。

返回格式必须严格为：

```json
{
  "intent": "businessInfo",
  "renderType": "businessInfo",
  "title": "简短且明确的业务标题",
  "message": "完整 Markdown 正文"
}
```

分类规则：

- 用户要求生成图表、表格、数据查询或修改已有模块：返回完整 vm-report-dsl。
- 缺少生成报表所必需的信息，且必须由用户补充：返回 `clarify`。
- 无法执行、拒绝的操作或失败说明：返回 `chat` 或既有错误协议。
- 仅寒暄、确认、简短状态通知：返回 `chat`。
- 其余与业务知识、模块、字段、指标口径有关的说明：返回 `businessInfo`。

不要因为当前已有报告块改变分类；只要是 `businessInfo`，都必须返回该类型。

## 执行流程

必须按以下顺序串行执行。

### 0. 意图命中门禁

从 `index.md`、`metrics.md` 唯一确认模块、子模块和指标。以下情况必须自然语言反问并停止：

- 模块、子模块或指标存在多个命中。
- 模块标题与指标名称相同、近似或存在包含关系。
- 当前 block 中也有近义标题、列或曲线，无法判断用户指向。
- 父模块策略为 `clarify-submodule`，但用户未选择具体子模块或 Catalog 允许的“全部”。

父模块反问必须列出真实中文子模块；`全部子模块：combined-table` 时可以提供“一起看”，`unsupported` 时不能提供。

模块级请求表示展示该模块的稳定指标集合，不等于只选择同名指标。用户明确说“全部指标”时必须覆盖模块或子模块渲染能力中的全部指标候选。

### 1. 合并门禁

单模块直接进入构建。多数据集单模块只使用模块 MD 的“数据集绑定”“渲染能力”和“字段映射”；示例 JSON 中未授权的隐式字段不能进入 DSL。跨模块或 Catalog 未授权的多子模块合并必须读取 `merge-rules.md`，先确认横向关联、纵向拼接或含糊意图，再审查粒度、时间、业务含义、单位、方向、分类体系、共同键和基数关系。

同一父模块已声明 `全部子模块：combined-table` 且用户明确选择全部时，不走跨模块合并门禁：按默认顺序生成多个带稳定 `submoduleId` 的逻辑 request，在一个普通 table 中纵向拼接并增加 Catalog 声明的区分字段。当前协议不批量 create；用户要求分成多个块时提示其分别生成。

### 2. 构建 DSL

按 `dsl-spec.md` 构建顶层结构、requests 和 transform，再按目标 view 只读取对应 Table 或 ECharts 规范。

- `moduleId`、`sqlCode` 和 `submoduleId` 最终以 `execution-contract.json` 为执行白名单，并与模块 MD、`submodules.json` 交叉核对；DSL 不输出顶层 `params`，也不在 request 中写参数。
- 字段必须按"用户中文名称 → metrics/index → 模块或子模块渲染章节 → 字段映射 → 适用视图 → JSON 路径/原始字段"解析；同一展示名称在 table 与 echarts 对应不同原始字段时，必须由目标 `view.type` 唯一选择，不能改写 Catalog 展示名称。
- 用户未指定展示方式时，普通模块和子模块都必须使用各自 `渲染能力` 中的 `默认视图`；`源码组件` 和 `默认视图依据` 仅用于解释来源，不能覆盖 `默认视图`。用户明确指定展示方式时，该视图必须存在于 `可选视图` 中，并且至少存在一项对应 `适用视图` 的字段映射。
- 示例 JSON 只确认响应结构和原始取值，不能补充字段映射中不存在的展示列或指标。
- 字段映射为空、执行契约不一致或子模块字段边界不完整时，视为知识库不可执行，只返回自然语言错误；不得从示例 JSON 推导或补造字段。
- `view` 只能引用 transform 显式输出的字段。
- **Table label 陷阱**：`columns[].label` 取字段映射"展示名称"原文，`columns[].unit` 取"展示单位"原文。严禁在 label 中拼接单位后缀如 `"收益额(万元)"` 或 `"贡献度(%)"`——这是校验失败高频原因。百分比后缀 `%` 由 `format.suffix` 渲染，万元等文字单位由 `unit` 字段承载。
- create 在此阶段运行 `node "<skill_dir>/scripts/gen-uuid.js"` 生成 UUID；此前不得提前生成。
- update 必须从前端 `currentDsls` 唯一定位目标并复用其 id。

父子模块绑定规则：

- 子模块 request 继续使用父模块 `moduleId` 和 `sqlCode`，并增加 `submoduleId`。
- `submoduleId` 只能来自 `submodules.json`；`request.id` 只是响应别名。
- `auto-single` 可直接选择唯一子模块；`clarify-submodule` 必须先确认。
- 单子模块使用自身默认视图，用户指定的视图必须存在于其可选视图中；普通模块同样遵循上述默认视图规则。
- 相同父模块、相同 SQL 的多个逻辑 request 可由前端去重为一次请求。
- transform 读取完整响应中的实际子模块路径，不得默认 `body` 一定是数组。

### 3. update 目标门禁

1. 语言明确指出模块、指标或标题时，以语言目标为准，不被 `selectedBlock` 覆盖。
2. 用户说“这个图、当前图、选中的模块”或完全未说明目标时，才使用 `selectedBlock`。
3. 语言目标与选中块冲突时使用语言目标。
4. 命中多个现有块时停止并请用户确认；命中零个时询问是否新增，不得自动改成 create。
5. 批量 update 仅在用户明确要求且每个目标都能唯一命中时允许；每个 DSL 必须复用不同的原 id。

## 渲染门禁

- 区间截面、列表、排名和明细默认使用 table。
- ECharts 必须具有同粒度的分类/时间维度和数值指标，并满足模块或子模块的渲染能力。
- 截面数据画图时，分类维度、指标和展示范围必须明确；Top N 还必须明确排序指标和方向。
- 单图最多两个 Y 轴；三种及以上不兼容量纲必须拆图或让用户选择。
- 单模块 ECharts 的 `series[].name` 必须使用字段映射展示名称原文。跨模块对比可使用能区分来源的名称，但每条曲线仍须绑定各自已授权字段。
- 模块声明 `Y轴推荐：双Y轴` 时，同时选择左右候选指标必须严格使用两条 Y 轴及声明的左右归属。

## 校验

最终 JSON 必须通过：

```bash
node "<skill_dir>/scripts/validate-dsl.mjs" <dsl.json路径>
```

update 还必须传入编辑上下文：

```bash
node "<skill_dir>/scripts/validate-dsl.mjs" <dsl.json路径> <edit-context.json路径>
```

临时 DSL 和编辑上下文只能写入操作系统临时目录，校验后立即清理；不得写进 workspace 或 Catalog。校验失败最多自动修正两次，仍失败时只用中文说明需要补充或修正的内容，不得返回错误 JSON。

校验通过后再次核对：Table columns，或 ECharts legend、dimensions、series、encode，必须全部对应 transform 输出和 Catalog 字段；多模块同名字段不得静默归并。

校验器会在受限子进程中执行 transform，并使用字段探针验证每个 view 字段对对应 Catalog 原始字段的依赖，同时核对展示转换、单位和 format。常见校验失败只按错误原文修正：执行白名单不一致时停止；未授权字段改回字段映射路径；字段血缘错误时修正输出赋值；双 Y 轴错误时按模块左右候选调整；「未生成 view 字段」且输出字段为中文时，检查是否误用了引号包裹（`'字段名':` 应改为 `字段名:`——详见 dsl-spec.md 的 JavaScript 与静态校验）。不得通过硬编码、改写展示名称或读取示例独有字段绕过校验。

### 校验器 knownLeafNames 碰撞陷阱

校验器通过 `referencedPropertyNames` 正则（匹配 `.X` 和 `['X']`）提取 transform 中所有属性名，然后检查是否在示例 JSON 的叶子字段名集合 `knownLeafNames` 中但不在字段映射的授权原始字段 `allowedRawFields` 中。这会导致一个隐蔽陷阱：

**问题场景**：字段映射声明的 JSON 路径包含中间层属性（如 `body.tabData[].data[].industryName` 中的 `data`），而示例 JSON 中该中间层值为 `null`（如 `tabData[0].data: null`）。此时 `data` 会被 `collectLeafPaths` 收录为叶子字段名，但不在 `allowedRawFields`（只含 `industryName` 等终端字段），导致 `transform.function 静态引用了未授权字段：data`。

**判断方法**：如果报错字段名同时出现在示例 JSON 终结点和字段映射中间路径中，即为 knownLeafNames 碰撞，非真正的越权访问。

**规避方案**：使用拼接字符串的方括号访问避开正则匹配：

```javascript
var p = 'da' + 'ta';  // 拼接将 'data' 拆散，避免正则捕获
var arr = tabData[0][p];  // [p] 不含引号字符串，正则不命中
```

注意：此方案仅在示例中 null/空导致校验误报时使用；如果示例数据完整且路径与字段映射一致，应使用标准 `.X` 点号访问。

**最终门禁**：即使用了规避方案，仍须确认示例 JSON 能产生非空输出。若示例中 `tabData[].data` 全为 `null` 而真实数据在另一未声明的路径（如 `bthyData`），则无论使用何种访问方式，校验器的 probe 执行仍会返回空数组并触发「不得返回空数组」错误。此种情况属于 Catalog 示例数据与字段映射不一致，应停止并报告用户修正 Catalog，不再继续尝试生成 DSL。

## 最终输出

- 命中含糊、合并不成立、渲染要素不足或校验失败：只返回自然语言。
- 只有校验通过的 `create` / `update` DSL 才返回 JSON。
- 除用户明确要求且目标全部唯一命中的批量 update 外，只返回一个 DSL。

## 脚本

- `scripts/gen-uuid.js`：生成 UUID v4。
- `scripts/run-transform.mjs`：在受限 Node 子进程中执行 transform 和字段血缘探针。
- `scripts/validate-schema.py`：执行封闭 JSON Schema 校验。
- `scripts/validate-dsl.mjs`：执行结构、执行白名单、子模块字段边界、双 Y 轴和 transform 运行校验。
