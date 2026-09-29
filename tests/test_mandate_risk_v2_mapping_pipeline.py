import json

import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingPipeline
from app.mandate_risk_v2.mapping_prompts import MAPPING_SYSTEM_PROMPT, batch_prompt
from app.mandate_risk_v2.models import Definition, EvidenceRef, Requirement, RequirementIR


class Chunk:
    def __init__(self, content):
        self.contentDelta = content
        self.usage = {"total_tokens": 7}


class Provider:
    def __init__(self, *, challenge=False):
        self.prompts = []
        self.challenge = challenge

    async def run_skill(self, run_input):
        prompt = run_input.user_prompt
        self.prompts.append(prompt)
        if "# V2 mapping batch" in prompt:
            rows = json.loads(prompt.split("# Raw metric rows (JSON)\n", 1)[1].split("\n", 1)[0])
            yield Chunk(json.dumps({"links": [
                {"requirement_id": "REQ-0001", "raw_row_id": rows[0]["row_id"],
                 "level": "DIRECT", "compatibility": [
                     {"dimension": "denominator", "requirement_basis": "NAV",
                      "metric_basis": "NAV", "relation": "EQUIVALENT", "reason": "same"}],
                 "evidence_clause_ids": ["c0001"], "reason": "direct"}],
                 "row_assessments": [
                     {"raw_row_id": row["row_id"],
                      "outcome": "LINKED" if index == 0 else "NOT_RELEVANT",
                      "reason": "audited"} for index, row in enumerate(rows)]}))
        elif "# V2 final destinations" in prompt:
            yield Chunk(json.dumps({"dispositions": [{"requirement_id": "REQ-0001",
                "reason": "one aspect", "destinations": [{"destination": "MAIN_TABLE",
                "raw_row_ids": [2], "evidence_clause_ids": ["c0001"],
                "aspect": "portfolio exposure", "reason": "matching algorithm"}]}]}))
        elif "# V2 independent critic" in prompt:
            yield Chunk(json.dumps({"verdicts": [{"requirement_id": "REQ-0001",
                "destination": "MAIN_TABLE", "raw_row_id": 2,
                "aspect": "portfolio exposure",
                "verdict": "CHALLENGE" if self.challenge else "CONFIRM",
                "reason": "verified", "evidence_clause_ids": ["c0001"]}]}))
        else:
            pytest.fail("unexpected prompt")


def _data():
    ir = RequirementIR(document_name="new.pdf", requirements=[Requirement(
        requirement_id="REQ-0001", requirement_type="QUANTITATIVE_LIMIT",
        semantic_summary="Cap exposure at NAV basis", evidence=EvidenceRef(clause_ids=["c0001"]),
    )])
    clauses = [DocumentClause(clause_id="c0001", text="Exposure shall not exceed NAV.", page=1)]
    registry = RawRiskMetricRegistry([
        RawRiskMetric(row_id=2, source_row=2, metric_name="Never-seen Exposure Measure",
                      algorithm="exposure / NAV"),
        RawRiskMetric(row_id=3, source_row=3, metric_name="Other Measure", algorithm="turnover"),
    ])
    return ir, clauses, registry


def test_mapping_prompt_gives_exact_relation_enum_not_generic_synonyms():
    ir, clauses, registry = _data()
    prompt = MAPPING_SYSTEM_PROMPT + batch_prompt(ir, clauses, registry.all())
    assert '"relation":"EQUIVALENT"' in prompt
    assert "MISMATCH" in prompt
    assert "PARTIAL" in prompt


def test_mapping_prompt_includes_definition_source_without_turning_it_into_requirement():
    ir, clauses, registry = _data()
    ir.definitions.append(Definition(definition_id="DEF-0001", term="NAV",
                                     semantic_summary="Net asset value",
                                     evidence=EvidenceRef(clause_ids=["c0002"])))
    clauses.append(DocumentClause(clause_id="c0002", text="NAV means net asset value.", page=2))
    prompt = batch_prompt(ir, clauses, registry.all())
    assert "NAV means net asset value." in prompt


@pytest.mark.anyio
async def test_new_metric_is_mapped_only_after_independent_critic():
    ir, clauses, registry = _data()
    provider = Provider()
    result = await MappingPipeline(batch_size=2).run(
        ir=ir, clauses=clauses, registry=registry, provider=provider,
    )
    assert [link.raw_row_id for link in result.direct_links] == [2]
    assert len(provider.prompts) == 3
    assert result.usage["total_tokens"] == 21


@pytest.mark.anyio
async def test_critic_challenge_moves_unconfirmed_direct_to_pending_not_main_table():
    ir, clauses, registry = _data()
    result = await MappingPipeline(batch_size=2, max_critic_repairs=0).run(
        ir=ir, clauses=clauses, registry=registry, provider=Provider(challenge=True),
    )
    assert result.direct_links == []
    destination = result.dispositions.dispositions[0].destinations[0]
    assert destination.destination == "PENDING_REVIEW"
    assert "Critic" in destination.reason
