from __future__ import annotations

from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import (
    CriticReview,
    FinalMappingReview,
    MappingBatch,
    MappingLink,
    critic_targets,
)
from app.mandate_risk_v2.models import RequirementIR


def _requirements(ir: RequirementIR):
    return {item.requirement_id: item for item in ir.requirements}


def _related_requirement_ids(ir: RequirementIR, requirement_id: str) -> set[str]:
    related: set[str] = set()
    for requirement in ir.requirements:
        if requirement.requirement_id == requirement_id:
            related.update(relation.target_requirement_id for relation in requirement.relations)
        elif any(relation.target_requirement_id == requirement_id for relation in requirement.relations):
            related.add(requirement.requirement_id)
    return related


def _validate_evidence(ir: RequirementIR, requirement_id: str, clause_ids: list[str]):
    requirement = _requirements(ir).get(requirement_id)
    if requirement is None:
        raise ValueError(f"unknown requirement_id: {requirement_id}")
    own = set(requirement.evidence.clause_ids)
    definitions = {cid for item in ir.definitions for cid in item.evidence.clause_ids}
    contextual = {cid for item in ir.contextual_facts for cid in item.evidence.clause_ids}
    related_ids = _related_requirement_ids(ir, requirement_id)
    related = {cid for item in ir.requirements if item.requirement_id in related_ids for cid in item.evidence.clause_ids}
    known = {cid for item in (*ir.requirements, *ir.definitions, *ir.contextual_facts) for cid in item.evidence.clause_ids}
    cited = set(clause_ids)
    if len(cited) != len(clause_ids):
        raise ValueError(f"invalid evidence for {requirement_id}: duplicate clause_id")
    if not cited.issubset(known):
        raise ValueError(f"invalid evidence for {requirement_id}: unknown clause_ids={sorted(cited-known)}")
    if not cited.intersection(own):
        raise ValueError(f"requirement {requirement_id} has no own evidence in citation")
    unsupported = cited - (own | definitions | contextual | related)
    if unsupported:
        raise ValueError(f"invalid evidence for {requirement_id}: unrelated requirement clause_ids={sorted(unsupported)}")


def _validate_link_details(link: MappingLink, *, require_scores: bool) -> None:
    dimensions = [item.dimension for item in link.compatibility]
    if len(set(dimensions)) != len(dimensions):
        raise ValueError(f"duplicate compatibility dimension: {(link.requirement_id, link.raw_row_id)}")
    if require_scores and link.level != "REJECTED" and link.match_score is None:
        raise ValueError("screening link requires match_score")
    if link.match_score is not None and not (link.score_reason or "").strip():
        raise ValueError("match_score requires score_reason")


def validate_batch(payload: dict, *, ir: RequirementIR, registry: RawRiskMetricRegistry,
                   batch_row_ids: set[int], require_scores: bool = False) -> MappingBatch:
    batch = MappingBatch.model_validate(payload)
    actual = [item.raw_row_id for item in batch.row_assessments]
    if len(actual) != len(set(actual)) or set(actual) != batch_row_ids:
        raise ValueError("mapping batch row assessments incomplete or duplicated")
    linked_rows = {item.raw_row_id for item in batch.links}
    seen: set[tuple[str, int]] = set()
    for link in batch.links:
        if registry.get(link.raw_row_id) is None or link.raw_row_id not in batch_row_ids:
            raise ValueError(f"unknown or cross-batch raw_row_id: {link.raw_row_id}")
        _validate_evidence(ir, link.requirement_id, link.evidence_clause_ids)
        identity = (link.requirement_id, link.raw_row_id)
        if identity in seen:
            raise ValueError(f"duplicate mapping link: {identity}")
        seen.add(identity)
        _validate_link_details(link, require_scores=require_scores)
    for item in batch.row_assessments:
        if (item.raw_row_id in linked_rows) != (item.outcome == "LINKED"):
            raise ValueError(f"row assessment disagrees with links: {item.raw_row_id}")
    return batch


