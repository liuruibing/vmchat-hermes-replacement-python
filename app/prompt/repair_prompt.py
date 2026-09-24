import os
import json
from typing import Any, Dict, List, Optional, Union, Mapping
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
    system_prompt = "\n".join([
        "你是 VM Report DSL 修复专家。",
        "你生成的 DSL 尝试校验失败，必须根据下方提供的校验错误列表（Validation Issues）对原 DSL 进行针对性修补。",
        "你必须且只能输出修复后的合法 JSON 对象或 JSON 数组，不得输出任何 Markdown 代码围栏、自然语言解释或 Chain-of-Thought 思维链。",
        "本修复阶段没有 shell、Node、文件写入或脚本执行工具；Skill 中涉及 gen-uuid.js、validate-dsl.mjs 或临时文件的旧指令均不执行。Python 服务端会在你的修复结果返回后重新校验。",
        "修复时必须保持与原 ID 和已确认模块一致，优先严格按照 Validation Issues 修正字段、共同键、transform、视图、签名、缺失属性或语法限制；不得通过删除 request 或改成无关模块绕过语义校验。",
        "transform.function 必须按 request.id 从 responses 取数，例如 responses.req_averagePePb 或 responses['req_averagePePb']；禁止使用 responses[0]、responses[1] 等数组下标。",
        "view.type === 'echarts' 时，title、legend、dataset、xAxis/yAxis（Cartesian 时）和 series 必须为 view 的直接属性。禁止 view.echarts、view.options 或任何图表配置包装层。",
        "# Skill 规则",
        skill_md if skill_md else "Skill rules loaded.",
    ])

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

    # 5. Format currentDslsSection (Notice header: "当前已有报表块定义：")
    if current_dsls:
        dsl_blocks = []
        for d in current_dsls:
            if isinstance(d, BaseModel):
                d_dict = d.model_dump()
            elif isinstance(d, dict):
                d_dict = d
            else:
                d_dict = getattr(d, "__dict__", {})

            block_id = d_dict.get("blockId") or d_dict.get("block_id") or d_dict.get("id") or "Untitled"
            title = d_dict.get("title") or "Untitled"
            dsl_val = d_dict.get("dsl")
            if dsl_val is None:
                dsl_val = d_dict
            elif isinstance(dsl_val, BaseModel):
                dsl_val = dsl_val.model_dump()

            dsl_blocks.append(
                f"--- Block {block_id}: {title} ---\n"
                f"{json.dumps(dsl_val, indent=2, ensure_ascii=False)}"
            )
        current_dsls_section = "\n".join([
            "<current_dsls>",
            "当前已有报表块定义：",
            *dsl_blocks,
            "</current_dsls>",
        ])
    else:
        current_dsls_section = ""

    # 6. Format resourceContextSection
    resource_entries: List[str] = []
    if resource_context:
        if isinstance(resource_context, dict) or hasattr(resource_context, "items"):
            items = resource_context.items()
        else:
            items = resource_context
        for res_path, res_text in items:
            resource_entries.append(f"--- Resource: {res_path} ---\n{res_text}")

    if resource_entries:
        resource_context_section = "\n".join([
            "<read_resource_context>",
            *resource_entries,
            "</read_resource_context>",
        ])
    else:
        resource_context_section = ""

    # 7. Invalid candidate formatting
    if isinstance(invalid_candidate, BaseModel):
        cand_val = invalid_candidate.model_dump()
    else:
        cand_val = invalid_candidate
    invalid_candidate_json = json.dumps(cand_val, indent=2, ensure_ascii=False)

    selected_block_text = selected_block_id if selected_block_id else "无"

    # 8. User prompt lines assembly (.filter(Boolean))
    user_prompt_lines = [
        resource_context_section,
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

    user_prompt = "\n".join([line for line in user_prompt_lines if line])

    # 9. Total length check
    total_len = len(system_prompt) + len(user_prompt)
    if total_len > max_chars:
        raise ValueError(
            f"PROMPT_CONTEXT_TOO_LARGE: Repair prompt content length ({total_len}) exceeds limit ({max_chars})"
        )

    return PromptOutput(systemPrompt=system_prompt, userPrompt=user_prompt)


buildRepairPrompt = build_repair_prompt
