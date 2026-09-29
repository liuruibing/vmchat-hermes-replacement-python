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
EXTRACTION_BATCH_SIZE = 32
EXTRACTION_BATCH_OVERLAP = 6
FULL_DOCUMENT_MAX_CLAUSES = 120
FULL_DOCUMENT_MAX_CHARS = 60_000
MAX_REPAIR_ROUNDS = 2
MAX_COVERAGE_VALIDATION_REPAIRS = 2


class RequirementCoverageIncomplete(RuntimeError):
    def __init__(self, review: CoverageReview) -> None:
        self.review = review
        missing = ", ".join(item.clause_id for item in review.missing_clauses) or "none"
        partial = ", ".join(item.requirement_id for item in review.partial_requirements) or "none"
        unresolved_hints = ", ".join(
            item.clause_id
            for item in review.hint_assessments
            if item.disposition in {"MISSING", "PARTIAL"}
        ) or "none"
        super().__init__(
            "MANDATE_REQUIREMENT_COVERAGE_INCOMPLETE: "
            f"missing_clauses={missing}; partial_requirements={partial}; "
            f"unresolved_hints={unresolved_hints}"
        )


@dataclass
class RequirementPipelineResult:
    clauses: List[DocumentClause]
    requirement_ir: RequirementIR
    coverage_review: CoverageReview
    usage: Dict[str, Any]
    extraction_attempts: int
    extraction_mode: str


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


def choose_extraction_windows(
    clauses: Sequence[DocumentClause],
    *,
    batch_size: int = EXTRACTION_BATCH_SIZE,
    overlap: int = EXTRACTION_BATCH_OVERLAP,
    full_document_max_clauses: int = FULL_DOCUMENT_MAX_CLAUSES,
    full_document_max_chars: int = FULL_DOCUMENT_MAX_CHARS,
) -> Tuple[str, List[List[DocumentClause]]]:
    """Prefer one global AI reading when the Mandate comfortably fits."""

    total_chars = sum(len(clause.text) for clause in clauses)
    if len(clauses) <= full_document_max_clauses and total_chars <= full_document_max_chars:
        return "full_document", [list(clauses)]
    return "chunked", chunk_clauses(clauses, max_clauses=batch_size, overlap=overlap)


