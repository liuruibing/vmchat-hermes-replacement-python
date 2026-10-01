from __future__ import annotations

from pathlib import Path
from typing import Literal, Sequence

from pydantic import Field

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.mapping import MappingResult
from app.mandate_risk_v2.mapping_models import CompatibilityDimension, MappingLink, MetricRowAssessment
from app.mandate_risk_v2.models import (
    CanonicalEvidence,
    ContextFact,
    Definition,
    Requirement,
    RequirementIR,
    StrictModel,
)


class RequirementResultItem(StrictModel):
    """One frozen Requirement plus Python-owned source evidence."""

    requirement: Requirement
    evidence: list[CanonicalEvidence] = Field(default_factory=list)


class MetricReference(StrictModel):
    """Read-only projection of one authoritative metric-catalogue row."""

    raw_row_id: int
    source_row: int
    metric_name: str
    algorithm: str = ""
    mandate: str = ""
    strategy_type: str = ""
    risk_type_1: str = ""
    risk_type_2: str = ""


class MetricRequirementResult(StrictModel):
    """One document-supported Requirement -> metric association."""

    requirement: RequirementResultItem
    mapping_level: Literal["DIRECT", "REVIEW", "REJECTED"]
    mapping_reason: str
    compatibility: list[CompatibilityDimension] = Field(default_factory=list)
    mapping_evidence: list[CanonicalEvidence] = Field(default_factory=list)
    review_notes: list[str] = Field(default_factory=list)
    match_score: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    score_reason: str | None = None


class MatchedMetricResult(StrictModel):
    metric: MetricReference
    requirements: list[MetricRequirementResult] = Field(default_factory=list)
    match_score: float | None = Field(default=None, ge=0, le=100, allow_inf_nan=False)
    score_reason: str | None = None


class DestinationResultItem(StrictModel):
    destination: Literal["PENDING_REVIEW", "LIBRARY_GAP", "NON_METRIC"]
    requirement: RequirementResultItem
    aspect: str
    reason: str
    candidate_metrics: list[MetricReference] = Field(default_factory=list)
    evidence: list[CanonicalEvidence] = Field(default_factory=list)


class V2AnalysisResult(StrictModel):
    """Stable structured V2 output from which Markdown/UI views can be rendered."""

    document_name: str
    coverage_status: Literal["complete"] = "complete"
    metric_catalogue_name: str
    metric_catalogue_sha256: str | None = None
    catalogue_assessments: list[MetricRowAssessment] = Field(default_factory=list)
    document_profile: dict = Field(default_factory=dict)
    requirements: list[RequirementResultItem] = Field(default_factory=list)
    matched_metrics: list[MatchedMetricResult] = Field(default_factory=list)
    candidate_metrics: list[MatchedMetricResult] = Field(default_factory=list)
    screened_metrics: list[MatchedMetricResult] = Field(default_factory=list)
    score_type: Literal["model_relevance"] = "model_relevance"
    pending_review: list[DestinationResultItem] = Field(default_factory=list)
    library_gaps: list[DestinationResultItem] = Field(default_factory=list)
    non_metric_requirements: list[DestinationResultItem] = Field(default_factory=list)
    unresolved_requirements: list[RequirementResultItem] = Field(default_factory=list)
    definitions: list[Definition] = Field(default_factory=list)
    contextual_facts: list[ContextFact] = Field(default_factory=list)
    summary: str = ""


def _metric_reference(metric: RawRiskMetric) -> MetricReference:
    return MetricReference(
        raw_row_id=metric.row_id,
        source_row=metric.source_row,
        metric_name=metric.metric_name,
        algorithm=metric.algorithm,
        mandate=metric.mandate,
        strategy_type=metric.strategy_type,
        risk_type_1=metric.effective_risk_type_1 or metric.raw_risk_type_1,
        risk_type_2=metric.effective_risk_type_2 or metric.raw_risk_type_2,
    )


def _catalogue_name(registry: RawRiskMetricRegistry) -> str:
    if not registry.source_path:
        return "传入的只读指标库"
    return Path(registry.source_path).name


