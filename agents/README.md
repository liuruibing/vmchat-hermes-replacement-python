# Agent Packages

The runtime discovers `agents/*/agent.json`.

A simple knowledge AI can be created without changing FastAPI code:

```text
agents/my_ai/
  agent.json
  SKILL.md
  knowledge/
    handbook.md
    faq.md
  roles/
    expert.json
```

Example `agent.json`:

```json
{
  "id": "my-ai",
  "name": "My AI",
  "version": "1.0.0",
  "workflow": "simple-chat",
  "skill_path": "SKILL.md",
  "knowledge_paths": ["knowledge"],
  "roles_dir": "roles",
  "default_role": "expert"
}
```

Example role:

```json
{
  "id": "expert",
  "name": "Domain Expert",
  "system_prompt": "You are a precise domain assistant.",
  "allowed_skills": [],
  "allowed_tools": ["knowledge.search"],
  "knowledge_scopes": ["default"]
}
```

`simple-chat` automatically gets:

- server-side session memory;
- bounded context selection;
- role prompt;
- Skill;
- agent knowledge search;
- SSE streaming.

Use a custom workflow only when an Agent needs domain-specific structured output, validators, external execution, or repair loops.
