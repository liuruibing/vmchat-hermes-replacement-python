#!/usr/bin/env python3
"""
本地 OMP OpenAI 兼容代理网关 (app/provider/omp_openai_gateway.py)
作用：暴露标准 /v1/chat/completions 接口，接收远程 LangChain 请求，
通过本地 omp CLI 调用真实的 Gemini 3.8 Flash，并按 OpenAI 格式返回。
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from pathlib import Path
import shutil
import signal
import tempfile
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("omp-gateway")

app = FastAPI(title="Local OMP OpenAI Proxy Gateway")

DEFAULT_MODEL = os.getenv("OMP_MODEL", "google-antigravity/gemini-3.8-flash")
PORT = int(os.getenv("OMP_GATEWAY_PORT", "8005"))


async def call_omp(system_prompt: str, user_prompt: str, model_name: str = "") -> tuple[str, dict]:
    executable = shutil.which("omp")
    if not executable:
        raise RuntimeError("OMP_NOT_INSTALLED: 未在本地找到 omp 命令行工具")

    model = model_name or DEFAULT_MODEL
    call_id = uuid.uuid4().hex[:8]
    logger.info("OMP [%s] 任务发起, 模型: %s", call_id, model)

    with tempfile.TemporaryDirectory(prefix="omp-call-") as directory:
        workdir = Path(directory)
        # --no-tools disables built-ins, not MCP discovery. Shadow only the
        # locally configured rea server; never change the user's global config.
        mcp_dir = workdir / ".omp"
        mcp_dir.mkdir()
        (mcp_dir / "mcp.json").write_text(
            json.dumps({"mcpServers": {"rea": {
                "type": "stdio", "command": "npx", "enabled": False,
            }}}),
            encoding="utf-8",
        )
        (workdir / "system.txt").write_text(system_prompt or "You are a helpful assistant.", encoding="utf-8")
        (workdir / "request.txt").write_text(user_prompt or "", encoding="utf-8")

        command = [
            executable,
            "-p",
            "--no-session",
            "--no-tools",
            "--no-extensions",
            "--no-skills",
            "--no-rules",
            "--no-lsp",
            "--no-pty",
            "--no-title",
            "--thinking",
            os.getenv("OMP_THINKING", "low"),
            "--mode",
            "json",
            "--system-prompt",
            str(workdir / "system.txt"),
            "@" + str(workdir / "request.txt"),
        ]
        if model:
            command[1:1] = ["--model", model]

        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=directory,
            stdin=asyncio.subprocess.DEVNULL,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            start_new_session=True,
            limit=8 * 1024 * 1024,
        )

        message = None
        stderr_reader = asyncio.create_task(process.stderr.read())
        try:
            async for line in process.stdout:
                try:
                    event = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if event.get("type") == "message_end" and event.get("message", {}).get("role") == "assistant":
                    message = event["message"]
            await process.wait()
            stderr_data = await stderr_reader
        finally:
            if process.returncode is None:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                await process.wait()
            await stderr_reader
        model_error = str((message or {}).get("errorMessage") or "").strip()
        stop_reason = (message or {}).get("stopReason")
        if process.returncode != 0 or stop_reason in {"error", "aborted", "length"}:
            err_msg = model_error or stderr_data.decode("utf-8", errors="replace").strip()
            err_msg = err_msg or f"stopReason={stop_reason or 'unknown'}; no error details emitted"
            logger.error("OMP [%s] 进程失败 exit=%d: %s", call_id, process.returncode, err_msg)
            raise RuntimeError(f"OMP_PROCESS_FAILED exit={process.returncode}: {err_msg[:2000]}")

        if not message:
            raise RuntimeError("OMP_NO_ASSISTANT_RESULT: 未获取到有效回复")

        content_items = message.get("content", [])
        text = "".join(item.get("text", "") for item in content_items if item.get("type") == "text")
        usage_raw = message.get("usage") or {}
        usage = {
            "prompt_tokens": usage_raw.get("input", 0) + usage_raw.get("cacheRead", 0),
            "completion_tokens": usage_raw.get("output", 0),
            "total_tokens": usage_raw.get("totalTokens", 0),
        }
        logger.info("OMP [%s] 完成! 生成长度: %d 字符, Tokens: %d", call_id, len(text), usage["total_tokens"])
        return text, usage


async def call_until_disconnect(request, system_prompt, user_prompt, model):
    async def disconnected():
        while not await request.is_disconnected():
            await asyncio.sleep(0.25)

    model_task = asyncio.create_task(call_omp(system_prompt, user_prompt, model_name=model))
    disconnect_task = asyncio.create_task(disconnected())
    try:
        done, _ = await asyncio.wait(
            {model_task, disconnect_task}, return_when=asyncio.FIRST_COMPLETED)
        if disconnect_task in done:
            raise asyncio.CancelledError()
        return await model_task
    finally:
        model_task.cancel()
        disconnect_task.cancel()
        await asyncio.gather(model_task, disconnect_task, return_exceptions=True)


@app.get("/health")
@app.get("/v1/health")
async def health():
    return {"status": "ok", "provider": "omp-gateway", "model": DEFAULT_MODEL}


@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": DEFAULT_MODEL,
                "object": "model",
                "created": int(time.time()),
                "owned_by": "omp",
            }
        ],
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        body = await request.json()
    except Exception as err:
        return JSONResponse(status_code=400, content={"error": f"Invalid JSON body: {err}"})

    messages = body.get("messages", [])
    model = body.get("model", DEFAULT_MODEL)
    stream = body.get("stream", False)

    # 提取系统提示词和用户提示词
    system_parts = []
    user_parts = []
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if isinstance(content, list):
            content = "".join(c.get("text", "") for c in content if isinstance(c, dict))
        if role == "system":
            system_parts.append(str(content))
        elif role == "user":
            user_parts.append(str(content))
        elif role == "assistant":
            user_parts.append(f"\n[Assistant]: {content}")

    system_prompt = "\n\n".join(system_parts)
    user_prompt = "\n\n".join(user_parts)

    try:
        text, usage = await call_until_disconnect(request, system_prompt, user_prompt, model)
    except Exception as exc:
        logger.exception("调用本地 OMP 出错")
        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "message": str(exc),
                    "type": "omp_error",
                    "code": "internal_error",
                }
            },
        )

    completion_id = f"chatcmpl-{uuid.uuid4().hex}"
    created_ts = int(time.time())

    # 流式模式（LangChain 开启 streaming 时）
    if stream:
        async def event_generator():
            # 发送角色头
            first_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_ts,
                "model": model,
                "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}],
            }
            yield f"data: {json.dumps(first_chunk, ensure_ascii=False)}\n\n"

            # 发送内容
            content_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_ts,
                "model": model,
                "choices": [{"index": 0, "delta": {"content": text}, "finish_reason": None}],
            }
            yield f"data: {json.dumps(content_chunk, ensure_ascii=False)}\n\n"

            # 发送结束
            end_chunk = {
                "id": completion_id,
                "object": "chat.completion.chunk",
                "created": created_ts,
                "model": model,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
                "usage": usage,
            }
            yield f"data: {json.dumps(end_chunk, ensure_ascii=False)}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # 非流式模式
    return {
        "id": completion_id,
        "object": "chat.completion",
        "created": created_ts,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": text,
                },
                "finish_reason": "stop",
            }
        ],
        "usage": usage,
    }


if __name__ == "__main__":
    logger.info("启动本地 OMP OpenAI 代理网关, 监听端口: %d", PORT)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
