from copy import deepcopy

import pytest

from app.mandate_risk.catalogue import load_prebuilt_registry
from app.mandate_risk_v2.concept_knowledge import metric_concept_reference
from scripts.evaluate_mandate_recognition import evaluate


def gold():
    return {"annotations": [
        {"raw_row_id": 2, "metric_name": "Return", "expected": "MATCH", "evidence_ids": ["a"]},
        {"raw_row_id": 3, "metric_name": "Beta", "expected": "NO_MATCH", "evidence_ids": ["a"]},
        {"raw_row_id": 4, "metric_name": "Region", "expected": "NEEDS_ADJUDICATION", "evidence_ids": ["a"]},
    ], "evidence_sources": {"a": {"page": 1, "quote": "capital growth"}}}


def metric(row_id, name, level="DIRECT"):
    return {"metric": {"raw_row_id": row_id, "metric_name": name}, "requirements": [{
        "mapping_level": level, "mapping_evidence": [{"clause_id": "c0001", "page": 1,
                                                     "text": "The portfolio seeks capital growth."}],
    }]}


def test_reclassification_as_review_cannot_hide_false_positives_and_duplicates_do_not_inflate_recall():
    result = {"screened_metrics": [metric(2, "Return"), metric(2, "Return", "REVIEW"),
                                    metric(3, "Beta", "REVIEW"), metric(4, "Region")]}
    report = evaluate(result, gold())
    assert report["combined"]["tp"] == 1
    assert report["combined"]["fp"] == 1
    assert report["combined"]["precision"] == .5
    assert report["combined"]["recall"] == 1
    assert report["review"]["false_positive_ids"] == [3]
    assert report["selected_needs_adjudication_ids"] == [4]
    assert set(report["evidence_status_counts"]) == {"UNVERIFIED_WITHOUT_PDF"}


def test_empty_selection_counts_missed_metrics_and_handles_zero_denominators():
    report = evaluate({"screened_metrics": []}, gold())
    assert report["combined"]["false_negative_ids"] == [2]
    assert report["combined"]["precision"] is None
    assert report["combined"]["recall"] == 0
    assert report["combined"]["f1"] == 0
    empty_gold = {"annotations": [], "evidence_sources": {}}
    report = evaluate({"screened_metrics": []}, empty_gold)
    assert report["combined"]["precision"] is None
    assert report["combined"]["recall"] is None
    assert report["combined"]["f1"] is None


@pytest.mark.parametrize("error", ["missing", "fabricated", "wrong_page", "wrong_anchor"])
def test_source_evidence_is_not_assumed_correct(error):
    item = metric(2, "Return")
    quotes = item["requirements"][0]["mapping_evidence"]
    if error == "missing":
        quotes.clear()
    elif error == "fabricated":
        quotes[0]["text"] = "Invented requirement."
    elif error == "wrong_page":
        quotes[0]["page"] = 9
    else:
        quotes[0]["text"] = "Borrowing is forbidden."
    report = evaluate({"screened_metrics": [item]}, gold(),
                      pdf_pages={1: "The portfolio seeks capital growth. Borrowing is forbidden."})
    assert "SOURCE_AND_ANCHOR_VERIFIED" not in report["evidence_status_counts"]


def test_unclassified_selection_still_counts_as_a_false_positive():
    item = metric(3, "Beta")
    item["requirements"] = []
    report = evaluate({"screened_metrics": [item]}, gold())
    assert report["combined"]["false_positive_ids"] == [3]
    assert report["unclassified_selected_ids"] == [3]
    assert report["evidence_status_counts"] == {"MISSING_EVIDENCE": 1}


@pytest.mark.parametrize("payload", [
    {"event": "run.failed", "error": "provider failure"}, {},
    {"screened_metrics": [metric(99, "Unknown")]},
    {"screened_metrics": [metric(2, "Renamed concept")]},
])
def test_failed_runs_unknown_metrics_and_changed_identities_are_not_scored_as_success(payload):
    with pytest.raises(ValueError):
        evaluate(payload, gold())


def test_metric_reference_cannot_survive_a_reused_row_id_or_changed_algorithm():
    row = load_prebuilt_registry().get(12)
    assert row is not None
    reference = metric_concept_reference(row)
    assert reference is not None
    for update in ({"metric_name": "Different concept"}, {"algorithm": "Var(Rp)"}, {"row_id": 999}):
        assert metric_concept_reference(row.model_copy(update=update)) is None
    # A consumer mutating a reference must not change future recognition calls.
    original = deepcopy(reference)
    reference["aliases"].append("incorrect alias")
    assert metric_concept_reference(row) == original
