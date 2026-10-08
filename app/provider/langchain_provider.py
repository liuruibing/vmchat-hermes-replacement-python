# ==============================================================================
# 文件：app/provider/langchain_provider.py
# 文件作用：使用 LangChain 把模型服务包装成项目统一的 Provider 接口。
# 全局位置：工作流节点 → context.provider → 本文件 → ChatDeepSeek/ChatOpenAI → 模型服务。
# 谁调用它：main.py 按配置创建实例；聊天、报表和风险分析流程通过 Provider 接口调用它。
# 输入：模型名、服务地址和密钥，以及包含 Prompt、取消信号和工具回调的任务对象。
# 输出：完整生成结果，或含正文、过程说明及 token 用量的 ModelStreamChunk 片段。
# 主要流程：build_model 选客户端；generate 取完整结果；stream 接收片段；run_skill 控制工具循环。
# 前端类比：像封装 fetch/axios 的 API client；工具回调类似外部传入的读取和搜索函数。
# 边界：LangChain 提供模型/消息/工具接口，工具执行循环由本文件的 Python 代码控制。
# 阅读入口：先看 build_model()，再看 generate()，最后看 run_skill() 中的 bind_tools 和 while 循环。
# ==============================================================================

import json
import os
import re
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field
from langchain_deepseek import ChatDeepSeek
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    ChatOpenAI = None
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


# 普通 Python 类型提示类似 TypeScript 类型，本身不会自动校验传入的数据。
# 这里继承 Pydantic BaseModel，构造/解析对象时才会实际校验字段类型及 Literal 允许值。
# 这只检查结果结构；DSL 中的指标、字段是否可用，还需工作流的业务校验。
class VmChatModelResultSchema(BaseModel):
    # Literal 类似 TS 的字符串字面量联合；Optional[T] 类似 T | null；Union 允许多种类型。
    type: Literal["dsl", "text"]
    category: Optional[Literal["clarify", "reject"]] = None
    dsl: Optional[Union[Dict[str, Any], List[Dict[str, Any]]]] = None
    text: Optional[str] = None

    # 转成项目统一的字典结构，让调用方不用依赖 Pydantic 对象的具体实现。
    def to_result(self) -> Dict[str, Any]:
        if self.type == "dsl":
            return {"type": "dsl", "dsl": self.dsl}
        else:
            return {"type": "text", "category": self.category, "text": self.text}


# 模型可能在 JSON 前后添加文字；先找第一个完整的对象/数组，再交给 json.loads 校验语法。
# stack 记录尚未闭合的括号；字符串里的括号不参与配对，转义引号也不能结束字符串。
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


# 不同客户端用 input_tokens 或 prompt_tokens 等不同名字，统一后上层才能汇总用量。
# token 是模型处理文本的计数单位，不能直接等同于字符数或实际费用。
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


# 流式片段可能把 <think> 拆成 "<thi" 和 "nk>"，所以解析状态要跨片段保留。
# in_tag 表示当前是否位于标签内；buffer 暂存尚未完整收到的标签开头。
class ThinkTagState:
    def __init__(self, in_tag: bool = False, buffer: str = ""):
        self.in_tag = in_tag
        self.inTag = in_tag
        self.buffer = buffer


def create_think_tag_state() -> ThinkTagState:
    return ThinkTagState()


createThinkTagState = create_think_tag_state


# 有些服务把过程文字放进 <think> 标签；这里把它与正文分开，供上层决定如何展示。
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


# 工具参数结构及 Field 描述会告诉模型该传什么参数；后面的工具循环仍会检查实际返回值。
class ReadSkillResourceInput(BaseModel):
    path: str = Field(description="Relative path to skill resource file")


class SearchKnowledgeInput(BaseModel):
    query: str = Field(description="Natural-language query for relevant agent knowledge")


