"""Local V2 server using real model calls through the authenticated omp CLI.

Run: .venv/bin/python scripts/mandate_risk_v2_omp_server.py
Binds to localhost:8002 by default; OMP_SERVER_PORT can override the port.
OMP_EVIDENCE_DIR stores model call records without changing other providers.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
import shutil
import signal
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.config import AppConfig
from app.main import create_app
from app.provider.fixed_provider import ModelStreamChunk, is_aborted

logger = logging.getLogger("omp-runtime")
EVIDENCE = Path(os.getenv("OMP_EVIDENCE_DIR", str(ROOT / ".runtime/omp-runtime"))).expanduser().resolve()


def parse_assistant(message: dict) -> tuple[str, dict]:
    if message.get("stopReason") in {"error", "aborted", "length"}:
        raise RuntimeError(f"OMP_MODEL_FAILED: {message.get('errorMessage') or message['stopReason']}")
    text = "".join(item.get("text", "") for item in message.get("content", [])
                   if item.get("type") == "text")
    if not text.strip():
        raise RuntimeError("OMP_EMPTY_RESPONSE")
    usage = message.get("usage") or {}
    return text, {
        "prompt_tokens": usage.get("input", 0) + usage.get("cacheRead", 0),
        "completion_tokens": usage.get("output", 0),
        "total_tokens": usage.get("totalTokens", 0),
    }


class OmpTestProvider:
    def __init__(self):
        self.model_name = os.getenv("OMP_TEST_MODEL", "").strip()

    @property
    def runtime_info(self):
        return {"provider": "omp", "model": self.model_name or "OMP 默认配置（由 CLI 决定）"}

    async def run_skill(self, request):
        if is_aborted(request.signal):
            raise RuntimeError("ABORTED")
        executable = shutil.which("omp")
        if executable is None:
            raise RuntimeError("OMP_NOT_INSTALLED")
        call_id = uuid.uuid4().hex
        timeout = request.timeout_seconds or 240
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        stage = request.user_prompt.splitlines()[0][:100]
        logger.info("OMP %s start %s", call_id[:8], stage)
        with tempfile.TemporaryDirectory(prefix="vmchat-omp-") as directory:
            workdir = Path(directory)
            (workdir / "system.txt").write_text(request.system_prompt, encoding="utf-8")
            (workdir / "request.txt").write_text(request.user_prompt, encoding="utf-8")
            command = [executable, "-p", "--no-session", "--no-tools", "--no-extensions",
                       "--no-skills", "--no-rules", "--no-lsp", "--no-pty", "--no-title",
                       "--thinking", os.getenv("OMP_TEST_THINKING", "low"), "--mode", "json", "--system-prompt",
                       str(workdir / "system.txt"), "@" + str(workdir / "request.txt")]
            if self.model_name:
                command[1:1] = ["--model", self.model_name]
            with (EVIDENCE / f"{call_id}.stderr").open("wb") as stderr:
                process = await asyncio.create_subprocess_exec(
                    *command, cwd=directory, stdout=asyncio.subprocess.PIPE, stderr=stderr,
                    start_new_session=True, limit=4 * 1024 * 1024,
                )
                message = None

                async def collect():
                    nonlocal message
                    async for line in process.stdout:
                        if is_aborted(request.signal):
                            raise RuntimeError("ABORTED")
                        try:
                            event = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant":
                            message = event["message"]
                    return await process.wait()

                try:
                    returncode = await asyncio.wait_for(collect(), timeout=timeout)
                finally:
                    if process.returncode is None:
                        os.killpg(process.pid, signal.SIGTERM)
                        try:
                            await asyncio.wait_for(process.wait(), timeout=3)
                        except asyncio.TimeoutError:
                            os.killpg(process.pid, signal.SIGKILL)
                            await process.wait()
                if message is None:
                    raise RuntimeError(f"OMP_NO_ASSISTANT_RESULT: exit={returncode}")
                (EVIDENCE / f"{call_id}.json").write_text(json.dumps({
                    "stage": stage, "exit": returncode, "message": message,
                }, ensure_ascii=False, indent=2), encoding="utf-8")
                text, usage = parse_assistant(message)
                if returncode:
                    raise RuntimeError(f"OMP_PROCESS_FAILED: exit={returncode}")
                logger.info("OMP %s complete model=%s tokens=%s", call_id[:8], message.get("model"), usage["total_tokens"])
                yield ModelStreamChunk(content_delta=text, usage=usage, done=True)


def local_app():
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    config = AppConfig(
        llm_model="omp/default", max_prompt_chars=120000,
        session_db_path=str(EVIDENCE / "sessions.sqlite3"),
        artifact_db_path=str(EVIDENCE / "artifacts.sqlite3"),
        knowledge_db_path=str(EVIDENCE / "knowledge.sqlite3"),
        document_db_path=str(EVIDENCE / "documents.sqlite3"),
        document_root=str(EVIDENCE / "documents"),
    )
    return create_app({"config": config, "provider": OmpTestProvider()})


if __name__ == "__main__":
    import uvicorn

    logging.basicConfig(level=logging.INFO)
    uvicorn.run(local_app(), host="127.0.0.1", port=int(os.getenv("OMP_SERVER_PORT", "8002")))
