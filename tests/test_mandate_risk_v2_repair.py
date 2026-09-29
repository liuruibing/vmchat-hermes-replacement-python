import json

import pytest

from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline


class Chunk:
    def __init__(self, content=None, usage=None):
        self.contentDelta = content
        self.usage = usage


def _json_line_after(prompt: str, marker: str):
    return json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])


DOCUMENT = (
    "[Page 1]\n"
    "If sleeve NAV is below USD 60 million, exposure shall not exceed USD 6 million.\n\n"
    "If sleeve NAV is USD 60 million or more, exposure shall not exceed 18% of sleeve NAV."
)


class RepairingProvider:
    def __init__(self):
        self.extraction_calls = 0
        self.coverage_calls = 0
        self.saw_feedback = False

    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            self.extraction_calls += 1
            clauses = _json_line_after(prompt, "# Input clauses (JSON)\n")
            if "# Previous coverage review feedback" in prompt:
                self.saw_feedback = True
            requirements = [
                {
                    "local_id": "r1",
                    "requirement_type": "CONDITIONAL_RULE",
                    "semantic_summary": "Below USD 60m NAV, exposure is capped at USD 6m.",
                    "conditions": [
                        {"left": "sleeve NAV", "operator": "<", "right": "USD 60 million"}
                    ],
                    "constraint": {"operator": "<=", "value": 6, "unit": "USD million"},
                    "evidence": {"clause_ids": [clauses[0]["clause_id"]]},
                }
            ]
            if self.saw_feedback:
                requirements.append(
                    {
                        "local_id": "r2",
                        "requirement_type": "CONDITIONAL_RULE",
                        "semantic_summary": "At or above USD 60m NAV, exposure is capped at 18% of NAV.",
                        "conditions": [
                            {"left": "sleeve NAV", "operator": ">=", "right": "USD 60 million"}
                        ],
                        "constraint": {"operator": "<=", "value": 18, "unit": "% of sleeve NAV"},
                        "evidence": {"clause_ids": [clauses[1]["clause_id"]]},
                    }
                )
            yield Chunk(
                content=json.dumps(
                    {"requirements": requirements, "definitions": [], "contextual_facts": []}
                ),
                usage={"total_tokens": 10},
            )
            return

        if "# Requirement coverage review" in prompt:
            self.coverage_calls += 1
            clauses = _json_line_after(prompt, "# All canonical clauses (JSON)\n")
            current_ir = _json_line_after(prompt, "# Current Requirement IR (JSON)\n")
            requirements = current_ir["requirements"]
            assessments = []
            for clause in clauses:
                matching = [
                    item["requirement_id"]
                    for item in requirements
                    if clause["clause_id"] in item["evidence"]["clause_ids"]
                ]
                if matching:
                    assessments.append(
                        {
                            "clause_id": clause["clause_id"],
                            "disposition": "COVERED",
                            "requirement_ids": matching,
                            "reason": "The branch is represented by a Requirement.",
                        }
                    )
                else:
                    assessments.append(
                        {
                            "clause_id": clause["clause_id"],
                            "disposition": "MISSING",
                            "requirement_ids": [],
                            "reason": "This conditional branch is missing.",
                        }
                    )

            if len(requirements) == 1:
                yield Chunk(
                    content=json.dumps(
                        {
                            "missing_clauses": [
                                {
                                    "clause_id": clauses[1]["clause_id"],
                                    "reason": "The second conditional branch is missing.",
                                }
                            ],
                            "partial_requirements": [],
                            "hint_assessments": assessments,
                        }
                    ),
                    usage={"total_tokens": 4},
                )
                return
            yield Chunk(
                content=json.dumps(
                    {
                        "missing_clauses": [],
                        "partial_requirements": [],
                        "hint_assessments": assessments,
                    }
                ),
                usage={"total_tokens": 4},
            )
            return

        pytest.fail("unexpected prompt")


@pytest.mark.anyio
async def test_coverage_feedback_triggers_full_semantic_reextract_and_closes_branch_gap():
    provider = RepairingProvider()
    result = await RequirementExtractionPipeline(
        batch_size=8,
        overlap=1,
        max_repair_rounds=2,
    ).run(
        document_name="branching.pdf",
        document_text=DOCUMENT,
        provider=provider,
    )

    assert provider.extraction_calls == 2
    assert provider.coverage_calls == 2
    assert provider.saw_feedback is True
    assert result.extraction_attempts == 2
    assert result.coverage_review.complete is True
    assert len(result.requirement_ir.requirements) == 2
    assert [item.conditions[0].operator for item in result.requirement_ir.requirements] == ["<", ">="]
    assert result.usage["complete"] is True
    assert result.usage["total_tokens"] == 28
