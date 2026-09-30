import json
from types import SimpleNamespace

import httpx
import pytest

from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline


@pytest.mark.anyio
async def test_incomplete_model_stream_retries_without_merging_partial_json(monkeypatch):
    import app.mandate_risk_v2.pipeline as module
    async def no_delay(_seconds):
        pass
    monkeypatch.setattr(module.asyncio, 'sleep', no_delay)
    calls = []
    class Provider:
        async def run_skill(self, run_input):
            calls.append(run_input)
            if len(calls) == 1:
                yield SimpleNamespace(contentDelta='{"truncated":', usage=None)
                raise httpx.RemoteProtocolError('peer closed connection without sending complete message body')
            yield SimpleNamespace(contentDelta=json.dumps({'complete': True}), usage={'total_tokens': 2})
    payload, usage = await RequirementExtractionPipeline()._call_model(
        provider=Provider(), system_prompt='system', user_prompt='same clauses', signal=None,
        stage='destinations')
    assert payload == {'complete': True}
    assert usage == {'total_tokens': 2}
    assert len(calls) == 2 and calls[0] is calls[1]


@pytest.mark.anyio
async def test_model_transport_retries_are_bounded(monkeypatch):
    import app.mandate_risk_v2.pipeline as module
    async def no_delay(_seconds):
        pass
    monkeypatch.setattr(module.asyncio, 'sleep', no_delay)
    calls = []
    class Provider:
        async def run_skill(self, run_input):
            calls.append(run_input)
            raise httpx.RemoteProtocolError('incomplete chunked read')
            yield
    with pytest.raises(httpx.RemoteProtocolError):
        await RequirementExtractionPipeline()._call_model(
            provider=Provider(), system_prompt='system', user_prompt='input', signal=None)
    assert len(calls) == 3


@pytest.mark.anyio
async def test_invalid_model_output_does_not_trigger_transport_retries():
    calls = []
    class Provider:
        async def run_skill(self, run_input):
            calls.append(run_input)
            yield SimpleNamespace(contentDelta='invalid JSON', usage=None)
    with pytest.raises(ValueError):
        await RequirementExtractionPipeline()._call_model(
            provider=Provider(), system_prompt='system', user_prompt='input', signal=None)
    assert len(calls) == 1


@pytest.mark.anyio
async def test_cancelled_request_does_not_restart_a_broken_model_stream():
    signal = SimpleNamespace(aborted=False)
    calls = []
    class Provider:
        async def run_skill(self, run_input):
            calls.append(run_input)
            signal.aborted = True
            raise httpx.RemoteProtocolError('incomplete chunked read')
            yield
    with pytest.raises(httpx.RemoteProtocolError):
        await RequirementExtractionPipeline()._call_model(
            provider=Provider(), system_prompt='system', user_prompt='input', signal=signal)
    assert len(calls) == 1