class RequirementExtractionPipeline:
    """Phase A: PDF text -> Requirement IR -> explicit coverage gate.

    There is intentionally no metric catalogue dependency in this class. Normal
    sized Mandates are read globally in one semantic pass. Very long documents
    fall back to overlapping windows. Coverage hints are generic recall signals,
    and the reviewer must explicitly dispose every hint. When review finds an
    omission, the document is re-read; Python never patches business semantics.
    Invalid reviewer bookkeeping is retried separately so a malformed COVERED
    reference cannot abort the semantic repair loop.
    """

    def __init__(
        self,
        *,
        batch_size: int = EXTRACTION_BATCH_SIZE,
        overlap: int = EXTRACTION_BATCH_OVERLAP,
        timeout_seconds: int = MODEL_TIMEOUT_SECONDS,
        max_repair_rounds: int = MAX_REPAIR_ROUNDS,
        full_document_max_clauses: int = FULL_DOCUMENT_MAX_CLAUSES,
        full_document_max_chars: int = FULL_DOCUMENT_MAX_CHARS,
    ) -> None:
        self.batch_size = batch_size
        self.overlap = overlap
        self.timeout_seconds = timeout_seconds
        self.max_repair_rounds = max_repair_rounds
        self.full_document_max_clauses = full_document_max_clauses
        self.full_document_max_chars = full_document_max_chars
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
        last_err = None
        for attempt in range(3):
            try:
                content, usage, usage_reported = await asyncio.wait_for(
                    _collect_skill_output(run_skill, run_input, signal),
                    timeout=self.timeout_seconds,
                )
                return extract_first_json_object(content), usage if usage_reported else None
            except Exception as e:
                last_err = e
                err_msg = str(e)
                if ("503" in err_msg or "UNAVAILABLE" in err_msg or "high demand" in err_msg or "502" in err_msg) and attempt < 2:
                    await asyncio.sleep(2.0 * (attempt + 1))
                    continue
                raise e
        raise last_err or RuntimeError("Model call failed after retries")

    async def _extract_attempt(
        self,
        *,
        document_name: str,
        windows: Sequence[Sequence[DocumentClause]],
        provider: Any,
        signal: Any,
        review_feedback: dict | None,
        extraction_usage: List[Dict[str, int]],
    ) -> Tuple[RequirementIR, int]:
        batches = []
        call_count = 0
        for index, window in enumerate(windows, start=1):
            validation_feedback: str | None = None
            for validation_attempt in range(2):
                prompt = build_extraction_prompt(
                    document_name=document_name,
                    clauses=window,
                    batch_index=index,
                    batch_count=len(windows),
                    review_feedback=review_feedback,
                    validation_feedback=validation_feedback,
                )
                payload, usage = await self._call_model(
                    provider=provider,
                    system_prompt=EXTRACTION_SYSTEM_PROMPT,
                    user_prompt=prompt,
                    signal=signal,
                )
                call_count += 1
                if usage is not None:
                    extraction_usage.append(usage)
                try:
                    batches.append(validate_extraction_payload(payload, allowed_clauses=window))
                    break
                except ValueError as exc:
                    if validation_attempt:
                        raise ValueError(f"MANDATE_EXTRACTION_INVALID: {exc}") from exc
                    validation_feedback = str(exc)[:2000]
        return build_requirement_ir(document_name=document_name, batches=batches), call_count

    async def _review_coverage(
        self,
        *,
        document_name: str,
        clauses: Sequence[DocumentClause],
        requirement_ir: RequirementIR,
        coverage_hints: list[dict],
        expected_hint_clause_ids: Sequence[str],
        provider: Any,
        signal: Any,
        coverage_usage: List[Dict[str, int]],
    ) -> Tuple[CoverageReview, int]:
        """Retry only invalid reviewer bookkeeping, without changing Requirement semantics."""

        validation_feedback: str | None = None
        call_count = 0
        for repair_index in range(MAX_COVERAGE_VALIDATION_REPAIRS + 1):
            prompt = build_coverage_review_prompt(
                document_name=document_name,
                clauses=clauses,
                requirement_ir=requirement_ir,
                coverage_hints=coverage_hints,
                validation_feedback=validation_feedback,
            )
            payload, usage = await self._call_model(
                provider=provider,
                system_prompt=COVERAGE_SYSTEM_PROMPT,
                user_prompt=prompt,
                signal=signal,
            )
            call_count += 1
            if usage is not None:
                coverage_usage.append(usage)
            try:
                review = validate_coverage_review(
                    payload,
                    clauses=clauses,
                    requirement_ir=requirement_ir,
                    expected_hint_clause_ids=expected_hint_clause_ids,
                )
            except ValueError as exc:
                if repair_index >= MAX_COVERAGE_VALIDATION_REPAIRS:
                    raise ValueError(f"MANDATE_COVERAGE_REVIEW_INVALID: {exc}") from exc
                validation_feedback = str(exc)[:2000]
                continue
            return review, call_count
        raise RuntimeError("MANDATE_COVERAGE_REVIEW_REPAIR_UNREACHABLE")

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
        extraction_mode, windows = choose_extraction_windows(
            clauses,
            batch_size=self.batch_size,
            overlap=self.overlap,
            full_document_max_clauses=self.full_document_max_clauses,
            full_document_max_chars=self.full_document_max_chars,
        )
        coverage_hints = build_coverage_hints(clauses)
        expected_hint_clause_ids = [str(item["clause_id"]) for item in coverage_hints]

        extraction_usage: List[Dict[str, int]] = []
        extraction_expected_calls = 0
        coverage_usage: List[Dict[str, int]] = []
        coverage_expected_calls = 0
        review_feedback: dict | None = None
        final_review: CoverageReview | None = None
        attempts = self.max_repair_rounds + 1

        for attempt_index in range(attempts):
            if _is_aborted(signal):
                raise RuntimeError("客户端连接已中断")

            final_ir, extraction_calls = await self._extract_attempt(
                document_name=document_name,
                windows=windows,
                provider=provider,
                signal=signal,
                review_feedback=review_feedback,
                extraction_usage=extraction_usage,
            )
            extraction_expected_calls += extraction_calls
            final_review, coverage_calls = await self._review_coverage(
                document_name=document_name,
                clauses=clauses,
                requirement_ir=final_ir,
                coverage_hints=coverage_hints,
                expected_hint_clause_ids=expected_hint_clause_ids,
                provider=provider,
                signal=signal,
                coverage_usage=coverage_usage,
            )
            coverage_expected_calls += coverage_calls
            if final_review.complete:
                completed_attempts = attempt_index + 1
                usage = _aggregate_usage(
                    extraction_usage,
                    extraction_expected_calls,
                    coverage_usage,
                    coverage_expected_calls,
                )
                return RequirementPipelineResult(
                    clauses=clauses,
                    requirement_ir=final_ir,
                    coverage_review=final_review,
                    usage=usage,
                    extraction_attempts=completed_attempts,
                    extraction_mode=extraction_mode,
                )

            review_feedback = final_review.model_dump()

        assert final_review is not None
        raise RequirementCoverageIncomplete(final_review)
