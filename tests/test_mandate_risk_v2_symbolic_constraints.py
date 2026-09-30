import pytest

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.extractor import validate_extraction_payload
from app.mandate_risk_v2.models import Requirement
from app.mandate_risk_v2.report import format_requirement_constraint


def payload():
    return {"requirements": [{"local_id": "r1", "requirement_type": "OBJECTIVE",
        "semantic_summary": "Returns should exceed the benchmark",
        "constraint": {"operator": ">", "value": None, "benchmark": "Reference Index",
            "raw_value_text": "returns exceeding the Reference Index"},
        "evidence": {"clause_ids": ["c0001"]}}]}


def test_symbolic_comparison_preserves_benchmark_without_inventing_a_numeric_target():
    clauses = [DocumentClause(clause_id="c0001", text="Seek returns exceeding the Reference Index.", page=1)]
    batch = validate_extraction_payload(payload(), allowed_clauses=clauses)
    assert batch.requirements[0].constraint.value is None
    requirement = Requirement(requirement_id="REQ-0001", **batch.requirements[0].model_dump(exclude={"local_id"}))
    assert format_requirement_constraint(requirement) == "> Reference Index"


def test_symbolic_comparison_rejects_an_ungrounded_benchmark():
    invalid = payload()
    invalid["requirements"][0]["constraint"]["benchmark"] = "Invented Reference"
    with pytest.raises(ValueError, match="benchmark.*evidence"):
        validate_extraction_payload(invalid, allowed_clauses=[DocumentClause(
            clause_id="c0001", text="Seek returns exceeding the Reference Index.")])


def test_numeric_comparison_still_requires_a_value_or_grounded_symbolic_bound():
    invalid = payload()
    invalid["requirements"][0]["constraint"] = {"operator": "<=", "value": None}
    with pytest.raises(ValueError, match="requires value"):
        validate_extraction_payload(invalid, allowed_clauses=[DocumentClause(
            clause_id="c0001", text="Exposure shall be no more than 17%.")])


def test_incomplete_comparison_feedback_includes_original_constraint_and_its_evidence():
    invalid = payload()
    text = "Investment shall not exceed the lower of 100% of fund market value and RMB 100 million."
    invalid['requirements'][0]['constraint'] = {
        'operator': '<=', 'value': None,
        'raw_value_text': 'the lower of 100% of fund market value and RMB 100 million',
    }
    with pytest.raises(ValueError) as error:
        validate_extraction_payload(invalid, allowed_clauses=[DocumentClause(clause_id='c0001', text=text)])
    assert 'requires value, benchmark or formula' in str(error.value)
    assert '"operator":"<="' in str(error.value)
    assert text in str(error.value)
