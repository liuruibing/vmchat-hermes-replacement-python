from app.provider.fixed_provider import ModelSkillRunInput, ModelGenerateInput
import inspect
import json
import os
import re
from dataclasses import dataclass
from typing import Any, AsyncGenerator, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field

from app.compatibility.hermes_events import (
    ClientDisconnectedError,
    HermesSseEvent,
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    code_point_chunks,
    codePointChunks,
)
from app.compatibility.hermes_request import VmChatInput
from app.contracts.types import (
    ValidationFailure,
    ValidationIssue,
    ValidationResult,
    ValidationSuccess,
    VmChatRunError,
)
from app.resources.resource_types import LoadedResources
from app.resources.skill_resource_reader import (
    SkillResourceReader,
    SkillResourceReaderOptions,
)

from app.prompt.generate_prompt import build_generate_prompt
from app.prompt.repair_prompt import build_repair_prompt
from app.validation.validate_vm_report_dsl import validate_vm_report_dsl_set
from app.provider.fixed_provider import VmChatModelProvider

@dataclass
class OrchestratorInput:
    input: VmChatInput
    resources: LoadedResources
    provider: Any
    signal: Optional[Any] = None
    rolePrompt: str = ""
    knowledgeSearch: Optional[Any] = None


class OrchestratorUsage(BaseModel):
    prompt_tokens: int = Field(default=0, alias="prompt_tokens")
    completion_tokens: int = Field(default=0, alias="completion_tokens")
    total_tokens: int = Field(default=0, alias="total_tokens")

    model_config = ConfigDict(populate_by_name=True)


class OrchestratorOutput(BaseModel):
    resultType: Literal["dsl", "text"] = Field(..., alias="resultType")
    text: str
    attemptCount: int = Field(..., alias="attemptCount")
    repairAttempts: int = Field(..., alias="repairAttempts")
    usage: Dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

    @property
    def result_type(self) -> Literal["dsl", "text"]:
        return self.resultType

    @property
    def attempt_count(self) -> int:
        return self.attemptCount

    @property
    def repair_attempts(self) -> int:
        return self.repairAttempts


MAX_DSL_REPAIR_ATTEMPTS = 5
const_MAX_DSL_REPAIR_ATTEMPTS = 5


@dataclass
class StreamOrchestratorOptions:
    input: VmChatInput
    resources: LoadedResources
    provider: Any
    signal: Optional[Any] = None
    messageChunkChars: Optional[int] = None
    message_chunk_chars: Optional[int] = None
    rolePrompt: str = ""
    knowledgeSearch: Optional[Any] = None


class ReasoningDeltaStreamEvent(BaseModel):
    type: Literal["reasoning.delta"] = "reasoning.delta"
    event: Literal["reasoning.delta"] = "reasoning.delta"
    delta: str
    sequence: int = 0


class MessageDeltaStreamEvent(BaseModel):
    type: Literal["message.delta"] = "message.delta"
    event: Literal["message.delta"] = "message.delta"
    delta: str


class StreamDoneEvent(BaseModel):
    type: Literal["stream.done", "run.completed"] = "stream.done"
    event: Literal["stream.done", "run.completed"] = "run.completed"
    output: str
    usage: Optional[Dict[str, Any]] = None


VmChatStreamEvent = Union[
    ReasoningDeltaStreamEvent,
    MessageDeltaStreamEvent,
    StreamDoneEvent,
    HermesSseEvent,
]


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    return bool(getattr(signal, "aborted", False))


def _add_usage(target: Dict[str, int], usage: Any) -> None:
    if not usage:
        return
    if isinstance(usage, dict):
        target["prompt_tokens"] += int(usage.get("prompt_tokens") or 0)
        target["completion_tokens"] += int(usage.get("completion_tokens") or 0)
        target["total_tokens"] += int(usage.get("total_tokens") or 0)
    else:
        target["prompt_tokens"] += int(getattr(usage, "prompt_tokens", 0) or 0)
        target["completion_tokens"] += int(getattr(usage, "completion_tokens", 0) or 0)
        target["total_tokens"] += int(getattr(usage, "total_tokens", 0) or 0)


