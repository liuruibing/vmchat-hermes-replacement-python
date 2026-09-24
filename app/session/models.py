from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict


class SessionMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    createdAt: float = Field(alias="created_at")
    runId: Optional[str] = Field(default=None, alias="run_id")

    model_config = ConfigDict(populate_by_name=True)


class SessionUiState(BaseModel):
    selectedBlockId: Optional[str] = Field(default=None, alias="selected_block_id")
    globalQueryParameters: Dict[str, Any] = Field(default_factory=dict, alias="global_query_parameters")
    blockSummaries: List[Dict[str, Any]] = Field(default_factory=list, alias="block_summaries")

    model_config = ConfigDict(populate_by_name=True)


class SessionState(BaseModel):
    sessionId: str = Field(alias="session_id")
    agentId: str = Field(default="performance-ai", alias="agent_id")
    roleId: str = Field(default="performance-analyst", alias="role_id")
    summary: str = ""
    messages: List[SessionMessage] = Field(default_factory=list)
    semanticState: Dict[str, Any] = Field(default_factory=dict, alias="semantic_state")
    artifactIds: List[str] = Field(default_factory=list, alias="artifact_ids")
    uiState: SessionUiState = Field(default_factory=SessionUiState, alias="ui_state")
    createdAt: float = Field(alias="created_at")
    updatedAt: float = Field(alias="updated_at")

    model_config = ConfigDict(populate_by_name=True)
