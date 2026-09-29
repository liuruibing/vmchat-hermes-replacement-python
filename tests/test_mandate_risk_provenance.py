from pathlib import Path

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.validator import validate_model_result


ROOT = Path(__file__).resolve().parents[1]
METRICS = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw" / "risk_metrics.raw.csv"


def test_page_markers_are_provenance_not_clause_content():
    document_text = (
        "[Page 1]\nFirst sentence.\n\n"
        "[Page 2]\nThe portfolio has low Tracking Error."
    )

    clauses = split_document_clauses(document_text)

    assert [item.page for item in clauses] == [1, 2]
    assert clauses[0].text == "First sentence."
    assert clauses[1].text == "The portfolio has low Tracking Error."
    assert all("[Page " not in item.text for item in clauses)


def test_section_numbers_are_kept_with_their_requirement():
    document_text = (
        "[Page 4]\n6.\nNew purchases shall target a spread of 10 bps.\n\n"
        "[Page 6]\n9.8.\nThe exposure to any single sector shall not exceed 100%."
    )

    clauses = split_document_clauses(document_text)

    assert [item.page for item in clauses] == [4, 6]
    assert clauses[0].text == "6.\nNew purchases shall target a spread of 10 bps."
    assert clauses[1].text == "9.8.\nThe exposure to any single sector shall not exceed 100%."
    assert all(document_text[item.source_start:item.source_end] == item.text for item in clauses)


def test_numbered_list_item_starts_a_new_clause_without_sentence_punctuation():
    document_text = (
        "[Page 7]\nsector<100%\n"
        "2) Liquidity of underlying assets: 1 day >0%, 7 days >0%"
    )

    clauses = split_document_clauses(document_text)

    assert [item.text for item in clauses] == [
        "sector<100%",
        "2) Liquidity of underlying assets: 1 day >0%, 7 days >0%",
    ]
    assert [item.page for item in clauses] == [7, 7]
    assert all(document_text[item.source_start:item.source_end] == item.text for item in clauses)


def test_printed_page_number_is_not_part_of_a_cross_page_clause_fragment():
    document_text = (
        "[Page 6]\n1) Diversification: single name <100%, top 10 <100%, single\n\n"
        "[Page 7]\nRepeated document header.\n\n7  \nsector<100%\n"
        "2) Liquidity: 1 day >0%, 7 days >0%"
    )

    clauses = split_document_clauses(document_text)
    sector = next(item for item in clauses if "sector<100%" in item.text)

    assert sector.text == "sector<100%"
    assert sector.page == 7
    assert document_text[sector.source_start:sector.source_end] == sector.text


def test_blank_paragraph_starts_a_new_clause_after_unpunctuated_limit():
    document_text = (
        "[Page 7]\n2) Liquidity of underlying assets: 1 day >0%, 7 days >0%\n \n"
        "The holdings in a single fund shall not exceed 100% of its assets."
    )

    clauses = split_document_clauses(document_text)

    assert [item.text for item in clauses] == [
        "2) Liquidity of underlying assets: 1 day >0%, 7 days >0%",
        "The holdings in a single fund shall not exceed 100% of its assets.",
    ]
    assert all(document_text[item.source_start:item.source_end] == item.text for item in clauses)


def test_validator_uses_python_page_and_ignores_model_page():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    document_text = (
        "[Page 1]\nIntroduction.\n\n"
        "[Page 2]\nThe portfolio has low Tracking Error."
    )
    clauses = split_document_clauses(document_text)
    evidence_clause = next(item for item in clauses if "Tracking Error" in item.text)

    payload = {
        "matches": [
            {
                "raw_row_id": tracking.row_id,
                "metric_name": tracking.metric_name,
                "match_level": "DIRECT",
                "confidence": 0.99,
                "reason": "Explicit tracking error requirement.",
                "evidence": [
                    {
                        "clause_id": evidence_clause.clause_id,
                        "text": "low Tracking Error",
                        "page": 999,
                    }
                ],
            }
        ],
        "gaps": [],
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[tracking.row_id],
        document_text=document_text,
        document_name="sample.pdf",
        strategy_type="权益",
        candidate_clause_ids={tracking.row_id: [evidence_clause.clause_id]},
    )

    assert result.selected_metrics == []
    assert len(result.review_metrics) == 1
    assert result.review_metrics[0].evidence[0].page == 2
    assert result.review_metrics[0].evidence[0].text == "The portfolio has low Tracking Error."


def test_numeric_gap_requires_quote_with_the_stated_number():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document_text = (
        "[Page 4]\nThe manager shall make relative value investments. "
        "New purchase yield should exceed the benchmark by 10 bps."
    )
    clauses = split_document_clauses(document_text)
    payload = {
        "summary": "已找到一个指标库缺口。",
        "gaps": [
            {
                "requirement": "新购收益率高于基准收益率 10bps",
                "reason": "No equivalent metric.",
                "evidence": [{"clause_id": clauses[0].clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[],
        document_text=document_text,
        document_name="fixed.pdf",
        strategy_type="固收",
    )

    assert result.library_gaps == []
    assert "一个指标库缺口" not in result.summary


def test_composite_gap_requires_each_distinct_numeric_unit():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    document_text = (
        "[Page 6]\nFor small funds the limit is RMB 100 million. "
        "For larger funds of RMB 1 billion the limit is 100%."
    )
    clauses = split_document_clauses(document_text)
    payload = {
        "gaps": [
            {
                "requirement": "RMB 1 billion: 100%; RMB 100 million for smaller funds",
                "evidence": [{"clause_id": clauses[1].clause_id}],
            }
        ]
    }

    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[],
        document_text=document_text,
        document_name="equity.pdf",
        strategy_type="权益",
    )

    assert result.library_gaps == []
