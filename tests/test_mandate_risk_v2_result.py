import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingResult
from app.mandate_risk_v2.mapping_models import (
    CompatibilityDimension,
    CriticReview,
    FinalMappingReview,
    MappingLink,
    RequirementDestination,
    RequirementDisposition,
)
from app.mandate_risk_v2.models import (
    EvidenceRef,
    Requirement,
    RequirementConstraint,
    RequirementIR,
    RequirementMeasurement,
)
from app.mandate_risk_v2.report import render_v2_report
from app.mandate_risk_v2.result import build_v2_analysis_result


def _compatibility():
    return [
        CompatibilityDimension(
            dimension="measurement_object",
            requirement_basis="portfolio liquidity",
            metric_basis="liquid assets",
            relation="EQUIVALENT",
            reason="same measurement object",
        )
    ]


def _fixture():
    clauses = [
        DocumentClause(
            clause_id="c0001",
            text="The portfolio shall maintain at least 7% liquidity.",
            page=3,
            source_start=10,
            source_end=62,
        ),
        DocumentClause(
            clause_id="c0002",
            text="The portfolio shall not exceed 12% in the same liquidity bucket.",
            page=4,
            source_start=63,
            source_end=130,
        ),
    ]
    requirements = [
        Requirement(
            requirement_id="REQ-0001",
            requirement_type="QUANTITATIVE_LIMIT",
            semantic_summary="Maintain at least 7% portfolio liquidity.",
            measurement=RequirementMeasurement(
                concept="liquidity",
                object="portfolio liquidity",
            ),
            constraint=RequirementConstraint(
                operator=">=",
                value=7,
                unit="%",
                raw_value_text="at least 7%",
            ),
            evidence=EvidenceRef(clause_ids=["c0001"]),
        ),
        Requirement(
            requirement_id="REQ-0002",
            requirement_type="QUANTITATIVE_LIMIT",
            semantic_summary="Cap the same liquidity bucket at 12%.",
            measurement=RequirementMeasurement(
                concept="liquidity",
                object="portfolio liquidity",
            ),
            constraint=RequirementConstraint(
                operator="<=",
                value=12,
                unit="%",
                raw_value_text="not exceed 12%",
                attributes={"time_basis": "ongoing"},
            ),
            evidence=EvidenceRef(clause_ids=["c0002"]),
        ),
    ]
    ir = RequirementIR(document_name="limits.pdf", requirements=requirements)
    registry = RawRiskMetricRegistry(
        [
            RawRiskMetric(
                row_id=2,
                source_row=2,
                metric_name="Synthetic Liquidity Metric",
                algorithm="liquid assets / NAV",
                mandate="portfolio liquidity",
                strategy_type="混合",
                effective_risk_type_1="流动性风险",
                effective_risk_type_2="流动性",
            )
        ],
        source_path="/tmp/risk_metrics.raw.csv",
        source_sha256="abc123",
    )
    links = [
        MappingLink(
            requirement_id=requirement.requirement_id,
            raw_row_id=2,
            level="DIRECT",
            compatibility=_compatibility(),
            evidence_clause_ids=requirement.evidence.clause_ids,
            reason="directly equivalent",
        )
        for requirement in requirements
    ]
    dispositions = FinalMappingReview(
        dispositions=[
            RequirementDisposition(
                requirement_id=requirement.requirement_id,
                reason="confirmed",
                destinations=[
                    RequirementDestination(
                        destination="MAIN_TABLE",
                        raw_row_ids=[2],
                        evidence_clause_ids=requirement.evidence.clause_ids,
                        aspect="liquidity",
                        reason="direct mapping",
                    )
                ],
            )
            for requirement in requirements
        ]
    )
    mapping = MappingResult(
        links=links,
        dispositions=dispositions,
        critic=CriticReview(verdicts=[]),
        usage={"complete": True, "total_tokens": 0},
    )
    return ir, clauses, registry, mapping


