from __future__ import annotations

import re
from typing import Dict, Iterable, List, Sequence, Tuple

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.constraint_validator import validate_requirement_constraints
from app.mandate_risk_v2.models import (
    CanonicalEvidence,
    ContextFact,
    Definition,
    ExtractionBatch,
    Requirement,
    RequirementIR,
    RequirementRelation,
)


def chunk_clauses(
    clauses: Sequence[DocumentClause],
    *,
    max_clauses: int = 24,
    overlap: int = 2,
) -> List[List[DocumentClause]]:
    """Create contiguous semantic-reading windows without changing provenance.

    Overlap gives the model local context around an artificial batch boundary.
    Duplicate extractions from the overlap are removed later only when their
    type and evidence identity are exactly the same; semantic guesses are never
    merged by Python.
    """

    if max_clauses <= 0:
        raise ValueError("max_clauses must be positive")
    if overlap < 0 or overlap >= max_clauses:
        raise ValueError("overlap must be >= 0 and < max_clauses")
    if not clauses:
        return []

    step = max_clauses - overlap
    return [
        list(clauses[start : start + max_clauses])
        for start in range(0, len(clauses), step)
    ]


def _known_clause_ids(clauses: Iterable[DocumentClause]) -> set[str]:
    return {clause.clause_id for clause in clauses}


def _validate_evidence_ids(
    clause_ids: Sequence[str],
    *,
    known_clause_ids: set[str],
    owner: str,
) -> None:
    if len(set(clause_ids)) != len(clause_ids):
        raise ValueError(f"{owner} evidence contains duplicate clause_id")
    unknown = [clause_id for clause_id in clause_ids if clause_id not in known_clause_ids]
    if unknown:
        raise ValueError(f"{owner} evidence contains unknown clause_id: {', '.join(unknown)}")


def validate_extraction_payload(
    payload: dict,
    *,
    allowed_clauses: Sequence[DocumentClause],
) -> ExtractionBatch:
    """Parse untrusted model JSON and validate all identity-bearing references."""

    batch = ExtractionBatch.model_validate(payload)
    known = _known_clause_ids(allowed_clauses)

    requirement_ids = [item.local_id for item in batch.requirements]
    if len(set(requirement_ids)) != len(requirement_ids):
        raise ValueError("requirement local_id must be unique within one extraction batch")

    definition_ids = [item.local_id for item in batch.definitions]
    if len(set(definition_ids)) != len(definition_ids):
        raise ValueError("definition local_id must be unique within one extraction batch")

    context_ids = [item.local_id for item in batch.contextual_facts]
    if len(set(context_ids)) != len(context_ids):
        raise ValueError("context fact local_id must be unique within one extraction batch")

    requirement_id_set = set(requirement_ids)
    for item in batch.requirements:
        _validate_evidence_ids(
            item.evidence.clause_ids,
            known_clause_ids=known,
            owner=f"requirement {item.local_id}",
        )
        for relation in item.relations:
            if relation.target_local_id not in requirement_id_set:
                raise ValueError(
                    f"requirement {item.local_id} relation targets unknown local_id: "
                    f"{relation.target_local_id}"
                )

    for item in batch.definitions:
        _validate_evidence_ids(
            item.evidence.clause_ids,
            known_clause_ids=known,
            owner=f"definition {item.local_id}",
        )
    for item in batch.contextual_facts:
        _validate_evidence_ids(
            item.evidence.clause_ids,
            known_clause_ids=known,
            owner=f"context fact {item.local_id}",
        )

    validate_requirement_constraints(batch.requirements, clauses=allowed_clauses)
    return batch


