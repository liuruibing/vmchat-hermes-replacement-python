import json
from pathlib import Path

from app.agents.registry import AgentRegistry


def test_agent_registry_loads_agent_and_role(tmp_path: Path):
    package = tmp_path / "demo"
    roles = package / "roles"
    roles.mkdir(parents=True)

    (package / "agent.json").write_text(
        json.dumps(
            {
                "id": "demo-ai",
                "name": "Demo",
                "workflow": "simple-chat",
                "roles_dir": "roles",
                "default_role": "expert",
                "knowledge_paths": [],
            }
        ),
        encoding="utf-8",
    )
    (roles / "expert.json").write_text(
        json.dumps(
            {
                "id": "expert",
                "name": "Expert",
                "system_prompt": "Answer precisely.",
            }
        ),
        encoding="utf-8",
    )

    registry = AgentRegistry(str(tmp_path)).load()
    agent = registry.require("demo-ai")
    role = registry.get_role("demo-ai")

    assert agent.workflow == "simple-chat"
    assert role is not None
    assert role.systemPrompt == "Answer precisely."
