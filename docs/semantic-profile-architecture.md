# VM Chat 结构化语义 Profile 优化方案

## 目标

解决跨模块指标在业务上可以合并，但模型因为 Wiki 信息不足、字段名不同或单位不同而过度拒绝的问题。

本方案不引入 36 x 36 的人工合并矩阵，也不要求逐个维护复杂 metadata。核心思路是：

SQL + 模块字段映射 + 样例 JSON -> 运行时自动生成 Semantic Profile -> LLM 依据 Profile 生成 DSL。

## 设计原则

1. Wiki 降级为业务叙述，不再承担结构事实的唯一来源。
2. SQL 不直接整段塞给模型，只提取轻量证据，例如底层表、参数、GROUP BY 字段、是否出现基金/日期/行业。
3. 样例 JSON 中稳定出现但未进入展示字段映射的字段，可以作为结构关联键，但不能展示给用户。
4. 日期字段名不同不等于语义不同。TDATE、D_DATE、XAXISDATA 等会映射为 canonical date。
5. 单位不同不等于不能合并。数据层可合并后，再由 table 或双 Y 轴解决展示差异。
6. 分类体系明确冲突时才拒绝行业横向关联。

## 运行时资源

ResourceLoader 会在启动时生成以下虚拟资源，不写入 resources/manifest.json：

- catalog/profile-index.json
- catalog/profiles/<moduleId>.json
- skill/references/merge-guidance-v2.md

Profile 主要包含：

- shape
- entity
- grain
- joinKeys
- taxonomy
- render dimensions / metrics
- fields
- structuralOnlyFields
- sqlEvidence
- quality

## SQL 证据来源

按优先级读取：

1. 环境变量 VMCHAT_SQL_KNOWLEDGE_PATH
2. delivery/02_vm_modules_sql_statements.md
3. docs/vm-modules-sql-statements.md

SQL 原文不会暴露给模型，只暴露提取后的结构摘要。

如果 SQL 看起来是占位 SQL、缺少与模块结构一致的日期/行业/基金证据，Profile 会产生 quality.warnings，并把 sqlTrust 标记为 low。此时模型应优先相信字段映射和样例 JSON 的稳定结构。

## 跨模块判断示例

### 产品时序

stockExposureTiming、averagePePb、hldStockNumTime：

- entity = fund
- shape = time_series
- canonical join key = date

即使原始日期字段分别是 TDATE、D_DATE、XAXISDATA，也允许按 date 做 outer join。

### 申万行业

swInduStockAlloca、swInduStockVala、swInduStockAnal：

- entity = fund
- shape = cross_section
- canonical join key = industry
- taxonomy = SWSR

允许 industryCode 优先、industryName 兜底的横向关联。

### 不同行业体系

swInduStockAlloca 与 hsInduStockAlloca：

- canonical join key 都是 industry
- taxonomy 不同

应拒绝直接按行业关联。

## 调试

可以直接运行：

    python scripts/inspect_semantic_profiles.py averagePePb stockExposureTiming hldStockNumTime

查看完整 Profile：

    python scripts/inspect_semantic_profiles.py swInduStockAlloca swInduStockVala swInduStockAnal --full

## 后续建议

第一阶段先观察真实对话命中率，不要立即增加更多人工规则。

当出现误判时优先修正自动提取逻辑或少量 override，而不是继续扩写 Wiki。只有无法从 SQL、样例结构、字段映射中稳定推断的少数业务例外，才值得维护人工 override。
