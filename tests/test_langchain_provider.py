import pytest
from langchain_core.messages import AIMessageChunk
from langchain_deepseek import ChatDeepSeek

from app.provider.fixed_provider import ModelSkillRunInput
from app.provider.langchain_provider import LangChainVmChatProvider


def test_build_model_uses_deepseek_provider():
    provider = LangChainVmChatProvider(
        model_name="deepseek-v4-flash",
        base_url="https://api.deepseek.com/v1",
        api_key="test-key",
    )

    model = provider.build_model()

    assert isinstance(model, ChatDeepSeek)
    assert model.model_name == "deepseek-v4-flash"
    assert str(model.api_base) == "https://api.deepseek.com/v1"


def test_build_model_accepts_stage_request_timeout():
    provider = LangChainVmChatProvider(model_name="deepseek-v4-flash", api_key="test-key")
    model = provider.build_model(timeout_seconds=240)
    assert model.request_timeout == 240


@pytest.mark.anyio
async def test_run_skill_uses_the_stage_timeout(monkeypatch):
    class Model:
        def bind_tools(self, _tools):
            return self

        async def astream(self, _messages):
            yield AIMessageChunk(content='{"complete":true}')

    timeouts = []

    def build_model(*, timeout_seconds):
        timeouts.append(timeout_seconds)
        return Model()

    provider = LangChainVmChatProvider(model_name="deepseek-v4-flash")
    monkeypatch.setattr(provider, "build_model", build_model)
    chunks = [chunk async for chunk in provider.run_skill(ModelSkillRunInput(
        system_prompt="system", user_prompt="user", read_resource=lambda _path: "",
        timeout_seconds=240,
    ))]
    assert timeouts == [240]
    assert [chunk.contentDelta for chunk in chunks if chunk.contentDelta] == ['{"complete":true}']


@pytest.mark.anyio
async def test_run_skill_emits_final_content_once(monkeypatch):
    class BoundModel:
        async def astream(self, _messages):
            yield AIMessageChunk(
                content="第一段",
                additional_kwargs={"reasoning_content": "正在检索"},
            )
            yield AIMessageChunk(content="第二段")

    class Model:
        def bind_tools(self, _tools):
            return BoundModel()

    provider = LangChainVmChatProvider(model_name="deepseek-v4-flash")
    monkeypatch.setattr(provider, "build_model", lambda: Model())

    chunks = [
        chunk
        async for chunk in provider.run_skill(
            ModelSkillRunInput(
                system_prompt="system",
                user_prompt="user",
                read_resource=lambda _path: "",
            )
        )
    ]

    assert [chunk.reasoningDelta for chunk in chunks if chunk.reasoningDelta] == ["正在检索"]
    assert [chunk.contentDelta for chunk in chunks if chunk.contentDelta] == ["第一段第二段"]
