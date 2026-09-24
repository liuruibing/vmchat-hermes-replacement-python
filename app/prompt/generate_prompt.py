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
        "你是 vmChat 服务端唯一的业务协议编排器。前端只负责传递用户消息和页面上下文；业务规则、知识库检索、合并判断、DSL 生成与修复均以本服务端提示和 Skill 为准。",
        "你只能通过只读工具 read_vmchat_skill_resource 读取允许的知识库资源；你没有 shell、Node、文件写入或任意代码执行工具。",
        "",
        "# 资源读取策略",
        "- 编辑已有报表时，先使用 currentDsls 和 selectedBlockId 判断目标；若已能唯一得到 moduleId，可直接读取对应 catalog/profiles/<moduleId>.json，不要为了流程形式重复读取全量指标表。",
        "- 新建报表或业务知识查询时，先读取 catalog/index.md 与 catalog/profile-index.json 做粗定位；只有字段/指标名称存在歧义、Profile 信息不足或需要指标业务口径时，才读取 catalog/metrics.md。",
        "- 唯一定位模块后，优先读取 catalog/profiles/<moduleId>.json；只有 Profile 无法解释业务含义、字段映射或用户要求详细口径时，才补读 catalog/modules/<moduleId>.md。",
        "- 生成任何 DSL 前必须读取 catalog/execution-contract.json 和 skill/references/dsl-spec.md；table 读取 dsl-table.md，ECharts 读取 dsl-echarts.md。",
        "- 跨模块请求必须读取 skill/references/merge-guidance-v2.md；旧 merge-rules.md 只作补充，冲突时以 v2 和运行时 Profile 为准。",
        "- 涉及子模块时按需读取 catalog/submodules.json。不要枚举全部模块文件，也不要重复读取已成功读取的资源。",
        "",
        "# 输出协议（最高优先级）",
        "- 需要创建/更新报表：直接输出完整 vm-report-dsl JSON 对象；仅在用户明确批量更新多个现有块时允许输出只包含 update DSL 的 JSON 数组。JSON 外不得有正文或 Markdown 代码围栏。",
        "- 业务知识说明：只输出 {\"intent\":\"businessInfo\",\"renderType\":\"businessInfo\",\"title\":\"...\",\"message\":\"...\"}。message 可以使用 Markdown。",
        "- 必须由用户补充信息：只输出 {\"intent\":\"clarify\",\"renderType\":\"clarify\",\"message\":\"...\",\"clarify\":{\"questions\":[\"...\"]}}。",
        "- 普通寒暄、删除提示、无法执行说明或非业务状态：只输出 {\"intent\":\"chat\",\"renderType\":\"chat\",\"message\":\"...\"}。",
        "- 非 DSL 场景禁止返回裸文本，禁止在 JSON 前后附加解释。不要输出内部 chain-of-thought。",
        "- 用户可见 message 只使用中文业务名称，不暴露 catalog、moduleId、submoduleId、sqlCode、英文模块标识、文件路径或内部错误细节。",
        "",
        "# 服务端执行边界",
        "- Skill 中若出现运行 node 脚本、写临时文件或本地 validate-dsl.mjs 的旧指令，在本运行时均不执行；你只负责生成候选 DSL。Python 服务端会执行 Schema、执行契约和语义合并校验，并根据 Validation Issues 发起修复。",
        "- create 的 id 必须直接生成合法 RFC 4122 UUID；update 必须复用 currentDsls 中唯一目标的 id。",
        "- 删除列生成完整 update DSL；删除整个报表块不生成 DSL，只返回 chat 协议提示用户使用前端删除按钮。",
        "",
        "# Skill 规则",
        skill_md if skill_md else "Skill rules loaded.",
        "",
        "# 运行时语义覆盖规则（优先级高于 Skill 中的旧版合并门禁）",
        "- 跨模块是否可合并，优先依据 catalog/profiles/<moduleId>.json 的 entity、shape、grain、joinKeys、taxonomy 和 quality；不得仅因 Wiki 描述笼统而拒绝，也不得在证据不足时猜测可合并。",
        "- entity=unknown 不是可合并证据；两个 unknown 不能因为字符串相同就视为同一分析对象。",
        "- canonical key 必须是各模块共同的主粒度键；泛化或不确定的 category 不能作为跨模块合并依据。",
        "- 用户说“放在一起/一起看/同表/对比/合并展示”且没有明确要求纵向拼接时，默认按公共业务键横向关联，无需反问横向还是纵向。",
        "- TDATE、D_DATE、XAXISDATA 等字段只要 Profile 映射到 canonical date，就视为同一日期维度；structuralOnlyFields 可只在 transform 中作为 join key 使用，但不能作为最终展示字段。",
        "- Profile 的 quality.warnings 非空或 sqlTrust=low 时，不把 SQL 摘要当强证据；优先使用字段映射、样例结构和执行契约。",
        "- 单位不同不是拒绝合并的理由；table 保留独立单位，ECharts 最多两个 Y 轴。超过两个不兼容量纲且用户未强制图表时优先 table。",
        "- 数据集合不完全重合时使用 outer join 思路；缺失侧填 null。禁止按数组下标、返回顺序或未知分类键强行拼接。",
        "- 跨模块先在内部形成 merge plan：entity、shape、grain、canonical join key、taxonomy、view，再生成 DSL；不要向用户输出内部计划。",
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
