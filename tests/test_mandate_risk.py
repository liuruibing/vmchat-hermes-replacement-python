import json
from pathlib import Path

import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.agents.registry import AgentRegistry
from app.mandate_risk.matcher import (
    build_candidates,
    build_mandate_recall_candidates,
    infer_strategy_type,
    merge_candidate_sets,
    select_candidates,
)
from app.mandate_risk.models import CandidateClauseHint, MetricCandidate, RawRiskMetric
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.validator import validate_model_result
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk import MandateRiskLangGraphWorkflow


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "agents" / "mandate_risk_ai" / "knowledge" / "raw"
METRICS = RAW_DIR / "risk_metrics.raw.csv"
MANIFEST = RAW_DIR / "source-manifest.json"

SAMPLE = """境内上市权益（高分红策略）
Listed Equity; and Cash and Cash Equivalents </= 1 Year
Benchmark
MSCI China A International High Dividend Yield Index
Investment Strategy
The primary investment objective of the Sub-Portfolio is to gain stable dividend yield and achieve long term capital growth through mainly investing into high-quality Common Shares issued by Chinese Issuers with an emphasis on value and good growth outlook, and to generate a total returns in excess of the Sub-Portfolio Benchmark Index. The Sub-Portfolio targets to achieve an outperformance of 0.5% p.a. over a 3 to 5-year investment horizon.
To ensure the Sub-Portfolio to generate a comparable return against the Benchmark in the long term through investing in permissible instruments in the China A-Share market.
The Sub-Portfolio shall deliver excess return over the designated Benchmark by executing geographic, Industry/Sector and trading strategies. The Sub-Portfolio shall be actively managed to achieve the Investment Objective, by investing in Funds or stocks, which are listed through China A-Share market.
The Sub-Portfolio should be managed under the enhanced index strategy with proper active management and low Tracking Error. The investment strategy could be a blend of bottom-up and top-down approach. The Sub-Portfolio shall invest in listed stocks with solid fundamentals to gain stable dividend yield and achieve long term capital growth.
"""


def test_report_chat_agent_is_registered_with_simple_chat_workflow():
    agents = AgentRegistry(str(ROOT / "agents")).load()
    agent = agents.require("mandate-risk-chat")
    role = agents.get_role(agent.id, "risk-assistant")

    assert agent.workflow == "simple-chat"
    assert role is not None
    assert "报告" in role.systemPrompt


def test_raw_registry_preserves_source_values_and_separate_effective_grouping():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    assert len(registry.all()) == 34
    assert registry.source_sha256 == "cd097edb49be7b73152292722db71d41e7f65d40444b35cd7fc3e96a071fc4d5"

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert manifest["xlsx_sha256"] == "3c14c4fcb991f7d8876140cc2e95ce508b73b31092c9d7bf8e844ab2dd4e6871"
    assert manifest["source_sheet"] == "风险指标库"
    assert manifest["metric_rows"] == 34

    excess = registry.get_by_name("超额收益率（基准超额）")
    assert excess is not None
    assert excess.raw_risk_type_1 == ""
    assert excess.raw_risk_type_2 == ""
    assert excess.effective_risk_type_1 == "收益风险（6）"
    assert excess.effective_risk_type_2 == "收益率"
    assert excess.algorithm == "Ri- Bi"

    region = registry.get_by_name("区域分布")
    assert region is not None
    assert region.algorithm == ""
    assert region.mandate == ""


def test_equity_strategy_filters_fixed_income_rows():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    strategy, confidence = infer_strategy_type(SAMPLE)
    assert strategy == "权益"
    assert confidence > 0.7

    eligible = registry.eligible_for_strategy(strategy)
    names = {item.metric_name for item in eligible}
    assert "跟踪误差" in names
    assert "超额收益率（基准超额）" in names
    assert "久期" not in names
    assert "信用利差（债券）" not in names

    candidates = build_candidates(SAMPLE, eligible)
    scores = {item.metric_name: item.deterministic_score for item in candidates}
    assert scores["跟踪误差"] > 0
    assert scores["超额收益率（基准超额）"] > 0
    assert scores["股息贡献率"] > 0


