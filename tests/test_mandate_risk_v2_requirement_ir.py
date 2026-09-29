import pytest

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk_v2.coverage import build_coverage_hints, validate_coverage_review
from app.mandate_risk_v2.extractor import (
    build_requirement_ir,
    canonical_evidence,
    chunk_clauses,
    validate_extraction_payload,
)
from app.mandate_risk_v2.prompts import EXTRACTION_SYSTEM_PROMPT, build_extraction_prompt


def test_extraction_prompt_is_document_understanding_first():
    clauses = split_document_clauses("[Page 1]\nThe portfolio shall keep liquidity above 8% of NAV.")
    prompt = build_extraction_prompt(document_name="synthetic.pdf", clauses=clauses)
    assert "Input clauses" in prompt
    assert "Risk Metric" not in prompt
    assert "Candidate metrics" not in prompt
    assert "不要猜测、发明或推荐正式指标名称" in EXTRACTION_SYSTEM_PROMPT
    assert "raw_value_text" in prompt
    assert "value_to" in prompt


def test_covered_hint_rejects_any_referenced_requirement_without_its_clause():
    clauses = split_document_clauses("[Page 1]\nA shall not exceed 10%.\n\nB shall not exceed 20%.")
    payload = {"requirements": [
        {"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT", "semantic_summary": "A limit",
         "evidence": {"clause_ids": [clauses[0].clause_id]}},
        {"local_id": "r2", "requirement_type": "QUANTITATIVE_LIMIT", "semantic_summary": "B limit",
         "evidence": {"clause_ids": [clauses[1].clause_id]}},
    ], "definitions": [], "contextual_facts": []}
    ir = build_requirement_ir(document_name="synthetic.pdf",
        batches=[validate_extraction_payload(payload, allowed_clauses=clauses)])
    review = {"missing_clauses": [], "partial_requirements": [], "hint_assessments": [
        {"clause_id": clauses[0].clause_id, "disposition": "COVERED",
         "requirement_ids": ["REQ-0001", "REQ-0002"], "reason": "mixed references"}]}
    with pytest.raises(ValueError, match="do not cite that clause"):
        validate_coverage_review(review, clauses=clauses, requirement_ir=ir,
            expected_hint_clause_ids=[clauses[0].clause_id])


def test_extraction_rejects_unknown_clause_id():
    clauses = split_document_clauses("[Page 1]\nThe portfolio shall keep liquidity above 8% of NAV.")
    payload = {"requirements": [{"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
        "semantic_summary": "Liquidity must remain above 8% of NAV.",
        "evidence": {"clause_ids": ["invented-clause"]}}], "definitions": [], "contextual_facts": []}
    with pytest.raises(ValueError, match="unknown clause_id"):
        validate_extraction_payload(payload, allowed_clauses=clauses)


def test_measurement_object_preserves_multiple_objects_without_python_merge():
    clauses = split_document_clauses("[Page 1]\nAssets may include public credit and cash equivalents.")
    payload = {"requirements": [{"local_id": "r1", "requirement_type": "SCOPE",
        "semantic_summary": "Permitted assets", "measurement": {"concept": "asset exposure",
        "object": ["public credit", "cash equivalents"], "qualifiers": {}},
        "evidence": {"clause_ids": [clauses[0].clause_id]}}], "definitions": [], "contextual_facts": []}
    batch = validate_extraction_payload(payload, allowed_clauses=clauses)
    assert batch.requirements[0].measurement.object == ["public credit", "cash equivalents"]


def test_definition_remains_definition_and_evidence_is_python_owned():
    document = ("[Page 1]\n“Liquidity Buffer” means assets convertible to cash within five business days.\n\n"
                "[Page 2]\nThe portfolio shall maintain a Liquidity Buffer of at least 12% of NAV.")
    clauses = split_document_clauses(document)
    payload = {"requirements": [{"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
        "semantic_summary": "Maintain a liquidity buffer of at least 12% of NAV.",
        "constraint": {"operator": ">=", "value": 12, "unit": "%", "raw_value_text": "at least 12%"},
        "evidence": {"clause_ids": [clauses[1].clause_id]}}],
        "definitions": [{"local_id": "d1", "term": "Liquidity Buffer",
        "semantic_summary": "Assets convertible to cash within five business days.",
        "evidence": {"clause_ids": [clauses[0].clause_id]}}], "contextual_facts": []}
    batch = validate_extraction_payload(payload, allowed_clauses=clauses)
    ir = build_requirement_ir(document_name="synthetic.pdf", batches=[batch])
    assert len(ir.requirements) == 1 and len(ir.definitions) == 1
    evidence = canonical_evidence(ir.requirements[0].evidence.clause_ids, clauses)
    assert evidence[0].text == clauses[1].text and evidence[0].page == 2
    assert evidence[0].source_start == clauses[1].source_start
    assert evidence[0].source_end == clauses[1].source_end


