import json
from pathlib import Path
from typing import Any, Dict

from app.compatibility.hermes_events import serialize_sse_event

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "hermes-contract"
def extract_raw_events_from_sse(sse_content: str) -> list[tuple[str, Dict[str, Any]]]:
    events = []
    for line in sse_content.splitlines():
        trimmed = line.strip()
        if not trimmed or not trimmed.startswith("data:"):
            continue
        json_str = trimmed[5:].strip()
        try:
            payload = json.loads(json_str)
            # Store the EXACT line from the file (plus standard SSE newlines)
            expected_raw = f"{trimmed}\n\n"
            events.append((expected_raw, payload))
        except json.JSONDecodeError:
            pass
    return events

def test_serialize_matches_wire_bytes():
    """
    Ensure that serializing an event in Python produces the exact same wire bytes
    as the original Node.js backend (no extra spaces, exact field names).
    """
    files_tested = list(FIXTURES_DIR.glob("*.sse"))
    assert len(files_tested) >= 6, f"Expected at least 6 fixture files, found {len(files_tested)} in {FIXTURES_DIR}"

    for file_path in files_tested:
        content = file_path.read_text(encoding="utf8")
        events = extract_raw_events_from_sse(content)
        
        for expected_raw, payload in events:
            # We recreate the wire bytes in Python
            python_wire = serialize_sse_event(payload)
            
            assert python_wire == expected_raw, f"Serialization mismatch in {file_path.name}:\nExpected: {repr(expected_raw)}\nGot: {repr(python_wire)}"
