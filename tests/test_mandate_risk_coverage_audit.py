import json

import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import (
    build_candidates,
    build_mandate_recall_candidates,
    infer_strategy_type,
    select_candidates,
)
from app.mandate_risk.models import RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk import prompts
from app.workflow.engine import WorkflowContext
from app.workflow.graphs import mandate_risk as mandate_risk_workflow
from app.workflow.graphs.mandate_risk import MandateRiskLangGraphWorkflow
from app.workflow.graphs.mandate_risk import _usage_summary


class Chunk:
    def __init__(self, content=None, usage=None):
        self.contentDelta = content
        self.usage = usage


def test_usage_summary_does_not_call_partial_token_fields_complete():
    usage = _usage_summary(
        coverage_reports=[{"prompt_tokens": 8}],
        coverage_expected=1,
        semantic_reports=[{"total_tokens": 7}],
        semantic_expected=1,
    )

    assert usage["complete"] is False
    assert usage["coverage_audit"]["complete"] is False
    assert usage["coverage_audit"]["reported_usage"]["prompt_tokens"] == 8
    assert "total_tokens" not in usage


def _metric_source(tmp_path, rows):
    path = tmp_path / "metrics.csv"
    path.write_text(
        "风险类型一级,风险类型二级,指标名称,指标算法,Mandate字段,适用策略种类\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )
    return path


def _context(document, provider):
    return WorkflowContext(
        input_val=VmChatInput(
            userMessage=f"<document_text>{document}</document_text>",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=provider,
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
    )


def _json_section(prompt, marker):
    return json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])


def test_build_coverage_audit_prompt_exposes_raw_metrics_and_clauses():
    metric_a = RawRiskMetric(
        row_id=101,
        source_row=2,
        raw_risk_type_1="信用风险",
        raw_risk_type_2="",
        metric_name="单券集中度上限",
        algorithm="单只信用债投资规模不得超过基金资产净值的10%",
        mandate="",
        strategy_type="固收",
        effective_risk_type_1="信用风险",
        effective_risk_type_2="",
    )
    metric_b = RawRiskMetric(
        row_id=202,
        source_row=3,
        raw_risk_type_1="流动性风险",
        raw_risk_type_2="",
        metric_name="现金及高流动性资产比例",
        algorithm="现金及到期日在一年以内的国债不得低于基金资产净值的5%",
        mandate="",
        strategy_type="固收",
        effective_risk_type_1="流动性风险",
        effective_risk_type_2="",
    )
    registry = RawRiskMetricRegistry([metric_a, metric_b])

    document_text = (
        "[Page 1]\n"
        "The aggregate investment in any single corporate bond shall not exceed 10% of the portfolio NAV.\n\n"
        "[Page 2]\n"
        "The fund shall maintain at least 5% of its net assets in cash and sovereign instruments maturing within one year."
    )

    prompt = prompts.build_coverage_audit_prompt(
        document_text=document_text,
        document_name="new.pdf",
        strategy_type="固收",
        registry=registry,
    )

    # 验证指标库行真实信息暴露
    assert "101" in prompt
    assert "单券集中度上限" in prompt
    assert "单只信用债投资规模不得超过基金资产净值的10%" in prompt

    assert "202" in prompt
    assert "现金及高流动性资产比例" in prompt
    assert "现金及到期日在一年以内的国债不得低于基金资产净值的5%" in prompt

    for clause in split_document_clauses(document_text):
        assert json.dumps(
            {"clause_id": clause.clause_id, "page": clause.page, "text": clause.text},
            ensure_ascii=False,
            separators=(",", ":"),
        ) in prompt

    # 验证输出契约关键字段约束暴露
    assert "raw_row_id" in prompt
    assert "clause_id" in prompt


DOCUMENT = (
    "[Page 1]\n"
    "The aggregate market value of bonds issued by any single issuer shall not exceed 8% of portfolio net assets.\n\n"
    "[Page 2]\n"
    "The portfolio shall maintain at least 12% of net assets in cash and sovereign bonds maturing within one year."
)


def _cross_language_source(tmp_path):
    return _metric_source(
        tmp_path,
        [
            ",,单一债券发行人敞口占比,单一发行人发行的债券市值/投资组合净资产,,固收",
            ",,现金及短期主权债券储备率,现金及剩余期限不超过一年的主权债券市值/组合净资产,,固收",
            ",,单券日收益波动幅度,单只债券日收益率标准差/历史观测期间,,固收",
        ],
    )


