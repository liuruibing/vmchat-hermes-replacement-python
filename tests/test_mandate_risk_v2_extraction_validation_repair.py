import json

import pytest

from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline


class Chunk:
    def __init__(self, content):
        self.contentDelta = content
        self.usage = {"total_tokens": 2}


class Provider:
    def __init__(self):
        self.extractions = 0
        self.saw_feedback = False

    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            self.extractions += 1
            self.saw_feedback |= "# Previous extraction failed deterministic validation" in prompt
            clauses = json.loads(prompt.split("# Input clauses (JSON)\n", 1)[1].split("\n", 1)[0])
            value = {"bad": "shape"} if self.extractions == 1 else "portfolio liquidity"
            yield Chunk(json.dumps({"requirements": [{
                "local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
                "semantic_summary": "Maintain at least 7% liquidity",
                "measurement": {"object": value},
                "evidence": {"clause_ids": [clauses[0]["clause_id"]]},
            }], "definitions": [], "contextual_facts": []}))
        elif "# Requirement coverage review" in prompt:
            hints = json.loads(prompt.split("# Python coverage hints (JSON; every hint must be assessed exactly once)\n", 1)[1].split("\n", 1)[0])
            yield Chunk(json.dumps({"missing_clauses": [], "partial_requirements": [],
                "hint_assessments": [{"clause_id": item["clause_id"],
                    "disposition": "COVERED", "requirement_ids": ["REQ-0001"], "reason": "covered"}
                    for item in hints]}))
        else:
            pytest.fail("unexpected prompt")


@pytest.mark.anyio
async def test_invalid_extraction_shape_retries_same_clauses_without_python_semantic_fix():
    provider = Provider()
    result = await RequirementExtractionPipeline().run(
        document_name="new.pdf",
        document_text="[Page 1]\nPortfolio shall maintain at least 7% liquidity.",
        provider=provider,
    )
    assert provider.extractions == 2
    assert provider.saw_feedback
    assert result.requirement_ir.requirements[0].measurement.object == "portfolio liquidity"
    assert result.usage["requirement_extraction"]["expected_calls"] == 2