def _extract_first_json_value(text: str) -> Optional[str]:
    source = str(text or "").strip()
    fence_match = re.match(r"^```(?:json)?\s*([\s\S]*?)\s*```$", source, re.IGNORECASE)
    if fence_match:
        source = fence_match.group(1).strip()

    start = -1
    for index, char in enumerate(source):
        if char in ("{", "["):
            start = index
            break
    if start < 0:
        return None

    stack: List[str] = []
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char in ("{", "["):
            stack.append(char)
            continue
        if char not in ("}", "]"):
            continue
        expected = "{" if char == "}" else "["
        if not stack or stack[-1] != expected:
            return None
        stack.pop()
        if not stack:
            return source[start : index + 1]
    return None


def _is_nonreport_protocol(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    intent = str(value.get("intent") or "").strip().lower()
    render_type = str(value.get("renderType") or "").strip().lower()
    allowed = {"chat", "clarify", "businessinfo"}
    return intent in allowed or render_type in allowed


def _is_dsl_candidate(value: Any) -> bool:
    if isinstance(value, list):
        return bool(value) and all(_is_dsl_candidate(item) for item in value)
    if not isinstance(value, dict) or _is_nonreport_protocol(value):
        return False
    action = str(value.get("action") or "").strip().lower()
    if action in {"create", "update"}:
        return True
    return any(key in value for key in ("requests", "transform", "view", "views", "moduleId", "sqlCode"))


def _classify_model_output(text: str) -> Dict[str, Any]:
    trimmed = str(text or "").strip()
    json_text = _extract_first_json_value(trimmed)
    parsed: Any = None
    if json_text:
        try:
            parsed = json.loads(json_text)
        except Exception:
            parsed = None

    if parsed is not None:
        if _is_nonreport_protocol(parsed):
            return {
                "kind": "text",
                "text": json.dumps(parsed, ensure_ascii=False),
                "candidate": None,
                "issues": None,
            }
        if _is_dsl_candidate(parsed):
            return {
                "kind": "dsl",
                "text": "",
                "candidate": parsed,
                "issues": None,
            }

    if re.search(
        r'"(?:action|requests|transform|view|views|moduleId|sqlCode)"\s*:',
        trimmed,
        re.IGNORECASE,
    ):
        return {
            "kind": "dsl",
            "text": "",
            "candidate": trimmed,
            "issues": [
                ValidationIssue(
                    code="INVALID_JSON",
                    path="/",
                    message="模型输出的 DSL 不是完整且唯一的 JSON 对象或数组",
                )
            ],
        }

    return {"kind": "text", "text": trimmed, "candidate": None, "issues": None}


class RunFailedEvent(BaseModel):
    type: Literal["run.failed"] = "run.failed"
    event: Literal["run.failed"] = "run.failed"
    error: str

VmChatStreamEvent = Union[
    ReasoningDeltaStreamEvent, MessageDeltaStreamEvent, StreamDoneEvent, RunFailedEvent
]

def _call_build_generate_prompt(
    input_val: VmChatInput, skill_md: str, role_prompt: str = ""
) -> tuple[str, str]:
    opts = {"input": input_val, "skillMd": skill_md, "rolePrompt": role_prompt}
    res = build_generate_prompt(opts)
    return res.systemPrompt, res.userPrompt

def _call_build_repair_prompt(
    current_dsl_payload: Any,
    errors: List[ValidationIssue],
    input_val: VmChatInput,
    resource_context: Dict[str, Any],
    skill_md: str,
) -> tuple[str, str]:
    opts = {
        "invalidCandidate": current_dsl_payload,
        "validationErrors": errors,
        "input": input_val,
        "resourceContext": resource_context,
        "skillMd": skill_md,
    }
    res = build_repair_prompt(opts)
    return res.systemPrompt, res.userPrompt

def _call_validate_vm_report_dsl_set(
    current_dsl_payload: Any, resources: Any, current_block_ids: List[str]
) -> ValidationResult:
    return validate_vm_report_dsl_set(
        current_dsl_payload,
        {
            "catalogContract": getattr(resources, "catalogContract", None)
            or getattr(resources, "catalog_contract", None),
            "schemaJson": getattr(resources, "schemaJson", None)
            or getattr(resources, "schema_json", None),
            "currentBlockIds": current_block_ids,
            "moduleProfiles": getattr(resources, "moduleProfiles", None)
            or getattr(resources, "module_profiles", None),
        },
    )

async def validate_and_repair_dsl(
    options: Optional[Dict[str, Any]] = None, **kwargs: Any
) -> Dict[str, Any]:
    opts = dict(options or {})
    opts.update(kwargs)

    initial_candidate = opts.get("initialCandidate")
    if initial_candidate is None and "initial_candidate" in opts:
        initial_candidate = opts.get("initial_candidate")

    initial_issues = opts.get("initialIssues")
    if initial_issues is None and "initial_issues" in opts:
        initial_issues = opts.get("initial_issues")

    initial_usage = opts.get("initialUsage")
    if initial_usage is None and "initial_usage" in opts:
        initial_usage = opts.get("initial_usage")

    input_val: VmChatInput = opts.get("input")
    resource_context = opts.get("resourceContext")
    if resource_context is None and "resource_context" in opts:
        resource_context = opts.get("resource_context")

    resources: LoadedResources = opts.get("resources")
    provider = opts.get("provider")
    signal = opts.get("signal")

    max_output_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
    attempt_count = 1
    repair_attempts = 0
    total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

    _add_usage(total_usage, initial_usage)

    current_dsls = getattr(input_val, "currentDsls", None) or getattr(
        input_val, "current_dsls", None
    )
    if current_dsls is None:
        current_dsls = []

    current_block_ids: List[str] = []
    for d in current_dsls:
        bid = None
        if isinstance(d, dict):
            bid = d.get("blockId") or d.get("id") or d.get("block_id")
        else:
            bid = (
                getattr(d, "blockId", None)
                or getattr(d, "id", None)
                or getattr(d, "block_id", None)
            )
        if bid:
            current_block_ids.append(bid)

    current_dsl_payload = initial_candidate
    val_result: ValidationResult

    if initial_issues and len(initial_issues) > 0:
        val_result = ValidationFailure(errors=initial_issues)
    else:
        val_result = _call_validate_vm_report_dsl_set(
            current_dsl_payload, resources, current_block_ids
        )

    while (
        not getattr(val_result, "ok", False)
        and repair_attempts < MAX_DSL_REPAIR_ATTEMPTS
    ):
        if _is_aborted(signal):
            raise ClientDisconnectedError(
                "CLIENT_DISCONNECTED: Execution aborted during repair"
            )

        repair_attempts += 1
        attempt_count += 1

        errors = getattr(val_result, "errors", []) or []
        skill_md = getattr(resources, "skillMd", None) or getattr(
            resources, "skill_md", ""
        )

        sys_prompt, user_prompt = _call_build_repair_prompt(
            current_dsl_payload, errors, input_val, resource_context, skill_md
        )

        gen_fn = getattr(provider, "generate", None)
        if gen_fn is None:
            raise RuntimeError("Provider does not have generate method")

        repair_kwargs = {
            "systemPrompt": sys_prompt,
            "system_prompt": sys_prompt,
            "userPrompt": user_prompt,
            "user_prompt": user_prompt,
            "signal": signal,
            "purpose": "repair",
        }

        if inspect.iscoroutinefunction(gen_fn):
            repair_output = await gen_fn(ModelGenerateInput(**repair_kwargs))
        else:
            repair_res = gen_fn(ModelGenerateInput(**repair_kwargs))
            if inspect.isawaitable(repair_res):
                repair_output = await repair_res
            else:
                repair_output = repair_res

        repair_usage = getattr(repair_output, "usage", None) or (
            repair_output.get("usage") if isinstance(repair_output, dict) else None
        )
        _add_usage(total_usage, repair_usage)

        repair_result = getattr(repair_output, "result", None) or (
            repair_output.get("result") if isinstance(repair_output, dict) else None
        )
        result_type = getattr(repair_result, "type", None) or (
            repair_result.get("type") if isinstance(repair_result, dict) else None
        )

        if result_type == "text":
            val_result = ValidationFailure(
                errors=[
                    ValidationIssue(
                        code="REPAIR_DSL_REQUIRED",
                        path="/",
                        message="修复请求必须返回 DSL JSON",
                    )
                ]
            )
            continue

        current_dsl_payload = getattr(repair_result, "dsl", None) or (
            repair_result.get("dsl") if isinstance(repair_result, dict) else None
        )
        val_result = _call_validate_vm_report_dsl_set(
            current_dsl_payload, resources, current_block_ids
        )
    if not getattr(val_result, "ok", False):
        raise VmChatRunError(
            "DSL_REPAIR_EXHAUSTED",
            "AI 助手生成的报表格式无法自动修复，请调整描述后重试",
        )

    final_text = ""
    dsls = getattr(val_result, "dsls", []) or []
    is_array_candidate = (
        isinstance(current_dsl_payload, list) or len(dsls) > 1
    )

    if is_array_candidate:
        dsls_data = [d.model_dump(exclude_none=True) if hasattr(d, "model_dump") else d for d in dsls]
        final_text = json.dumps(dsls_data, indent=2, ensure_ascii=False)
    else:
        first_item = dsls[0] if dsls else current_dsl_payload
        first_data = (
            first_item.model_dump(exclude_none=True)
            if hasattr(first_item, "model_dump")
            else first_item
        )
        final_text = json.dumps(first_data, indent=2, ensure_ascii=False)

    if len(final_text) > max_output_chars:
        raise VmChatRunError(
            "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
            f"生成的 DSL 长度 ({len(final_text)}) 超过上限 ({max_output_chars})",
        )

    return {
        "text": final_text,
        "attemptCount": attempt_count,
        "attempt_count": attempt_count,
        "repairAttempts": repair_attempts,
        "repair_attempts": repair_attempts,
        "usage": total_usage,
    }


validateAndRepairDsl = validate_and_repair_dsl


async def run_vm_chat_orchestrator(
    options: Union[OrchestratorInput, Dict[str, Any]]
) -> OrchestratorOutput:
    if isinstance(options, dict):
        input_val = options.get("input")
        resources = options.get("resources")
        provider = options.get("provider")
        signal = options.get("signal")
        role_prompt = options.get("rolePrompt") or options.get("role_prompt") or ""
        knowledge_search = options.get("knowledgeSearch") or options.get("knowledge_search")
    else:
        input_val = options.input
        resources = options.resources
        provider = options.provider
        signal = options.signal
        role_prompt = getattr(options, "rolePrompt", "") or ""
        knowledge_search = getattr(options, "knowledgeSearch", None)

    max_prompt_chars = int(os.environ.get("MAX_PROMPT_CHARS", "120000"))
    skill_md = getattr(resources, "skillMd", None) or getattr(
        resources, "skill_md", ""
    )

    sys_prompt, user_prompt = _call_build_generate_prompt(input_val, skill_md, role_prompt)
    initial_context_chars = len(sys_prompt) + len(user_prompt)

    reader_options = SkillResourceReaderOptions(
        maxContextChars=max_prompt_chars,
        initialContextChars=initial_context_chars,
    )
    reader = SkillResourceReader(resources, reader_options)

    visible_output = ""
    run_usage: Optional[Dict[str, Any]] = None

    run_skill_fn = getattr(provider, "run_skill", None) or getattr(
        provider, "runSkill", None
    )
    if run_skill_fn is None:
        raise RuntimeError("Provider does not have runSkill or run_skill method")

    run_kwargs = {
        "systemPrompt": sys_prompt,
        "system_prompt": sys_prompt,
        "userPrompt": user_prompt,
        "user_prompt": user_prompt,
        "readResource": lambda p: reader.read(p),
        "read_resource": lambda p: reader.read(p),
        "searchKnowledge": knowledge_search,
        "search_knowledge": knowledge_search,
        "signal": signal,
    }

    stream = run_skill_fn(ModelSkillRunInput(**run_kwargs))
    if hasattr(stream, "__aiter__"):
        async for chunk in stream:
            if _is_aborted(signal):
                raise ClientDisconnectedError(
                    "CLIENT_DISCONNECTED: Execution aborted during run"
                )
            delta = getattr(chunk, "contentDelta", None) or getattr(
                chunk, "content_delta", None
            )
            if delta:
                visible_output += delta
            usage = getattr(chunk, "usage", None) or (
                chunk.get("usage") if isinstance(chunk, dict) else None
            )
            if usage:
                run_usage = usage
    else:
        for chunk in stream:
            if _is_aborted(signal):
                raise ClientDisconnectedError(
                    "CLIENT_DISCONNECTED: Execution aborted during run"
                )
            delta = getattr(chunk, "contentDelta", None) or getattr(
                chunk, "content_delta", None
            )
            if delta:
                visible_output += delta
            usage = getattr(chunk, "usage", None) or (
                chunk.get("usage") if isinstance(chunk, dict) else None
            )
            if usage:
                run_usage = usage

    trimmed = visible_output.strip()
    if not trimmed:
        raise VmChatRunError(
            "EMPTY_MODEL_OUTPUT", "AI 助手未生成有效内容，请重试"
        )

    classified = _classify_model_output(trimmed)

    if classified["kind"] == "text":
        output_text = str(classified.get("text") or trimmed)
        max_output_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
        if len(output_text) > max_output_chars:
            raise VmChatRunError(
                "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
                f"生成的文本长度 ({len(output_text)}) 超过上限 ({max_output_chars})",
            )
        tokens = {
            "prompt_tokens": int(
                (run_usage or {}).get("prompt_tokens", 0)
                if isinstance(run_usage, dict)
                else getattr(run_usage, "prompt_tokens", 0) or 0
            ),
            "completion_tokens": int(
                (run_usage or {}).get("completion_tokens", 0)
                if isinstance(run_usage, dict)
                else getattr(run_usage, "completion_tokens", 0) or 0
            ),
            "total_tokens": int(
                (run_usage or {}).get("total_tokens", 0)
                if isinstance(run_usage, dict)
                else getattr(run_usage, "total_tokens", 0) or 0
            ),
        }
        return OrchestratorOutput(
            resultType="text",
            text=output_text,
            attemptCount=1,
            repairAttempts=0,
            usage=tokens,
        )

    initial_candidate = classified.get("candidate")
    initial_issues = classified.get("issues")

    read_res = reader.get_read_resources()
    repaired = await validate_and_repair_dsl(
        initialCandidate=initial_candidate,
        initialIssues=initial_issues,
        initialUsage=run_usage,
        input=input_val,
        resourceContext=read_res,
        resources=resources,
        provider=provider,
        signal=signal,
    )

    return OrchestratorOutput(
        resultType="dsl",
        text=repaired["text"],
        attemptCount=repaired["attemptCount"],
        repairAttempts=repaired["repairAttempts"],
        usage=repaired["usage"],
    )


runVmChatOrchestrator = run_vm_chat_orchestrator


async def stream_vm_chat(
    options: Union[StreamOrchestratorOptions, Dict[str, Any]],
) -> AsyncGenerator[HermesSseEvent, None]:
    if isinstance(options, dict):
        input_val = options.get("input")
        resources = options.get("resources")
        provider = options.get("provider")
        signal = options.get("signal")
        role_prompt = options.get("rolePrompt") or options.get("role_prompt") or ""
        knowledge_search = options.get("knowledgeSearch") or options.get("knowledge_search")
        msg_chunk_chars = options.get("messageChunkChars") or options.get(
            "message_chunk_chars"
        )
    else:
        input_val = options.input
        resources = options.resources
        provider = options.provider
        signal = options.signal
        role_prompt = getattr(options, "rolePrompt", "") or ""
        knowledge_search = getattr(options, "knowledgeSearch", None)
        msg_chunk_chars = getattr(options, "messageChunkChars", None) or getattr(
            options, "message_chunk_chars", None
        )

    normalized_chunk_size = (
        int(msg_chunk_chars)
        if (
            msg_chunk_chars is not None
            and isinstance(msg_chunk_chars, int)
            and msg_chunk_chars > 0
        )
        else 256
    )

    max_prompt_chars = int(os.environ.get("MAX_PROMPT_CHARS", "120000"))
    skill_md = getattr(resources, "skillMd", None) or getattr(
        resources, "skill_md", ""
    )

    sys_prompt, user_prompt = _call_build_generate_prompt(input_val, skill_md, role_prompt)
    initial_context_chars = len(sys_prompt) + len(user_prompt)

    reader_options = SkillResourceReaderOptions(
        maxContextChars=max_prompt_chars,
        initialContextChars=initial_context_chars,
    )
    reader = SkillResourceReader(resources, reader_options)

    visible_output = ""
    initial_usage: Optional[Dict[str, Any]] = None
    reasoning_seq = 0

    run_skill_fn = getattr(provider, "run_skill", None) or getattr(
        provider, "runSkill", None
    )
    if run_skill_fn is None:
        raise RuntimeError("Provider does not have runSkill or run_skill method")

    run_kwargs = ModelSkillRunInput(
        system_prompt=sys_prompt,
        user_prompt=user_prompt,
        read_resource=lambda p: reader.read(p),
        search_knowledge=knowledge_search,
        signal=signal,
    )

    stream = run_skill_fn(run_kwargs)
    if hasattr(stream, "__aiter__"):
        async for chunk in stream:
            if _is_aborted(signal):
                raise ClientDisconnectedError(
                    "CLIENT_DISCONNECTED: Execution aborted during stream"
                )

            r_delta = getattr(chunk, "reasoningDelta", None) or getattr(
                chunk, "reasoning_delta", None
            )
            if r_delta:
                reasoning_seq += 1
                yield ReasoningDeltaEvent(delta=r_delta, sequence=reasoning_seq)

            c_delta = getattr(chunk, "contentDelta", None) or getattr(
                chunk, "content_delta", None
            )
            if c_delta:
                visible_output += c_delta

            usage = getattr(chunk, "usage", None) or (
                chunk.get("usage") if isinstance(chunk, dict) else None
            )
            if usage:
                initial_usage = usage
    else:
        for chunk in stream:
            if _is_aborted(signal):
                raise ClientDisconnectedError(
                    "CLIENT_DISCONNECTED: Execution aborted during stream"
                )

            r_delta = getattr(chunk, "reasoningDelta", None) or getattr(
                chunk, "reasoning_delta", None
            )
            if r_delta:
                reasoning_seq += 1
                yield ReasoningDeltaEvent(delta=r_delta, sequence=reasoning_seq)

            c_delta = getattr(chunk, "contentDelta", None) or getattr(
                chunk, "content_delta", None
            )
            if c_delta:
                visible_output += c_delta

            usage = getattr(chunk, "usage", None) or (
                chunk.get("usage") if isinstance(chunk, dict) else None
            )
            if usage:
                initial_usage = usage

    trimmed = visible_output.strip()
    if not trimmed:
        raise VmChatRunError(
            "EMPTY_MODEL_OUTPUT", "AI 助手未生成有效内容，请重试"
        )

    classified = _classify_model_output(trimmed)
    final_text = ""
    final_usage: Optional[Dict[str, Any]] = None

    if classified["kind"] == "text":
        final_text = str(classified.get("text") or trimmed)
        max_output_chars = int(os.environ.get("MAX_FINAL_OUTPUT_CHARS", "200000"))
        if len(final_text) > max_output_chars:
            raise VmChatRunError(
                "MAX_FINAL_OUTPUT_CHARS_EXCEEDED",
                f"生成的文本长度 ({len(final_text)}) 超过上限 ({max_output_chars})",
            )
        final_usage = initial_usage or {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
        }
    else:
        try:
            repaired = await validate_and_repair_dsl(
                initialCandidate=classified.get("candidate"),
                initialIssues=classified.get("issues"),
                initialUsage=initial_usage,
                input=input_val,
                resourceContext=reader.get_read_resources(),
                resources=resources,
                provider=provider,
                signal=signal,
            )
            final_text = repaired["text"]
            final_usage = repaired["usage"]
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield RunFailedEvent(error=f"AI 助手任务执行失败: {str(e)}")
            return

    for chunk in code_point_chunks(final_text, normalized_chunk_size):
        yield MessageDeltaEvent(delta=chunk)

    yield RunCompletedEvent(output=final_text, usage=final_usage or {})


streamVmChat = stream_vm_chat
