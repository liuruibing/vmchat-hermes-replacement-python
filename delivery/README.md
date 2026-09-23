# 银河项目 VM 智能报表交付文档包

本项目为 **`vmchat-hermes-replacement-python`** 的专项交付成果包，全面整理并涵盖了 36 个 VM 报表模块的业务指标定义、底层数仓 SQL 语句、映射清单、指标合并决策体系以及整套 Python 系统的端到端业务数据流说明。

---

## 一、交付文件索引

| 序号 | 文件名称 | 类型 | 说明 |
| :---: | :--- | :--- | :--- |
| **01** | [**`01_business_metrics_and_merge_rules.md`**](./01_business_metrics_and_merge_rules.md) | 业务规范文档 | **36个模块业务含义全景与合并边界规范**：<br/>按 8 大金融板块深入解析全部模块业务场景，从数仓主键粒度、防范重复统计、时间形态维度给出合并判定决策树，并针对性诊断修正了既有 Wiki 中的合并描述缺陷。 |
| **02** | [**`02_vm_modules_sql_statements.md`**](./02_vm_modules_sql_statements.md) | 技术详解文档 | **36个 VM 模块真实数仓 SQL 查询语句全集**：<br/>收录全部 36 个模块在底层数仓中的完整原生 SQL 查询语句（包含 `WITH` 临时表、多表 JOIN、量化模型公式、开窗函数等），附入参与字段说明，长达 2300+ 行。 |
| **03** | [**`03_sql_code_inventory.md`**](./03_sql_code_inventory.md) | 清单对照表 | **VM 模块与 sqlCode 全量清单说明表**：<br/>表格化对照全部 36 个模块的 `moduleId`、模块名称、`sqlCode`、数据库配置名称、数据形态（单/多数据集）、子模块及 Wiki 路径。 |
| **04** | [**`04_python_project_dataflow_architecture.md`**](./04_python_project_dataflow_architecture.md) | 架构流程文档 | **Python 项目业务流程与数据流架构说明**：<br/>包含端到端数据流向 Mermaid 时序图，系统阐述从用户提问、FastAPI 接入、知识库装配、大模型推理、本地 DSL 严谨校验自愈循环，到前端 Vue 调度渲染的完整闭环。 |
| **05** | [**`scripts/all_vm_modules_queries.sql`**](./scripts/all_vm_modules_queries.sql) | 可执行脚本 | **可在 DBX / DBeaver 直接运行的纯 SQL 脚本集合**：<br/>按模块分段编排，填入产品参数即可一键直连数仓执行验证。 |

---

## 二、快速使用指南

1. **查阅业务指标定义与合并方案**：直接查阅 `01_business_metrics_and_merge_rules.md`；
2. **复制具体模块的底层 SQL 查询逻辑**：查阅 `02_vm_modules_sql_statements.md` 或直接使用 `scripts/all_vm_modules_queries.sql`；
3. **核对前端与契约的 sqlCode**：查阅 `03_sql_code_inventory.md`；
4. **了解本 Python 服务如何与前端联调及内部自愈机制**：查阅 `04_python_project_dataflow_architecture.md`。
