import os
import json
from typing import Any, Dict, List, Optional, Union, Mapping, Iterable, Tuple
from pydantic import BaseModel, Field, ConfigDict

from app.compatibility.hermes_request import VmChatInput
from app.contracts.types import ValidationIssue
from app.prompt.generate_prompt import PromptOutput


class RepairPromptOptions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    invalidCandidate: Any = Field(..., alias="invalid_candidate")
    validationErrors: List[ValidationIssue] = Field(default_factory=list, alias="validation_errors")
    input: Union[VmChatInput, Dict[str, Any], Any]
    resourceContext: Optional[Union[Mapping[str, str], Any]] = Field(default=None, alias="resource_context")
    skillMd: str = Field(default="", alias="skill_md")
    maxPromptChars: Optional[int] = Field(default=None, alias="max_prompt_chars")

    @property
    def invalid_candidate(self) -> Any:
        return self.invalidCandidate

    @property
    def validation_errors(self) -> List[ValidationIssue]:
        return self.validationErrors

    @property
    def resource_context(self) -> Optional[Union[Mapping[str, str], Any]]:
        return self.resourceContext

    @property
    def skill_md(self) -> str:
        return self.skillMd

    @property
    def max_prompt_chars(self) -> Optional[int]:
        return self.maxPromptChars


def _build_repair_system_prompt(skill_md: str, include_full_skill: bool = True) -> str:
    lines = [
        "你是 VM Report DSL 修复专家。",
        "你生成的 DSL 尝试校验失败，必须根据下方提供的校验错误列表（Validation Issues）对原 DSL 进行针对性修补。",
        "你必须且只能输出修复后的合法 JSON 对象或 JSON 数组，不得输出任何 Markdown 代码围栏、自然语言解释或 Chain-of-Thought 思维链。",
        "本修复阶段没有 shell、Node、文件写入或脚本执行工具；Skill 中涉及 gen-uuid.js、validate-dsl.mjs 或临时文件的旧指令均不执行。Python 服务端会在你的修复结果返回后重新校验。",
        "修复时必须保持与原 ID 和已确认模块一致，优先严格按照 Validation Issues 修正字段、共同键、transform、视图、签名、缺失属性或语法限制；不得通过删除 request 或改成无关模块绕过语义校验。",
        "transform.function 必须按 request.id 从 responses 取数，例如 responses.req_averagePePb 或 responses['req_averagePePb']；禁止使用 responses[0]、responses[1] 等数组下标。",
        "view.type === 'echarts' 时，title、legend、dataset、xAxis/yAxis（Cartesian 时）和 series 必须为 view 的直接属性。禁止 view.echarts、view.options 或任何图表配置包装层。",
    ]
    if include_full_skill and skill_md:
        lines.extend(["# Skill 规则", skill_md])
    else:
        lines.extend([
            "# Skill 规则",
            "初始生成阶段已经应用完整 Skill；修复阶段以 Validation Issues、候选 DSL 与下方必要资源为准，不重复注入完整 Skill。",
        ])
    lines.extend([
        "",
        "# 修复阶段运行时覆盖",
        "- 不执行 Skill 中任何 Node、shell、临时文件或 validate-dsl.mjs 指令；只根据 Validation Issues 修复 JSON，随后由 Python 服务端重新校验。",
        "- 不得通过删除跨模块 request、改成无关模块、按数组下标对齐或隐藏共同键来绕过语义合并错误。",
    ])
    return "\n".join(lines)


def _candidate_request_metadata(candidate: Any) -> Tuple[set[str], bool, Optional[str]]:
    module_ids: set[str] = set()
    has_submodule = False
    view_type: Optional[str] = None

    def visit(value: Any) -> None:
        nonlocal has_submodule, view_type
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_none=True)
        if isinstance(value, list):
            for item in value:
                visit(item)
            return
        if not isinstance(value, dict):
            return

        requests = value.get("requests")
        if isinstance(requests, list):
            for request in requests:
                if isinstance(request, BaseModel):
                    request = request.model_dump(exclude_none=True)
                if not isinstance(request, dict):
                    continue
                module_id = request.get("moduleId") or request.get("module_id")
                if isinstance(module_id, str) and module_id.strip():
                    module_ids.add(module_id.strip())
                submodule_id = request.get("submoduleId") or request.get("submodule_id")
                if isinstance(submodule_id, str) and submodule_id.strip():
                    has_submodule = True

        view = value.get("view")
        if isinstance(view, BaseModel):
            view = view.model_dump(exclude_none=True)
        if isinstance(view, dict):
            raw_view_type = view.get("type")
            if isinstance(raw_view_type, str) and raw_view_type.strip():
                view_type = raw_view_type.strip().lower()

    parsed_candidate = candidate
    if isinstance(candidate, str):
        try:
            parsed_candidate = json.loads(candidate)
        except Exception:
            parsed_candidate = candidate
    visit(parsed_candidate)
    return module_ids, has_submodule, view_type


