from __future__ import annotations

import asyncio
import json
from typing import Any, Literal

from pydantic import Field

from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.mapping_models import MetricRowAssessment
from app.mandate_risk_v2.models import EvidenceRef, Requirement, StrictModel
from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline
from app.mandate_risk_v2.result import (
    MatchedMetricResult, MetricRequirementResult, RequirementResultItem,
    V2AnalysisResult, _catalogue_name, _metric_reference,
)


SCREENING_SYSTEM_PROMPT = """你是 PDF 风险指标筛选员，帮助用户从给定指标库筛出与文档相关的指标，供人工选择。
直接阅读 PDF 原文及指标库，理解文档的资产、策略、目标、约束和风险暴露后筛选，不进行逐条要求拆解或合规审计。
完整浏览给定库行，每行恰好返回一个结果。DIRECT 表示原文有明确对应测量概念；REVIEW 表示有合理的间接监控用途或适用条件需确认；NOT_RELEVANT 表示没有合理文档关联。
合同未点名指标、算法缺失、口径不完全一致，不是自动排除理由；简要写在 differences 中即可。一般风险政策不能支持整个库；无相关资产暴露的专属指标不要牵强关联。
match_score 是 0–100 的数字，表达文档相关程度，不是正确概率。90–100 明确对应且适用；75–89 关联清晰但有口径差异；50–74 间接监控或依据较弱；0–49 关联弱或存在重大不适用因素。独立评分，不固定按 DIRECT/REVIEW 给分，不凑数量。
DIRECT/REVIEW 必须引用最能支持该指标的 1–3 个真实 clause_id，跨页定义或条件需要时可补充；reason 简要解释原文与该指标的关联。只返回 ID，原文及页码由程序读取，不改写原文，不编造阈值、指标或组合值。
NOT_RELEVANT 简述排除原因，evidence_clause_ids 可为空。分段文档只判断本段支持的关联，不根据本段未提及推断全文不适用。
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
                  registry: RawRiskMetricRegistry, provider: Any, signal: Any = None):
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
                          "mandate": r.mandate, "strategy_type": r.strategy_type} for r in batch_rows
                     ], ensure_ascii=False, separators=(",", ":"))]
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
        batches = await asyncio.gather(*(
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
            selected = [item for item in by_row[metric.row_id] if item.level != "NOT_RELEVANT"]
            assessments.append(MetricRowAssessment(
                raw_row_id=metric.row_id, outcome="LINKED" if selected else "NOT_RELEVANT",
                reason="；".join(dict.fromkeys(item.reason for item in by_row[metric.row_id])),
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
            (matched if any(item.level == "DIRECT" for item in selected) else candidates).append(result)
        screened.sort(key=lambda item: (-item.match_score, item.metric.raw_row_id))
        analysis = V2AnalysisResult(
            document_name=document_name, analysis_mode="screening", coverage_status="not_audited",
            metric_catalogue_name=_catalogue_name(registry), metric_catalogue_sha256=registry.source_sha256 or None,
            catalogue_assessments=assessments, requirements=requirements,
            screened_metrics=screened, matched_metrics=matched, candidate_metrics=candidates,
            summary=f"浏览 {len(rows)} 个库指标，筛选出 {len(screened)} 个相关指标，按匹配分排序；供人工选择。",
        )
        complete = len(reports) == call_count and all(
            report is not None and "total_tokens" in report for report in reports)
        usage = {"complete": complete, "analysis_mode": "screening", "expected_calls": call_count,
                 "reported_calls": sum(report is not None for report in reports),
                 "document_windows": len(windows), "validation_errors": validation_errors}
        if complete:
            usage["total_tokens"] = sum(report["total_tokens"] for report in reports)
        return analysis, usage
