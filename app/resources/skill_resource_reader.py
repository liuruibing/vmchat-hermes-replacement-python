from typing import Mapping
from pydantic import BaseModel, Field
from app.resources.resource_types import LoadedResources


class SkillResourceReaderOptions(BaseModel):
    maxContextChars: int = Field(..., alias="maxContextChars")
    initialContextChars: int = Field(..., alias="initialContextChars")
    maxResourceChars: int = Field(default=40000, alias="maxResourceChars")

    model_config = {"populate_by_name": True}

    @property
    def max_context_chars(self) -> int:
        return self.maxContextChars

    @property
    def initial_context_chars(self) -> int:
        return self.initialContextChars


class SkillResourceReader:
    def __init__(self, resources: LoadedResources, options: SkillResourceReaderOptions) -> None:
        self._resources = resources
        self._max_context_chars = getattr(options, "maxContextChars", getattr(options, "max_context_chars", 0))
        self._initial_context_chars = getattr(options, "initialContextChars", getattr(options, "initial_context_chars", 0))
        self._max_resource_chars = getattr(options, "maxResourceChars", getattr(options, "max_resource_chars", 40000))
        self._read_resources_map: dict[str, str] = {}
        self._current_read_chars = 0

    def read(self, resource_path: str = "", **kwargs: str) -> str:
        res_path = resource_path or kwargs.get("resourcePath", "")
        if not res_path or not isinstance(res_path, str):
            return "RESOURCE_NOT_ALLOWED"

        # Safety checks: no backslashes, no relative path escaping, no absolute paths
        if "\\" in res_path or res_path.startswith("/") or ".." in res_path:
            return "RESOURCE_NOT_ALLOWED"

        # Check whitelist
        tool_resources = getattr(self._resources, "toolResourceTextByPath", None)
        if tool_resources is None:
            tool_resources = getattr(self._resources, "tool_resource_text_by_path", None)

        if tool_resources is None or res_path not in tool_resources:
            return "RESOURCE_NOT_ALLOWED"

        content = tool_resources[res_path]

        # Check repeated read
        if res_path in self._read_resources_map:
            return "RESOURCE_ALREADY_READ"

        # Check both the global prompt budget and the dedicated knowledge budget.
        # This prevents tool-driven context from filling the entire model window.
        new_length = len(content)
        if self._current_read_chars + new_length > self._max_resource_chars:
            return "RESOURCE_BUDGET_EXCEEDED"
        if self._initial_context_chars + self._current_read_chars + new_length > self._max_context_chars:
            return "RESOURCE_CONTEXT_TOO_LARGE"

        # Record successful read
        self._read_resources_map[res_path] = content
        self._current_read_chars += new_length

        return content

    def get_read_resources(self) -> Mapping[str, str]:
        return self._read_resources_map

    def getReadResources(self) -> Mapping[str, str]:
        return self.get_read_resources()
