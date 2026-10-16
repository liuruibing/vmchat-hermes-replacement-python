import asyncio
import json
import shlex

import pytest

from scripts import omp_openai_gateway as gateway


@pytest.mark.parametrize('exit_code', [0, 1])
def test_stdout_model_error_is_reported_even_without_stderr(tmp_path, monkeypatch, exit_code):
    event = {'type': 'message_end', 'message': {
        'role': 'assistant', 'stopReason': 'error',
        'errorMessage': 'INVALID_ARGUMENT: unsupported tool schema if/then',
        'content': [],
    }}
    executable = tmp_path / 'omp'
    executable.write_text(
        '#!/bin/sh\nprintf "%s\\n" ' + shlex.quote(json.dumps(event))
        + f'\nexit {exit_code}\n', encoding='utf-8',
    )
    executable.chmod(0o700)
    monkeypatch.setattr(gateway.shutil, 'which', lambda _name: str(executable))

    with pytest.raises(RuntimeError, match='INVALID_ARGUMENT: unsupported tool schema if/then'):
        asyncio.run(gateway.call_omp('system', 'request'))


@pytest.mark.parametrize('reason', ['aborted', 'length'])
def test_partial_model_output_is_not_returned_as_success(tmp_path, monkeypatch, reason):
    event = {'type': 'message_end', 'message': {
        'role': 'assistant', 'stopReason': reason,
        'content': [{'type': 'text', 'text': '{"incomplete":'}],
    }}
    executable = tmp_path / 'omp'
    executable.write_text(
        '#!/bin/sh\nprintf "%s\\n" ' + shlex.quote(json.dumps(event)) + '\n',
        encoding='utf-8',
    )
    executable.chmod(0o700)
    monkeypatch.setattr(gateway.shutil, 'which', lambda _name: str(executable))

    with pytest.raises(RuntimeError, match=f'stopReason={reason}'):
        asyncio.run(gateway.call_omp('system', 'request'))


@pytest.mark.anyio
async def test_cancelled_call_reaps_its_omp_process(tmp_path, monkeypatch):
    executable = tmp_path / 'omp'
    executable.write_text('#!/bin/sh\nexec sleep 60\n', encoding='utf-8')
    executable.chmod(0o700)
    monkeypatch.setattr(gateway.shutil, 'which', lambda _name: str(executable))
    spawn = asyncio.create_subprocess_exec
    processes = []
    started = asyncio.Event()

    async def capture(*args, **kwargs):
        process = await spawn(*args, **kwargs)
        processes.append(process)
        started.set()
        return process

    monkeypatch.setattr(gateway.asyncio, 'create_subprocess_exec', capture)
    task = asyncio.create_task(gateway.call_omp('system', 'request'))
    await asyncio.wait_for(started.wait(), 2)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await asyncio.wait_for(task, 2)
    assert processes[0].returncode is not None
    assert processes[0].returncode < 0
