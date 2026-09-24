import os
import pathlib
from typing import Dict, List, Literal, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field


load_dotenv()


class AppConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 7310
    service_api_key: str = ""
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:9528", "http://127.0.0.1:9528"])
    llm_provider: Literal["langchain", "fixed"] = "fixed"
    llm_base_url: str = ""
    llm_api_key: str = ""
    llm_model: str = "deepseek-v4-flash"
    llm_output_mode: Literal["structured", "text-json"] = "structured"
    llm_network_retries: int = 0
    allow_missing_usage: bool = False
    max_prompt_chars: int = 120000
    max_stored_runs: int = 100
    max_final_output_chars: int = 200000
    fixed_provider_fixture: str = ""
    request_body_limit_bytes: int = 1048576
    sse_chunk_chars: int = 256
    vmchat_frontend_root: str = ""
    templates_file: str = ".runtime/vmchat-templates.json"
    default_agent_id: str = "performance-ai"
    default_role_id: str = "performance-analyst"
    agents_root: str = "agents"
    session_db_path: str = ".runtime/ai-sessions.sqlite3"
    artifact_db_path: str = ".runtime/ai-artifacts.sqlite3"
    knowledge_db_path: str = ".runtime/knowledge.duckdb"
    session_recent_messages: int = 6
    session_relevant_history_messages: int = 4
    max_context_tokens: int = 32000
    max_context_dsl_tokens: int = 9000
    max_context_history_tokens: int = 5000

    # JS camelCase property aliases
    @property
    def serviceApiKey(self) -> str:
        return self.service_api_key

    @property
    def corsOrigins(self) -> List[str]:
        return self.cors_origins

    @property
    def llmProvider(self) -> str:
        return self.llm_provider

    @property
    def llmBaseUrl(self) -> str:
        return self.llm_base_url

    @property
    def llmApiKey(self) -> str:
        return self.llm_api_key

    @property
    def llmModel(self) -> str:
        return self.llm_model

    @property
    def llmOutputMode(self) -> str:
        return self.llm_output_mode

    @property
    def llmNetworkRetries(self) -> int:
        return self.llm_network_retries

    @property
    def allowMissingUsage(self) -> bool:
        return self.allow_missing_usage

    @property
    def maxPromptChars(self) -> int:
        return self.max_prompt_chars

    @property
    def maxStoredRuns(self) -> int:
        return self.max_stored_runs

    @property
    def maxFinalOutputChars(self) -> int:
        return self.max_final_output_chars

    @property
    def fixedProviderFixture(self) -> str:
        return self.fixed_provider_fixture

    @property
    def requestBodyLimitBytes(self) -> int:
        return self.request_body_limit_bytes

    @property
    def sseChunkChars(self) -> int:
        return self.sse_chunk_chars

    @property
    def vmchatFrontendRoot(self) -> str:
        return self.vmchat_frontend_root

    @property
    def templatesFile(self) -> str:
        return self.templates_file