def _text_key(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip().casefold()


def _requirement_fingerprint(item) -> Tuple[str, str, Tuple[str, ...]]:
    # Deliberately conservative: Python removes only exact evidence-identical
    # duplicates caused by overlapping extraction windows. It does not decide
    # whether two semantically similar requirements are equivalent.
    return (
        item.requirement_type,
        _text_key(item.semantic_summary),
        tuple(sorted(item.evidence.clause_ids)),
    )


def build_requirement_ir(
    *,
    document_name: str,
    batches: Sequence[ExtractionBatch],
) -> RequirementIR:
    requirements: List[Requirement] = []
    definitions: List[Definition] = []
    contextual_facts: List[ContextFact] = []
    seen_requirements: Dict[Tuple[str, str, Tuple[str, ...]], str] = {}
    seen_definitions: set[Tuple[str, Tuple[str, ...]]] = set()
    seen_context: set[Tuple[str, str, Tuple[str, ...]]] = set()

    for batch_index, batch in enumerate(batches, start=1):
        local_to_final: Dict[str, str] = {}
        pending = []
        for item in batch.requirements:
            fingerprint = _requirement_fingerprint(item)
            existing = seen_requirements.get(fingerprint)
            if existing:
                local_to_final[item.local_id] = existing
                continue
            requirement_id = f"REQ-{len(requirements) + len(pending) + 1:04d}"
            local_to_final[item.local_id] = requirement_id
            pending.append((item, fingerprint, requirement_id))

        for item, fingerprint, requirement_id in pending:
            relations = [
                RequirementRelation(
                    type=relation.type,
                    target_requirement_id=local_to_final[relation.target_local_id],
                )
                for relation in item.relations
            ]
            requirements.append(
                Requirement(
                    requirement_id=requirement_id,
                    requirement_type=item.requirement_type,
                    semantic_summary=item.semantic_summary,
                    subject=item.subject,
                    measurement=item.measurement,
                    constraint=item.constraint,
                    scope=item.scope,
                    conditions=item.conditions,
                    exceptions=item.exceptions,
                    relations=relations,
                    evidence=item.evidence,
                    attributes={**item.attributes, "source_batch": batch_index},
                )
            )
            seen_requirements[fingerprint] = requirement_id

        for item in batch.definitions:
            fingerprint = (_text_key(item.term), tuple(sorted(item.evidence.clause_ids)))
            if fingerprint in seen_definitions:
                continue
            definitions.append(
                Definition(
                    definition_id=f"DEF-{len(definitions) + 1:04d}",
                    term=item.term,
                    semantic_summary=item.semantic_summary,
                    evidence=item.evidence,
                )
            )
            seen_definitions.add(fingerprint)

        for item in batch.contextual_facts:
            fingerprint = (
                _text_key(item.fact_type),
                _text_key(item.semantic_summary),
                tuple(sorted(item.evidence.clause_ids)),
            )
            if fingerprint in seen_context:
                continue
            contextual_facts.append(
                ContextFact(
                    fact_id=f"CTX-{len(contextual_facts) + 1:04d}",
                    fact_type=item.fact_type,
                    semantic_summary=item.semantic_summary,
                    value=item.value,
                    evidence=item.evidence,
                    attributes=item.attributes,
                )
            )
            seen_context.add(fingerprint)

    return RequirementIR(
        document_name=document_name,
        requirements=requirements,
        definitions=definitions,
        contextual_facts=contextual_facts,
    )


def canonical_evidence(
    clause_ids: Sequence[str], clauses: Sequence[DocumentClause]
) -> List[CanonicalEvidence]:
    """Rebuild report evidence from Python-owned clause provenance."""

    by_id = {clause.clause_id: clause for clause in clauses}
    result: List[CanonicalEvidence] = []
    for clause_id in clause_ids:
        clause = by_id.get(clause_id)
        if clause is None:
            raise ValueError(f"unknown clause_id: {clause_id}")
        result.append(
            CanonicalEvidence(
                clause_id=clause.clause_id,
                text=clause.text,
                page=clause.page,
                source_start=clause.source_start,
                source_end=clause.source_end,
            )
        )
    return result
