"""Run V2 PDF upload -> run -> SSE against an explicitly selected backend.

Example:
  python scripts/mandate_risk_v2_remote_e2e.py --base-url http://127.0.0.1:8002 \
      --model deepseek-v4-flash --pdf /path/fixed.pdf --pdf /path/equity.pdf
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
import uuid
from pathlib import Path
from urllib.request import Request, urlopen


def terminal_event(lines, *, progress=None):
    for line in lines:
        if not line.startswith(b"data: "):
            continue
        event = json.loads(line[6:])
        if event.get("event") == "reasoning.delta" and progress:
            progress(str(event.get("delta") or ""))
        if event.get("event") in {"run.completed", "run.failed"}:
            return event
    raise RuntimeError("SSE stream ended without terminal event")


def _request(url: str, *, body: bytes | None = None, content_type: str | None = None,
             timeout: int = 900):
    headers = {"Accept": "application/json"}
    if content_type:
        headers["Content-Type"] = content_type
    token = os.getenv("MANDATE_RISK_E2E_BEARER_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return urlopen(Request(url, data=body, headers=headers), timeout=timeout)


def run_one(base_url: str, pdf: Path, model: str, timeout: int):
    raw = pdf.read_bytes()
    boundary = f"mandate-v2-{uuid.uuid4().hex}"
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; "
            f"filename=\"{pdf.name}\"\r\nContent-Type: application/pdf\r\n\r\n").encode() + raw + \
           f"\r\n--{boundary}--\r\n".encode()
    started = time.monotonic()
    with _request(f"{base_url}/v1/documents", body=body,
                  content_type=f"multipart/form-data; boundary={boundary}", timeout=timeout) as response:
        document_id = json.load(response)["document"]["document_id"]
    payload = {
        "agent_id": "mandate-risk-v2-lab", "role_id": "requirement-analyst",
        "workflow": "mandate-risk-analysis-v2", "model": model,
        "session_id": f"mandate-v2-e2e-{uuid.uuid4().hex}",
        "input": [{"role": "user", "content": "请依据合同原文和原始指标库完成 V2 风险指标映射。"}],
        "documents": [document_id],
    }
    with _request(f"{base_url}/v1/runs", body=json.dumps(payload).encode("utf-8"),
                  content_type="application/json", timeout=timeout) as response:
        run_id = json.load(response)["run_id"]
    headers = {"Accept": "text/event-stream"}
    token = os.getenv("MANDATE_RISK_E2E_BEARER_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    with urlopen(Request(f"{base_url}/v1/runs/{run_id}/events", headers=headers),
                 timeout=timeout) as response:
        terminal = terminal_event(response, progress=lambda message: print(
            f"[progress] {pdf.name}: {message}", file=sys.stderr, flush=True,
        ))
    output = terminal.get("output") or ""
    return {
        "pdf": str(pdf), "sha256": hashlib.sha256(raw).hexdigest(),
        "run_id": run_id, "event": terminal["event"],
        "error": terminal.get("error"), "usage": terminal.get("usage"),
        "elapsed_seconds": round(time.monotonic() - started, 2),
        "has_six_column_table": (
            "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in output
        ),
        "output": output,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--pdf", type=Path, action="append", required=True)
    parser.add_argument("--report-dir", type=Path)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    if args.report_dir:
        args.report_dir.mkdir(parents=True, exist_ok=True)
    failed = False
    for pdf in args.pdf:
        result = run_one(args.base_url.rstrip("/"), pdf, args.model, args.timeout)
        output = result.pop("output")
        if args.report_dir and output:
            report_path = args.report_dir / f"{result['run_id']}.md"
            report_path.write_text(output, encoding="utf-8")
            result["report_path"] = str(report_path)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        failed |= result["event"] != "run.completed" or not result["has_six_column_table"]
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