class LangChainVmChatProvider(VmChatModelProvider):
    def __init__(
        self,
        options: Optional[Dict[str, Any]] = None,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        mode: Optional[Literal["structured", "text-json"]] = None,
    ):
        # self 类似 JS 的 this；or 从左向右取第一个真值，实现显式参数 → options → 环境变量的优先级。
        # 同时接受 camelCase/snake_case 配置，方便前端与 Python 调用方使用同一接口。
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

    # * 后面的参数只能按名字传：build_model(timeout_seconds=60)，避免位置参数混淆。
    # 创建的是连接远端服务的客户端，并不是在本地训练或加载一个模型。
    def build_model(self, *, timeout_seconds: float = 120) -> Any:
        # 环境变量读出来是字符串，int 转成数字；未配置时使用默认的 "3"。
        retries = int(os.getenv("LLM_NETWORK_RETRIES", "3"))
        # kwargs 是参数字典，类似 JS 的 options；下方 **kwargs 会把键展开为函数的命名参数。
        kwargs: Dict[str, Any] = {
            "model": self.model_name,
            "temperature": 0,
            "max_retries": retries,
            "timeout": timeout_seconds,
        }
        if self.base_url:
            kwargs["base_url"] = self.base_url
        if self.api_key:
            kwargs["api_key"] = self.api_key

        # ChatOpenAI 也能连接配置了 base_url 的兼容服务；名字不代表请求一定发给 OpenAI。
        # 按模型名/地址选择适配器，让后面仍能统一使用 ainvoke、astream 等接口。
        is_deepseek = "deepseek" in (self.model_name or "").lower()
        if (not is_deepseek or "googleapis" in (self.base_url or "")) and ChatOpenAI is not None:
            return ChatOpenAI(**kwargs)
        return ChatDeepSeek(**kwargs)

    # async def + await 类似 JS 的 async/await：等待网络时可让出执行权，不是开一个新线程。
    # generate 的调用方一次拿到完整结果；它与下方 run_skill 的工具循环是两条不同路径。
    async def generate(self, input: ModelGenerateInput) -> ModelGenerateOutput:
        # signal 类似前端取消标记。这里在检查点停止流程，不能保证立刻中断正在等待的网络请求。
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request aborted")

        model = self.build_model()
        # system 提供任务规则，user 提供本次问题；messages 是按顺序交给模型的对话记录。
        messages = [
            {"role": "system", "content": input.systemPrompt},
            {"role": "user", "content": input.userPrompt},
        ]

        # structured 让模型客户端按 schema 接收/解析输出；支持程度取决于适配器及服务。
        if self.mode == "structured":
            try:
                structured_model = model.with_structured_output(
                    VmChatModelResultSchema,
                    name="vmchat_result",
                    strict=True,
                    include_raw=True,
                )
                # ainvoke 像 await 一次 API 请求，完成后返回整条模型消息。
                # include_raw=True 保留原始消息和 parsed 结果：前者可读用量，后者供业务使用。
                res = await structured_model.ainvoke(messages)
                raw_msg = res.get("raw") if isinstance(res, dict) else None
                parsed_obj = res.get("parsed") if isinstance(res, dict) else res

                # getattr(obj, "字段", 默认值) 类似带默认值的属性读取，兼容客户端的不同返回结构。
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

        # text-json 兼容只会返回文字的入口：先提取 JSON，再用 Pydantic 做运行时校验。
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
                # 没有 JSON 时，仅在满足现有文字规则的情况下按澄清回答返回，其他情况报解析错误。
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
                # 兼容旧格式：有些模型直接返回 DSL，而不是包在 {type, dsl} 外层里。
                is_direct_dsl = isinstance(parsed_json, list) or (
                    isinstance(parsed_json, dict)
                    and ("action" in parsed_json or "requests" in parsed_json or "views" in parsed_json)
                )
                if is_direct_dsl:
                    return ModelGenerateOutput(
                        result={"type": "dsl", "dsl": parsed_json},
                        usage=usage,
                    )
                if isinstance(parsed_json, dict):
                    text_val = (
                        parsed_json.get("text")
                        or parsed_json.get("reply")
                        or parsed_json.get("content")
                        or parsed_json.get("message")
                    )
                    if text_val and isinstance(text_val, str):
                        cat = parsed_json.get("category")
                        if cat not in ("clarify", "reject"):
                            cat = "clarify"
                        return ModelGenerateOutput(
                            result={"type": "text", "category": cat, "text": text_val},
                            usage=usage,
                        )
                raise RuntimeError(str(val_err))
        except Exception as err:
            msg = str(err)
            if msg.startswith("MODEL_TEXT_JSON_PARSE_FAILED:"):
                raise err
            raise RuntimeError(f"MODEL_TEXT_JSON_PARSE_FAILED: {msg}")

    # 包含 yield 的 async def 是异步生成器，类似 JS 的 async function*。
    # 调用方用 async for 消费片段；是否逐段发送到前端，还取决于工作流/SSE 层的处理。
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

        # chunk 是一小块模型消息，不保证是一句话，也可能只包含用量等元信息。
        async for chunk in model.astream(messages):
            if is_aborted(input.signal):
                raise RuntimeError("ABORTED: Request aborted during stream")

            usage_meta = getattr(chunk, "usage_metadata", None)
            if not usage_meta and hasattr(chunk, "response_metadata"):
                usage_meta = getattr(chunk, "response_metadata", {}).get("usage")
            # 用量可能到最后才出现；这里保存最近一次报告的值，不把每个片段重复累加。
            if usage_meta:
                norm_usage = normalize_usage_metadata(usage_meta)
                if norm_usage:
                    last_usage = norm_usage

            # 服务可能用专门字段发送过程文字，也可能混在正文的 <think> 标签里，两种都兼容。
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

        # 流结束后仍可能剩下不完整标签，按当前状态交回，避免无声丢掉尾部文字。
        if tag_state.buffer:
            if tag_state.in_tag:
                yield ModelStreamChunk(reasoningDelta=tag_state.buffer)
            else:
                yield ModelStreamChunk(contentDelta=tag_state.buffer)
            tag_state.buffer = ""

        # yield 把一个结果交给消费者；done=True 是本项目约定的结束标记，不是模型文字。
        yield ModelStreamChunk(
            usage=last_usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            done=True,
        )

    # 一次技能任务可以包含多轮：模型请求工具 → Python 执行 → 结果回填 → 再问模型。
    # 本项目自己写 while 循环控制这些轮次，并没有在这里使用 LangChain create_agent。
    async def run_skill(self, input: ModelSkillRunInput):
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request aborted")

        model = (self.build_model(timeout_seconds=input.timeout_seconds)
                 if input.timeout_seconds is not None else self.build_model())
        # @tool 把函数名、参数结构和 docstring 变成模型可读的工具说明；此时还没执行读取。
        @tool("read_vmchat_skill_resource", args_schema=ReadSkillResourceInput)
        def read_resource_tool(path: str) -> str:
            """Read one allow-listed agent resource by relative path."""
            if input.read_resource:
                return input.read_resource(path)
            return ""

        tools = [read_resource_tool]
        if input.search_knowledge:
            @tool("search_agent_knowledge", args_schema=SearchKnowledgeInput)
            def search_knowledge_tool(query: str) -> str:
                """Search the active agent knowledge base and return only relevant chunks."""
                if input.search_knowledge:
                    return input.search_knowledge(query)
                return "KNOWLEDGE_NOT_FOUND"
            tools.append(search_knowledge_tool)

        # bind_tools 声明“可请求哪些工具”，不会自动执行函数。下面根据工具名调用业务回调。
        bound_model = model.bind_tools(tools)
        
        messages: List[Any] = [
            {"role": "system", "content": input.systemPrompt},
            {"role": "user", "content": input.userPrompt},
        ]

        # 分别限制轮数、读取次数、搜索次数和回填字符量，防止循环失控或对话上下文过大。
        # chars 按 Python 字符串长度统计，与上面模型报告的 token 用量是不同概念。
        turn_count = 0
        read_count = 0
        max_resource_reads = int(os.getenv("MAX_SKILL_RESOURCE_READS", "24"))
        max_search_calls = int(os.getenv("MAX_KNOWLEDGE_SEARCH_CALLS", "6"))
        max_tool_context_chars = int(os.getenv("MAX_TOOL_CONTEXT_CHARS", "50000"))
        search_count = 0
        tool_context_chars = 0
        total_prompt_tokens = 0
        total_completion_tokens = 0
        total_tokens = 0

        # 每轮带上之前的消息和工具结果；没有工具请求就结束，否则继续到下一轮。
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

                # AIMessageChunk 的 + 是 LangChain 的合并操作：文字和被拆开的工具参数都要拼完整。
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

                # 工具阶段只逐段发出过程文字，正文在无工具调用的最终轮结束后统一交回。
                raw_content = chunk.content if isinstance(chunk.content, str) else ""
                if raw_content:
                    parsed = parse_think_tags(raw_content, tag_state)
                    if parsed["reasoning"]:
                        yield ModelStreamChunk(reasoningDelta=parsed["reasoning"])

            # 一轮内记录模型报告的用量，轮结束后再累计整个技能任务，避免按 chunk 重复计数。
            total_prompt_tokens += turn_prompt_tokens
            total_completion_tokens += turn_completion_tokens
            total_tokens += turn_total_tokens or (turn_prompt_tokens + turn_completion_tokens)

            # 优先读已拼完整的工具调用；兼容客户端仍只提供 tool_call_chunks 的情况。
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
                # 先保留模型的工具请求，再补对应的 ToolMessage，下一轮才能理解请求与结果的关系。
                messages.append(accumulated_chunk)

                for tc in tool_calls:
                    call_id = tc.get("id") if isinstance(tc, dict) else getattr(tc, "id", None)
                    tool_name = tc.get("name") if isinstance(tc, dict) else getattr(tc, "name", None)

                    # 模型输出仍是外部数据：只允许已有工具名，并要求有用于关联结果的调用 ID。
                    if not call_id or tool_name not in ("read_vmchat_skill_resource", "search_agent_knowledge"):
                        messages.append(
                            ToolMessage(
                                content="RESOURCE_NOT_ALLOWED",
                                tool_call_id=call_id or "invalid_tool_call",
                            )
                        )
                        continue

                    # 参数可能已是字典，也可能还是 JSON 字符串；先解析和检查，再交给业务函数。
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

                    if tool_name == "search_agent_knowledge":
                        query_arg: Optional[str] = None
                        if isinstance(raw_args, dict) and isinstance(raw_args.get("query"), str):
                            query_arg = raw_args["query"]
                        elif isinstance(raw_args, str):
                            try:
                                parsed_args = json.loads(raw_args)
                                if isinstance(parsed_args, dict) and isinstance(parsed_args.get("query"), str):
                                    query_arg = parsed_args["query"]
                            except Exception:
                                query_arg = None

                        search_count += 1
                        if search_count > max_search_calls:
                            messages.append(
                                ToolMessage(
                                    content="KNOWLEDGE_SEARCH_LIMIT_EXCEEDED",
                                    tool_call_id=call_id,
                                )
                            )
                            continue

                        # 这里直接调用同步回调，不使用 await；真正的检索实现由 input 提供。
                        search_fn = getattr(input, "searchKnowledge", None) or getattr(input, "search_knowledge", None)
                        tool_result_text = (
                            search_fn(query_arg)
                            if query_arg and callable(search_fn)
                            else "KNOWLEDGE_NOT_FOUND"
                        )
                        # 搜索结果也会占用下一轮模型上下文；超过额度时回填提示文字，而非全部内容。
                        if tool_context_chars + len(tool_result_text) > max_tool_context_chars:
                            tool_result_text = "KNOWLEDGE_CONTEXT_BUDGET_EXCEEDED"
                        else:
                            tool_context_chars += len(tool_result_text)
                        messages.append(
                            ToolMessage(content=tool_result_text, tool_call_id=call_id)
                        )
                        continue

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

                    # 同步读取回调还负责具体资源限制；Provider 再控制调用次数和总上下文量。
                    read_fn = getattr(input, "readResource", None) or getattr(input, "read_resource", None)
                    tool_result_text = read_fn(path_arg) if callable(read_fn) else ""
                    if tool_result_text not in (
                        "RESOURCE_NOT_ALLOWED",
                        "RESOURCE_ALREADY_READ",
                        "RESOURCE_CONTEXT_TOO_LARGE",
                        "RESOURCE_BUDGET_EXCEEDED",
                    ):
                        if tool_context_chars + len(tool_result_text) > max_tool_context_chars:
                            tool_result_text = "RESOURCE_BUDGET_EXCEEDED"
                        else:
                            tool_context_chars += len(tool_result_text)

                    # ToolMessage 是“工具执行结果”，tool_call_id 把它与前面的模型请求配对。
                    # 结果只是加入 messages；到下一轮 astream 时才真正发回模型。
                    messages.append(
                        ToolMessage(
                            content=tool_result_text,
                            tool_call_id=call_id,
                        )
                    )
            # 本轮没再请求工具，就将它当作最终回答；清理过程标签后向上层交回完整正文。
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
