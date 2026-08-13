import json
from pathlib import Path
from typing import Any, Dict, List

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "hermes-contract"

def parse_sse_stream(sse_content: str) -> Dict[str, Any]:
    lines = sse_content.splitlines()
    events: List[Dict[str, Any]] = []
    accumulated_content = ""
    final_output = ""
    usage = None
    is_failed = False
    error_message = ""

    for line in lines:
        trimmed = line.strip()
        if not trimmed or not trimmed.startswith("data:"):
            continue
        json_str = trimmed[5:].strip()
        try:
            payload = json.loads(json_str)
            events.append({"event": payload.get("event"), "payload": payload})

            if payload.get("event") == "message.delta":
                accumulated_content += payload.get("delta", "")
            elif payload.get("event") == "run.completed":
                final_output = payload.get("output") or accumulated_content
                usage = payload.get("usage")
            elif payload.get("event") == "run.failed":
                is_failed = True
                error_message = payload.get("error") or "Execution failed"
        except json.JSONDecodeError:
            pass

    return {
        "events": events,
        "accumulated_content": accumulated_content,
        "final_output": final_output,
        "usage": usage,
        "is_failed": is_failed,
        "error_message": error_message,
    }


def test_replays_create_success_sse():
    content = (FIXTURES_DIR / "create-success.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert not parsed["is_failed"]
    assert len(parsed["events"]) == 2
    assert parsed["accumulated_content"] == parsed["final_output"]
    dsl = json.loads(parsed["final_output"])
    assert dsl["action"] == "create"
    assert dsl["requests"][0]["moduleId"] == "stockNetExposureTiming"


def test_replays_update_success_sse():
    content = (FIXTURES_DIR / "update-success.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert not parsed["is_failed"]
    dsl = json.loads(parsed["final_output"])
    assert dsl["action"] == "update"
    assert dsl["targetBlockId"] == "block-001"


def test_replays_clarification_sse():
    content = (FIXTURES_DIR / "clarification.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert not parsed["is_failed"]
    assert "期货十大盈利品种" in parsed["final_output"]


def test_replays_rejection_sse():
    content = (FIXTURES_DIR / "rejection.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert not parsed["is_failed"]
    assert "删除按钮" in parsed["final_output"]


def test_replays_provider_error_sse():
    content = (FIXTURES_DIR / "provider-error.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert parsed["is_failed"]
    assert "模型调用异常" in parsed["error_message"]


def test_replays_disconnected_partial_sse():
    content = (FIXTURES_DIR / "disconnected-partial.sse").read_text(encoding="utf8")
    parsed = parse_sse_stream(content)

    assert not parsed["is_failed"]
    assert parsed["final_output"] == ""
    assert "未完成的流" in parsed["accumulated_content"]
