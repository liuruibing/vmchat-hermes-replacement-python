import json
import os
import re
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
from langchain_core.tools import tool
from langchain_core.messages import ToolMessage, AIMessageChunk

from app.provider.fixed_provider import (
    ModelGenerateInput,
    ModelGenerateOutput,
    ModelSkillRunInput,
    ModelStreamChunk,
    VmChatModelProvider,
    is_aborted,
)


class VmChatModelResultSchema(BaseModel):
    type: Literal["dsl", "text"]
    category: Optional[Literal["clarify", "reject"]] = None
    dsl: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    text: Optional[str] = None

    def to_result(self) -> Dict[str, Any]:
        if self.type == "dsl":
            return {"type": "dsl", "dsl": self.dsl}
        else:
            return {"type": "text", "category": self.category, "text": self.text}


def extract_first_json_value(text: str) -> Optional[str]:
    if not text:
        return None
    start_idx = -1
    for i, ch in enumerate(text):
        if ch in ("{", "["):
            start_idx = i
            break
    if start_idx == -1:
        return None

    stack = []
    in_string = False
    escape_next = False

    for i in range(start_idx, len(text)):
        ch = text[i]
        if escape_next:
            escape_next = False
            continue
        if ch == "\\":
            escape_next = True
            continue
        if ch == '"':
            in_string = not in_string
            continue
        if in_string:
            continue

        if ch in ("{", "["):
            stack.append(ch)
        elif ch in ("}", "]"):
            expected = "{" if ch == "}" else "["
            if not stack or stack[-1] != expected:
                return None
            stack.pop()
            if not stack:
                return text[start_idx : i + 1]

    return None


extractFirstJsonValue = extract_first_json_value
extract_first_json_object = extract_first_json_value
extractFirstJsonObject = extract_first_json_value


def normalize_usage_metadata(raw: Any) -> Optional[Dict[str, int]]:
    if not raw or not isinstance(raw, dict):
        return None
    prompt_tokens = int(raw.get("prompt_tokens") or raw.get("input_tokens") or 0)
    completion_tokens = int(raw.get("completion_tokens") or raw.get("output_tokens") or 0)
    total_tokens = int(raw.get("total_tokens") or (prompt_tokens + completion_tokens))
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


normalizeUsageMetadata = normalize_usage_metadata


class ThinkTagState:
    def __init__(self, in_tag: bool = False, buffer: str = ""):
        self.in_tag = in_tag
        self.inTag = in_tag
        self.buffer = buffer


def create_think_tag_state() -> ThinkTagState:
    return ThinkTagState()


createThinkTagState = create_think_tag_state


def parse_think_tags(text: str, state: ThinkTagState) -> Dict[str, str]:
    reasoning = ""
    content = ""

    input_text = state.buffer + text
    state.buffer = ""

    i = 0
    while i < len(input_text):
        if input_text[i] == "<":
            if not state.in_tag:
                remain = len(input_text) - i
                candidate = input_text[i : i + 7]
                if candidate == "<think>":
                    state.in_tag = True
                    state.inTag = True
                    i += 7
                    continue
                if remain < 7 and "<think>".startswith(input_text[i:]):
                    state.buffer = input_text[i:]
                    return {"reasoning": reasoning, "content": content}
                content += "<"
                i += 1
                continue

            remain = len(input_text) - i
            candidate = input_text[i : i + 8]
            if candidate == "</think>":
                state.in_tag = False
                state.inTag = False
                i += 8
                continue
            if remain < 8 and "</think>".startswith(input_text[i:]):
                state.buffer = input_text[i:]
                return {"reasoning": reasoning, "content": content}
            reasoning += "<"
            i += 1
            continue

        if state.in_tag:
            reasoning += input_text[i]
        else:
            content += input_text[i]
        i += 1

    return {"reasoning": reasoning, "content": content}


parseThinkTags = parse_think_tags


class ReadSkillResourceInput(BaseModel):
    path: str = Field(description="Relative path to skill resource file")


