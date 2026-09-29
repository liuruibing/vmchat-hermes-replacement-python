import json

import pytest

from app.mandate_risk_v2.pipeline import (
    RequirementCoverageIncomplete,
    RequirementExtractionPipeline,
)


class Chunk:
    def __init__(self, content=None, usage=None):
        self.contentDelta = content
        self.usage = usage


def _json_line_after(prompt: str, marker: str):
    return json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])


def _coverage_assessments(prompt: str, *, missing_clause_id: str | None = None):
    hints = _json_line_after(
        prompt,
        "# Python coverage hints (JSON; every hint must be assessed exactly once)\n",
    )
    current_ir = _json_line_after(prompt, "# Current Requirement IR (JSON)\n")
    requirements = current_ir["requirements"]
    definitions = current_ir["definitions"]
    contexts = current_ir["contextual_facts"]
    result = []
    for hint in hints:
        clause_id = hint["clause_id"]
        if clause_id == missing_clause_id:
            result.append(
                {
                    "clause_id": clause_id,
                    "disposition": "MISSING",
                    "requirement_ids": [],
                    "reason": "An important requirement is not represented yet.",
                }
            )
            continue
        requirement_ids = [
            item["requirement_id"]
            for item in requirements
            if clause_id in item["evidence"]["clause_ids"]
        ]
        if requirement_ids:
            result.append(
                {
                    "clause_id": clause_id,
                    "disposition": "COVERED",
                    "requirement_ids": requirement_ids,
                    "reason": "Covered by the cited requirement.",
                }
            )
            continue
        if any(clause_id in item["evidence"]["clause_ids"] for item in definitions + contexts):
            result.append(
                {
                    "clause_id": clause_id,
                    "disposition": "DEFINITION_OR_CONTEXT",
                    "requirement_ids": [],
                    "reason": "The numeric content belongs to a definition/context, not a mandate obligation.",
                }
            )
            continue
        result.append(
            {
                "clause_id": clause_id,
                "disposition": "NOT_REQUIREMENT",
                "requirement_ids": [],
                "reason": "No mandate requirement is expressed by this hinted clause.",
            }
        )
    return result


DOCUMENT = (
    "[Page 1]\n"
    '“Liquidity Reserve” means assets convertible to cash within three business days.\n\n'
    "[Page 2]\n"
    "The portfolio shall maintain at least 9% of NAV in the Liquidity Reserve."
)


class CompleteProvider:
    def __init__(self):
        self.extraction_calls = 0
        self.coverage_calls = 0

    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            self.extraction_calls += 1
            clauses = _json_line_after(prompt, "# Input clauses (JSON)\n")
            by_page = {item["page"]: item["clause_id"] for item in clauses}
            yield Chunk(
                content=json.dumps(
                    {
                        "requirements": [
                            {
                                "local_id": "r1",
                                "requirement_type": "QUANTITATIVE_LIMIT",
                                "semantic_summary": "Maintain at least 9% of NAV in the Liquidity Reserve.",
                                "measurement": {
                                    "concept": "liquidity reserve",
                                    "object": "share of NAV held in qualifying liquid assets",
                                    "qualifiers": {},
                                },
                                "constraint": {
                                    "operator": ">=",
                                    "value": 9,
                                    "unit": "% of NAV",
                                },
                                "evidence": {"clause_ids": [by_page[2]]},
                            }
                        ],
                        "definitions": [
                            {
                                "local_id": "d1",
                                "term": "Liquidity Reserve",
                                "semantic_summary": "Assets convertible to cash within three business days.",
                                "evidence": {"clause_ids": [by_page[1]]},
                            }
                        ],
                        "contextual_facts": [],
                    }
                ),
                usage={"total_tokens": 11},
            )
            return

        if "# Requirement coverage review" in prompt:
            self.coverage_calls += 1
            current_ir = _json_line_after(prompt, "# Current Requirement IR (JSON)\n")
            assert current_ir["requirements"][0]["constraint"]["value"] == 9
            yield Chunk(
                content=json.dumps(
                    {
                        "missing_clauses": [],
                        "partial_requirements": [],
                        "hint_assessments": _coverage_assessments(prompt),
                    }
                ),
                usage={"total_tokens": 7},
            )
            return

        pytest.fail("unexpected model prompt")