def build_v2_analysis_result(
    *,
    ir: RequirementIR,
    clauses: Sequence[DocumentClause],
    registry: RawRiskMetricRegistry,
    mapping: MappingResult,
) -> V2AnalysisResult:
    """Build one canonical business result without inventing display-time semantics."""

    requirement_results = {
        item.requirement_id: RequirementResultItem(
            requirement=item,
            evidence=canonical_evidence(item.evidence.clause_ids, clauses),
        )
        for item in ir.requirements
    }

    direct_by_row: dict[int, list] = {}
    for link in mapping.direct_links:
        direct_by_row.setdefault(link.raw_row_id, []).append(link)

    candidates_by_row: dict[int, list] = {}
    for link in mapping.candidate_links:
        candidates_by_row.setdefault(link.raw_row_id, []).append(link)

    screening_by_row: dict[int, list[MappingLink]] = {}
    for link in mapping.screening_links:
        screening_by_row.setdefault(link.raw_row_id, []).append(link)

    def metric_requirement(link: MappingLink) -> MetricRequirementResult:
        notes = [destination.reason for item in mapping.dispositions.dispositions
                 if item.requirement_id == link.requirement_id
                 for destination in item.destinations
                 if destination.destination == "PENDING_REVIEW" and link.raw_row_id in destination.raw_row_ids]
        return MetricRequirementResult(
            requirement=requirement_results[link.requirement_id],
            mapping_level=link.level, mapping_reason=link.reason,
            compatibility=link.compatibility,
            mapping_evidence=canonical_evidence(link.evidence_clause_ids, clauses),
            review_notes=notes,
            match_score=link.match_score, score_reason=link.score_reason,
        )

    matched_metrics: list[MatchedMetricResult] = []
    candidate_metrics: list[MatchedMetricResult] = []
    screened_metrics: list[MatchedMetricResult] = []
    for metric in registry.all():
        links = direct_by_row.get(metric.row_id, [])
        if links:
            matched_metrics.append(
                MatchedMetricResult(
                    metric=_metric_reference(metric),
                    requirements=[metric_requirement(link) for link in links],
                )
            )
        candidates = candidates_by_row.get(metric.row_id, [])
        if candidates:
            candidate_metrics.append(
                MatchedMetricResult(
                    metric=_metric_reference(metric),
                    requirements=[metric_requirement(link) for link in candidates],
                )
            )
        screened_links = screening_by_row.get(metric.row_id, [])
        if screened_links:
            scored = [link for link in screened_links if link.match_score is not None]
            strongest = max(scored, key=lambda link: link.match_score) if scored else None
            screened_metrics.append(MatchedMetricResult(
                metric=_metric_reference(metric),
                requirements=[metric_requirement(link) for link in screened_links],
                match_score=strongest.match_score if strongest else None,
                score_reason=strongest.score_reason if strongest else None,
            ))
    screened_metrics.sort(key=lambda item: (
        item.match_score is None, -(item.match_score or 0), item.metric.raw_row_id,
    ))

    pending: list[DestinationResultItem] = []
    gaps: list[DestinationResultItem] = []
    non_metrics: list[DestinationResultItem] = []
    for disposition in mapping.dispositions.dispositions:
        requirement_result = requirement_results[disposition.requirement_id]
        for destination in disposition.destinations:
            if destination.destination == "MAIN_TABLE":
                continue
            item = DestinationResultItem(
                destination=destination.destination,
                requirement=requirement_result,
                aspect=destination.aspect,
                reason=destination.reason,
                candidate_metrics=[
                    _metric_reference(registry.require(row_id))
                    for row_id in destination.raw_row_ids
                ],
                evidence=canonical_evidence(destination.evidence_clause_ids, clauses),
            )
            if destination.destination == "PENDING_REVIEW":
                pending.append(item)
            elif destination.destination == "LIBRARY_GAP":
                gaps.append(item)
            elif destination.destination == "NON_METRIC":
                non_metrics.append(item)

    summary = (
        f"识别 {len(requirement_results)} 条 Requirement；"
        f"筛选出 {len(screened_metrics)} 个相关指标，按匹配分排序；"
        f"{len(pending)} 个待确认项；"
        f"{len(gaps)} 个指标库缺口；"
        f"{len(non_metrics)} 个非指标要求。"
    )

    return V2AnalysisResult(
        document_name=ir.document_name,
        metric_catalogue_name=_catalogue_name(registry),
        metric_catalogue_sha256=registry.source_sha256 or None,
        catalogue_assessments=mapping.row_assessments,
        document_profile=ir.document_profile,
        requirements=list(requirement_results.values()),
        matched_metrics=matched_metrics,
        candidate_metrics=candidate_metrics,
        screened_metrics=screened_metrics,
        pending_review=pending,
        library_gaps=gaps,
        non_metric_requirements=non_metrics,
        # A completed Phase A is fail-closed, so unresolved extraction items are
        # empty here by construction. Keeping the field makes the API explicit
        # and leaves room for a future best-effort/manual-review mode.
        unresolved_requirements=[],
        definitions=ir.definitions,
        contextual_facts=ir.contextual_facts,
        summary=summary,
    )