class LangChainVmChatProvider(VmChatModelProvider):
    def __init__(
        self,
        options: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        mode: Optional[Literal["structured", "text-json"]] = None,
    ):
        opts = options or {}
        self.model_name = (
            model_name
            or opts.get("modelName")
            or opts.get("model_name")
            or os.getenv("LLM_MODEL")
            or "deepseek-v4-flash"
        )
        self.base_url = (
            base_url
            or opts.get("baseURL")
            or opts.get("base_url")
            or os.getenv("LLM_BASE_URL")
            or ""
        )
        self.api_key = (
            api_key
            or opts.get("apiKey")
            or opts.get("api_key")
            or os.getenv("LLM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or ""
        )
        self.mode = (
            mode
            or opts.get("mode")
            or os.getenv("LLM_OUTPUT_MODE")
            or "structured"
        )

    def build_model(self) -> ChatDeepSeek:
        kwargs: Dict[str, Any] = {
            "model": self.model_name,
            "temperature": 0,
            "max_retries": 0,
            "timeout": 120,
        }
        if self.base_url:
            kwargs["base_url"] = self.base_url
        if self.api_key:
            kwargs["api_key"] = self.api_key
        return ChatDeepSeek(**kwargs)

    async def generate(self, input: ModelGenerateInput) -> ModelGenerateOutput:
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request aborted")

        model = self.build_model()
        messages = [
            {"role": "system", "content": input.systemPrompt},
            {"role": "user", "content": input.userPrompt},
        ]

        if self.mode == "structured":
            try:
                structured_model = model.with_structured_output(
                    VmChatModelResultSchema,
                    name="vmchat_result",
                    strict=True,
                    include_raw=True,
                )
                res = await structured_model.ainvoke(messages)
                raw_msg = res.get("raw") if isinstance(res, dict) else None
                parsed_obj = res.get("parsed") if isinstance(res, dict) else res

                usage_meta = getattr(raw_msg, "usage_metadata", None) if raw_msg else None
                if not usage_meta and raw_msg and hasattr(raw_msg, "response_metadata"):
                    usage_meta = raw_msg.response_metadata.get("usage")
                usage = normalize_usage_metadata(usage_meta)

                if isinstance(parsed_obj, VmChatModelResultSchema):
                    parsed_res = parsed_obj.to_result()
                elif isinstance(parsed_obj, dict):
                    parsed_res = parsed_obj
                else:
                    parsed_res = parsed_obj

                return ModelGenerateOutput(result=parsed_res, usage=usage)
            except Exception as err:
                msg = str(err)
                raise RuntimeError(f"MODEL_STRUCTURED_OUTPUT_FAILED: {msg}")

        # mode === "text-json"
        try:
            res = await model.ainvoke(messages)
            usage = normalize_usage_metadata(
                getattr(res, "usage_metadata", None)
                or (getattr(res, "response_metadata", {}).get("usage") if hasattr(res, "response_metadata") else None)
            )
            content_text = res.content if isinstance(res.content, str) else json.dumps(res.content, ensure_ascii=False)

            json_str = extract_first_json_value(content_text)
            if not json_str:
                plain_text = content_text.strip()
                if plain_text and re.search(r"[\u3400-\u9fff]", plain_text) and not re.search(r"<think>|</think>", plain_text, re.IGNORECASE):
                    return ModelGenerateOutput(
                        result={"type": "text", "category": "clarify", "text": plain_text},
                        usage=usage,
                    )
                raise RuntimeError("No balanced JSON value or safe text found in output")

            parsed_json = json.loads(json_str)
            try:
                validated = VmChatModelResultSchema.model_validate(parsed_json)
                if validated.type == "dsl" and validated.dsl is not None:
                    return ModelGenerateOutput(
                        result={"type": "dsl", "dsl": validated.dsl},
                        usage=usage,
                    )
                elif validated.type == "text" and validated.category in ("clarify", "reject") and validated.text is not None:
                    return ModelGenerateOutput(
                        result={"type": "text", "category": validated.category, "text": validated.text},
                        usage=usage,
                    )
                raise ValueError("Validation failed")
            except Exception as val_err:
                is_direct_dsl = isinstance(parsed_json, list) or (
                    isinstance(parsed_json, dict)
                    and ("action" in parsed_json or "requests" in parsed_json or "views" in parsed_json)
                )
                if is_direct_dsl:
                    return ModelGenerateOutput(
                        result={"type": "dsl", "dsl": parsed_json},
                        usage=usage,
                    )
                raise RuntimeError(str(val_err))
        except Exception as err:
            msg = str(err)
            if msg.startswith("MODEL_TEXT_JSON_PARSE_FAILED:"):
                raise err
            raise RuntimeError(f"MODEL_TEXT_JSON_PARSE_FAILED: {msg}")

    async def stream(self, input: ModelGenerateInput):
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request aborted")

        model = self.build_model()
        messages = [
            {"role": "system", "content": input.systemPrompt},
            {"role": "user", "content": input.userPrompt},
        ]

        tag_state = create_think_tag_state()
        last_usage: Optional[Dict[str, int]] = None

        async for chunk in model.astream(messages):
            if is_aborted(input.signal):
                raise RuntimeError("ABORTED: Request aborted during stream")

            usage_meta = getattr(chunk, "usage_metadata", None)
            if not usage_meta and hasattr(chunk, "response_metadata"):
                usage_meta = getattr(chunk, "response_metadata", {}).get("usage")
            if usage_meta:
                norm_usage = normalize_usage_metadata(usage_meta)
                if norm_usage:
                    last_usage = norm_usage

            additional_kwargs = getattr(chunk, "additional_kwargs", {}) or {}
            additional_reasoning = (
                additional_kwargs.get("reasoning_content")
                or additional_kwargs.get("reasoning")
                or additional_kwargs.get("thinking")
                or ""
            )

            if additional_reasoning:
                yield ModelStreamChunk(reasoningDelta=additional_reasoning)

            raw_content = chunk.content if isinstance(chunk.content, str) else ""
            if raw_content:
                parsed = parse_think_tags(raw_content, tag_state)
                if parsed["reasoning"]:
                    yield ModelStreamChunk(reasoningDelta=parsed["reasoning"])
                if parsed["content"]:
                    yield ModelStreamChunk(contentDelta=parsed["content"])

        if tag_state.buffer:
            if tag_state.in_tag:
                yield ModelStreamChunk(reasoningDelta=tag_state.buffer)
            else:
                yield ModelStreamChunk(contentDelta=tag_state.buffer)
            tag_state.buffer = ""

        yield ModelStreamChunk(
            usage=last_usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            done=True,
        )

    async def run_skill(self, input: ModelSkillRunInput):
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request aborted")

        model = self.build_model()
        @tool("read_vmchat_skill_resource", args_schema=ReadSkillResourceInput)
        def read_resource_tool(path: str) -> str:
            """Read a vmchat skill resource file by path."""
            if input.read_resource:
                return input.read_resource(path)
            return ""
        bound_model = model.bind_tools([read_resource_tool])
        
        messages: List[Any] = [
            {"role": "system", "content": input.systemPrompt},
            {"role": "user", "content": input.userPrompt},
        ]

        turn_count = 0
        read_count = 0
        max_resource_reads = int(os.getenv("MAX_SKILL_RESOURCE_READS", "24"))
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0

        while True:
            turn_count += 1
            if turn_count > 12:
                raise RuntimeError("SKILL_AGENT_TURN_LIMIT_EXCEEDED: Exceeded 12 turns")

            if is_aborted(input.signal):
                raise RuntimeError("ABORTED: Request aborted")

            tag_state = create_think_tag_state()
            accumulated_chunk: Optional[AIMessageChunk] = None
            turn_prompt_tokens = 0
            turn_completion_tokens = 0
            turn_total_tokens = 0

            async for chunk in bound_model.astream(messages):
                if is_aborted(input.signal):
                    raise RuntimeError("ABORTED: Request aborted during stream")

                accumulated_chunk = accumulated_chunk + chunk if accumulated_chunk else chunk

                usage_meta = getattr(chunk, "usage_metadata", None)
                if usage_meta:
                    turn_prompt_tokens = usage_meta.get("input_tokens", turn_prompt_tokens)
                    turn_completion_tokens = usage_meta.get("output_tokens", turn_completion_tokens)
                    turn_total_tokens = usage_meta.get("total_tokens", turn_total_tokens)

                additional_kwargs = getattr(chunk, "additional_kwargs", {}) or {}
                additional_reasoning = (
                    additional_kwargs.get("reasoning_content")
                    or additional_kwargs.get("reasoning")
                    or additional_kwargs.get("thinking")
                    or ""
                )

                if additional_reasoning:
                    yield ModelStreamChunk(reasoningDelta=additional_reasoning)

                raw_content = chunk.content if isinstance(chunk.content, str) else ""
                if raw_content:
                    parsed = parse_think_tags(raw_content, tag_state)
                    if parsed["reasoning"]:
                        yield ModelStreamChunk(reasoningDelta=parsed["reasoning"])

            total_prompt_tokens += turn_prompt_tokens
            total_completion_tokens += turn_completion_tokens
            total_tokens += turn_total_tokens or (turn_prompt_tokens + turn_completion_tokens)

            tool_calls = (
                accumulated_chunk.tool_calls
                if accumulated_chunk and getattr(accumulated_chunk, "tool_calls", None)
                else (
                    getattr(accumulated_chunk, "tool_call_chunks", [])
                    if accumulated_chunk
                    else []
                )
            )

            if tool_calls and len(tool_calls) > 0:
                messages.append(accumulated_chunk)

                for tc in tool_calls:
                    call_id = tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", None)
                    tool_name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)

                    if not call_id or tool_name != "read_vmchat_skill_resource":
                        messages.append(
                            ToolMessage(
                                content="RESOURCE_NOT_ALLOWED",
                                tool_call_id=call_id or "invalid_tool_call",
                            )
                        )
                        continue

                    raw_args = tc.get("args") if isinstance(tc, dict) else getattr(tc, "args", None)
                    path_arg: Optional[str] = None
                    if isinstance(raw_args, dict) and isinstance(raw_args.get("path"), str):
                        path_arg = raw_args["path"]
                    elif isinstance(raw_args, str):
                        try:
                            parsed_args = json.loads(raw_args)
                            if isinstance(parsed_args, dict) and isinstance(parsed_args.get("path"), str):
                                path_arg = parsed_args["path"]
                        except Exception:
                            path_arg = None

                    if not path_arg:
                        messages.append(
                            ToolMessage(
                                content="RESOURCE_NOT_ALLOWED",
                                tool_call_id=call_id,
                            )
                        )
                        continue

                    read_count += 1
                    if read_count > max_resource_reads:
                        raise RuntimeError(
                            f"SKILL_RESOURCE_READ_LIMIT_EXCEEDED: Exceeded {max_resource_reads} resource reads"
                        )

                    read_fn = getattr(input, "readResource", None) or getattr(input, "read_resource", None)
                    tool_result_text = read_fn(path_arg) if callable(read_fn) else ""

                    messages.append(
                        ToolMessage(
                            content=tool_result_text,
                            tool_call_id=call_id,
                        )
                    )
            else:
                if accumulated_chunk:
                    raw_content = accumulated_chunk.content
                    content_text = raw_content if isinstance(raw_content, str) else json.dumps(raw_content, ensure_ascii=False)

                    final_parsed = parse_think_tags(content_text, create_think_tag_state())
                    visible_text = final_parsed["content"] or content_text
                    clean_text = re.sub(r"<think>[\s\S]*?</think>", "", visible_text, flags=re.IGNORECASE).strip()
                    if clean_text:
                        yield ModelStreamChunk(contentDelta=clean_text)

                if tag_state.buffer and not tag_state.in_tag:
                    yield ModelStreamChunk(contentDelta=tag_state.buffer)

                yield ModelStreamChunk(
                    usage={
                        "prompt_tokens": total_prompt_tokens,
                        "completion_tokens": total_completion_tokens,
                        "total_tokens": total_tokens,
                    },
                    done=True,
                )
                break
