from dataclasses import dataclass, field
from typing import Any, Optional
from pydantic import BaseModel, Field


class ManifestFileEntry(BaseModel):
    path: str
    sha256: str


class Manifest(BaseModel):
    schemaVersion: str = Field(..., alias="schemaVersion")
    catalogVersion: str = Field(..., alias="catalogVersion")
    moduleCount: int = Field(..., alias="moduleCount")
    files: list[ManifestFileEntry]

    model_config = {"populate_by_name": True}

    @property
    def schema_version(self) -> str:
        return self.schemaVersion

    @property
    def catalog_version(self) -> str:
        return self.catalogVersion

    @property
    def module_count(self) -> int:
        return self.moduleCount


@dataclass
class LoadedResources:
    manifest: Manifest
    skillMd: str
    schemaJson: dict[str, Any]
    catalogContract: dict[str, Any]
    catalogIndexMd: str
    catalogMetricsMd: str
    submodulesJson: Optional[list[Any]]
    moduleMarkdownMap: dict[str, str]
    toolResourceTextByPath: dict[str, str]
    moduleProfiles: dict[str, dict[str, Any]] = field(default_factory=dict)
    profileIndex: dict[str, Any] = field(default_factory=dict)

    @property
    def skill_md(self) -> str:
        return self.skillMd

    @property
    def schema_json(self) -> dict[str, Any]:
        return self.schemaJson

    @property
    def catalog_contract(self) -> dict[str, Any]:
        return self.catalogContract

    @property
    def catalog_index_md(self) -> str:
        return self.catalogIndexMd

    @property
    def catalog_metrics_md(self) -> str:
        return self.catalogMetricsMd

    @property
    def submodules_json(self) -> Optional[list[Any]]:
        return self.submodulesJson

    @property
    def module_markdown_map(self) -> dict[str, str]:
        return self.moduleMarkdownMap

    @property
    def tool_resource_text_by_path(self) -> dict[str, str]:
        return self.toolResourceTextByPath

    @property
    def module_profiles(self) -> dict[str, dict[str, Any]]:
        return self.moduleProfiles

    @property
    def profile_index(self) -> dict[str, Any]:
        return self.profileIndex
