import json
import os
import re
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field

from app.compatibility.hermes_request import VmChatInput


class ModelGenerateInput(BaseModel):
    systemPrompt: str = Field(alias="system_prompt")
    userPrompt: str = Field(alias="user_prompt")
    signal: Optional[Any] = None
    purpose: Optional[Literal["generate", "repair"]] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @property
    def system_prompt(self) -> str:
        return self.systemPrompt

    @property
    def user_prompt(self) -> str:
        return self.userPrompt

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class ModelSkillRunInput(BaseModel):
    systemPrompt: str = Field(alias="system_prompt")
    userPrompt: str = Field(alias="user_prompt")
    readResource: Callable[[str], str] = Field(alias="read_resource")
    signal: Optional[Any] = None

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @property
    def system_prompt(self) -> str:
        return self.systemPrompt

    @property
    def user_prompt(self) -> str:
        return self.userPrompt

    @property
    def read_resource(self) -> Callable[[str], str]:
        return self.readResource

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class ModelResultDsl(BaseModel):
    type: Literal["dsl"] = "dsl"
    dsl: Union[Dict[str, Any], List[Dict[str, Any]]]

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class ModelResultText(BaseModel):
    type: Literal["text"] = "text"
    category: Literal["clarify", "reject"]
    text: str

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


VmChatModelResult = Union[ModelResultDsl, ModelResultText, Dict[str, Any]]


class ModelUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class ModelGenerateOutput(BaseModel):
    result: VmChatModelResult
    usage: Optional[Union[ModelUsage, Dict[str, Any]]] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


class ModelStreamChunk(BaseModel):
    reasoningDelta: Optional[str] = Field(default=None, alias="reasoning_delta")
    contentDelta: Optional[str] = Field(default=None, alias="content_delta")
    usage: Optional[Dict[str, Any]] = None
    done: Optional[bool] = None

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    @property
    def reasoning_delta(self) -> Optional[str]:
        return self.reasoningDelta

    @property
    def content_delta(self) -> Optional[str]:
        return self.contentDelta

    def __getitem__(self, item: str) -> Any:
        return getattr(self, item)

    def get(self, item: str, default: Any = None) -> Any:
        return getattr(self, item, default)


def is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    if getattr(signal, "aborted", False):
        return True
    if hasattr(signal, "is_set") and callable(signal.is_set):
        return signal.is_set()
    return False


class VmChatModelProvider(ABC):
    @abstractmethod
    async def generate(self, input: ModelGenerateInput) -> ModelGenerateOutput:
        pass

    @abstractmethod
    async def stream(self, input: ModelGenerateInput):
        pass

    @abstractmethod
    async def run_skill(self, input: ModelSkillRunInput):
        pass

    async def runSkill(self, input: ModelSkillRunInput):
        async for chunk in self.run_skill(input):
            yield chunk


