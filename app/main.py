import asyncio
from contextlib import asynccontextmanager
from dataclasses import dataclass
import hmac
import json
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
from app.template_store import TemplateStore

from app.provider.fixed_provider import FixedVmChatProvider, VmChatModelProvider
from app.provider.langchain_provider import LangChainVmChatProvider
from app.orchestrator.vmchat_orchestrator import stream_vm_chat
from app.orchestrator.simple_chat_orchestrator import stream_simple_chat
from app.resources.wiki_catalog import get_wiki_tree, get_wiki_document
from app.agents.registry import AgentRegistry
from app.session.store import SqliteSessionStore
from app.session.manager import SessionManager
from app.context.manager import ContextManager
from app.artifacts.store import SqliteArtifactStore
from app.knowledge.store import DuckDbKnowledgeStore, SqliteKnowledgeStore
from app.knowledge.service import KnowledgeService

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
    template_store: Any = None
    agent_registry: Any = None
    session_manager: Any = None
    context_manager: Any = None
    artifact_store: Any = None
    knowledge_service: Any = None

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

    agent_registry = (
        deps_override.get("agent_registry")
        or deps_override.get("agentRegistry")
        or AgentRegistry(getattr(config, "agents_root", "agents")).load()
    )
    default_agent_id = getattr(config, "default_agent_id", "performance-ai")
    default_role_id = getattr(config, "default_role_id", "performance-analyst")
    default_agent = agent_registry.get(default_agent_id) if agent_registry else None

    configured_resource_loader = deps_override.get("resource_loader") or deps_override.get("resourceLoader")
    if configured_resource_loader is not None:
        resource_loader = configured_resource_loader
    elif default_agent is not None and default_agent.resourcesDir:
        resource_loader = ResourceLoader(resources_dir=default_agent.resourcesDir)
    else:
        resource_loader = ResourceLoader()

    run_store = deps_override.get("run_store") or deps_override.get("runStore") or RunStore(max_stored_runs=config.max_stored_runs)
    run_limiter = deps_override.get("run_limiter") or deps_override.get("runLimiter") or RunLimiter()
    active_registry = deps_override.get("active_registry") or deps_override.get("activeRegistry") or ActiveRunRegistry()
    template_store = (
        deps_override.get("template_store")
        or deps_override.get("templateStore")
        or TemplateStore(config.templates_file)
    )

    isolated_runtime = bool(deps_override)
    default_session_path = ":memory:" if isolated_runtime else getattr(
        config, "session_db_path", ".runtime/ai-sessions.sqlite3"
    )
    default_artifact_path = ":memory:" if isolated_runtime else getattr(
        config, "artifact_db_path", ".runtime/ai-artifacts.sqlite3"
    )
    default_knowledge_path = ":memory:" if isolated_runtime else getattr(
        config, "knowledge_db_path", ".runtime/knowledge.duckdb"
    )

    session_store = (
        deps_override.get("session_store")
        or deps_override.get("sessionStore")
        or SqliteSessionStore(default_session_path)
    )
    session_manager = (
        deps_override.get("session_manager")
        or deps_override.get("sessionManager")
        or SessionManager(
            session_store,
            recent_messages=getattr(config, "session_recent_messages", 6),
            relevant_history_messages=getattr(config, "session_relevant_history_messages", 4),
        )
    )
    context_manager = (
        deps_override.get("context_manager")
        or deps_override.get("contextManager")
        or ContextManager(
            session_manager,
            max_context_tokens=getattr(config, "max_context_tokens", 32000),
            max_dsl_tokens=getattr(config, "max_context_dsl_tokens", 9000),
            max_history_tokens=getattr(config, "max_context_history_tokens", 5000),
        )
    )
    artifact_store = (
        deps_override.get("artifact_store")
        or deps_override.get("artifactStore")
        or SqliteArtifactStore(default_artifact_path)
    )

    knowledge_service = deps_override.get("knowledge_service") or deps_override.get("knowledgeService")
    knowledge_store = None
    knowledge_backend = "custom" if knowledge_service is not None else "disabled"
    if knowledge_service is None:
        try:
            knowledge_store = DuckDbKnowledgeStore(default_knowledge_path)
            knowledge_service = KnowledgeService(knowledge_store)
            knowledge_backend = "duckdb"
        except Exception as err:
            logger.info(f"[app] DuckDB unavailable, using SQLite knowledge store: {err}")
            fallback_path = str(default_knowledge_path)
            if fallback_path.endswith(".duckdb"):
                fallback_path = fallback_path[:-7] + ".sqlite3"
            knowledge_store = SqliteKnowledgeStore(fallback_path)
            knowledge_service = KnowledgeService(knowledge_store)
            knowledge_backend = "sqlite"

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
            if knowledge_service is not None and resource_loader.is_ready():
                loaded = resource_loader.get_resources()
                resource_map = getattr(loaded, "toolResourceTextByPath", None) or getattr(
                    loaded, "tool_resource_text_by_path", None
                )
                if isinstance(resource_map, dict):
                    stats = await asyncio.to_thread(
                        knowledge_service.index_resource_map,
                        default_agent_id,
                        resource_map,
                    )
                    logger.info(f"[app] Knowledge index ready for {default_agent_id}: {stats}")

                if agent_registry is not None:
                    for agent in agent_registry.list_agents():
                        if agent.id == default_agent_id:
                            continue
                        generic_docs = agent_registry.collect_knowledge(agent.id)
                        if generic_docs:
                            stats = await asyncio.to_thread(
                                knowledge_service.index_resource_map,
                                agent.id,
                                generic_docs,
                            )
                            logger.info(f"[app] Knowledge index ready for {agent.id}: {stats}")
        except Exception as err:
            logger.warning(f"[app] ResourceLoader/Knowledge load failed at startup: {err}")

        yield

        # Shutdown
        active_registry.abort_all()
        if hasattr(run_store, "destroy") and callable(run_store.destroy):
            run_store.destroy()
        if hasattr(session_store, "close") and callable(session_store.close):
            session_store.close()
        if hasattr(artifact_store, "close") and callable(artifact_store.close):
            artifact_store.close()
        if knowledge_store is not None and hasattr(knowledge_store, "close"):
            knowledge_store.close()

    app = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    @app.middleware("http")
    async def auth_and_degraded_middleware(request: Request, call_next):
        is_run_or_wiki = request.url.path.startswith("/v1/runs") or request.url.path.startswith("/v1/wiki")
        is_template = request.url.path.startswith("/v1/templates")
        is_runtime = (
            request.url.path.startswith("/v1/sessions")
            or request.url.path.startswith("/v1/agents")
            or request.url.path.startswith("/v1/knowledge")
            or request.url.path.startswith("/v1/artifacts")
        )
        if is_run_or_wiki or is_template or is_runtime:
            if not verify_bearer_auth(request, config.service_api_key):
                return JSONResponse(
                    status_code=403,
                    content={"error": "FORBIDDEN: Invalid or missing bearer token"}
                )
            if request.url.path.startswith("/v1/wiki") and not resource_loader.is_ready():
                return JSONResponse(status_code=503, content={"error": "SERVICE_DEGRADED: Resources not loaded"})
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
                "sessionStore": "sqlite",
                "knowledgeReady": knowledge_service is not None,
                "knowledgeBackend": knowledge_backend,
                "defaultAgent": default_agent_id,
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

    @app.get("/v1/agents")
    async def list_agents():
        agents = []
        for agent in agent_registry.list_agents() if agent_registry else []:
            role = agent_registry.get_role(agent.id, agent.defaultRole) if agent_registry else None
            agents.append({
                "id": agent.id,
                "name": agent.name,
                "version": agent.version,
                "workflow": agent.workflow,
                "defaultRole": agent.defaultRole,
                "defaultRoleName": role.name if role else None,
                "metadata": agent.metadata,
            })
        return JSONResponse(status_code=200, content={"agents": agents})

    @app.get("/v1/agents/{agentId}/roles")
    async def list_agent_roles(agentId: str):
        if agent_registry is None or agent_registry.get(agentId) is None:
            return JSONResponse(status_code=404, content={"error": "AGENT_NOT_FOUND"})
        roles = agent_registry.list_roles(agentId)
        return JSONResponse(
            status_code=200,
            content={
                "agent_id": agentId,
                "roles": [
                    {
                        "id": role.id,
                        "name": role.name,
                        "allowedSkills": role.allowedSkills,
                        "allowedTools": role.allowedTools,
                        "knowledgeScopes": role.knowledgeScopes,
                        "metadata": role.metadata,
                    }
                    for role in roles
                ],
            },
        )

    @app.get("/v1/sessions/{sessionId}")
    async def get_session(sessionId: str):
        state = session_store.get(sessionId)
        if state is None:
            return JSONResponse(status_code=404, content={"error": "SESSION_NOT_FOUND"})
        payload = state.model_dump(by_alias=True)
        payload["message_count"] = len(state.messages)
        # Session inspection returns state, but not every historical message body.
        payload["messages"] = [
            {
                "role": item.role,
                "created_at": item.createdAt,
                "run_id": item.runId,
                "preview": item.content[:240],
            }
            for item in state.messages[-12:]
        ]
        return JSONResponse(status_code=200, content=payload)

    @app.delete("/v1/sessions/{sessionId}")
    async def delete_session(sessionId: str):
        deleted = session_manager.delete(sessionId)
        return JSONResponse(status_code=200, content={"ok": True, "deleted": deleted})

    @app.post("/v1/knowledge/search")
    async def search_knowledge(request: Request):
        if knowledge_service is None:
            return JSONResponse(status_code=503, content={"error": "KNOWLEDGE_SERVICE_UNAVAILABLE"})
        body = await request.json()
        query = str(body.get("query") or "").strip() if isinstance(body, dict) else ""
        if not query:
            return JSONResponse(status_code=400, content={"error": "query is required"})
        agent_id = str(body.get("agent_id") or default_agent_id)
        limit = min(20, max(1, int(body.get("limit") or 8)))
        hits = knowledge_service.search(agent_id=agent_id, query=query, limit=limit)
        return JSONResponse(
            status_code=200,
            content={
                "query": query,
                "agent_id": agent_id,
                "hits": [
                    {
                        "path": hit.path,
                        "title": hit.title,
                        "content": hit.content,
                        "score": hit.score,
                        "metadata": hit.metadata,
                    }
                    for hit in hits
                ],
            },
        )

    @app.get("/v1/artifacts/{artifactId}")
    async def get_artifact(artifactId: str):
        artifact = artifact_store.get(artifactId)
        if artifact is None:
            return JSONResponse(status_code=404, content={"error": "ARTIFACT_NOT_FOUND"})
        return JSONResponse(
            status_code=200,
            content=artifact.model_dump(by_alias=True),
        )

    @app.get("/v1/templates")
    async def list_templates():
        return JSONResponse(status_code=200, content={"ok": True, "templates": template_store.list()})

    @app.get("/v1/templates/{templateId}")
    async def get_template(templateId: str):
        template = template_store.get(templateId)
        if template is None:
            return JSONResponse(status_code=404, content={"error": "TEMPLATE_NOT_FOUND"})
        return JSONResponse(status_code=200, content={"ok": True, "template": template})

    @app.put("/v1/templates")
    async def replace_templates(request: Request):
        try:
            body = await request.json()
            source = body.get("templates") if isinstance(body, dict) else body
            if not isinstance(source, list):
                raise ValueError("templates must be an array")
            templates = template_store.replace_all(source)
            return JSONResponse(status_code=200, content={"ok": True, "templates": templates})
        except ValueError as err:
            return JSONResponse(status_code=400, content={"error": f"INVALID_TEMPLATES: {err}"})
        except Exception as err:
            logger.exception("[templates] replace failed")
            return JSONResponse(status_code=500, content={"error": f"SERVER_ERROR: {err}"})

    @app.post("/v1/templates")
    async def upsert_template(request: Request):
        try:
            body = await request.json()
            template = body.get("template") if isinstance(body, dict) and isinstance(body.get("template"), dict) else body
            saved = template_store.upsert(template)
            return JSONResponse(status_code=200, content={"ok": True, "template": saved})
        except ValueError as err:
            return JSONResponse(status_code=400, content={"error": f"INVALID_TEMPLATE: {err}"})
        except Exception as err:
            logger.exception("[templates] upsert failed")
            return JSONResponse(status_code=500, content={"error": f"SERVER_ERROR: {err}"})

    @app.put("/v1/templates/{templateId}")
    async def update_template(templateId: str, request: Request):
        try:
            body = await request.json()
            template = body.get("template") if isinstance(body, dict) and isinstance(body.get("template"), dict) else body
            saved = template_store.upsert(template, templateId)
            return JSONResponse(status_code=200, content={"ok": True, "template": saved})
        except ValueError as err:
            return JSONResponse(status_code=400, content={"error": f"INVALID_TEMPLATE: {err}"})
        except Exception as err:
            logger.exception("[templates] update failed")
            return JSONResponse(status_code=500, content={"error": f"SERVER_ERROR: {err}"})

    @app.delete("/v1/templates/{templateId}")
    async def delete_template(templateId: str):
        if not template_store.delete(templateId):
            return JSONResponse(status_code=404, content={"error": "TEMPLATE_NOT_FOUND"})
        return JSONResponse(status_code=200, content={"ok": True, "deleted": templateId})

    @app.post("/v1/runs")
    async def create_run(request: Request):
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

            agent_id = normalized_req.agent_id or default_agent_id
            role_id = normalized_req.role_id or default_role_id
            agent = agent_registry.get(agent_id) if agent_registry else None
            if agent_registry and agent is None:
                raise ValueError(f"UNKNOWN_AGENT: {agent_id}")
            if agent is not None and agent.workflow == "vm-report" and not resource_loader.is_ready():
                raise RuntimeError("SERVICE_DEGRADED: Resources not loaded")
            role = agent_registry.get_role(agent_id, role_id) if agent_registry else None
            if agent is not None and role is None and agent.defaultRole:
                role_id = agent.defaultRole

            session_state = session_manager.get_or_create(
                normalized_req.session_id,
                agent_id=agent_id,
                role_id=role_id,
            )
            prepared_input, context_report = context_manager.prepare(session_state, vm_input)
            session_manager.update_ui_state(session_state, vm_input)
        except Exception as err:
            return JSONResponse(
                status_code=400,
                content={"error": f"INVALID_INPUT: {err}"}
            )

        try:
            record = run_store.create(normalized_req, prepared_input)
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
                    "context": {
                        "estimated_tokens": context_report.total_estimated_tokens,
                        "history_tokens": context_report.history_tokens,
                        "dsl_tokens": context_report.dsl_tokens,
                        "full_dsl_blocks": context_report.full_dsl_blocks,
                        "summarized_dsl_blocks": context_report.summarized_dsl_blocks,
                    },
                }
            )
        except Exception as err:
            return JSONResponse(
                status_code=500,
                content={"error": f"SERVER_ERROR: {err}"}
            )

    @app.get("/v1/runs/{runId}/events")
    async def run_events(runId: str, request: Request):
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

                agent_id = getattr(vm_input, "agentId", None) or default_agent_id
                role_id = getattr(vm_input, "roleId", None) or default_role_id
                agent = agent_registry.get(agent_id) if agent_registry else None
                if agent_registry is not None and agent is None:
                    raise VmChatRunError("UNKNOWN_AGENT", f"未知 Agent: {agent_id}")
                workflow = agent.workflow if agent is not None else "vm-report"
                role = agent_registry.get_role(agent_id, role_id) if agent_registry else None
                role_prompt = role.systemPrompt if role else ""
                knowledge_search = (
                    (lambda query: knowledge_service.format_for_tool(agent_id, query))
                    if knowledge_service is not None
                    else None
                )

                full_output = ""
                has_reasoning = False
                sequence = 0
                last_usage: Dict[str, Any] = {}

                if workflow == "simple-chat":
                    skill_md = agent_registry.read_skill(agent_id) if agent_registry else ""
                    stream_gen = stream_simple_chat(
                        input_val=vm_input,
                        provider=provider,
                        skill_md=skill_md,
                        role_prompt=role_prompt,
                        knowledge_search=knowledge_search,
                        signal=controller,
                        message_chunk_chars=config.sse_chunk_chars,
                    ).__aiter__()
                else:
                    if not resource_loader.is_ready():
                        raise VmChatRunError(
                            "SERVICE_DEGRADED",
                            "当前 Agent 资源尚未加载完成",
                        )
                    loaded_resources = resource_loader.get_resources()
                    opts = {
                        "input": vm_input,
                        "resources": loaded_resources,
                        "provider": provider,
                        "signal": controller,
                        "message_chunk_chars": config.sse_chunk_chars,
                        "role_prompt": role_prompt,
                        "knowledge_search": knowledge_search,
                    }
                    stream_gen = stream_vm_chat(opts).__aiter__()

                if stream_gen is not None:
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

                artifact_id = None
                try:
                    parsed_output = json.loads(full_output)
                    is_dsl_artifact = isinstance(parsed_output, list) or (
                        isinstance(parsed_output, dict)
                        and any(key in parsed_output for key in ("action", "requests", "view", "views"))
                    )
                    if is_dsl_artifact:
                        artifact = artifact_store.create(
                            session_id=getattr(getattr(record, "request", None), "session_id", None) or runId,
                            kind="vm-report-dsl",
                            payload=parsed_output,
                            metadata={"runId": runId},
                        )
                        artifact_id = artifact.id
                except Exception:
                    artifact_id = None

                request_obj = getattr(record, "request", None)
                session_id_for_turn = (
                    getattr(request_obj, "session_id", None)
                    if request_obj is not None
                    else None
                ) or runId
                session_state = session_manager.get_or_create(
                    session_id_for_turn,
                    agent_id=getattr(vm_input, "agentId", default_agent_id),
                    role_id=getattr(vm_input, "roleId", default_role_id),
                )
                session_manager.complete_turn(
                    session_state,
                    vm_input.userMessage,
                    full_output,
                    run_id=runId,
                    artifact_id=artifact_id,
                )

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
