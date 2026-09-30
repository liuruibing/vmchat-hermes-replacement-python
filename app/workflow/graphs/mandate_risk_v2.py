from __future__ import annotations

import re
import os
from pathlib import Path
from typing import Any, AsyncGenerator, Tuple

from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk_v2.mapping import MappingPipeline
from app.mandate_risk_v2.report import render_v2_report
from app.mandate_risk_v2.result import build_v2_analysis_result
from app.mandate_risk_v2.pipeline import (
    RequirementCoverageIncomplete,
    RequirementExtractionPipeline,
)
from app.workflow.engine import WorkflowContext


class MandateRiskV2Workflow:
    """Experimental V2: independent Requirement IR, catalogue mapping and critic."""

    id = "mandate-risk-analysis-v2"

    def __init__(self, pipeline: RequirementExtractionPipeline | None = None,
                 mapping_pipeline: MappingPipeline | None = None,
                 metric_registry: RawRiskMetricRegistry | None = None,
                 phase_a_only: bool = False) -> None:
        self.pipeline = pipeline or RequirementExtractionPipeline()
        self.mapping_pipeline = mapping_pipeline or MappingPipeline()
        self.metric_registry = metric_registry
        self.phase_a_only = phase_a_only

    def _load_registry(self) -> RawRiskMetricRegistry:
        if self.metric_registry is not None:
            return self.metric_registry
        configured = (os.getenv("MANDATE_RISK_METRIC_SOURCE") or
                      os.getenv("MANDATE_RISK_METRIC_XLSX") or
                      "agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv")
        path = Path(configured)
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[3] / path
        if not path.is_file():
            raise RuntimeError(f"MANDATE_RISK_METRIC_LIBRARY_NOT_FOUND: {path}")
        return RawRiskMetricRegistry.from_path(path)

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        try:
            document_name, document_text = _resolve_uploaded_document(context)
        except Exception as err:
            yield RunFailedEvent(error=f"V2 文档加载失败: {err}")
            return

        yield ReasoningDeltaEvent(
            delta=("V2 Phase A：先独立理解 Mandate Requirement，再做完整性审计；本阶段不读取风险指标库。"
                   if self.phase_a_only else
                   "V2 Phase A：先理解 PDF 要求并审计覆盖；随后筛选相关库指标、评估匹配分并独立复核。"),
            sequence=1,
        )

        try:
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
                usage = {
                    "complete": bool(result.usage.get("complete") and mapping.usage.get("complete")),
                    "requirement_phase": result.usage,
                    "mapping_phase": mapping.usage,
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
                if usage["complete"]:
                    usage["total_tokens"] = (result.usage["total_tokens"] +
                                             mapping.usage["total_tokens"])
            except Exception as err:
                yield RunFailedEvent(error=f"V2 指标映射或 Critic 复核失败: {err}")
                return
            yield ReasoningDeltaEvent(
                delta="Phase B 完成：相关指标筛选、匹配评分和独立复核已完成，结果供用户筛选判断。",
                sequence=3,
            )
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
