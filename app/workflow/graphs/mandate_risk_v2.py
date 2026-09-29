from __future__ import annotations

import re
from typing import Any, AsyncGenerator, Tuple

from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.mandate_risk_v2.extractor import canonical_evidence
from app.mandate_risk_v2.pipeline import (
    RequirementCoverageIncomplete,
    RequirementExtractionPipeline,
)
from app.workflow.engine import WorkflowContext


class MandateRiskV2Workflow:
    """Dormant Phase-A workflow for validating the AI-first Requirement IR path.

    It is intentionally not registered as the production mandate-risk workflow
    yet. V1 remains untouched while Phase A is proven against Gold fixtures and
    real PDFs.
    """

    id = "mandate-risk-analysis-v2"

    def __init__(self, pipeline: RequirementExtractionPipeline | None = None) -> None:
        self.pipeline = pipeline or RequirementExtractionPipeline()

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        try:
            document_name, document_text = _resolve_uploaded_document(context)
        except Exception as err:
            yield RunFailedEvent(error=f"V2 文档加载失败: {err}")
            return

        yield ReasoningDeltaEvent(
            delta="V2 Phase A：先独立理解 Mandate Requirement，再做完整性审计；本阶段不读取风险指标库。",
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

        markdown = _render_requirement_ir(result)
        for chunk in code_point_chunks(markdown, context.message_chunk_chars):
            yield MessageDeltaEvent(delta=chunk)
        yield RunCompletedEvent(output=markdown, usage=result.usage)


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
