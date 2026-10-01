import json

import pytest

from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline


class Chunk:
    def __init__(self, content=None, usage=None):
        self.contentDelta = content
        self.usage = usage


def _json_line_after(prompt: str, marker: str):
    return json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])


DOCUMENT = "[Page 1]\nA shall not exceed 10%.\n\nB shall not exceed 20%."


class ValidationRepairProvider:
    def __init__(self):
        self.extraction_calls = 0
        self.coverage_calls = 0
        self.saw_validation_feedback = False
        self.saw_reextract_feedback = False

    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            self.extraction_calls += 1
            clauses = _json_line_after(prompt, "# Input clauses (JSON)\n")
            if "# Previous coverage review feedback" in prompt:
                self.saw_reextract_feedback = True
            requirements = [{"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
                "semantic_summary": "A shall not exceed 10%.",
                "constraint": {"operator": "<=", "value": 10, "unit": "%", "raw_value_text": "10%"},
                "evidence": {"clause_ids": [clauses[0]["clause_id"]]}}]
            if self.saw_reextract_feedback:
                requirements.append({"local_id": "r2", "requirement_type": "QUANTITATIVE_LIMIT",
                    "semantic_summary": "B shall not exceed 20%.",
                    "constraint": {"operator": "<=", "value": 20, "unit": "%", "raw_value_text": "20%"},
                    "evidence": {"clause_ids": [clauses[1]["clause_id"]]}})
            yield Chunk(content=json.dumps({"requirements": requirements, "definitions": [], "contextual_facts": []}),
                        usage={"total_tokens": 10})
            return
        if "# Requirement coverage review" in prompt:
            self.coverage_calls += 1
            hints = _json_line_after(prompt, "# Python coverage hints (JSON; every canonical clause appears exactly once and must be assessed)\n")
            current_ir = _json_line_after(prompt, "# Current Requirement IR (JSON)\n")
            evidence_map = _json_line_after(prompt, "# Deterministic requirement evidence map for clauses (JSON)\n")
            first_clause_id, second_clause_id = [item["clause_id"] for item in hints]
            if self.coverage_calls == 1:
                assert evidence_map[first_clause_id] == ["REQ-0001"] and evidence_map[second_clause_id] == []
                payload = {"missing_clauses": [], "partial_requirements": [], "hint_assessments": [
                    {"clause_id": first_clause_id, "disposition": "COVERED", "requirement_ids": ["REQ-0001"], "reason": "covered"},
                    {"clause_id": second_clause_id, "disposition": "COVERED", "requirement_ids": ["REQ-0001"], "reason": "wrong ref"}]}
            elif self.coverage_calls == 2:
                self.saw_validation_feedback = "# Previous coverage review failed deterministic validation" in prompt
                payload = {"missing_clauses": [{"clause_id": second_clause_id,
                    "reason": "The second limit is not represented."}], "partial_requirements": [], "hint_assessments": [
                    {"clause_id": first_clause_id, "disposition": "COVERED", "requirement_ids": ["REQ-0001"], "reason": "covered"},
                    {"clause_id": second_clause_id, "disposition": "MISSING", "requirement_ids": [], "reason": "missing"}]}
            else:
                assessments = []
                for hint in hints:
                    clause_id = hint["clause_id"]
                    requirement_ids = [item["requirement_id"] for item in current_ir["requirements"]
                                       if clause_id in item["evidence"]["clause_ids"]]
                    assessments.append({"clause_id": clause_id, "disposition": "COVERED",
                                        "requirement_ids": requirement_ids, "reason": "covered"})
                payload = {"missing_clauses": [], "partial_requirements": [], "hint_assessments": assessments}
            yield Chunk(content=json.dumps(payload), usage={"total_tokens": 4})
            return
        pytest.fail("unexpected prompt")


@pytest.mark.anyio
async def test_invalid_covered_reference_is_repaired_then_reextracted():
    provider = ValidationRepairProvider()
    result = await RequirementExtractionPipeline(max_repair_rounds=2).run(
        document_name="synthetic.pdf", document_text=DOCUMENT, provider=provider)
    assert result.coverage_review.complete is True
    assert provider.extraction_calls == 2 and provider.coverage_calls == 3
    assert provider.saw_validation_feedback is True and provider.saw_reextract_feedback is True
    assert len(result.requirement_ir.requirements) == 2
    assert result.usage["complete"] is True
    assert result.usage["coverage_review"]["expected_calls"] == 3
    assert result.usage["total_tokens"] == 32