def validate_dispositions(payload: dict, *, ir: RequirementIR, registry: RawRiskMetricRegistry, links: list[MappingLink]) -> FinalMappingReview:
    review = FinalMappingReview.model_validate(payload)
    expected = set(_requirements(ir))
    actual = [item.requirement_id for item in review.dispositions]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("requirement dispositions missing, duplicated or unknown")
    link_map = {(link.requirement_id, link.raw_row_id): link for link in links}
    for disposition in review.dispositions:
        seen_aspects: set[str] = set()
        for destination in disposition.destinations:
            _validate_evidence(ir, disposition.requirement_id, destination.evidence_clause_ids)
            if destination.aspect in seen_aspects:
                raise ValueError("duplicate requirement aspect")
            seen_aspects.add(destination.aspect)
            if len(set(destination.raw_row_ids)) != len(destination.raw_row_ids):
                raise ValueError("duplicate destination raw_row_id")
            for row_id in destination.raw_row_ids:
                if registry.get(row_id) is None:
                    raise ValueError(f"unknown destination raw_row_id: {row_id}")
                link = link_map.get((disposition.requirement_id, row_id))
                if link is None:
                    raise ValueError("destination has no mapping link")
                if link.level == "REJECTED":
                    raise ValueError("destination cannot select a REJECTED link")
            if destination.destination == "MAIN_TABLE" and not destination.raw_row_ids:
                raise ValueError("MAIN_TABLE has no screening link")
            if destination.destination in {"LIBRARY_GAP", "NON_METRIC"} and destination.raw_row_ids:
                raise ValueError("non-metric destination cannot reference metric rows")
    return review


def validate_critic(payload: dict, *, ir: RequirementIR, dispositions: FinalMappingReview,
                    registry: RawRiskMetricRegistry | None = None,
                    links: list[MappingLink] | None = None, require_scores: bool = False) -> CriticReview:
    targets = {item["target_id"]: item for item in critic_targets(dispositions)}
    verdicts = []
    for verdict in payload.get("verdicts", []):
        if not isinstance(verdict, dict) or "target_id" not in verdict:
            verdicts.append(verdict)
            continue
        target_id = verdict["target_id"]
        if not isinstance(target_id, str) or target_id not in targets:
            raise ValueError(f"unknown critic target_id: {target_id}")
        identity = {key: value for key, value in targets[target_id].items() if key != "target_id"}
        if any(key in verdict and verdict[key] != value for key, value in identity.items()):
            raise ValueError(f"critic target identity mismatch: {target_id}")
        verdicts.append({**identity, **{key: value for key, value in verdict.items() if key != "target_id"}})
    normalized = dict(payload)
    if "verdicts" in normalized:
        normalized["verdicts"] = verdicts
    review = CriticReview.model_validate(normalized)
    expected = {
        (item.requirement_id, dest.destination, row_id, dest.aspect)
        for item in dispositions.dispositions
        for dest in item.destinations
        if dest.destination in {"MAIN_TABLE", "LIBRARY_GAP", "NON_METRIC"}
        for row_id in (dest.raw_row_ids if dest.destination == "MAIN_TABLE" else [None])
    }
    actual = [(item.requirement_id, item.destination, item.raw_row_id, item.aspect) for item in review.verdicts]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("critic verdicts missing, duplicated or unexpected")
    for verdict in review.verdicts:
        _validate_evidence(ir, verdict.requirement_id, verdict.evidence_clause_ids)
    existing = {(link.requirement_id, link.raw_row_id): link for link in links or []}
    recalled: set[tuple[str, int]] = set()
    for link in review.recalled_links:
        if link.level != "REVIEW":
            raise ValueError("critic recalled links must be REVIEW candidates")
        if registry is None or registry.get(link.raw_row_id) is None:
            raise ValueError(f"unknown recalled raw_row_id: {link.raw_row_id}")
        identity = (link.requirement_id, link.raw_row_id)
        if identity in recalled or (identity in existing and existing[identity].level != "REJECTED"):
            raise ValueError("critic recalled duplicate existing candidate")
        _validate_evidence(ir, link.requirement_id, link.evidence_clause_ids)
        _validate_link_details(link, require_scores=require_scores)
        recalled.add(identity)
    rejected: set[tuple[str, int]] = set()
    for item in review.rejected_candidates:
        identity = (item.requirement_id, item.raw_row_id)
        if identity in rejected or identity not in existing or existing[identity].level == "REJECTED":
            raise ValueError("critic rejection must identify one existing screening candidate")
        _validate_evidence(ir, item.requirement_id, item.evidence_clause_ids)
        rejected.add(identity)
    adjusted: set[tuple[str, int]] = set()
    for item in review.score_adjustments:
        identity = (item.requirement_id, item.raw_row_id)
        if (identity in adjusted or identity in rejected or identity not in existing
                or existing[identity].level == "REJECTED"):
            raise ValueError("critic score adjustment must identify one retained existing link")
        if not item.score_reason.strip():
            raise ValueError("critic score adjustment requires score_reason")
        _validate_evidence(ir, item.requirement_id, item.evidence_clause_ids)
        adjusted.add(identity)
    aspects = {(item.requirement_id, destination.aspect)
               for item in dispositions.dispositions for destination in item.destinations}
    for item in review.missing_aspects:
        _validate_evidence(ir, item.requirement_id, item.evidence_clause_ids)
        identity = (item.requirement_id, item.aspect)
        if identity in aspects:
            raise ValueError("critic missing aspect duplicates an existing destination or missing aspect")
        aspects.add(identity)
    return review
