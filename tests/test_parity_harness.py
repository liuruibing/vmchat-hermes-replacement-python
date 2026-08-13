import sys
from pathlib import Path

import httpx
import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from scripts.parity_harness import capture_raw_stream, normalize_post_contract


@pytest.mark.anyio
async def test_capture_raw_stream_preserves_response_bytes():
    expected = b"data: {\"event\":\"run.completed\"}\r\n\r\n"

    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, stream=httpx.ByteStream(expected))

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        captured = await capture_raw_stream(
            "http://test.local/events", "test-token", client=client
        )

    assert captured == expected


def test_normalize_post_contract_ignores_only_run_id():
    response = {"run_id": "dynamic", "status": "queued", "session_id": "same"}

    assert normalize_post_contract(response) == {
        "status": "queued",
        "session_id": "same",
    }
