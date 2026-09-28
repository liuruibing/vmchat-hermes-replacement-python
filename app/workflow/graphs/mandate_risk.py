from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any, AsyncGenerator, Dict, List, Tuple

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from app.compatibility.hermes_events import (
    MessageDeltaEvent,
    ReasoningDeltaEvent,
    RunCompletedEvent,
    RunFailedEvent,
    code_point_chunks,
)
from app.mandate_risk.json_utils import extract_first_json_object
from app.mandate_risk.matcher import build_candidates, infer_strategy_type
from app.mandate_risk.prompts import SYSTEM_PROMPT, build_semantic_judge_prompt
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.renderer import render_markdown
from app.mandate_risk.validator import validate_model_result
from app.provider.fixed_provider import ModelSkillRunInput
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_state import MandateRiskGraphState


DEFAULT_METRIC_SOURCE = "agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv"


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _extract_document_payload(user_message: str) -> Tuple[str, str]:
    raw = str(user_message or "").strip()
    name_match = re.search(r"<document_name>\s*(.*?)\s*</document_name>", raw, re.S | re.I)
    text_match = re.search(r"<document_text>\s*(.*?)\s*</document_text>", raw, re.S | re.I)
    document_name = name_match.group(1).strip() if name_match else "vmChat输入文本"
    document_text = text_match.group(1).strip() if text_match else raw
    return document_name, document_text


def _usage_from_chunk(chunk: Any) -> Dict[str, int]:
    raw = getattr(chunk, "usage", None)
    if raw is None:
        return {}
    if not isinstance(raw, dict) and hasattr(raw, "model_dump"):
        raw = raw.model_dump()
    if not isinstance(raw, dict):
        return {}
    return {
        "prompt_tokens": int(raw.get("prompt_tokens") or raw.get("input_tokens") or 0),
        "completion_tokens": int(raw.get("completion_tokens") or raw.get("output_tokens") or 0),
        "total_tokens": int(raw.get("total_tokens") or 0),
    }