def test_latin_metric_names_use_token_boundaries():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    var_metric = registry.get_by_name("VaR")
    assert var_metric is not None

    candidate = build_candidates(
        "Risk policies may be varied from time to time.",
        [var_metric],
    )[0]

    assert candidate.deterministic_score == 0.0
    assert candidate.matched_clauses == []
    assert select_candidates([candidate]) == []


def test_distinctive_mandate_fallback_can_recall_without_metric_name():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    credit_spread = registry.get_by_name("信用利差（债券）")
    assert credit_spread is not None

    # Primary precision remains unchanged: no literal credit-spread concept.
    primary = build_candidates(
        "The portfolio seeks reasonable credit risk exposure and adds value through relative value investment.",
        [credit_spread],
    )[0]
    assert primary.deterministic_score == 0.0

    fallback = build_mandate_recall_candidates(
        "The portfolio seeks reasonable credit risk exposure and adds value through relative value investment.",
        [credit_spread],
    )[0]
    assert fallback.deterministic_score >= 4.0
    assert fallback.matched_clauses
    selected = select_candidates([fallback])
    assert [item.raw_row_id for item in selected] == [credit_spread.row_id]


def test_generic_mandate_does_not_create_fallback_candidate():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    var_metric = registry.get_by_name("VaR")
    assert var_metric is not None

    fallback = build_mandate_recall_candidates(
        "The strategy seeks long term capital growth.",
        [var_metric],
    )[0]

    assert fallback.deterministic_score == 0.0
    assert fallback.matched_clauses == []
    assert select_candidates([fallback]) == []


def test_single_latin_mandate_fragment_does_not_create_fallback_candidate():
    metric = RawRiskMetric(
        row_id=999,
        source_row=999,
        metric_name="Synthetic Metric",
        mandate="Government",
        strategy_type="固收",
    )

    fallback = build_mandate_recall_candidates(
        "The portfolio may invest in Government Agency securities.",
        [metric],
    )[0]

    assert fallback.deterministic_score == 0.0
    assert fallback.matched_clauses == []
    assert select_candidates([fallback]) == []


def test_shared_specific_mandate_does_not_independently_recall_multiple_metrics():
    first = RawRiskMetric(
        row_id=901,
        source_row=901,
        metric_name="Metric A",
        mandate="reasonable credit risk exposure",
        strategy_type="固收",
    )
    second = RawRiskMetric(
        row_id=902,
        source_row=902,
        metric_name="Metric B",
        mandate="reasonable credit risk exposure",
        strategy_type="固收",
    )

    fallback = build_mandate_recall_candidates(
        "The portfolio seeks reasonable credit risk exposure.",
        [first, second],
    )

    assert all(item.deterministic_score == 0.0 for item in fallback)
    assert select_candidates(fallback) == []


def test_default_candidate_selection_has_no_hard_twelve_item_cap():
    candidates = [
        MetricCandidate(
            raw_row_id=index,
            metric_name=f"metric-{index}",
            deterministic_score=4.0,
            matched_clauses=[
                CandidateClauseHint(
                    clause_id=f"c{index:04d}",
                    text=f"evidence {index}",
                    score=4.0,
                )
            ],
        )
        for index in range(1, 21)
    ]

    assert len(select_candidates(candidates)) == 20
    assert len(select_candidates(candidates, limit=12)) == 12


def test_merge_candidate_sets_prefers_primary_by_row_id():
    primary = MetricCandidate(
        raw_row_id=7,
        metric_name="metric",
        deterministic_score=12.0,
        matched_clauses=[CandidateClauseHint(clause_id="c0001", text="primary", score=12.0)],
    )
    fallback = MetricCandidate(
        raw_row_id=7,
        metric_name="metric",
        deterministic_score=4.0,
        matched_clauses=[CandidateClauseHint(clause_id="c0002", text="fallback", score=4.0)],
    )

    merged = merge_candidate_sets([primary], [fallback])
    assert len(merged) == 1
    assert merged[0].deterministic_score == 12.0
    assert merged[0].matched_clauses[0].text == "primary"


