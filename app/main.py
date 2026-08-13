import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
import hmac
import logging
from typing import Any, Dict, Optional

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from app.config import AppConfig, load_config
from app.compatibility.hermes_events import serialize_sse_event
from app.compatibility.hermes_request import (
    GlobalQueryParameters,
    VmChatInput,
    normalize_create_run_request,
    normalize_vm_chat_input,
)
from app.contracts.types import VmChatRunError
from app.resources.resource_loader import ResourceLoader
from app.runs.run_limiter import RunLimiter
from app.runs.run_store import RunStore
from app.runs.run_types import AbortController

from app.provider.fixed_provider import FixedVmChatProvider, VmChatModelProvider
from app.provider.langchain_provider import LangChainVmChatProvider
from app.orchestrator.vmchat_orchestrator import stream_vm_chat
from app.resources.wiki_catalog import get_wiki_tree, get_wiki_document

logger = logging.getLogger("app")


class ActiveRunRegistry:
    def __init__(self):
        self._controllers: Dict[str, Any] = {}

    def register(self, id_: str, controller: Any) -> None:
        self._controllers[id_] = controller

    def unregister(self, id_: str) -> None:
        self._controllers.pop(id_, None)

    def abort_all(self) -> None:
        for controller in list(self._controllers.values()):
            if hasattr(controller, "abort") and callable(controller.abort):
                try:
                    controller.abort()
                except Exception:
                    pass
            elif hasattr(controller, "cancel") and callable(controller.cancel):
                try:
                    controller.cancel()
                except Exception:
                    pass
        self._controllers.clear()

    # Alias for JS camelCase
    def abortAll(self) -> None:
        self.abort_all()


ActiveRunRegistryImpl = ActiveRunRegistry


@dataclass
class AppDependencies:
    config: AppConfig
    resource_loader: Any
    run_store: Any
    run_limiter: Any
    provider: Any
    active_registry: Optional[ActiveRunRegistry] = None

    @property
    def resourceLoader(self):
        return self.resource_loader

    @property
    def runStore(self):
        return self.run_store

    @property
    def runLimiter(self):
        return self.run_limiter

    @property
    def activeRegistry(self):
        return self.active_registry


def verify_bearer_auth(request: Request, api_key: str) -> bool:
    if not api_key:
        return True
    if request.method == "OPTIONS":
        return True

    auth_header = request.headers.get("authorization") or request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header[7:].strip()
    token_bytes = token.encode("utf-8")
    key_bytes = api_key.encode("utf-8")

    return hmac.compare_digest(token_bytes, key_bytes)


# Alias for JS camelCase compatibility
verifyBearerAuth = verify_bearer_auth


