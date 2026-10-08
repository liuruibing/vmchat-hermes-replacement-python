import json

import pytest
from langchain_core.messages import AIMessageChunk

from app.provider.colab_provider import ColabVmChatProvider, TextToolModel
from app.provider.fixed_provider import ModelSkillRunInput


def test_colab_provider_can_be_selected_from_environment():
    from app.config import load_config

    assert load_config({'LLM_PROVIDER': 'colab'}).llm_provider == 'colab'


class TextOnlyModel:
    def __init__(self, replies):
        self.replies = iter(replies)
        self.requests = []

    async def astream(self, messages):
        self.requests.append(messages)
        assert all(isinstance(m, dict) and m['role'] != 'tool' for m in messages)
        assert all('tool_calls' not in m for m in messages)
        reply = next(self.replies)
        yield AIMessageChunk(content=reply[:12])
        yield AIMessageChunk(content=reply[12:])


@pytest.mark.asyncio
async def test_colab_skill_executes_resource_read_then_returns_model_answer():
    model = TextOnlyModel([
        json.dumps({'colab_tool_calls': [{'name': 'read_vmchat_skill_resource', 'arguments': {'path': 'catalog/test.md'}}]}),
        '资源已读取，股票净敞口为多头敞口减去空头敞口。',
    ])
    provider = ColabVmChatProvider()
    provider.build_model = lambda **kwargs: TextToolModel(model)
    reads = []

    def read(path):
        reads.append(path)
        return '股票净敞口为多头减空头。'

    chunks = [c async for c in provider.run_skill(ModelSkillRunInput(
        systemPrompt='依据资源回答', userPrompt='解释股票净敞口', read_resource=read,
    ))]
    assert reads == ['catalog/test.md']
    assert '资源已读取' in ''.join(c.contentDelta or '' for c in chunks)
    assert len(model.requests) == 2
    assert any('股票净敞口为多头减空头' in m['content'] for m in model.requests[1])


@pytest.mark.asyncio
@pytest.mark.parametrize('calls', [
    [{'name': 'shell', 'arguments': {'command': 'whoami'}}],
    [{'name': 'read_vmchat_skill_resource', 'arguments': 'bad'}],
    [],
])
async def test_colab_rejects_invalid_text_tool_requests(calls):
    model = TextOnlyModel([json.dumps({'colab_tool_calls': calls})])
    from langchain_core.tools import tool

    @tool
    def read_vmchat_skill_resource(path: str) -> str:
        """Read an allowed resource."""
        return path

    bound = TextToolModel(model).bind_tools([read_vmchat_skill_resource])
    with pytest.raises(RuntimeError, match='COLAB_TOOL_REQUEST_INVALID'):
        _ = [c async for c in bound.astream([{'role': 'user', 'content': 'test'}])]


@pytest.mark.asyncio
async def test_colab_preserves_final_dsl_json_without_treating_it_as_a_tool():
    output = json.dumps({'action': 'create', 'requests': [], 'view': {'type': 'line'}})
    model = TextOnlyModel([output])
    bound = TextToolModel(model).bind_tools([])
    chunks = [c async for c in bound.astream([{'role': 'user', 'content': 'test'}])]
    assert ''.join(c.content for c in chunks) == output
    assert not any(c.tool_calls for c in chunks)


def test_colab_reserves_bounded_output_tokens(monkeypatch):
    monkeypatch.delenv('COLAB_MAX_OUTPUT_TOKENS', raising=False)
    provider = ColabVmChatProvider(model_name='google/gemini-3.5-flash', api_key='test')
    model = provider.build_model(timeout_seconds=240).model
    assert model.max_tokens == 16384
    assert model.request_timeout == 240
    monkeypatch.setenv('COLAB_MAX_OUTPUT_TOKENS', '8192')
    assert provider.build_model().model.max_tokens == 8192
