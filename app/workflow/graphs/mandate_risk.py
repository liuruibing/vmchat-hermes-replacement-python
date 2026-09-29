from __future__ import annotations

import asyncio
import os
import re
import time
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
from app.mandate_risk.clauses import split_document_clauses
from app.mandate_risk.matcher import (
    build_candidates,
    build_coverage_audit_candidates,
    build_mandate_recall_candidates,
    infer_strategy_type,
    merge_candidate_sets,
    select_candidates,
)
from app.mandate_risk.models import MetricCandidate
from app.mandate_risk.prompts import (
    COVERAGE_AUDIT_SYSTEM_PROMPT,
    SYSTEM_PROMPT,
    build_coverage_audit_prompt,
    build_semantic_judge_prompt,
)
from app.mandate_risk.registry import RawRiskMetricRegistry
from app.mandate_risk.renderer import render_markdown
from app.mandate_risk.validator import validate_model_result
from app.provider.fixed_provider import ModelSkillRunInput
from app.workflow.engine import WorkflowContext
from app.workflow.graphs.mandate_risk_state import MandateRiskGraphState


DEFAULT_METRIC_SOURCE = "agents/mandate_risk_ai/knowledge/raw/risk_metrics.raw.csv"
COVERAGE_AUDIT_BATCH_SIZE = 24
COVERAGE_AUDIT_TIMEOUT_SECONDS = 120


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    return bool(
        getattr(signal, "aborted", False)
        or getattr(getattr(signal, "signal", None), "aborted", False)
    )


def _extract_document_payload(user_message: str) -> Tuple[str, str]:
    """Legacy text-input fallback retained for API/backward compatibility."""
    raw = str(user_message or "").strip()
    name_match = re.search(r"<document_name>\s*(.*?)\s*</document_name>", raw, re.S | re.I)
    text_match = re.search(r"<document_text>\s*(.*?)\s*</document_text>", raw, re.S | re.I)
    document_name = name_match.group(1).strip() if name_match else "vmChat输入文本"
    document_text = text_match.group(1).strip() if text_match else raw
    return document_name, document_text


def _resolve_uploaded_document(context: WorkflowContext) -> Tuple[str, str]:
    document_ids = list(context.document_ids or getattr(context.input_val, "documentIds", []) or [])
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


def _usage_from_chunk(chunk: Any) -> Dict[str, int]:
    raw = getattr(chunk, "usage", None)
    if raw is None:
        return {}
    if not isinstance(raw, dict) and hasattr(raw, "model_dump"):
        raw = raw.model_dump()
    if not isinstance(raw, dict):
        return {}
    result: Dict[str, int] = {}
    for target, aliases in {
        "prompt_tokens": ("prompt_tokens", "input_tokens"),
        "completion_tokens": ("completion_tokens", "output_tokens"),
        "total_tokens": ("total_tokens",),
    }.items():
        for alias in aliases:
            if alias in raw and raw[alias] is not None:
                result[target] = int(raw[alias])
                break
    return result


def _usage_summary(
    coverage_reports: List[Dict[str, int]],
    coverage_expected: int,
    semantic_reports: List[Dict[str, int]],
    semantic_expected: int,
) -> Dict[str, Any]:
    def phase(reports: List[Dict[str, int]], expected: int) -> Dict[str, Any]:
        reported = {key: sum(item.get(key, 0) for item in reports) for key in (
            "prompt_tokens", "completion_tokens", "total_tokens"
        ) if any(key in item for item in reports)}
        return {
            "complete": len(reports) == expected and all(
                "total_tokens" in item for item in reports
            ),
            "reported_calls": len(reports),
            "expected_calls": expected,
            "reported_usage": reported or None,
        }

    coverage = phase(coverage_reports, coverage_expected)
    semantic = phase(semantic_reports, semantic_expected)
    complete = coverage["complete"] and semantic["complete"]
    result: Dict[str, Any] = {
        "complete": complete,
        "coverage_audit": coverage,
        "semantic_judge": semantic,
    }
    if complete:
        all_reports = coverage_reports + semantic_reports
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if all(key in item for item in all_reports):
                result[key] = sum(item[key] for item in all_reports)
    return result


