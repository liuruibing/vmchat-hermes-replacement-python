# 代码导览

打开 [index.html](index.html)，直接双击也可以离线阅读。

页面从公共请求入口出发，包含聊天、绩效报表、风险 V1、V2 screening 和 detailed 五条路线；38 个源码片段保留原文与行号，并附中文旁注。推荐按章节顺序阅读，再在第 3 章选择业务路线，第 7 章查看源码。

- `index.html`：自包含的完整讲解页，不依赖本地服务器。
- `runtime-map.html`：独立交互架构图。
- `runtime.architecture.json`：架构图输入规格。
- `teaching-data.json`：本次源码摘录、中文解释和流程数据。
- `verification.json`：当前源码版本、文件摘要与检查记录。
- `preview.png`：Chrome 中的页面预览。

核对日期：2026-10-08。源码版本：5d1e91255f6f66771a8302675ff3fbbc179411dc。范围为当前 Python 仓库的运行主链路，不包含外部前端仓库实现。后续业务代码变动后，本页摘录和行号需要同步更新。
