from __future__ import annotations

import asyncio
import json
from typing import Any, Literal

from pydantic import Field

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.concept_knowledge import SOURCES, metric_concept_reference
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.mapping_models import MetricRowAssessment
from app.mandate_risk_v2.models import EvidenceRef, Requirement, StrictModel
from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline, gather_model_tasks
from app.mandate_risk_v2.result import (
    MatchedMetricResult, MetricRequirementResult, RequirementResultItem,
    V2AnalysisResult, _catalogue_name, _metric_reference,
)
from app.mandate_risk_v2.reference_portfolio import ReferencePortfolioResolver


SCREENING_SYSTEM_PROMPT = """你是 PDF 风险指标筛选员，只筛选原文有明确对应测量概念或约束的指标，供人工选择。
直接阅读 PDF 原文及指标库，不进行逐条要求拆解或合规审计。指标入选必须有原文明确要求、使用或限制该指标/测量概念的依据；同义表述或明确等价的计算约束可以匹配，不要求名称逐字一致。仅在定义表出现而未实际要求或使用，不足以入选。
完整浏览给定库行，每行恰好返回一个结果。DIRECT 表示符合上述明确原文依据；REVIEW 表示只有间接监控用途、推导关系或尚不能确认概念对应；NOT_RELEVANT 表示没有对应文档依据。只有 DIRECT 会入选，REVIEW 不入选。
长期资本增长、稳定股息、主动管理、低跟踪误差、一般风险政策或资产暴露不能推导出原文未要求的其他指标。指标库 mandate、分类和算法只能用于理解指标，不能代替 PDF 原文。例如长期增长与低跟踪误差不支持下行Beta；超额收益与跟踪误差也不能自动推导信息比率。
concept_reference 为本库算法的辅助解释，不是合同证据；不得用外部常见定义覆盖本库口径。资本增长/总回报目标可对应基金收益率，超基准目标可对应基准超额收益，不要求每项都有数值上限；但不能从这些目标补出Beta、风险调整或额外比率。证券与发行人、绝对行业敞口与相对行业偏离、股息收益率与贡献/增长/基准比值、第三方基金底层与全组合流动性必须区分。名称未出现但公式等价也可DIRECT；算法未知与概念明确不同不能混为一谈。
不要求每个指标另有数值门槛：正文的管理调整、交易条件或例外明确以某测量概念为操作对象，属于实质使用，可以DIRECT；不能把这类操作性条款等同于仅在定义表出现。反之，公式的操作数、背景分类、基准配置不能各自升级成独立指标要求。
原文明示主要/限定投资某资产类别或市场时，可关联同一配置对象的占比概念，不要求原文再说“计算占比”或给数值门槛；算法、分母未明可说明差异，不从库mandate补造限额。必须区分发行人所在地、上市地和币种，不能把单纯工具许可扩展成其他对象的比例指标。
match_score 是 0–100 的数字，仅表达已判断的对应程度、用于排序，不是入选门槛或正确概率。高分不能使间接推断入选，不凑数量。
DIRECT/REVIEW 必须引用最能支持判断的 1–3 个真实 clause_id，跨页定义或条件需要时可补充；reason 必须区分明确要求与间接用途。原文概念明确但算法缺失或计算口径差异写入 differences；若差异意味着并非同一测量概念，则不得标 DIRECT。只返回 ID，原文及页码由程序读取，不改写原文，不编造阈值、指标或组合值。
NOT_RELEVANT 简述排除原因，evidence_clause_ids 可为空。分段文档只判断本段支持的明确对应，不根据本段未提及推断全文不适用。
只输出一个 JSON 对象，形状为 {"rows":[{"raw_row_id":2,"level":"DIRECT","match_score":92,"reason":"关联理由","evidence_clause_ids":["c0001"],"differences":"口径差异或空字符串"}]}。"""


