from __future__ import annotations

import json
from typing import Iterable

from app.mandate_risk.models import MetricCandidate
from app.mandate_risk.registry import RawRiskMetricRegistry


SYSTEM_PROMPT = """你是投资委托/投资策略风险指标匹配分析器。

硬约束：
1. 正式指标只能从 Python 提供的候选指标集合中选择；禁止创造、改名、纠正或补写指标库原始字段。
2. raw_row_id 是正式身份。metric_name 必须与该 raw_row_id 对应的库内原名完全一致。
3. PDF/文档中的策略事实与风险指标库是两套事实源：文档说明需求，指标库定义可选择指标。
4. DIRECT 仅用于文档明确要求与指标定义/Mandate直接对应；STRONG_INFERRED 需要很强的业务语义支撑；WEAK_INFERRED 只作为待确认；无关项必须 REJECTED。
5. 不因为“长期资本增长”等宽泛描述把 VaR、波动率、最大回撤等所有通用风险指标自动选中。
6. 每个 DIRECT/STRONG_INFERRED/WEAK_INFERRED 必须提供能在输入文档中逐字找到的 evidence.text。不要编造引文。
7. 如果文档有明确需求但候选库没有等价指标，写入 gaps；不得用相近指标冒充。
8. 不生成 green/amber/red，不创造文档未明确给出的阈值。
9. 只输出一个 JSON 对象，不要 Markdown，不要代码围栏，不要额外说明。
"""


def build_semantic_judge_prompt(
    *,
    document_text: str,
    document_name: str,
    strategy_type: str,
    registry: RawRiskMetricRegistry,
    candidates: Iterable[MetricCandidate],
) -> str:
    rows = []
    for candidate in candidates:
        metric = registry.require(candidate.raw_row_id)
        rows.append(
            {
                "raw_row_id": metric.row_id,
                "metric_name": metric.metric_name,
                "risk_type_1": metric.effective_risk_type_1,
                "risk_type_2": metric.effective_risk_type_2,
                "raw_risk_type_1": metric.raw_risk_type_1,
                "raw_risk_type_2": metric.raw_risk_type_2,
                "algorithm": metric.algorithm,
                "mandate": metric.mandate,
                "strategy_type": metric.strategy_type,
                "deterministic_score": candidate.deterministic_score,
                "exact_hits": candidate.exact_hits,
            }
        )

    schema = {
        "strategy_type": strategy_type,
        "summary": "一句话概括匹配结论",
        "matches": [
            {
                "raw_row_id": 14,
                "metric_name": "跟踪误差",
                "match_level": "DIRECT",
                "confidence": 0.98,
                "reason": "为什么这个指标与条款匹配",
                "evidence": [{"text": "文档中的原文引文", "page": None}],
            }
        ],
        "gaps": [
            {
                "requirement": "文档明确要求但库内无等价指标的需求",
                "reason": "为什么不能用现有指标冒充",
                "evidence": [{"text": "原文引文", "page": None}],
            }
        ],
    }

    return "\n\n".join(
        [
            f"<document_name>{document_name}</document_name>",
            f"<python_strategy_type>{strategy_type}</python_strategy_type>",
            "<document_text>\n" + document_text.strip() + "\n</document_text>",
            "<candidate_metrics>\n"
            + json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
            + "\n</candidate_metrics>",
            "<required_output_schema>\n"
            + json.dumps(schema, ensure_ascii=False, separators=(",", ":"))
            + "\n</required_output_schema>",
        ]
    )
