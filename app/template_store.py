"""持久化 vmChat 自定义模块、组合模块和布局模板。"""

from __future__ import annotations

import copy
import json
import os
import threading
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


class TemplateStore:
    """使用 JSON 文件保存模板，写入采用临时文件替换，避免半写文件。"""

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self._lock = threading.RLock()
        self._templates: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        with self._lock:
            if not self.path.exists():
                return
            try:
                payload = json.loads(self.path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                # 文件损坏时不阻断服务启动；下一次保存会生成合法文件。
                self._templates = []
                return
            source = payload.get("templates") if isinstance(payload, dict) else payload
            self._templates = self._normalize_list(source)

    @staticmethod
    def _normalize_list(source: Any) -> List[Dict[str, Any]]:
        if not isinstance(source, list):
            return []
        result: List[Dict[str, Any]] = []
        seen = set()
        for item in source:
            if not isinstance(item, dict):
                continue
            template_id = str(item.get("id") or "").strip()
            entity_type = str(item.get("entityType") or "").strip()
            if not template_id or not entity_type or template_id in seen:
                continue
            seen.add(template_id)
            result.append(copy.deepcopy(item))
        return result

    def _write(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_name(self.path.name + ".tmp")
        content = json.dumps({"templates": self._templates}, ensure_ascii=False, indent=2)
        temp_path.write_text(content + "\n", encoding="utf-8")
        os.replace(temp_path, self.path)

    def list(self) -> List[Dict[str, Any]]:
        with self._lock:
            return copy.deepcopy(self._templates)

    def get(self, template_id: str) -> Optional[Dict[str, Any]]:
        normalized_id = str(template_id or "").strip()
        with self._lock:
            for item in self._templates:
                if item.get("id") == normalized_id:
                    return copy.deepcopy(item)
        return None

    def replace_all(self, templates: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = self._normalize_list(list(templates) if templates is not None else [])
        with self._lock:
            self._templates = normalized
            self._write()
            return copy.deepcopy(self._templates)

    def upsert(self, template: Dict[str, Any], template_id: Optional[str] = None) -> Dict[str, Any]:
        if not isinstance(template, dict):
            raise ValueError("template must be an object")
        item = copy.deepcopy(template)
        normalized_id = str(template_id or item.get("id") or "").strip()
        entity_type = str(item.get("entityType") or "").strip()
        if not normalized_id:
            raise ValueError("template.id is required")
        if not entity_type:
            raise ValueError("template.entityType is required")
        item["id"] = normalized_id
        with self._lock:
            index = next((i for i, current in enumerate(self._templates) if current.get("id") == normalized_id), -1)
            if index >= 0:
                self._templates[index] = item
            else:
                self._templates.insert(0, item)
            self._write()
            return copy.deepcopy(item)

    def delete(self, template_id: str) -> bool:
        normalized_id = str(template_id or "").strip()
        with self._lock:
            original_length = len(self._templates)
            self._templates = [item for item in self._templates if item.get("id") != normalized_id]
            changed = len(self._templates) != original_length
            if changed:
                self._write()
            return changed
