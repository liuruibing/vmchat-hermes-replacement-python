#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from jsonschema.validators import validator_for


def format_path(parts):
    if not parts:
        return "$"
    result = "$"
    for part in parts:
        result += f"[{part}]" if isinstance(part, int) else f".{part}"
    return result


def leaf_errors(error):
    if not error.context:
        return [error]
    result = []
    for child in error.context:
        result.extend(leaf_errors(child))
    return result


def main():
    if len(sys.argv) != 3:
        raise SystemExit("用法：validate-schema.py <schema.json> <dsl.json>")
    schema = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    instance = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    validator = validator_class(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        detail = error.message
        if error.context:
            leaf = sorted(leaf_errors(error), key=lambda item: len(list(item.absolute_path)), reverse=True)[0]
            detail = leaf.message
            path = format_path(leaf.absolute_path)
        else:
            path = format_path(error.absolute_path)
        raise SystemExit(f"DSL Schema 校验失败：{path} {detail}")
    print("DSL Schema 校验通过")


if __name__ == "__main__":
    main()
