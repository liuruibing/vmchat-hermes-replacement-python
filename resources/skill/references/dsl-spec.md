# VM Report DSL 通用规范

本文档面向生成 DSL 的 skill。输入是用户问题以及已经生成好的 `modules/*.md`；输出是前端可执行的 VM Report DSL JSON。

## 目录

- 输入、输出语言与生成时机
- 指标范围和顶层结构
- update 目标与删除边界
- requests 与子模块组合
- Transform 生成规则
- 展示格式化规则
- 输出约束

## 输入

- 用户问题：决定要生成 `table` 还是 `echarts`，以及维度、指标、展示范围和合并口径。
- 模块 MD：提供字段路径、展示名称、展示转换、展示单位、指标业务说明、候选维度和候选指标。
- `execution-contract.json`：提供可执行的 `moduleId`、`sqlCode` 和 `submoduleId` 白名单。
- `submodules.json`：提供子模块的数据路径和字段路径边界。

## 输出语言

所有 JSON DSL 之外的用户可见文本必须使用中文，包括过程提示、澄清问题、错误说明、校验失败说明和最终回复。不得输出英文流程句。

JSON DSL 内的字段名、参数名、代码标识、JavaScript 函数和 ECharts 配置键可以保持英文。

## 澄清反问风格

只要还在确认模块、指标、展示范围、图表类型或合并口径，就必须使用清晰易读的自然中文反问。禁止将反问文案堆叠为大段无排版文本，禁止输出 Markdown 表格、代码块、JSON、DSL 片段。

反问文案统一采用“背景说明 + 选项列表 + 推荐选项”结构，禁止在回复中使用 `**` 加粗符号：
1. 背景说明（1–2 句）：说明知识库匹配情况及需要确认的原因（模块与字段名使用普通书名号 `「」`，禁止添加 `**`）。
2. 选项列表：使用 `1. 选项名称：说明` 的有序列表呈现供用户选择的路径。
3. 推荐选项：在列表下方附加 `💡 推荐选项：根据您这次的提问，建议选择 1. 选项名称`。

所有候选项必须使用 `index.md` 中的中文业务名称。不得在用户可见的澄清、错误或状态文案中出现 `catalog`、`moduleId`、`submoduleId`、`sqlCode`、英文模块标识或文件路径；这些信息只用于内部检索和最终 DSL。需要说明来源时统一称“知识库”。子模块按“父模块中文标题 > 子模块中文标题”展示，父标题和子标题都从 `index.md` 解析，不能用父模块 ID 代替父标题。

示例：命中「A股行业集中度」模块且需要确认渲染形式时，应回复：
根据知识库检索，您的需求匹配到「A股行业集中度」模块。在生成折线图时，由于前五大行业是动态排序的，图表需要确认具体固定的行业名称。

请确认您期望的展示形式：
1. 表格形式展示：直接呈现全部行业的配置比例时序数据，无需指定固定行业。
2. 指定行业绘制折线图：指定具体的 1~5 个行业（如“农林牧渔”、“医药生物”）分别绘制折线。

💡 推荐选项：根据您这次的提问，建议选择 1. 表格形式展示。

精确命中父模块时仍须读取模块 MD 的 `父模块查询策略`。策略为 `clarify-submodule` 且用户未选择子模块时，必须列出中文子模块反问；若 `全部子模块` 为 `combined-table`，同时允许用户回答“都看”。策略为 `unsupported` 时不得提供全部合并选项。

## 生成时机

DSL 只能在所有前置门禁通过后一次性生成。只要仍需要用户确认模块、指标、展示范围、图表类型或合并口径，就必须停止在自然语言反问，不能生成或输出任何 DSL 中间产物。

以下内容都视为 DSL 中间产物，澄清完成前禁止输出：顶层 `id` / UUID、`request.id`、`moduleId`、`submoduleId`、`sqlCode`、`transform.function`、`view`、JSON 片段或示例模板。

create 场景的 UUID 必须在最终构建 DSL 时才生成；不得为了“准备后续 DSL”提前生成 UUID。update 场景只有在前端回传的 `currentId` 与 `currentDsl.id` 已校验一致后，才允许复用该 id 生成完整 update DSL。

