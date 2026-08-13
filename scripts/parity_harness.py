import asyncio
import json
import httpx
from pathlib import Path

FIXTURES_DIR = Path(__file__).parent.parent / "tests" / "fixtures" / "hermes-contract"

async def _read_raw_stream(
    client: httpx.AsyncClient, url: str, token: str
) -> bytes:
    async with client.stream(
        "GET", url, headers={"Authorization": f"Bearer {token}"}
    ) as response:
        assert response.status_code == 200, (
            f"Expected 200, got {response.status_code}"
        )
        chunks = [chunk async for chunk in response.aiter_raw()]
        return b"".join(chunks)


async def capture_raw_stream(
    url: str, token: str, client: httpx.AsyncClient | None = None
) -> bytes:
    if client is not None:
        return await _read_raw_stream(client, url, token)

    async with httpx.AsyncClient(timeout=60.0) as owned_client:
        return await _read_raw_stream(owned_client, url, token)


def normalize_post_contract(body: dict) -> dict:
    return {key: value for key, value in body.items() if key != "run_id"}


async def capture_run(port: int, req_payload: dict, token: str) -> dict:
    url = f"http://127.0.0.1:{port}/v1/runs"
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(
            url, json=req_payload, headers={"Authorization": f"Bearer {token}"}
        )
        post_body = resp.json()
        result = {
            "status": resp.status_code,
            "post_contract": normalize_post_contract(post_body),
            "events": b"",
        }
        if resp.status_code != 200 or "run_id" not in post_body:
            return result

        run_id = post_body["run_id"]
        result["run_id"] = run_id
        result["events"] = await capture_raw_stream(
            f"http://127.0.0.1:{port}/v1/runs/{run_id}/events",
            token,
            client=client,
        )
        return result

async def run_parity():
    token = "test-token"
    request_payload = json.loads((FIXTURES_DIR / "create-request.json").read_text())

    print("Testing TS server on port 7311...")
    ts_result = await capture_run(7311, request_payload, token)

    print("Testing Py server on port 7310...")
    py_result = await capture_run(7310, request_payload, token)

    assert ts_result["status"] == py_result["status"], (
        f"Status mismatch: TS={ts_result['status']} Py={py_result['status']}"
    )
    assert ts_result["post_contract"] == py_result["post_contract"], (
        "POST contract mismatch:\n"
        f"TS: {ts_result['post_contract']}\n"
        f"Py: {py_result['post_contract']}"
    )

    if ts_result["status"] != 200:
        print("Parity harness matched the non-success POST contract.")
        return

    ts_body = ts_result["events"]
    py_body = py_result["events"]
    print(f"TS response body bytes: {len(ts_body)}")
    print(f"Py response body bytes: {len(py_body)}")
    assert ts_body == py_body, (
        "SSE response body bytes mismatch:\n"
        f"TS: {ts_body!r}\n"
        f"Py: {py_body!r}"
    )
    print("Parity harness matched the complete SSE response body bytes.")
        
if __name__ == "__main__":
    asyncio.run(run_parity())
