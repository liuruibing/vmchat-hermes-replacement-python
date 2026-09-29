import pytest

from scripts.mandate_risk_v2_remote_e2e import terminal_event


def test_sse_reader_ignores_nonterminal_events_and_keeps_report():
    lines = [
        b'data: {"event":"reasoning.delta","delta":"working"}\n',
        b'\n',
        b'data: {"event":"run.completed","output":"| x |","usage":{"total_tokens":4}}\n',
    ]
    result = terminal_event(lines)
    assert result["event"] == "run.completed"
    assert result["output"] == "| x |"


def test_sse_reader_can_report_phase_progress_without_ending_stream():
    progress = []
    terminal_event([
        b'data: {"event":"reasoning.delta","delta":"Phase A complete"}\n',
        b'data: {"event":"run.completed","output":"done"}\n',
    ], progress=progress.append)
    assert progress == ["Phase A complete"]


def test_sse_reader_fails_if_stream_ends_without_terminal_event():
    with pytest.raises(RuntimeError, match="without terminal"):
        terminal_event([b'data: {"event":"reasoning.delta"}\n'])
