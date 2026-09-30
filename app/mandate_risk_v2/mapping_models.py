from __future__ import annotations

from typing import Literal

from pydantic import Field

from app.mandate_risk_v2.models import StrictModel


# Reference dimensions for explaining a match; screening does not require all of them.
CORE_COMPATIBILITY_DIMENSIONS = (
    "measurement_object",
    "aggregation_level",
    "scope",
    "denominator",
    "time_point",
    "annualisation",
    "estimation_basis",
    "benchmark",
    "unit_semantics",
    "conditions",
    "strategy_applicability",
    "algorithm_semantics",
)


class CompatibilityDimension(StrictModel):
    dimension: str = Field(min_length=1)
    requirement_basis: str = Field(min_length=1)
    metric_basis: str = Field(min_length=1)
    relation: Literal["EQUIVALENT", "INSUFFICIENT", "CONFLICT", "NOT_APPLICABLE"]
    reason: str = Field(min_length=1)


class MappingLink(StrictModel):
    requirement_id: str
    raw_row_id: int
    level: Literal["DIRECT", "REVIEW", "REJECTED"]
    compatibility: list[CompatibilityDimension] = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(min_length=1)
    reason: str = Field(min_length=1)
    match_score: float | None = Field(default=None, ge=0, le=100, strict=True, allow_inf_nan=False)
    score_reason: str | None = Field(default=None, min_length=1)


class MetricRowAssessment(StrictModel):
    raw_row_id: int
    outcome: Literal["LINKED", "NOT_RELEVANT"]
    reason: str = Field(min_length=1)


class MappingBatch(StrictModel):
    links: list[MappingLink]
    row_assessments: list[MetricRowAssessment]


class RequirementDestination(StrictModel):
    destination: Literal["MAIN_TABLE", "PENDING_REVIEW", "LIBRARY_GAP", "NON_METRIC"]
    raw_row_ids: list[int]
    evidence_clause_ids: list[str] = Field(min_length=1)
    aspect: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class RequirementDisposition(StrictModel):
    requirement_id: str
    destinations: list[RequirementDestination] = Field(min_length=1)
    reason: str = Field(min_length=1)


class FinalMappingReview(StrictModel):
    dispositions: list[RequirementDisposition]


class CriticVerdict(StrictModel):
    requirement_id: str
    destination: Literal["MAIN_TABLE", "LIBRARY_GAP", "NON_METRIC"]
    raw_row_id: int | None
    aspect: str
    verdict: Literal["CONFIRM", "CHALLENGE", "UNRESOLVED"]
    reason: str = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(min_length=1)


class CandidateRejection(StrictModel):
    requirement_id: str
    raw_row_id: int
    reason: str = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(min_length=1)


class MissingAspect(StrictModel):
    requirement_id: str
    aspect: str = Field(min_length=1)
    reason: str = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(min_length=1)


class ScoreAdjustment(StrictModel):
    requirement_id: str
    raw_row_id: int
    match_score: float = Field(ge=0, le=100, strict=True, allow_inf_nan=False)
    score_reason: str = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(min_length=1)


class CriticReview(StrictModel):
    verdicts: list[CriticVerdict]
    recalled_links: list[MappingLink] = Field(default_factory=list)
    rejected_candidates: list[CandidateRejection] = Field(default_factory=list)
    missing_aspects: list[MissingAspect] = Field(default_factory=list)
    score_adjustments: list[ScoreAdjustment] = Field(default_factory=list)