def load_config(env: Optional[Dict[str, Optional[str]]] = None) -> AppConfig:
    if env is None:
        raw_env = dict(os.environ)
    else:
        raw_env = {k: v for k, v in env.items() if v is not None}

    llm_retries_str = raw_env.get("LLM_NETWORK_RETRIES", "0")
    try:
        llm_network_retries = int(llm_retries_str)
    except ValueError:
        llm_network_retries = 0

    if llm_network_retries != 0:
        raise ValueError("INVALID_CONFIG: LLM_NETWORK_RETRIES must be 0 because LLM generation POST is not idempotent")

    cors_raw = raw_env.get("CORS_ORIGINS", "http://localhost:9528,http://127.0.0.1:9528")
    cors_origins = [s.strip() for s in cors_raw.split(",") if s.strip()]

    frontend_root_raw = raw_env.get("VMCHAT_FRONTEND_ROOT", "../jn-fof-gf-vue")
    vmchat_frontend_root = str(pathlib.Path.cwd().joinpath(frontend_root_raw).resolve())

    llm_provider_val = raw_env.get("LLM_PROVIDER", "fixed")
    llm_provider: Literal["langchain", "fixed"] = "langchain" if llm_provider_val == "langchain" else "fixed"

    llm_output_mode_val = raw_env.get("LLM_OUTPUT_MODE", "structured")
    llm_output_mode: Literal["structured", "text-json"] = "text-json" if llm_output_mode_val == "text-json" else "structured"

    host = raw_env.get("HOST", "127.0.0.1")
    port = int(raw_env.get("PORT", "7310"))
    service_api_key = raw_env.get("SERVICE_API_KEY", "")
    llm_base_url = raw_env.get("LLM_BASE_URL", "")
    llm_api_key = raw_env.get("LLM_API_KEY") or raw_env.get("OPENAI_API_KEY", "")
    llm_model = raw_env.get("LLM_MODEL", "deepseek-v4-flash")
    allow_missing_usage = raw_env.get("ALLOW_MISSING_USAGE", "").lower() == "true"
    max_prompt_chars = int(raw_env.get("MAX_PROMPT_CHARS", "120000"))
    max_stored_runs = int(raw_env.get("MAX_STORED_RUNS", "100"))
    max_final_output_chars = int(raw_env.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
    fixed_provider_fixture = raw_env.get("FIXED_PROVIDER_FIXTURE", "")
    request_body_limit_bytes = int(raw_env.get("REQUEST_BODY_LIMIT_BYTES", "1048576"))
    sse_chunk_chars = int(raw_env.get("SSE_CHUNK_CHARS", "256"))
    templates_file = raw_env.get("VMCHAT_TEMPLATES_FILE", ".runtime/vmchat-templates.json")
    default_agent_id = raw_env.get("DEFAULT_AGENT_ID", "performance-ai")
    default_role_id = raw_env.get("DEFAULT_ROLE_ID", "performance-analyst")
    agents_root = raw_env.get("AGENTS_ROOT", "agents")
    session_db_path = raw_env.get("SESSION_DB_PATH", ".runtime/ai-sessions.sqlite3")
    artifact_db_path = raw_env.get("ARTIFACT_DB_PATH", ".runtime/ai-artifacts.sqlite3")
    knowledge_db_path = raw_env.get("KNOWLEDGE_DB_PATH", ".runtime/knowledge.duckdb")
    session_recent_messages = int(raw_env.get("SESSION_RECENT_MESSAGES", "6"))
    session_relevant_history_messages = int(raw_env.get("SESSION_RELEVANT_HISTORY_MESSAGES", "4"))
    max_context_tokens = int(raw_env.get("MAX_CONTEXT_TOKENS", "32000"))
    max_context_dsl_tokens = int(raw_env.get("MAX_CONTEXT_DSL_TOKENS", "9000"))
    max_context_history_tokens = int(raw_env.get("MAX_CONTEXT_HISTORY_TOKENS", "5000"))

    return AppConfig(
        host=host,
        port=port,
        service_api_key=service_api_key,
        cors_origins=cors_origins,
        llm_provider=llm_provider,
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        llm_model=llm_model,
        llm_output_mode=llm_output_mode,
        llm_network_retries=0,
        allow_missing_usage=allow_missing_usage,
        max_prompt_chars=max_prompt_chars,
        max_stored_runs=max_stored_runs,
        max_final_output_chars=max_final_output_chars,
        fixed_provider_fixture=fixed_provider_fixture,
        request_body_limit_bytes=request_body_limit_bytes,
        sse_chunk_chars=sse_chunk_chars,
        vmchat_frontend_root=vmchat_frontend_root,
        templates_file=templates_file,
        default_agent_id=default_agent_id,
        default_role_id=default_role_id,
        agents_root=agents_root,
        session_db_path=session_db_path,
        artifact_db_path=artifact_db_path,
        knowledge_db_path=knowledge_db_path,
        session_recent_messages=session_recent_messages,
        session_relevant_history_messages=session_relevant_history_messages,
        max_context_tokens=max_context_tokens,
        max_context_dsl_tokens=max_context_dsl_tokens,
        max_context_history_tokens=max_context_history_tokens,
    )


# Alias for JS camelCase compatibility
loadConfig = load_config
