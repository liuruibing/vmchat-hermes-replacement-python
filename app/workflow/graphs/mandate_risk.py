# ==============================================================================
# 文件：app/workflow/graphs/mandate_risk.py
# 文件作用：实现 V1 投资委托风险分析，建立候选指标、检查遗漏、请求模型判断并校验报告。
# 全局位置：main.py → Engine（mandate-risk-analysis）→ 本文件的图 → Provider / 指标库 / 校验器。
# 谁调用它：legacy.py 注册实例，WorkflowEngine 按 mandate-risk-analysis id 调用 stream(context)。
# 输入：已解析的 PDF 文本或兼容的文本输入、真实指标目录、角色/Skill 和 Provider。
# 输出：风险指标分析 Markdown、过程说明、用量统计和完成/失败事件。
# 主要流程：prepare → coverage_audit → semantic_judge → validate → render。
# 前端类比：像分阶段的数据处理流水线，state 保存文档、候选、接口响应和校验后的展示数据。
# 边界：LangGraph 控制步骤；候选召回与最终校验由 Python 执行；模型只能在送审资料范围内判断。
# 阅读入口：先看 StateGraph 连线，再看五个节点；stream() 负责读取文档、执行图和发送事件。
# ==============================================================================

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
    # document_loader 是上层传入的回调，类似 props.loadDocument(id)；读取的是已解析文本。
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
    # 不同 Provider 的字段名可能不同，只保留实际报告的字段；缺失不能当成真实的 0 用量。
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
    # 每次调用都报告 total_tokens 才声明统计完整；分别汇总覆盖审计和语义判断两阶段。
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
    # 消费 Provider 的同步/异步片段并拼成完整文本，类似从 ReadableStream 收集一整份响应。
    # usage 取当前调用最后报告的值，避免把同一次调用的累计快照反复相加。
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
    # 校验本次送审候选恰好各出现一次，类似按主键检查接口列表：拒绝未知、重复和漏项。
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
        # a or b 从左到右取第一个真值；这里优先用传入路径，再读环境变量，最后用默认库。
        configured = (
            metric_source_path
            or os.getenv("MANDATE_RISK_METRIC_SOURCE")
            or os.getenv("MANDATE_RISK_METRIC_XLSX")
            or DEFAULT_METRIC_SOURCE
        )
        self.metric_source_path = str(configured)
        # 图状态的内存检查点；不是数据库，也不负责长期保存 PDF 或会话。
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
        # 内部节点是闭包：state 提供中间数据，context / registry 提供本次依赖。
        async def prepare(state: MandateRiskGraphState) -> Dict[str, Any]:
            # 节点返回局部字典更新，类似 store.patch；这里先用确定性 Python 规则建立候选池。
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
            # 两组候选合并后再交给模型，模型后续只能在真实库行与原文条款范围内判断。
            candidates = merge_candidate_sets(primary, fallback)

            return {
                "strategy_type": strategy_type,
                "strategy_confidence": confidence,
                "candidate_row_ids": [item.raw_row_id for item in candidates],
                "candidates": [item.model_dump() for item in candidates],
            }

        async def coverage_audit(state: MandateRiskGraphState) -> Dict[str, Any]:
            # 查漏节点：让模型检查适用目录中有无遗漏，但每个提案仍需绑定真实库行和条款 id。
            if state.get("error"):
                # 此图使用固定边；前一步失败时后续节点仍会进入，但立即跳过自己的业务处理。
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
            # 列表切片类似 array.slice(start, end)；分批控制单次 Prompt 的规模，不是并行请求。
            batches = [
                eligible[index : index + COVERAGE_AUDIT_BATCH_SIZE]
                for index in range(0, len(eligible), COVERAGE_AUDIT_BATCH_SIZE)
            ]
            # 字典推导式建立 clause_id → 条款的索引，类似前端把数组转成按 id 查找的 Map。
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

            # 逐批 await，每批完成才开始下一批；enumerate 同时给出从 1 开始的序号。
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
                    # wait_for 给这一批设超时；超时会取消被等待的任务，与只等待保活的 wait 不同。
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

                # {... for ...} 这里是 set（集合），类似 JS Set，用于去重与快速检查是否属于本批。
                batch_ids = {metric.row_id for metric in batch}
                for proposal in proposed_rows:
                    if not isinstance(proposal, dict):
                        return {"error": "受控覆盖审计包含非对象提案"}
                    raw_row_id = proposal.get("raw_row_id")
                    # Python 的 bool 也是 int 的子类，所以先排除 True/False，才接受整数行号。
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
            # 用行号合并候选；已有行只补条款提示，避免同一指标出现多份候选。
            merged_by_id = {item.raw_row_id: item for item in existing}
            for item in audit_candidates:
                current = merged_by_id.get(item.raw_row_id)
                if current is None:
                    merged_by_id[item.raw_row_id] = item
                    continue
                clause_hints = {hint.clause_id: hint for hint in current.matched_clauses}
                for hint in item.matched_clauses:
                    clause_hints.setdefault(hint.clause_id, hint)
                # model_copy(update=...) 类似 {...current, matched_clauses: ...}，返回新对象。
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
            # 模型判断候选与文档的语义关系，结果先放 model_payload，尚未通过最终业务校验。
            if state.get("error"):
                return {}
            if _is_aborted(context.signal):
                return {"error": "客户端连接已中断"}

            # 从 state 中的字典恢复成 Pydantic 对象，model_validate 在这里执行实际结构校验。
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
            # 最多两次：首次判断 + 一次格式/候选完整性修正；这是节点内部循环，不是图的回边。
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
                # 资料已放进 Prompt，本次禁止额外资源读取和知识检索；Provider 决定模型调用方式。
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
            # Python 用真实库行、条款和原文校验模型答案；图不会自动判断业务正确性。
            if state.get("error"):
                return {}
            try:
                payload = dict(state.get("model_payload") or {})
                payload["matches"] = [dict(item) for item in (payload.get("matches") or [])]
                # 新增召回来源有单独的级别保护：不能直接当作已确认的 DIRECT 匹配。
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
            # 将已校验结果转成 Markdown；这里只排版，不再次调用模型生成报告。
            if state.get("error"):
                return {}
            from app.mandate_risk.models import RiskAnalysisResult

            result = RiskAnalysisResult.model_validate(state.get("result") or {})
            return {"markdown": render_markdown(result, registry)}

        # add_node 注册“名字 → 函数”；每个函数接收 state、返回局部更新。
        builder = StateGraph(MandateRiskGraphState)
        builder.add_node("prepare", prepare)
        builder.add_node("coverage_audit", coverage_audit)
        builder.add_node("semantic_judge", semantic_judge)
        builder.add_node("validate", validate)
        builder.add_node("render", render)
        # 固定边定义五步顺序；遇到业务错误由 error 字段传递，后续节点自行跳过。
        builder.add_edge(START, "prepare")
        builder.add_edge("prepare", "coverage_audit")
        builder.add_edge("coverage_audit", "semantic_judge")
        builder.add_edge("semantic_judge", "validate")
        builder.add_edge("validate", "render")
        builder.add_edge("render", END)
        # compile 只构建可执行的图；下面 ainvoke 才驱动各节点。
        return builder.compile(checkpointer=self._checkpointer)

    async def stream(self, context: WorkflowContext) -> AsyncGenerator[Any, None]:
        # async def 中有 yield 就是异步生成器，调用方用 async for 读取业务事件。
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

        # 本次初始状态：先放 PDF 正文，候选和结果由后续节点填入。
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
            # thread_id 是检查点分组，不是系统线程；ainvoke 完成时拿到整个流程的最终状态。
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

        # 等整张图结束后才交出过程说明与报告；这是业务事件流，不是实时模型 token 转发。
        for sequence, delta in enumerate(result.get("reasoning") or [], start=1):
            yield ReasoningDeltaEvent(delta=str(delta), sequence=sequence)

        markdown = str(result.get("markdown") or "")
        if not markdown:
            yield RunFailedEvent(error="风险指标分析未生成有效报告")
            return

        chunk_size = max(64, int(context.message_chunk_chars or 256))
        for chunk in code_point_chunks(markdown, chunk_size):
            yield MessageDeltaEvent(delta=chunk)

        # 最后发送完成事件，main.py 负责 SSE 序列化、任务状态更新和结果保存。
        yield RunCompletedEvent(output=markdown, usage=result.get("usage") or {})
