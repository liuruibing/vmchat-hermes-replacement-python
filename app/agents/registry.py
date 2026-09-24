from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from app.agents.models import AgentDefinition, RoleDefinition


class AgentRegistry:
    """Loads declarative Agent Packages from agents/*/agent.json."""

    def __init__(self, root: str = "agents") -> None:
        self.root = Path(root).resolve()
        self._agents: Dict[str, AgentDefinition] = {}
        self._roles: Dict[tuple[str, str], RoleDefinition] = {}

    def load(self) -> "AgentRegistry":
        self._agents.clear()
        self._roles.clear()
        if not self.root.exists():
            return self

        for manifest_path in sorted(self.root.glob("*/agent.json")):
            package_dir = manifest_path.parent
            raw = json.loads(manifest_path.read_text(encoding="utf-8"))
            agent = AgentDefinition.model_validate(raw)

            def resolve_optional(path_value: Optional[str]) -> Optional[str]:
                if not path_value:
                    return None
                return str((package_dir / path_value).resolve())

            agent.resourcesDir = resolve_optional(agent.resourcesDir)
            agent.skillPath = resolve_optional(agent.skillPath)
            agent.rolesDir = resolve_optional(agent.rolesDir)
            agent.knowledgePaths = [
                str((package_dir / path).resolve())
                for path in agent.knowledgePaths
            ]

            if agent.id in self._agents:
                raise RuntimeError(f"DUPLICATE_AGENT_ID: {agent.id}")
            self._agents[agent.id] = agent

            if agent.rolesDir:
                roles_dir = Path(agent.rolesDir)
                if roles_dir.exists():
                    for role_path in sorted(roles_dir.glob("*.json")):
                        role = RoleDefinition.model_validate(
                            json.loads(role_path.read_text(encoding="utf-8"))
                        )
                        self._roles[(agent.id, role.id)] = role

        return self

    def read_skill(self, agent_id: str) -> str:
        agent = self.require(agent_id)
        if not agent.skillPath:
            return ""
        path = Path(agent.skillPath)
        if not path.is_file():
            raise RuntimeError(f"MISSING_AGENT_SKILL: {agent.skillPath}")
        return path.read_text(encoding="utf-8")

    def collect_knowledge(self, agent_id: str) -> Dict[str, str]:
        agent = self.require(agent_id)
        documents: Dict[str, str] = {}
        allowed_suffixes = {".md", ".txt", ".json", ".yaml", ".yml"}
        for configured in agent.knowledgePaths:
            source = Path(configured)
            if source.is_file():
                if source.suffix.lower() in allowed_suffixes:
                    documents[source.name] = source.read_text(encoding="utf-8")
                continue
            if not source.is_dir():
                continue
            for file_path in sorted(source.rglob("*")):
                if not file_path.is_file() or file_path.suffix.lower() not in allowed_suffixes:
                    continue
                rel = file_path.relative_to(source).as_posix()
                key = f"{source.name}/{rel}"
                documents[key] = file_path.read_text(encoding="utf-8")
        return documents

    def list_agents(self) -> List[AgentDefinition]:
        return list(self._agents.values())

    def get(self, agent_id: str) -> Optional[AgentDefinition]:
        return self._agents.get(agent_id)

    def require(self, agent_id: str) -> AgentDefinition:
        agent = self.get(agent_id)
        if agent is None:
            raise ValueError(f"UNKNOWN_AGENT: {agent_id}")
        return agent

    def get_role(self, agent_id: str, role_id: Optional[str] = None) -> Optional[RoleDefinition]:
        agent = self.get(agent_id)
        if agent is None:
            return None
        resolved = role_id or agent.defaultRole
        if not resolved:
            return None
        return self._roles.get((agent_id, resolved))