def _summarize_current_dsls(current_dsls: Iterable[Any]) -> str:
    summaries: List[str] = []
    for item in current_dsls or []:
        if isinstance(item, BaseModel):
            item = item.model_dump(exclude_none=True)
        elif not isinstance(item, dict):
            item = getattr(item, "__dict__", {})
        if not isinstance(item, dict):
            continue

        dsl = item.get("dsl")
        if isinstance(dsl, BaseModel):
            dsl = dsl.model_dump(exclude_none=True)
        if not isinstance(dsl, dict):
            dsl = item

        requests_summary: List[Dict[str, Any]] = []
        for request in dsl.get("requests") or []:
            if isinstance(request, BaseModel):
                request = request.model_dump(exclude_none=True)
            if not isinstance(request, dict):
                continue
            req_summary: Dict[str, Any] = {}
            for key in ("id", "moduleId", "submoduleId", "sqlCode"):
                value = request.get(key)
                if value not in (None, ""):
                    req_summary[key] = value
            if req_summary:
                requests_summary.append(req_summary)

        view = dsl.get("view")
        if isinstance(view, BaseModel):
            view = view.model_dump(exclude_none=True)
        view_type = view.get("type") if isinstance(view, dict) else None

        summary = {
            "blockId": item.get("blockId") or item.get("block_id") or item.get("id"),
            "title": item.get("title"),
            "dslId": dsl.get("id"),
            "action": dsl.get("action"),
            "viewType": view_type,
            "requests": requests_summary,
        }
        summaries.append(json.dumps({k: v for k, v in summary.items() if v not in (None, "", [])}, ensure_ascii=False))

    if not summaries:
        return ""
    return "\n".join([
        "<current_dsls>",
        "当前已有报表块摘要（修复阶段不重复注入完整 transform/view）：",
        *[f"- {summary}" for summary in summaries],
        "</current_dsls>",
    ])


def _resource_priority(
    resource_path: str,
    module_ids: set[str],
    has_submodule: bool,
    view_type: Optional[str],
) -> int:
    path = str(resource_path or "")
    if any(
        path == f"catalog/profiles/{module_id}.json"
        or path == f"catalog/modules/{module_id}.md"
        for module_id in module_ids
    ):
        return 0
    if path == "catalog/execution-contract.json":
        return 1
    if path == "skill/references/merge-guidance-v2.md" and len(module_ids) > 1:
        return 1
    if path == "catalog/submodules.json" and has_submodule:
        return 1
    if path == "skill/references/dsl-spec.md":
        return 2
    if view_type == "table" and path == "skill/references/dsl-table.md":
        return 2
    if view_type == "echarts" and path == "skill/references/dsl-echarts.md":
        return 2
    if path.startswith("catalog/profiles/"):
        return 3
    if path.startswith("catalog/modules/"):
        return 4
    if path.startswith("skill/references/"):
        return 5
    if path == "catalog/profile-index.json":
        return 7
    if path == "catalog/index.md":
        return 8
    if path == "catalog/metrics.md":
        return 9
    return 6


def _iter_resource_items(resource_context: Any) -> List[Tuple[str, str]]:
    if not resource_context:
        return []
    if isinstance(resource_context, dict) or hasattr(resource_context, "items"):
        raw_items = resource_context.items()
    else:
        raw_items = resource_context
    items: List[Tuple[str, str]] = []
    for res_path, res_text in raw_items:
        if res_path is None or res_text is None:
            continue
        items.append((str(res_path), str(res_text)))
    return items


def _format_resource_context(
    items: List[Tuple[str, str]],
    max_chars: Optional[int] = None,
    invalid_candidate: Any = None,
) -> str:
    if not items or max_chars == 0:
        return ""

    if max_chars is None:
        selected = items
    else:
        module_ids, has_submodule, view_type = _candidate_request_metadata(invalid_candidate)
        selected = sorted(
            enumerate(items),
            key=lambda pair: (
                _resource_priority(pair[1][0], module_ids, has_submodule, view_type),
                pair[0],
            ),
        )
        selected = [item for _, item in selected]

    prefix = "<read_resource_context>\n"
    suffix = "\n</read_resource_context>"
    if max_chars is not None and max_chars <= len(prefix) + len(suffix) + 16:
        return ""

    chunks: List[str] = []
    used = len(prefix) + len(suffix)
    omitted = 0

    for res_path, res_text in selected:
        chunk = f"--- Resource: {res_path} ---\n{res_text}"
        addition = len(chunk) + (1 if chunks else 0)
        if max_chars is None or used + addition <= max_chars:
            chunks.append(chunk)
            used += addition
            continue

        omitted += 1

    if max_chars is not None and omitted:
        marker = f"[省略 {omitted} 个低优先级资源以满足修复提示长度预算]"
        addition = len(marker) + (1 if chunks else 0)
        if used + addition <= max_chars:
            chunks.append(marker)
            used += addition

    if not chunks:
        return ""
    return prefix + "\n".join(chunks) + suffix


