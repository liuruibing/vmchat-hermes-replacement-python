# ==============================================================================
# 文件：app/workflow/graphs/mandate_risk_v2.py
# 文件作用：实现 V2 投资委托分析入口，在快速筛选与详细分析之间选择，并输出前端报告和表格数据。
# 全局位置：main.py → Engine（mandate-risk-analysis-v2）→ 本文件 → 分析 Pipeline → Provider。
# 谁调用它：legacy.py 注册实例，WorkflowEngine 按 mandate-risk-analysis-v2 id 调用 stream(context)。
# 输入：已解析的 PDF、真实指标目录、Provider，以及 screening/detailed 与 phase_a_only 配置。
# 输出：报告正文、阶段进度、用量统计和结构化 metadata，供前端展示指标表格及原文依据。
# 主要流程：screening 直接筛选；detailed 先提取要求（Phase A），再映射指标并独立复核（Phase B）。
# 前端类比：像 async function* 驱动的多步任务，根据配置选择分支并逐步通知页面进度。
# 边界：这里没有 StateGraph，控制流是普通 Python if/await/yield；LangChain 或 OMP 由 Provider 决定。
# 阅读入口：先看 stream() 的 screening 分支，再看 detailed 分支和 _resolve_uploaded_document()。
# ==============================================================================

from __future__ import annotations

import re
import os
from typing import Any, AsyncGenerator, Tuple

from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.catalogue import load_prebuilt_registry
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.mapping import MappingPipeline
from app.mandate_risk_v2.reference_portfolio import ReferencePortfolioResolver
from app.mandate_risk_v2.report import render_screening_report, render_v2_report
from app.mandate_risk_v2.screening import ScreeningPipeline
from app.mandate_risk_v2.result import build_v2_analysis_result
from app.mandate_risk_v2.strategy_evidence import StrategyEvidencePipeline
from app.mandate_risk_v2.pipeline import (
    RequirementCoverageIncomplete,
    RequirementExtractionPipeline,
)
from app.workflow.engine import WorkflowContext


