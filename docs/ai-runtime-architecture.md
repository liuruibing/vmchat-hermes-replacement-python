# AI Runtime Architecture

## Goal

The Python service is no longer only a vmChat DSL backend. It is evolving into a reusable **AI Runtime** where a domain AI is packaged as an Agent Package.

The core runtime owns:

- sessions and conversation memory;
- prompt/context budgets;
- roles;
- skills;
- knowledge retrieval;
- model providers;
- artifacts;
- run lifecycle and SSE;
- workflow dispatch.

Domain code stays outside the core.

## Runtime layers

```text
FastAPI / SSE
    |
    v
AI Runtime
    |
    +-- Agent Registry
    +-- Session Manager
    +-- Context Manager
    +-- Role Registry
    +-- Knowledge Service
    +-- Artifact Store
    +-- Model Provider
    +-- Workflow
          |
          +-- vm-report
          +-- simple-chat
```

### Run != Session

A Run is one execution and is still managed by `RunStore`.

A Session is long-lived and now persists in SQLite:

```text
session-123
  messages
  summary
  ui state
  semantic state
  artifact ids
  agent / role
```

The frontend may still send history for backwards compatibility, but it is only used to bootstrap an empty server-side session. Once a session exists, Python owns conversation history.

## Context strategy

The model never receives the whole session.

`ContextManager` selects:

- recent messages;
- a few older messages relevant to the current query;
- a bounded session summary;
- full DSL for selected/relevant report blocks;
- compact summaries for unrelated blocks.

Large DSL results are stored as artifacts. The session keeps an artifact reference rather than copying the full DSL into every later prompt.

Knowledge/tool context has a separate budget, so resource reads cannot consume the whole model window.

## Agent Packages

An Agent Package lives under:

```text
agents/<agent>/
  agent.json
  roles/
    <role>.json
  ... skill / knowledge files
```

Example:

```json
{
  "id": "research-ai",
  "name": "Research AI",
  "workflow": "simple-chat",
  "skill_path": "SKILL.md",
  "knowledge_paths": ["knowledge"],
  "roles_dir": "roles",
  "default_role": "researcher"
}
```

For a normal RAG/knowledge assistant, adding a new package usually only requires:

1. `agent.json`
2. a Skill
3. Wiki/knowledge documents
4. one or more Roles

No FastAPI route or model-provider code needs to be copied.

For domain workflows with structured output and validators, add a workflow implementation. The current `performance-ai` uses the existing `vm-report` workflow.

## Knowledge

`KnowledgeService` chunks and incrementally indexes agent knowledge.

Search is hybrid-ready:

1. lexical/structured matching;
2. optional embedding similarity;
3. score merge;
4. Top-K context returned to the model.

The runtime supports `DuckDbKnowledgeStore`. If the `duckdb` Python package is not installed, it automatically falls back to SQLite so deployments remain compatible.

To enable DuckDB locally or in Colab:

```bash
pip install duckdb
```

Optional vector retrieval is enabled with:

```text
EMBEDDING_MODEL
EMBEDDING_API_KEY
EMBEDDING_BASE_URL   # optional OpenAI-compatible endpoint
```

Without an embedding provider, retrieval remains lexical. This is intentional: exact metric aliases and structured business identifiers should not depend only on vector similarity.

## Performance AI

The current vmChat domain is now represented by:

```text
agents/performance_ai/
  agent.json
  roles/performance-analyst.json
```

Its workflow remains:

```text
user request
  -> metric/module knowledge retrieval
  -> DSL generation
  -> Python validation
  -> repair if required
  -> artifact + frontend
```

Existing Semantic Profiles, merge validation and DSL repair remain domain-specific and should gradually move behind the `performance-ai` package boundary.

## API additions

- `GET /v1/agents`
- `GET /v1/agents/{agentId}/roles`
- `GET /v1/sessions/{sessionId}`
- `DELETE /v1/sessions/{sessionId}`
- `POST /v1/knowledge/search`
- `GET /v1/artifacts/{artifactId}`

Existing `/v1/runs` and SSE remain compatible.

## Next migration steps

1. Move remaining vmChat-specific prompt/validator files into the performance agent package without changing behavior.
2. Add a Metric Registry to the performance agent so metric -> source/grain/join-key resolution becomes deterministic.
3. Add a workflow registry / LangGraph adapter for complex stateful workflows.
4. Replace the deterministic session synopsis with an optional background LLM summarizer.
5. Add evaluation suites under each Agent Package.


## LangGraph Workflow 层

Runtime Core 不直接依赖具体业务流程。所有 Agent 通过 `WorkflowEngine -> WorkflowRegistry` 选择工作流；LangGraph 只是其中一个 workflow 实现技术。

当前内置 LangGraph：

- `simple-chat`: `retrieve_knowledge -> answer`
- `vm-report`: `resolve_semantics -> generate -> validate -> repair -> validate -> finalize`

`vm-report` 的 `resolve_semantics` 会优先从运行时 Module Profile 中确定用户明确点名的指标，并生成结构化 `semanticPlan`（entity / shape / grain / joinKey / taxonomy）。这些结果作为高优先级提示注入 generate/repair，但最终 DSL 仍由 Python Validator 决定是否合法。

### State 边界

Graph State 只保存本次 run 的轻量执行状态，例如：

- resolved metrics
- semantic plan
- candidate DSL
- validation errors
- usage
- resource path refs

完整 Session、Wiki、Artifact DB、Provider 实例不会进入 Graph State。

长期会话继续由 `SessionManager` 管理；页面 DSL 大对象由 `ArtifactStore` 管理；知识正文由 `KnowledgeService` 按需 Top-K 检索。

### Checkpoint

LangGraph 当前使用共享的 `InMemorySaver` 做 run 级 checkpoint，thread id 优先使用 `run_id`。它用于测试/单进程恢复能力，不替代长期 Session Store。

后续如果需要进程重启后的 workflow resume，可在 Workflow 层替换持久化 checkpointer，而无需修改 Session/Knowledge/Artifact API。

## Context Budget

ContextManager 会在 Python 端强制执行总预算：

- `MAX_CONTEXT_TOKENS`: 总模型上下文目标预算
- `MAX_CONTEXT_RESERVED_TOKENS`: 为 system/role/skill/当前问题/知识检索预留
- `MAX_CONTEXT_DSL_TOKENS`: 页面 DSL 上限
- `MAX_CONTEXT_HISTORY_TOKENS`: 历史对话上限

运行时优先保留 selected/relevant DSL，再裁剪较老 history，必要时截短 session summary。如果 selected/relevant DSL 自身已经超过动态预算，会在调用 LLM 前返回明确的 `CONTEXT_DSL_TOO_LARGE`，而不是继续堆到模型窗口溢出。

`POST /v1/runs` 返回 context telemetry，包括 estimated/budget/reserved tokens、被丢弃的历史条数以及 summary 是否被截断。
