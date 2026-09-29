from __future__ import annotations

from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping_models import (
    CORE_COMPATIBILITY_DIMENSIONS,
    CriticReview,
    FinalMappingReview,
    MappingBatch,
    MappingLink,
)
from app.mandate_risk_v2.models import RequirementIR


_CORE_DIMENSION_SET = set(CORE_COMPATIBILITY_DIMENSIONS)


def _requirements(ir: RequirementIR):
    return {item.requirement_id: item for item in ir.requirements}


def _related_requirement_ids(ir: RequirementIR, requirement_id: str) -> set[str]:
    """Return only explicitly linked Requirements, in either relation direction."""

    related: set[str] = set()
    for requirement in ir.requirements:
        if requirement.requirement_id == requirement_id:
            related.update(relation.target_requirement_id for relation in requirement.relations)
        elif any(
            relation.target_requirement_id == requirement_id
            for relation in requirement.relations
        ):
            related.add(requirement.requirement_id)
    return related


def _validate_evidence(ir: RequirementIR, requirement_id: str, clause_ids: list[str]):
    requirement = _requirements(ir).get(requirement_id)
    if requirement is None:
        raise ValueError(f"unknown requirement_id: {requirement_id}")

    own = set(requirement.evidence.clause_ids)
    definitions = {
        clause_id
        for item in ir.definitions
        for clause_id in item.evidence.clause_ids
    }
    contextual = {
        clause_id
        for item in ir.contextual_facts
        for clause_id in item.evidence.clause_ids
    }
    related_ids = _related_requirement_ids(ir, requirement_id)
    related = {
        clause_id
        for item in ir.requirements
        if item.requirement_id in related_ids
        for clause_id in item.evidence.clause_ids
    }
    known = {
        clause_id
        for item in (*ir.requirements, *ir.definitions, *ir.contextual_facts)
        for clause_id in item.evidence.clause_ids
    }
    allowed = own | definitions | contextual | related

    cited = set(clause_ids)
    if len(cited) != len(clause_ids):
        raise ValueError(f"invalid evidence for {requirement_id}: duplicate clause_id")
    if not cited.issubset(known):
        raise ValueError(
            f"invalid evidence for {requirement_id}: unknown clause_ids={sorted(cited - known)}"
        )
    if not cited.intersection(own):
        raise ValueError(
            f"requirement {requirement_id} has no own evidence in citation: "
            f"cited={sorted(cited)}, required_one_of={sorted(own)}"
        )
    unsupported = cited - allowed
    if unsupported:
        raise ValueError(
            f"invalid evidence for {requirement_id}: unrelated requirement clause_ids="
            f"{sorted(unsupported)}"
        )


def _validate_compatibility(link: MappingLink, *, registry: RawRiskMetricRegistry) -> None:
    dimensions = [item.dimension for item in link.compatibility]
    if len(set(dimensions)) != len(dimensions):
        raise ValueError(
            f"duplicate compatibility dimension: {(link.requirement_id, link.raw_row_id)}"
        )

    dimension_map = {item.dimension: item for item in link.compatibility}
    if link.level != "REJECTED":
        missing = _CORE_DIMENSION_SET - set(dimension_map)
        if missing:
            raise ValueError(
                f"{link.level} compatibility matrix missing core dimensions: "
                + ", ".join(sorted(missing))
            )

    if link.level == "DIRECT" and any(
        item.relation in {"INSUFFICIENT", "CONFLICT"}
        for item in link.compatibility
    ):
        raise ValueError("DIRECT has incompatible compatibility dimension")

    # This is a source-availability check, not a semantic inference.  If the
    # authoritative row has no algorithm text, the model cannot claim that the
    # row itself supplies an equivalent algorithm basis for a DIRECT mapping.
    if link.level == "DIRECT":
        row = registry.require(link.raw_row_id)
        algorithm_dimension = dimension_map["algorithm_semantics"]
        if not (row.algorithm or "").strip() and algorithm_dimension.relation == "EQUIVALENT":
            raise ValueError(
                "DIRECT algorithm_semantics cannot be EQUIVALENT when metric algorithm is empty"
            )


def validate_batch(
    payload: dict, *, ir: RequirementIR, registry: RawRiskMetricRegistry,
    batch_row_ids: set[int],
) -> MappingBatch:
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
        _validate_compatibility(link, registry=registry)
    for item in batch.row_assessments:
        if (item.raw_row_id in linked_rows) != (item.outcome == "LINKED"):
            raise ValueError(f"row assessment disagrees with links: {item.raw_row_id}")
    return batch


def validate_dispositions(
    payload: dict, *, ir: RequirementIR, registry: RawRiskMetricRegistry,
    links: list[MappingLink],
) -> FinalMappingReview:
    review = FinalMappingReview.model_validate(payload)
    expected = set(_requirements(ir))
    actual = [item.requirement_id for item in review.dispositions]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("requirement dispositions missing, duplicated or unknown")
    link_map = {(link.requirement_id, link.raw_row_id): link for link in links}
    selected_direct: set[tuple[str, int]] = set()
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
                if destination.destination == "MAIN_TABLE" and link.level != "DIRECT":
                    raise ValueError("MAIN_TABLE has no DIRECT link")
                if destination.destination == "PENDING_REVIEW" and link.level != "REVIEW":
                    raise ValueError("PENDING_REVIEW metric row has no REVIEW link")
                if destination.destination == "MAIN_TABLE":
                    selected_direct.add((disposition.requirement_id, row_id))
            if destination.destination == "MAIN_TABLE" and not destination.raw_row_ids:
                raise ValueError("MAIN_TABLE has no DIRECT link")
            if destination.destination in {"LIBRARY_GAP", "NON_METRIC"} and destination.raw_row_ids:
                raise ValueError("non-metric destination cannot reference metric rows")
    proposed_direct = {
        (link.requirement_id, link.raw_row_id) for link in links if link.level == "DIRECT"
    }
    if selected_direct != proposed_direct:
        raise ValueError("DIRECT links lack matching MAIN_TABLE destination")
    return review


def validate_critic(payload: dict, *, ir: RequirementIR, dispositions: FinalMappingReview) -> CriticReview:
    review = CriticReview.model_validate(payload)
    expected = {
        (item.requirement_id, dest.destination, row_id, dest.aspect)
        for item in dispositions.dispositions
        for dest in item.destinations
        if dest.destination in {"MAIN_TABLE", "LIBRARY_GAP"}
        for row_id in (dest.raw_row_ids if dest.destination == "MAIN_TABLE" else [None])
    }
    actual = [
        (item.requirement_id, item.destination, item.raw_row_id, item.aspect)
        for item in review.verdicts
    ]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError("critic verdicts missing, duplicated or unexpected")
    for verdict in review.verdicts:
        _validate_evidence(ir, verdict.requirement_id, verdict.evidence_clause_ids)
    return review
