from __future__ import annotations

import json
from typing import Any, Dict


def extract_first_json_object(text: str) -> Dict[str, Any]:
    raw = str(text or "")
    start = raw.find("{")
    if start < 0:
        raise ValueError("MODEL_JSON_NOT_FOUND")

    depth = 0
    in_string = False
    escaped = False
    for index in range(start, len(raw)):
        ch = raw[index]
        if escaped:
            escaped = False
            continue
        if ch == "\\":
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                parsed = json.loads(raw[start : index + 1])
                if not isinstance(parsed, dict):
                    raise ValueError("MODEL_JSON_OBJECT_REQUIRED")
                return parsed
    raise ValueError("MODEL_JSON_UNBALANCED")
