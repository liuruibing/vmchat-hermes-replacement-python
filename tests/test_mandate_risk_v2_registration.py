from app.agents.registry import AgentRegistry
from app.workflow.legacy import build_default_workflow_registry


async def _unused_stream(*args, **kwargs):
    if False:
        yield None


def test_v2_lab_agent_is_separate_from_production_v1_agent():
    agents = AgentRegistry("agents").load()

    v1 = agents.require("mandate-risk-ai")
    v2 = agents.require("mandate-risk-v2-lab")

    assert v1.workflow == "mandate-risk-analysis"
    assert v2.workflow == "mandate-risk-analysis-v2"
    assert v2.metadata.get("experimental") is True
    assert v2.id != v1.id

    role = agents.get_role("mandate-risk-v2-lab", "requirement-analyst")
    assert role is not None
    assert role.allowedSkills == []
    assert role.allowedTools == []
    assert "默认快速筛选" in role.systemPrompt
    assert "详细模式" in role.systemPrompt
    assert "独立 Critic 复核" in role.systemPrompt


def test_default_workflow_registry_exposes_v2_without_replacing_v1():
    workflows = build_default_workflow_registry(
        simple_chat_stream=_unused_stream,
        vm_report_stream=_unused_stream,
    )

    assert workflows.require("mandate-risk-analysis").id == "mandate-risk-analysis"
    assert workflows.require("mandate-risk-analysis-v2").id == "mandate-risk-analysis-v2"
    assert "mandate-risk-analysis" in workflows.list_ids()
    assert "mandate-risk-analysis-v2" in workflows.list_ids()