class ScreeningRow(StrictModel):
    raw_row_id: int = Field(strict=True)
    level: Literal["DIRECT", "REVIEW", "NOT_RELEVANT"]
    match_score: float = Field(strict=True, ge=0, le=100, allow_inf_nan=False)
    reason: str = Field(min_length=1)
    evidence_clause_ids: list[str] = Field(default_factory=list)
    differences: str = ""


class ScreeningBatch(StrictModel):
    rows: list[ScreeningRow]


class ScreeningPipeline:
    """Read PDF + catalogue directly; validate provenance without a semantic audit."""

    def __init__(self, *, batch_size: int = 40, concurrency: int = 2,
                 document_window_chars: int = 60_000) -> None:
        if min(batch_size, concurrency, document_window_chars) < 1:
            raise ValueError("screening limits must be positive")
        self.batch_size = batch_size
        self.concurrency = concurrency
        self.document_window_chars = document_window_chars
        self._model = RequirementExtractionPipeline()

    async def run(self, *, document_name: str, document_text: str,
                  registry: RawRiskMetricRegistry, provider: Any, signal: Any = None,
                  reference_portfolio_resolver: ReferencePortfolioResolver | None = None,
                  as_of_date: str | None = None):
        clauses = split_document_clauses(document_text)
        rows = registry.all()
        if not clauses:
            raise ValueError("DOCUMENT_HAS_NO_EXTRACTABLE_TEXT")
        if not rows:
            raise ValueError("MANDATE_RISK_METRIC_LIBRARY_INVALID: empty")

        windows = []
        window, size = [], 0
        for clause in clauses:
            clause_size = len(clause.text) + len(clause.clause_id) + 32
            if window and size + clause_size > self.document_window_chars:
                windows.append(window)
                window, size = [], 0
            window.append(clause)
            size += clause_size
        if window:
            windows.append(window)

        semaphore = asyncio.Semaphore(self.concurrency)
        reports = []
        validation_errors = []
        call_count = 0

        async def screen(window, batch_rows, window_index):
            nonlocal call_count
            parts = ["# V2 fast metric screening", f"Document: {document_name}",
                     f"Document window: {window_index + 1}/{len(windows)}",
                     "# PDF clauses (JSON)", json.dumps([
                         {"clause_id": c.clause_id, "page": c.page, "text": c.text} for c in window
                     ], ensure_ascii=False, separators=(",", ":")),
                     "# Raw metric rows (JSON)", json.dumps([
                         {"raw_row_id": r.row_id, "name": r.metric_name, "algorithm": r.algorithm,
                          "mandate": r.mandate, "strategy_type": r.strategy_type,
                          "concept_reference": metric_concept_reference(r)} for r in batch_rows
                     ], ensure_ascii=False, separators=(",", ":")),
                     "# Concept reference provenance (not PDF evidence)",
                     json.dumps(SOURCES, ensure_ascii=False, separators=(",", ":"))]
            allowed_rows = {row.row_id for row in batch_rows}
            allowed_clauses = {clause.clause_id for clause in window}
            async with semaphore:
                for attempt in range(2):
                    try:
                        call_count += 1
                        payload, usage = await self._model._call_model(
                            provider=provider, system_prompt=SCREENING_SYSTEM_PROMPT,
                            user_prompt="\n".join(parts), signal=signal, stage="screening",
                        )
                        reports.append(usage)
                        batch = ScreeningBatch.model_validate(payload)
                        ids = [item.raw_row_id for item in batch.rows]
                        if len(ids) != len(set(ids)) or set(ids) != allowed_rows:
                            raise ValueError("each assigned catalogue row must appear exactly once")
                        for item in batch.rows:
                            if item.level != "NOT_RELEVANT" and not item.evidence_clause_ids:
                                raise ValueError(f"row {item.raw_row_id}: selected metric needs PDF evidence")
                            if not set(item.evidence_clause_ids) <= allowed_clauses:
                                raise ValueError(f"row {item.raw_row_id}: unknown evidence clause_id")
                            if not item.reason.strip():
                                raise ValueError(f"row {item.raw_row_id}: empty reason")
                        return batch.rows
                    except (ValueError, TypeError) as exc:
                        if attempt:
                            raise ValueError(f"MANDATE_SCREENING_INVALID: {exc}") from exc
                        feedback = str(exc)[:2000]
                        validation_errors.append(feedback)
                        parts.extend(["# Previous output failed structural validation", feedback])

        # gather preserves window order, making aggregation independent of response timing.
        batches = await gather_model_tasks(*(
            screen(window, rows[offset:offset + self.batch_size], index)
            for index, window in enumerate(windows)
            for offset in range(0, len(rows), self.batch_size)
        ))
        by_row = {row.row_id: [] for row in rows}
        for batch in batches:
            for item in batch:
                by_row[item.raw_row_id].append(item)

        screened, matched, candidates, requirements, assessments = [], [], [], [], []
        for metric in rows:
            selected = [item for item in by_row[metric.row_id] if item.level == "DIRECT"]
            assessments.append(MetricRowAssessment(
                raw_row_id=metric.row_id, outcome="LINKED" if selected else "NOT_RELEVANT",
                reason="；".join(dict.fromkeys(
                    ("未入选：仅有间接或待确认关联，不满足原文明示准入要求。" + item.reason)
                    if item.level == "REVIEW" else item.reason
                    for item in by_row[metric.row_id]
                )),
            ))
            if not selected:
                continue
            associations = []
            for item in selected:
                evidence = canonical_evidence(list(dict.fromkeys(item.evidence_clause_ids)), clauses)
                requirement = RequirementResultItem(
                    requirement=Requirement(
                        requirement_id=f"SRC-{len(requirements) + 1:04d}", requirement_type="OTHER",
                        semantic_summary="\n".join(quote.text for quote in evidence),
                        evidence=EvidenceRef(clause_ids=[quote.clause_id for quote in evidence]),
                        attributes={"screening_evidence": True},
                    ), evidence=evidence,
                )
                requirements.append(requirement)
                associations.append(MetricRequirementResult(
                    requirement=requirement, mapping_level=item.level, mapping_reason=item.reason,
                    mapping_evidence=evidence, match_score=item.match_score, score_reason=item.reason,
                    review_notes=[item.differences] if item.differences.strip() else [],
                ))
            strongest = max(selected, key=lambda item: item.match_score)
            result = MatchedMetricResult(metric=_metric_reference(metric), requirements=associations,
                                         match_score=strongest.match_score, score_reason=strongest.reason)
            screened.append(result)
            matched.append(result)
        screened.sort(key=lambda item: (-item.match_score, item.metric.raw_row_id))
        analysis = V2AnalysisResult(
            document_name=document_name, analysis_mode="screening", coverage_status="not_audited",
            metric_catalogue_name=_catalogue_name(registry), metric_catalogue_sha256=registry.source_sha256 or None,
            catalogue_assessments=assessments, requirements=requirements,
            screened_metrics=screened, matched_metrics=matched, candidate_metrics=candidates,
            summary=f"浏览 {len(rows)} 个库指标，筛选出 {len(screened)} 个相关指标，按匹配分排序；供人工选择。",
        )
        resolver = reference_portfolio_resolver or ReferencePortfolioResolver(as_of_date=as_of_date)
        analysis = resolver.enrich_result(analysis)
        complete = len(reports) == call_count and all(
            report is not None and "total_tokens" in report for report in reports)
        usage = {"complete": complete, "analysis_mode": "screening", "expected_calls": call_count,
                 "reported_calls": sum(report is not None for report in reports),
                 "document_windows": len(windows), "validation_errors": validation_errors}
        if complete:
            usage["total_tokens"] = sum(report["total_tokens"] for report in reports)
        return analysis, usage
