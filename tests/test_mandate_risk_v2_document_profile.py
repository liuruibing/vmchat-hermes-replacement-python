from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.extractor import (
    build_requirement_ir,
    canonicalize_document_profile,
    validate_document_profile_draft,
    validate_extraction_payload,
)
from app.mandate_risk_v2.models import (
    DocumentProfileDraft,
    DocumentProfileItemDraft,
    ExtractionBatch,
)


def _make_clauses():
    return [
        DocumentClause(clause_id="c0001", page=1, text="本基金投资范围包括境内依法发行上市的股票和债券。", source_start=0, source_end=25),
        DocumentClause(clause_id="c0002", page=1, text="主要投资工具为沪深A股、国债及央行票据。", source_start=26, source_end=50),
        DocumentClause(clause_id="c0003", page=2, text="业绩比较基准：沪深300指数收益率*60% + 中债综合指数收益率*40%。", source_start=51, source_end=90),
        DocumentClause(clause_id="c0004", page=2, text="投资策略采用Top-down大类资产配置与Bottom-up个股选择结合。", source_start=91, source_end=130),
        DocumentClause(clause_id="c0005", page=3, text="深入研究宏观经济趋势，动态调整股票与债券的配置比例。", source_start=131, source_end=165),
    ]


def test_profile_validation_missing_evidence():

    # Draft with empty evidence_clause_ids raises Pydantic ValidationError during model_validate
    with pytest.raises(ValidationError):
        DocumentProfileDraft(
            asset_scope=DocumentProfileItemDraft(summary="境内股票", evidence_clause_ids=[])
        )

    # Draft with empty summary raises Pydantic ValidationError
    with pytest.raises(ValidationError):
        DocumentProfileDraft(
            asset_scope=DocumentProfileItemDraft(summary="", evidence_clause_ids=["c0001"])
        )


def test_profile_validation_invalid_citations():
    clauses = _make_clauses()
    known = {c.clause_id for c in clauses}

    draft = DocumentProfileDraft(
        asset_scope=DocumentProfileItemDraft(summary="境内股票", evidence_clause_ids=["c9999"])
    )
    with pytest.raises(ValueError, match="unknown clause_id"):
        validate_document_profile_draft(draft, known_clause_ids=known)

    draft_dup = DocumentProfileDraft(
        instruments=DocumentProfileItemDraft(summary="股票", evidence_clause_ids=["c0001", "c0001"])
    )
    with pytest.raises(ValueError, match="duplicate clause_id"):
        validate_document_profile_draft(draft_dup, known_clause_ids=known)


def test_profile_window_merging_and_dedup():
    clauses = _make_clauses()

    draft_window1 = DocumentProfileDraft(
        asset_scope=DocumentProfileItemDraft(summary="境内股票与债券", evidence_clause_ids=["c0001"]),
        investment_strategy=DocumentProfileItemDraft(summary="Top-down资产配置策略", evidence_clause_ids=["c0004"]),
    )
    draft_window2 = DocumentProfileDraft(
        asset_scope=DocumentProfileItemDraft(summary="境内股票与债券", evidence_clause_ids=["c0001"]),
        benchmark=DocumentProfileItemDraft(summary="沪深300*60% + 中债*40%", evidence_clause_ids=["c0003"]),
        investment_strategy=DocumentProfileItemDraft(summary="动态调整股债配置比例", evidence_clause_ids=["c0005"]),
    )

    profile = canonicalize_document_profile([draft_window1, draft_window2], clauses)

    assert set(profile.keys()) == {"asset_scope", "instruments", "benchmark", "investment_strategy"}

    # Deduplicated identical summaries and evidence clause_ids for asset_scope
    assert profile["asset_scope"]["summary"] == "境内股票与债券"
    assert [e["clause_id"] for e in profile["asset_scope"]["evidence"]] == ["c0001"]
    assert profile["asset_scope"]["evidence"][0]["text"] == clauses[0].text
    assert profile["asset_scope"]["evidence"][0]["page"] == 1
    assert profile["asset_scope"]["evidence"][0]["source_start"] == 0

    # Merged strategy summaries and multi-clause evidence across paragraphs without loss
    assert profile["investment_strategy"]["summary"] == "Top-down资产配置策略\n动态调整股债配置比例"
    assert [e["clause_id"] for e in profile["investment_strategy"]["evidence"]] == ["c0004", "c0005"]
    assert profile["investment_strategy"]["evidence"][0]["page"] == 2
    assert profile["investment_strategy"]["evidence"][1]["page"] == 3

    # Benchmark present from window 2
    assert profile["benchmark"]["summary"] == "沪深300*60% + 中债*40%"
    assert [e["clause_id"] for e in profile["benchmark"]["evidence"]] == ["c0003"]

    # Instruments missing across windows -> null
    assert profile["instruments"] is None



def test_profile_strategy_preserves_document_order_when_model_reverses_citations():
    clauses = _make_clauses()
    draft = DocumentProfileDraft(
        investment_strategy=DocumentProfileItemDraft(
            summary="结合配置与个股选择，并动态调整股债比例",
            evidence_clause_ids=["c0005", "c0004"],
        ),
    )
    evidence = canonicalize_document_profile([draft], clauses)["investment_strategy"]["evidence"]
    assert [item["clause_id"] for item in evidence] == ["c0004", "c0005"]
    assert [item["text"] for item in evidence] == [clauses[3].text, clauses[4].text]

def test_profile_absent_information():
    clauses = _make_clauses()
    profile = canonicalize_document_profile([None], clauses)
    assert profile == {
        "asset_scope": None,
        "instruments": None,
        "benchmark": None,
        "investment_strategy": None,
    }


def test_screening_and_extraction_profile_contract():
    clauses = _make_clauses()
    payload = {
        "requirements": [],
        "definitions": [],
        "contextual_facts": [],
        "document_profile": {
            "asset_scope": {"summary": "境内股票", "evidence_clause_ids": ["c0001"]},
            "instruments": {"summary": "A股", "evidence_clause_ids": ["c0002"]},
            "benchmark": None,
            "investment_strategy": None,
        },
    }

    batch = validate_extraction_payload(payload, allowed_clauses=clauses)
    ir = build_requirement_ir(document_name="test.pdf", batches=[batch], clauses=clauses)

    assert set(ir.document_profile.keys()) == {"asset_scope", "instruments", "benchmark", "investment_strategy"}
    assert ir.document_profile["asset_scope"]["summary"] == "境内股票"
    assert ir.document_profile["asset_scope"]["evidence"][0]["clause_id"] == "c0001"
    assert ir.document_profile["instruments"]["summary"] == "A股"
    assert ir.document_profile["benchmark"] is None
    assert ir.document_profile["investment_strategy"] is None
