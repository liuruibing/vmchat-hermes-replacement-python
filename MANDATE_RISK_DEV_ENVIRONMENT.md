# Mandate 风险指标拆解系统 — 开发、联调与优化指南

> 本文档汇总了前端页面地址、Colab 远程后端接口、SSH 连接方式及核心业务代码架构，方便后续协同开发与算法优化。

---

## 一、前端访问与工程路径

### 1. 访问地址
* **本地快速测试页面（单文件完整版）**：
  👉 **`http://localhost:9528/static/test-mandate-risk.html`**
* **公司内网局域网访问地址（供同事访问）**：
  👉 **`http://192.168.30.92:9528/static/test-mandate-risk.html`**
* **友邦绩效 Vue 业务集成页面**：
  👉 `http://localhost:9528/#/mandateRisk`

### 2. 前端工程与源码位置
* **项目根路径**：
  `/Volumes/onePiece/公司前端项目/友邦绩效/datadriver-fund-amc-tyjx-vue`
* **Node.js 运行环境**：
  `v14.19.0`（路径：`/Users/liuruibing/.nvm/v14.19.0/bin/node`）
* **核心业务代码目录**：
  `src/views/mandateRisk/`
  * `index.vue`：Mandate 风险拆解主容器页面
  * `api/index.js`：Colab 后端通信客户端（PDF 上传、Run 创建、SSE 流式解析）
  * `components/MarkdownReport.vue`：Markdown 指标表格渲染组件（已修复 `table-layout: fixed` 自适应防撑开）
  * `components/ReasoningPanel.vue`：AI 深度思考推理流展示组件
  * `components/DocumentCard.vue`：PDF 上传卡片与解析状态
  * `test-mandate-risk.html`：免编译开箱即用的完整静态联调页面
* **Webpack 代理配置**：
  `config/index.js` 中的 `/mandate-api` 代理目标：已映射至 Colab 最新隧道。

---

## 二、后端服务与 API 契约

### 1. 后端访问地址
* **Cloudflare 公网隧道 Base URL（通过本地 OMP 代理直达 Gemini 3.8 Flash）**：
  👉 **`https://opinion-bobby-heroes-florence.trycloudflare.com`**
* **本地直接访问 Base URL**：
  `http://127.0.0.1:8002`

### 本地 OMP 模型代理（8005）

Docker 的模型请求可通过 `scripts/omp_openai_gateway.py` 转发到本机 OMP CLI：

```bash
.venv/bin/python scripts/omp_openai_gateway.py
```

默认监听 `0.0.0.0:8005`，模型为 `google-antigravity/gemini-3.8-flash`；`OMP_GATEWAY_PORT` 可用于临时验证端口。不要把该无鉴权代理暴露到不可信网络。

OMP 的 `--no-tools` 仅关闭内置工具，仍可能发现全局 MCP。当前本机全局 `rea` MCP 的工具 Schema 含 Gemini 不支持的 `if/then`，会造成模型 HTTP 400，最终被代理包装为 HTTP 500。代理在每次请求的临时目录写入 `.omp/mcp.json`，仅对此次调用禁用同名 `rea` 服务；不修改用户全局配置、模型或认证。其他名称的 MCP 不在此修复范围内。

OMP stdout JSON 中的 assistant `errorMessage` 优先作为失败详情；stderr 并行读取。`error`、`aborted`、`length` 结束状态不作为成功回答返回。不要以 `/health` 成功代替模型可用验证：先向 `/v1/chat/completions` 发最小请求，再通过业务 `/v1/runs/{run_id}/events` 确认完整分析到达 `run.completed`。

### 2. 后端工程信息
* **代码仓库路径**：
  `/Volumes/onePiece/公司前端项目/AI项目/vmchat-hermes-replacement-python`
* **当前活跃分支**：
  `research/mandate-risk-speed-2026-10-14`
