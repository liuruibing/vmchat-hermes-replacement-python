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
