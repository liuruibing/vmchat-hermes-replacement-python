import json
from pathlib import Path

import pytest

from app.compatibility.hermes_request import GlobalQueryParameters, VmChatInput
from app.mandate_risk.matcher import build_candidates, infer_strategy_type, select_candidates
from app.mandate_risk.models import CandidateClauseHint, MetricCandidate
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


def test_non_generic_mandate_text_can_recall_without_metric_name():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    credit_spread = registry.get_by_name("信用利差（债券）")
    assert credit_spread is not None

    candidate = build_candidates(
        "The portfolio seeks reasonable credit risk exposure and adds value through relative value investment.",
        [credit_spread],
    )[0]

    assert candidate.deterministic_score >= 4.0
    assert candidate.matched_clauses
    selected = select_candidates([candidate])
    assert [item.raw_row_id for item in selected] == [credit_spread.row_id]


def test_generic_mandate_only_match_stays_below_default_threshold():
    registry = RawRiskMetricRegistry.from_path(METRICS)
    var_metric = registry.get_by_name("VaR")
    assert var_metric is not None

    candidate = build_candidates(
        "The strategy seeks long term capital growth.",
        [var_metric],
    )[0]

    assert candidate.deterministic_score == 0.5
    assert candidate.matched_clauses
    assert select_candidates([candidate]) == []


def test_default_candidate_selection_has_no_hard_twelve_item_cap():
    candidates = [
        MetricCandidate(
            raw_row_id=index,
            metric_name=f"metric-{index}",
            deterministic_score=2.0,
            matched_clauses=[
                CandidateClauseHint(
                    clause_id=f"c{index:04d}",
                    text=f"evidence {index}",
                    score=2.0,
                )
            ],
        )
        for index in range(1, 21)
    ]

    assert len(select_candidates(candidates)) == 20
    assert len(select_candidates(candidates, limit=12)) == 12


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
    async def run_skill(self, _input):
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
        yield Chunk(reasoning="matching")
        yield Chunk(content=json.dumps(payload, ensure_ascii=False))
        yield Chunk(usage={"prompt_tokens": 100, "completion_tokens": 50, "total_tokens": 150})


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
    assert completed.usage["total_tokens"] == 150