def test_conditional_branches_are_preserved_as_distinct_requirements():
    document = ("[Page 1]\nIf vehicle NAV is below USD 50 million, exposure shall not exceed USD 5 million.\n\n"
                "If vehicle NAV is USD 50 million or more, exposure shall not exceed 15% of vehicle NAV.")
    clauses = split_document_clauses(document)
    payload = {"requirements": [
        {"local_id": "r1", "requirement_type": "CONDITIONAL_RULE",
         "semantic_summary": "Below USD 50m NAV, exposure is capped at USD 5m.",
         "conditions": [{"left": "vehicle NAV", "operator": "<", "right": "USD 50 million"}],
         "constraint": {"operator": "<=", "value": 5, "unit": "USD million", "raw_value_text": "USD 5 million"},
         "evidence": {"clause_ids": [clauses[0].clause_id]}},
        {"local_id": "r2", "requirement_type": "CONDITIONAL_RULE",
         "semantic_summary": "At or above USD 50m NAV, exposure is capped at 15% of NAV.",
         "conditions": [{"left": "vehicle NAV", "operator": ">=", "right": "USD 50 million"}],
         "constraint": {"operator": "<=", "value": 15, "unit": "% of vehicle NAV", "raw_value_text": "15%"},
         "evidence": {"clause_ids": [clauses[1].clause_id]}},
    ], "definitions": [], "contextual_facts": []}
    batch = validate_extraction_payload(payload, allowed_clauses=clauses)
    ir = build_requirement_ir(document_name="branching.pdf", batches=[batch])
    assert len(ir.requirements) == 2
    assert [x.constraint.value for x in ir.requirements] == [5, 15]
    assert [x.conditions[0].operator for x in ir.requirements] == ["<", ">="]


def test_constraint_range_and_source_provenance_are_fail_closed():
    clauses = split_document_clauses("[Page 1]\nEquity exposure shall remain between 20% and 40% of NAV.")
    base = {"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
        "semantic_summary": "Equity exposure range", "constraint": {"operator": "BETWEEN",
        "value": 20, "value_to": 40, "unit": "%", "raw_value_text": "between 20% and 40%"},
        "evidence": {"clause_ids": [clauses[0].clause_id]}}
    batch = validate_extraction_payload({"requirements": [base], "definitions": [], "contextual_facts": []},
                                        allowed_clauses=clauses)
    assert batch.requirements[0].constraint.value_to == 40
    invalid = {**base, "constraint": {**base["constraint"], "value_to": 50}}
    with pytest.raises(ValueError, match="value_to is not present"):
        validate_extraction_payload({"requirements": [invalid], "definitions": [], "contextual_facts": []},
                                    allowed_clauses=clauses)


def test_overlap_only_exact_duplicate_is_deduped():
    clauses = split_document_clauses("[Page 1]\nA shall remain below 10%.\n\nB shall remain below 20%.\n\nC shall remain below 30%.")
    windows = chunk_clauses(clauses, max_clauses=2, overlap=1)
    duplicate_payload = {"requirements": [{"local_id": "r1", "requirement_type": "QUANTITATIVE_LIMIT",
        "semantic_summary": "B shall remain below 20%.", "evidence": {"clause_ids": [clauses[1].clause_id]}}],
        "definitions": [], "contextual_facts": []}
    batch1 = validate_extraction_payload(duplicate_payload, allowed_clauses=windows[0])
    batch2 = validate_extraction_payload(duplicate_payload, allowed_clauses=windows[1])
    ir = build_requirement_ir(document_name="overlap.pdf", batches=[batch1, batch2])
    assert len(ir.requirements) == 1 and ir.requirements[0].requirement_id == "REQ-0001"


def test_coverage_audits_every_clause_and_percent_is_a_high_risk_signal():
    clauses = split_document_clauses("[Page 1]\nIf NAV is below USD 40 million, exposure shall not exceed 12%.\n\nThe portfolio seeks long-term value creation.")
    hints = build_coverage_hints(clauses)
    assert [item["clause_id"] for item in hints] == [clauses[0].clause_id, clauses[1].clause_id]
    assert set(hints[0]["signals"]) == {"numeric_or_unit", "comparison_or_threshold",
        "obligation_or_prohibition", "condition_or_exception"}
    assert hints[0]["priority"] == "high"
    assert hints[1]["signals"] == [] and hints[1]["priority"] == "normal"
    percent_only = build_coverage_hints(split_document_clauses("[Page 1]\nAllocation: 0.5%."))[0]
    assert "numeric_or_unit" in percent_only["signals"]
    assert "metric" not in hints[0] and "requirement_type" not in hints[0]


def test_coverage_review_rejects_untrusted_references():
    clauses = split_document_clauses("[Page 1]\nThe portfolio shall maintain at least 10% in liquid assets.")
    batch = validate_extraction_payload({"requirements": [{"local_id": "r1",
        "requirement_type": "QUANTITATIVE_LIMIT", "semantic_summary": "Maintain at least 10% in liquid assets.",
        "evidence": {"clause_ids": [clauses[0].clause_id]}}], "definitions": [], "contextual_facts": []},
        allowed_clauses=clauses)
    ir = build_requirement_ir(document_name="coverage.pdf", batches=[batch])
    with pytest.raises(ValueError, match="unknown missing clause_id"):
        validate_coverage_review({"missing_clauses": [{"clause_id": "invented", "reason": "missing branch"}],
            "partial_requirements": []}, clauses=clauses, requirement_ir=ir)
    with pytest.raises(ValueError, match="unknown requirement_id"):
        validate_coverage_review({"missing_clauses": [], "partial_requirements": [{"requirement_id": "REQ-9999",
            "reason": "partial", "related_clause_ids": [clauses[0].clause_id]}]},
            clauses=clauses, requirement_ir=ir)