def test_validator_rejects_renamed_or_out_of_registry_metrics():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    tracking = registry.get_by_name("跟踪误差")
    assert tracking is not None

    payload = {
        "summary": "test",
        "matches": [
            {
                "raw_row_id": tracking.row_id,
                "metric_name": "Tracking Error",
                "match_level": "DIRECT",
                "confidence": 0.99,
                "evidence": [{"text": "low Tracking Error"}],
            },
            {
                "raw_row_id": 999,
                "metric_name": "高股息股票占比",
                "match_level": "DIRECT",
                "confidence": 0.99,
                "evidence": [{"text": "gain stable dividend yield"}],
            },
        ],
    }
    result = validate_model_result(
        payload=payload,
        registry=registry,
        allowed_row_ids=[item.row_id for item in registry.all()],
        document_text=SAMPLE,
        document_name="sample",
        strategy_type="权益",
    )
    assert result.selected_metrics == []


class Chunk:
    def __init__(self, content=None, reasoning=None, usage=None):
        self.contentDelta = content
        self.reasoningDelta = reasoning
        self.usage = usage


class Provider:
    async def run_skill(self, run_input):
        audit_chunk = _empty_coverage_audit_chunk(run_input.user_prompt)
        if audit_chunk:
            yield audit_chunk
            return
        payload = {
            "strategy_type": "权益",
            "summary": "高分红增强指数策略，核心约束是超额收益与低跟踪误差。",
            "matches": [
                {
                    "raw_row_id": 14,
                    "metric_name": "跟踪误差",
                    "match_level": "DIRECT",
                    "confidence": 0.99,
                    "reason": "文档明确出现 low Tracking Error。",
                    "evidence": [{"text": "low Tracking Error", "page": None}],
                },
                {
                    "raw_row_id": 3,
                    "metric_name": "超额收益率（基准超额）",
                    "match_level": "DIRECT",
                    "confidence": 0.98,
                    "reason": "文档明确要求相对基准取得超额收益。",
                    "evidence": [{"text": "generate a total returns in excess of the Sub-Portfolio Benchmark Index", "page": None}],
                },
                {
                    "raw_row_id": 5,
                    "metric_name": "股息贡献率",
                    "match_level": "STRONG_INFERRED",
                    "confidence": 0.87,
                    "reason": "与 stable dividend yield 直接相关。",
                    "evidence": [{"text": "gain stable dividend yield", "page": None}],
                },
            ],
            "gaps": [],
        }
        matches_by_id = {item["raw_row_id"]: item for item in payload["matches"]}
        for candidate in _candidate_rows_from_prompt(run_input.user_prompt):
            row_id = candidate["raw_row_id"]
            if row_id not in matches_by_id:
                matches_by_id[row_id] = {
                    "raw_row_id": row_id,
                    "metric_name": candidate["metric_name"],
                    "match_level": "REJECTED",
                    "confidence": 0.0,
                    "reason": "The document does not require this metric.",
                    "evidence": [],
                }
        payload["matches"] = list(matches_by_id.values())
        yield Chunk(reasoning="matching")
        yield Chunk(content=json.dumps(payload, ensure_ascii=False))
        yield Chunk(usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150})


def _synthetic_metric_source(tmp_path, rows):
    path = tmp_path / "metrics.csv"
    path.write_text(
        "风险类型一级,风险类型二级,指标名称,指标算法,Mandate字段,适用策略种类\n"
        + "\n".join(rows)
        + "\n",
        encoding="utf-8",
    )
    return path


def _synthetic_candidate_payload(candidate_rows):
    return {
        "strategy_type": "权益",
        "summary": "synthetic candidate coverage",
        "matches": [
            {
                "raw_row_id": row["raw_row_id"],
                "metric_name": row["metric_name"],
                "match_level": "REJECTED",
                "confidence": 0.0,
                "reason": "The document does not require this metric.",
                "evidence": [],
            }
            for row in candidate_rows
        ],
        "gaps": [],
    }