class MandateRiskV2Workflow:
    """V2 defaults to fast screening; detailed Requirement IR analysis is opt-in."""

    id = "mandate-risk-analysis-v2"
    def __init__(self, pipeline: RequirementExtractionPipeline | None = None,
                 mapping_pipeline: MappingPipeline | None = None,
                 strategy_evidence_pipeline: StrategyEvidencePipeline | None = None,
                 metric_registry: RawRiskMetricRegistry | None = None,
                 reference_portfolio_resolver: ReferencePortfolioResolver | None = None,
                 phase_a_only: bool = False, mode: str | None = None) -> None:
        # A | None 类似 TS 的 A | null；允许注入实现，否则创建默认 Pipeline（分阶段处理对象）。
        self.pipeline = pipeline or RequirementExtractionPipeline()
        self.mapping_pipeline = mapping_pipeline or MappingPipeline()
        self.strategy_evidence_pipeline = strategy_evidence_pipeline or StrategyEvidencePipeline()
        self.metric_registry = metric_registry
        self.reference_portfolio_resolver = reference_portfolio_resolver or ReferencePortfolioResolver()
        self.phase_a_only = phase_a_only

        # Python 条件表达式“值 if 条件 else 其它值”类似 JS 三元表达式。
        self.mode = mode if mode is not None else os.getenv("MANDATE_RISK_V2_MODE", "screening")
        if self.mode not in {"screening", "detailed"}:
            raise ValueError("MANDATE_RISK_V2_MODE must be screening or detailed")
    def _load_registry(self) -> RawRiskMetricRegistry:
        # Default application startup injects the prevalidated snapshot shared with V1.
        # Standalone workflows load once on first use; runs never reparse the source.
        if self.metric_registry is None:
            self.metric_registry = load_prebuilt_registry()
        return self.metric_registry

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        # 含 yield 的 async def 是异步生成器：先交出进度事件，再 await 分析，最后交出完成事件。
        try:
            document_name, document_text = _resolve_uploaded_document(context)
        except Exception as err:
            yield RunFailedEvent(error=f"V2 文档加载失败: {err}")
            return

        if self.mode == "screening" and not self.phase_a_only:
            # 默认快速路径。这里 yield 的是明确的阶段进度，不是模型内部逐 token 的输出。
            yield ReasoningDeltaEvent(
                delta="快速筛选：直接阅读 PDF 和完整指标库，筛选相关指标并给出匹配分、原文依据。", sequence=1,
            )
            try:
                analysis, screening_usage = await ScreeningPipeline().run(
                    document_name=document_name, document_text=document_text,
                    registry=self._load_registry(), provider=context.provider, signal=context.signal,
                    reference_portfolio_resolver=self.reference_portfolio_resolver,
                )
            except Exception as err:
                yield RunFailedEvent(error=f"V2 快速指标筛选失败: {err}")
                return
            yield ReasoningDeltaEvent(
                delta=f"筛选完成：{len(analysis.screened_metrics)} 个相关指标；开始策略依据与指标关联分析。", sequence=2,
            )
            clauses = split_document_clauses(document_text)
            try:
                strategy_evidence, strategy_usage = await self.strategy_evidence_pipeline.run(
                    document_name=document_name,
                    clauses=clauses,
                    displayed_metrics=analysis.screened_metrics,
                    provider=context.provider,
                    signal=context.signal,
                )
                analysis.strategy_evidence = strategy_evidence
            except Exception as err:
                yield RunFailedEvent(error=f"V2 策略依据与指标关联分析失败: {err}")
                return
            yield ReasoningDeltaEvent(
                delta="策略依据与指标关联分析完成，结果供用户筛选判断。", sequence=3,
            )
            markdown = render_screening_report(analysis)
            for chunk in code_point_chunks(markdown, context.message_chunk_chars):
                yield MessageDeltaEvent(delta=chunk)
            complete = bool(screening_usage.get("complete") and strategy_usage.get("complete"))
            usage = {
                "complete": complete,
                "analysis_mode": "screening",
                "screening_phase": screening_usage,
                "strategy_evidence_phase": strategy_usage,
                "result_counts": {
                    "screened_metrics": len(analysis.screened_metrics),
                    "matched_metrics": len(analysis.matched_metrics),
                    "candidate_metrics": len(analysis.candidate_metrics),
                },
            }
            if complete:
                usage["total_tokens"] = screening_usage.get("total_tokens", 0) + strategy_usage.get("total_tokens", 0)
            yield RunCompletedEvent(output=markdown, usage=usage, metadata={
                "mandate_risk_v2": {"phase": "complete", "mode": "screening",
                                    "result": analysis.model_dump(mode="json")},
            })
            return

        yield ReasoningDeltaEvent(
            delta=("V2 Phase A：先独立理解 Mandate Requirement，再做完整性审计；本阶段不读取风险指标库。"
                   if self.phase_a_only else
                   "V2 Phase A：先理解 PDF 要求并审计覆盖；随后筛选相关库指标、评估匹配分并独立复核。"),
            sequence=1,
        )

        try:
            # Phase A 先理解文档要求，不读取指标库；模型交互及完整性审计封装在 pipeline 内。
            result = await self.pipeline.run(
                document_name=document_name,
                document_text=document_text,
                provider=context.provider,
                signal=context.signal,
            )
        except RequirementCoverageIncomplete as err:
            yield RunFailedEvent(error=str(err))
            return
        except Exception as err:
            yield RunFailedEvent(error=f"V2 Requirement IR 分析失败: {err}")
            return

        # phase_a_only 用于仅查看要求提取；完整 detailed 模式还要执行指标映射与 Critic 复核。
        completion_metadata: dict[str, Any] | None = None
        if self.phase_a_only:
            markdown = _render_requirement_ir(result)
            usage = result.usage
            completion_metadata = {
                "mandate_risk_v2": {
                    "phase": "requirement_ir",
                    "requirement_ir": result.requirement_ir.model_dump(mode="json"),
                }
            }
        else:
            yield ReasoningDeltaEvent(
                delta=(f"Phase A 完成：识别 {len(result.requirement_ir.requirements)} 条 Requirement；"
                       "开始审计完整指标库并独立复核。"),
                sequence=2,
            )
            try:
                registry = self._load_registry()
                mapping = await self.mapping_pipeline.run(
                    ir=result.requirement_ir, clauses=result.clauses,
                    registry=registry, provider=context.provider, signal=context.signal,
                )
                analysis = build_v2_analysis_result(
                    ir=result.requirement_ir,
                    clauses=result.clauses,
                    registry=registry,
                    mapping=mapping,
                    reference_portfolio_resolver=self.reference_portfolio_resolver,
                )
            except Exception as err:
                yield RunFailedEvent(error=f"V2 指标映射或 Critic 复核失败: {err}")
                return

            yield ReasoningDeltaEvent(
                delta="Phase B 完成：相关指标筛选与独立复核已完成；开始策略依据与指标关联分析。", sequence=3,
            )
            try:
                displayed_metrics = analysis.matched_metrics + analysis.candidate_metrics
                strategy_evidence, strategy_usage = await self.strategy_evidence_pipeline.run(
                    document_name=document_name,
                    clauses=result.clauses,
                    displayed_metrics=displayed_metrics,
                    provider=context.provider,
                    signal=context.signal,
                )
                analysis.strategy_evidence = strategy_evidence
            except Exception as err:
                yield RunFailedEvent(error=f"V2 策略依据与指标关联分析失败: {err}")
                return
            yield ReasoningDeltaEvent(
                delta="策略依据与指标关联分析完成，结果供用户筛选判断。", sequence=4,
            )
            markdown = render_v2_report(
                ir=result.requirement_ir, clauses=result.clauses,
                registry=registry, mapping=mapping, analysis=analysis,
            )
            completion_metadata = {
                "mandate_risk_v2": {
                    "phase": "complete",
                    "result": analysis.model_dump(mode="json"),
                }
            }
            complete = bool(result.usage.get("complete") and mapping.usage.get("complete") and strategy_usage.get("complete"))
            usage = {
                "complete": complete,
                "requirement_phase": result.usage,
                "mapping_phase": mapping.usage,
                "strategy_evidence_phase": strategy_usage,
                "result_counts": {
                    "requirements": len(analysis.requirements),
                    "matched_metrics": len(analysis.matched_metrics),
                    "candidate_metrics": len(analysis.candidate_metrics),
                    "screened_metrics": len(analysis.screened_metrics),
                    "pending_review": len(analysis.pending_review),
                    "library_gaps": len(analysis.library_gaps),
                    "non_metric_requirements": len(analysis.non_metric_requirements),
                    "unresolved_requirements": len(analysis.unresolved_requirements),
                },
            }
            if complete:
                usage["total_tokens"] = (result.usage["total_tokens"] +
                                         mapping.usage["total_tokens"] +
                                         strategy_usage["total_tokens"])

        for chunk in code_point_chunks(markdown, context.message_chunk_chars):
            yield MessageDeltaEvent(delta=chunk)
        yield RunCompletedEvent(
            output=markdown,
            usage=usage,
            metadata=completion_metadata,
        )