class FixedVmChatProvider(VmChatModelProvider):
    def __init__(self, fixture_path: Optional[str] = None):
        if os.getenv("NODE_ENV") == "production":
            raise RuntimeError("SECURITY_ERROR: FixedVmChatProvider is forbidden in production environment")
        self.fixture_path = fixture_path or os.getenv("FIXED_PROVIDER_FIXTURE") or ""
        self.fixturePath = self.fixture_path

    def build_inline_dsl(self, input: ModelGenerateInput) -> Dict[str, Any]:
        user_prompt = input.userPrompt
        user_msg_match = re.search(r"用户输入[：:]\s*([^\n]+)", user_prompt)
        user_msg_text = user_msg_match.group(1).strip() if user_msg_match else user_prompt

        is_update = "意图: update" in user_prompt or "意图: batch-update" in user_prompt
        is_batch = "意图: batch-update" in user_prompt
        is_echarts = bool(re.search(r"(图|走势|分布|择时)", user_msg_text)) and not user_msg_text.endswith("表") and "表格" not in user_msg_text

        target_id_match = re.search(r"目标报表块 ID[：:]\s*([^\n]+)", user_prompt)
        raw_target_id = (
            target_id_match.group(1).split(",")[0].strip()
            if target_id_match and target_id_match.group(1) and target_id_match.group(1) != "无"
            else "block-001"
        )
        target_id = (
            raw_target_id
            if re.match(r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$", raw_target_id, re.IGNORECASE)
            else "3d1d1f05-7f55-46eb-8e5f-155018a7b97a"
        )

        mod_match = re.search(r"--- Module: .*?\((.*?)\) ---\s*sqlCode:\s*([^\n]+)", user_prompt)
        module_id = mod_match.group(1).strip() if mod_match and mod_match.group(1) else "stockExposureTiming"
        sql_code = mod_match.group(2).strip() if mod_match and mod_match.group(2) else "712b930b-87a5-4cba-8da0-3671d4c8dc54"

        single_dsl = {
            "action": "update" if is_update else "create",
            "id": target_id,
            "requests": [{"id": "req1", "moduleId": module_id, "sqlCode": sql_code}],
            "transform": {
                "language": "javascript",
                "function": "function transform(responses) { return [{ col1: responses.req1 }]; }",
            },
            "view": (
                {
                    "type": "echarts",
                    "title": "默认图",
                    "legend": {"show": True, "data": ["列1"]},
                    "dataset": {"source": "$transform", "dimensions": ["col1"]},
                    "series": [{"type": "line", "name": "列1", "encode": {"x": "col1", "y": "col1"}, "format": {"type": "raw"}}],
                    "xAxis": {"type": "category"},
                    "yAxis": [{"type": "value"}],
                }
                if is_echarts
                else {
                    "type": "table",
                    "title": "默认表",
                    "columns": [{"field": "col1", "label": "列1"}],
                }
            ),
        }

        return {"dsl": [single_dsl] if is_batch else single_dsl, "isBatch": is_batch}

    async def generate(self, input: ModelGenerateInput) -> ModelGenerateOutput:
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request was aborted")

        if not self.fixture_path:
            inline_res = self.build_inline_dsl(input)
            return ModelGenerateOutput(
                result={"type": "dsl", "dsl": inline_res["dsl"]},
                usage={"prompt_tokens": 100, "completion_tokens": 100, "total_tokens": 200},
            )

        abs_path = os.path.abspath(self.fixture_path)
        try:
            with open(abs_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            raise RuntimeError(f"MISSING_FIXTURE: Failed to read fixed provider fixture at {abs_path}")

        trimmed = content.strip()
        if trimmed.startswith("{") or trimmed.startswith("["):
            parsed = json.loads(trimmed)
            return ModelGenerateOutput(
                result={"type": "dsl", "dsl": parsed},
                usage={"prompt_tokens": 150, "completion_tokens": 150, "total_tokens": 300},
            )

        return ModelGenerateOutput(
            result={"type": "text", "category": "clarify", "text": trimmed},
            usage={"prompt_tokens": 50, "completion_tokens": 50, "total_tokens": 100},
        )

    async def stream(self, input: ModelGenerateInput):
        if is_aborted(input.signal):
            raise RuntimeError("ABORTED: Request was aborted")

        output = await self.generate(input)
        res_data = output.result if isinstance(output.result, dict) else output.result.model_dump()
        
        res_type = res_data.get("type")
        if res_type == "dsl":
            result_text = json.dumps(res_data.get("dsl"), ensure_ascii=False, indent=2)
        else:
            result_text = res_data.get("text", "")

        chunk_size = 20
        for i in range(0, len(result_text), chunk_size):
            if is_aborted(input.signal):
                raise RuntimeError("ABORTED: Request was aborted")
            yield ModelStreamChunk(contentDelta=result_text[i : i + chunk_size])

        usage = (
            output.usage if isinstance(output.usage, dict)
            else (output.usage.model_dump() if hasattr(output.usage, "model_dump") else {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})
        )
        yield ModelStreamChunk(
            usage=usage or {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
            done=True,
        )

    async def run_skill(self, input: ModelSkillRunInput):
        gen_input = ModelGenerateInput(
            systemPrompt=input.systemPrompt,
            userPrompt=input.userPrompt,
            signal=input.signal,
        )
        async for chunk in self.stream(gen_input):
            yield chunk
