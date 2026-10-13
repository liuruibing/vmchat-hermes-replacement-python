from __future__ import annotations

import asyncio
import json
from typing import Any, Literal, Sequence
from pydantic import Field

from app.mandate_risk.clauses import DocumentClause
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.models import StrictModel
from app.mandate_risk_v2.pipeline import RequirementExtractionPipeline
from app.mandate_risk_v2.result import (
    MatchedMetricResult,
    StrategyEvidenceCategory,
    StrategyEvidenceResult,
    StrategyEvidenceSection,
    StrategyMetricLink,
    StrategyPoint,
    UnlinkedMetric,
)


class StrategyEvidenceSectionDraft(StrictModel):
    category: StrategyEvidenceCategory
    title: str
    evidence_clause_ids: list[str] = Field(default_factory=list)

class StrategyMetricLinkDraft(StrictModel):
    raw_row_id: int = Field(strict=True)
    basis: Literal["EXPLICIT", "INFERRED", "UNCERTAIN"]
    reason: str
    evidence_clause_ids: list[str] = Field(default_factory=list)


class StrategyPointDraft(StrictModel):
    title: str
    summary: str
    evidence_clause_ids: list[str] = Field(default_factory=list)
    metric_links: list[StrategyMetricLinkDraft] = Field(default_factory=list)


class UnlinkedMetricDraft(StrictModel):
    raw_row_id: int = Field(strict=True)
    reason: str


class StrategyEvidenceBatch(StrictModel):
    sections: list[StrategyEvidenceSectionDraft]
    points: list[StrategyPointDraft] = Field(default_factory=list)
    unlinked_metrics: list[UnlinkedMetricDraft] = Field(default_factory=list)