def _extract_document_payload(user_message: str) -> Tuple[str, str]:
    raw = str(user_message or "").strip()
    name_match = re.search(r"<document_name>\s*(.*?)\s*</document_name>", raw, re.S | re.I)
    text_match = re.search(r"<document_text>\s*(.*?)\s*</document_text>", raw, re.S | re.I)
    document_name = name_match.group(1).strip() if name_match else "vmChat输入文本"
    document_text = text_match.group(1).strip() if text_match else raw
    return document_name, document_text


def _resolve_uploaded_document(context: WorkflowContext) -> Tuple[str, str]:
    # Tuple[str, str] 类似 TS 元组 [string, string]，返回文件名和解析正文。
    # document_loader 是运行时注入的读取回调；流程不用直接操作上传目录或 PDF 解析器。
    document_ids = list(
        context.document_ids or getattr(context.input_val, "documentIds", []) or []
    )
    if not document_ids:
        return _extract_document_payload(context.input_val.userMessage)
    if len(document_ids) != 1:
        raise ValueError("MANDATE_RISK_REQUIRES_ONE_DOCUMENT: 当前一次分析仅支持 1 个 PDF")
    if context.document_loader is None:
        raise RuntimeError("DOCUMENT_RUNTIME_UNAVAILABLE")

    document = context.document_loader(document_ids[0])
    # hasattr 类似检查对象是否有属性：兼容 Pydantic 对象、普通 dict 和其它对象。
    if hasattr(document, "model_dump"):
        payload = document.model_dump()
    elif isinstance(document, dict):
        payload = document
    else:
        payload = {
            "filename": getattr(document, "filename", ""),
            "text": getattr(document, "text", ""),
        }
    document_name = str(payload.get("filename") or document_ids[0]).strip()
    document_text = str(payload.get("text") or "").strip()
    if not document_text:
        raise ValueError("DOCUMENT_HAS_NO_EXTRACTABLE_TEXT")
    return document_name, document_text


def _render_requirement_ir(result) -> str:
    # IR（中间表示）是 Python 整理出的要求结构；此处只渲染报告，不调用模型或推断新要求。
    ir = result.requirement_ir
    lines = [
        "# Mandate Requirement IR（V2 Phase A）",
        "",
        "> 当前输出只验证 PDF 理解和 Requirement 完整性，尚未执行正式风险指标映射。",
        "",
        f"- 文档：`{ir.document_name}`",
        f"- Requirements：`{len(ir.requirements)}`",
        f"- Definitions：`{len(ir.definitions)}`",
        f"- Context facts：`{len(ir.contextual_facts)}`",
        "- Coverage review：`complete`",
        "",
        "## Requirements",
        "",
        "| ID | 类型 | Requirement | 页码 |",
        "|---|---|---|---|",
    ]
    for requirement in ir.requirements:
        evidence = canonical_evidence(requirement.evidence.clause_ids, result.clauses)
        pages = sorted({item.page for item in evidence if item.page is not None})
        page_text = ", ".join(str(page) for page in pages) if pages else "—"
        summary = requirement.semantic_summary.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {requirement.requirement_id} | {requirement.requirement_type} | "
            f"{summary} | {page_text} |"
        )

    if ir.definitions:
        lines.extend(["", "## Definitions", ""])
        for definition in ir.definitions:
            evidence = canonical_evidence(definition.evidence.clause_ids, result.clauses)
            pages = sorted({item.page for item in evidence if item.page is not None})
            page_text = ", ".join(str(page) for page in pages) if pages else "—"
            lines.append(
                f"- **{definition.term}**（p.{page_text}）：{definition.semantic_summary}"
            )

    return "\n".join(lines).strip() + "\n"
