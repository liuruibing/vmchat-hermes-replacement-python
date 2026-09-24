from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class RoleDefinition(BaseModel):
    id: str
    name: str
    systemPrompt: str = Field(default="", alias="system_prompt")
    allowedSkills: List[str] = Field(default_factory=list, alias="allowed_skills")
    allowedTools: List[str] = Field(default_factory=list, alias="allowed_tools")
    knowledgeScopes: List[str] = Field(default_factory=list, alias="knowledge_scopes")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)


class AgentDefinition(BaseModel):
    id: str
    name: str
    version: str = "1.0.0"
    workflow: str = "vm-report"
    resourcesDir: Optional[str] = Field(default=None, alias="resources_dir")
    skillPath: Optional[str] = Field(default=None, alias="skill_path")
    knowledgePaths: List[str] = Field(default_factory=list, alias="knowledge_paths")
    rolesDir: Optional[str] = Field(default=None, alias="roles_dir")
    defaultRole: Optional[str] = Field(default=None, alias="default_role")
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)