def test_structured_result_preserves_many_requirements_for_one_metric():
    ir, clauses, registry, mapping = _fixture()
    result = build_v2_analysis_result(
        ir=ir,
        clauses=clauses,
        registry=registry,
        mapping=mapping,
    )

    assert result.document_name == "limits.pdf"
    assert result.coverage_status == "complete"
    assert result.metric_catalogue_name == "risk_metrics.raw.csv"
    assert len(result.requirements) == 2
    assert len(result.matched_metrics) == 1
    assert [
        item.requirement.requirement.requirement_id
        for item in result.matched_metrics[0].requirements
    ] == ["REQ-0001", "REQ-0002"]
    assert result.matched_metrics[0].requirements[0].requirement.evidence[0].page == 3
    assert result.matched_metrics[0].requirements[1].requirement.requirement.constraint.value == 12
    assert result.unresolved_requirements == []


def test_report_keeps_six_column_contract_and_renders_requirement_constraints():
    ir, clauses, registry, mapping = _fixture()
    markdown = render_v2_report(
        ir=ir,
        clauses=clauses,
        registry=registry,
        mapping=mapping,
    )

    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in markdown
    assert "Synthetic Liquidity Metric" in markdown
    assert "Maintain at least 7% portfolio liquidity." in markdown
    assert "Cap the same liquidity bucket at 12%." in markdown
    assert "结构化约束：`>= 7%`" in markdown
    assert "结构化约束：`<= 12%`" in markdown
    assert "原始范围表达：`at least 7%`" in markdown
    assert "Constraint qualifiers：`{\"time_basis\":\"ongoing\"}`" in markdown
    assert "The portfolio shall maintain at least 7% liquidity.（第 3 页）" in markdown
    assert "主表“值”表示实际组合值" in markdown


@pytest.mark.parametrize("destination", ["PENDING_REVIEW", "LIBRARY_GAP"])
def test_metric_keeps_review_requirement_when_another_requirement_is_direct(destination):
    ir, clauses, registry, mapping = _fixture()
    review_link = mapping.links[1]
    review_link.level = "REVIEW"
    review_link.reason = "Relevant monitoring purpose; the upper-limit basis needs confirmation."
    review_link.compatibility[0].relation = "INSUFFICIENT"
    review_link.compatibility[0].reason = "Upper-limit measurement basis needs confirmation."
    review_destination = mapping.dispositions.dispositions[1].destinations[0]
    review_destination.destination = destination
    review_destination.reason = "No confirmed algorithm for the upper limit."
    if destination == "LIBRARY_GAP":
        review_destination.raw_row_ids = []

    result = build_v2_analysis_result(
        ir=ir, clauses=clauses, registry=registry, mapping=mapping,
    )
    assert len(result.matched_metrics) == 1
    assert len(result.candidate_metrics) == 1
    formal = result.matched_metrics[0]
    candidate = result.candidate_metrics[0]
    assert formal.metric.raw_row_id == candidate.metric.raw_row_id == 2
    assert [link.requirement.requirement.requirement_id for link in formal.requirements] == ["REQ-0001"]
    assert [link.mapping_level for link in formal.requirements] == ["DIRECT"]
    assert [link.requirement.requirement.requirement_id for link in candidate.requirements] == ["REQ-0002"]
    assert candidate.requirements[0].mapping_level == "REVIEW"
    assert candidate.requirements[0].mapping_reason == review_link.reason
    assert candidate.requirements[0].mapping_evidence[0].page == 4

    report = render_v2_report(
        ir=ir, clauses=clauses, registry=registry, mapping=mapping, analysis=result,
    )
    main_table = report.split("## 筛选结果", 1)[1].split("## 指标匹配依据", 1)[0]
    assert clauses[0].text in main_table
    assert clauses[1].text in main_table
    assert len(result.screened_metrics) == 1
    assert len(result.screened_metrics[0].requirements) == 2
    assert review_link.reason in report
    assert review_link.compatibility[0].reason in report
