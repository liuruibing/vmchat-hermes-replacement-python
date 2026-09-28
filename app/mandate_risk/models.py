from __future__ import annotations

from typing import List, Literal

from pydantic import BaseModel, Field


MatchLevel = Literal["DIRECT", "STRONG_INFERRED", "WEAK_INFERRED", "REJECTED"]


class RawRiskMetric(BaseModel):
    """One immutable row from the authoritative risk-metric sheet.

    ``raw_*`` values are stored exactly as read from the source snapshot.
    Derived grouping fields are separate so callers never have to mutate the
    source row.
    """

    row_id: int
    source_row: int
    raw_risk_type_1: str = ""
    raw_risk_type_2: str = ""
    metric_name: str
    algorithm: str = ""
    mandate: str = ""
    strategy_type: str = ""
    effective_risk_type_1: str = ""
    effective_risk_type_2: str = ""


class CandidateClauseHint(BaseModel):
    clause_id: str
    text: str
    score: float = 0.0
    source_start: int = 0
    source_end: int = 0


class MetricCandidate(BaseModel):
    raw_row_id: int
    metric_name: str
    strategy_match: bool = True
    deterministic_score: float = 0.0
    exact_hits: List[str] = Field(default_factory=list)
    matched_clauses: List[CandidateClauseHint] = Field(default_factory=list)


class EvidenceQuote(BaseModel):
    text: str
    page: int | None = None
    clause_id: str | None = None
    source_start: int | None = None
    source_end: int | None = None


class MetricMatch(BaseModel):
    raw_row_id: int
    metric_name: str
    match_level: MatchLevel
    confidence: float = 0.0
    reason: str = ""
    evidence: List[EvidenceQuote] = Field(default_factory=list)


class LibraryGap(BaseModel):
    requirement: str
    reason: str = ""
    evidence: List[EvidenceQuote] = Field(default_factory=list)


class RiskAnalysisResult(BaseModel):
    document_name: str = ""
    strategy_type: str = ""
    selected_metrics: List[MetricMatch] = Field(default_factory=list)
    review_metrics: List[MetricMatch] = Field(default_factory=list)
    rejected_metrics: List[MetricMatch] = Field(default_factory=list)
    library_gaps: List[LibraryGap] = Field(default_factory=list)
    summary: str = ""
