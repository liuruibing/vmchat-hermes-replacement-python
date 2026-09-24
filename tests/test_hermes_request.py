import json
import pytest
from app.compatibility.hermes_request import (
    HermesCreateRunRequest,
    extract_json_block,
    normalize_create_run_request,
    normalize_vm_chat_input,
)


def test_normalize_create_run_request_valid():
    long_instructions = "A" * 600000
    raw = {
        "model": "deepseek-v4-flash",
        "instructions": long_instructions,
        "input": [{"role": "user", "content": "Hello"}],
        "session_id": "session-001",
        "skills": ["vm-report-dsl"],
    }

    normalized = normalize_create_run_request(raw)
    assert normalized.model == "deepseek-v4-flash"
    assert len(normalized.instructions) == 512000
    assert len(normalized.input) == 1
    assert normalized.session_id == "session-001"
    assert normalized.skills == ["vm-report-dsl"]


def test_rejects_non_string_message_content():
    raw = {
        "input": [{"role": "user", "content": 12345}],
    }
    with pytest.raises(ValueError, match="INVALID_REQUEST_FORMAT: Message content must be a string"):
        normalize_create_run_request(raw)


def test_rejects_input_with_over_20_items():
    input_items = [{"role": "user", "content": f"msg {i}"} for i in range(21)]
    with pytest.raises(ValueError, match="INVALID_REQUEST_FORMAT"):
        normalize_create_run_request({"input": input_items})


def test_rejects_non_empty_tools():
    raw = {
        "input": [{"role": "user", "content": "hi"}],
        "tools": [{"type": "function"}],
    }
    with pytest.raises(ValueError, match="UNSUPPORTED_TOOLS"):
        normalize_create_run_request(raw)


def test_accepts_agent_defined_skills_at_wire_normalization_layer():
    raw = {
        "input": [{"role": "user", "content": "hi"}],
        "skills": ["other-skill", "other-skill"],
    }
    normalized = normalize_create_run_request(raw)
    assert normalized.skills == ["other-skill"]


def test_normalize_vm_chat_input():
    instructions = "\n".join([
        "当前 selectedBlockId：block-123",
        "当前 currentDsls：",
        json.dumps([
            {
                "blockId": "block-123",
                "id": "dsl-123",
                "title": "股票净敞口",
                "dsl": {"action": "create", "id": "dsl-123", "requests": []},
            }
        ]),
        "当前全局查询条件（用户在界面顶部设置）：",
        json.dumps({"benchmarkCode": "000300.SH", "startDate": ""}),
    ])

    req = normalize_create_run_request({
        "input": [
            {"role": "user", "content": "锚点"},
            {"role": "user", "content": "把这个图变成表格"},
        ],
        "instructions": instructions,
    })

    vm_input = normalize_vm_chat_input(req)
    assert vm_input.userMessage == "把这个图变成表格"
    assert vm_input.selectedBlockId == "block-123"
    assert len(vm_input.currentDsls) == 1
    assert "benchmarkCode" in vm_input.globalQueryParameters.names
    assert vm_input.globalQueryParameters.nonemptyFlags["benchmarkCode"] is True
    assert vm_input.globalQueryParameters.nonemptyFlags["startDate"] is False


def test_parses_nested_current_dsls_without_truncating():
    instructions = "\n".join([
        "当前 currentDsls：",
        json.dumps(
            [
                {
                    "blockId": "block-123",
                    "id": "dsl-123",
                    "title": "股票净敞口",
                    "dsl": {
                        "action": "create",
                        "id": "dsl-123",
                        "requests": [{"id": "req-1", "moduleId": "averagePePb", "params": {"values": [1, 2]}}],
                        "view": {"type": "table", "columns": [{"field": "value", "label": "值"}]},
                    },
                }
            ],
            indent=2,
        ),
        "当前全局查询条件：",
        json.dumps({"startDate": "20220101"}),
    ])

    req = normalize_create_run_request({
        "input": [{"role": "user", "content": "持仓平均PE/PB时序"}],
        "instructions": instructions,
    })

    vm_input = normalize_vm_chat_input(req)
    assert len(vm_input.currentDsls) == 1
    assert vm_input.currentDsls[0].dsl.requests is not None
    assert len(vm_input.currentDsls[0].dsl.requests) == 1
    assert vm_input.globalQueryParameters.names == ["startDate"]


def test_throws_invalid_vmchat_context_when_current_dsls_malformed():
    req = normalize_create_run_request({
        "input": [{"role": "user", "content": "test"}],
        "instructions": "当前 currentDsls：\n[invalid json...",
    })
    with pytest.raises(ValueError, match="INVALID_VMCHAT_CONTEXT"):
        normalize_vm_chat_input(req)


def test_throws_invalid_vmchat_context_when_global_query_params_malformed():
    req = normalize_create_run_request({
        "input": [{"role": "user", "content": "test"}],
        "instructions": "当前全局查询条件：\n{invalid json...",
    })
    with pytest.raises(ValueError, match="INVALID_VMCHAT_CONTEXT"):
        normalize_vm_chat_input(req)


def test_extract_json_block_strings_with_brackets_and_escapes():
    sample_text = 'Marker:\n{"key": "a [b] {c} \\"quoted\\"", "list": [1, 2, {"nested": true}]}'
    result = extract_json_block(sample_text, "Marker:")
    assert json.loads(result) == {
        "key": 'a [b] {c} "quoted"',
        "list": [1, 2, {"nested": True}],
    }


def test_structured_context_takes_precedence_and_history_excludes_current_user():
    req = normalize_create_run_request({
        "input": [
            {"role": "user", "content": "vmChat 会话锚点：legacy。请记录但不要回复这条锚点。"},
            {"role": "user", "content": "上一轮问题"},
            {"role": "assistant", "content": "上一轮回答"},
            {"role": "user", "content": "把当前图改成表格"},
        ],
        "instructions": "当前 selectedBlockId：legacy-block\n当前 currentDsls：\n[]\n当前全局查询条件：\n{}",
        "context": {
            "selectedBlockId": "structured-block",
            "currentDsls": [
                {
                    "blockId": "structured-block",
                    "id": "00000000-0000-4000-8000-000000000001",
                    "title": "结构化上下文",
                    "dsl": {
                        "action": "create",
                        "id": "00000000-0000-4000-8000-000000000001",
                        "requests": [],
                    },
                }
            ],
            "globalQueryParams": {
                "fundCode": "F001",
                "beginDate": "",
            },
        },
    })

    vm_input = normalize_vm_chat_input(req)

    assert vm_input.userMessage == "把当前图改成表格"
    assert vm_input.selectedBlockId == "structured-block"
    assert len(vm_input.currentDsls) == 1
    assert vm_input.currentDsls[0].blockId == "structured-block"
    assert vm_input.globalQueryParameters.nonemptyFlags["fundCode"] is True
    assert vm_input.globalQueryParameters.nonemptyFlags["beginDate"] is False
    assert [item.content for item in vm_input.historyMessages] == ["上一轮问题", "上一轮回答"]


def test_rejects_non_object_structured_context():
    with pytest.raises(ValueError, match="context must be an object"):
        normalize_create_run_request({
            "input": [{"role": "user", "content": "test"}],
            "context": ["bad"],
        })
