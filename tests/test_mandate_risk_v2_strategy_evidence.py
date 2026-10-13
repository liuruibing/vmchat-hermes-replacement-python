from __future__ import annotations

import json
import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk_v2.result import MatchedMetricResult, MetricReference
from app.mandate_risk_v2.strategy_evidence import StrategyEvidencePipeline


CLAUSES = [
    DocumentClause(clause_id="c0001", page=1, text="The fund aims for long term capital growth by investing in equity and bonds.", source_start=0, source_end=74),
    DocumentClause(clause_id="c0002", page=2, text="Maintain at least 15% liquid assets at all times for redemption requirements.", source_start=75, source_end=153),
    DocumentClause(clause_id="c0003", page=3, text="Tracking error shall not exceed 3% relative to benchmark.", source_start=154, source_end=212),
]


def make_metric(row_id: int, name: str) -> MatchedMetricResult:
    return MatchedMetricResult(
        metric=MetricReference(
            raw_row_id=row_id,
            source_row=row_id,
            metric_name=name,
            algorithm=f"algo_{row_id}",
        ),
        match_score=90,
        score_reason="screened metric",
    )


class MockProvider:
    def __init__(self, responses: list[dict]):
        self.responses = responses
        self.calls = []

    async def run_skill(self, request):
        self.calls.append(request)
        response = self.responses[min(len(self.calls) - 1, len(self.responses) - 1)]
        yield type("Chunk", (), {"contentDelta": json.dumps(response), "usage": {"total_tokens": 12}})()


@pytest.mark.anyio
async def test_provenance_validation_rejects_unknown_clause_ids():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # invalid clause_id "c9999"
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c9999"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"]
            }]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_empty_point_evidence_clause_ids_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # empty point evidence_clause_ids
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": [],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"]
            }]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )


@pytest.mark.anyio
async def test_empty_metric_link_evidence_clause_ids_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # empty link evidence_clause_ids
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": []
            }]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )


@pytest.mark.anyio
async def test_metric_membership_validation_rejects_unknown_raw_row_ids():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # row_id 999 is not in displayed metrics
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 999,
                "basis": "EXPLICIT",
                "reason": "未知指标ID",
                "evidence_clause_ids": ["c0002"]
            }]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_duplicate_same_point_links_are_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # metric link row_id 2 appears twice in the same strategy point
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [
                {"raw_row_id": 2, "basis": "EXPLICIT", "reason": "理由1", "evidence_clause_ids": ["c0002"]},
                {"raw_row_id": 2, "basis": "INFERRED", "reason": "理由2", "evidence_clause_ids": ["c0002"]},
            ]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_same_window_contradiction_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # metric 2 is linked in point AND listed in unlinked_metrics in same batch
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [
                {"raw_row_id": 2, "basis": "EXPLICIT", "reason": "理由1", "evidence_clause_ids": ["c0002"]}
            ]
        }],
        "unlinked_metrics": [
            {"raw_row_id": 2, "reason": "未找到关联"}
        ]
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )


@pytest.mark.anyio
async def test_omitted_metric_in_window_rejected():
    displayed = [make_metric(2, "Liquidity Ratio"), make_metric(3, "Tracking Error")]
    # model omits metric 3 from both points and unlinked_metrics
    provider = MockProvider([{
        "sections": [],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [
                {"raw_row_id": 2, "basis": "EXPLICIT", "reason": "理由1", "evidence_clause_ids": ["c0002"]}
            ]
        }],
        "unlinked_metrics": []
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )


@pytest.mark.anyio
async def test_point_deduplication_merges_different_links():
    displayed = [make_metric(2, "Liquidity Ratio"), make_metric(3, "Tracking Error")]
    # Draft 1: point A links row 2. Draft 2: point A links row 3.
    # Merges links under point A, row 2 and 3 are linked in points, unlinked is empty.
    resp = {
        "sections": [
            {"category": "investment_strategy", "title": "综合风控", "evidence_clause_ids": ["c0001"]}
        ],
        "points": [
            {
                "title": "综合风控要点",
                "summary": "涵盖流动性与跟踪误差",
                "evidence_clause_ids": ["c0001"],
                "metric_links": [{"raw_row_id": 2, "basis": "EXPLICIT", "reason": "流动性限制", "evidence_clause_ids": ["c0001"]}]
            },
            {
                "title": "综合风控要点",
                "summary": "涵盖流动性与跟踪误差",
                "evidence_clause_ids": ["c0001"],
                "metric_links": [{"raw_row_id": 3, "basis": "INFERRED", "reason": "跟踪误差约束", "evidence_clause_ids": ["c0001"]}]
            }
        ],
        "unlinked_metrics": []
    }
    provider = MockProvider([resp])
    result, usage = await StrategyEvidencePipeline().run(
        document_name="dedup.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert len(result.points) == 1
    assert {link.raw_row_id for link in result.points[0].metric_links} == {2, 3}
    assert result.unlinked_metrics == []


@pytest.mark.anyio
async def test_cross_window_link_priority_overrides_earlier_unlinked_disposition():
    displayed = [make_metric(2, "Liquidity Ratio"), make_metric(3, "Tracking Error")]
    # Window 1 (c0001): row 2 and row 3 are unlinked
    window1_resp = {
        "sections": [{"category": "investment_strategy", "title": "投资目标", "evidence_clause_ids": ["c0001"]}],
        "points": [{
            "title": "长期资本增值目标",
            "summary": "主要投资于股票和债券",
            "evidence_clause_ids": ["c0001"],
            "metric_links": []
        }],
        "unlinked_metrics": [
            {"raw_row_id": 2, "reason": "窗口1未包含流动性量化限制"},
            {"raw_row_id": 3, "reason": "窗口1未包含跟踪误差限制"}
        ]
    }
    # Window 2 (c0002): row 2 linked (EXPLICIT c0002), row 3 unlinked
    window2_resp = {
        "sections": [{"category": "instruments", "title": "流动性管理", "evidence_clause_ids": ["c0002"]}],
        "points": [
            {
                "title": "流动性管理要求",
                "summary": "维持至少15%流动性资产",
                "evidence_clause_ids": ["c0002"],
                "metric_links": [{"raw_row_id": 2, "basis": "EXPLICIT", "reason": "明确15%流动性要求", "evidence_clause_ids": ["c0002"]}]
            }
        ],
        "unlinked_metrics": [
            {"raw_row_id": 3, "reason": "窗口2未包含跟踪误差限制"}
        ]
    }
    # Window 3 (c0003): row 3 linked (EXPLICIT c0003), row 2 unlinked
    window3_resp = {
        "sections": [{"category": "benchmark", "title": "跟踪误差控制", "evidence_clause_ids": ["c0003"]}],
        "points": [
            {
                "title": "跟踪误差控制",
                "summary": "跟踪误差不超过3%",
                "evidence_clause_ids": ["c0003"],
                "metric_links": [{"raw_row_id": 3, "basis": "EXPLICIT", "reason": "明确跟踪误差上限", "evidence_clause_ids": ["c0003"]}]
            }
        ],
        "unlinked_metrics": [
            {"raw_row_id": 2, "reason": "窗口3未包含流动性限制"}
        ]
    }
    provider = MockProvider([window1_resp, window2_resp, window3_resp])
    pipeline = StrategyEvidencePipeline(document_window_chars=120)

    result, usage = await pipeline.run(
        document_name="multi_window.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert usage["document_windows"] == 3
    assert len(result.points) == 3
    # Rows 2 and 3 were linked in window 2 & 3 respectively, so they MUST NOT be in unlinked_metrics!
    assert result.unlinked_metrics == []
    linked_ids = {link.raw_row_id for pt in result.points for link in pt.metric_links}
    assert linked_ids == {2, 3}


@pytest.mark.anyio
async def test_empty_selected_metrics_returns_points_with_zero_links_and_empty_unlinked():
    displayed = []
    provider = MockProvider([{
        "sections": [{"category": "investment_strategy", "title": "投资策略与风格", "evidence_clause_ids": ["c0001"]}],
        "points": [{
            "title": "投资策略与风格",
            "summary": "长期资本增值策略",
            "evidence_clause_ids": ["c0001"],
            "metric_links": []
        }],
        "unlinked_metrics": []
    }])

    result, usage = await StrategyEvidencePipeline().run(
        document_name="empty_metrics.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert len(result.points) == 1
    assert result.points[0].metric_links == []
    assert result.unlinked_metrics == []


@pytest.mark.anyio
async def test_omitted_sections_field_in_batch_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # Payload omits "sections" key entirely
    provider = MockProvider([{
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"],
            }],
        }],
        "unlinked_metrics": [],
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_unknown_evidence_clause_in_section_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    provider = MockProvider([{
        "sections": [{
            "category": "instruments",
            "title": "投资范围",
            "evidence_clause_ids": ["c9999"],
        }],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"],
            }],
        }],
        "unlinked_metrics": [],
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_empty_evidence_in_section_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    provider = MockProvider([{
        "sections": [{
            "category": "instruments",
            "title": "投资范围",
            "evidence_clause_ids": [],
        }],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"],
            }],
        }],
        "unlinked_metrics": [],
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_empty_title_in_section_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    provider = MockProvider([{
        "sections": [{
            "category": "instruments",
            "title": "   ",
            "evidence_clause_ids": ["c0001"],
        }],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"],
            }],
        }],
        "unlinked_metrics": [],
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_invalid_category_in_section_rejected():
    displayed = [make_metric(2, "Liquidity Ratio")]
    provider = MockProvider([{
        "sections": [{
            "category": "invalid_category",
            "title": "非法分类",
            "evidence_clause_ids": ["c0001"],
        }],
        "points": [{
            "title": "流动性要求",
            "summary": "维持充足流动性",
            "evidence_clause_ids": ["c0002"],
            "metric_links": [{
                "raw_row_id": 2,
                "basis": "EXPLICIT",
                "reason": "明确流动性要求",
                "evidence_clause_ids": ["c0002"],
            }],
        }],
        "unlinked_metrics": [],
    }])
    with pytest.raises(ValueError, match="STRATEGY_EVIDENCE_INVALID"):
        await StrategyEvidencePipeline().run(
            document_name="test.pdf",
            clauses=CLAUSES,
            displayed_metrics=displayed,
            provider=provider,
        )
    assert len(provider.calls) == 2