@pytest.mark.anyio
async def test_cross_language_audit_recalls_rows_into_semantic_judge_with_python_evidence(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(mandate_risk_workflow, "COVERAGE_AUDIT_BATCH_SIZE", 2, raising=False)
    source = _cross_language_source(tmp_path)
    workflow = MandateRiskLangGraphWorkflow(str(source))
    registry = workflow._load_registry()
    strategy = infer_strategy_type(DOCUMENT)[0]
    eligible = registry.eligible_for_strategy(strategy)

    assert strategy == "固收"
    assert len(eligible) == 3
    assert select_candidates(build_candidates(DOCUMENT, eligible)) == []
    assert select_candidates(build_mandate_recall_candidates(DOCUMENT, eligible)) == []

    class CrossLanguageProvider:
        def __init__(self):
            self.audit_batches = []
            self.semantic_candidates = None

        async def run_skill(self, run_input):
            prompt = run_input.user_prompt
            if "# Controlled coverage audit batch" in prompt:
                metrics = _json_section(prompt, "# Audit metric rows (JSON)\n")
                clauses = _json_section(prompt, "# Input document clauses (JSON)\n")
                self.audit_batches.append([row["raw_row_id"] for row in metrics])
                clause_by_page = {item["page"]: item["clause_id"] for item in clauses}
                proposal_clause = {
                    "单一债券发行人敞口占比": clause_by_page[1],
                    "现金及短期主权债券储备率": clause_by_page[2],
                    # Similar bond topic, but the contract does not constrain volatility.
                    "单券日收益波动幅度": clause_by_page[1],
                }
                proposals = [
                    {"raw_row_id": row["raw_row_id"], "clause_ids": [proposal_clause[row["metric_name"]]]}
                    for row in metrics
                    if row["metric_name"] in proposal_clause
                ]
                strategy_type = _json_section(prompt, "# Audit batch metadata (JSON)\n")["strategy_type"]
                payload = {"strategy_type": strategy_type, "proposals": proposals}
                yield Chunk(content=json.dumps(payload, ensure_ascii=False), usage={"total_tokens": 11})
                return

            self.semantic_candidates = _json_section(
                prompt, "# Candidate metrics from Python (only these rows may be selected as matches)\n"
            )
            matches = []
            for candidate in self.semantic_candidates:
                matched = candidate["metric_name"] != "单券日收益波动幅度"
                matches.append({
                    "raw_row_id": candidate["raw_row_id"],
                    "metric_name": candidate["metric_name"],
                    "match_level": (
                        "DIRECT" if candidate["metric_name"] == "单一债券发行人敞口占比"
                        else "STRONG_INFERRED" if matched else "REJECTED"
                    ),
                    "confidence": 0.8 if matched else 0.0,
                    "reason": "测量对象和条款相符" if matched else "条款只限制发行人敞口，不限制单券收益波动",
                    "evidence": ([{"clause_id": candidate["matched_clauses"][0]["clause_id"]}] if matched else []),
                })
            yield Chunk(
                content=json.dumps({"matches": matches, "gaps": []}, ensure_ascii=False),
                usage={"total_tokens": 7},
            )

    provider = CrossLanguageProvider()
    events = [event async for event in workflow.stream(_context(DOCUMENT, provider))]

    assert provider.audit_batches == [[2, 3], [4]]
    assert {item["recall_source"] for item in provider.semantic_candidates} == {"coverage_audit"}
    assert len(provider.semantic_candidates) == 3
    for candidate in provider.semantic_candidates:
        assert candidate["matched_clauses"]
        assert candidate["matched_clauses"][0]["text"] in DOCUMENT
        assert candidate["matched_clauses"][0]["page"] in {1, 2}
    assert not [event for event in events if event.event == "run.failed"]
    completed = next(event for event in events if event.event == "run.completed")
    assert "单券日收益波动幅度" not in completed.output
    assert "单一债券发行人敞口占比" in completed.output
    assert "现金及短期主权债券储备率" in completed.output
    assert "- 匹配级别：`DIRECT`" not in completed.output
    assert "阶段2受控召回保护" in completed.output
    assert completed.usage["complete"] is True
    assert completed.usage["total_tokens"] == 29
    audit_note = next(event.delta for event in events if event.event == "reasoning.delta")
    assert "审计耗时" in audit_note
    assert "累计模型 tokens 22" in audit_note


@pytest.mark.anyio
async def test_audit_clauses_are_union_merged_with_existing_candidate_for_same_row(tmp_path):
    source = _metric_source(
        tmp_path,
        [",,组合流动性缓冲率,高流动性资产/组合净值,,固收"],
    )
    document = (
        "[Page 1]\n组合流动性缓冲率应纳入定期报告。\n\n"
        "[Page 2]\nThe portfolio shall maintain a liquidity buffer of at least 15% of net assets."
    )

    class SameRowProvider:
        def __init__(self):
            self.semantic_candidates = None

        async def run_skill(self, run_input):
            prompt = run_input.user_prompt
            if "# Controlled coverage audit batch" in prompt:
                clauses = _json_section(prompt, "# Input document clauses (JSON)\n")
                metadata = _json_section(prompt, "# Audit batch metadata (JSON)\n")
                yield Chunk(content=json.dumps({
                    "strategy_type": metadata["strategy_type"],
                    "proposals": [{
                        "raw_row_id": 2,
                        "clause_ids": [item["clause_id"] for item in clauses],
                    }],
                }))
                return
            self.semantic_candidates = _json_section(
                prompt, "# Candidate metrics from Python (only these rows may be selected as matches)\n"
            )
            yield Chunk(content=json.dumps({
                "matches": [{
                    "raw_row_id": 2,
                    "metric_name": "组合流动性缓冲率",
                    "match_level": "REJECTED",
                    "confidence": 0,
                    "reason": "仅用于验证条款合并",
                    "evidence": [],
                }],
                "gaps": [],
            }))

    provider = SameRowProvider()
    events = [event async for event in MandateRiskLangGraphWorkflow(str(source)).stream(
        _context(document, provider)
    )]

    candidate = provider.semantic_candidates[0]
    assert candidate["recall_source"] == "primary"
    assert [item["page"] for item in candidate["matched_clauses"]] == [1, 2]
    assert [item["text"] for item in candidate["matched_clauses"]] == [
        "组合流动性缓冲率应纳入定期报告。",
        "The portfolio shall maintain a liquidity buffer of at least 15% of net assets.",
    ]
    assert not [event for event in events if event.event == "run.failed"]


@pytest.mark.anyio
async def test_missing_usage_from_any_phase_marks_totals_incomplete_without_partial_total(tmp_path):
    source = _metric_source(tmp_path, [",,单一债券发行人敞口占比,发行人债券市值/组合净资产,,固收"])

    class MissingSemanticUsageProvider:
        async def run_skill(self, run_input):
            prompt = run_input.user_prompt
            if "# Controlled coverage audit batch" in prompt:
                metadata = _json_section(prompt, "# Audit batch metadata (JSON)\n")
                yield Chunk(content=json.dumps({"strategy_type": metadata["strategy_type"], "proposals": []}), usage={"total_tokens": 5})
                return
            yield Chunk(content=json.dumps({"matches": [], "gaps": []}))

    events = [event async for event in MandateRiskLangGraphWorkflow(str(source)).stream(
        _context(DOCUMENT, MissingSemanticUsageProvider())
    )]
    completed = next(event for event in events if event.event == "run.completed")

    assert completed.usage["complete"] is False
    assert completed.usage["coverage_audit"]["complete"] is True
    assert completed.usage["semantic_judge"]["complete"] is False
    assert "total_tokens" not in completed.usage


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("invalid_proposal", "error_fragment"),
    [
        ({"raw_row_id": 999, "clause_ids": ["c0001"]}, "未知或未送审指标行"),
        ({"raw_row_id": 2, "clause_ids": ["invented-clause"]}, "不存在的 clause_id"),
    ],
)
async def test_coverage_audit_rejects_untrusted_row_and_clause_ids(
    tmp_path, invalid_proposal, error_fragment
):
    source = _cross_language_source(tmp_path)

    class InvalidAuditProvider:
        async def run_skill(self, run_input):
            if "# Controlled coverage audit batch" in run_input.user_prompt:
                strategy_type = _json_section(
                    run_input.user_prompt, "# Audit batch metadata (JSON)\n"
                )["strategy_type"]
                yield Chunk(content=json.dumps({
                    "strategy_type": strategy_type,
                    "proposals": [invalid_proposal],
                }))
            else:
                pytest.fail("非法审计提案不应进入 semantic_judge")

    events = [event async for event in MandateRiskLangGraphWorkflow(str(source)).stream(
        _context(DOCUMENT, InvalidAuditProvider())
    )]
    failures = [event for event in events if event.event == "run.failed"]
    assert len(failures) == 1
    assert error_fragment in failures[0].error
    assert not [event for event in events if event.event == "run.completed"]


