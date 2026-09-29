from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any, Dict, List, Sequence, Tuple

from app.mandate_risk.clauses import DocumentClause, split_document_clauses
from app.mandate_risk.json_utils import extract_first_json_object
from app.mandate_risk_v2.coverage import build_coverage_hints, validate_coverage_review
from app.mandate_risk_v2.extractor import (
    build_requirement_ir,
    chunk_clauses,
    validate_extraction_payload,
)
from app.mandate_risk_v2.models import CoverageReview, RequirementIR
from app.mandate_risk_v2.prompts import (
    COVERAGE_SYSTEM_PROMPT,
    EXTRACTION_SYSTEM_PROMPT,
    build_coverage_review_prompt,
    build_extraction_prompt,
)
from app.provider.fixed_provider import ModelSkillRunInput


MODEL_TIMEOUT_SECONDS = 120
EXTRACTION_BATCH_SIZE = 24
EXTRACTION_BATCH_OVERLAP = 2
MAX_REPAIR_ROUNDS = 2


class RequirementCoverageIncomplete(RuntimeError):
    def __init__(self, review: CoverageReview) -> None:
        self.review = review
        missing = ", ".join(item.clause_id for item in review.missing_clauses) or "none"
        partial = ", ".join(item.requirement_id for item in review.partial_requirements) or "none"
        super().__init__(
            "MANDATE_REQUIREMENT_COVERAGE_INCOMPLETE: "
            f"missing_clauses={missing}; partial_requirements={partial}"
        )


@dataclass
class RequirementPipelineResult:
    clauses: List[DocumentClause]
    requirement_ir: RequirementIR
    coverage_review: CoverageReview
    usage: Dict[str, Any]
    extraction_attempts: int


def _is_aborted(signal: Any) -> bool:
    if signal is None:
        return False
    if getattr(signal, "aborted", False):
        return True
    is_set = getattr(signal, "is_set", None)
    return bool(callable(is_set) and is_set())


def _usage_from_chunk(chunk: Any) -> Dict[str, int]:
    raw = getattr(chunk, "usage", None)
    if raw is None:
        return {}
    if not isinstance(raw, dict) and hasattr(raw, "model_dump"):
        raw = raw.model_dump()
    if not isinstance(raw, dict):
        return {}
    result: Dict[str, int] = {}
    aliases = {
        "prompt_tokens": ("prompt_tokens", "input_tokens"),
        "completion_tokens": ("completion_tokens", "output_tokens"),
        "total_tokens": ("total_tokens",),
    }
    for target, keys in aliases.items():
        for key in keys:
            if raw.get(key) is not None:
                result[target] = int(raw[key])
                break
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
                usage = chunk_usage
                usage_reported = True
    else:
        for chunk in stream:
            if _is_aborted(signal):
                raise RuntimeError("客户端连接已中断")
            delta = getattr(chunk, "contentDelta", None) or getattr(chunk, "content_delta", None)
            if delta:
                content_parts.append(str(delta))
            chunk_usage = _usage_from_chunk(chunk)
            if chunk_usage:
                usage = chunk_usage
                usage_reported = True
    return "".join(content_parts), usage, usage_reported


def _aggregate_usage(
    extraction: Sequence[Dict[str, int]],
    extraction_expected: int,
    coverage: Sequence[Dict[str, int]],
    coverage_expected: int,
) -> Dict[str, Any]:
    def phase(reports: Sequence[Dict[str, int]], expected: int):
        complete = len(reports) == expected and all("total_tokens" in report for report in reports)
        reported = {
            key: sum(report.get(key, 0) for report in reports)
            for key in ("prompt_tokens", "completion_tokens", "total_tokens")
            if any(key in report for report in reports)
        }
        return {
            "complete": complete,
            "reported_calls": len(reports),
            "expected_calls": expected,
            "reported_usage": reported or None,
        }

    extraction_phase = phase(extraction, extraction_expected)
    coverage_phase = phase(coverage, coverage_expected)
    complete = extraction_phase["complete"] and coverage_phase["complete"]
    result: Dict[str, Any] = {
        "complete": complete,
        "requirement_extraction": extraction_phase,
        "coverage_review": coverage_phase,
    }
    all_reports = list(extraction) + list(coverage)
    if complete and all_reports:
        for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
            if all(key in report for report in all_reports):
                result[key] = sum(report[key] for report in all_reports)
    return result