STRATEGY_EVIDENCE_SYSTEM_PROMPT = """你是投资委托策略依据与当前指标关联分析员。
请阅读 PDF 原文条款和当前已选定的风险监控指标，提取委托原文三大核心语义业务板块（投资标的/工具、业绩比较基准、投资策略与目标）与投资策略要点，并评估每个策略要点与当前已选指标的关联关系。

输入说明：
- 当前已选指标包含 raw_row_id、metric_name、algorithm、mandate（指标库适用分类线索）、strategy_type、risk_type_1、risk_type_2 以及前序阶段评估理由 score_reason。
- 注意：指标库 mandate 字段仅为知识库分类线索，不是 PDF 原文依据；score_reason 为前序阶段筛选/评估的理由，不能替代本阶段对 PDF 原文条款的引用和关联解释。

指示：
1. 提取委托原文三大核心语义业务板块 sections（仅限 instruments、benchmark、investment_strategy 三类语义板块）：
   - 本阶段目标是为用户提供委托原文三大核心板块（投资范围与标的、业绩比较基准、投资策略与目标）的紧凑真实原文依据，而非复刻 PDF 目录或整篇文档搬运。
   - sections 中每个对象必须包含 category，取值仅限以下三者之一：
     - "instruments": 投资范围与允许投资标的/工具（如 Permitted Instruments / Investment Scope / Permitted Assets）。提取允许投资的证券资产类别（如 Listed Equity 等）、现金及现金等价物要求（如期限不超过 1 年等）等实质条款。严禁堆砌无关行政规定。
     - "benchmark": 业绩比较基准（如 Benchmark）。提取原文约定的真实业绩比较基准全称、指数代码、基准配置比例及偏离约束条款。基准名称、代码和比例必须全部来自当前文档，不得使用示例基准补齐。
     - "investment_strategy": 投资策略与目标（如 Investment Strategy / Objectives / Approach）。提取实质性的投资策略、风格、地域/行业配置、选股及交易方法（如主动管理、股票型、增强指数低跟踪误差、自下而上结合自上而下、追求稳定股息与资本增值等），以及支持策略的实质性投资目标（Investment Objectives）。
   - 边界与过滤规则：
     - 严禁将独立的数值限额与合规限制章节（如 Investment Restrictions / Negative List）、风险管理政策（Risk Policy）、词汇定义表（Glossary / Definitions）或纯行政/法律签署程序条款作为单独分类，也严禁将它们全量硬塞进 investment_strategy 充数；仅提取真正属于上述三大板块的实质性原文。
     - 具体的数值限制、合规指标要求将在下方的 points 与 metric_links 中精准引用与关联，不需要也不能在上方三大板块中泛滥堆砌。
     - 标题 title 必须保留 PDF 原文对应的实际章节标题（如 "Permitted Instruments"、"Benchmark"、"Investment Strategy"、"投资范围与工具"、"业绩比较基准" 等；若跨条款或无独立标题，填写准确反映该段原文的真实业务标题，不得为空）。章节编号和标题语言不得作为分类的硬性条件。
     - evidence_clause_ids: 属于该板块的 1 个或多个连续/相关的真实 clause_id（不得为空，不得伪造）。
     - 真实缺失原则：若当前窗口/文档确实不包含某个分类的原文内容（例如文档未约定业绩基准），绝不得伪造原文或假造 clause_id，直接省略该 category 即可。
   - 每个 section 包含：
     - category: "instruments" | "benchmark" | "investment_strategy"（必填，三者之一）。
     - title: 原文章节标题（保留原文有意义标题或准确概括标题，不得为空）。
     - evidence_clause_ids: 属于该分类的 1 个或多个真实 clause_id（不得为空）。

2. 提取策略要点 points：
   - 提取任意条数/语言/标题/表格中的实质策略要点，包括投资目标、投资风格、资产配置策略、风险控制与监控策略等。
   - 每个策略要点 points 必须包含 title（中文短语）、summary（基于原文的简释）、evidence_clause_ids（支持该策略要点的 1–3 个或多个真实 clause_id，不得为空）。
   - metric_links 包含与该策略要点相关的当前指标关联：
     - raw_row_id: 必须是给出的当前已选指标库行 ID 之一。
     - basis: "EXPLICIT"（原文明确要求/提及该测量概念/指标）、"INFERRED"（推导/间接监控用途）、"UNCERTAIN"（关联弱/待核实）。
       - 注意：仅当原文明确要求或指定该测量概念/指标时方可设为 EXPLICIT。单纯词汇定义或泛泛的资本增值描述不能直接设为 EXPLICIT。如由主动管理/超额收益/主动风险推导信息比率用途时，不得因 TE 已定义而直接标为 EXPLICIT。
     - reason: 非空中文说明，解释该策略要点与该指标的关联关系及依据 basis。
     - evidence_clause_ids: 支持该具体关联关系的 1–3 个或多个真实 clause_id（不得为空，可与要点 evidence 相同或补充）。

3. 处置未关联指标 unlinked_metrics 与完整覆盖：
   - 输入给出的每一个当前已选指标，在本次返回中必须恰好被处置一次：要么在至少一个策略要点的 metric_links 中关联，要么在 unlinked_metrics 中给出非空 reason。
   - 在同一个窗口输出中，同一个指标不得同时出现在 metric_links 和 unlinked_metrics 中。

4. 约束规则：
   - 每个给出的 raw_row_id 必须属于输入的当前已选指标 ID 集合，不得出现未知或过期的 raw_row_id。
   - 同一个策略要点内，metric_links 不得包含重复的 raw_row_id。
   - evidence_clause_ids 必须全为输入的真实 clause_id，不得为空，不得伪造 ID 或改写原文。
   - 只输出一个 JSON 对象，结构为:
     {"sections":[{"category":"instruments","title":"...","evidence_clause_ids":["c0001"]},{"category":"benchmark","title":"...","evidence_clause_ids":["c0002"]},{"category":"investment_strategy","title":"...","evidence_clause_ids":["c0003"]}],"points":[{"title":"...","summary":"...","evidence_clause_ids":["c0001"],"metric_links":[{"raw_row_id":2,"basis":"EXPLICIT","reason":"...","evidence_clause_ids":["c0001"]}]}],"unlinked_metrics":[{"raw_row_id":3,"reason":"..."}]}
"""


