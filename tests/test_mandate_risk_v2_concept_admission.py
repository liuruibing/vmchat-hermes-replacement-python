import pytest

from app.mandate_risk_v2.mapping import MappingResult, _apply_unconfirmed_critic_verdicts
from app.mandate_risk_v2.mapping_models import FinalMappingReview, MappingLink, critic_targets
from app.mandate_risk_v2.mapping_validator import validate_batch, validate_critic
from tests.test_mandate_risk_v2_mapping_contract import _fixture, _link, _batch_payload


@pytest.mark.parametrize("dimension", ["measurement_object", "aggregation_level", "scope", "denominator", "unit_semantics", "algorithm_semantics"])
@pytest.mark.parametrize("level", ["DIRECT", "REVIEW"])
def test_a_known_different_concept_cannot_be_retained_as_a_high_scoring_candidate(dimension, level):
    ir, registry = _fixture()
    item = _link(level=level)
    item.update(match_score=99, score_reason="High relevance cannot resolve a known contradiction.")
    next(d for d in item["compatibility"] if d["dimension"] == dimension)["relation"] = "CONFLICT"
    with pytest.raises(ValueError, match="contradicts concept identity"):
        validate_batch(_batch_payload(item), ir=ir, registry=registry, batch_row_ids={2, 3})
    item["level"] = "REJECTED"
    batch = validate_batch(_batch_payload(item), ir=ir, registry=registry, batch_row_ids={2, 3})
    assert batch.links[0].level == "REJECTED"


def test_unknown_parameters_do_not_become_false_concept_conflicts():
    ir, registry = _fixture()
    item = _link(level="REVIEW")
    for dimension in item["compatibility"]:
        if dimension["dimension"] in {"denominator", "algorithm_semantics"}:
            dimension["relation"] = "INSUFFICIENT"
        elif dimension["dimension"] == "estimation_basis":
            dimension["relation"] = "CONFLICT"
    batch = validate_batch(_batch_payload(item), ir=ir, registry=registry, batch_row_ids={2, 3})
    assert batch.links[0].level == "REVIEW"


def pending():
    return FinalMappingReview.model_validate({"dispositions": [{
        "requirement_id": "REQ-0001", "reason": "Same concept with unknown calculation basis.",
        "destinations": [{"destination": "PENDING_REVIEW", "raw_row_ids": [2],
                          "evidence_clause_ids": ["c0001"], "aspect": "exposure",
                          "reason": "Confirm implementation before use."}],
    }]})


@pytest.mark.parametrize("with_destination", [False, True])
def test_every_candidate_requires_an_independent_verdict_even_without_a_destination(with_destination):
    ir, registry = _fixture()
    links = [MappingLink.model_validate(_link(level="REVIEW"))]
    dispositions = pending() if with_destination else FinalMappingReview(dispositions=[])
    with pytest.raises(ValueError, match="critic verdicts missing"):
        validate_critic({"verdicts": []}, ir=ir, dispositions=dispositions, registry=registry, links=links)


@pytest.mark.parametrize("verdict,retained", [("CHALLENGE", False), ("UNRESOLVED", True), ("CONFIRM", True)])
def test_critic_admission_rejects_different_concepts_but_preserves_unknown_implementations(verdict, retained):
    ir, registry = _fixture()
    links = [MappingLink.model_validate(_link(level="REVIEW"))]
    dispositions = pending()
    review = validate_critic({"verdicts": [{
        "target_id": "TGT-0001", "verdict": verdict,
        "reason": "Independent comparison of the source requirement and catalogue algorithm.",
        "evidence_clause_ids": ["c0001"],
    }]}, ir=ir, dispositions=dispositions, registry=registry, links=links)
    final = _apply_unconfirmed_critic_verdicts(dispositions, review)
    result = MappingResult(links=links, dispositions=final, critic=review, usage={})
    assert bool(result.screening_links) is retained
    assert bool(result.candidate_links) is retained
    assert bool(final.dispositions[0].destinations[0].raw_row_ids) is retained


def test_mixed_aspect_candidates_cannot_hide_an_unreviewed_row():
    dispositions = pending()
    dispositions.dispositions[0].destinations[0].raw_row_ids = [2, 3]
    ir, registry = _fixture()
    targets = critic_targets(dispositions)
    assert {target["raw_row_id"] for target in targets} == {2, 3}
    with pytest.raises(ValueError, match="critic verdicts missing"):
        validate_critic({"verdicts": [{"target_id": "TGT-0001", "verdict": "CONFIRM",
                                     "reason": "Only the first row was reviewed.",
                                     "evidence_clause_ids": ["c0001"]}]},
                        ir=ir, dispositions=dispositions, registry=registry)