class MandateRiskLangGraphWorkflow:
    id = "mandate-risk-analysis"

    def __init__(self, metric_source_path: str | None = None) -> None:
        configured = (
            metric_source_path
            or os.getenv("MANDATE_RISK_METRIC_SOURCE")
            or os.getenv("MANDATE_RISK_METRIC_XLSX")
            or DEFAULT_METRIC_SOURCE
        )
        self.metric_source_path = str(configured)
        self._checkpointer = InMemorySaver()

    def _load_registry(self) -> RawRiskMetricRegistry:
        path = Path(self.metric_source_path)
        if not path.is_file():
            raise RuntimeError(f"MANDATE_RISK_METRIC_LIBRARY_NOT_FOUND: {path}")
        registry = RawRiskMetricRegistry.from_path(path)
        if len(registry.all()) != 34:
            raise RuntimeError(
                "MANDATE_RISK_METRIC_LIBRARY_INVALID: expected 34 rows, "
                f"got {len(registry.all())}"
            )
        return registry

    def _compile(self, context: WorkflowContext, registry: RawRiskMetricRegistry):
        async def prepare(state: MandateRiskGraphState) -> Dict[str, Any]:
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}
            document_text = str(state.get("document_text") or "").strip()
            if not document_text:
                return {"error": "没有可分析的投资策略文本"}
            strategy_type, confidence = infer_strategy_type(document_text)
            eligible = registry.eligible_for_strategy(strategy_type)
            candidates = build_candidates(document_text, eligible)
            return {
                "strategy_type": strategy_type,
                "strategy_confidence": confidence,
                "candidate_row_ids": [item.raw_row_id for item in candidates],
                "candidates": [item.model_dump() for item in candidates],
            }

        async def semantic_judge(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            candidate_ids = [int(item) for item in state.get("candidate_row_ids") or []]
            candidate_models = build_candidates(
                str(state.get("document_text") or ""),
                [registry.require(item) for item in candidate_ids],
            )
            user_prompt = build_semantic_judge_prompt(
                document_text=str(state.get("document_text") or ""),
                document_name=str(state.get("document_name") or ""),
                strategy_type=str(state.get("strategy_type") or "未知"),
                registry=registry,
                candidates=candidate_models,
            )
            system_prompt = "\n\n".join(
                part
                for part in [
                    context.role_prompt.strip() if context.role_prompt else "",
                    SYSTEM_PROMPT,
                    "# Agent Skill\n" + context.skill_md.strip() if context.skill_md else "",
                ]
                if part
            )

            run_skill = getattr(context.provider, "run_skill", None) or getattr(
                context.provider, "runSkill", None
            )
            if run_skill is None:
                return {"error": "AI Provider 不支持 Skill 运行"}

            stream = run_skill(
                ModelSkillRunInput(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
                    search_knowledge=None,
                    signal=context.signal,
                )
            )
            content_parts: List[str] = []
            reasoning: List[str] = []
            usage: Dict[str, int] = {}
            if hasattr(stream, "__aiter__"):
                async for chunk in stream:
                    if _is_aborted(context.signal):
                        return {"error": "客户端连接已中断"}
                    r_delta = getattr(chunk, "reasoningDelta", None) or getattr(
                        chunk, "reasoning_delta", None
                    )
                    if r_delta:
                        reasoning.append(str(r_delta))
                    delta = getattr(chunk, "contentDelta", None) or getattr(
                        chunk, "content_delta", None
                    )
                    if delta:
                        content_parts.append(str(delta))
                    chunk_usage = _usage_from_chunk(chunk)
                    if chunk_usage:
                        usage = chunk_usage
            else:
                for chunk in stream:
                    delta = getattr(chunk, "contentDelta", None) or getattr(
                        chunk, "content_delta", None
                    )
                    if delta:
                        content_parts.append(str(delta))
                    chunk_usage = _usage_from_chunk(chunk)
                    if chunk_usage:
                        usage = chunk_usage

            try:
                payload = extract_first_json_object("".join(content_parts))
            except Exception as err:
                return {"error": f"风险指标语义匹配结果不是有效 JSON: {err}"}
            return {"model_payload": payload, "reasoning": reasoning, "usage": usage}

        async def validate(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            try:
                result = validate_model_result(
                    payload=state.get("model_payload") or {},
                    registry=registry,
                    allowed_row_ids=state.get("candidate_row_ids") or [],
                    document_text=str(state.get("document_text") or ""),
                    document_name=str(state.get("document_name") or ""),
                    strategy_type=str(state.get("strategy_type") or "未知"),
                )
                return {"result": result.model_dump()}
            except Exception as err:
                return {"error": f"风险指标匹配校验失败: {err}"}

        async def render(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            from app.mandate_risk.models import RiskAnalysisResult

            result = RiskAnalysisResult.model_validate(state.get("result") or {})
            return {"markdown": render_markdown(result, registry)}

        builder = StateGraph(MandateRiskGraphState)
        builder.add_node("prepare", prepare)
        builder.add_node("semantic_judge", semantic_judge)
        builder.add_node("validate", validate)
        builder.add_node("render", render)
        builder.add_edge(START, "prepare")
        builder.add_edge("prepare", "semantic_judge")
        builder.add_edge("semantic_judge", "validate")
        builder.add_edge("validate", "render")
        builder.add_edge("render", END)
        return builder.compile(checkpointer=self._checkpointer)

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        try:
            registry = self._load_registry()
        except Exception as err:
            yield RunFailedEvent(error=str(err))
            return

        document_name, document_text = _extract_document_payload(context.input_val.userMessage)
        initial: MandateRiskGraphState = {
            "document_name": document_name,
            "document_text": document_text,
            "strategy_type": "",
            "strategy_confidence": 0.0,
            "candidate_row_ids": [],
            "candidates": [],
            "model_payload": {},
            "result": {},
            "markdown": "",
            "reasoning": [],
            "usage": {},
            "error": "",
        }

        try:
            thread_id = context.run_id or context.session_id or "mandate-risk"
            result = await self._compile(context, registry).ainvoke(
                initial,
                config={"configurable": {"thread_id": thread_id}},
            )
        except Exception as err:
            yield RunFailedEvent(error=f"风险指标分析失败: {err}")
            return

        if result.get("error"):
            yield RunFailedEvent(error=str(result["error"]))
            return

        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        markdown = str(result.get("markdown") or "")
        if not markdown:
            yield RunFailedEvent(error="风险指标分析未生成有效报告")
            return

        chunk_size = max(64, int(context.message_chunk_chars or 256))
        for chunk in code_point_chunks(markdown, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        yield RunCompletedEvent(output=markdown, usage=result.get("usage") or {})