def _candidate_rows_from_prompt(prompt):
    marker = "# Candidate metrics from Python (only these rows may be selected as matches)\n"
    rows_json = prompt.split(marker, 1)[1].split("\n\n# Strategy-eligible", 1)[0]
    return json.loads(rows_json)


def _empty_coverage_audit_chunk(prompt):
    if "# Controlled coverage audit batch" not in prompt:
        return None
    marker = "# Audit batch metadata (JSON)\n"
    metadata = json.loads(prompt.split(marker, 1)[1].split("\n", 1)[0])
    return Chunk(content=json.dumps({"strategy_type": metadata["strategy_type"], "proposals": []}))


@pytest.mark.anyio
async def test_mandate_risk_retries_when_model_omits_a_candidate_row(tmp_path):
    metric_source = _synthetic_metric_source(
        tmp_path,
        [
            ",,跟踪误差,TE=σ(Rp−Rb),,权益",
            ",,股息贡献率,股息收益占整体收益比重,,权益",
        ],
    )
    document = "境内上市权益策略要求 low Tracking Error，并追求 stable dividend yield。"

    class OmitThenCompleteProvider:
        def __init__(self):
            self.calls = 0

        async def run_skill(self, run_input):
            audit_chunk = _empty_coverage_audit_chunk(run_input.user_prompt)
            if audit_chunk:
                yield audit_chunk
                return
            self.calls += 1
            candidates = _candidate_rows_from_prompt(run_input.user_prompt)
            assert len(candidates) == 2
            payload = _synthetic_candidate_payload(
                candidates if self.calls == 2 else candidates[:1]
            )
            yield Chunk(content=json.dumps(payload, ensure_ascii=False))

    provider = OmitThenCompleteProvider()
    workflow = MandateRiskLangGraphWorkflow(str(metric_source))
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage=f"<document_text>{document}</document_text>",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=provider,
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
    )

    events = [event async for event in workflow.stream(context)]

    assert provider.calls == 2
    assert not [event for event in events if event.event == "run.failed"]
    assert any(event.event == "run.completed" for event in events)


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("invalid_case", "error_fragment"),
    [
        ("missing", "漏掉候选指标行"),
        ("duplicate", "候选行重复"),
        ("unknown", "未知指标行"),
        ("wrong_metric_name", "metric_name 与指标库不符"),
    ],
)
async def test_mandate_risk_fails_after_two_incomplete_or_invalid_candidate_lists(
    tmp_path, invalid_case, error_fragment
):
    metric_source = _synthetic_metric_source(
        tmp_path,
        [
            ",,跟踪误差,TE=σ(Rp−Rb),,权益",
            ",,股息贡献率,股息收益占整体收益比重,,权益",
        ],
    )
    document = "境内上市权益策略要求 low Tracking Error，并追求 stable dividend yield。"

    class RepeatedlyInvalidProvider:
        def __init__(self):
            self.calls = 0

        async def run_skill(self, run_input):
            audit_chunk = _empty_coverage_audit_chunk(run_input.user_prompt)
            if audit_chunk:
                yield audit_chunk
                return
            self.calls += 1
            candidates = _candidate_rows_from_prompt(run_input.user_prompt)
            payload = _synthetic_candidate_payload(candidates)
            if invalid_case == "missing":
                payload["matches"].pop()
            elif invalid_case == "duplicate":
                payload["matches"].append(dict(payload["matches"][0]))
            elif invalid_case == "unknown":
                payload["matches"].append(
                    {
                        "raw_row_id": 999,
                        "metric_name": "不存在的指标",
                        "match_level": "REJECTED",
                        "confidence": 0,
                        "evidence": [],
                    }
                )
            else:
                payload["matches"][0]["metric_name"] = "错误指标名称"
            yield Chunk(content=json.dumps(payload, ensure_ascii=False))

    provider = RepeatedlyInvalidProvider()
    workflow = MandateRiskLangGraphWorkflow(str(metric_source))
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage=f"<document_text>{document}</document_text>",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=provider,
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
    )

    events = [event async for event in workflow.stream(context)]

    assert provider.calls == 2
    failed = [event for event in events if event.event == "run.failed"]
    assert len(failed) == 1
    assert not [event for event in events if event.event == "run.completed"]
    assert error_fragment in failed[0].error