* **统一工作流 (Workflow ID)**：
  * **`mandate-risk-copilot`**：基于 LangGraph 的统一多意图分析与问答工作流（默认路由）。
  * **`mandate-risk-analysis-v2`**：原串行 V2 分析工作流（保留作为性能与精度对比基准）。
* **运行框架与模型**：
  * **框架**：FastAPI + LangGraph 工作流图（`StateGraph` 并发子图与意图路由）
  * **大模型**：Google `google-antigravity/gemini-3.8-flash`（经本地 `scripts/omp_openai_gateway.py` 8005 代理或直连）

### 3. LangGraph 并发分析与统一多意图架构说明

1. **双路并发分析子图 (`ParallelMandateAnalysis`)**：
   - **分支 A (Screening)**：阅读 PDF 条款与 34 项完整指标库，输出相关指标匹配分、依据与差异；毫秒级附加本地参考组合。
   - **分支 B (Strategy Evidence)**：独立阅读 PDF 原文与指标目录，提取三大语义板块（Instruments / Benchmark / Investment Strategy）和策略要点，不依赖前序打分理由。
   - **安全 Join**：以分支 A 最终入选指标为主键合并，未建立策略关联的指标明确归入 `unlinked_metrics`，严禁将筛选理由伪造为策略依据；单分支异常或取消时自动熔断取消兄弟任务。
   - **提速实测**：端到端分析耗时由 35s+ 缩短至 ~19.26s。

2. **多意图路由与会话持久化 (`MandateRiskCopilotWorkflow`)**：
   - `operation: 'analyze'`：必须提供 PDF，触发双路并发分析；完整结构化结果通过 `MandateAnalysisStore` 存入既有 `ai-artifacts.sqlite3`，会话保存引用。
   - `operation: 'ask'` (文档/报告追问)：读取当前会话绑定文档的前序分析结构体与相关条款切片，~3-6 秒内响应，不重新跑整篇分析。
   - `operation: 'ask'` (纯指标知识咨询)：仅查询指标知识库，**不加载 PDF，不注入无关会话历史**，~4-5 秒内响应，不污染主界面分析报表。

### 3. 核心 API 接口定义

#### ① 健康检查与就绪探针
* **请求**：`GET /health`
* **响应示例**：
  ```json
  {
    "status": "ok",
    "documentStore": "sqlite",
    "maxDocumentBytes": 20971520,
    "workflows": ["mandate-risk-analysis", "mandate-risk-analysis-v2", "mandate-risk-copilot", "simple-chat", "vm-report"],
    "langGraphEnabled": true
  ```

#### ② 上传合同 PDF 文件
* **请求**：`POST /v1/documents`
* **Header**：`Content-Type: multipart/form-data`
* **Body**：`file: <PDF二进制流>`（单文件上限 20 MB）
* **响应 (201 Created)**：
  ```json
  {
    "document": {
      "document_id": "doc_cb819d6fa47c420db963eaf18ebeb75e",
      "filename": "固收sample.pdf",
      "size_bytes": 166912,
      "page_count": 6,
      "status": "ready"
    }
  }
  ```

#### ③ 发起 Mandate 风险指标拆解任务
* **请求**：`POST /v1/runs`
* **Header**：`Content-Type: application/json`
* **Body**：
  ```json
  {
    "agent_id": "mandate-risk-ai",
    "role_id": "risk-analyst",
    "workflow": "mandate-risk-analysis",
    "model": "gemini-3.5-flash-lite",
    "input": [{ "role": "user", "content": "请分析我上传的 PDF，根据风险指标库识别适用的风险指标..." }],
    "documents": ["doc_cb819d6fa47c420db963eaf18ebeb75e"],
    "session_id": "mandate_session_001"
  }
  ```
* **响应**：`{ "run_id": "run-91a6d447-398b-4bb6-8047-9296227e532a" }`

