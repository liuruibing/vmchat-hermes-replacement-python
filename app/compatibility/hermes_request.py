import json
import re
from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field


class HermesChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class HermesCreateRunRequest(BaseModel):
    model: str
    input: List[HermesChatMessage]
    instructions: str
    session_id: str
    skills: List[str]
    tools: List[Any] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    agent_id: str = "performance-ai"
    role_id: str = "performance-analyst"


class VmReportDslRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    moduleId: Optional[str] = None
    sqlCode: Optional[str] = None
    submoduleId: Optional[str] = None
    params: Optional[Dict[str, Any]] = None


class VmReportDsl(BaseModel):
    model_config = ConfigDict(extra="allow")

    action: Optional[str] = None
    id: Optional[str] = None
    title: Optional[str] = None
    targetBlockId: Optional[str] = None
    requests: Optional[List[Union[VmReportDslRequest, Dict[str, Any]]]] = None
    transform: Optional[Union[str, Dict[str, Any]]] = None
    view: Optional[Dict[str, Any]] = None
    views: Optional[List[Dict[str, Any]]] = None


class CurrentDslItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    blockId: str
    id: str
    title: str
    viewType: Optional[str] = None
    dsl: Union[VmReportDsl, Dict[str, Any]]


class GlobalQueryParameters(BaseModel):
    names: List[str] = Field(default_factory=list)
    nonemptyFlags: Dict[str, bool] = Field(default_factory=dict)


class VmChatInput(BaseModel):
    userMessage: str
    selectedBlockId: Optional[str] = None
    currentDsls: List[CurrentDslItem] = Field(default_factory=list)
    globalQueryParameters: GlobalQueryParameters
    historyMessages: List[HermesChatMessage] = Field(default_factory=list)
    sessionSummary: str = ""
    agentId: str = "performance-ai"
    roleId: str = "performance-analyst"


def extract_json_block(text: str, marker: str) -> str:
    """
    Extract one JSON value from a prompt marker without confusing nested arrays
    or braces with the end of the top-level value.
    """
    marker_index = text.find(marker)
    if marker_index == -1:
        return ""

    marker_line_end = text.find("\n", marker_index + len(marker))
    if marker_line_end == -1:
        start_pos = marker_index + len(marker)
    else:
        start_pos = marker_line_end + 1

    source = text[start_pos:].lstrip()
    if not source or (source[0] != "[" and source[0] != "{"):
        raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed JSON block")

    stack: List[str] = []
    in_string = False
    escaped = False

    for i, char in enumerate(source):
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

        if char in ("[", "{"):
            stack.append(char)
            continue

        if char not in ("]", "}"):
            continue

        expected = "[" if char == "]" else "{"
        if not stack or stack.pop() != expected:
            raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed JSON block")

        if len(stack) == 0:
            return source[: i + 1]

    raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed JSON block")


def normalize_create_run_request(raw: Any) -> HermesCreateRunRequest:
    if not isinstance(raw, dict):
        raise ValueError("INVALID_REQUEST_FORMAT: Request body must be a JSON object")

    model = raw["model"][:256] if isinstance(raw.get("model"), str) else "deepseek-v4-flash"
    session_id = raw["session_id"][:256] if isinstance(raw.get("session_id"), str) else "default-session"
    agent_id = raw["agent_id"][:128] if isinstance(raw.get("agent_id"), str) else "performance-ai"
    role_id = raw["role_id"][:128] if isinstance(raw.get("role_id"), str) else "performance-analyst"
    instructions = raw["instructions"][:512000] if isinstance(raw.get("instructions"), str) else ""

    raw_context = raw.get("context") or {}
    if not isinstance(raw_context, dict):
        raise ValueError("INVALID_REQUEST_FORMAT: context must be an object")
    try:
        context_size = len(json.dumps(raw_context, ensure_ascii=False))
    except Exception as err:
        raise ValueError("INVALID_REQUEST_FORMAT: context must be JSON serializable") from err
    if context_size > 512000:
        raise ValueError("INVALID_REQUEST_FORMAT: context is too large")

    if raw.get("tools") is not None:
        if not isinstance(raw["tools"], list):
            raise ValueError("INVALID_REQUEST_FORMAT: tools must be an array")
        if len(raw["tools"]) > 0:
            raise ValueError("UNSUPPORTED_TOOLS: Tools execution is not supported by vmChat backend")

    skills: List[str] = []
    if raw.get("skills") is not None:
        if not isinstance(raw["skills"], list):
            raise ValueError("INVALID_REQUEST_FORMAT: skills must be an array")
        for skill in raw["skills"]:
            s_str = str(skill)
            if s_str != "vm-report-dsl":
                raise ValueError(f"UNSUPPORTED_SKILLS: Skill '{s_str}' is not supported")
            if s_str not in skills:
                skills.append(s_str)

    raw_input = raw.get("input")
    if not isinstance(raw_input, list) or len(raw_input) == 0 or len(raw_input) > 20:
        raise ValueError("INVALID_REQUEST_FORMAT: input must be an array of 1 to 20 messages")

    input_msgs: List[HermesChatMessage] = []
    for item in raw_input:
        if not isinstance(item, dict):
            raise ValueError("INVALID_REQUEST_FORMAT: input item must be an object")

        role = str(item.get("role"))
        if role not in ("user", "assistant"):
            raise ValueError(f"INVALID_REQUEST_FORMAT: Invalid role '{role}'")

        content = item.get("content")
        if not isinstance(content, str):
            raise ValueError("INVALID_REQUEST_FORMAT: Message content must be a string")

        content_str = content[:16000]
        input_msgs.append(HermesChatMessage(role=role, content=content_str))

    return HermesCreateRunRequest(
        model=model,
        input=input_msgs,
        instructions=instructions,
        session_id=session_id,
        skills=skills,
        tools=[],
        context=raw_context,
        agent_id=agent_id or "performance-ai",
        role_id=role_id or "performance-analyst",
    )