## 指标范围

模块标题、模块标识和 `index.md` 中的模块名称表示模块级请求，不等同于选择同名或近似同名的单个指标。

若出现名称碰撞，必须先反问，不得默认按模块或指标继续。名称碰撞包括：

- 用户原文同时能命中模块标题/模块标识和指标名称。
- 模块标题与指标名称高度相似、存在包含关系或只差“时序、列表、占比、走势、明细、模块”等后缀。
- 同一指标名称出现在多个模块或子模块中。
- 当前 block 标题、`view.title`、`series[].name` 或 `columns[].label` 中存在同名/近义名称，导致无法判断用户是在说整个模块、当前图表，还是某个指标。

反问必须要求用户确认“按模块展示全部指标”还是“只展示/修改某个指标”。只有用户明确确认模块级请求，或不存在名称碰撞且没有字段级表达时，才按模块级请求继续。

用户说“全部、全部展示、所有指标、完整展示、这个模块的指标都要”时，最终 DSL 必须覆盖命中模块 `渲染能力` 中的全部指标候选，并逐一映射到字段映射表。ECharts 需要在 `legend.data`、`series[].name`、`dataset.dimensions`、`series[].encode.y` 和 `transform.function` 中都能找到对应输出；table 需要在 `columns[]` 和 `transform.function` 中都能找到对应输出。


## 顶层结构

```json
{
  "action": "create",
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "requests": [],
  "transform": {
    "language": "javascript",
    "function": "function transform(responses) { return []; }"
  },
  "view": {}
}
```

| 字段 | 必填 | 说明 |
|---|---|---|
| `action` | 是 | 只允许 `create` 或 `update` |
| `id` | 是 | 最终 UUID 以生成 DSL 的 skill 规则为准；create 时由 skill 生成，update 时必须复用前端当前 DSL id |
| `requests` | 是 | VM 请求列表 |
| `transform` | 是 | JavaScript 数据转换函数 |
| `view` | 是 | `table` 或 `echarts` |

## update 目标选择

update 必须先在前端回传的 `currentDsls` 中唯一定位目标，再复用其 DSL `id`。`selectedBlock` 只是自然语言理解上下文，不是执行阶段的默认目标。

- 语言明确指出标题、模块或指标时，以语言目标为准。
- 只有“这个图”“当前图”“选中的模块”等指代表达，或用户没有说明目标时，才可以使用 `selectedBlock`。
- 语言目标与 `selectedBlock` 冲突时，以语言目标为准。
- 同一语言目标命中多个报表块时，必须列出能区分它们的标题、产品、日期、频率或页面序号，自然语言请用户确认，不得返回 DSL。
- 未命中任何已有报表块时，说明目标不存在并询问是否新增；未获得用户明确新增指令前不得输出 create DSL。
- 批量 update 只能在用户明确要求批量修改，且每个目标分别唯一命中时输出。

## 删除操作边界

VM Report DSL 只负责 `create` 和 `update`。不得输出 `removeBlock`、删除指令或任何能直接删除前端报表块的包装 JSON。

用户要求删除报表块时，只用自然语言提示其通过前端删除按钮完成。删除动作必须来自用户直接操作前端，不得由 Hermes 响应触发。


## requests

每个 request 只允许：

```json
{
  "id": "cash",
  "moduleId": "cashPositionTiming",
  "sqlCode": "b9f4277e-2793-4a0d-b9ed-e665e4bbd717"
}
```

命中子模块时额外输出：

```json
"submoduleId": "latestNetValue"
```

规则：

- `id` 必须唯一。
- `moduleId` 和 `sqlCode` 来自 `execution-contract.json`，并与模块 MD frontmatter 交叉一致。
- `submoduleId` 必须同时存在于 `execution-contract.json` 和 `submodules.json`，并属于同一 `moduleId`。
- request 中不得写 `params`。
- 同一父模块允许全部子模块合并时，为每个子模块分别生成一个 request；这些 request 可以共享 `moduleId` 和 `sqlCode`，但必须使用不同 `id` 与各自稳定 `submoduleId`。前端可对相同 SQL 去重。