def create_app(deps_override: Optional[Dict[str, Any]] = None) -> FastAPI:
    if deps_override is None:
        deps_override = {}

    config = deps_override.get("config") or load_config()
    resource_loader = deps_override.get("resource_loader") or deps_override.get("resourceLoader") or ResourceLoader()
    run_store = deps_override.get("run_store") or deps_override.get("runStore") or RunStore(max_stored_runs=config.max_stored_runs)
    run_limiter = deps_override.get("run_limiter") or deps_override.get("runLimiter") or RunLimiter()
    active_registry = deps_override.get("active_registry") or deps_override.get("activeRegistry") or ActiveRunRegistry()

    if deps_override.get("provider"):
        provider = deps_override["provider"]
    elif config.llm_provider == "langchain" and LangChainVmChatProvider is not None:
        provider = LangChainVmChatProvider(
            model_name=config.llm_model,
            base_url=config.llm_base_url,
            api_key=config.llm_api_key,
            mode=config.llm_output_mode,
        )
    elif FixedVmChatProvider is not None:
        provider = FixedVmChatProvider(config.fixed_provider_fixture)
    else:
        provider = None

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Load resources at startup
        try:
            await resource_loader.load()
        except Exception as err:
            logger.warning(f"[app] ResourceLoader load failed at startup: {err}")

        yield

        # Shutdown
        active_registry.abort_all()
        if hasattr(run_store, "destroy") and callable(run_store.destroy):
            run_store.destroy()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    @app.middleware("http")
    async def auth_and_degraded_middleware(request: Request, call_next):
        if request.url.path.startswith("/v1/runs") or request.url.path.startswith("/v1/wiki"):
            if not verify_bearer_auth(request, config.service_api_key):
                return JSONResponse(
                    status_code=403,
                    content={"error": "FORBIDDEN: Invalid or missing bearer token"}
                )
            if not resource_loader.is_ready():
                return JSONResponse(
                    status_code=503,
                    content={"error": "SERVICE_DEGRADED: Resources not loaded"}
                )
        return await call_next(request)

    @app.get("/health")
    async def health():
        ready = resource_loader.is_ready()
        status = "ok" if ready else "degraded"
        status_code = 200 if ready else 503
        model_configured = bool(config.llm_api_key or config.llm_provider == "fixed")

        return JSONResponse(
            status_code=status_code,
            content={
                "status": status,
                "skillLoaded": ready,
                "catalogLoaded": ready,
                "schemaLoaded": ready,
                "modelConfigured": model_configured,
            }
        )

    @app.get("/v1/wiki/tree")
    async def get_wiki_tree_endpoint():
        if not resource_loader.is_ready():
            return JSONResponse(
                status_code=503,
                content={"error": "SERVICE_DEGRADED: Resources not loaded"}
            )
        resources = resource_loader.get_resources()
        return JSONResponse(status_code=200, content=get_wiki_tree(resources))

    @app.get("/v1/wiki/documents/{documentId:path}")
    async def get_wiki_document_endpoint(documentId: str):
        if not resource_loader.is_ready():
            return JSONResponse(
                status_code=503,
                content={"error": "SERVICE_DEGRADED: Resources not loaded"}
            )
        resources = resource_loader.get_resources()
        doc = get_wiki_document(resources, documentId)
        if doc is None:
            return JSONResponse(
                status_code=404,
                content={"error": "WIKI_DOCUMENT_NOT_FOUND"}
            )
        return JSONResponse(status_code=200, content=doc)

    @app.post("/v1/runs")
    async def create_run(request: Request):
        if not resource_loader.is_ready():
            return JSONResponse(
                status_code=503,
                content={"error": "SERVICE_DEGRADED: Resources not loaded"}
            )

        try:
            try:
                body = await request.json()
            except Exception:
                body = {}
            normalized_req = normalize_create_run_request(body)
        except Exception as err:
            return JSONResponse(
                status_code=400,
                content={"error": f"INVALID_REQUEST: {err}"}
            )

        try:
            vm_input = normalize_vm_chat_input(normalized_req)
        except Exception as err:
            return JSONResponse(
                status_code=400,
                content={"error": f"INVALID_INPUT: {err}"}
            )

        try:
            record = run_store.create(normalized_req, vm_input)
            req_obj = getattr(record, "request", None)
            session_id = None
            if isinstance(req_obj, dict):
                session_id = req_obj.get("session_id")
            elif hasattr(req_obj, "session_id"):
                session_id = getattr(req_obj, "session_id")
            if not session_id:
                session_id = record.id

            return JSONResponse(
                status_code=200,
                content={
                    "run_id": record.id,
                    "status": "queued",
                    "session_id": session_id,
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={"error": f"SERVER_ERROR: {err}"}
            )

    @app.get("/v1/runs/{runId}/events")
    async def run_events(runId: str, request: Request):
        if not resource_loader.is_ready():
            return JSONResponse(
                status_code=503,
                content={"error": "SERVICE_DEGRADED: Resources not loaded"}
            )

        claim_result = run_store.claim(runId)
        outcome = getattr(claim_result, "outcome", None) or (claim_result.get("outcome") if isinstance(claim_result, dict) else None)

        if outcome == "not_found":
            return JSONResponse(status_code=404, content={"error": "RUN_NOT_FOUND"})

        if outcome == "streaming":
            return JSONResponse(status_code=409, content={"error": "RUN_ALREADY_STREAMING"})

        record = getattr(claim_result, "record", None) or (claim_result.get("record") if isinstance(claim_result, dict) else None)

        if outcome == "replay":
            async def replay_generator():
                event_buffer = getattr(record, "eventBuffer", None) or getattr(record, "event_buffer", [])
                for frame in event_buffer:
                    yield frame

            return StreamingResponse(
                replay_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )

        # outcome == "claimed"
        try_acquire = getattr(run_limiter, "try_acquire", None) or getattr(run_limiter, "tryAcquire", None)
        release_permit = try_acquire() if callable(try_acquire) else None

        if not release_permit:
            err_frame = serialize_sse_event({
                "event": "run.failed",
                "error": "系统繁忙，当前并发请求较多，请稍后重试",
            })
            run_store.fail(runId, err_frame)

            async def limit_err_generator():
                yield err_frame

            return StreamingResponse(
                limit_err_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Accel-Buffering": "no",
                }
            )

        controller = getattr(record, "controller", None) or AbortController()
        if active_registry:
            active_registry.register(runId, controller)

        async def event_generator():
            is_normal_ended = False

            def is_aborted() -> bool:
                if hasattr(controller, "is_aborted") and controller.is_aborted:
                    return True
                signal = getattr(controller, "signal", None)
                if signal and getattr(signal, "aborted", False):
                    return True
                return False

            def write_sse_frame(frame: str, allow_aborted: bool = False) -> str:
                if not allow_aborted and is_aborted():
                    raise RuntimeError("CLIENT_DISCONNECTED: Client disconnected during streaming")
                run_store.append_event(runId, frame)
                return frame

            try:
                loaded_resources = resource_loader.get_resources()
                vm_input = (
                    getattr(record, "normalizedInput", None)
                    or getattr(record, "normalized_input", None)
                    or VmChatInput(
                        userMessage="Default prompt",
                        selectedBlockId=None,
                        currentDsls=[],
                        globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
                        historyMessages=[],
                    )
                )

                full_output = ""
                has_reasoning = False
                sequence = 0
                last_usage: Dict[str, Any] = {}

                # If orchestrator stream_vm_chat is available, stream from it
                if stream_vm_chat is not None:
                    opts = {
                        "input": vm_input,
                        "resources": loaded_resources,
                        "provider": provider,
                        "signal": controller,
                        "message_chunk_chars": config.sse_chunk_chars,
                    }
                    stream_gen = stream_vm_chat(opts).__aiter__()
                    next_event_task = asyncio.create_task(stream_gen.__anext__())

                    try:
                        while True:
                            done, _ = await asyncio.wait({next_event_task}, timeout=12.0)
                            if not done:
                                if not is_aborted():
                                    yield ": keep-alive\n\n"
                                continue

                            try:
                                event = next_event_task.result()
                            except StopAsyncIteration:
                                break

                            next_event_task = asyncio.create_task(stream_gen.__anext__())

                            if is_aborted():
                                raise RuntimeError("CLIENT_DISCONNECTED")

                            event_type = getattr(event, "event", None) or getattr(event, "type", None) or (
                                (event.get("event") or event.get("type")) if isinstance(event, dict) else None
                            )

                            if event_type == "reasoning.delta":
                                has_reasoning = True
                                sequence += 1
                                delta = getattr(event, "delta", None) or (event.get("delta") if isinstance(event, dict) else "")
                                frame = write_sse_frame(serialize_sse_event({
                                    "event": "reasoning.delta",
                                    "delta": delta,
                                    "sequence": sequence,
                                }))
                                yield frame
                            elif event_type == "message.delta":
                                delta = getattr(event, "delta", None) or (event.get("delta") if isinstance(event, dict) else "")
                                full_output += delta
                                frame = write_sse_frame(serialize_sse_event({
                                    "event": "message.delta",
                                    "delta": delta,
                                }))
                                yield frame
                            elif event_type == "stream.done":
                                event_output = getattr(event, "output", None) or (event.get("output") if isinstance(event, dict) else "")
                                if event_output != full_output:
                                    raise VmChatRunError(
                                        "STREAM_OUTPUT_MISMATCH",
                                        "AI 助手输出校验失败，请重试",
                                    )
                                last_usage = getattr(event, "usage", None) or (event.get("usage") if isinstance(event, dict) else {}) or {}
                            elif event_type == "run.completed":
                                event_output = getattr(event, "output", None) or (event.get("output") if isinstance(event, dict) else "")
                                full_output = event_output or full_output
                                last_usage = getattr(event, "usage", None) or (event.get("usage") if isinstance(event, dict) else {}) or {}
                            elif event_type == "run.failed":
                                fail_msg = getattr(event, "error", None) or (event.get("error") if isinstance(event, dict) else "") or "AI 助手任务执行失败"
                                err_frame = serialize_sse_event({"event": "run.failed", "error": fail_msg})
                                run_store.fail(runId, err_frame)
                                yield err_frame
                                return
                    finally:
                        if not next_event_task.done():
                            next_event_task.cancel()

                if has_reasoning:
                    frame = write_sse_frame(serialize_sse_event({"event": "reasoning.done"}))
                    yield frame

                frame = write_sse_frame(serialize_sse_event({
                    "event": "run.completed",
                    "output": full_output,
                    "usage": last_usage,
                }))
                yield frame

                is_normal_ended = True
                run_store.complete(runId, full_output)

            except (Exception, asyncio.CancelledError, GeneratorExit) as err:
                msg = str(err) or err.__class__.__name__
                if not is_normal_ended:
                    if not (isinstance(err, (asyncio.CancelledError, GeneratorExit)) or "CLIENT_DISCONNECTED" in msg):
                        import traceback
                        traceback.print_exc()
                    fail_msg = (
                        "客户端连接已中断"
                        if isinstance(err, (asyncio.CancelledError, GeneratorExit)) or "CLIENT_DISCONNECTED" in msg
                        else getattr(err, "public_message", None) if isinstance(err, VmChatRunError)
                        else getattr(err, "publicMessage", None) if isinstance(err, VmChatRunError)
                        else "AI 助手任务执行失败"
                    )
                    err_frame = serialize_sse_event({"event": "run.failed", "error": fail_msg})
                    try:
                        write_sse_frame(err_frame, allow_aborted=True)
                    except Exception:
                        pass
                    run_store.fail(runId, err_frame)
                    yield err_frame
            finally:
                if active_registry:
                    active_registry.unregister(runId)
                if callable(release_permit):
                    release_permit()

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",
            }
        )

    return app


# Default app instance
app = create_app()

# Aliases for JS compatibility
buildApp = create_app
build_app = create_app