@pytest.mark.anyio
async def test_sections_can_exist_without_metric_links_and_accept_arbitrary_headings():
    displayed = [make_metric(2, "Liquidity Ratio")]
    # Section exists with arbitrary heading in English and Chinese, without any metric link
    provider = MockProvider([{
        "sections": [
            {"category": "instruments", "title": "Investment Scope & Permissible Instruments", "evidence_clause_ids": ["c0001"]},
            {"category": "benchmark", "title": "基准配置与偏离约束 (Benchmark & Deviations)", "evidence_clause_ids": ["c0003"]},
        ],
        "points": [],
        "unlinked_metrics": [
            {"raw_row_id": 2, "reason": "未在策略要点中关联"},
        ],
    }])
    result, usage = await StrategyEvidencePipeline().run(
        document_name="arbitrary.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert len(result.sections) == 2
    assert result.sections[0].section_id == "DS-0001"
    assert result.sections[0].category == "instruments"
    assert result.sections[0].title == "Investment Scope & Permissible Instruments"
    assert result.sections[0].evidence[0].clause_id == "c0001"
    assert result.sections[0].evidence[0].text == CLAUSES[0].text
    assert result.sections[0].evidence[0].page == 1
    assert result.sections[1].section_id == "DS-0002"
    assert result.sections[1].category == "benchmark"
    assert result.sections[1].title == "基准配置与偏离约束 (Benchmark & Deviations)"
    assert result.sections[1].evidence[0].clause_id == "c0003"
    assert result.points == []
    assert len(result.unlinked_metrics) == 1


@pytest.mark.anyio
async def test_references_and_sections_ordered_by_document_source_order():
    displayed = []
    # Draft provided clauses in reverse order inside section, and sections in reverse category order
    provider = MockProvider([{
        "sections": [
            {"category": "benchmark", "title": "尾部章节：基准约束", "evidence_clause_ids": ["c0003"]},
            {"category": "instruments", "title": "头部章节：投资目标与流动性", "evidence_clause_ids": ["c0002", "c0001"]},
        ],
        "points": [],
        "unlinked_metrics": [],
    }])
    result, usage = await StrategyEvidencePipeline().run(
        document_name="order.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert len(result.sections) == 2
    assert result.sections[0].section_id == "DS-0001"
    assert result.sections[0].category == "instruments"
    assert result.sections[0].title == "头部章节：投资目标与流动性"
    # Within the section, references must be sorted by source_start (c0001 before c0002)
    assert [ev.clause_id for ev in result.sections[0].evidence] == ["c0001", "c0002"]
    assert result.sections[1].section_id == "DS-0002"
    assert result.sections[1].category == "benchmark"
    assert result.sections[1].title == "尾部章节：基准约束"
    assert [ev.clause_id for ev in result.sections[1].evidence] == ["c0003"]


@pytest.mark.anyio
async def test_multiwindow_merge_by_category_deduplicates_clauses_and_preserves_source_title():
    displayed = []
    # Window 1 (c0001): section "investment_strategy" with c0001
    w1 = {
        "sections": [
            {"category": "investment_strategy", "title": "投资策略与风格", "evidence_clause_ids": ["c0001"]},
        ],
        "points": [],
        "unlinked_metrics": [],
    }
    # Window 2 (c0002): section "instruments" with c0002
    w2 = {
        "sections": [
            {"category": "instruments", "title": "流动性与标的范围", "evidence_clause_ids": ["c0002"]},
        ],
        "points": [],
        "unlinked_metrics": [],
    }
    # Window 3 (c0003): section "investment_strategy" with duplicate c0003
    # Also contains "benchmark" with c0003
    w3 = {
        "sections": [
            {"category": "investment_strategy", "title": "选股与交易策略", "evidence_clause_ids": ["c0003", "c0003"]},
            {"category": "benchmark", "title": "业绩基准约束", "evidence_clause_ids": ["c0003"]},
        ],
        "points": [],
        "unlinked_metrics": [],
    }
    provider = MockProvider([w1, w2, w3])
    pipeline = StrategyEvidencePipeline(document_window_chars=120)
    result, usage = await pipeline.run(
        document_name="multi_merge.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    # "investment_strategy" from w1 and w3 merge into one section!
    # Duplicate c0003 removed; cross-window evidence combined and sorted [c0001, c0003].
    # Category order: instruments, benchmark, investment_strategy.
    assert len(result.sections) == 3
    categories = [s.category for s in result.sections]
    assert categories == ["instruments", "benchmark", "investment_strategy"]
    titles = [s.title for s in result.sections]
    assert titles == ["流动性与标的范围", "业绩基准约束", "投资策略与风格"]
    assert result.sections[0].section_id == "DS-0001"
    assert [ev.clause_id for ev in result.sections[0].evidence] == ["c0002"]
    assert result.sections[1].section_id == "DS-0002"
    assert [ev.clause_id for ev in result.sections[1].evidence] == ["c0003"]
    assert result.sections[2].section_id == "DS-0003"
    assert [ev.clause_id for ev in result.sections[2].evidence] == ["c0001", "c0003"]


@pytest.mark.anyio
async def test_missing_required_categories_truthfully_omitted_without_invented_sections():
    displayed = []
    # PDF only has Permitted Instruments, benchmark and investment_strategy are truthfully absent
    provider = MockProvider([{
        "sections": [
            {"category": "instruments", "title": "Permitted Instruments Only", "evidence_clause_ids": ["c0001"]},
        ],
        "points": [],
        "unlinked_metrics": [],
    }])
    result, usage = await StrategyEvidencePipeline().run(
        document_name="missing_categories.pdf",
        clauses=CLAUSES,
        displayed_metrics=displayed,
        provider=provider,
    )
    assert len(result.sections) == 1
    assert result.sections[0].category == "instruments"
    assert result.sections[0].section_id == "DS-0001"
    assert result.sections[0].title == "Permitted Instruments Only"
    assert [ev.clause_id for ev in result.sections[0].evidence] == ["c0001"]
