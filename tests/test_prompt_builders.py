import pytest
from app.prompt import build_generate_prompt, build_repair_prompt, GeneratePromptOptions, RepairPromptOptions
from app.contracts.types import ValidationIssue


def test_builds_generation_prompt_without_js_preselected_candidates():
    prompt = build_generate_prompt({
        "input": {
            "userMessage": "我想知道股票净敞口",
            "selectedBlockId": "b-1",
            "currentDsls": [{"id": "b-1", "action": "create", "view": {"title": "Test"}}],
            "globalQueryParameters": {
                "benchmarkCode": "000300.SH",
                "startDate": "2024-01-01",
            },
            "nonemptyFlags": {
                "benchmarkCode": True,
                "startDate": False,
            },
            "historyMessages": [],
        },
        "skillMd": "# Hermes Skill\nUse read_vmchat_skill_resource tool.",
    })

    assert "# Hermes Skill" in prompt.system_prompt
    assert "catalog/profile-index.json" in prompt.system_prompt
    assert "catalog/profiles/<moduleId>.json" in prompt.system_prompt
    assert "merge-guidance-v2.md" in prompt.system_prompt
    assert "单位不同不是拒绝合并的理由" in prompt.system_prompt
    assert "非 DSL 场景禁止返回裸文本" in prompt.system_prompt
    assert "entity=unknown 不是可合并证据" in prompt.system_prompt
    assert "只有字段/指标名称存在歧义" in prompt.system_prompt
    assert "Python 服务端会执行 Schema、执行契约和语义合并校验" in prompt.system_prompt
    assert "意图:" not in prompt.system_prompt
    assert "候选 Catalog" not in prompt.system_prompt

    assert "benchmarkCode (nonempty: true)" in prompt.user_prompt
    assert "startDate (nonempty: false)" in prompt.user_prompt
    assert "000300.SH" not in prompt.user_prompt
    assert "2024-01-01" not in prompt.user_prompt
    assert "selectedBlockId: b-1" in prompt.user_prompt


def test_truncates_oldest_history_first_when_user_prompt_exceeds_max_prompt_chars():
    history_messages = [
        {
            "role": "user" if i % 2 == 0 else "assistant",
            "content": f"Message {i} " + ("x" * 500),
        }
        for i in range(10)
    ]

    prompt = build_generate_prompt({
        "input": {
            "userMessage": "最新请求",
            "historyMessages": history_messages,
        },
        "skillMd": "Skill",
        "maxPromptChars": 5000,
    })

    assert len(prompt.system_prompt) + len(prompt.user_prompt) <= 5000
    assert "最新请求" in prompt.user_prompt


def test_throws_prompt_context_too_large_if_protected_content_alone_exceeds_limit():
    huge_skill = "Skill " * 10000

    with pytest.raises(Exception, match="PROMPT_CONTEXT_TOO_LARGE"):
        build_generate_prompt({
            "input": {"userMessage": "test"},
            "skillMd": huge_skill,
            "maxPromptChars": 500,
        })


def test_builds_repair_prompt_with_invalid_candidate_validation_issues_and_resource_context():
    resource_context = {
        "catalog/index.md": "# Catalog Index",
        "catalog/modules/modA.md": "# Module A",
    }

    prompt = build_repair_prompt({
        "invalidCandidate": {"action": "create", "id": "bad"},
        "validationErrors": [
            ValidationIssue(code="INVALID_UUID", path="/id", message="ID 必须是有效 UUID")
        ],
        "input": {
            "userMessage": "股票净敞口时序",
        },
        "resourceContext": resource_context,
        "skillMd": "Skill",
    })

    assert "INVALID_UUID" in prompt.user_prompt
    assert "ID 必须是有效 UUID" in prompt.user_prompt
    assert "# Catalog Index" in prompt.user_prompt
    assert "# Module A" in prompt.user_prompt
