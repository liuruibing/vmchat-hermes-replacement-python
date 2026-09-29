import pytest

from scripts.mandate_risk_v2_remote_e2e import (
    evaluate_gold,
    select_gold_spec,
    terminal_event,
)


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


def test_gold_can_assert_whole_report_and_specific_sections():
    report = """# Mandate 风险指标报告（V2）

## 匹配摘要

| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |
| --- | --- | --- | --- | --- | --- |
| key | 久期 | duration limit | — | — | — |

## 待确认

- REQ-0002 / tracking error：跟踪误差；annualised ex-ante basis unresolved

## 指标库缺口

### REQ-0003 / purchase yield
- 原因：new purchase yield is 10 basis points above benchmark
"""
    spec = {
        "must_contain": ["10 basis points"],
        "must_not_contain": ["invented metric"],
        "sections": {
            "## 匹配摘要": {"must_contain": ["久期"], "must_not_contain": ["跟踪误差"]},
            "## 待确认": {"must_contain": ["annualised ex-ante"]},
            "## 指标库缺口": {"must_contain": ["purchase yield"]},
        },
    }
    assert evaluate_gold(report, spec) == []

    spec["sections"]["## 匹配摘要"]["must_not_contain"] = ["久期"]
    errors = evaluate_gold(report, spec)
    assert any("forbidden text: 久期" in item for item in errors)


def test_gold_selection_prefers_sha_over_filename_and_rejects_duplicates():
    gold = {"documents": [
        {"name": "same.pdf", "must_contain": ["name fallback"]},
        {"name": "other.pdf", "sha256": "abc", "must_contain": ["sha match"]},
    ]}
    assert select_gold_spec(gold, pdf_name="same.pdf", sha256="abc")["must_contain"] == ["sha match"]
    assert select_gold_spec(gold, pdf_name="same.pdf", sha256="missing")["must_contain"] == ["name fallback"]
    assert select_gold_spec(gold, pdf_name="none.pdf", sha256="missing") is None

    duplicate = {"documents": [{"name": "x.pdf"}, {"name": "x.pdf"}]}
    with pytest.raises(ValueError, match="duplicate name"):
        select_gold_spec(duplicate, pdf_name="x.pdf", sha256="missing")