## Transform 生成规则

每个 DSL 都必须包含：

```json
"transform": {
  "language": "javascript",
  "function": "function transform(responses) { return []; }"
}
```

### 字段解析门禁

每个维度、指标、过滤条件和多模块共同键必须按以下顺序解析：

1. 使用用户中文名称定位模块或子模块的字段映射行。
2. ECharts 同时使用渲染能力中的维度和指标候选缩小范围。
3. 结合展示名称、指标业务说明、`metrics.md` 和用户上下文唯一确定目标字段。
4. 按目标 `view.type` 过滤该行的适用视图，再读取 JSON 路径、原始字段、展示转换和单位。同一展示名称存在 table/echarts 两套字段时必须由视图唯一选择，不能跨视图取值。
5. 过滤字段必须来自字段映射或渲染候选，过滤值只能来自用户原文。
6. transform 读取真实原始字段并显式写入最终输出字段；view 只能引用这些输出字段。

字段映射决定“展示什么”，示例 JSON 只证明响应结构和原始取值。不得把示例 JSON 独有的 `TDATE`、`FCODE` 等字段补进 view。

多数据集模块必须读取“数据集绑定”。动态列按其中的动态列名、动态字段名、动态取值和已解析字段建立映射；transform 实际读取的每个叶子字段都必须属于字段映射。示例 JSON 中未进入字段映射的分类值或辅助字段不得作为隐式维度使用。

以下情况停止并自然语言反问：字段无法唯一命中、映射与样例冲突、渲染候选与映射冲突、样例缺少目标路径、跨模块同名字段语义不同、过滤条件含糊，或图表维度/指标/范围不完整。

用户只选部分字段时，只输出所选字段以及渲染或合并必需的维度/共同键。

### JavaScript 与静态校验

- 函数签名固定为 `function transform(responses)`，并显式返回数组。
- 中文展示名称作为输出字段时，必须使用裸属性名（`字段名: value`），不得使用引号包裹（`'字段名': value`）。校验器的 `sourceWritesField` 正则只匹配 `字段名\\s*:` 裸形式，带引号会导致「未生成 view 字段」误报。
- **特殊字符字段名（括号等）**：当展示名称含 `(` `)` 等 JS 标识符非法字符时，对象字面量 `{最大回撤期间(起): value}` 会编译失败（`transform.function 无法编译`）。此时改用 `outRow['字段名'] = value` 方括号赋值模式——校验器的 `assignedPropertyPattern`（`\[\s*['"]字段名['"]\s*\]\s*=`）可正确匹配，且允许括号等特殊字符。一旦有一个字段需要方括号，整个 transform 应统一用 `outRow` 模式，避免混用两种写法。
- 使用 `responses.<requestId>` 并引用每个 request。
- 前端传入完整成功响应；按模块或子模块声明继续读取 `body.YLData`、`body.lastData` 等真实路径，不得默认 `body` 是数组。
- 每个 view field 必须以字面量属性名显式写入输出对象。
- 禁止 `?.`、`??`、`.toFixed()` 和字符串展示格式化。
- 禁止直接返回原始 rows，或用 `Object.keys()` / `for...in` 动态制造输出字段名。共同键集合可以用 `Object.keys(keySet).sort()`，但输出字段仍须显式声明。

正确的显式映射形式（对象字面量，适用于字段名不含特殊字符）：

```javascript
function transform(responses) {
  var response = responses && responses.pePb;
  var rows = response && Array.isArray(response.body) ? response.body : [];
  var result = [];
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    result.push({ TDATE: row.TDATE, F_PETTM: row.F_PETTM, F_PB: row.F_PB });
  }
  return result;
}
```

字段名含括号等特殊字符时，改用 `outRow['字段名']` 方括号模式：

```javascript
function transform(responses) {
  var response = responses && responses.maxDrawdown;
  var rows = response && Array.isArray(response.body) ? response.body : [];
  var result = [];
  for (var i = 0; i < rows.length; i++) {
    var row = rows[i];
    var outRow = {};
    outRow['期间'] = row.dataAround;
    outRow['最大回撤'] = row.fq_maxdraw * 100;
    outRow['最大回撤期间(起)'] = row.fq_maxdraw_topdate;
    outRow['最大回撤期间(止)'] = row.fq_maxdraw_lowdate;
    result.push(outRow);
  }
  return result;
}
```