#### ④ 接收实时流式分析报告 (SSE)
* **请求**：`GET /v1/runs/{run_id}/events`
* **Header**：`Accept: text/event-stream`
* **流式事件类型**：
  * `data: {"event": "reasoning.delta", "delta": "思考片段...", "sequence": N}`
  * `data: {"event": "message.delta", "delta": "Markdown内容片段..."}`
  * `data: {"event": "run.completed", "output": "完整的Markdown风险报告全文"}`

---

## 三、Google Colab SSH 远程连接与运维

### 1. 本机终端免密连接
本机终端直接执行以下命令，即可一键进入 Colab 虚拟机的交互式 Shell：
```bash
ssh colab
```

### 2. 本地 SSH 配置文件 (`~/.ssh/config`)
```ssh-config
Host colab
    User root
    ProxyCommand colab ssh --proxy-mode -s colab
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    RequestTTY yes
    RemoteCommand cd /content 2>/dev/null; exec bash -l
```
* **使用的本地公钥**：`~/.ssh/id_ed25519.pub`

### 3. Colab 命令行管理工具 (`colab`)
* **查看当前运行的会话**：`colab sessions`
* **新建会话**：`colab new -s colab`
* **清理/停止会话**：`colab stop -s colab`

### 4. 远程虚拟机内部运维信息
* **代码目录**：`/content/vmchat-hermes-replacement-python`
* **Python 虚拟环境**：`/content/vmchat-hermes-replacement-python/.venv/`
* **核心服务启动命令**：
  ```bash
  nohup uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 > /content/uvicorn.log 2>&1 &
  ```
* **公网隧道启动命令**：
  ```bash
  nohup /content/cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate > /content/cloudflared.log 2>&1 &
  ```
* **查看日志**：
  * 后端接口日志：`tail -f /content/uvicorn.log`
  * 隧道映射日志：`tail -f /content/cloudflared.log`

---

## 四、待 Codex 重点优化的业务算法点

当前输出与投资经理业务底稿（Excel 预期）存在以下几个核心优化项，可直接指导 Codex 进行针对性改进：

### 1. 填补【分组】字段缺失（目前硬编码显示为 `—`）
* **现状**：`app/mandate_risk/renderer.py` 中将分组固定填为了 `"—"`。
* **目标**：在 `RawRiskMetric` 或 `registry.py` 中引入业务三层分类：
  * **`key（直观判断组合运行情况）`**：如 久期、DV01、基金收益率
  * **`core（体现策略特征）`**：如 剩余期限
  * **`Indicator（趋势变化分析）`**：如 信用利差、内部评级分布、换手率（Turnover）、债券资产变现天数

### 2. 优化固收策略下的漏召回门禁
* **现状**：
  * `Turnover`（换手率）在底层 CSV 中只标记了 `权益`，导致固收合同识别后被策略过滤器硬剔除；
  * `Dv01` 与久期重叠被去重策略误杀；
  * `剩余期限`（对应 `Buy and Maintain`）与 `债券资产变现天数`（对应 `Capital Management`）被过于严格的门禁降级剔除。
* **目标文件**：
  * `指标知识库.md`（唯一人工维护的权威风险指标 Markdown 知识库，修改后显式执行 `python -m app.mandate_risk.catalogue` 生成 `指标知识库.generated.json` 并重启服务）
  * `app/mandate_risk/matcher.py`（召回词库与触发器放开）
  * `app/workflow/graphs/mandate_risk.py`（候选池打分与排序逻辑）

### 3. 【Mandate解读】风格由“分析日志”精简为“合同条款原文 Quote”
* **现状**：输出长段说明性自辩文案（*“Python校验...证据表明指标相关但未形成明确约束故降为...”*）。
* **目标**：优化 `app/mandate_risk/prompts.py` 中的提示词，直接提取并展示合同对应的英文关键短语：
  * 如：`Focus on CNY denominated long-term Public Credit`
  * 如：`Managed in a Buy and Maintain style`
  * 如：`reasonable credit risk exposure.`
  * 如：`Capital Management`