VALID_SECTION_CATEGORIES: tuple[StrategyEvidenceCategory, ...] = (
    "instruments",
    "benchmark",
    "investment_strategy",
)

class StrategyEvidencePipeline:
    def __init__(self, *, concurrency: int = 2, document_window_chars: int = 60_000) -> None:
        if min(concurrency, document_window_chars) < 1:
            raise ValueError("strategy evidence limits must be positive")
        self.concurrency = concurrency
        self.document_window_chars = document_window_chars
        self._model = RequirementExtractionPipeline()

    async def run(
        self,
        *,
        document_name: str,
        clauses: Sequence[DocumentClause],
        displayed_metrics: Sequence[MatchedMetricResult],
        provider: Any,
        signal: Any = None,
    ) -> tuple[StrategyEvidenceResult, dict[str, Any]]:
        if not clauses:
            raise ValueError("DOCUMENT_HAS_NO_EXTRACTABLE_TEXT")

        unique_metrics: dict[int, MatchedMetricResult] = {}
        for item in displayed_metrics:
            row_id = item.metric.raw_row_id
            if row_id not in unique_metrics:
                unique_metrics[row_id] = item

        allowed_rows = set(unique_metrics.keys())

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

        metrics_json = json.dumps([
            {
                "raw_row_id": m.metric.raw_row_id,
                "metric_name": m.metric.metric_name,
                "algorithm": m.metric.algorithm,
                "mandate": m.metric.mandate,
                "strategy_type": m.metric.strategy_type,
                "risk_type_1": m.metric.risk_type_1,
                "risk_type_2": m.metric.risk_type_2,
                "score_reason": m.score_reason or "",
            }
            for m in unique_metrics.values()
        ], ensure_ascii=False, separators=(",", ":"))

        async def analyze_window(window_clauses: list[DocumentClause], window_index: int) -> StrategyEvidenceBatch:
            nonlocal call_count
            allowed_clauses = {clause.clause_id for clause in window_clauses}
            parts = [
                "# V2 strategy evidence and metric association analysis",
                f"Document: {document_name}",
                f"Document window: {window_index + 1}/{len(windows)}",
                "# PDF clauses (JSON)",
                json.dumps([
                    {"clause_id": c.clause_id, "page": c.page, "text": c.text}
                    for c in window_clauses
                ], ensure_ascii=False, separators=(",", ":")),
                "# Currently selected raw metric rows (JSON)",
                metrics_json,
            ]
            async with semaphore:
                for attempt in range(2):
                    try:
                        call_count += 1
                        payload, usage = await self._model._call_model(
                            provider=provider,
                            system_prompt=STRATEGY_EVIDENCE_SYSTEM_PROMPT,
                            user_prompt="\n".join(parts),
                            signal=signal,
                            stage="strategy_evidence",
                        )
                        reports.append(usage)
                        batch = StrategyEvidenceBatch.model_validate(payload)

                        for section in batch.sections:
                            if not section.title.strip():
                                raise ValueError("strategy section title cannot be empty")
                            if not section.evidence_clause_ids:
                                raise ValueError("strategy section needs PDF evidence")
                            if not set(section.evidence_clause_ids) <= allowed_clauses:
                                raise ValueError("strategy section contains unknown evidence clause_id")

                        linked_rows_in_batch: set[int] = set()

                        for point in batch.points:
                            if not point.title.strip():
                                raise ValueError("strategy point title cannot be empty")
                            if not point.summary.strip():
                                raise ValueError("strategy point summary cannot be empty")
                            if not point.evidence_clause_ids:
                                raise ValueError("strategy point needs PDF evidence")
                            if not set(point.evidence_clause_ids) <= allowed_clauses:
                                raise ValueError("strategy point contains unknown evidence clause_id")

                            seen_rows_in_point: set[int] = set()
                            for link in point.metric_links:
                                if link.raw_row_id not in allowed_rows:
                                    raise ValueError(
                                        f"metric link raw_row_id {link.raw_row_id} is not in selected metrics"
                                    )
                                if link.raw_row_id in seen_rows_in_point:
                                    raise ValueError(
                                        f"duplicate metric link raw_row_id {link.raw_row_id} in point"
                                    )
                                seen_rows_in_point.add(link.raw_row_id)
                                linked_rows_in_batch.add(link.raw_row_id)
                                if not link.reason.strip():
                                    raise ValueError("metric link reason cannot be empty")
                                if not link.evidence_clause_ids:
                                    raise ValueError("metric link needs PDF evidence")
                                if not set(link.evidence_clause_ids) <= allowed_clauses:
                                    raise ValueError("metric link contains unknown evidence clause_id")

                        seen_unlinked: set[int] = set()
                        for unlinked in batch.unlinked_metrics:
                            if unlinked.raw_row_id not in allowed_rows:
                                raise ValueError(
                                    f"unlinked metric raw_row_id {unlinked.raw_row_id} is not in selected metrics"
                                )
                            if unlinked.raw_row_id in seen_unlinked:
                                raise ValueError(f"duplicate unlinked metric raw_row_id {unlinked.raw_row_id}")
                            seen_unlinked.add(unlinked.raw_row_id)
                            if not unlinked.reason.strip():
                                raise ValueError("unlinked metric reason cannot be empty")

                        if linked_rows_in_batch & seen_unlinked:
                            contradictions = linked_rows_in_batch & seen_unlinked
                            raise ValueError(
                                f"metric {contradictions} cannot be both linked and unlinked in the same window batch"
                            )

                        accounted_rows = linked_rows_in_batch | seen_unlinked
                        if allowed_rows and accounted_rows != allowed_rows:
                            missing = allowed_rows - accounted_rows
                            raise ValueError(
                                f"batch must explicitly account for all selected metrics, missing: {missing}"
                            )

                        return batch
                    except (ValueError, TypeError) as exc:
                        if attempt:
                            raise ValueError(f"STRATEGY_EVIDENCE_INVALID: {exc}") from exc
                        feedback = str(exc)[:2000]
                        validation_errors.append(feedback)
                        parts.extend(["# Previous output failed structural validation", feedback])
            raise ValueError("STRATEGY_EVIDENCE_INVALID: maximum attempts exceeded")

        batches = await asyncio.gather(*(
            analyze_window(w, idx) for idx, w in enumerate(windows)
        ))

        unlinked_reasons_by_row: dict[int, list[str]] = {row_id: [] for row_id in allowed_rows}
        all_point_drafts: list[StrategyPointDraft] = []

        for batch in batches:
            all_point_drafts.extend(batch.points)
            for unlinked in batch.unlinked_metrics:
                unlinked_reasons_by_row[unlinked.raw_row_id].append(unlinked.reason)
        all_section_drafts: list[StrategyEvidenceSectionDraft] = []
        for batch in batches:
            all_section_drafts.extend(batch.sections)

        merged_sections_by_category: dict[StrategyEvidenceCategory, dict[str, Any]] = {}
        for idx, sec in enumerate(all_section_drafts):
            cat = sec.category
            if cat not in VALID_SECTION_CATEGORIES:
                continue
            if cat not in merged_sections_by_category:
                merged_sections_by_category[cat] = {
                    "category": cat,
                    "title": sec.title.strip(),
                    "clause_ids": [],
                    "first_seen_index": idx,
                }
            existing = merged_sections_by_category[cat]
            if not existing["title"] and sec.title.strip():
                existing["title"] = sec.title.strip()
            existing_cids = set(existing["clause_ids"])
            for cid in sec.evidence_clause_ids:
                if cid not in existing_cids:
                    existing["clause_ids"].append(cid)
                    existing_cids.add(cid)

        resolved_sections: list[dict[str, Any]] = []
        for cat in VALID_SECTION_CATEGORIES:
            item = merged_sections_by_category.get(cat)
            if not item or not item["clause_ids"]:
                continue
            evidence = canonical_evidence(item["clause_ids"], clauses)
            if not evidence:
                continue
            evidence.sort(key=lambda ev: (ev.source_start, ev.source_end))
            resolved_sections.append({
                "category": cat,
                "title": item["title"],
                "evidence": evidence,
                "first_seen_index": item["first_seen_index"],
                "earliest_source_start": min(ev.source_start for ev in evidence),
            })

        canonical_sections: list[StrategyEvidenceSection] = []
        for idx, sec in enumerate(resolved_sections, start=1):
            canonical_sections.append(
                StrategyEvidenceSection(
                    section_id=f"DS-{idx:04d}",
                    category=sec["category"],
                    title=sec["title"],
                    evidence=sec["evidence"],
                )
            )


        canonical_points_map: dict[tuple[str, str, tuple[str, ...]], StrategyPointDraft] = {}

        for point_draft in all_point_drafts:
            evidence_ids = tuple(sorted(dict.fromkeys(point_draft.evidence_clause_ids)))
            key = (point_draft.title.strip(), point_draft.summary.strip(), evidence_ids)
            if key not in canonical_points_map:
                canonical_points_map[key] = StrategyPointDraft(
                    title=point_draft.title.strip(),
                    summary=point_draft.summary.strip(),
                    evidence_clause_ids=list(evidence_ids),
                    metric_links=[],
                )
            existing_point = canonical_points_map[key]
            existing_link_rows = {link.raw_row_id for link in existing_point.metric_links}
            for link in point_draft.metric_links:
                if link.raw_row_id not in existing_link_rows:
                    existing_point.metric_links.append(link)
                    existing_link_rows.add(link.raw_row_id)

        canonical_points: list[StrategyPoint] = []
        point_counter = 1

        for key, point_draft in canonical_points_map.items():
            point_id = f"ST-{point_counter:04d}"
            point_counter += 1

            point_evidence = canonical_evidence(point_draft.evidence_clause_ids, clauses)

            metric_links: list[StrategyMetricLink] = []
            for link_draft in point_draft.metric_links:
                link_evidence = canonical_evidence(list(dict.fromkeys(link_draft.evidence_clause_ids)), clauses)
                metric_name = unique_metrics[link_draft.raw_row_id].metric.metric_name
                metric_links.append(StrategyMetricLink(
                    raw_row_id=link_draft.raw_row_id,
                    metric_name=metric_name,
                    basis=link_draft.basis,
                    reason=link_draft.reason.strip(),
                    evidence=link_evidence,
                ))

            canonical_points.append(StrategyPoint(
                point_id=point_id,
                title=point_draft.title,
                summary=point_draft.summary,
                evidence=point_evidence,
                metric_links=metric_links,
            ))

        linked_row_ids: set[int] = {
            link.raw_row_id for pt in canonical_points for link in pt.metric_links
        }

        unlinked_metrics: list[UnlinkedMetric] = []
        for row_id, metric_item in unique_metrics.items():
            if row_id in linked_row_ids:
                continue
            reasons = unlinked_reasons_by_row[row_id]
            reason = "；".join(dict.fromkeys(r.strip() for r in reasons if r.strip()))
            unlinked_metrics.append(UnlinkedMetric(
                raw_row_id=row_id,
                metric_name=metric_item.metric.metric_name,
                reason=reason,
            ))

        result = StrategyEvidenceResult(
            sections=canonical_sections,
            points=canonical_points,
            unlinked_metrics=unlinked_metrics,
        )

        complete = len(reports) == call_count and all(
            report is not None and "total_tokens" in report for report in reports
        )
        usage: dict[str, Any] = {
            "complete": complete,
            "expected_calls": call_count,
            "reported_calls": sum(report is not None for report in reports),
            "document_windows": len(windows),
            "validation_errors": validation_errors,
        }
        if complete:
            usage["total_tokens"] = sum(report["total_tokens"] for report in reports)

        return result, usage