def normalize_vm_chat_input(request: HermesCreateRunRequest) -> VmChatInput:
    user_message = ""
    last_user_index = -1
    for idx in range(len(request.input) - 1, -1, -1):
        item = request.input[idx]
        if item.role == "user":
            user_message = item.content
            last_user_index = idx
            break

    history_source = request.input[:last_user_index] if last_user_index >= 0 else request.input
    history_messages = [
        item
        for item in history_source
        if item.role in ("user", "assistant")
        and not (
            item.role == "user"
            and item.content.strip().startswith("vmChat 会话锚点：")
        )
    ]

    # Prefer structured machine context. The legacy instruction markers remain a
    # compatibility fallback for older frontends.
    context = request.context if isinstance(request.context, dict) else {}
    text_to_search = "\n".join([request.instructions] + [i.content for i in request.input])

    selected_block_id: Optional[str] = None
    context_selected = context.get("selectedBlockId")
    if isinstance(context_selected, str) and context_selected.strip():
        selected_block_id = context_selected.strip()
    else:
        sel_block_match = re.search(r"当前 selectedBlockId：\s*([^\n]+)", text_to_search)
        if sel_block_match and sel_block_match.group(1):
            val = sel_block_match.group(1).strip()
            if val and val != "null" and val != "undefined":
                selected_block_id = val

    current_dsls: List[CurrentDslItem] = []
    if "currentDsls" in context:
        parsed = context.get("currentDsls")
        if not isinstance(parsed, list):
            raise ValueError("INVALID_VMCHAT_CONTEXT: currentDsls is not an array")
        try:
            current_dsls = [
                item if isinstance(item, CurrentDslItem) else CurrentDslItem.model_validate(item)
                for item in parsed
            ]
        except Exception as err:
            raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed currentDsls context") from err
    elif "当前 currentDsls：" in text_to_search:
        try:
            json_str = extract_json_block(text_to_search, "当前 currentDsls：")
            parsed = json.loads(json_str)
            if not isinstance(parsed, list):
                raise ValueError("INVALID_VMCHAT_CONTEXT: currentDsls is not an array")
            current_dsls = [
                item if isinstance(item, CurrentDslItem) else CurrentDslItem.model_validate(item)
                for item in parsed
            ]
        except Exception as err:
            if isinstance(err, ValueError) and str(err).startswith("INVALID_VMCHAT_CONTEXT"):
                raise err
            raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed currentDsls JSON block") from err

    names: List[str] = []
    nonempty_flags: Dict[str, bool] = {}
    context_params = context.get("globalQueryParams")
    if context_params is None:
        context_params = context.get("globalQueryParameters")

    if context_params is not None:
        if not isinstance(context_params, dict) or isinstance(context_params, list):
            raise ValueError("INVALID_VMCHAT_CONTEXT: globalQueryParams is not an object")
        for k, val in context_params.items():
            names.append(str(k))
            val_str = str(val).strip() if val is not None else ""
            nonempty_flags[str(k)] = bool(val and len(val_str) > 0)
    elif "当前全局查询条件" in text_to_search:
        try:
            json_str = extract_json_block(text_to_search, "当前全局查询条件")
            parsed_obj = json.loads(json_str)
            if not isinstance(parsed_obj, dict) or isinstance(parsed_obj, list):
                raise ValueError("INVALID_VMCHAT_CONTEXT: globalQueryParams is not an object")
            for k, val in parsed_obj.items():
                names.append(k)
                val_str = str(val).strip() if val is not None else ""
                nonempty_flags[k] = bool(val and len(val_str) > 0)
        except Exception as err:
            if isinstance(err, ValueError) and str(err).startswith("INVALID_VMCHAT_CONTEXT"):
                raise err
            raise ValueError("INVALID_VMCHAT_CONTEXT: Malformed globalQueryParams JSON block") from err

    return VmChatInput(
        userMessage=user_message,
        selectedBlockId=selected_block_id,
        currentDsls=current_dsls,
        globalQueryParameters=GlobalQueryParameters(
            names=names,
            nonemptyFlags=nonempty_flags,
        ),
        historyMessages=history_messages,
        sessionSummary="",
        agentId=request.agent_id,
        roleId=request.role_id,
    )


# Aliases for JS camelCase compatibility
extractJsonBlock = extract_json_block
normalizeCreateRunRequest = normalize_create_run_request
normalizeVmChatInput = normalize_vm_chat_input