@pytest.mark.anyio
async def test_mandate_risk_accepts_empty_matches_when_there_are_no_candidates(tmp_path):
    metric_source = _synthetic_metric_source(
        tmp_path,
        [",,不存在于文本的指标,synthetic algorithm,,权益"],
    )
    document = "境内上市权益策略以长期资本增长为目标。"

    class EmptyMatchesProvider:
        async def run_skill(self, run_input):
            audit_chunk = _empty_coverage_audit_chunk(run_input.user_prompt)
            if audit_chunk:
                yield audit_chunk
                return
            assert _candidate_rows_from_prompt(run_input.user_prompt) == []
            yield Chunk(content=json.dumps({"matches": [], "gaps": []}))

    workflow = MandateRiskLangGraphWorkflow(str(metric_source))
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage=f"<document_text>{document}</document_text>",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=EmptyMatchesProvider(),
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
    )

    events = [event async for event in workflow.stream(context)]

    assert not [event for event in events if event.event == "run.failed"]
    assert any(event.event == "run.completed" for event in events)


@pytest.mark.anyio
async def test_mandate_risk_workflow_returns_validated_markdown():
    workflow = MandateRiskLangGraphWorkflow(str(METRICS))
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage=(
                "<document_name>境内上市权益-高分红策略.pdf</document_name>"
                f"<document_text>{SAMPLE}</document_text>"
            ),
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=Provider(),
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
        skill_md="只允许从原始风险指标库匹配。",
        role_prompt="输出可审计的风险指标匹配结果。",
    )

    events = []
    async for event in workflow.stream(context):
        events.append(event)

    assert [e for e in events if getattr(e, "event", None) == "run.failed"] == []
    completed = next(e for e in events if getattr(e, "event", None) == "run.completed")
    assert "# 风险指标匹配报告" in completed.output
    assert "跟踪误差" in completed.output
    assert "超额收益率（基准超额）" in completed.output
    assert "股息贡献率" in completed.output
    assert "高股息股票占比" not in completed.output
    assert "34 条，只读匹配" in completed.output
    assert completed.usage["complete"] is False
    assert completed.usage["coverage_audit"]["complete"] is False
    assert completed.usage["semantic_judge"]["reported_usage"]["total_tokens"] == 150
    assert "total_tokens" not in completed.usage


@pytest.mark.anyio
async def test_mandate_risk_retries_once_when_model_json_is_truncated():
    class TruncatedThenValidProvider:
        def __init__(self):
            self.calls = 0

        async def run_skill(self, _input):
            audit_chunk = _empty_coverage_audit_chunk(_input.user_prompt)
            if audit_chunk:
                yield audit_chunk
                return
            self.calls += 1
            if self.calls == 1:
                yield Chunk(content='{"matches":[')
            else:
                candidates = _candidate_rows_from_prompt(_input.user_prompt)
                yield Chunk(content=json.dumps(_synthetic_candidate_payload(candidates)))

    provider = TruncatedThenValidProvider()
    workflow = MandateRiskLangGraphWorkflow(str(METRICS))
    context = WorkflowContext(
        input_val=VmChatInput(
            userMessage=f"<document_text>{SAMPLE}</document_text>",
            globalQueryParameters=GlobalQueryParameters(names=[], nonemptyFlags={}),
        ),
        provider=provider,
        agent_id="mandate-risk-ai",
        role_id="risk-analyst",
    )
    events = [event async for event in workflow.stream(context)]

    assert provider.calls == 2
    assert not [event for event in events if event.event == "run.failed"]
    assert any(event.event == "run.completed" for event in events)