def build_repair_prompt(
    options: Union[RepairPromptOptions, Dict[str, Any], Any]
) -> PromptOutput:
    # 1. Resolve options fields
    if isinstance(options, dict):
        invalid_candidate = options.get("invalidCandidate") if "invalidCandidate" in options else options.get("invalid_candidate")
        validation_errors = options.get("validationErrors") if "validationErrors" in options else options.get("validation_errors", [])
        input_obj = options.get("input")
        resource_context = options.get("resourceContext") if "resourceContext" in options else options.get("resource_context")
        skill_md = options.get("skillMd") if "skillMd" in options else options.get("skill_md")
        if skill_md is None:
            skill_md = ""
        max_prompt_chars = options.get("maxPromptChars") if "maxPromptChars" in options else options.get("max_prompt_chars")
    else:
        invalid_candidate = getattr(options, "invalidCandidate", None)
        if invalid_candidate is None:
            invalid_candidate = getattr(options, "invalid_candidate", None)
        validation_errors = getattr(options, "validationErrors", None)
        if validation_errors is None:
            validation_errors = getattr(options, "validation_errors", None)
        if validation_errors is None:
            validation_errors = []

        input_obj = getattr(options, "input", None)

        resource_context = getattr(options, "resourceContext", None)
        if resource_context is None:
            resource_context = getattr(options, "resource_context", None)

        skill_md = getattr(options, "skillMd", None)
        if skill_md is None:
            skill_md = getattr(options, "skill_md", None)
        if skill_md is None:
            skill_md = ""

        max_prompt_chars = getattr(options, "maxPromptChars", None)
        if max_prompt_chars is None:
            max_prompt_chars = getattr(options, "max_prompt_chars", None)

    max_chars = (
        max_prompt_chars
        if max_prompt_chars is not None
        else int(os.getenv("MAX_PROMPT_CHARS", "120000"))
    )

    # 2. System prompt
    system_prompt = _build_repair_system_prompt(skill_md, include_full_skill=True)

    # 3. Format validationErrors
    issues_formatted = []
    for e in validation_errors:
        if isinstance(e, BaseModel):
            code = e.code
            path = e.path
            message = e.message
        elif isinstance(e, dict):
            code = e.get("code", "")
            path = e.get("path", "")
            message = e.get("message", "")
        else:
            code = getattr(e, "code", "")
            path = getattr(e, "path", "")
            message = getattr(e, "message", "")
        issues_formatted.append(f"- Code: {code} | Path: {path} | Message: {message}")
    issues_list = "\n".join(issues_formatted)

    # 4. Parse globalQueryParameters and nonemptyFlags
    if isinstance(input_obj, dict):
        raw_params = input_obj.get("globalQueryParameters") if "globalQueryParameters" in input_obj else input_obj.get("global_query_parameters", {})
        nonempty_flags_from_input = input_obj.get("nonemptyFlags") if "nonemptyFlags" in input_obj else input_obj.get("nonempty_flags", {})
        current_dsls = input_obj.get("currentDsls") if "currentDsls" in input_obj else input_obj.get("current_dsls", [])
        selected_block_id = input_obj.get("selectedBlockId") if "selectedBlockId" in input_obj else input_obj.get("selected_block_id")
        user_message = input_obj.get("userMessage") if "userMessage" in input_obj else input_obj.get("user_message", "")
    else:
        raw_params = getattr(input_obj, "globalQueryParameters", None)
        if raw_params is None:
            raw_params = getattr(input_obj, "global_query_parameters", {})
        nonempty_flags_from_input = getattr(input_obj, "nonemptyFlags", None)
        if nonempty_flags_from_input is None:
            nonempty_flags_from_input = getattr(input_obj, "nonempty_flags", {})
        current_dsls = getattr(input_obj, "currentDsls", None)
        if current_dsls is None:
            current_dsls = getattr(input_obj, "current_dsls", [])
        selected_block_id = getattr(input_obj, "selectedBlockId", None)
        if selected_block_id is None:
            selected_block_id = getattr(input_obj, "selected_block_id", None)
        user_message = getattr(input_obj, "userMessage", None)
        if user_message is None:
            user_message = getattr(input_obj, "user_message", "")

    if isinstance(raw_params, BaseModel):
        raw_params = raw_params.model_dump()
    if isinstance(nonempty_flags_from_input, BaseModel):
        nonempty_flags_from_input = nonempty_flags_from_input.model_dump()

    param_names: List[str] = []
    nonempty_flags: Dict[str, bool] = dict(nonempty_flags_from_input) if isinstance(nonempty_flags_from_input, dict) else {}

    if isinstance(raw_params, dict):
        names_val = raw_params.get("names")
        if isinstance(names_val, list):
            param_names = names_val
            flags_val = raw_params.get("nonemptyFlags") if "nonemptyFlags" in raw_params else raw_params.get("nonempty_flags")
            if isinstance(flags_val, dict):
                nonempty_flags = flags_val
        else:
            param_names = [k for k in raw_params.keys() if k not in ("names", "nonemptyFlags", "nonempty_flags")]
    elif hasattr(raw_params, "names") and isinstance(getattr(raw_params, "names"), list):
        param_names = getattr(raw_params, "names")
        flags_val = getattr(raw_params, "nonemptyFlags", None)
        if flags_val is None:
            flags_val = getattr(raw_params, "nonempty_flags", None)
        if isinstance(flags_val, dict):
            nonempty_flags = flags_val

    param_flags_text = ", ".join(
        f"{name} (nonempty: {'true' if bool(nonempty_flags.get(name)) else 'false'})"
        for name in param_names
    )

    # 5. Compact currentDslsSection. Repair already receives the full invalid
    # candidate, so existing blocks are only needed for identity/target context.
    current_dsls_section = _summarize_current_dsls(current_dsls)

    # 6. Format resourceContextSection
    resource_items = _iter_resource_items(resource_context)
    resource_context_section = _format_resource_context(resource_items)

    # 7. Invalid candidate formatting
    if isinstance(invalid_candidate, BaseModel):
        cand_val = invalid_candidate.model_dump()
    else:
        cand_val = invalid_candidate
    invalid_candidate_json = json.dumps(cand_val, indent=2, ensure_ascii=False)

    selected_block_text = selected_block_id if selected_block_id else "无"

    # 8. User prompt lines assembly
    def build_user_prompt(resource_section: str) -> str:
        user_prompt_lines = [
            resource_section,
            current_dsls_section,
            f"<global_query_parameters>\n界面全局查询条件字段: {param_flags_text or '无'}\n</global_query_parameters>",
            "",
            "<invalid_candidate>",
            invalid_candidate_json,
            "</invalid_candidate>",
            "",
            "<validation_errors>",
            issues_list,
            "</validation_errors>",
            "",
            "<user_request>",
            f"selectedBlockId: {selected_block_text}",
            f"用户输入: {user_message}",
            "</user_request>",
        ]
        return "\n".join([line for line in user_prompt_lines if line])

    user_prompt = build_user_prompt(resource_context_section)

    # 9. Total length check with deterministic repair compaction. Initial model
    # resource reads share the same MAX_PROMPT_CHARS budget, but repair also adds
    # the invalid candidate, validation errors and page state. Reusing every
    # resource verbatim can therefore overflow even when the initial turn fit.
    total_len = len(system_prompt) + len(user_prompt)
    if total_len > max_chars:
        system_prompt = _build_repair_system_prompt("", include_full_skill=False)
        core_user_prompt = build_user_prompt("")
        core_len = len(system_prompt) + len(core_user_prompt)
        if core_len > max_chars:
            raise ValueError(
                f"PROMPT_CONTEXT_TOO_LARGE: Repair core content length ({core_len}) exceeds limit ({max_chars})"
            )

        # Leave a small safety margin for section delimiters and future prompt
        # wording changes, then keep whole resources by semantic priority.
        safety_margin = min(1024, max(128, max_chars // 100))
        resource_budget = max(0, max_chars - core_len - safety_margin)
        compact_resource_section = _format_resource_context(
            resource_items,
            max_chars=resource_budget,
            invalid_candidate=invalid_candidate,
        )
        user_prompt = build_user_prompt(compact_resource_section)
        total_len = len(system_prompt) + len(user_prompt)

    if total_len > max_chars:
        raise ValueError(
            f"PROMPT_CONTEXT_TOO_LARGE: Repair prompt content length ({total_len}) exceeds limit ({max_chars})"
        )

    return PromptOutput(systemPrompt=system_prompt, userPrompt=user_prompt)


buildRepairPrompt = build_repair_prompt
