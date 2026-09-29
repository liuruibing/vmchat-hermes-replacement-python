import json

import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_v2 import MandateRiskV2Workflow
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry


class Chunk:
    def __init__(self, content=None, usage=None):
        self.contentDelta = content
        self.usage = usage


def _json_line_after(prompt: str, marker: str):
    return json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])


class Provider:
    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            clauses = _json_line_after(prompt, "# Input clauses (JSON)\n")
            target = next(item for item in clauses if "at least 7%" in item["text"])
            yield Chunk(
                content=json.dumps(
                    {
                        "requirements": [
                            {
                                "local_id": "r1",
                                "requirement_type": "QUANTITATIVE_LIMIT",
                                "semantic_summary": "The portfolio must maintain at least 7% liquidity.",
                                "constraint": {"operator": ">=", "value": 7, "unit": "%"},
                                "evidence": {"clause_ids": [target["clause_id"]]},
                            }
                        ],
                        "definitions": [],
                        "contextual_facts": [],
                    }
                ),
                usage={"total_tokens": 5},
            )
            return
        if "# Requirement coverage review" in prompt:
            hints = _json_line_after(
                prompt,
                "# Python coverage hints (JSON; every hint must be assessed exactly once)\n",
            )
            current_ir = _json_line_after(prompt, "# Current Requirement IR (JSON)\n")
            requirement_id = current_ir["requirements"][0]["requirement_id"]
            yield Chunk(
                content=json.dumps(
                    {
                        "missing_clauses": [],
                        "partial_requirements": [],
                        "hint_assessments": [
                            {
                                "clause_id": item["clause_id"],
                                "disposition": "COVERED",
                                "requirement_ids": [requirement_id],
                                "reason": "The quantitative obligation is covered.",
                            }
                            for item in hints
                        ],
                    }
                ),
                usage={"total_tokens": 3},
            )
            return
        pytest.fail("unexpected prompt")


@pytest.mark.anyio
async def test_v2_workflow_can_be_invoked_without_touching_metric_catalogue():
    input_val = VmChatInput(
        userMessage=(
            "<document_name>lab.pdf</document_name>"
            "<document_text>[Page 1]\n"
            "The portfolio shall maintain at least 7% liquidity."
            "</document_text>"
        ),
        globalQueryParameters=GlobalQueryParameters(),
        agentId="mandate-risk-v2-lab",
        roleId="requirement-analyst",
    )
    context = WorkflowContext(
        input_val=input_val,
        provider=Provider(),
        agent_id="mandate-risk-v2-lab",
        role_id="requirement-analyst",
    )

    events = [event async for event in MandateRiskV2Workflow(phase_a_only=True).stream(context)]

    assert events[0].event == "reasoning.delta"
    assert "不读取风险指标库" in events[0].delta
    assert events[-1].event == "run.completed"
    assert "REQ-0001" in events[-1].output
    assert "7%" in events[-1].output
    assert events[-1].usage["total_tokens"] == 8


class FullProvider(Provider):
    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# V2 mapping batch" in prompt:
            yield Chunk(content=json.dumps({"links": [{
                "requirement_id": "REQ-0001", "raw_row_id": 2, "level": "DIRECT",
                "compatibility": [{"dimension": "denominator", "requirement_basis": "NAV",
                                   "metric_basis": "NAV", "relation": "EQUIVALENT", "reason": "same"}],
                "evidence_clause_ids": ["c0001"], "reason": "direct",
            }], "row_assessments": [{"raw_row_id": 2, "outcome": "LINKED", "reason": "direct"}]}),
                usage={"total_tokens": 7})
        elif "# V2 final destinations" in prompt:
            yield Chunk(content=json.dumps({"dispositions": [{"requirement_id": "REQ-0001",
                "reason": "complete", "destinations": [{"destination": "MAIN_TABLE", "raw_row_ids": [2],
                "evidence_clause_ids": ["c0001"], "aspect": "liquidity", "reason": "direct"}]}]}),
                usage={"total_tokens": 7})
        elif "# V2 independent critic" in prompt:
            yield Chunk(content=json.dumps({"verdicts": [{"requirement_id": "REQ-0001",
                "destination": "MAIN_TABLE", "raw_row_id": 2, "aspect": "liquidity",
                "verdict": "CONFIRM", "reason": "verified", "evidence_clause_ids": ["c0001"]}]}),
                usage={"total_tokens": 7})
        else:
            async for chunk in super().run_skill(run_input):
                yield chunk


@pytest.mark.anyio
async def test_v2_workflow_outputs_critic_confirmed_six_column_report():
    input_val = VmChatInput(
        userMessage=("<document_name>new.pdf</document_name><document_text>[Page 1]\n"
                     "The portfolio shall maintain at least 7% liquidity.</document_text>"),
        globalQueryParameters=GlobalQueryParameters(), agentId="mandate-risk-v2-lab",
        roleId="requirement-analyst",
    )
    context = WorkflowContext(input_val=input_val, provider=FullProvider(),
                              agent_id="mandate-risk-v2-lab", role_id="requirement-analyst")
    registry = RawRiskMetricRegistry([RawRiskMetric(
        row_id=2, source_row=2, metric_name="Unseen Liquidity Metric",
        algorithm="liquid assets / NAV",
    )])
    events = [event async for event in MandateRiskV2Workflow(metric_registry=registry).stream(context)]
    assert events[-1].event == "run.completed"
    assert any(event.event == "reasoning.delta" and "Phase A 完成" in event.delta
               for event in events)
    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in events[-1].output
    assert "Unseen Liquidity Metric" in events[-1].output
    assert events[-1].usage["total_tokens"] == 29