@pytest.mark.anyio
async def test_phase_a_pipeline_builds_requirement_ir_before_any_metric_mapping():
    provider = CompleteProvider()
    result = await RequirementExtractionPipeline(batch_size=8, overlap=1).run(
        document_name="synthetic.pdf",
        document_text=DOCUMENT,
        provider=provider,
    )

    assert provider.extraction_calls == 1
    assert provider.coverage_calls == 1
    assert result.coverage_review.complete is True
    assert result.extraction_mode == "full_document"
    assert len(result.requirement_ir.requirements) == 1
    assert len(result.requirement_ir.definitions) == 1
    requirement = result.requirement_ir.requirements[0]
    assert requirement.requirement_id == "REQ-0001"
    assert requirement.constraint.value == 9
    assert requirement.evidence.clause_ids == [result.clauses[1].clause_id]
    assert result.usage["complete"] is True
    assert result.usage["total_tokens"] == 18


class MissingCoverageProvider(CompleteProvider):
    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        if "# Requirement extraction batch" in prompt:
            async for chunk in super().run_skill(run_input):
                yield chunk
            return
        if "# Requirement coverage review" in prompt:
            clauses = _json_line_after(prompt, "# All canonical clauses (JSON)\n")
            requirement_clause = next(item for item in clauses if item["page"] == 2)
            yield Chunk(
                content=json.dumps(
                    {
                        "missing_clauses": [
                            {
                                "clause_id": requirement_clause["clause_id"],
                                "reason": "Reviewer says an important branch or qualifier is still unresolved.",
                            }
                        ],
                        "partial_requirements": [],
                        "hint_assessments": _coverage_assessments(
                            prompt, missing_clause_id=requirement_clause["clause_id"]
                        ),
                    }
                )
            )
            return
        pytest.fail("unexpected model prompt")


@pytest.mark.anyio
async def test_phase_a_pipeline_fails_closed_when_coverage_is_incomplete():
    with pytest.raises(RequirementCoverageIncomplete, match="COVERAGE_INCOMPLETE") as exc:
        await RequirementExtractionPipeline(
            batch_size=8,
            overlap=1,
            max_repair_rounds=0,
        ).run(
            document_name="synthetic.pdf",
            document_text=DOCUMENT,
            provider=MissingCoverageProvider(),
        )

    assert exc.value.review.complete is False
    assert len(exc.value.review.missing_clauses) == 1


class InvalidCoverageProvider(CompleteProvider):
    async def run_skill(self, run_input):
        if "# Requirement extraction batch" in run_input.user_prompt:
            async for chunk in super().run_skill(run_input):
                yield chunk
            return
        yield Chunk(
            content=json.dumps(
                {
                    "missing_clauses": [
                        {"clause_id": "fake-clause", "reason": "invented"}
                    ],
                    "partial_requirements": [],
                    "hint_assessments": [],
                }
            )
        )


@pytest.mark.anyio
async def test_phase_a_pipeline_rejects_model_invented_coverage_clause():
    with pytest.raises(ValueError, match="unknown missing clause_id"):
        await RequirementExtractionPipeline(batch_size=8, overlap=1).run(
            document_name="synthetic.pdf",
            document_text=DOCUMENT,
            provider=InvalidCoverageProvider(),
        )


class OmittedHintProvider(CompleteProvider):
    async def run_skill(self, run_input):
        if "# Requirement extraction batch" in run_input.user_prompt:
            async for chunk in super().run_skill(run_input):
                yield chunk
            return
        yield Chunk(
            content=json.dumps(
                {
                    "missing_clauses": [],
                    "partial_requirements": [],
                    "hint_assessments": [],
                }
            )
        )


@pytest.mark.anyio
async def test_empty_coverage_review_cannot_silently_skip_high_risk_hints():
    with pytest.raises(ValueError, match="omitted hint assessments"):
        await RequirementExtractionPipeline(batch_size=8, overlap=1).run(
            document_name="synthetic.pdf",
            document_text=DOCUMENT,
            provider=OmittedHintProvider(),
        )