class RequirementExtractionPipeline:
    """Phase A: PDF text -> Requirement IR -> explicit coverage gate.

    There is intentionally no metric catalogue dependency in this class. When
    the reviewer finds an omission, the whole document is re-read with the
    review feedback as a hint. The previous IR is discarded rather than patched
    by Python, so semantic repair remains an AI responsibility.
    """

    def __init__(
        self,
        *,
        batch_size: int = EXTRACTION_BATCH_SIZE,
        overlap: int = EXTRACTION_BATCH_OVERLAP,
        timeout_seconds: int = MODEL_TIMEOUT_SECONDS,
        max_repair_rounds: int = MAX_REPAIR_ROUNDS,
    ) -> None:
        self.batch_size = batch_size
        self.overlap = overlap
        self.timeout_seconds = timeout_seconds
        self.max_repair_rounds = max_repair_rounds
        if max_repair_rounds < 0:
            raise ValueError("max_repair_rounds must be >= 0")

    async def _call_model(
        self,
        *,
        provider: Any,
        system_prompt: str,
        user_prompt: str,
        signal: Any,
    ) -> Tuple[dict, Dict[str, int] | None]:
        run_skill = getattr(provider, "run_skill", None) or getattr(provider, "runSkill", None)
        if run_skill is None:
            raise RuntimeError("AI Provider 不支持 Skill 运行")
        run_input = ModelSkillRunInput(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            read_resource=lambda _path: "RESOURCE_NOT_ALLOWED",
            search_knowledge=None,
            signal=signal,
        )
        content, usage, usage_reported = await asyncio.wait_for(
            _collect_skill_output(run_skill, run_input, signal),
            timeout=self.timeout_seconds,
        )
        return extract_first_json_object(content), usage if usage_reported else None

    async def _extract_attempt(
        self,
        *,
        document_name: str,
        windows: Sequence[Sequence[DocumentClause]],
        provider: Any,
        signal: Any,
        review_feedback: dict | None,
        extraction_usage: List[Dict[str, int]],
    ) -> RequirementIR:
        batches = []
        for index, window in enumerate(windows, start=1):
            prompt = build_extraction_prompt(
                document_name=document_name,
                clauses=window,
                batch_index=index,
                batch_count=len(windows),
                review_feedback=review_feedback,
            )
            payload, usage = await self._call_model(
                provider=provider,
                system_prompt=EXTRACTION_SYSTEM_PROMPT,
                user_prompt=prompt,
                signal=signal,
            )
            batches.append(validate_extraction_payload(payload, allowed_clauses=window))
            if usage is not None:
                extraction_usage.append(usage)
        return build_requirement_ir(document_name=document_name, batches=batches)

    async def run(
        self,
        *,
        document_name: str,
        document_text: str,
        provider: Any,
        signal: Any = None,
    ) -> RequirementPipelineResult:
        if _is_aborted(signal):
            raise RuntimeError("客户端连接已中断")
        raw = str(document_text or "").strip()
        if not raw:
            raise ValueError("没有可分析的投资策略文本")

        clauses = split_document_clauses(raw)
        if not clauses:
            raise ValueError("MANDATE_REQUIREMENT_NO_CLAUSES")
        windows = chunk_clauses(clauses, max_clauses=self.batch_size, overlap=self.overlap)

        extraction_usage: List[Dict[str, int]] = []
        coverage_usage: List[Dict[str, int]] = []
        review_feedback: dict | None = None
        final_review: CoverageReview | None = None
        final_ir: RequirementIR | None = None
        attempts = self.max_repair_rounds + 1

        for attempt_index in range(attempts):
            if _is_aborted(signal):
                raise RuntimeError("客户端连接已中断")

            final_ir = await self._extract_attempt(
                document_name=document_name,
                windows=windows,
                provider=provider,
                signal=signal,
                review_feedback=review_feedback,
                extraction_usage=extraction_usage,
            )
            coverage_prompt = build_coverage_review_prompt(
                document_name=document_name,
                clauses=clauses,
                requirement_ir=final_ir,
                coverage_hints=build_coverage_hints(clauses),
            )
            coverage_payload, coverage_usage_item = await self._call_model(
                provider=provider,
                system_prompt=COVERAGE_SYSTEM_PROMPT,
                user_prompt=coverage_prompt,
                signal=signal,
            )
            if coverage_usage_item is not None:
                coverage_usage.append(coverage_usage_item)
            final_review = validate_coverage_review(
                coverage_payload,
                clauses=clauses,
                requirement_ir=final_ir,
            )
            if final_review.complete:
                completed_attempts = attempt_index + 1
                usage = _aggregate_usage(
                    extraction_usage,
                    len(windows) * completed_attempts,
                    coverage_usage,
                    completed_attempts,
                )
                return RequirementPipelineResult(
                    clauses=clauses,
                    requirement_ir=final_ir,
                    coverage_review=final_review,
                    usage=usage,
                    extraction_attempts=completed_attempts,
                )

            review_feedback = final_review.model_dump()

        assert final_review is not None
        raise RequirementCoverageIncomplete(final_review)
