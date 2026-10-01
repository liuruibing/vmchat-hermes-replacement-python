from __future__ import annotations

from typing import Any, Dict, List, Literal, Union

from pydantic import BaseModel, ConfigDict, Field


RequirementType = Literal[
    "OBJECTIVE",
    "STRATEGY",
    "SCOPE",
    "QUANTITATIVE_TARGET",
    "QUANTITATIVE_LIMIT",
    "PROHIBITION",
    "PERMISSION",
    "CONDITIONAL_RULE",
    "EXTERNAL_POLICY",
    "GOVERNANCE",
    "OTHER",
]
RelationType = Literal[
    "BRANCH_OF",
    "QUALIFIES",
    "EXCEPTION_TO",
    "DEFINES_SCOPE_FOR",
    "DEPENDS_ON",
]
CoverageHintDisposition = Literal[
    "COVERED",
    "DEFINITION_OR_CONTEXT",
    "NOT_REQUIREMENT",
    "MISSING",
    "PARTIAL",
]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceRef(StrictModel):
    clause_ids: List[str] = Field(min_length=1)


class RequirementSubject(StrictModel):
    text: str = ""
    normalized_type: str | None = None


class RequirementMeasurement(StrictModel):
    concept: str | None = None
    object: str | List[str] | None = None
    qualifiers: Dict[str, Any] = Field(default_factory=dict)


class RequirementConstraint(StrictModel):
    operator: str | None = None
    value: Any = None
    value_to: Any = None
    unit: str | None = None
    raw_value_text: str | None = None
    formula: str | None = None
    benchmark: str | None = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class RequirementCondition(StrictModel):
    left: str | None = None
    operator: str | None = None
    right: Any = None
    text: str | None = None
    attributes: Dict[str, Any] = Field(default_factory=dict)


class DraftRelation(StrictModel):
    type: RelationType
    target_local_id: str


class RequirementRelation(StrictModel):
    type: RelationType
    target_requirement_id: str


class RequirementDraft(StrictModel):
    local_id: str
    requirement_type: RequirementType
    semantic_summary: str
    subject: RequirementSubject = Field(default_factory=RequirementSubject)
    measurement: RequirementMeasurement = Field(default_factory=RequirementMeasurement)
    constraint: RequirementConstraint | None = None
    scope: Dict[str, Any] = Field(default_factory=dict)
    conditions: List[Union[RequirementCondition, Dict[str, Any], str]] = Field(default_factory=list)
    exceptions: List[Union[Dict[str, Any], str]] = Field(default_factory=list)
    relations: List[DraftRelation] = Field(default_factory=list)
    evidence: EvidenceRef
    attributes: Dict[str, Any] = Field(default_factory=dict)


class DefinitionDraft(StrictModel):
    local_id: str
    term: str
    semantic_summary: str
    evidence: EvidenceRef


class ContextFactDraft(StrictModel):
    local_id: str
    fact_type: str
    semantic_summary: str
    value: Any = None
    evidence: EvidenceRef
    attributes: Dict[str, Any] = Field(default_factory=dict)


class ExtractionBatch(StrictModel):
    requirements: List[RequirementDraft] = Field(default_factory=list)
    definitions: List[DefinitionDraft] = Field(default_factory=list)
    contextual_facts: List[ContextFactDraft] = Field(default_factory=list)


class Requirement(StrictModel):
    requirement_id: str
    requirement_type: RequirementType
    semantic_summary: str
    subject: RequirementSubject = Field(default_factory=RequirementSubject)
    measurement: RequirementMeasurement = Field(default_factory=RequirementMeasurement)
    constraint: RequirementConstraint | None = None
    scope: Dict[str, Any] = Field(default_factory=dict)
    conditions: List[Union[RequirementCondition, Dict[str, Any], str]] = Field(default_factory=list)
    exceptions: List[Union[Dict[str, Any], str]] = Field(default_factory=list)
    relations: List[RequirementRelation] = Field(default_factory=list)
    evidence: EvidenceRef
    attributes: Dict[str, Any] = Field(default_factory=dict)


class Definition(StrictModel):
    definition_id: str
    term: str
    semantic_summary: str
    evidence: EvidenceRef


class ContextFact(StrictModel):
    fact_id: str
    fact_type: str
    semantic_summary: str
    value: Any = None
    evidence: EvidenceRef
    attributes: Dict[str, Any] = Field(default_factory=dict)


class RequirementIR(StrictModel):
    document_name: str
    requirements: List[Requirement] = Field(default_factory=list)
    definitions: List[Definition] = Field(default_factory=list)
    contextual_facts: List[ContextFact] = Field(default_factory=list)
    document_profile: Dict[str, Any] = Field(default_factory=dict)


class CanonicalEvidence(StrictModel):
    clause_id: str
    text: str
    page: int | None = None
    source_start: int
    source_end: int


class MissingClause(StrictModel):
    clause_id: str
    reason: str


class PartialRequirement(StrictModel):
    requirement_id: str
    reason: str
    related_clause_ids: List[str] = Field(default_factory=list)


class CoverageHintAssessment(StrictModel):
    clause_id: str
    disposition: CoverageHintDisposition
    requirement_ids: List[str] = Field(default_factory=list)
    reason: str = ""


class CoverageReview(StrictModel):
    missing_clauses: List[MissingClause] = Field(default_factory=list)
    partial_requirements: List[PartialRequirement] = Field(default_factory=list)
    hint_assessments: List[CoverageHintAssessment] = Field(default_factory=list)

    @property
    def complete(self) -> bool:
        if self.missing_clauses or self.partial_requirements:
            return False
        return all(
            item.disposition not in {"MISSING", "PARTIAL"}
            for item in self.hint_assessments
        )
