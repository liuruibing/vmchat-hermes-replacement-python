import asyncio
import hashlib
import json
import os
from typing import Any, Optional
from app.resources.resource_types import LoadedResources, Manifest
from app.resources.module_profile_builder import (
    MERGE_GUIDANCE_V2,
    build_module_profiles,
    build_profile_index,
)


def _get_all_relative_files(dir_path: str, base_dir: Optional[str] = None) -> list[str]:
    if base_dir is None:
        base_dir = dir_path
    results: list[str] = []
    try:
        entries = sorted(os.scandir(dir_path), key=lambda e: e.name)
    except FileNotFoundError:
        return results

    for entry in entries:
        full = os.path.join(dir_path, entry.name)
        if entry.is_dir(follow_symlinks=False):
            results.extend(_get_all_relative_files(full, base_dir))
        elif entry.is_file(follow_symlinks=False) or entry.is_symlink():
            rel = os.path.relpath(full, base_dir).replace("\\", "/")
            if rel != "manifest.json":
                results.append(rel)
    return results


class ResourceLoader:
    def __init__(self, resources_dir: Optional[str] = None, resourcesDir: Optional[str] = None) -> None:
        chosen_dir = resources_dir or resourcesDir
        if not chosen_dir:
            chosen_dir = os.path.join(os.getcwd(), "resources")
        self._resources_dir = os.path.abspath(chosen_dir)
        self._ready = False
        self._resources: Optional[LoadedResources] = None

    def is_ready(self) -> bool:
        return self._ready

    def isReady(self) -> bool:
        return self.is_ready()

    def get_resources(self) -> LoadedResources:
        if not self._ready or self._resources is None:
            raise RuntimeError("NOT_READY: ResourceLoader has not loaded valid resources")
        return self._resources

    def getResources(self) -> LoadedResources:
        return self.get_resources()

    def load_sync(self) -> LoadedResources:
        self._ready = False
        self._resources = None

        manifest_path = os.path.join(self._resources_dir, "manifest.json")
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest_raw = f.read()
        except Exception:
            raise RuntimeError(f"MISSING_MANIFEST: manifest.json not found at {manifest_path}")

        try:
            manifest_dict = json.loads(manifest_raw)
        except Exception as err:
            throw_msg = str(err)
            raise RuntimeError(f"INVALID_MANIFEST: Failed to parse manifest.json: {throw_msg}")

        if not isinstance(manifest_dict, dict) or not isinstance(manifest_dict.get("files"), list):
            raise RuntimeError("INVALID_MANIFEST: manifest.files is not an array")

        try:
            manifest = Manifest.model_validate(manifest_dict)
        except Exception as err:
            raise RuntimeError(f"INVALID_MANIFEST: Failed to parse manifest.json: {err}")

        manifest_paths: set[str] = set()
        file_content_map: dict[str, bytes] = {}

        for entry in manifest.files:
            if not entry.path or os.path.isabs(entry.path) or entry.path.startswith(".."):
                raise RuntimeError(f"UNSAFE_PATH: Manifest contains unsafe path '{entry.path}'")

            full_path = os.path.abspath(os.path.join(self._resources_dir, entry.path))
            rel_to_root = os.path.relpath(full_path, self._resources_dir).replace("\\", "/")
            if rel_to_root.startswith("..") or os.path.isabs(rel_to_root):
                raise RuntimeError(f"UNSAFE_PATH: Path '{entry.path}' escapes resources root")

            if not os.path.lexists(full_path):
                raise RuntimeError(f"MISSING_RESOURCE_FILE: File '{entry.path}' listed in manifest is missing")

            if os.path.islink(full_path):
                raise RuntimeError(f"SYMLINK_NOT_ALLOWED: Path '{entry.path}' is a symbolic link")

            with open(full_path, "rb") as f:
                buffer = f.read()

            computed_hash = hashlib.sha256(buffer).hexdigest()
            if computed_hash != entry.sha256:
                raise RuntimeError(
                    f"CHECKSUM_MISMATCH: File '{entry.path}' hash '{computed_hash}' disagrees with manifest '{entry.sha256}'"
                )

            manifest_paths.add(entry.path)
            file_content_map[entry.path] = buffer

        # Unlisted files check
        existing_files = _get_all_relative_files(self._resources_dir)
        for existing in existing_files:
            if existing not in manifest_paths:
                raise RuntimeError(f"UNLISTED_RESOURCE_FILE: Unlisted resource file found at '{existing}'")

        # Required files check
        required_files = [
            "skill/SKILL.md",
            "schemas/dsl.schema.json",
            "catalog/execution-contract.json",
            "catalog/index.md",
            "catalog/metrics.md",
        ]
        for req in required_files:
            if req not in file_content_map:
                raise RuntimeError(f"MISSING_RESOURCE_FILE: Required resource file '{req}' is missing from manifest")

        # Read & parse schemaJson
        schema_buffer = file_content_map["schemas/dsl.schema.json"]
        try:
            schema_json = json.loads(schema_buffer.decode("utf-8"))
        except Exception as err:
            raise RuntimeError(f"INVALID_JSON: Failed to parse schemas/dsl.schema.json: {err}")

        # Read & parse catalogContract
        contract_buffer = file_content_map["catalog/execution-contract.json"]
        try:
            catalog_contract = json.loads(contract_buffer.decode("utf-8"))
        except Exception as err:
            raise RuntimeError(f"INVALID_JSON: Failed to parse catalog/execution-contract.json: {err}")

        modules_obj = catalog_contract.get("modules", {})
        if not isinstance(modules_obj, dict):
            modules_obj = {}
        module_keys = list(modules_obj.keys())
        if manifest.moduleCount != len(module_keys):
            raise RuntimeError(
                f"MODULE_COUNT_MISMATCH: Manifest moduleCount ({manifest.moduleCount}) disagrees with contract ({len(module_keys)})"
            )

        # Check module sqlCode integrity
        known_catalog_ids: set[str] = set()
        for module_id in module_keys:
            mod_meta = modules_obj.get(module_id)
            if (
                not mod_meta
                or not isinstance(mod_meta, dict)
                or not mod_meta.get("sqlCode")
                or not isinstance(mod_meta.get("sqlCode"), str)
                or not mod_meta.get("sqlCode").strip()
            ):
                raise RuntimeError(f"MISSING_SQL_CODE: Module '{module_id}' is missing sqlCode")
            known_catalog_ids.add(module_id)

        # Load & check module markdowns
        module_markdown_map: dict[str, str] = {}
        for module_id in module_keys:
            rel_path = f"catalog/modules/{module_id}.md"
            mod_buf = file_content_map.get(rel_path)
            if not mod_buf or not mod_buf.decode("utf-8").strip():
                raise RuntimeError(f"MISSING_MODULE_MARKDOWN: {rel_path} is missing or empty")
            module_markdown_map[module_id] = mod_buf.decode("utf-8")

        # Build runtime semantic profiles from existing catalog markdowns.
        # The optional delivery SQL document is outside the signed resources tree:
        # it is used only as additional evidence and is never exposed raw to the model.
        repo_root = os.path.abspath(os.path.join(self._resources_dir, os.pardir))
        sql_document_path = os.path.join(
            repo_root, "delivery", "02_vm_modules_sql_statements.md"
        )
        sql_document = ""
        if os.path.isfile(sql_document_path):
            try:
                with open(sql_document_path, "r", encoding="utf-8") as f:
                    sql_document = f.read()
            except Exception:
                sql_document = ""

        module_profiles = build_module_profiles(
            module_markdown_map=module_markdown_map,
            sql_document=sql_document,
        )
        profile_index = build_profile_index(module_profiles)

        skill_buf = file_content_map["skill/SKILL.md"]
        catalog_index_buf = file_content_map["catalog/index.md"]
        catalog_metrics_buf = file_content_map["catalog/metrics.md"]
        submodules_buf = file_content_map.get("catalog/submodules.json")

        submodules_json: Optional[list[Any]] = None
        if submodules_buf is not None:
            try:
                submodules_json = json.loads(submodules_buf.decode("utf-8"))
            except Exception as err:
                raise RuntimeError(f"INVALID_JSON: Failed to parse catalog/submodules.json: {err}")

            if isinstance(submodules_json, list):
                for sub in submodules_json:
                    if isinstance(sub, dict):
                        sub_id = sub.get("id")
                        if sub_id:
                            if sub_id in known_catalog_ids:
                                raise RuntimeError(f"DUPLICATE_CATALOG_ID: Duplicate catalog id '{sub_id}'")
                            known_catalog_ids.add(sub_id)
                        sub_module_id = sub.get("moduleId")
                        if sub_module_id and sub_module_id not in modules_obj:
                            raise RuntimeError(
                                f"INVALID_SUBMODULE_PARENT: Submodule '{sub_id or 'unknown'}' references invalid parent module '{sub_module_id}'"
                            )

        # Construct whitelist toolResourceTextByPath
        tool_resource_map: dict[str, str] = {}
        tool_resource_map["catalog/index.md"] = catalog_index_buf.decode("utf-8")
        tool_resource_map["catalog/metrics.md"] = catalog_metrics_buf.decode("utf-8")
        tool_resource_map["catalog/execution-contract.json"] = contract_buffer.decode("utf-8")
        if submodules_buf is not None:
            tool_resource_map["catalog/submodules.json"] = submodules_buf.decode("utf-8")

        for mod_id, content in module_markdown_map.items():
            tool_resource_map[f"catalog/modules/{mod_id}.md"] = content

        # Generated semantic resources are virtual resources: they are derived from
        # already verified catalog files, so they do not need manifest entries.
        tool_resource_map["catalog/profile-index.json"] = json.dumps(
            profile_index,
            ensure_ascii=False,
            indent=2,
        )
        for mod_id, profile in module_profiles.items():
            tool_resource_map[f"catalog/profiles/{mod_id}.json"] = json.dumps(
                profile,
                ensure_ascii=False,
                indent=2,
            )
        tool_resource_map["skill/references/merge-guidance-v2.md"] = MERGE_GUIDANCE_V2

        allowed_references = [
            "skill/references/dsl-spec.md",
            "skill/references/dsl-table.md",
            "skill/references/dsl-echarts.md",
            "skill/references/merge-rules.md",
        ]
        for ref_path in allowed_references:
            ref_buf = file_content_map.get(ref_path)
            if ref_buf is not None:
                tool_resource_map[ref_path] = ref_buf.decode("utf-8")

        self._resources = LoadedResources(
            manifest=manifest,
            skillMd=skill_buf.decode("utf-8"),
            schemaJson=schema_json,
            catalogContract=catalog_contract,
            catalogIndexMd=catalog_index_buf.decode("utf-8"),
            catalogMetricsMd=catalog_metrics_buf.decode("utf-8"),
            submodulesJson=submodules_json,
            moduleMarkdownMap=module_markdown_map,
            toolResourceTextByPath=tool_resource_map,
        )

        self._ready = True
        return self._resources

    async def load(self) -> LoadedResources:
        return await asyncio.to_thread(self.load_sync)