async def _collect_skill_output(run_skill: Any, run_input: ModelSkillRunInput, signal: Any):
    stream = run_skill(run_input)
    content_parts: List[str] = []
    usage: Dict[str, int] = {}
    usage_reported = False
    if hasattr(stream, "__aiter__"):
        async for chunk in stream:
            if _is_aborted(signal):
                raise RuntimeError("客户端连接已中断")
            delta = getattr(chunk, "contentDelta", None) or getattr(chunk, "content_delta", None)
            if delta:
                content_parts.append(str(delta))
            chunk_usage = _usage_from_chunk(chunk)
            if chunk_usage:
                usage_reported = True
            if chunk_usage:
                usage = chunk_usage
    else:
        for chunk in stream:
            if _is_aborted(signal):
                raise RuntimeError("客户端连接已中断")
            delta = getattr(chunk, "contentDelta", None) or getattr(chunk, "content_delta", None)
            if delta:
                content_parts.append(str(delta))
            chunk_usage = _usage_from_chunk(chunk)
            if chunk_usage:
                usage_reported = True
            if chunk_usage:
                usage = chunk_usage
    return "".join(content_parts), usage, usage_reported


def _candidate_matches_error(
    payload: Dict[str, Any], candidate_row_ids: List[int], registry: RawRiskMetricRegistry
) -> str | None:
    matches = payload.get("matches")
    if not isinstance(matches, list):
        return "matches 字段必须是数组"

    expected_ids = set(candidate_row_ids)
    seen_ids = set()
    for match in matches:
        if not isinstance(match, dict):
            return "matches 中包含非对象项"
        raw_row_id = match.get("raw_row_id")
        if isinstance(raw_row_id, bool) or not isinstance(raw_row_id, int):
            return "matches 中包含无效 raw_row_id"
        row_id = raw_row_id
        if registry.get(row_id) is None:
            return f"matches 中包含未知指标行: {row_id}"
        if row_id not in expected_ids:
            return f"matches 中包含未送审候选行: {row_id}"
        if row_id in seen_ids:
            return f"matches 中候选行重复: {row_id}"
        seen_ids.add(row_id)
        metric = registry.require(row_id)
        if match.get("metric_name") != metric.metric_name:
            return f"raw_row_id {row_id} 的 metric_name 与指标库不符"

    missing_ids = expected_ids - seen_ids
    if missing_ids:
        return "matches 漏掉候选指标行: " + ", ".join(
            str(row_id) for row_id in sorted(missing_ids)
        )
    return None


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
        if not registry.all():
            raise RuntimeError("MANDATE_RISK_METRIC_LIBRARY_INVALID: no metric rows")
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

            # Keep the original high-precision concept matcher as the primary
            # pool. A separate fallback pool may add metrics only through
            # distinctive, authoritative Mandate phrases. This raises recall
            # without weakening the precision semantics of the primary matcher.
            primary = select_candidates(build_candidates(document_text, eligible))
            fallback = select_candidates(
                build_mandate_recall_candidates(document_text, eligible)
            )
            candidates = merge_candidate_sets(primary, fallback)

            return {
                "strategy_type": strategy_type,
                "strategy_confidence": confidence,
                "candidate_row_ids": [item.raw_row_id for item in candidates],
                "candidates": [item.model_dump() for item in candidates],
            }

        async def coverage_audit(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            strategy_type = str(state.get("strategy_type") or "未知")
            eligible = registry.eligible_for_strategy(strategy_type)
            if not eligible:
                return {
                    "coverage_audit_row_ids": [],
                    "coverage_audit_calls": 0,
                    "coverage_audit_usage_reports": [],
                    "coverage_audit_reasoning": ["受控覆盖审计完成：当前策略适用目录为空，未调用模型。"],
                }
            batches = [
                eligible[index : index + COVERAGE_AUDIT_BATCH_SIZE]
                for index in range(0, len(eligible), COVERAGE_AUDIT_BATCH_SIZE)
            ]
            clauses_by_id = {
                clause.clause_id: clause
                for clause in split_document_clauses(str(state.get("document_text") or ""))
            }
            eligible_ids = {metric.row_id for metric in eligible}
            proposals_by_row: Dict[int, List[str]] = {}
            elapsed_ms = 0
            usage_reports: List[Dict[str, int]] = []
            run_skill = getattr(context.provider, "run_skill", None) or getattr(
                context.provider, "runSkill", None
            )
            if run_skill is None:
                return {"error": "AI Provider 不支持 Skill 运行（受控覆盖审计）"}

            for index, batch in enumerate(batches, start=1):
                if _is_aborted(context.signal):
                    return {"error": "客户端连接已中断"}
                prompt = build_coverage_audit_prompt(
                    document_text=str(state.get("document_text") or ""),
                    document_name=str(state.get("document_name") or ""),
                    strategy_type=strategy_type,
                    registry=registry,
                    metrics=batch,
                    batch_index=index,
                    batch_count=len(batches),
                )
                run_input = ModelSkillRunInput(
                    system_prompt=COVERAGE_AUDIT_SYSTEM_PROMPT,
                    user_prompt=prompt,
                    read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
                    search_knowledge=None,
                    signal=context.signal,
                )
                started = time.monotonic()
                try:
                    content, batch_usage, usage_reported = await asyncio.wait_for(
                        _collect_skill_output(run_skill, run_input, context.signal),
                        timeout=COVERAGE_AUDIT_TIMEOUT_SECONDS,
                    )
                except asyncio.TimeoutError:
                    return {"error": f"受控覆盖审计超时：第 {index}/{len(batches)} 批未完成"}
                except Exception as err:
                    return {"error": f"受控覆盖审计调用失败：第 {index}/{len(batches)} 批：{err}"}
                elapsed_ms += round((time.monotonic() - started) * 1000)
                if usage_reported:
                    usage_reports.append(batch_usage)

                try:
                    payload = extract_first_json_object(content)
                except ValueError as err:
                    return {"error": f"受控覆盖审计返回无效 JSON：第 {index}/{len(batches)} 批：{err}"}
                if payload.get("strategy_type") != strategy_type:
                    return {"error": "受控覆盖审计策略类型与 Python 策略不符"}
                proposed_rows = payload.get("proposals")
                if not isinstance(proposed_rows, list):
                    return {"error": "受控覆盖审计 proposals 字段必须是数组"}

                batch_ids = {metric.row_id for metric in batch}
                for proposal in proposed_rows:
                    if not isinstance(proposal, dict):
                        return {"error": "受控覆盖审计包含非对象提案"}
                    raw_row_id = proposal.get("raw_row_id")
                    if isinstance(raw_row_id, bool) or not isinstance(raw_row_id, int):
                        return {"error": "受控覆盖审计包含无效 raw_row_id"}
                    if (
                        raw_row_id not in eligible_ids
                        or raw_row_id not in batch_ids
                        or registry.get(raw_row_id) is None
                    ):
                        return {"error": f"受控覆盖审计包含未知或未送审指标行：{raw_row_id}"}
                    if raw_row_id in proposals_by_row:
                        return {"error": f"受控覆盖审计重复提案指标行：{raw_row_id}"}
                    clause_ids = proposal.get("clause_ids")
                    if (
                        not isinstance(clause_ids, list)
                        or not clause_ids
                        or any(not isinstance(item, str) for item in clause_ids)
                    ):
                        return {"error": f"受控覆盖审计提案缺少有效 clause_id：{raw_row_id}"}
                    if len(set(clause_ids)) != len(clause_ids):
                        return {"error": f"受控覆盖审计提案包含重复 clause_id：{raw_row_id}"}
                    unknown_clause_ids = [item for item in clause_ids if item not in clauses_by_id]
                    if unknown_clause_ids:
                        return {
                            "error": "受控覆盖审计提案包含不存在的 clause_id："
                            + ", ".join(unknown_clause_ids)
                        }
                    proposals_by_row[raw_row_id] = clause_ids

            try:
                audit_candidates = build_coverage_audit_candidates(
                    str(state.get("document_text") or ""), proposals_by_row, eligible
                )
            except Exception as err:
                return {"error": f"受控覆盖审计候选重建失败：{err}"}

            existing = [MetricCandidate.model_validate(item) for item in (state.get("candidates") or [])]
            existing_ids = {item.raw_row_id for item in existing}
            newly_recalled_ids = [item.raw_row_id for item in audit_candidates if item.raw_row_id not in existing_ids]
            merged_by_id = {item.raw_row_id: item for item in existing}
            for item in audit_candidates:
                current = merged_by_id.get(item.raw_row_id)
                if current is None:
                    merged_by_id[item.raw_row_id] = item
                    continue
                clause_hints = {hint.clause_id: hint for hint in current.matched_clauses}
                for hint in item.matched_clauses:
                    clause_hints.setdefault(hint.clause_id, hint)
                merged_by_id[item.raw_row_id] = current.model_copy(
                    update={"matched_clauses": list(clause_hints.values())}
                )
            merged = sorted(
                merged_by_id.values(),
                key=lambda item: (-item.deterministic_score, item.raw_row_id),
            )
            if len(usage_reports) == len(batches) and all(
                "total_tokens" in item for item in usage_reports
            ):
                usage_summary = f"审计各批累计模型 tokens {sum(item['total_tokens'] for item in usage_reports)}"
            elif len(usage_reports) == len(batches):
                usage_summary = "各批均报告 usage，但未提供完整 total_tokens"
            else:
                usage_summary = f"审计 usage 不完整（{len(usage_reports)}/{len(batches)} 批报告 usage）"
            audit_note = (
                f"受控覆盖审计完成：策略适用目录 {len(eligible)} 行，分 {len(batches)} 批，"
                f"提案 {len(audit_candidates)} 行，其中新增召回 {len(newly_recalled_ids)} 行；"
                f"审计耗时 {elapsed_ms} ms；{usage_summary}。"
            )
            return {
                "candidate_row_ids": [item.raw_row_id for item in merged],
                "candidates": [item.model_dump() for item in merged],
                "coverage_audit_row_ids": newly_recalled_ids,
                "coverage_audit_calls": len(batches),
                "coverage_audit_usage_reports": usage_reports,
                "coverage_audit_reasoning": [audit_note],
            }

        async def semantic_judge(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            candidate_models = [
                MetricCandidate.model_validate(item)
                for item in (state.get("candidates") or [])
            ]
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

            reasoning: List[str] = []
            semantic_usage_reports: List[Dict[str, int]] = []
            semantic_calls = 0
            retry_reason = "JSON 不完整"
            for attempt in range(2):
                prompt = user_prompt
                if attempt:
                    prompt += (
                        "\n\n# JSON retry\n上次输出未通过校验："
                        + retry_reason
                        + "。这次请按全部已送审候选行修正并仅输出一个完整 JSON 对象；"
                        "matches 中每个候选 raw_row_id 必须恰好出现一次，"
                        "raw_row_id 与 metric_name 必须对应指标库原行；"
                        "evidence 只写 clause_id，"
                        "不要重复原文、解释或 Markdown。"
                    )
                semantic_calls += 1
                stream = run_skill(
                    ModelSkillRunInput(
                        system_prompt=system_prompt,
                        user_prompt=prompt,
                        read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
                        search_knowledge=None,
                        signal=context.signal,
                    )
                )
                content_parts: List[str] = []
                attempt_usage: Dict[str, int] = {}
                attempt_usage_reported = False
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
                            attempt_usage = chunk_usage
                        if chunk_usage:
                            attempt_usage_reported = True
                else:
                    for chunk in stream:
                        delta = getattr(chunk, "contentDelta", None) or getattr(
                            chunk, "content_delta", None
                        )
                        if delta:
                            content_parts.append(str(delta))
                        chunk_usage = _usage_from_chunk(chunk)
                        if chunk_usage:
                            attempt_usage = chunk_usage
                        if chunk_usage:
                            attempt_usage_reported = True

                if attempt_usage_reported:
                    semantic_usage_reports.append(attempt_usage)

                try:
                    payload = extract_first_json_object("".join(content_parts))
                except ValueError as err:
                    if attempt or str(err) not in {
                        "MODEL_JSON_UNBALANCED",
                        "MODEL_JSON_NOT_FOUND",
                    }:
                        return {"error": f"风险指标语义匹配结果不是有效 JSON: {err}"}
                    retry_reason = "JSON 不完整"
                    continue

                candidate_error = _candidate_matches_error(
                    payload,
                    state.get("candidate_row_ids") or [],
                    registry,
                )
                if candidate_error is None:
                    return {
                        "model_payload": payload,
                        "reasoning": [*(state.get("coverage_audit_reasoning") or []), *reasoning],
                        "usage": _usage_summary(
                            state.get("coverage_audit_usage_reports") or [],
                            state.get("coverage_audit_calls") or 0,
                            semantic_usage_reports,
                            semantic_calls,
                        ),
                    }
                if attempt:
                    return {"error": f"风险指标候选行完整性校验失败: {candidate_error}"}
                retry_reason = candidate_error

            return {"error": "风险指标语义匹配结果不是有效 JSON"}

        async def validate(state: MandateRiskGraphState) -> Dict[str, Any]:
            if state.get("error"):
                return {}
            try:
                payload = dict(state.get("model_payload") or {})
                payload["matches"] = [dict(item) for item in (payload.get("matches") or [])]
                audit_row_ids = set(state.get("coverage_audit_row_ids") or [])
                for match in payload["matches"]:
                    if match.get("raw_row_id") in audit_row_ids and match.get("match_level") == "DIRECT":
                        match["match_level"] = "STRONG_INFERRED"
                        reason = str(match.get("reason") or "").strip()
                        match["reason"] = (
                            reason + "；阶段2受控召回保护：该来源暂不允许 DIRECT，需阶段3单独验证。"
                        ).strip("；")
                candidate_models = [
                    MetricCandidate.model_validate(item)
                    for item in (state.get("candidates") or [])
                ]
                clause_map = {
                    item.raw_row_id: [hint.clause_id for hint in item.matched_clauses]
                    for item in candidate_models
                }
                result = validate_model_result(
                    payload=payload,
                    registry=registry,
                    allowed_row_ids=state.get("candidate_row_ids") or [],
                    document_text=str(state.get("document_text") or ""),
                    document_name=str(state.get("document_name") or ""),
                    strategy_type=str(state.get("strategy_type") or "未知"),
                    candidate_clause_ids=clause_map,
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
        builder.add_node("coverage_audit", coverage_audit)
        builder.add_node("semantic_judge", semantic_judge)
        builder.add_node("validate", validate)
        builder.add_node("render", render)
        builder.add_edge(START, "prepare")
        builder.add_edge("prepare", "coverage_audit")
        builder.add_edge("coverage_audit", "semantic_judge")
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

        try:
            document_name, document_text = _resolve_uploaded_document(context)
        except Exception as err:
            yield RunFailedEvent(error=f"文档读取失败: {err}")
            return

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
