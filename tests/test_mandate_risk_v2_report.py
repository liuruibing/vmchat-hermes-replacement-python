import pytest

from app.mandate_risk_v2.report import render_v2_report
from tests.test_mandate_risk_v2_mapping_pipeline import Provider, _data
from app.mandate_risk_v2.mapping import MappingPipeline
from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.models import Definition, EvidenceRef


@pytest.mark.anyio
async def test_report_uses_six_columns_verbatim_clause_and_unknown_group():
    ir, clauses, registry = _data()
    mapping = await MappingPipeline(batch_size=2).run(
        ir=ir, clauses=clauses, registry=registry, provider=Provider(),
    )
    report = render_v2_report(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert "| 分组 | 名称 | Mandate解读 | 值 | 参考组合 | 相似度 |" in report
    assert "| 待分类 | Never-seen Exposure Measure | Exposure shall not exceed NAV. | — | — | 93/100 |" in report
    assert "Other Measure" not in report
    assert "第 1 页" in report


@pytest.mark.anyio
async def test_summary_quote_chooses_requirement_clause_before_supporting_definition():
    ir, clauses, registry = _data()
    mapping = await MappingPipeline(batch_size=2).run(
        ir=ir, clauses=clauses, registry=registry, provider=Provider(),
    )
    ir.definitions.append(Definition(definition_id="DEF-0001", term="NAV",
                                     semantic_summary="Net asset value",
                                     evidence=EvidenceRef(clause_ids=["c0002"])))
    clauses.append(DocumentClause(clause_id="c0002", text="NAV means net asset value.", page=2))
    mapping.links[0].evidence_clause_ids = ["c0002", "c0001"]
    report = render_v2_report(ir=ir, clauses=clauses, registry=registry, mapping=mapping)
    assert "| 待分类 | Never-seen Exposure Measure | Exposure shall not exceed NAV. |" in report
