import os
import json
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict

from app.compatibility.hermes_request import VmChatInput


class PromptOutput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    systemPrompt: str = Field(..., alias="system_prompt")
    userPrompt: str = Field(..., alias="user_prompt")

    @property
    def system_prompt(self) -> str:
        return self.systemPrompt

    @property
    def user_prompt(self) -> str:
        return self.userPrompt


class GeneratePromptOptions(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    input: Union[VmChatInput, Dict[str, Any], Any]
    skillMd: str = Field(default="", alias="skill_md")
    maxPromptChars: Optional[int] = Field(default=None, alias="max_prompt_chars")

    @property
    def skill_md(self) -> str:
        return self.skillMd

    @property
    def max_prompt_chars(self) -> Optional[int]:
        return self.maxPromptChars


def build_generate_prompt(
    options: Union[GeneratePromptOptions, Dict[str, Any], Any]
) -> PromptOutput:
    # 1. Resolve max_chars and skill_md
    max_prompt_chars = None
    if isinstance(options, dict):
        max_prompt_chars = options.get("maxPromptChars") if "maxPromptChars" in options else options.get("max_prompt_chars")
        skill_md = options.get("skillMd") if "skillMd" in options else options.get("skill_md")
        if skill_md is None:
            skill_md = ""
        input_obj = options.get("input")
    else:
        max_prompt_chars = getattr(options, "maxPromptChars", None)
        if max_prompt_chars is None:
            max_prompt_chars = getattr(options, "max_prompt_chars", None)
        skill_md = getattr(options, "skillMd", None)
        if skill_md is None:
            skill_md = getattr(options, "skill_md", None)
        if skill_md is None:
            skill_md = ""
        input_obj = getattr(options, "input", None)

    max_chars = (
        max_prompt_chars
        if max_prompt_chars is not None
        else int(os.getenv("MAX_PROMPT_CHARS", "120000"))
    )

    # 2. Build systemPrompt
    system_prompt = "\n".join([
        "你是 vmChat 的 Hermes Skill 协议助手。",
        "你必须遵循下方嵌入的完整 Hermes Skill 规则与指引，自主完成决策与资源查找。",
        "你在本服务端环境中可以通过只读工具 `read_vmchat_skill_resource` 读取关联资源文件。资源目录规范与路径如下：",
        "1. `catalog/index.md`：查看全部模块目录列表与场景推荐；",
        "2. `catalog/metrics.md`：查看全量指标、维度与对应的模块映射；",
        "3. `catalog/execution-contract.json`：查看模块底层执行参数与 sqlCode 映射；",
        "4. `catalog/submodules.json`：查看带有子模块定义及父模块关联的 JSON 结构；",
        "5. `catalog/profile-index.json`：运行时自动生成的模块结构语义索引，用于快速判断 shape、entity、grain、joinKeys、taxonomy；",
        "6. `catalog/profiles/<moduleId>.json`：模块结构化语义卡，由模块字段映射、样例 JSON 和可选 SQL 证据自动提取；",
        "7. `catalog/modules/<moduleId>.md`：补充业务叙述的后备资源；profile 已包含字段映射、样例结构与渲染候选，正常 DSL 生成无需重复读取模块 MD；",
        "8. `skill/references/` 下规范文件：`dsl-spec.md`、`dsl-table.md`、`dsl-echarts.md`、`merge-rules.md`，以及跨模块时必须读取的 `merge-guidance-v2.md`。",
        "",
        "在处理用户请求时，你必须遵守以下流程：",
        "- 必须先使用 `read_vmchat_skill_resource` 工具读取 `catalog/index.md`、`catalog/metrics.md` 与 `catalog/profile-index.json`；",
        "- 唯一定位模块后，必须读取对应 `catalog/profiles/<moduleId>.json`；只有 profile 无法唯一解释业务含义或用户正在询问详细业务知识时，才补读 `catalog/modules/<moduleId>.md`；",
        "- 涉及跨模块合并时必须读取 `skill/references/merge-guidance-v2.md`；旧版 `merge-rules.md` 仍可读取，但冲突时以 v2 为准；",
        "- 生成任何 DSL 前必须读取 `catalog/execution-contract.json`；涉及子模块、DSL 或视图配置时按需读取相关 reference 或 submodules.json；",
        "- 根据 Skill 自主判断问答、新建（create）、更新（update）、批量更新（batch update）、合并、子模块、删列、删块或澄清；",
        "- 删列时生成 update DSL 并在 columns 中移除对应列；删除整块时按 Skill 返回自然的中文说明，不得生成空 DSL；",
        "- 需生成 DSL 时，直接返回合法的 JSON 对象或数组（不得加 markdown 代码围栏）；无需生成 DSL 时返回简洁自然的中文说明。",
        "",
        "# Skill 规则",
        skill_md if skill_md else "Skill rules loaded.",
        "",
        "# 运行时语义覆盖规则（优先级高于上方旧版 Skill 合并门禁）",
        "- 跨模块是否可合并，优先依据 catalog/profiles/<moduleId>.json 的结构化事实，不得仅因 Wiki 业务说明笼统而拒绝。",
        "- 上方旧版 Skill 中“定位模块后必须读取模块 MD”的要求被本运行时规则覆盖：profile 已包含字段映射、样例结构、默认视图与 SQL 摘要，除非语义仍不明确，否则不要重复读取模块 MD，以控制 token 和工具调用次数。",
        "- 用户说“放在一起/一起看/同表/对比/合并展示”时，默认按公共业务键做横向关联；除非用户明确要求纵向拼接，否则不要反问横向还是纵向。",
        "- TDATE、D_DATE、XAXISDATA 等字段只要 profile 映射到同一个 canonical key=date，就视为同一日期维度。",
        "- profile.structuralOnlyFields 允许仅在 transform 中作为 join key 使用，但不能作为最终展示字段。",
        "- profile.quality.warnings 非空或 sqlTrust=low 时，不得把 SQL 摘要当作强证据；优先使用字段映射和样例 JSON 的稳定结构，并避免基于可疑 SQL 推断新的业务口径。",
        "- 单位不同不是拒绝合并的理由；table 保留独立单位，ECharts 使用最多两个 Y 轴。超过两个不兼容量纲且用户未强制图表时优先 table。",
        "- 跨模块时先在内部形成 merge plan：entity、shape、canonical join key、taxonomy、view，再生成 DSL；不要输出该内部计划。",
    ])

    # 3. Parse globalQueryParameters and nonemptyFlags
    if isinstance(input_obj, dict):
        raw_params = input_obj.get("globalQueryParameters") if "globalQueryParameters" in input_obj else input_obj.get("global_query_parameters", {})
        nonempty_flags_from_input = input_obj.get("nonemptyFlags") if "nonemptyFlags" in input_obj else input_obj.get("nonempty_flags", {})
        current_dsls = input_obj.get("currentDsls") if "currentDsls" in input_obj else input_obj.get("current_dsls", [])
        selected_block_id = input_obj.get("selectedBlockId") if "selectedBlockId" in input_obj else input_obj.get("selected_block_id")
        user_message = input_obj.get("userMessage") if "userMessage" in input_obj else input_obj.get("user_message", "")
        history_messages = input_obj.get("historyMessages") if "historyMessages" in input_obj else input_obj.get("history_messages", [])
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
        history_messages = getattr(input_obj, "historyMessages", None)
        if history_messages is None:
            history_messages = getattr(input_obj, "history_messages", [])

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

    # 4. Format currentDslsSection
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
            "当前已有报表块定义（全局上下文）：",
            *dsl_blocks,
            "</current_dsls>",
        ])
    else:
        current_dsls_section = ""

    # 5. Format userRequestBlock
    selected_block_text = selected_block_id if selected_block_id else "无"
    user_request_block = "\n".join([
        "<user_request>",
        f"selectedBlockId: {selected_block_text}",
        f"用户输入: {user_message}",
        "</user_request>",
    ])

    # 6. Format baseUserPromptLines
    base_user_prompt_lines = [line for line in [
        current_dsls_section,
        f"<global_query_parameters>\n界面全局查询条件字段: {param_flags_text or '无'}\n</global_query_parameters>",
        user_request_block,
    ] if line]

    protected_content = "\n".join([system_prompt, *base_user_prompt_lines])
    if len(protected_content) > max_chars:
        raise ValueError(
            f"PROMPT_CONTEXT_TOO_LARGE: Protected prompt content length ({len(protected_content)}) exceeds limit ({max_chars})"
        )

    # 7. History messages allocation: max 10, truncate oldest first if needed
    raw_history = history_messages[-10:] if history_messages else []
    included_history_count = len(raw_history)

    while included_history_count >= 0:
        history_slice = raw_history[len(raw_history) - included_history_count:] if included_history_count > 0 else []

        if history_slice:
            history_lines = ["<chat_history>"]
            for h in history_slice:
                if isinstance(h, dict):
                    role = h.get("role", "")
                    content = h.get("content", "")
                elif isinstance(h, BaseModel):
                    role = h.role
                    content = h.content
                else:
                    role = getattr(h, "role", "")
                    content = getattr(h, "content", "")
                history_lines.append(f"{role}: {content}")
            history_lines.append("</chat_history>")
            history_text = "\n".join(history_lines)
        else:
            history_text = ""

        candidate_parts = [p for p in [history_text, *base_user_prompt_lines] if p]
        candidate_prompt = "\n\n".join(candidate_parts)

        if len(system_prompt) + len(candidate_prompt) <= max_chars:
            return PromptOutput(systemPrompt=system_prompt, userPrompt=candidate_prompt)

        included_history_count -= 1

    raise ValueError(
        f"PROMPT_CONTEXT_TOO_LARGE: Unable to fit user prompt into context budget of {max_chars} chars"
    )


buildGeneratePrompt = build_generate_prompt