动态列也必须逐个显式赋值，例如 `outRow['医药生物'] = row.F_HY11`，不得运行时动态生成展示字段名。

### 单模块与排序

- 根据响应区域提取用户需要的字段；`head` 单值可包装为一行数组。
- 子模块只能读取其声明的数据集和字段边界。
- 过滤条件先执行过滤，再生成输出对象。
- 截面数据转 ECharts 时，Top N 必须按用户确认的指标和方向排序后截取；用户要求全部时不得截取。
- 排序前检查样例数值符号。亏损为负数时，“亏损最多”通常使用 `a - b` 让最负值排在前面。

### Catalog 授权的子模块组合

父模块明确允许 `combined-table` 且用户选择全部时：

- 分别读取每个逻辑 request 对应的子模块数据集。
- 按模块 MD 默认顺序纵向拼接。
- 每行增加 MD 声明的合并区分字段。
- 兼容字段使用 MD 的合并统一字段作为公共列名。
- 相同结构字段使用统一输出字段；不得用 `||`、`??` 或三元表达式静默覆盖同行多侧值。
- view 仍是一个普通 table；不生成 `sections`、多个 view 或批量 create。

### 多模块横向关联

- 各模块分别按真实响应路径取值，共同键必须由各自字段映射和业务说明证明语义一致。
- 对全部共同键取合集、去重、排序，再按键回填；缺失侧填 `null`。
- 输出字段使用唯一、可区分来源的名称。
- 禁止按数组下标拼接或仅凭字段同名认定可关联。
- 不存在可靠共同键时返回合并门禁，不生成 transform。

推荐使用 key map 做外连接；不同模块的同名字段必须按 `merge-rules.md` 保留来源或使用用户确认的归并规则。

## 展示格式化规则

Table 的 `columns[].format` 与 ECharts 的 `series[].format` 使用同一规则：

- transform 输出 number，不使用 `toFixed` 或拼接 `%`。
- MD 声明的数值换算在 transform 中执行；format 只负责小数位、符号、前后缀和空值。
- 不得根据字段名、数值范围或常识猜测格式。MD 未声明时使用 `{"type":"raw"}`。
- ECharts 每个 series 必须显式包含 format。

允许的 `format.type` 只有：`raw`、`text`、`date`、`decimal`、`percentage`。禁止 `number`、`string`、`percent`、`integer` 和其他类型。

| MD 展示转换 | transform 输出 | format |
|---|---|---|
| 未声明转换或单位 | 原值 | `{"type":"raw"}` |
| 原值直接使用 | 原值 | 文本用 `text`，数值用 `raw` |
| 保留 N 位小数 | 原值 number | `{"type":"decimal","digits":N,"nullValue":"-"}` |
| 原值 × 100，单位 `%` | `原值 * 100` | `{"type":"percentage","suffix":"%","nullValue":"-"}` |
| 原值 × 100，保留 N 位，单位 `%` | `原值 * 100` | `{"type":"percentage","digits":N,"suffix":"%","nullValue":"-"}` |
| 原值 ÷ 10000 | `原值 / 10000` | `{"type":"decimal","nullValue":"-"}` |
| 原值 ÷ 10000，保留 N 位 | `原值 / 10000` | `{"type":"decimal","digits":N,"nullValue":"-"}` |

Catalog 展示转换只允许上述规范词汇；不得把“百分化”等同义描述自行解释为转换规则。Table 中单位明确时 `columns[].unit` 必须原样提供；存在数值转换时 `format` 必须提供并与转换一致。

百分比不得在 format 中再次设置 `multiplier: 100`，否则会二次换算。

## 输出约束

- DSL 字段、路径、展示名称和格式化规则应来自对应 MD。
- 用户未指定维度、指标、展示范围或合并口径，且无法从问题唯一判断时，必须自然语言反问，不得返回 DSL。