@pytest.mark.anyio
async def test_coverage_audit_rejects_strategy_mismatch(tmp_path):
    source = _cross_language_source(tmp_path)

    class WrongStrategyProvider:
        async def run_skill(self, run_input):
            if "# Controlled coverage audit batch" in run_input.user_prompt:
                yield Chunk(content=json.dumps({"strategy_type": "权益", "proposals": []}))
            else:
                pytest.fail("错误策略的审计结果不应进入 semantic_judge")

    events = [event async for event in MandateRiskLangGraphWorkflow(str(source)).stream(
        _context(DOCUMENT, WrongStrategyProvider())
    )]
    failures = [event for event in events if event.event == "run.failed"]
    assert len(failures) == 1
    assert "审计策略类型与 Python 策略不符" in failures[0].error
    assert not [event for event in events if event.event == "run.completed"]


@pytest.mark.anyio
async def test_coverage_audit_timeout_fails_run_instead_of_rendering_partial_report(
    tmp_path, monkeypatch
):
    monkeypatch.setattr(mandate_risk_workflow, "COVERAGE_AUDIT_TIMEOUT_SECONDS", 0.01, raising=False)
    source = _cross_language_source(tmp_path)

    class HangingAuditProvider:
        async def run_skill(self, run_input):
            if "# Controlled coverage audit batch" in run_input.user_prompt:
                import asyncio
                await asyncio.sleep(1)
            yield Chunk(content=json.dumps({"matches": [], "gaps": []}))

    events = [event async for event in MandateRiskLangGraphWorkflow(str(source)).stream(
        _context(DOCUMENT, HangingAuditProvider())
    )]
    failures = [event for event in events if event.event == "run.failed"]
    assert len(failures) == 1
    assert "受控覆盖审计超时" in failures[0].error
    assert not [event for event in events if event.event == "run.completed"]
