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

    assert len(result.selected_metrics) == 1
    assert result.selected_metrics[0].evidence[0].page == 2
    assert result.selected_metrics[0].evidence[0].text == "The portfolio has low Tracking Error."
